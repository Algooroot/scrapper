# Ecart des accessoires (excell1.json vs furnitures_accessories_shades_counts.json)

## Resume
- Total `Nbr Accessoire` (excell1.json): **10018**
- Total `total_accessories` (furnitures_accessories_shades_counts.json): **9965**
- Ecart: **53** (excell1.json plus grand)

## Pourquoi cet ecart ?
L ecart provient de quelques noms dont la somme des accessoires ne correspond pas entre les deux fichiers.

## Ou se situe l ecart (par nom)

| Nom (normalise) | Somme excell1 | Somme counts | Ecart |
|---|---:|---:|---:|
| c2,5-2,5 with long seat (l) right | 80 | 66 | +14 |
| 2,5 seater with long seat (l) left | 80 | 66 | +14 |
| 2,5 with long seat (l) right with 1 headrest | 80 | 66 | +14 |
| build your own | 755 | 765 | -10 |
| 3,5 seater with 1 headrest | 80 | 73 | +7 |
| 3,5 seater | 80 | 73 | +7 |
| c2,5-3,5 seater | 80 | 73 | +7 |
| long seat | 75 | 77 | -2 |
| swing table | 2 | 0 | +2 |

## Details par nom (lignes concernees)

### c2,5-2,5 with long seat (l) right (ecart +14)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| C2,5-2,5 with Long Seat (L) right | 1420435 | 19 | 327 |
| C2,5-2,5 with Long Seat (L) right | 1460435 | 17 | 335 |
| C2,5-2,5 with Long Seat (L) right | 1422435 | 22 | 337 |
| C2,5-2,5 with Long Seat (L) right | 1462435 | 22 | 337 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| C2,5-2,5 with Long Seat (L) right | 79227 | 8 | 345 |
| C2,5-2,5 with Long Seat (L) right | 79265 | 22 | 337 |
| C2,5-2,5 with Long Seat (L) right | 79271 | 17 | 335 |
| C2,5-2,5 with Long Seat (L) right | 79278 | 19 | 327 |

### 2,5 seater with long seat (l) left (ecart +14)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| 2,5 seater with Long Seat (L) left | 1420173 | 19 | 327 |
| 2,5 seater with Long Seat (L) left | 1460173 | 17 | 335 |
| 2,5 seater with Long Seat (L) left | 1422173 | 22 | 337 |
| 2,5 seater with Long Seat (L) left | 1462173 | 22 | 337 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| 2,5 seater with Long Seat (L) left | 79228 | 8 | 345 |
| 2,5 seater with Long Seat (L) left | 79266 | 22 | 337 |
| 2,5 seater with Long Seat (L) left | 79272 | 17 | 335 |
| 2,5 seater with Long Seat (L) left | 79279 | 19 | 327 |

### 2,5 with long seat (l) right with 1 headrest (ecart +14)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| 2,5 with Long Seat (L) right with 1 headrest | 1420453 | 19 | 327 |
| 2,5 with Long Seat (L) right with 1 headrest | 1460453 | 17 | 335 |
| 2,5 with Long Seat (L) right with 1 headrest | 1422453 | 22 | 337 |
| 2,5 with Long Seat (L) right with 1 headrest | 1462453 | 22 | 337 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| 2,5 with Long Seat (L) right with 1 headrest | 79226 | 8 | 345 |
| 2,5 with Long Seat (L) right with 1 headrest | 79264 | 22 | 337 |
| 2,5 with Long Seat (L) right with 1 headrest | 79270 | 17 | 335 |
| 2,5 with Long Seat (L) right with 1 headrest | 79277 | 19 | 327 |

### build your own (ecart -10)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| Build your own |  | 80 | 328 |
| Build your own |  | 120 | 329 |
| Build your own |  | 125 | 329 |
| Build your own | Stella_wood | 17 | 335 |
| Build your own | Ella_wood | 15 | 345 |
| Build your own | Emily-wide | 29 | 335 |
| Build your own | Emily-wood | 29 | 334 |
| Build your own | Mary-HR-wood | 10 | 122 |
| Build your own | Mary-HR | 12 | 319 |
| Build your own | Flora-wood | 37 | 304 |
| Build your own | Fiona-steel | 37 | 339 |
| Build your own | Fiona-wood | 28 | 344 |
| Build your own | Flora | 38 | 304 |
| Build your own | Fiona | 37 | 345 |
| Build your own | Ella | 22 | 337 |
| Build your own | Emily | 29 | 281 |
| Build your own | Aurora | 2 | 206 |
| Build your own | Sapphire | 11 | 326 |
| Build your own | Stella | 19 | 327 |
| Build your own | Arion19 A20 | 19 | 327 |
| Build your own | Arion19 A10 | 20 | 327 |
| Build your own | Wave | 19 | 335 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| Build your own | 15924 | 19 | 335 |
| Build your own | 21271 | 20 | 327 |
| Build your own | 21276 | 19 | 327 |
| Build your own | 21636 | 19 | 327 |
| Build your own | 21735 | 11 | 326 |
| Build your own | 22737 | 12 | 206 |
| Build your own | 25541 | 29 | 281 |
| Build your own | 40436 | 22 | 337 |
| Build your own | 48794 | 37 | 345 |
| Build your own | 48831 | 38 | 304 |
| Build your own | 51933 | 28 | 344 |
| Build your own | 51940 | 37 | 339 |
| Build your own | 53122 | 37 | 304 |
| Build your own | 54153 | 12 | 319 |
| Build your own | 54164 | 10 | 122 |
| Build your own | 54172 | 29 | 334 |
| Build your own | 58734 | 29 | 335 |
| Build your own | 73471 | 15 | 345 |
| Build your own | 73472 | 17 | 335 |
| Build your own | 82464 | 125 | 329 |
| Build your own | 82465 | 120 | 329 |
| Build your own | 82466 | 80 | 328 |

### 3,5 seater with 1 headrest (ecart +7)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| 3,5 seater with 1 headrest | 1420499 | 19 | 327 |
| 3,5 seater with 1 headrest | 1460499 | 17 | 335 |
| 3,5 seater with 1 headrest | 1422499 | 22 | 337 |
| 3,5 seater with 1 headrest | 1462499 | 22 | 337 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| 3,5 seater with 1 headrest | 79224 | 15 | 345 |
| 3,5 seater with 1 headrest | 79262 | 22 | 337 |
| 3,5 seater with 1 headrest | 79268 | 17 | 335 |
| 3,5 seater with 1 headrest | 79275 | 19 | 327 |

### 3,5 seater (ecart +7)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| 3,5 seater | 1420172 | 19 | 327 |
| 3,5 seater | 1460172 | 17 | 335 |
| 3,5 seater | 1422172 | 22 | 337 |
| 3,5 seater | 1462172 | 22 | 337 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| 3,5 seater | 79223 | 15 | 345 |
| 3,5 seater | 79261 | 22 | 337 |
| 3,5 seater | 79267 | 17 | 335 |
| 3,5 seater | 79274 | 19 | 327 |

### c2,5-3,5 seater (ecart +7)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| C2,5-3,5 seater | 1420498 | 19 | 327 |
| C2,5-3,5 seater | 1460498 | 17 | 335 |
| C2,5-3,5 seater | 1422498 | 22 | 337 |
| C2,5-3,5 seater | 1462498 | 22 | 337 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| C2,5-3,5 seater | 79225 | 15 | 345 |
| C2,5-3,5 seater | 79263 | 22 | 337 |
| C2,5-3,5 seater | 79269 | 17 | 335 |
| C2,5-3,5 seater | 79276 | 19 | 327 |

### long seat (ecart -2)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| Long Seat | 1468240 | 23 | 328 |
| Long Seat | 1467240 | 26 | 328 |
| Long Seat | 1466240 | 26 | 328 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| Long Seat | 82575 | 27 | 328 |
| Long Seat | 82587 | 27 | 328 |
| Long Seat | 82599 | 23 | 328 |

### swing table (ecart +2)

excell1.json:

| Nom | REF | Nbr Accessoire | Texture |
|---|---|---:|---|
| Stressless® Swing table | 5269013 | 2 | 10 |

furnitures_accessories_shades_counts.json:

| name | furniture_id | total_accessories | total_shades |
|---|---:|---:|---:|
| Stressless® Swing table | 44976 | 0 | 10 |

=========================================================
La différence totale est 10018 − 9965 = 53.
Elle vient d’écarts par nom (après normalisation des noms, ex. retrait de Stressless®). Voici les écarts qui expliquent exactement +53 :

2,5 seater with Long Seat (L) left: +14 (80 vs 66)
2,5 with Long Seat (L) right with 1 headrest: +14 (80 vs 66)
C2,5-2,5 with Long Seat (L) right: +14 (80 vs 66)
3,5 seater: +7 (80 vs 73)
3,5 seater with 1 headrest: +7 (80 vs 73)
C2,5-3,5 seater: +7 (80 vs 73)
Swing table: +2 (2 vs 0)
Long Seat: -2 (75 vs 77)
Build your own: -10 (755 vs 765)
Somme des écarts = +53, donc le total d’excell1.json est plus grand.
=============================================
2,5 seater with Long Seat (L) left: +14 (80 vs 66)
2,5 with Long Seat (L) right with 1 headrest: +14 (80 vs 66)
C2,5-2,5 with Long Seat (L) right: +14 (80 vs 66)
3,5 seater: +7 (80 vs 73)
3,5 seater with 1 headrest: +7 (80 vs 73)
C2,5-3,5 seater: +7 (80 vs 73)
Swing table: +2 (2 vs 0)
Long Seat: -2 (75 vs 77)
Build your own: -10 (755 vs 765)
Somme des écarts = +53, donc le total d’excell1.json est plus grand.

