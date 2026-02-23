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
