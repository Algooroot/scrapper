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

  
