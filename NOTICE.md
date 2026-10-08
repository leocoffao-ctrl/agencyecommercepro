# Attributions

`vitrine-kit` est distribué sous licence MIT (voir `LICENSE`). Une partie de ses skills est adaptée de projets open source publiés sous licence MIT. Leurs auteurs conservent leurs droits ; les textes de licence d'origine sont dans `licenses/`.

## Ce qui est adapté, et de quoi

| Dans ce dépôt | Projet d'origine | Auteur | Licence | Nature de la reprise |
|---|---|---|---|---|
| `vk-seo` : `seo-audit`, `seo-geo`, `seo-schema`, `seo-data`, `seo-pages` et leurs `references/` | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | agricidaniel | MIT | Méthode, grilles de score et références reprises ; scripts locaux remplacés par des règles de conduite ; réécrit en français et branché sur le contexte de marque. Les fichiers `references/` sont repris tels quels, en anglais |
| `vk-ads` : `ads-audit` et ses `references/` | [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | agricidaniel | MIT | Principes et catalogues de contrôles repris ; `references/` tels quels |
| `vk-marketing` : `copywriting`, `cro`, `email-flows`, `ad-creative` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Corey Haines | MIT | Cadres d'analyse repris ; exemples SaaS remplacés par des règles e-commerce et vitrine |
| `vk-shopify` : `shopify-liquid`, `references/liquid-officiel.md` | [Shopify/Shopify-AI-Toolkit](https://github.com/Shopify/Shopify-AI-Toolkit) | Shopify Inc. | MIT | Référence Liquid reprise ; étapes de validation distante retirées |
| `vk-design` : `site-clone`, `references/extraction.md` | [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) | JCodesMore | MIT | Méthode d'extraction reprise ; cible changée (structure et comportement seulement) |
| `vk-social` : `social-publish` (workflow, `reference/zernio/`, `templates/post-body.json`) | [Enriquemarq1/zernio-library-skills](https://github.com/Enriquemarq1/zernio-library-skills) | Enrique Marquez | MIT | Workflow repris ; `reference/zernio/` tels quels |
| `vk-social` : `reference/anti-ia.md`, `scripts/check_anti_ia.py`, `reference/humanizer/` | [blader/humanizer](https://github.com/blader/humanizer) | Siqi Chen | MIT | Adaptation française ; original conservé dans `reference/humanizer/` |
| `vk-social` : `social-plan`, `reference/accroches.md`, `scripts/check_legende.py`, `scripts/score_accroche.py`, `scripts/audit.py` | [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) | Jake Schincariol | MIT | Adaptation française de plusieurs skills et scripts |

Chaque skill adapté le rappelle dans ses premières lignes. Les skills `social-publish` et `social-plan` portent en plus leur propre fichier `NOTICE`, pour rester en règle s'ils sont distribués seuls.

## Ce qui est écrit pour ce kit

- `vk-core` : `setup`, `brand-context`, `start`, le gabarit de contexte et la configuration.
- `vk-seo` : `seo-writer` et `article_checks.py`.
- `vk-content` : `blog-pipeline`, `directory-pages`, leurs scripts, le prompt master et la feuille de style.
- `vk-reels` : `mascot-reels`, le moteur de rendu, les sprites et les thèmes.
- L'architecture d'ensemble : contexte partagé, mode dégradé par connecteur, garde-fous, contrôles et tests.

## Ce qui n'est pas redistribué

- Les skills de design de tiers utilisés pendant la construction du kit : voir `docs/dependances-design.md`.
- La spécification OpenAPI de Zernio : à consulter sur https://docs.zernio.com/.
- Les polices du moteur vidéo : téléchargées au premier rendu depuis `google/fonts` (Titan One et Pixelify Sans, SIL Open Font License).

## Marques

Shopify, Meta, Instagram, Google, TikTok, Pinterest, LinkedIn, YouTube, Zernio, DataForSEO, Matrixify et WordPress sont des marques de leurs détenteurs respectifs, citées pour décrire des intégrations. Ce dépôt n'est affilié à aucune d'elles.
