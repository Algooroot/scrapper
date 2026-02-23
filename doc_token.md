# Récupérer `TON_BEARER_TOKEN` depuis le navigateur

## Prérequis

- Être déjà connecté sur `https://gestion.innersense.fr`.

## Étapes (Chrome / Edge)

1. Ouvre la page `https://gestion.innersense.fr`.
2. Appuie sur `F12` pour ouvrir les DevTools.
3. Va dans l'onglet `Network` (Réseau).
4. Recharge la page (`Ctrl+R`).
5. Dans la liste des requêtes, clique une requête API, par exemple :
   `https://gestion.innersense.fr/api/v7/furnitures/22751/with_defaults_and_configuration_full`
6. Va dans `Headers` > `Request Headers`.
7. Trouve la ligne :
   `authorization: Bearer xxxxxxxxx`
8. Copie la valeur après `Bearer `.
   Cette valeur est `TON_BEARER_TOKEN`.

## Étapes (Firefox)

1. `F12` > onglet `Réseau`.
2. Recharge la page.
3. Clique une requête `api/v7/...`.
4. Dans `En-têtes de requête`, copie la valeur de `Authorization: Bearer ...`.

## Utilisation du token

```bash
python3 fetch_furnitures.py --furniture-id 59185 --token "TON_BEARER_TOKEN" --pretty --out result_59185.json
```

## Important (sécurité)

- Ne partage jamais ce token publiquement.
- Si le token fuit, révoque-le / régénère-le.
