
# Documentation d'utilisation

## Étape 1 : Récupérer le token d'authentification

Avant de commencer, il faut d'abord installer `Python 3` sur votre machine, car les scripts de cette documentation s'exécutent avec `python3`.

Pour récupérer le token d'authentification, ouvrez la liste d'un catalogue dans l'interface Innersense, par exemple :

`https://gestion.innersense.fr/admin/catalogs/118`

Ensuite :

1. Filtrez la liste sur le STATUS `Published`.
2. Faites un clic droit, puis choisissez `Inspecter`.
3. Ouvrez l'onglet `Network`.
4. Dans la recherche du panneau `Network`, tapez `with`.
5. Rechargez ou laissez charger la liste.
6. Sélectionnez la requête concernée par le bouttom 3D.
7. Ouvrez l'onglet `Headers`.
8. Repérez la ligne `Authorization`.
9. Copiez la valeur située après le mot `Bearer`.

Cette valeur correspond au token à utiliser dans les commandes des étapes suivantes.

## Étape 2 : Récupérer la liste des IDs de fournitures

Placez-vous d'abord dans le dossier du script depuis le terminal. Dans mon cas


cd /var/www/html/scrappe_data_picolino


Lancez ensuite la commande suivante :



INNERSENSE_TOKEN='b50fc5d5ee14431d0181fa26804d014e1270cead3b4821b8ec1ba109afe455bf' \
python3 fetch_published_furniture_ids.py \
  --catalog-id 111 \
  --page-start 1 \
  --page-end 100 \
  --mode auto \
  --order created_at_desc \
  --out furniture_ids_catalog_111.json
  


Explications :

- `INNERSENSE_TOKEN` doit contenir le token récupéré à l'étape 1.
- `--catalog-id 117` correspond à l'identifiant du catalogue.
- Si vous travaillez sur le catalogue `https://gestion.innersense.fr/admin/catalogs/118`, alors il faut utiliser `--catalog-id 118`.
- `--out furniture_ids_catalog_117.json` permet de choisir le nom du fichier JSON généré.


Exemple de personnalisation :

- `--out liste_fournitures_catalogue_118.json`


Après avoir appuyé sur Entrée, le script démarre et génère la liste des IDs des fournitures publiées.

## Étape 3 : Générer le fichier Excel avec les accessoires et les shades

Une fois le fichier JSON des IDs récupéré, lancez la commande suivante :


python3 fetch_furnitures_counts_batch.py \
  --ids-json furniture_ids_catalog_111.json \
  --token "b50fc5d5ee14431d0181fa26804d014e1270cead3b4821b8ec1ba109afe455bf" \
  --xls-out furnitures_accessories_shades_counts_11_1.xls \
  --pretty


Explications :

- `--token` doit contenir le token récupéré à l'étape 1.
- `--ids-json furniture_ids_catalog_195.json` doit contenir le nom du fichier JSON généré à l'étape 2.
- `--xls-out furnitures_accessories_shades_counts_195_1.xls` permet de choisir le nom du fichier Excel généré.

Ce script génère un fichier Excel contenant les informations de comptage des accessoires et des shades pour les fournitures listées dans le fichier JSON.
