#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from typing import Any, Dict, List, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_ADMIN_URL = "https://gestion.innersense.fr/admin/catalogs/{catalog_id}/furnitures"
API_CANDIDATE_URLS = [
    "https://gestion.innersense.fr/api/v7/catalogs/{catalog_id}/furnitures",
    "https://gestion.innersense.fr/api/v7/furnitures",
]


def fetch_page_html(
    catalog_id: int,
    page: int,
    order: str,
    token: str | None,
    cookie: str | None,
    timeout: int,
) -> str:
    params = urlencode({"order": order, "page": page})
    url = f"{BASE_ADMIN_URL.format(catalog_id=catalog_id)}?{params}"
    headers = {"Accept": "text/html"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if cookie:
        headers["Cookie"] = cookie

    req = Request(url=url, headers=headers, method="GET")
    with urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def extract_furniture_ids_from_json(payload: Any) -> List[int]:
    ids: Set[int] = set()
    object_hint_keys = {
        "reference",
        "client_reference",
        "prod_status",
        "published",
        "provider_name",
        "collection_id",
        "furniture_type",
    }

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            # Cas explicite
            fid = value.get("furniture_id")
            if isinstance(fid, int):
                ids.add(fid)
            elif isinstance(fid, str) and fid.isdigit():
                ids.add(int(fid))

            fids = value.get("furniture_ids")
            if isinstance(fids, list):
                for item in fids:
                    if isinstance(item, int):
                        ids.add(item)
                    elif isinstance(item, str) and item.isdigit():
                        ids.add(int(item))

            # Cas objet "furniture-like" avec clé id
            if "id" in value and isinstance(value["id"], int):
                if object_hint_keys.intersection(value.keys()):
                    ids.add(value["id"])

            for sub in value.values():
                walk(sub)
            return

        if isinstance(value, list):
            for item in value:
                walk(item)

    walk(payload)
    return sorted(ids)


def fetch_page_ids_via_api(
    catalog_id: int,
    page: int,
    order: str,
    token: str,
    timeout: int,
) -> Tuple[List[int], str]:
    last_error = "aucun endpoint API compatible"
    for endpoint in API_CANDIDATE_URLS:
        url = endpoint.format(catalog_id=catalog_id)
        query: Dict[str, Any] = {"page": page, "order": order}
        if "catalogs/{catalog_id}/furnitures" not in endpoint:
            query["catalog_id"] = catalog_id
        full_url = f"{url}?{urlencode(query)}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        req = Request(url=full_url, headers=headers, method="GET")
        try:
            with urlopen(req, timeout=timeout) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                payload = json.loads(resp.read().decode(charset, errors="replace"))
                ids = extract_furniture_ids_from_json(payload)
                if ids:
                    return ids, f"api:{endpoint}"
                last_error = f"réponse JSON sans IDs ({endpoint})"
        except HTTPError as e:
            last_error = f"{endpoint} -> HTTP {e.code}"
            continue
        except (URLError, json.JSONDecodeError, ValueError) as e:
            last_error = f"{endpoint} -> {e}"
            continue

    return [], last_error


def extract_furniture_ids(html: str) -> List[int]:
    patterns = [
        # Ligne de tableau ActiveAdmin: <tr ... id="furniture_94469">
        r'id=["\']furniture_(\d+)["\']',
        # Checkboxes de sélection batch
        r'id=["\']batch_action_item_(\d+)["\']',
        r'value=["\'](\d+)["\']\s+class=["\']collection_selection["\']',
        # Liens vers la ressource meuble
        r"/admin/catalogs/\d+/furnitures/(\d+)(?:\b|/|\?)",
        r"/admin/furnitures/(\d+)(?:\b|/|\?)",
        # Fallbacks éventuels
        r'data-id="(\d+)"',
        r'data-resource-id="(\d+)"',
    ]
    ids: Set[int] = set()
    for pattern in patterns:
        for match in re.findall(pattern, html):
            try:
                ids.add(int(match))
            except ValueError:
                continue
    return sorted(ids)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Récupère les furniture-id depuis les pages admin furnitures "
            "et exporte la liste."
        )
    )
    parser.add_argument("--catalog-id", type=int, default=111)
    parser.add_argument("--page-start", type=int, default=1)
    parser.add_argument("--page-end", type=int, default=50)
    parser.add_argument("--order", default="created_at_desc")
    parser.add_argument(
        "--mode",
        choices=["auto", "api", "admin"],
        default="auto",
        help="auto: API puis admin, api: API uniquement, admin: HTML admin uniquement",
    )
    parser.add_argument(
        "--token",
        help="Bearer token (sinon utiliser env INNERSENSE_TOKEN).",
    )
    parser.add_argument(
        "--bearer-token",
        help=(
            "Alias rétrocompatible de --token "
            "(sinon utiliser env INNERSENSE_BEARER_TOKEN)."
        ),
    )
    parser.add_argument(
        "--cookie",
        help="Cookie de session navigateur (fallback, sinon env INNERSENSE_COOKIE).",
    )
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument(
        "--out",
        default="furniture_ids.json",
        help="Fichier JSON de sortie (défaut: furniture_ids.json).",
    )
    parser.add_argument(
        "--csv-out",
        default="furniture_ids.csv",
        help="Fichier CSV de sortie (défaut: furniture_ids.csv).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.page_start < 1 or args.page_end < args.page_start:
        print("Plage de pages invalide.", file=sys.stderr)
        return 1

    token = (
        args.token
        or args.bearer_token
        or os.getenv("INNERSENSE_TOKEN")
        or os.getenv("INNERSENSE_BEARER_TOKEN")
    )
    cookie = args.cookie or os.getenv("INNERSENSE_COOKIE")
    if not token and not cookie:
        print(
            "Authentification manquante. Fournis --token "
            "(ou INNERSENSE_TOKEN / INNERSENSE_BEARER_TOKEN), "
            "ou --cookie (ou INNERSENSE_COOKIE).",
            file=sys.stderr,
        )
        return 1

    by_page: Dict[int, List[int]] = {}
    all_ids: Set[int] = set()
    id_to_pages: Dict[int, List[int]] = defaultdict(list)

    try:
        for page in range(args.page_start, args.page_end + 1):
            ids: List[int] = []
            status_suffix = ""

            use_api = args.mode in ("auto", "api")
            use_admin = args.mode in ("auto", "admin")

            if use_api and token:
                ids, api_status = fetch_page_ids_via_api(
                    catalog_id=args.catalog_id,
                    page=page,
                    order=args.order,
                    token=token,
                    timeout=args.timeout,
                )
                if ids:
                    status_suffix = f" via {api_status}"
                else:
                    status_suffix = f" (API: {api_status})"
                    if args.mode == "api":
                        by_page[page] = ids
                        print(f"page {page}: 0 ids{status_suffix}", file=sys.stderr)
                        continue

            if not ids and use_admin:
                html = fetch_page_html(
                    catalog_id=args.catalog_id,
                    page=page,
                    order=args.order,
                    token=token,
                    cookie=cookie,
                    timeout=args.timeout,
                )
                ids = extract_furniture_ids(html)
                if not ids and "/admin/login" in html:
                    if token and not cookie:
                        status_suffix += (
                            " (redirigé vers /admin/login: le token API seul ne suffit "
                            "probablement pas pour /admin; essaye --cookie)"
                        )
                    else:
                        status_suffix += " (probable session expirée / cookie invalide)"
                elif not ids and 'id="index_table_furnitures"' in html:
                    status_suffix += " (table trouvée mais aucun id extrait)"

            status_msg = f"page {page}: {len(ids)} ids"
            status_msg += status_suffix
            by_page[page] = ids
            for fid in ids:
                all_ids.add(fid)
                id_to_pages[fid].append(page)
            print(status_msg, file=sys.stderr)
    except HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        return 1
    except URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        return 1

    unique_ids = sorted(all_ids)
    result = {
        "catalog_id": args.catalog_id,
        "page_start": args.page_start,
        "page_end": args.page_end,
        "order": args.order,
        "total_unique_furniture_ids": len(unique_ids),
        "total_rows_across_pages": sum(len(v) for v in by_page.values()),
        "furniture_ids": unique_ids,
        "ids_by_page": by_page,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    with open(args.csv_out, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["furniture_id", "pages"])
        for fid in unique_ids:
            pages = ",".join(str(p) for p in sorted(set(id_to_pages[fid])))
            writer.writerow([fid, pages])

    print(
        f"Export terminé: {len(unique_ids)} ids uniques "
        f"-> {args.out}, {args.csv_out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
