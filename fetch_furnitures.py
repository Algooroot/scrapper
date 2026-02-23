#!/usr/bin/env python3
import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL_TEMPLATE = (
    "https://gestion.innersense.fr/api/v7/furnitures/"
    "{furniture_id}/with_defaults_and_configuration_full"
)


def load_payload_from_api(
    furniture_id: int, token: str | None, cookie: str | None, timeout: int
) -> Any:
    url = API_URL_TEMPLATE.format(furniture_id=furniture_id)
    headers = {"Accept": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"
    if cookie:
        headers["Cookie"] = cookie

    req = Request(url=url, headers=headers, method="GET")
    with urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset))


def load_payload_from_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_shade_objects(node: Any) -> List[Dict[str, Any]]:
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


def shade_stats(shades: Iterable[Dict[str, Any]], accessories: List[Dict[str, Any]]) -> Dict[str, Any]:
    shades = list(shades)
    key_counters: Dict[str, Counter] = {}

    for shade in shades:
        for key, val in shade.items():
            if isinstance(val, (str, int, float, bool)) or val is None:
                key_counters.setdefault(key, Counter())[str(val)] += 1

    return {
        "total_shades": len(shades),
        "stats_by_key": {k: dict(v) for k, v in key_counters.items()},
        "accessories_blackout_support": dict(
            Counter(str(a.get("blackout_support")) for a in accessories)
        ),
        "accessories_shade_rotation": dict(
            Counter(str(a.get("shade_rotation")) for a in accessories)
        ),
    }


def build_output(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, list):
        accessories = payload
    elif isinstance(payload, dict):
        accessories = payload.get("accessories", [])
        if not isinstance(accessories, list):
            accessories = []
    else:
        raise ValueError("Le payload JSON n'est ni une liste ni un objet.")

    shades = find_shade_objects(payload)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_accessories": len(accessories),
        "accessories": accessories,
        "shades": shades,
        "shade_stats": shade_stats(shades, accessories),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Récupère les données furniture et exporte accessories + statistiques shades."
        )
    )
    parser.add_argument("--furniture-id", type=int, default=71821)
    parser.add_argument("--token", help="Bearer token (sinon utiliser env INNERSENSE_TOKEN)")
    parser.add_argument("--cookie", help="Cookie session (sinon utiliser env INNERSENSE_COOKIE)")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument(
        "--input-file",
        help="Lit les données depuis un fichier JSON local (utile pour test sans API).",
    )
    parser.add_argument("--out", help="Fichier de sortie JSON. Sinon stdout.")
    parser.add_argument("--pretty", action="store_true", help="JSON indenté.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = args.token or os.getenv("INNERSENSE_TOKEN")
    cookie = args.cookie or os.getenv("INNERSENSE_COOKIE")

    try:
        if args.input_file:
            payload = load_payload_from_file(args.input_file)
        else:
            payload = load_payload_from_api(
                furniture_id=args.furniture_id,
                token=token,
                cookie=cookie,
                timeout=args.timeout,
            )
    except HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        return 1
    except URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Erreur de lecture: {e}", file=sys.stderr)
        return 1

    try:
        result = build_output(payload)
    except Exception as e:
        print(f"Erreur de transformation JSON: {e}", file=sys.stderr)
        return 1

    json_text = json.dumps(
        result, ensure_ascii=False, indent=2 if args.pretty else None
    )

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(json_text)
            if args.pretty:
                f.write("\n")
    else:
        print(json_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
