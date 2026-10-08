---
name: seo-schema
description: Audite, corrige et génère les données structurées JSON-LD d'un site — Product et Offer, Organization, LocalBusiness, Service, BlogPosting, CollectionPage, Event, BreadcrumbList — en traitant les doublons émis par le thème ou les extensions et en refusant toute donnée invisible ou invérifiable. À utiliser dès que l'utilisateur parle de schema, de JSON-LD, de données structurées, de rich results, d'extraits enrichis, du test des résultats enrichis ou de microdonnées, même sans dire « schema ».
---

# Données structurées

Adapté de `AgriciDaniel/claude-seo/skills/seo-schema` et de la section schema de `seo-ecommerce` (MIT). Règles de validation et statut des types (actifs, retirés) conservés.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 1. Détecter ce qui existe, toujours avant de générer

Lis la page et relève :
- chaque `<script type="application/ld+json">` : type et source probable (thème, extension, section maison, champ personnalisé) ;
- les microdonnées (`itemscope`, `itemprop`) ;
- les doublons de `Product`, `Organization`, `BreadcrumbList`.

Compare avec ce que le contexte §7 annonce comme déjà émis.

**Règle** : un seul bloc par entité et par page. Si on active un schema maison, on désactive l'autre source et on le note dans le livrable. Pas d'`aggregateRating` ni de `review` tant qu'aucune source d'avis ne les affiche réellement sur la page.

## 2. Types par page

| Page | Types |
|---|---|
| Fiche produit à variantes | `ProductGroup` (`variesBy`) + `hasVariant` → `Product` par variante, ou `Product` + une `Offer` par variante si plus simple |
| Produit par abonnement | `Product` + `Offer` (prix de départ), récurrence décrite dans la description ; aucune propriété d'abonnement inventée |
| Collection, page boutique | `CollectionPage` + `ItemList` + `BreadcrumbList` |
| Accueil | `Organization` (+ `WebSite`) |
| Entreprise qui reçoit du public | `LocalBusiness` ou son sous-type exact, avec adresse et horaires vérifiés |
| Page de service | `Service` relié au fournisseur (`provider`), zone desservie |
| Article, guide | `BlogPosting` ou `Article` (auteur, dates, image) + `BreadcrumbList` |
| Page d'annuaire sur un tiers | `Article` dont `about` décrit l'entité (voir `directory-pages`). Jamais le type commercial de l'entité en racine : le site écrit sur elle, il n'est pas elle |
| Événement, atelier daté | `Event` seulement si les dates sont réelles et à jour ; sinon `Service` |

`FAQPage` et `HowTo` : voir `references/types-deprecies.md` avant d'en proposer. Les résultats enrichis correspondants ont été retirés ; on ne les ajoute pas pour le SERP.

## 3. Règles de validation

1. `@context` `https://schema.org`, URL absolues sur le domaine canonique du contexte §1.
2. `price` en nombre sans symbole, point décimal ; `priceCurrency` selon le contexte.
3. `availability` en URL complète, cohérente avec le stock réel.
4. `image` : URL haute définition, 1200 px de large si possible.
5. `brand` : la marque du site pour ses propres produits ; pour un produit d'un tiers, la marque du fabricant.
6. `shippingDetails` : zones, tarifs et délais **demandés**, jamais devinés. Fait manquant = `A_COMPLETER` visible.
7. `hasMerchantReturnPolicy` : seulement si la politique publiée est cohérente avec les conditions de vente. Sinon, le signaler et ne rien générer.
8. `Organization` : nom, raison sociale, URL, logo, `sameAs` vérifiés, adresse. Les identifiants légaux viennent du contexte §1, jamais d'une recherche approximative.
9. Aucune donnée absente de la page ou invérifiable.

Types retirés ou dépréciés : `references/types-deprecies.md`.

## 4. Intégration

**Shopify** — un snippet par gabarit, rendu dans la section, alimenté par les objets Liquid (`product.variants`, `variant.sku`, prix sans devise avec point décimal, image en 1200 px). Toujours échapper avec `| json`. Pour les pages éditoriales : un champ personnalisé qui contient le JSON-LD, rempli par import avec essai à blanc.

**WordPress** — un seul émetteur : l'extension SEO **ou** le thème, pas les deux. Le complément passe par le filtre de l'extension, pas par un second bloc.

**Site statique** — un composant par type, données dans le front matter, JSON sérialisé au moment du build.

Dans tous les cas : tester chaque gabarit dans le test des résultats enrichis et le validateur schema.org avant diffusion, et noter le résultat.

## 5. Livrable

1. Inventaire actuel : page → blocs trouvés → source → problème.
2. JSON-LD proposé, validé, avec `A_COMPLETER` visible pour tout fait manquant.
3. Code d'intégration pour la plateforme du contexte §7.
4. Sources à désactiver et impact.
5. Tests faits, tests à refaire après mise en ligne.

## Dépendances

Aucun connecteur requis. La validation finale dans les outils de test en ligne reste à faire par l'utilisateur si le navigateur n'est pas disponible.
