---
name: blog-pipeline
description: Production régulière d'articles de blog de bout en bout — choix des sujets dans un backlog, recherche, rédaction SEO + GEO, contrôles automatiques, création des articles dans le CMS avec publication programmée, fichier d'import de secours et livraison d'un dossier par lot. Conçu pour tourner en tâche planifiée. À utiliser dès que l'utilisateur demande les articles de la semaine, un lot d'articles, un calendrier éditorial, un import d'articles, ou veut automatiser son blog, même sans dire pipeline.
---

# Pipeline de blog

Ce skill orchestre, il ne recopie pas. Il enchaîne des skills existants et ajoute ce qui leur manque pour tourner seuls : le choix des sujets, la mémoire d'un lot à l'autre, la création des articles dans le CMS, le fichier de secours et la livraison.

| Rôle | Skill | Ce qu'on y prend |
|---|---|---|
| Contexte | `brand-context` | offre, ton, affirmations autorisées, stack |
| Rédaction | `seo-writer` | Phases 0 à 6, structure, règles d'écriture, maillage, test final |
| Visibilité IA | `seo-geo` | citabilité, passages autonomes, fraîcheur |
| Audit | `seo-audit` | contrôles en direct (statuts, balises, schema) appliqués au lot |
| Données | `seo-data` | pays et langue, coûts, erreurs connues |

Charge-les dans cet ordre au début du run. Si l'un manque, continue avec les règles résumées ici et signale-le dans le récapitulatif.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## Constantes du projet

Elles vivent dans `kit.config.json`, bloc `blog`, jamais dans ce fichier :

- `delivery_folder` : dossier qui reçoit un sous-dossier par lot (Drive, ou dossier local) ;
- `backlog` : tableur ou CSV des sujets. Colonnes : `#, Semaine, Mot-clé principal, Requêtes secondaires, Titre de travail, Intention, Rôle, Pivot commercial, Liens obligatoires, Notes, Statut` ;
- `handle`, `path_prefix`, `author`, `template_suffix`, `platform_blog_id` : où et comment les articles se créent ;
- `articles_per_run`, `cadence_days`, `publish_time`, `timezone` : le rythme ;
- `theme_renders_h1`, `theme_emits_jsonld` : ce que le gabarit fait déjà.

Budget de données : `seo.run_budget_usd` par run, sans redemander. Au-delà : s'arrêter et le noter.

Le run ne modifie pas le backlog. L'état vit dans les `MANIFEST.json` des dossiers de lot : l'utilisateur garde la main sur le tableur, le pipeline garde la mémoire.

## Étape 1 — État et choix des sujets

1. Liste les sous-dossiers du dossier de livraison et lis chaque `MANIFEST.json` : slugs produits, mots-clés traités, dates prévues.
2. Récupère l'inventaire en ligne par le sitemap. C'est l'arborescence de référence : celle du contexte peut être en retard.
3. Lis le backlog. Prends les premières lignes dont le statut n'est ni « Fait » ni « Écarté », dont le mot-clé n'est dans aucun manifeste et dont le sujet n'est pas déjà couvert par une URL en ligne. Une ligne marquée « à valider » se saute tant qu'elle n'est pas repassée en « à produire ».
4. Saison : une ligne saisonnière dont la fenêtre tombe dans les dix jours passe devant.
5. Un sujet qui échoue en Phase 0 (même intention qu'une page existante) est remplacé par la ligne suivante, et le récapitulatif propose la mise à jour de la page existante.
6. Dates : un article tous les `cadence_days` jours à `publish_time`. Première date = la plus tardive entre la dernière date des manifestes et la dernière date programmée dans le CMS, plus un intervalle, et jamais avant le jour du run plus un intervalle.

## Étape 2 — Recherche, avant toute rédaction

Pour chaque sujet :
- suggestions de recherche gratuites pour le fan-out ;
- DataForSEO, dans le budget, pays et langue explicites : volumes de tout le lot en **un** appel ; page de résultats du mot-clé principal pour les concurrents réels ; si le budget le permet, une question posée au scraper ChatGPT pour voir qui les IA citent. Compte sans crédit : on continue sans, et le récapitulatif le dit ;
- lecture des cinq concurrents et des sources primaires. Aucun chiffre sans source vérifiée le jour même ;
- Search Console si le connecteur répond.

## Étape 3 — Rédaction

Applique `seo-writer` en entier, avec les écarts que le gabarit du site impose (contexte §7) :

1. **Pas de `<h1>` dans le corps** si le gabarit affiche déjà le titre. Le titre d'accroche devient le champ titre de l'article ; le title SEO va dans le champ SEO.
2. **Pas de commentaire HTML dans le corps.** Brief, faits et tâches vont dans `BRIEF-<slug>.md`.
3. **JSON-LD** : seulement les types que le gabarit n'émet pas.
4. **Chaque lien interne répond 200** au moment du run. Un lien vers un article du même lot est autorisé.
5. **Registre** : celui du contexte §5. Si les articles déjà publiés en utilisent un autre, signale-le une fois et suis le contexte.
6. Gabarit du corps, identique d'un article à l'autre : signature datée → bandeau de méthode si données périssables → réponse rapide (`id="reponse-rapide"`) → sommaire → bloc de données daté → sections H2 avec `id` → tableau de décision → checklist → limites → FAQ en `<details><summary>` → à lire ensuite → sources → JSON-LD.
7. Longueur indicative : 1 800 à 2 800 mots. Qualité avant volume : un article qui ne passe pas le test final ne sort pas, et le récapitulatif le dit.

## Étape 4 — Contrôles et fichier d'import

Écris chaque corps dans `<slug>.html` et un `manifest-lot.json` (format dans l'en-tête du script), puis :

```bash
python3 scripts/build_articles.py manifest-lot.json "Blog Posts - <marque> <AAAA-MM-JJ>.csv" \
  --config brand/kit.config.json --format matrixify
```

`--format json` produit un lot neutre pour un autre CMS. Le script bloque (code 1) sur les erreurs listées dans `seo-writer`, Phase 5. Corrige et relance jusqu'au code 0. Joins la sortie au récapitulatif, avec la checklist remplie.

Notes sur le format Matrixify (Shopify) :
- CSV UTF-8 dont le nom contient « Blog Posts ». CSV et non tableur : une cellule de tableur plafonne à 32 767 caractères.
- `Command = NEW` : la ligne échoue si le slug existe, donc aucun article publié n'est écrasé.
- `Published = FALSE` : l'article arrive masqué.
- Toujours un essai à blanc avant l'import réel.

## Étape 4 bis — Création dans le CMS

Seulement si le script sort en code 0, et seulement si l'utilisateur a autorisé la création directe (contexte §9).

**Shopify (connecteur Shopify)**
1. Suis le déroulé du connecteur : schéma (`ArticleCreateInput`) → validation → exécution.
2. Vérifie le suffixe de gabarit sur les derniers articles du blog avant d'écrire.
3. Anti-doublon : cherche chaque slug. S'il existe, ne le recrée pas et ne le modifie pas.
4. Un `articleCreate` par article, dans l'ordre des dates, avec le corps exact du fichier, le résumé, les tags, le suffixe de gabarit, la date de publication future au fuseau du projet, et les champs SEO.
5. La publication est **programmée**, jamais immédiate. Un article qui porte un doute factuel bloquant est créé masqué, sans date, et signalé.
6. Relis chaque article créé : slug (la plateforme peut le suffixer), gabarit, date, champs SEO, longueur du corps. Tout écart va au récapitulatif. Ne corrige que les articles créés dans ce run.

**WordPress (API REST ou connecteur)** : même logique avec `status: future` et la date programmée ; champs SEO par l'extension en place.

**Autre CMS ou pas de connecteur** : le fichier d'import ou le lot JSON est la voie de publication, et le récapitulatif l'annonce en tête.

Si une création est refusée, reste en attente ou renvoie une erreur : n'insiste pas et ne recrée pas en boucle. Bascule sur le fichier de secours et liste ce qui a été créé et ce qui ne l'a pas été.

## Étape 5 — Livraison

Crée un sous-dossier `S<semaine ISO> — <date du premier créneau>` et déposes-y :

1. le fichier d'import de secours ;
2. `<slug>.html` pour chaque article ;
3. `BRIEF-<slug>.md` pour chaque article : Phase 0 complète, tableau `FAIT | SOURCE | DATE DE RELEVÉ | CERTITUDE`, tableau de maillage, liens retour à poser, prompt d'image, sortie du script et checklist ;
4. `RECAP.md` : articles (titre, slug, title, date prévue), état dans le CMS (créé et programmé, avec son identifiant, ou non créé et pourquoi), ce qu'il reste à faire à la main (relecture, visuels, liens retour), alertes (sujet écarté, compte de données à sec, skill manquant, anomalie repérée sur le site), coût de données du run ;
5. `MANIFEST.json` : `[{"n_backlog": …, "mot_cle": "…", "handle": "…", "date_prevue": "…", "cms_id": "… ou null"}]`. C'est la mémoire des runs suivants : ne jamais l'oublier.

Réponse finale du run : cinq lignes au plus, le lien du dossier, les titres, l'état dans le CMS, les alertes.

## Garde-fous

- Le pipeline programme, il ne publie jamais immédiatement.
- Il ne supprime rien, ne modifie aucun article existant, aucun thème, aucun gabarit.
- Il ne souscrit à aucun plan payant.
- Il ne vise aucune requête d'une page commerciale protégée.
- En cas de doute bloquant, il livre moins d'articles, solides, et le dit.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| CMS (Shopify, WordPress) | articles créés et programmés | fichier d'import à charger à la main |
| Stockage (Drive) | dossier de lot partagé, mémoire entre runs | dossier local, à conserver d'un run à l'autre |
| DataForSEO | volumes et concurrents réels | recherche gratuite, signalée comme telle |
| Tableur de backlog | sujets choisis par l'utilisateur | l'utilisateur donne les sujets dans la conversation |
