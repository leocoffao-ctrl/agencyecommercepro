# Étude de cas : le projet d'origine

> **À compléter avant publication.** Les lignes marquées `A_COMPLETER` attendent un chiffre réel et sa source. Ne publie pas cette page avec un chiffre estimé : c'est la règle que le kit applique à tous ses livrables.

## Le projet

Coffao (coffao.com) est une boutique Shopify de café de spécialité en coffrets. Le kit est né des skills écrits et ajustés pour la faire tourner : un cerveau de marque partagé, puis un skill par tâche récurrente.

## Ce qui tournait en production

| Tâche | Fréquence | Skill du kit qui en découle |
|---|---|---|
| Articles de blog créés et programmés dans Shopify | `A_COMPLETER` par semaine | `blog-pipeline`, `seo-writer` |
| Audit des posts et plan de la semaine | hebdomadaire | `social-plan` |
| Publication Instagram et LinkedIn | `A_COMPLETER` | `social-publish` |
| Vidéos pixel art avec mascottes | `A_COMPLETER` | `mascot-reels` |
| Pages d'annuaire | `A_COMPLETER` fiches | `directory-pages` |
| Audit SEO et plan d'action | `A_COMPLETER` | `seo-audit` |

## Résultats

| Mesure | Avant | Après | Période | Source |
|---|---|---|---|---|
| Clics organiques par mois | `A_COMPLETER` | `A_COMPLETER` | `A_COMPLETER` | Search Console |
| Articles publiés | `A_COMPLETER` | `A_COMPLETER` | `A_COMPLETER` | Shopify |
| Temps passé par article | `A_COMPLETER` | `A_COMPLETER` | — | estimation, à déclarer comme telle |

## Ce que la généralisation a demandé

1. **Sortir les faits des skills.** Offre, prix, identifiants de comptes et de dossiers, conventions du thème : tout est passé dans `brand-context.md` et `kit.config.json`.
2. **Paramétrer les scripts.** Le domaine, les mots bannis, les seuils et les gabarits étaient écrits en dur ; ils sont lus dans la configuration.
3. **Fusionner les doublons.** Deux skills de fiches (fabricants et lieux) sont devenus un seul, piloté par un type d'entité.
4. **Ouvrir au site vitrine.** Les skills pensés pour une boutique ont reçu une branche « page de service », « demande de devis », « prise de contact ».
5. **Écrire le mode dégradé.** Chaque skill dit ce qu'il fait sans le connecteur payant.
6. **Garder les droits propres.** Mascottes, charte et listes commerciales du projet d'origine restent privées ; le moteur vidéo est livré avec deux personnages de démonstration.
7. **Créditer.** Les skills adaptés de projets open source portent leur attribution, et les licences d'origine sont dans le dépôt.
