#!/usr/bin/env python3
import argparse
import html
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL_TEMPLATE = (
    "https://gestion.innersense.fr/api/v7/furnitures/"
    "{furniture_id}/with_defaults_and_configuration_full"
)


def load_ids_from_json(path: str) -> List[int]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ids = data.get("furniture_ids", [])
    if not isinstance(ids, list):
        raise ValueError("Le champ 'furniture_ids' est absent ou invalide.")

    out: List[int] = []
    seen = set()
    for value in ids:
        fid = int(value)
        if fid in seen:
            continue
        seen.add(fid)
        out.append(fid)
    return out


def load_payload_from_api(
    furniture_id: int,
    token: str | None,
    cookie: str | None,
    timeout: int,
    user_agent: str | None,
    referer: str | None,
) -> Any:
    url = API_URL_TEMPLATE.format(furniture_id=furniture_id)
    headers = {"Accept": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"
    if cookie:
        headers["Cookie"] = cookie
    if user_agent:
        headers["User-Agent"] = user_agent
    if referer:
        headers["Referer"] = referer

    req = Request(url=url, headers=headers, method="GET")
    with urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset))


def find_shades(node: Any) -> List[Dict[str, Any]]:
    shades: List[Dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, sub in value.items():
                key_l = key.lower()
                if key_l == "shades" and isinstance(sub, list):
                    for item in sub:
                        if isinstance(item, dict):
                            shades.append(item)
                elif "shade" in key_l and isinstance(sub, dict):
                    shades.append(sub)
                walk(sub)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(node)
    return shades


def count_accessories(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        accessories = payload.get("accessories", [])
        if isinstance(accessories, list):
            return len(accessories)
    return 0


def count_shades(payload: Any) -> int:
    if isinstance(payload, dict) and isinstance(payload.get("shades"), list):
        return len(payload["shades"])
    return len(find_shades(payload))


def get_name(payload: Any, furniture_id: int) -> str:
    if isinstance(payload, dict):
        furniture = payload.get("furniture")
        if isinstance(furniture, dict) and furniture.get("name"):
            return str(furniture["name"])
        if payload.get("name"):
            return str(payload["name"])
    return f"furniture_{furniture_id}"


def export_xls(path: str, rows: List[Dict[str, Any]]) -> None:
    total_accessories = sum(
        int(r["total_accessories"]) for r in rows if r.get("status") == "ok"
    )
    total_shades = sum(
        int(r["total_shades"]) for r in rows if r.get("status") == "ok"
    )
    total_ok = sum(1 for r in rows if r.get("status") == "ok")
    total_error = sum(1 for r in rows if r.get("status") != "ok")

    html_rows = []
    for r in rows:
        html_rows.append(
            "<tr>"
            f"<td>{int(r['furniture_id'])}</td>"
            f"<td>{html.escape(str(r.get('name') or ''))}</td>"
            f"<td>{int(r.get('total_accessories', 0))}</td>"
            f"<td>{int(r.get('total_shades', 0))}</td>"
            f"<td>{html.escape(str(r.get('status') or ''))}</td>"
            f"<td>{html.escape(str(r.get('error') or ''))}</td>"
            "</tr>"
        )

    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Furniture Batch Export</title>
</head>
<body>
<table border="1">
  <tr>
    <th>furniture_id</th>
    <th>name</th>
    <th>nbr Accessoir</th>
    <th>nbr shade</th>
    <th>status</th>
    <th>error</th>
  </tr>
  {''.join(html_rows)}
  <tr>
    <td colspan="2"><b>TOTAL (status=ok)</b></td>
    <td><b>{total_accessories}</b></td>
    <td><b>{total_shades}</b></td>
    <td><b>ok={total_ok}</b></td>
    <td><b>error={total_error}</b></td>
  </tr>
</table>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_doc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Itère sur un fichier de furniture_ids, appelle l'API et exporte les "
            "comptes accessories/shades dans un fichier .xls."
        )
    )
    parser.add_argument(
        "--ids-json",
        default="furniture_ids_catalog_111_published_sans_duplicata_sans_kite.json",
        help="Fichier JSON contenant 'furniture_ids'.",
    )
    parser.add_argument("--token", help="Bearer token (sinon env INNERSENSE_TOKEN)")
    parser.add_argument("--cookie", help="Cookie session (sinon env INNERSENSE_COOKIE)")
    parser.add_argument(
        "--cookie-file",
        help="Fichier texte contenant la valeur brute du header Cookie.",
    )
    parser.add_argument(
        "--user-agent",
        default=(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        help="User-Agent HTTP pour les requêtes API.",
    )
    parser.add_argument(
        "--referer",
        default="https://gestion.innersense.fr/admin/catalogs/111/furnitures",
        help="Referer HTTP pour les requêtes API.",
    )
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument(
        "--xls-out",
        default="furnitures_accessories_shades_counts.xls",
        help="Fichier .xls de sortie (tableau Excel HTML).",
    )
    parser.add_argument(
        "--json-out",
        help="Fichier JSON détaillé de sortie (optionnel).",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Formate le JSON de sortie (si --json-out est utilisé).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = args.token or os.getenv("INNERSENSE_TOKEN")
    cookie = args.cookie or os.getenv("INNERSENSE_COOKIE")
    if args.cookie_file:
        try:
            with open(args.cookie_file, "r", encoding="utf-8") as f:
                cookie = f.read().strip()
        except Exception as e:
            print(f"Erreur lecture cookie-file: {e}", file=sys.stderr)
            return 1

    try:
        furniture_ids = load_ids_from_json(args.ids_json)
    except Exception as e:
        print(f"Erreur lecture ids: {e}", file=sys.stderr)
        return 1

    rows: List[Dict[str, Any]] = []
    total = len(furniture_ids)

    for idx, furniture_id in enumerate(furniture_ids, start=1):
        print(f"[{idx}/{total}] furniture_id={furniture_id}", file=sys.stderr)
        row: Dict[str, Any] = {
            "furniture_id": furniture_id,
            "name": None,
            "total_accessories": 0,
            "total_shades": 0,
            "status": "ok",
            "error": None,
        }
        try:
            payload = load_payload_from_api(
                furniture_id=furniture_id,
                token=token,
                cookie=cookie,
                timeout=args.timeout,
                user_agent=args.user_agent,
                referer=args.referer,
            )
            row["name"] = get_name(payload, furniture_id)
            row["total_accessories"] = count_accessories(payload)
            row["total_shades"] = count_shades(payload)
        except HTTPError as e:
            row["status"] = "error"
            row["error"] = f"HTTP {e.code}: {e.reason}"
        except URLError as e:
            row["status"] = "error"
            row["error"] = f"Network: {e.reason}"
        except Exception as e:
            row["status"] = "error"
            row["error"] = str(e)
        rows.append(row)

    export_xls(args.xls_out, rows)

    if args.json_out:
        result = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_ids_json": args.ids_json,
            "total_ids": total,
            "total_ok": sum(1 for r in rows if r["status"] == "ok"),
            "total_error": sum(1 for r in rows if r["status"] != "ok"),
            "sum_accessories_ok": sum(
                int(r["total_accessories"]) for r in rows if r["status"] == "ok"
            ),
            "sum_shades_ok": sum(
                int(r["total_shades"]) for r in rows if r["status"] == "ok"
            ),
            "items": rows,
        }
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2 if args.pretty else None)
            if args.pretty:
                f.write("\n")

    total_ok = sum(1 for r in rows if r["status"] == "ok")
    total_error = len(rows) - total_ok
    total_401 = sum(
        1
        for r in rows
        if r.get("status") == "error" and "HTTP 401" in str(r.get("error"))
    )

    print(f"OK -> {args.xls_out}", file=sys.stderr)
    if args.json_out:
        print(f"OK -> {args.json_out}", file=sys.stderr)
    if total_ok == 0 and total_error > 0 and total_401 == total_error:
        print(
            "AUTH ERROR: toutes les requêtes API sont en 401. "
            "Passe un --token valide ou un --cookie/--cookie-file valide.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
