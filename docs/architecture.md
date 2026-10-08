# Architecture et choix de conception

## 1. Un contexte, lu par référence

**Problème.** Un skill qui recopie l'offre, les prix et le ton devient faux le jour où l'un d'eux change. Vingt skills, vingt endroits à corriger.

**Choix.** Un fichier `brand-context.md`, douze sections fixes, lu par chaque skill au moment où il s'exécute. Les skills ne contiennent aucune donnée de marque : seulement de la méthode et des renvois (« contexte §3 »).

**Conséquences.**
- Changer de projet revient à changer un dossier `brand/`.
- Le bloc « Étape 0 » est identique dans tous les skills ; `scripts/lint_repo.py` vérifie qu'il est présent.
- Trois règles de lecture évitent les inventions : une date de fraîcheur en tête, le marqueur `[hypothèse]` pour ce qui reste à valider, le marqueur `A_COMPLETER` pour un fait manquant. Si le fichier et le site divergent, le site gagne.

## 2. Deux fichiers, deux lecteurs

| Fichier | Lecteur | Contenu |
|---|---|---|
| `brand-context.md` | le modèle | ce qui se lit et s'interprète : offre, cibles, ton, règles |
| `kit.config.json` | les scripts | ce qui se teste : domaine, seuils, mots bannis, gabarits, plafonds |

Un script ne doit pas interpréter de la prose, et un modèle n'a pas besoin d'un seuil pour comprendre une marque. Le skill `setup` écrit les deux.

## 3. Des skills autonomes, regroupés en plugins

Chaque skill est un dossier qui se suffit : `SKILL.md`, `scripts/`, `references/`, `assets/`. On peut l'installer seul.

Conséquence assumée : quand deux skills ont besoin du même module, il est **copié** dans les deux (`article_checks.py` dans `seo-writer` et `blog-pipeline`), et le lint vérifie que les copies sont identiques. Un import entre plugins casserait dès qu'un seul des deux est installé.

Les plugins suivent le parcours d'un site : `vk-core` (cadrer), `vk-design` et `vk-shopify` (construire), `vk-seo` (être trouvé), `vk-content` (publier), `vk-marketing` (convertir), `vk-social`, `vk-reels` et `vk-ads` (diffuser et mesurer).

## 4. Des skills qui orchestrent

`blog-pipeline` ne réécrit pas les règles de rédaction : il charge `seo-writer`, `seo-geo`, `seo-audit` et `seo-data`, puis ajoute ce qui leur manque pour tourner sans personne — choix des sujets, mémoire, publication, livraison.

`social-plan` décide, `social-publish` exécute. Le plan est un document texte, une ligne par post, que l'utilisateur peut corriger à la main : l'automatisation suit ses modifications au lieu de les écraser.

## 5. L'état vit dans des fichiers

Une exécution planifiée démarre sans mémoire de la précédente. Chaque lot écrit donc un `MANIFEST.json` (sujets traités, slugs, dates, identifiants créés) dans son dossier de livraison, et le lot suivant commence par les relire. Le tableur de sujets reste la propriété de l'utilisateur : le pipeline le lit, il n'y écrit pas.

## 6. Des contrôles déterministes après la génération

Un modèle qui se relit laisse passer ses propres erreurs. Tout ce qui se vérifie mécaniquement est sorti de la relecture et confié à un script qui renvoie un code d'erreur :

| Risque | Contrôle |
|---|---|
| Lien interne cassé | requête sur chaque lien, code 200 exigé |
| FAQ du schema différente de la FAQ affichée | comparaison question par question |
| Données structurées en double avec le thème | types émis par le gabarit déclarés dans la configuration |
| Prix périmé dans un article | motif de prix interdit dans le corps |
| Brief de travail publié par erreur | commentaire HTML interdit dans le corps |
| Vocabulaire que la marque refuse | liste de la configuration |
| Texte qui « fait IA » | motifs de structure, pas seulement de vocabulaire |
| Hashtags ignorés par la plateforme | plafond par plateforme |

Ce qui ne se vérifie pas mécaniquement reste dans une checklist à remplir, preuve à l'appui.

## 7. Garde-fous

| Domaine | Règle | Où |
|---|---|---|
| Dépense d'API | coût annoncé avant, seuil de demande, plafond par exécution | `seo-data` |
| Publicité | lecture seule, propositions en brouillon | `ads-audit` |
| Thème en production | nouveaux fichiers à côté des anciens, aucune publication ni suppression sans demande | `shopify-liquid` |
| Publication | programmée, jamais immédiate ; validation explicite | `blog-pipeline`, `social-publish` |
| Faits | source et date de relevé, sinon le fait sort | `seo-writer`, `directory-pages` |
| Entités tierces | sources publiques, fiche factuelle, procédure de correction | `directory-pages` |
| Secrets | variables d'environnement, jamais dans un fichier | tous |

## 8. Mode dégradé

Un kit qui exige cinq abonnements n'est testé par personne. Chaque skill se termine par un tableau « avec / sans » connecteur et annonce dans son livrable ce que l'absence lui fait perdre (« audit partiel », « sondage manuel daté »). Une catégorie non mesurée sort du score au lieu d'être notée au hasard.

## 9. Ce qui est propre à une plateforme

Le cœur ne suppose aucune plateforme. Ce qui en dépend est isolé :

- `vk-shopify` : un plugin à part.
- `seo-audit`, `seo-schema`, `site-clone` : une section par plateforme (Shopify, WordPress, site statique).
- `blog-pipeline` : la création directe est décrite pour Shopify et WordPress, avec un fichier d'import comme voie commune.
- `social-publish` : les étapes de rédaction et de contrôle sont indépendantes du service ; l'upload, l'envoi et la vérification sont écrits pour une API donnée.

## 10. Moteur vidéo : du code plutôt que des assets

Une vidéo est un scénario JSON rendu image par image (Pillow), encodé par ffmpeg, avec un son synthétisé (numpy). Pas de photo, pas de musique sous droits, pas de montage. Le thème (palette, polices, couleurs des mascottes) est un fichier séparé : le même scénario se rend aux couleurs d'une autre marque.

## 11. Tests

- `scripts/lint_repo.py` : manifestes valides, en-têtes des skills, bloc de contexte présent, copies de modules identiques, aucune trace du projet d'origine ni de secret.
- `tests/run_tests.py` : chaque script est exécuté sur les exemples fictifs, cas conformes et cas fautifs, et un rendu vidéo court est produit si les dépendances sont là.
- `.github/workflows/ci.yml` : les deux, à chaque envoi.

## 12. Pistes d'évolution

- Un adaptateur de publication indépendant du service, avec une interface commune.
- Des jeux de motifs par langue pour les contrôles d'écriture.
- Un entrepôt de données (Search Console, statistiques sociales) pour remplacer les relevés à la demande par des séries dans le temps.
