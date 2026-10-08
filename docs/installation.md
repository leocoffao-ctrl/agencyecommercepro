# Installation

## Claude Code

Le dépôt est une place de marché de plugins : un fichier `.claude-plugin/marketplace.json` à la racine, et un dossier par plugin dans `plugins/`.

```bash
# depuis GitHub
claude plugin marketplace add leocoffao-ctrl/agencyecommercepro

# ou depuis une copie locale
git clone https://github.com/leocoffao-ctrl/agencyecommercepro.git
claude plugin marketplace add ./agencyecommercepro

# installer le socle, puis ce qui sert
claude plugin install vk-core@vitrine-kit
claude plugin install vk-seo@vitrine-kit
claude plugin install vk-content@vitrine-kit

# vérifier
claude plugin list
claude plugin validate ./agencyecommercepro
```

Dans une session, les mêmes opérations passent par `/plugin`. Les skills s'appellent avec le nom du plugin en préfixe : `/vk-core:setup`, `/vk-seo:seo-audit`. Claude les déclenche aussi seul quand la demande correspond à leur description.

## claude.ai et application de bureau

Un skill est un dossier autonome : `SKILL.md`, et éventuellement `scripts/`, `references/`, `assets/`. Pour en utiliser un sans passer par la place de marché, envoie son dossier (compressé) dans les réglages de skills de ton compte, ou ajoute le plugin entier s'il est proposé par ton organisation.

Dans un Project claude.ai, dépose `brand-context.md` dans les fichiers du Project : les skills le trouvent à `/mnt/project/brand-context.md`.

## Où vit le contexte de marque

Les skills cherchent `brand-context.md` dans cet ordre :

1. `./brand/brand-context.md`, puis `./brand-context.md` ;
2. le dossier désigné par la variable d'environnement `VK_BRAND_DIR` ;
3. `/mnt/project/brand-context.md`.

Les scripts lisent `kit.config.json`, passé par `--config`.

```
mon-projet/
└── brand/
    ├── brand-context.md     ← lu par les skills
    ├── kit.config.json      ← lu par les scripts
    └── assets/              ← logos, charte, visuels
```

Pour partir d'un exemple :

```bash
cp -r vitrine-kit/examples/atelier-verveine/brand mon-projet/brand
```

Puis lance `/vk-core:setup` : il relit ton site, pose ses questions et remplace les valeurs de l'exemple.

## Secrets

Aucune clé ne va dans le dépôt, dans `brand/` ou dans un livrable. Les skills attendent les clés dans des variables d'environnement, par exemple `ZERNIO_API_KEY`. Les identifiants non secrets (comptes, dossiers, bases) vont dans `kit.config.json`.

## Connecteurs

Tout est facultatif. Chaque skill indique ce qu'il fait avec et sans.

| Connecteur | Skills qui en profitent |
|---|---|
| DataForSEO | `seo-data`, `seo-audit`, `seo-geo`, `seo-pages`, `seo-writer`, `blog-pipeline` |
| Search Console | `seo-audit`, `seo-writer`, `blog-pipeline` |
| CMS (Shopify, WordPress) | `blog-pipeline`, `shopify-liquid`, `directory-pages` |
| Stockage (Drive ou dossier local) | `blog-pipeline`, `social-plan` |
| Outil de tâches | `seo-audit`, `cro`, `ads-audit` |
| API Zernio | `social-publish`, `social-plan` |
| Recherche de lieux | `directory-pages` |
| Navigateur | `site-clone` |

## Dépendances des scripts

Python 3.10 ou plus récent. Bibliothèque standard seulement, sauf `reel_engine.py` qui demande Pillow, numpy et ffmpeg :

```bash
pip install pillow numpy
```

## Vérifier l'installation

```bash
python3 scripts/lint_repo.py
python3 tests/run_tests.py
```
