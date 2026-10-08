---
name: directory-pages
description: Produit ou refond les pages d'un annuaire sur des entités tierces (marques, artisans, producteurs, lieux, prestataires) — collecte de données sourcées et datées, rédaction en 20 blocs autonomes, JSON-LD, métadonnées, générateur HTML, contrôles automatiques et score sur 100. À utiliser dès que l'utilisateur parle de fiche, d'annuaire, de page partenaire, de fiche de lieu ou de fournisseur, d'une liste de priorités de fiches, de se positionner sur le nom d'une marque tierce ou d'ouvrir un partenariat grâce à une fiche, même sans citer le prompt master.
---

# Pages d'annuaire

La référence complète est `references/prompt-master.md`. **Lis-la en entier avant la première fiche d'une session** : raisonnement, architecture en 20 blocs, volumétrie, règles de rédaction, liens, schema, métadonnées, garde-fous juridiques, checklist et grille de score. Ce fichier décrit seulement le déroulé.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

Le type d'entité traité (libellé, page pivot, préfixe d'URL, type de schema, seuils) se déclare dans `kit.config.json`, bloc `directory.types`. Un projet peut en avoir plusieurs (par exemple « producteur » et « boutique »).

## Déroulé pour chaque entité

### 1. Cadrage
Si une liste de priorités existe, lis la ligne de l'entité : slug cible, URL existantes, état d'indexation, prérequis technique (redirection, fusion), statut de partenariat. Les prérequis vont dans le rapport de livraison : la fiche ne se publie pas avant.

Si une fiche existe déjà en ligne, récupère-la : elle donne des pistes, **mais ce n'est pas une source**. Tout fait repris se revérifie, et les écarts constatés se signalent.

Pour un lieu, qualifie d'abord (prompt master §1.4) : existe-t-il encore sous cette enseigne ? Un domaine a-t-il changé de mains ?

### 2. Fiche de données — rien n'est rédigé avant
Sources autorisées, dans l'ordre du prompt master §1.2. Jamais d'annuaire tiers ni d'agrégateur.

Techniques qui marchent :
- **Offre et prix** : flux publics de la boutique de l'entité quand ils existent (WooCommerce `/wp-json/wc/store/v1/products`, Shopify `/products.json`), sinon lecture des pages de catégorie. Calcule toujours le prix unitaire comparable et note la disponibilité.
- **Création, forme juridique** : registre officiel des entreprises du pays, à partir de l'identifiant lu dans les mentions légales du site officiel.
- **Identifiant de lieu, note, horaires** : outil de recherche de lieux, sur l'adresse exacte. Note, nombre d'avis et date de relevé. Plusieurs établissements = plusieurs identifiants. Croise le site et la fiche d'établissement : les horaires divergent souvent, signale-le.
- **Histoire** : page de présentation, blog officiel, presse relayée par l'entité (remonte à l'article original).
- **Comptes sociaux** : ceux affichés sur le site officiel.

Écris la fiche de données en YAML avec, pour chaque champ, la valeur, la source et la date. Champ inconnu = vide, et le bloc correspondant disparaît ou le dit (« non communiqué »).

### 3. Rédaction
- Ordre des 20 blocs imposé. Bloc 10 **supprimé** sans relevé avec protocole. Bloc 12 toujours présent.
- Graphie canonique = celle du site officiel.
- Chaque bloc renomme l'entité en ouverture. H2 = question ou affirmation complète.
- Prix seulement dans le tableau daté et dans le bloc qui les commente.
- Comparatif : deux entités présentes dans l'annuaire, proches par la spécialité ou la région, prix relevés le même jour sur leurs sites officiels.
- Ton, registre et vocabulaire banni : contexte §5.
- Paraphrase les descriptions officielles.

Écris le contenu dans `contenu-<slug>.json` (format : `references/format-contenu.md`, exemple : `references/exemple-contenu.json`).

### 4. Générer et contrôler

```bash
python3 scripts/build_fiche.py contenu-<slug>.json sortie/ --config brand/kit.config.json
python3 scripts/check_fiche.py sortie/fiche-<slug>.html sortie/schema-<slug>.json \
  --config brand/kit.config.json --type <type>
```

Corrige jusqu'à zéro alerte bloquante, puis vérifie que chaque URL interne répond 200.

### 5. Livrables
1. `fiche-<slug>.html` : corps de l'article, HTML servi, zéro script, sans `<style>` ni commentaire.
2. `schema-<slug>.json` : `Article` avec `about`, `BreadcrumbList` vers la page pivot, `FAQPage` identique à la FAQ visible, `ItemList` de l'offre.
3. `donnees-<slug>.yaml` : fiche de données sourcée.
4. `livraison-<slug>.md` : métadonnées, redirections à faire avant publication, résultat des contrôles, score détaillé sur 100, questions ouvertes.

### 6. Questions à poser, une fois, en fin de livraison
Seulement ce qui bloque : relevés de test de la marque, présence dans l'offre, photo principale et ses droits, fourchette de marché de référence, arbitrages de slug et de redirection.

## Installation côté site

- `assets/fiche.css` : feuille de style des fiches, à charger par le gabarit des articles d'annuaire. Six variables de couleur à régler sur la palette du contexte §6.
- Un champ personnalisé d'article reçoit le JSON-LD, sorti par le gabarit s'il est rempli.
- Si la page pivot est tenue à la main, chaque nouvelle fiche doit y être ajoutée.

## Pièges fréquents

- Un annuaire existant compte souvent des dizaines de fiches très courtes : ce sont des brouillons, pas des sources.
- Des lieux ferment, changent de nom ou de propriétaire : vérifier avant d'écrire.
- Des domaines sont rachetés : contrôler chaque lien sortant.
- Des entités figurent dans deux types : choisir une page principale et rediriger l'autre.
- Une page de vente au nom de l'entité peut exister mais être vide : l'appel à l'action part alors vers l'offre générale, et la page vide se signale.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Recherche de lieux | identifiant de lieu, note et horaires datés | à fournir par l'utilisateur ; le contrôle du lien de carte bloque sinon |
| DataForSEO, Search Console | volumes sur les noms, positions des fiches | ordre de priorité à fournir |
| CMS | création directe de l'article | fichiers à coller |
