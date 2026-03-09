# Commande pour récupérer le furniture `59185`

## Avec token dans la commande

```bash
python3 fetch_furnitures.py --furniture-id 59185 --token "TON_BEARER_TOKEN" --pretty --out result_59185.json
```

## Avec variable d'environnement

```bash
export INNERSENSE_TOKEN="TON_BEARER_TOKEN"
python3 fetch_furnitures.py --furniture-id 59185 --pretty --out result_59185.json
```

## Export Excel `.xls` (3 colonnes: name, nbr Accessoir, nbr shade)

```bash
export INNERSENSE_TOKEN="TON_BEARER_TOKEN"
python3 fetch_furnitures.py --furniture-id 59185 --pretty --out result_59185.json --xls-out result_59185.xls
```

## Récupérer tous les `furniture-id` (50 pages admin)

```bash
export INNERSENSE_COOKIE="ae62ba49d4fb8fc83e2f361b96627c6ec9d13c2bb4814fbf544ef3d7451a20ac"
python3 fetch_furniture_ids.py \
  --catalog-id 111 \
  --page-start 1 \
  --page-end 50 \
  --order created_at_desc \
  --out furniture_ids_catalog_111.json \
  --csv-out furniture_ids_catalog_111.csv
```
python3 fetch_furnitures.py --furniture-id 94469 --token "ae62ba49d4fb8fc83e2f361b96627c6ec9d13c2bb4814fbf544ef3d7451a20ac"
 --pretty --out result_94469.json --xls-out result_94469.xls  


 python3 fetch_furnitures.py \
  --furniture-id 94469 \
  --token "ae62ba49d4fb8fc83e2f361b96627c6ec9d13c2bb4814fbf544ef3d7451a20ac" \
  --pretty \
  --out result_94469.json \
  --xls-out result_94469.xls


  python3 fetch_furniture_ids.py \
  --catalog-id 111 \
  --page-start 1 \
  --page-end 50 \
  --order created_at_desc \
  --cookie "..." \
  --out furniture_ids_catalog_111.json \
  --csv-out furniture_ids_catalog_111.csv

  
=======================================================

INNERSENSE_TOKEN='d239822b146915e86321feabbbeba9cc47870e6790c8e075335892d115334634' \
python3 fetch_published_furniture_ids.py \
  --catalog-id 117 \
  --page-start 1 \
  --page-end 100 \
  --mode auto \
  --order created_at_desc \
  --out furniture_ids_catalog_117.json \
  --csv-out furniture_ids_catalog_117.csv
===========================================================================================
INNERSENSE_TOKEN='b5aa721e377e376bc394b8f9254115bddc14acbf21614e88d20608d29ec265f0' \
python3 fetch_furniture_ids.py \
  --catalog-ids 60 198 488 494 228 404 421 195 223 117 \
  --page-start 1 \
  --page-end 50 \
  --mode auto \
  --order created_at_desc \
  --out-dir fichier_json_fourniture_id
================================================
INNERSENSE_TOKEN='d239822b146915e86321feabbbeba9cc47870e6790c8e075335892d115334634' \
python3 fetch_furnitures_counts_batch.py \
  --ids-json ids_228_published.json \
  --timeout 60 \
  --referer "https://gestion.innersense.fr/admin/catalogs/228/furnitures" \
  --xls-out furnitures_accessories_shades_counts_228.xls \
  --json-out furnitures_accessories_shades_counts_228.json \
  --pretty
