---
name: seo-writer
description: Rédige un article de fond optimisé pour les moteurs classiques et les moteurs génératifs — contrôles bloquants avant rédaction (cannibalisation, fan-out, thèse différenciante, vérification des faits, contrôle arithmétique), structure imposée, blocs autonomes et citables, architecture anti-péremption, maillage hiérarchisé, JSON-LD, script de contrôle et test final. À utiliser dès que l'utilisateur demande un article de blog, un guide, un comparatif, un contenu SEO, un pilier ou un satellite, ou donne un mot-clé à traiter, même sans parler de GEO.
---

# Rédaction SEO + GEO

Méthode en six phases. Elle sert à écrire un article qu'aucun concurrent ne pourrait signer, qui reste vrai dans six mois, et dont chaque bloc peut être cité seul.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

Trois éléments du contexte commandent tout l'article :
- **l'avantage structurel** (§10) : ce que la marque peut écrire honnêtement et pas ses concurrents. Il transparaît dans la thèse et les recommandations, jamais dans une phrase d'autopromotion ;
- **les pages commerciales protégées** (§10) : leurs requêtes ne sont jamais visées par un article ;
- **les affirmations autorisées** (§3) et la conformité (§12).

## Variables à remplir avant de commencer

```
MOT_CLE_PRINCIPAL    =
REQUETES_SECONDAIRES =
REQUETES_EXCLUES     =            ← celles que gardent les pages commerciales
INTENTION            = définitionnelle | décisionnelle | comparative | économique
ROLE                 = pilier | satellite | traitement d'objection
URL_CIBLE            =
PIVOT_COMMERCIAL     =
POSITION_ACTUELLE    =            ← Search Console, si la page existe
CONCURRENTS_TOP5     =            ← URL réelles relevées le jour même
```

## Phase 0 — Blocage

Rends les conclusions des cinq contrôles avant de rédiger. Si l'un échoue, arrête-toi et dis-le.

**0.1 Anti-cannibalisation.** Compare le mot-clé à l'arborescence du contexte §10 et à la liste des URL en ligne (sitemap).

| Situation | Décision |
|---|---|
| Aucune page ne couvre le champ | Écrire |
| Une page le couvre avec la même intention | Ne pas écrire. Proposer la mise à jour de l'existante |
| Une page le couvre avec une intention différente | Écrire, avec les deux liens croisés à poser, inscrits dans les tâches |

Règle absolue : le blog prend le définitionnel et le décisionnel, le transactionnel reste aux pages commerciales. Un article qui vise « acheter X » attaque sa propre boutique.

**0.2 Fan-out génératif.** Liste 8 à 12 sous-requêtes qu'un moteur génératif produirait à partir du mot-clé : définition, critères de distinction, comparaison avec le voisin sémantique, prix, comment vérifier, cas où ça ne s'applique pas, historique, acteurs. Chacune est-elle couverte par une page existante ? Sinon elle devient un H2. Une page couvre 4 à 6 sous-requêtes ; on ne crée jamais une page par sous-requête.

**0.3 Thèse différenciante.** Lis les cinq concurrents. Cherche ce qu'ils ont tous omis, simplifié ou faux. Gisements, par rendement :
1. la contradiction entre sources sérieuses qui ne mesurent pas la même chose ;
2. l'information périmée (norme changée, référentiel remplacé) ;
3. le chiffre invérifiable ou impossible (voir 0.5) ;
4. la distinction que tout le monde écrase ;
5. le contre-intuitif vérifiable ;
6. le résultat négatif que personne ne mentionne.

Test : si un concurrent pouvait écrire cette phrase sans mentir, la thèse est trop faible.

**0.4 Vérification factuelle.** Aucun chiffre, date, nom propre ou étude n'entre sans vérification à la source le jour même.
- Une étude se cite avec son type, son effectif et son résultat réel.
- Une source non évaluée par les pairs se déclare comme telle dans le corps.
- Une information à source unique se signale.
- Deux sources fiables qui se contredisent : on présente la contradiction, on ne tranche pas.
- Une donnée invérifiable sort. Pas de « environ », pas de chiffre repris d'un concurrent.

Produis le tableau `FAIT | SOURCE | DATE DE RELEVÉ | NIVEAU DE CERTITUDE`.

**0.5 Contrôle arithmétique.** Pour chaque chiffre repris, pose une question d'ordre de grandeur : est-il cohérent avec les autres chiffres de la page et avec les totaux connus du secteur ? Un chiffre incohérent s'écarte, et peut devenir une section : démontrer qu'un chiffre en circulation est faux crédibilise la page.

## Phase 1 — Structure imposée

```
 1. Titre d'accroche (≠ title SEO) + signature datée + date de relevé des données
 2. [Bandeau de méthode]       ← si l'article contient des données périssables
 3. Réponse rapide             ← 5 à 6 puces, la thèse entière
 4. Sommaire ancré
 5. [Bloc de données daté]     ← si applicable, voir Phase 1 bis
 6. Corps : 5 à 8 H2 atomisés
 7. Tableau de décision        ← sauf intention purement définitionnelle
 8. Checklist actionnable
 9. Limites / quand ce n'est pas la bonne réponse
10. FAQ, 6 à 8 questions
11. À lire ensuite, hiérarchisé
12. Sources et méthode, datées
```

**Réponse rapide** : 5 à 6 puces de 15 à 25 mots, avant le sommaire. Elles donnent la réponse, elles ne la promettent pas. Chaque puce reste vraie copiée seule. Deux au moins contiennent un fait chiffré ou une date.

**Tableau de décision** : `Votre situation` → `Ce qu'il faut faire` → `Pourquoi`. En-têtes autoportants, une ligne par cas, cellules complètes. Jamais d'image de tableau.

Si le gabarit du site affiche déjà le titre en H1 (contexte §7, `blog.theme_renders_h1`), le corps ne contient pas de `<h1>`.

## Phase 1 bis — Architecture anti-péremption

Dès que l'article contient des prix, des cours ou des statistiques :

- toutes les données périssables dans **un seul bloc**, avec son `id` et sa date de relevé ;
- aucun chiffre périssable ailleurs : le corps renvoie au bloc par une ancre ;
- le reste de l'article explique un mécanisme, qui ne change pas ;
- la prochaine date de révision est inscrite dans le bloc et dans le bandeau de méthode ;
- la FAQ peut reprendre les chiffres, puisqu'elle est révisée en même temps.

## Phase 2 — Règles d'écriture

**Atomisation.** Chaque bloc est compréhensible et citable sans son contexte.
- Chaque H2 et chaque paragraphe renomme son sujet. Jamais « cela », « ce dernier », « comme vu plus haut » en ouverture.
- Réponse en tête, explication ensuite.
- H2 formulés comme une question ou une affirmation complète.
- Bloc-réponse de 40 à 80 mots sous chaque H2 ; au moins un passage de 130 à 170 mots, factuel et autonome, dans le premier tiers.
- Un fait vérifiable et qualifié par section (« selon [source], à la date de… »).

**Lexique canonique.** Un nom principal par entité, tenu sur tout le site. Les définitions courtes se répètent à l'identique d'une page à l'autre. Les distinctions à tenir sont celles du contexte §5.

**Preuve.**

| Formulation | Valeur |
|---|---|
| « qualité premium », « sélectionné avec soin » | nulle |
| « testé en laboratoire » | faible, invérifiable |
| « analysé par lot » | correcte |
| mesure nommée, par qui, selon quel protocole, fiche consultable | forte |
| donnée propriétaire chiffrée | maximale |

**Transparence comme levier.** Inclure au moins une forme : « voici quand ce produit ne convient pas », « voici ce qui produit réellement l'effet », « voici pourquoi le marché est mauvais » (sans dénigrer nommément), « achetez ailleurs si… ». La transparence est suivie d'une raison objective de choisir la marque, sinon c'est du sabordage.

**Interdits.**
- Bourrage de mots-clés, statistiques décoratives.
- Superlatif invérifiable, adjectif qu'un concurrent écrirait à l'identique.
- Allégation réglementée dans le secteur (contexte §3 et §12).
- Prix de la marque en dur dans un texte éditorial, si la configuration l'interdit.
- Chiffre amené à bouger écrit en dur (nombre de partenaires, de références, d'avis) : formulation qualitative.
- Requête transactionnelle d'une page protégée.
- Millésime dans le slug.
- Ponctuation exclue par le contexte §5.

## Phase 3 — Maillage

Rends la liste exacte des liens, avec ancre rédigée et emplacement.

| Rôle | Liens internes contextuels |
|---|---|
| Satellite | 4 à 8 |
| Traitement d'objection | 6 à 10 |
| Pilier | 15 à 20, vers 12 destinations au moins |

Hiérarchie des destinations : niveau 1 commercial, niveau 2 pivots, niveau 3 satellites. Un lien vers le pivot commercial, placé à un moment de décision. Ancres intégrées à une phrase, trois variantes par destination à l'échelle du site, jamais l'expression clé seule. Dans le fil d'Ariane, l'échelon intermédiaire pointe vers la page commerciale.

Chaque lien interne doit répondre 200 le jour de la rédaction.

Format : `ANCRE | URL | section | niveau | raison`.

## Phase 4 — Métadonnées et balisage

| Élément | Contrainte |
|---|---|
| Title | 60 caractères au plus, mot-clé en tête, différent du titre affiché |
| Titre affiché | libre, peut porter la thèse |
| Meta description | 155 caractères au plus ; une promesse d'information à contre-courant vaut mieux qu'un résumé |
| Slug | court, sans mots vides, sans millésime |

Si la requête nue appartient à une page commerciale, le title s'ouvre sur un modifieur (« Comparer… », « Choisir… »).

JSON-LD : seulement les types que le gabarit n'émet pas déjà (`blog.theme_emits_jsonld`). `FAQPage` strictement identique à la FAQ visible si on en produit un ; `ItemList` pour un classement. Jamais d'`aggregateRating` sans avis affichés.

Image d'en-tête : 1200 × 630, WebP, moins de 150 Ko, dimensions déclarées, nom de fichier égal au slug, texte alternatif descriptif.

## Phase 5 — Autocontrôle

```bash
python3 scripts/article_checks.py article.html --config brand/kit.config.json \
  --handle <slug> --title "<titre affiché>" --seo-title "<title>" --seo-description "<meta>"
```

Le script bloque sur : slug invalide ou millésimé, title ou meta trop longs, title identique au titre, ponctuation exclue, commentaire HTML ou H1 dans le corps, prix en dur, `aggregateRating`, variable non résolue, section de réponse rapide absente, FAQ visible différente de la FAQ du schema, JSON-LD redondant avec le gabarit, balises non fermées, mots bannis, lien interne qui ne répond pas 200. Corrige jusqu'au code de sortie 0.

Puis remplis la checklist, avec la preuve à côté :

```
[ ] Thèse en une phrase qu'aucun concurrent ne pourrait écrire   → la phrase :
[ ] Aucune cannibalisation                                       → pages vérifiées :
[ ] Fan-out : n sous-requêtes couvertes par n H2                 → correspondance :
[ ] Contrôle arithmétique passé sur chaque chiffre repris
[ ] Sources non évaluées par les pairs déclarées dans le corps
[ ] Contradictions entre sources présentées, non tranchées
[ ] Information à source unique signalée
[ ] Test d'autonomie passé sur 3 blocs tirés au hasard
[ ] Chaque chiffre a sa source et sa date de relevé
[ ] Données périssables isolées dans un bloc daté, révision inscrite
[ ] Title ≠ titre, 60 et 155 caractères respectés
[ ] Title sans requête réservée à une page commerciale
[ ] FAQ visible = FAQ du schema
[ ] Volume de liens conforme au rôle, hiérarchie respectée
[ ] Aucun adjectif copiable par un concurrent
[ ] Aucune allégation réglementée
[ ] Une section « limites » ou « achetez ailleurs si »
[ ] L'appel à l'action ne suit pas une section qui nuance le produit
[ ] Un lecteur pressé a sa réponse en 15 secondes
```

## Phase 6 — Livrables

1. Les conclusions de la Phase 0, en clair.
2. `<slug>.html` : le corps en HTML sémantique, sans commentaire.
3. `BRIEF-<slug>.md` : variables, Phase 0, tableau des faits, tableau de maillage, liens retour à poser sur les pages existantes, limites assumées, tâches avant mise en ligne. Le brief ne va jamais dans le code public.
4. Title, meta description, slug.
5. La sortie du script et la checklist remplie.
6. Le prompt d'image :

```
Prompt (anglais) :
  Editorial [type] photograph, [sujet précis], [composition], [lumière],
  [palette du contexte de marque], negative space [où],
  no text, no logos, no people, no hands. Photorealistic, matte finish.
Negative prompt :
  text, letters, numbers, watermark, logo, brand, hands, people, faces,
  cartoon, oversaturated, HDR, plastic look, cluttered background
Format : 16:9, 1200×630, export WebP < 150 Ko, nom de fichier = slug
```

Le visuel illustre la thèse, pas le sujet général. Aucun chiffre ni texte dans l'image : une valeur affichée périme comme le reste.

## Le test final

Si une réponse est non, l'article ne sort pas.

1. Un concurrent pourrait-il écrire exactement cet article ?
2. Le lecteur repart-il avec quelque chose qu'il peut faire, vérifier ou décider ?
3. Chaque affirmation résisterait-elle à une vérification ?
4. Un fragment de 60 mots pris au hasard peut-il être copié dans une réponse d'IA en restant vrai, complet et attribuable ?
5. L'article sera-t-il encore vrai dans six mois, ou sait-il quand il doit être révisé ?

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| DataForSEO | volumes, concurrents réels, citations IA | suggestions de recherche gratuites, lecture manuelle des résultats |
| Search Console | position et impressions de l'existant | variables correspondantes laissées vides |

Pour produire une série d'articles sur un rythme régulier, passe par le skill `blog-pipeline`, qui orchestre celui-ci.
