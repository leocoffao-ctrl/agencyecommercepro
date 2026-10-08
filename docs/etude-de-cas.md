# Étude de cas : le projet d'origine

Coffao (coffao.com) est une boutique Shopify de café de spécialité vendu en coffrets. Le kit est né des skills écrits pour la faire tourner : un cerveau de marque partagé, puis un skill par tâche récurrente.

Les chiffres ci-dessous ont été relevés le 08/10/2026 dans l'admin Shopify, dans les livrables archivés des exécutions et dans deux audits datés. Chaque ligne indique sa source. Les chiffres de trafic de la Search Console manquent : ils ne sont pas disponibles avec le plan d'outil utilisé, et je ne les ai pas estimés.

## Ce qui tourne en production

| Tâche | Volume constaté | Source | Skill du kit qui en découle |
|---|---|---|---|
| Articles éditoriaux SEO + GEO (méthode `seo-writer`) | 16 articles publiés du 29/08 au 30/09/2026, environ un tous les deux jours à partir du 1er septembre | Shopify, blog Guides, dates de publication | `seo-writer` |
| Articles créés et programmés par le pipeline automatique | 9 articles créés lors de deux exécutions (1er et 7 octobre) : 3 publiés, 6 programmés du 9 au 19 octobre, un tous les deux jours | Shopify, blog Guides | `blog-pipeline` |
| Fiches café (une par lot de café) | 41 fiches publiées fin juillet et début août 2026 | Shopify, blog Guides | `directory-pages` (gabarit de fiche) |
| Pages d'annuaire | 68 fiches de lieux et 35 fiches de fabricants publiées en 2026 | Shopify, blogs Coffee Shops et Torréfacteurs | `directory-pages` |
| Contenu total | 193 articles sur trois blogs | Shopify | — |
| Audit SEO technique et plan d'action | 247 pages crawlées, 33 actions priorisées, dont 8 critiques | Feuille « Audit — Missions », 18/09/2026 | `seo-audit` |
| Plan réseaux hebdomadaire | Audit des 90 derniers jours puis 4 posts Instagram + LinkedIn programmés pour la semaine suivante | Document de consignes du 05/10/2026 | `social-plan`, `social-publish` |
| Vidéos pixel art avec mascottes | 2 Reels publiés sur 90 jours | Même document | `mascot-reels` |

## Ce que les contrôles automatiques ont attrapé

Le récapitulatif d'une exécution du pipeline (4 octobre 2026) montre le kit au travail :
- trois articles contrôlés, code de sortie 0, tous les liens internes vérifiés en 200 ;
- un titre de sujet corrigé avant publication : « 3 recettes testées » est devenu « trois recettes publiées », parce que rien n'avait été testé ;
- les sources à recontrôler listées une par une : source unique, copie tierce d'une étude, texte réglementaire lu dans une autre version ;
- quatre anomalies signalées sur des pages déjà en ligne, dont une affirmation de note de qualité sans dire qui l'avait attribuée ;
- 0 $ dépensé : le compte de données était à sec, et le pipeline a continué en mode dégradé en le disant.

## Résultats mesurés

| Mesure | Août 2026 | Septembre 2026 | Source |
|---|---|---|---|
| Mots-clés positionnés sur Google France | 15 | 47 | DataForSEO, audit du 08/09/2026 |
| Trafic organique estimé (visites par mois) | 59,5 | 305,9 | Même audit, estimation de l'outil |
| Mots-clés en première page | — | 8 | Même audit |
| Mots-clés en deuxième page | — | 23 (volume cumulé de 51 840 recherches par mois) | Même audit |

Ce que ces chiffres disent, et ce qu'ils ne disent pas :
- La progression vient des pages d'annuaire : 85 % du trafic estimé provenait de six fiches consacrées à des marques et à des lieux tiers. C'est la mécanique que décrit `directory-pages`.
- Le trafic estimé est un modèle de DataForSEO, pas une mesure de la Search Console.
- Au 08/09/2026, aucun mot-clé n'était dans le top 3, aucune page produit ne se classait sur une requête commerciale, et le profil de liens entrants était jugé toxique. L'audit l'écrit, et ce sont les actions critiques qui en sont sorties.
- Les réseaux sociaux démarrent : 6 posts par plateforme sur 90 jours, une portée médiane de 34 sur Instagram et de 52 sur LinkedIn. Moins de dix posts : l'audit décrit, il ne conclut pas. C'est la règle d'honnêteté de `social-plan`.

| Mesure à ajouter | Source |
|---|---|
| Clics et impressions organiques avant et après septembre 2026 | Search Console, export direct (`A_COMPLETER`) |

## Ce que la généralisation a demandé

1. **Sortir les faits des skills.** Offre, prix, identifiants de comptes et de dossiers, conventions du thème : tout est passé dans `brand-context.md` et `kit.config.json`.
2. **Paramétrer les scripts.** Le domaine, les mots bannis, les seuils et les gabarits étaient écrits en dur ; ils sont lus dans la configuration.
3. **Fusionner les doublons.** Deux skills de fiches (fabricants et lieux) sont devenus un seul, piloté par un type d'entité.
4. **Ouvrir au site vitrine.** Les skills pensés pour une boutique ont reçu une branche pour la page de service, la demande de devis et la prise de contact.
5. **Écrire le mode dégradé.** Chaque skill dit ce qu'il fait sans le connecteur payant, comme le pipeline l'a fait en production quand le compte de données était vide.
6. **Garder les droits propres.** Les mascottes, la charte et les listes commerciales du projet d'origine restent privées ; le moteur vidéo est livré avec deux personnages de démonstration.
7. **Créditer.** Les skills adaptés de projets open source portent leur attribution, et les licences d'origine sont dans le dépôt.
