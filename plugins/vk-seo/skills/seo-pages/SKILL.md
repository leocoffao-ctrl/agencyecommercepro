---
name: seo-pages
description: Optimise le SEO des pages qui rapportent — fiches produit, collections et page boutique d'un e-commerce, pages de service, de tarifs et de réalisations d'un site vitrine — (title, meta, H1, contenu, images, maillage, schema) et analyse la concurrence sur les requêtes transactionnelles et Google Shopping. À utiliser dès que l'utilisateur parle du SEO d'une fiche produit, d'une page de service, d'une collection, de la boutique, de Google Shopping, de prix concurrents, de mots-clés commerciaux ou de « pourquoi ma page ne ressort pas », même sans dire e-commerce.
---

# SEO des pages qui vendent

Adapté de `AgriciDaniel/claude-seo/skills/seo-ecommerce` (MIT). Check-list produit et pondération conservées ; étendu aux pages de service d'un site vitrine.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

Lis le type de site au contexte §1 : `ecommerce` suit la partie A, `vitrine` la partie B, `hybride` les deux.

## A. Page produit

Lis la page et, si la plateforme en expose, les données brutes du produit (prix, variantes, images, références).

**Title** (60 caractères au plus) — mot-clé principal, promesse, marque. Les requêtes réservées à chaque page sont au contexte §10.

**Meta description** (155 caractères au plus) — mot-clé, bénéfice, prix de départ ou condition forte (livraison, engagement), tirés du contexte §2.

**H1** unique, égal au nom du produit. Pas de H1 dupliqué par la navigation ou un gabarit partagé.

**Contenu** (200 mots uniques au moins, jamais la même description copiée entre produits) :
- à qui le produit convient, et à qui il ne convient pas ;
- ce qu'il contient ou ce qu'on reçoit, variante par variante ;
- un tableau récapitulatif ;
- une FAQ courte (livraison, usage, retour) ;
- les avis affichés en HTML, pas seulement injectés en JavaScript.

**Images** — trois au moins, texte alternatif descriptif, fichiers nommés, 800 px ou plus, chargement différé sauf la première.

**Maillage** — fil d'Ariane, liens vers les produits proches, les guides utiles et la page d'offre principale, ancres descriptives.

**Technique** — canonical sur l'URL courte du produit, une seule version indexable, vitesse mobile, un seul JSON-LD `Product` (voir `seo-schema`).

**Score sur 100** : schema 25 % · title et meta 15 % · images 20 % · contenu 20 % · maillage 10 % · technique 10 %.

### Collections et page boutique

- Introduction utile (aide au choix), 80 à 150 mots, texte complémentaire sous la grille si besoin.
- Pages de filtres et de tags : `noindex` ou canonical vers la collection.
- Nouvelles collections : seulement si un volume de recherche les justifie.

### Google Shopping et concurrence (DataForSEO, avec accord)

Règles du skill `seo-data` : pays et langue du projet, annonce du coût d'abord.

- Pages de résultats sur trois à cinq requêtes transactionnelles : qui est en première page, quels formats (Shopping, vidéos, questions associées).
- Mots-clés positionnés du domaine : quelles pages produit se positionnent, et sur quoi.
- Intersection de domaines contre un concurrent validé au contexte §10 : mots-clés produit qu'il a et pas nous.

Lecture des prix : situer l'offre face aux relevés, à unité comparable. Pas de conclusion sur un seul relevé.

## B. Page de service (site vitrine)

La page de service joue le rôle de la fiche produit : elle doit répondre à la requête et déclencher la prise de contact.

**Title** — prestation, lieu si l'activité est locale, marque.

**H1** unique — la prestation, dans les mots du client (contexte §5).

**Contenu** (400 mots uniques au moins) :
- le problème traité et pour qui ;
- le déroulé, étape par étape, avec les délais **datés** (« en moyenne, relevé le… ») ;
- le prix ou la fourchette, ou ce qui fait varier le devis ;
- deux ou trois réalisations liées, avec leurs chiffres ;
- les preuves autorisées au contexte §3 (certifications, assurances), jamais une preuve non sourcée ;
- une FAQ née des vraies questions reçues ;
- un seul appel à l'action, répété à deux endroits.

**Local** — nom, adresse, téléphone identiques partout (site, fiche d'établissement, annuaires). Zone d'intervention écrite en toutes lettres. Une page par prestation, pas une page par ville sans contenu propre.

**Images** — chantiers ou cas réels, texte alternatif qui décrit ce qu'on voit.

**Maillage** — services entre eux, service vers réalisations, guides vers service. Le blog ne vise jamais la requête d'une page de service.

**Schema** — `Service` relié à l'`Organization` ou au `LocalBusiness` du site (voir `seo-schema`).

**Score sur 100** : contenu 30 % · title, meta et H1 15 % · preuves et réalisations 20 % · local 15 % · maillage 10 % · technique et schema 10 %.

## Livrable

```
## SEO : [URL ou requête] — [date]
Score global XX/100 (détail par critère)
Title / meta / H1 actuels → proposés
Contenu : manques et plan (sections à ajouter)
Images : problèmes et corrections
Maillage : liens à créer (source → cible → ancre)
Schema : statut (renvoi à seo-schema)
Concurrence (si DataForSEO) : tableau, lecture, coût
Top 5 actions (effort S/M/L, impact)
```

Textes à rédiger : skill `copywriting`. Mises à jour en masse (meta, champs personnalisés) : par l'outil d'import de la plateforme, toujours avec un essai à blanc, en fusion et par petits lots.

## Dépendances

Sans DataForSEO : parties A et B complètes, la section concurrence se limite à la lecture manuelle des pages de résultats.
