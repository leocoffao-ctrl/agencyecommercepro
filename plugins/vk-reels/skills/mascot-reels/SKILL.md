---
name: mascot-reels
description: Crée des vidéos verticales en pixel art (Reels, TikTok, Shorts) avec des mascottes de marque — scénario JSON, faits vérifiés, rendu MP4 9:16 animé avec son 8-bit, couverture et storyboard, prêts à publier. Tout est dessiné par du code, sans photo ni asset tiers. À utiliser dès que l'utilisateur parle de mascotte, de Reel ou de vidéo animée, de pixel art, d'épisode, de série vidéo, de « fais expliquer X par un personnage », ou veut un format court récurrent pour ses réseaux, même sans dire « Reel ». La publication passe ensuite par social-publish.
---

# Vidéos pixel art avec mascottes

Tu produis une vidéo finie (MP4 1080 × 1920, 30 images par seconde, son 8-bit), sa couverture et son storyboard, à partir d'un scénario JSON rendu par `scripts/reel_engine.py`. Rien n'est filmé ni téléchargé : pas de droits à gérer sur les images.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 0. Avant tout

1. Lis `references/univers.md` : comment se construit un crew de mascottes, et comment on choisit laquelle parle.
2. Lis `references/spec-format.md` avant d'écrire un scénario.
3. Le thème (palette, polices, couleurs des mascottes) se règle dans un fichier `themes/*.json` : `references/theme-format.md`. Pars de `themes/demo.json` et applique la palette du contexte §6.

Dépendances de rendu : Python avec Pillow et numpy, et ffmpeg.

## 1. Choisir la mascotte et l'univers

Une mascotte = un rôle éditorial. On la choisit **par le sujet**, jamais au hasard. Le contexte §11 décrit le crew de la marque s'il existe. Les deux personnages livrés (`rond`, `carre`) sont des démonstrations : remplace-les ou habille-les aux couleurs de la marque.

| Univers | Décor | Convient pour |
|---|---|---|
| `rayures` | rayures diagonales, une couleur par scène | sujets du quotidien, recettes, lieux |
| `collines` | ciel, soleil, collines | origine, nature, fabrication |
| `tableau` | tableau quadrillé encadré | jargon expliqué, pédagogie |
| `carte` | carte, trajet pointillé, nuages | livraison, voyage, offre |

## 2. Collecter les faits

- Un contenu du site (guide, fiche, page d'offre) : lis-le et n'utilise que ce qu'il dit, avec sa date de relevé.
- L'offre de la marque : seulement les affirmations autorisées du contexte §3. Pas de prix sans revérification sur la source de vérité.
- Connaissance générale : formulations prudentes (« souvent », « en général »), rien de chiffré sans source.
- Éléments fournis par l'utilisateur (étiquette, fiche technique) : recopiés dans l'ordre de la hiérarchie d'information du contexte §5, sans rien inventer.

## 3. Écrire le scénario

Structure qui marche, quatre à six scènes, 28 à 40 secondes :

1. **Accroche** : étiquette de rubrique, titre sur deux lignes, la mascotte se présente.
2. à 4. **Contenu** : une idée par scène, un titre court, un ou deux accessoires, une ou deux bulles.
5. **Fin** : nom de la marque, signature, un seul appel à l'action.

Règles de lisibilité, à ne pas dégrader :
- Bulle de 80 caractères au plus, trois lignes au plus. Au-delà, coupe en deux bulles.
- Titres de 90 px ou plus, textes pixel de 46 px ou plus, étiquettes de 52 px ou plus.
- Contraste : texte sombre sur clair, clair sur sombre. Une couleur vive sur un fond vif : seulement avec `stroke` ou `bg`.
- Zones sûres : rien d'important au-dessus de 220 px ni sous 1560 px. Le moteur avertit si une bulle déborde.
- Les espaces insécables de la typographie française sont ajoutées par le moteur : écris le texte normalement.
- Un accessoire de la couleur du fond disparaît : change le `tone` de la scène.
- Ton, registre et précision : contexte §5.

**Passe anti-IA obligatoire sur les bulles et les titres.** Avant le rendu, relis chaque bulle et chaque titre avec `reference/anti-ia.md` du skill `social-publish` et, s'il est installé, lance son `check_anti_ia.py --json bulles.json` avec `platform: "visuel"` (zéro « FORT »). Aucun fait n'est ajouté par la réécriture. Une vidéo dont les bulles n'ont pas eu cette passe ne se publie pas.

Pars d'un scénario de `specs/` et adapte-le : c'est plus sûr que de partir de zéro.

## 4. Rendre

```bash
python3 scripts/reel_engine.py specs/<mon-reel>.json sortie/<mon-reel> --theme themes/<mon-theme>.json
```

Le moteur télécharge les polices du thème au premier lancement ; hors ligne, il continue avec une police intégrée et le signale. Sorties : `<filename>.mp4`, `cover.jpg` (l'accroche entièrement écrite), `storyboard.png`, `kf*.png`. `--no-audio` donne une vidéo muette pour un essai rapide.

**Regarde toujours `storyboard.png` avant de livrer** : chevauchement d'un titre et d'un accessoire, texte coupé, contraste, mascotte cachée. Corrige le JSON et relance ; un rendu prend 20 à 40 secondes.

## 5. Livrer

- Le MP4 et la couverture.
- Dans la réponse : le sujet, la mascotte, les faits utilisés avec leur source et leur date, une légende (accroche, un appel à l'action, lien avec UTM, hashtags dans le plafond de la plateforme).
- Publication : proposer `social-publish`. Ne jamais publier d'ici.

## 6. Faire évoluer le crew

- Nouvelle mascotte, pose ou expression : `scripts/sprites.py` (grille 32 × 32, primitives `ell`, `rect`, `face`). Déclare ses couleurs et sa voix dans le thème.
- Nouvel accessoire : une fonction `ic_<nom>` dans `reel_engine.py`, ajoutée à `ICONS`, dessinée en basse définition puis passée dans `outlined()`.
- Nouvel univers : une branche dans `bg()` et une ligne dans `MUSIC`. Documente-le dans `references/univers.md`.
- Toute modification : rends une vidéo de test et regarde le storyboard.

Une mascotte est un élément de marque. Dessine un personnage original : ne reproduis pas un personnage existant, même simplifié.

## Dépendances

| Élément | Avec | Sans |
|---|---|---|
| ffmpeg, Pillow, numpy | rendu complet | pas de rendu : le scénario JSON et le storyboard décrit en texte sont livrés |
| Accès réseau (premier lancement) | polices du thème | police intégrée, signalée |
| Skill `social-publish` | passe anti-IA automatisée, publication | relecture manuelle avec les mêmes règles |
