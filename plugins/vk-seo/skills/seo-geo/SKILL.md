---
name: seo-geo
description: Mesure et améliore la visibilité d'une marque dans les réponses des IA (ChatGPT, Google AI Overviews et AI Mode, Perplexity, Claude) — citations du domaine, mentions de la marque, accès des robots IA, citabilité des pages — avec des données réelles quand DataForSEO est branché. À utiliser dès que l'utilisateur parle de GEO, d'AEO, de recherche IA, de ChatGPT qui recommande ou non sa marque, d'AI Overviews, de llms.txt, de robots IA, de « est-ce que les IA nous citent », ou veut qu'une page soit reprise par les IA, même sans dire GEO.
---

# GEO — visibilité dans les réponses des IA

Adapté de `AgriciDaniel/claude-seo/skills/seo-geo` (MIT). Grille de score et règles sur les robots IA conservées ; le rendu Playwright et les scripts locaux sont remplacés par la lecture directe des pages et le connecteur DataForSEO.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

Avant tout appel DataForSEO, applique les règles du skill `seo-data` (pays et langue explicites, accord avant dépense). Les outils IA sont dans la catégorie « toujours demander ».

## Ce qui compte, d'après les sources du dépôt d'origine (données 2025-2026)

- Pour Google, optimiser pour l'IA générative reste du SEO : une page doit être indexée et éligible à un extrait pour apparaître dans une réponse IA. Voir `references/google-ai-optimization-guide.md`.
- Les mentions de la marque hors site (vidéo, forums, presse, sites de partenaires) pèsent davantage que les backlinks dans les citations IA.
- Les passages cités sont autonomes, factuels, placés tôt dans la page, d'une longueur d'environ 130 à 170 mots.
- La fraîcheur compte : dater les pages (publication et mise à jour réelle).
- AI Overviews suit les positions classiques ; AI Mode et ChatGPT puisent plus large. On mesure chaque surface séparément.
- `llms.txt` n'est **pas** un levier pour Google ni, preuves à l'appui, pour les grands moteurs IA. Priorité basse. Voir `references/llmstxt-evidence.md`.

Ces repères datent : chaque référence indique sa date de dernière vérification. Revérifie avant d'en faire un argument.

## Déroulé

### 1. Questions cibles
Liste 10 à 20 questions que les profils du contexte §4 posent aux IA, dans la langue du projet : comparaison d'offres, choix d'un prestataire, « où acheter », « meilleur X pour Y », questions locales. Montre la liste, garde celles que l'utilisateur valide.

### 2. Mesure (DataForSEO, avec accord)
- Scraper ChatGPT sur trois à cinq questions prioritaires, recherche web forcée : la marque est-elle citée ? Qui l'est à sa place ? Quelles sources sont liées ?
- Métriques de mentions sur le domaine, puis sur le nom de marque : volume, plateformes.
- Domaines les plus cités sur le sujet : ce sont les cibles de relations presse et de partenariats.
- Comparaison croisée avec deux à quatre concurrents repérés à l'étape précédente.

Sans connecteur : pose les questions à la main sur les surfaces accessibles, note la date, et présente le résultat comme un sondage, pas comme une mesure.

### 3. Accès technique
- `robots.txt` : statut de chaque robot, **rapporté séparément**. Le robot de recherche d'un fournisseur n'est pas son robot d'entraînement. Détail et tableau de correspondance : `references/crawlers-ia.md`.
- Le contenu clé est-il dans le HTML servi ? Les robots IA n'exécutent généralement pas le JavaScript. Vérifie dans la source que les textes d'offre, la FAQ et les fiches apparaissent.

### 4. Citabilité page par page

| Critère | Poids | Ce qu'on regarde |
|---|---|---|
| Citabilité | 25 % | Réponse directe de 40 à 60 mots en tête de section, phrases factuelles, définitions, données propres à la marque |
| Structure | 20 % | Hiérarchie de titres propre, intertitres en questions, tableaux, listes |
| Multimodal | 15 % | Images légendées, vidéo, tableau comparatif |
| Autorité et marque | 20 % | Auteur, dates, sources primaires, présence de la marque hors site |
| Accès technique | 20 % | Robots IA autorisés, contenu en HTML, rapidité |

Score sur 100 par page, puis moyenne. C'est une heuristique : aucun outil tiers n'a accès aux signaux internes des moteurs, écris-le dans le rapport.

## Livrable : `GEO-<marque>-<date>.md`

1. Score sur 100 et lecture par surface.
2. Questions testées : marque citée ou non, qui est cité à sa place, sources liées.
3. Accès des robots IA, robot par robot.
4. Cinq passages à réécrire, avec la version citable proposée (le skill `copywriting` peut finaliser).
5. Plan : gains rapides, effort moyen, fort impact (mentions externes).
6. Coût DataForSEO dépensé.

Les pages d'annuaire ont leurs propres règles de citabilité dans le skill `directory-pages` : signale seulement ce qui manque, ne les réécris pas ici.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| DataForSEO (outils IA) | mentions et citations mesurées | sondage manuel daté |
| Outil de tâches | actions créées | liste dans le livrable |
