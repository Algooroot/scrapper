#!/usr/bin/env python3
import argparse
import json
from typing import Any, Dict, List, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Supprime les doublons dans ids_by_page et recalcule les compteurs "
            "(total_rows_across_pages, total_unique_furniture_ids, furniture_ids)."
        )
    )
    parser.add_argument(
        "--input",
        default="furniture_ids_catalog_111_published.json",
        help="Fichier JSON source.",
    )
    parser.add_argument(
        "--out",
        default="furniture_ids_catalog_111_published_sans_duplicata.json",
        help="Fichier JSON de sortie.",
    )
    parser.add_argument(
        "--keep-per-page-only",
        action="store_true",
        help=(
            "Supprime uniquement les doublons à l'intérieur d'une page. "
            "Par défaut, supprime aussi les doublons entre pages "
            "(un id gardé sur sa première page)."
        ),
    )
    return parser.parse_args()


def sort_page_keys(ids_by_page: Dict[Any, Any]) -> List[Any]:
    def page_sort_key(key: Any) -> Tuple[int, str]:
        s = str(key)
        if s.isdigit():
            return (0, f"{int(s):09d}")
        return (1, s)

    return sorted(ids_by_page.keys(), key=page_sort_key)


def dedupe_ids_by_page(
    ids_by_page: Dict[Any, Any],
    global_dedupe: bool,
) -> Dict[str, List[int]]:
    result: Dict[str, List[int]] = {}
    seen_global = set()

    for page_key in sort_page_keys(ids_by_page):
        raw_ids = ids_by_page.get(page_key, [])
        if not isinstance(raw_ids, list):
            raw_ids = []

        seen_local = set()
        local_unique: List[int] = []
        for value in raw_ids:
            try:
                fid = int(value)
            except (TypeError, ValueError):
                continue
            if fid in seen_local:
                continue
            seen_local.add(fid)
            local_unique.append(fid)

        if global_dedupe:
            filtered = [fid for fid in local_unique if fid not in seen_global]
            seen_global.update(filtered)
        else:
            filtered = local_unique

        result[str(page_key)] = filtered

    return result


def main() -> int:
    args = parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    ids_by_page = data.get("ids_by_page")
    if not isinstance(ids_by_page, dict):
        raise ValueError("Le JSON ne contient pas 'ids_by_page' valide.")

    original_total_rows = 0
    original_unique = set()
    for values in ids_by_page.values():
        if isinstance(values, list):
            original_total_rows += len(values)
            for v in values:
                try:
                    original_unique.add(int(v))
                except (TypeError, ValueError):
                    pass

    cleaned_ids_by_page = dedupe_ids_by_page(
        ids_by_page=ids_by_page,
        global_dedupe=not args.keep_per_page_only,
    )

    cleaned_unique = sorted({fid for values in cleaned_ids_by_page.values() for fid in values})
    cleaned_total_rows = sum(len(values) for values in cleaned_ids_by_page.values())

    data["ids_by_page"] = cleaned_ids_by_page
    data["furniture_ids"] = cleaned_unique
    data["total_unique_furniture_ids"] = len(cleaned_unique)
    data["total_rows_across_pages"] = cleaned_total_rows
    data["dedupe_summary"] = {
        "mode": "per_page_only" if args.keep_per_page_only else "global_first_page_wins",
        "total_rows_before": original_total_rows,
        "total_rows_after": cleaned_total_rows,
        "removed_rows": original_total_rows - cleaned_total_rows,
        "total_unique_before": len(original_unique),
        "total_unique_after": len(cleaned_unique),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(
        f"OK -> {args.out} | total_rows_across_pages={cleaned_total_rows} | "
        f"total_unique_furniture_ids={len(cleaned_unique)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
