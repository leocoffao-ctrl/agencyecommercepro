---
name: seo-data
description: Pont entre les skills SEO et le connecteur DataForSEO — quel outil appeler pour quelle question, paramètres de pays et de langue obligatoires, coûts et garde-fou « demander avant de dépenser ». À utiliser avant tout appel DataForSEO et dès que l'utilisateur parle de volume de recherche, de difficulté de mot-clé, de SERP, de positions, de concurrents organiques, de visibilité dans ChatGPT ou les IA, de mentions de marque dans les LLM ou de Google Shopping, même s'il ne nomme pas DataForSEO.
---

# Données SEO — DataForSEO sous garde-fou

Adapté de `AgriciDaniel/claude-seo/skills/seo-dataforseo` (MIT). Le dépôt d'origine pilote un budget avec des scripts locaux. Ici, le garde-fou est une règle de conduite, applicable partout où le connecteur tourne.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## Règle 1 — Toujours le pays et la langue du projet

Les outils du connecteur ont souvent `location_name: "United States"` et `language_code: "en"` par défaut. Sur **chaque** appel, passe explicitement les valeurs du contexte §10 (reprises dans `kit.config.json`, bloc `seo`) :

```
location_name: "<pays du projet>"
language_code: "<langue du projet>"
```

Un résultat obtenu sans ces deux paramètres est faux pour le projet : jette-le et relance.

## Règle 2 — Demander avant de dépenser

Avant une série d'appels, annonce : outils prévus, nombre d'appels, coût estimé (grille `references/couts.md`). Ensuite :

- Total estimé inférieur ou égal au seuil `seo.ask_above_usd` (0,10 $ par défaut) : vas-y et indique le coût dans le livrable.
- Au-dessus : attends l'accord.
- Toujours demander pour : le scraper ChatGPT, les outils de mentions LLM, `backlinks_backlinks`, `backlinks_domain_intersection`, les outils marchands, tout appel avec `limit` supérieur à 100.
- En tâche planifiée, le plafond est `seo.run_budget_usd`. Atteint : on s'arrête et on le note.

Économies : regrouper les mots-clés dans un seul appel de volume, ne jamais relancer une requête déjà faite dans la conversation, commencer avec un `limit` bas (10 à 20).

## Règle 3 — Le bon outil pour la bonne question

| Question | Outil |
|---|---|
| Volume d'une liste de mots-clés | `kw_data_google_ads_search_volume` |
| Idées autour d'un mot-clé | `dataforseo_labs_google_keyword_ideas`, `_keyword_suggestions`, `_related_keywords` |
| Difficulté d'une liste | `dataforseo_labs_bulk_keyword_difficulty` |
| Intention de recherche | `dataforseo_labs_search_intent` |
| Qui est en première page aujourd'hui | `serp_organic_live_advanced` |
| Mots-clés sur lesquels le domaine se positionne | `dataforseo_labs_google_ranked_keywords` |
| Vue d'ensemble d'un domaine | `dataforseo_labs_google_domain_rank_overview` |
| Concurrents organiques | `dataforseo_labs_google_competitors_domain` |
| Mots-clés d'un concurrent absents chez nous | `dataforseo_labs_google_domain_intersection` avec `intersections: false` |
| Pages qui performent | `dataforseo_labs_google_relevant_pages` |
| Ce que répond ChatGPT à une question | `ai_optimization_chat_gpt_scraper` (`force_web_search: true`) |
| La marque est-elle citée par les IA | `ai_opt_llm_ment_search`, `_agg_metrics` |
| Domaines cités par les IA sur un sujet | `ai_opt_llm_ment_top_domains`, `_top_pages` |
| La marque face à ses concurrents dans les IA | `ai_opt_llm_ment_cross_agg_metrics` |
| Analyse technique d'une page | `on_page_instant_pages`, `on_page_lighthouse` |
| Saisonnalité | `kw_data_google_trends_explore` |

Avant le premier appel aux outils IA, vérifie que le pays et la langue du projet sont couverts (`ai_opt_llm_ment_loc_and_lang`, `ai_optimization_chat_gpt_scraper_locations`). S'ils ne le sont pas, dis-le au lieu de basculer en silence sur un autre pays.

Les noms d'outils évoluent : en cas d'écart, la liste exposée par le connecteur fait foi.

## Règle 4 — Erreurs connues

- **HTTP 402** : compte sans crédit. Arrête les appels, dis-le, continue avec la Search Console et la lecture directe des pages, en précisant ce qui manque.
- **« expected array, received string »** sur `keywords` : renvoie le même appel, la liste est parfois mal transmise au premier essai.
- Résultat vide : vérifie l'orthographe exacte et les accents avant de conclure à un volume nul.

## Règle 5 — Ce que DataForSEO ne remplace pas

- Positions et clics réels du site : la Search Console.
- Crawl complet : un outil de crawl lancé en local.

## Livrable type

Un tableau avec les colonnes utiles seulement (mot-clé, volume, difficulté, intention, position, URL positionnée), puis la lecture en trois à cinq points, puis le coût total dépensé.

## Dépendances

Sans le connecteur DataForSEO, ce skill n'a rien à appeler : oriente vers la Search Console, les suggestions de recherche gratuites et la lecture directe des pages de résultats, et dis ce que l'analyse perd (volumes, difficulté, visibilité IA mesurée).
