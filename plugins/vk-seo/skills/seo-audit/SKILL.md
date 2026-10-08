---
name: seo-audit
description: Audit SEO complet d'un site e-commerce ou vitrine — indexabilité, balises, contenus, architecture, données structurées, performance, visibilité IA — à partir d'un crawl, de la Search Console, d'un échantillon de pages en direct et de DataForSEO, puis plan d'action priorisé en quatre phases. À utiliser dès que l'utilisateur demande un audit SEO, un bilan du site, un état des lieux, un check technique, « qu'est-ce qui ne va pas sur le site », une analyse du trafic organique ou une liste d'actions SEO, même sans dire « audit ».
---

# Audit SEO

Adapté de `AgriciDaniel/claude-seo/skills/seo-audit` (MIT). Structure en catégories, score de santé et plan en quatre phases conservés. Les sous-agents et scripts locaux du dépôt d'origine (crawl, Playwright, rapports PDF) sont remplacés par les sources dont l'utilisateur dispose réellement.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 1. Sources, par ordre de fiabilité

1. **Crawl** fourni par l'utilisateur (export Screaming Frog, Sitebulb ou équivalent). Un crawl complet part rarement bien depuis un environnement cloud : beaucoup de plateformes répondent 429 aux adresses de centres de données. Sans export, demande-le ou fais un audit partiel en le disant.
2. **Search Console**, par le connecteur disponible (contexte §8) : performances, pages, requêtes, appareils, historique des positions.
3. **Échantillon en direct** : 10 à 20 URL représentatives (accueil, offre principale, deux fiches produit ou pages de service, liste ou collection, deux articles, pages légales), plus `robots.txt`, `sitemap.xml` et ses sous-sitemaps.
4. **DataForSEO**, selon les règles du skill `seo-data` (accord avant dépense) : analyse de page, Lighthouse, mots-clés positionnés, vue d'ensemble du domaine.

Chaque constat indique sa source et sa date. Une source absente rend la catégorie concernée « non mesurée », pas « bonne ».

## 2. Grille

Présente les chiffres en valeur **et en pourcentage**, avec une comparaison (période précédente, groupe de pages, objectif).

**Indexabilité** — statuts HTTP (2xx, 3xx, 4xx, 5xx), pages indexables et non indexables, non canoniques, noindex, chaînes de redirection. Couverture du sitemap : URL listées non crawlées, et l'inverse.

**Balises** — title, meta description, H1 : manquants, dupliqués, trop longs, par groupe de pages.

**Contenu** — nombre de mots par groupe, pages minces, duplication entre pages proches. Deux pages qui se concurrencent se signalent ; on ne supprime rien, l'utilisateur tranche.

**Architecture** — profondeur de clic, maillage interne, pages orphelines, liens vers des 404.

**Données structurées** — types présents par gabarit, doublons, erreurs. Détail par le skill `seo-schema`.

**Partage** — Open Graph et cartes sociales présents et justes.

**Performance** — poids de page, LCP, INP et CLS sur mobile, images non optimisées, scripts tiers.

**Visibilité IA** — accès des robots IA et citabilité, en résumé. Détail par le skill `seo-geo`.

## 3. Points propres à la plateforme

Lis la plateforme dans le contexte §7 et applique la liste qui correspond.

**Shopify**
- `/collections/*/products/*` : canonical vers `/products/*`.
- Pages de tags et collections filtrées : indexation à maîtriser.
- `/search`, `/cart`, `/account` : non indexables par défaut, à vérifier.
- Slugs abîmés par des caractères accentués : proposer un slug propre et une 301, sans rien supprimer.
- Pages de politique générées par défaut : vérifier qu'elles ne contredisent pas les CGV.

**WordPress / WooCommerce**
- Archives d'auteur, de date et de tags : indexation à maîtriser.
- Pagination et paramètres de tri : canonical cohérent.
- Pages jointes aux médias (attachment) : redirigées vers le fichier ou la page parente.
- Extensions SEO en double qui émettent deux jeux de balises ou de schema.

**Site statique ou autre**
- Barres obliques finales et casse : une seule forme par URL.
- En-têtes de cache et compression.
- Sitemap et `robots.txt` réellement servis à la racine.

Ajoute les règles locales du contexte §7 (gabarits inertes, sections partagées, conventions de nommage).

## 4. Score et priorités

Score de santé sur 100, pondéré : technique et indexabilité 30 % · contenu 20 % · balises 15 % · schema 10 % · performance 15 % · visibilité IA 10 %. Un score par catégorie avec « ce qui marche » et « ce qui coince ». Une catégorie non mesurée sort du calcul, et le score le dit.

Ce score est une heuristique de travail, pas un signal de Google : écris-le.

Sévérités : Critique (bloque l'indexation, la vente ou la prise de contact) > Haute > Moyenne > Basse > Info.

Plan en quatre phases : 1. Corrections critiques (semaine 1) · 2. Améliorations à fort impact (semaines 2 et 3) · 3. Contenu et autorité (mois 2) · 4. Suivi (continu).

Si l'utilisateur parle d'objectif de trafic, reprends l'horizon inscrit au contexte §10. S'il n'y en a pas, donne une fourchette prudente et la dépendance principale (volume du marché, autorité du domaine), sans promettre.

## 5. Livrables

- `AUDIT-SEO-<marque>-<date>.md` : synthèse, score, tableaux par catégorie, plan d'action.
- `actions.csv` : `titre;catégorie;sévérité;effort;page(s);preuve;recommandation`.
- Sur demande : création des actions dans l'outil de tâches du contexte §8, par petits lots, après avoir vérifié qu'une action équivalente n'existe pas déjà.
- Sur demande : rapport PDF (HTML vers PDF en attendant `document.fonts.ready`, contrôle visuel des pages).

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Export de crawl | grille complète | audit partiel sur échantillon, annoncé comme tel |
| Search Console | trafic et positions réels | catégories de trafic non mesurées |
| DataForSEO | Lighthouse, mots-clés positionnés | performance estimée sur l'échantillon |
| Outil de tâches | actions créées directement | `actions.csv` à importer |
