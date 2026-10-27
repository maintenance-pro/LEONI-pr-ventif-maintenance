# Préventif Maintenance 2026

Application de suivi des préventifs des sections Coupe, Cellule sertissage, Pré-assemblage et Surmoulage, construite à partir du planning Excel 2026 : alertes (retards, semaine en cours, semaine prochaine), planning par machine, équipes (techniciens A·S·T et M), affectations, fiche A4 hebdomadaire par technicien, matricules.

- **Application :** https://maintenance-pro.github.io/LEONI-pr-ventif-maintenance/ (aperçu en consultation tant que la base Firebase n'est pas reliée)
- **Application actuelle, pour les saisies :** https://claude.ai/artifact/MLPhKdrM3Rn6cdioj1UZRQ (privée : seules les personnes invitées peuvent l'ouvrir)
- **Mode d'emploi :** [LISEZ-MOI.txt](LISEZ-MOI.txt)

## Contenu

| Fichier | Rôle |
|---|---|
| `index.html` | L'application publiée sur GitHub Pages (version Firebase) |
| `database.rules.json` | Règles de sécurité à coller dans Firebase (Realtime Database › Règles) |
| `planing péventive coupe & préparation 2026.xlsx` | Planning source (une feuille par section) |
| `site/Preventif-2026-hors-ligne.html` | Copie de secours sans internet. Ce qui y est saisi reste dans le navigateur de l'ordinateur et n'apparaît pas en ligne. |
| `site/source/template.html` | Code de l'application (le planning est injecté à la place de `__PLAN_JSON__`) |
| `site/source/parse_plan.py` | Lit l'Excel et produit `plan.json` |
| `site/source/plan.json` | Planning utilisé par la version en ligne actuelle |
| `site/source/build.py` | `plan.json` + `template.html` → pages HTML |
| `site/source/seed.json` | Données reprises de l'application claude.ai à la première connexion du manager |
| `site/preventif.ico` | Icône du raccourci |
| `Exemple fiche A4 - …pdf` | Exemple de fiche hebdomadaire imprimée |

## Refaire le site (par exemple pour le planning 2027)

```
cd site/source
python parse_plan.py "../../<planning>.xlsx" plan.json
python build.py plan.json --firebase firebase-config.json --app-url https://maintenance-pro.github.io/LEONI-pr-ventif-maintenance/
```

`parse_plan.py` a besoin de `openpyxl` (`pip install openpyxl`). `build.py` écrit `index.html` (version Firebase, à copier à la racine du dépôt), `preventif-2026.html` (page claude.ai) et `preventif-2026-standalone.html` (copie hors ligne).

Les identifiants des machines (préfixe de la section + numéro de machine) servent de clé aux saisies : gardez les mêmes numéros d'une année à l'autre.

## Où sont les données saisies

Les préventifs faits ou reportés, les modifications du planning, l'organisation (sections, TL, techniciens) et les matricules sont enregistrés dans la base de l'application en ligne (Firebase Realtime Database une fois reliée), **pas dans ce dépôt**. Les comptes se créent sur la page de connexion (e-mail ou matricule) et sont autorisés par le manager dans Réglages › Comptes.
