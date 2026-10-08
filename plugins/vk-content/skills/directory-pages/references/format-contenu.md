# Format du contenu (JSON) attendu par `build_fiche.py`

Un fichier `contenu-<slug>.json` par fiche. Les textes acceptent du HTML en ligne (`<a>`, `<strong>`, `<br>`). Exemple complet : `exemple-contenu.json`.

## Champs racine

| Clé | Rôle |
|---|---|
| `type` | Clé de `directory.types` dans `kit.config.json` (page pivot, préfixe d'URL, seuils) |
| `slug`, `nom` | Slug de la fiche, graphie canonique de l'entité |
| `date_releve` | `JJ/MM/AAAA`, date du relevé des données |
| `meta_title`, `meta_description`, `schema_headline` | Métadonnées (60 et 155 caractères au plus) |
| `hero_url`, `alt_hero` | Image d'en-tête ; sans `hero_url`, une note part dans le fichier de livraison |
| `sous_titre`, `ligne_donnees`, `badges` | En-tête. `badges` = `[texte, classe]` (`vk-badge--partenaire`, `vk-badge--verif`) |
| `reponse_rapide` | Six puces autonomes |
| `infos` | Cartes `{titre, lignes[], place_id?, maps_label?}` |
| `sections` | Voir ci-dessous |
| `test_maison` | `{h2, p[]}` ou `null` : bloc 10, supprimé s'il n'y a pas de relevé avec protocole |
| `faq` | Huit paires `[question, réponse]` |
| `etat_encart` | `A` non revendiquée, `B` revendiquée, `C` partenaire |
| `encart_texte`, `encart_cta` | Texte libre de l'encart, bouton `[url, libellé]` |
| `sources` | Liste des sources datées |
| `prochaine_revision` | Sinon `directory.next_review` |
| `decouvre_texte`, `decouvre_boutons` | Bloc 20, boutons `[url, libellé]` |
| `schema_about` | Propriétés ajoutées à `about` (`url`, `sameAs`, `address`) |
| `labels` | Surcharge des libellés fixes (sommaire, encart, sources) |

## `sections`

| Clé | Bloc | Contenu |
|---|---|---|
| `identite` | 06 Présentation | `{h2, p[]}` |
| `specialite` | 07 Spécialité | `{h2, p[], echelle_labels[3]?, actif?, note_echelle?}`. `actif` = index, liste d'index ou `null` |
| `offre` | 08 Offre | `{h2, p[], entetes[], lignes[][], releve}` |
| `decision` | 09 Décision | `{h2, p[], entetes[3], lignes[][3]}` |
| `prix` | 11 Ce que ça vaut | `{h2, p[], jauge?[[libellé, min, max, texte]], echelle_max?, unite?, note_jauge?}`. La première ligne de la jauge est l'entité |
| `transparence` | 12 À qui ça ne convient pas | `{h2, intro, items[[titre, texte]]}` |
| `acces` | 13 Accès | `{h2, intro, items[[titre, texte]], outro[]?}` |
| `comparatif` | 14 Comparatif | `{h2, intro, entetes[], lignes[][], outro}` |
| `avis` | 15 Avis | `{h2, note, p[]}` |
| `alternatives` | 17 Alternatives | `{h2?, intro, liste[[slug, nom, description]]}` |

## Sorties

- `fiche-<slug>.html` : corps de l'article, sans `<style>` ni commentaire.
- `schema-<slug>.json` : `Article` (avec `about`), `BreadcrumbList`, `FAQPage`, `ItemList`.
- `livraison-<slug>.md` : URL cible, métadonnées, consignes d'intégration, notes (image manquante, bloc supprimé, état de l'encart).

## Adapter les libellés à un type d'entité

Pour un lieu, surcharge par exemple dans `directory.labels` ou dans `labels` :

```json
{"som_specialite": "Ce qu'on y sert", "som_offre": "Carte et prix", "som_decision": "Pour quelle occasion",
 "som_transparence": "Ce qui peut déranger", "som_acces": "Y aller", "alternatives_h2": "Quelles adresses ressemblent à {n} ?"}
```
