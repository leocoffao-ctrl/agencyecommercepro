---
name: site-clone
description: Reprend le style d'un site de référence (mise en page, rythme, typographie, interactions) et le reconstruit aux couleurs de la marque, d'abord en maquette puis dans la technologie du site (section Shopify, gabarit WordPress, composant statique). On prend la structure et le comportement, jamais le contenu ni l'identité. À utiliser dès que l'utilisateur partage l'URL d'un site qu'il aime, dit « je veux une page comme celle-là », « refais ce design pour ma marque », « inspire-toi de ce site », « clone ce style », ou veut refondre une page à partir d'une référence visuelle, même sans dire « clone ».
---

# Clone de style → page de la marque

Adapté de `JCodesMore/ai-website-cloner-template` (MIT). Le dépôt d'origine clone un site au pixel près, contenus et images compris. Ici on garde la méthode d'extraction et on change la cible : **on prend la structure et le comportement, jamais le contenu ni l'identité**, et on livre du code qui s'intègre au site existant.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

Regarde aussi les fichiers de marque indiqués au contexte §6 : charte, logos, visuels.

## Ce qu'on reprend, ce qu'on ne reprend pas

| On reprend | On ne reprend jamais |
|---|---|
| Grille, rythme vertical, espacements, proportions | Textes, slogans, noms de produits |
| Hiérarchie typographique (tailles, graisses, interlignes) | Logos, pictogrammes de marque, photos, illustrations |
| Types de composants (hero, cartes, onglets, carrousel) | Polices sous licence payante (on prend un équivalent libre) |
| Interactions (collant, survol, apparition au défilement) | Couleurs du site source (remplacées par la palette de la marque) |
| Logique de parcours (où sont les appels à l'action, ordre des arguments) | Toute combinaison qui rendrait la page reconnaissable comme la leur |

Si la référence est un concurrent direct, dis-le et pousse la transformation plus loin : une page qui rappelle trop un concurrent coûte en crédibilité.

## Déroulé

### 1. Cadrage — une question au plus si c'est flou
- URL de référence et zone visée (page entière ou une section).
- Page cible sur le site de la marque.
- Ce qui plaît dans la référence. Si ce n'est pas dit, propose trois hypothèses et avance avec la plus probable.

### 2. Extraction
Selon les outils disponibles, dans cet ordre :

1. **Navigateur** : captures à 1440 px et 390 px, puis le script d'extraction de styles calculés de `references/extraction.md` sur chaque bloc. C'est la méthode fidèle.
2. **Sans navigateur** : lecture de la page et de ses feuilles de style (tailles, espacements, points de rupture, transitions). Moins précis : annonce-le.

Pour chaque section, note dans `topologie.md` : ordre, rôle, modèle d'interaction (statique, clic, défilement, temps), états (survol, collant, onglets), comportement mobile. Le modèle d'interaction se vérifie **avant** de construire : un bloc piloté par le défilement refait en onglets cliquables, c'est une réécriture complète.

### 3. Traduction en tokens de la marque
Construis la table de correspondance et montre-la :

| Rôle | Valeur source | Valeur de la marque (contexte §6) |
|---|---|---|
| Fond principal | … | … |
| Accent, appel à l'action | … | … |
| Texte | … | … |
| Titres | … | … |
| Texte courant | … | … |
| Rayons, ombres | … | … |

Garde les proportions et le rythme de la source ; applique l'univers visuel de la marque. Écarte d'emblée les directions notées « à ne jamais proposer ».

### 4. Maquette
Un fichier HTML autonome avec le **vrai contenu** : vraies offres, vrais prix lus sur la source de vérité du contexte §2, vraie voix. Pas de faux texte. Ordinateur et mobile. L'utilisateur valide avant toute conversion.

### 5. Conversion dans la technologie du site
Seulement après validation, selon la plateforme du contexte §7.

**Shopify** — règles du skill `shopify-liquid` : nouvelle section à côté de l'existante, CSS et JS dans `assets/`, tout texte et toute image éditables par `{% schema %}`, images avec `widths` et `sizes`, gabarit JSON qui référence la section.

**WordPress** — nouveau gabarit ou nouveau bloc dans le thème enfant, champs éditables par l'outil de champs en place, styles en file d'attente, test en préproduction.

**Site statique** — composant isolé, contenu dans les données ou le front matter, styles limités au composant.

Dans tous les cas : rien de l'existant n'est remplacé avant la bascule.

### 6. Livraison
- Fichiers rangés selon l'arborescence du site, plus la maquette.
- `INTEGRATION.md` : fichiers à créer (chemin exact), ordre, test à faire, retour arrière possible.
- Validation par le relecteur du contexte §1 avant mise en production.

## Contrôle final
- La page est-elle encore reconnaissable comme le site source ? Si oui, retravailler.
- Contraste texte sur fond de 4,5:1 au moins.
- Mobile à 390 px vérifié, aucune couleur hors palette, un seul H1.

## Pour aller plus loin en design

Ce plugin ne redistribue pas de skill de goût ou de critique d'interface. Ceux qui ont servi de référence pendant la construction du kit sont listés, avec leurs auteurs et leurs licences, dans `docs/dependances-design.md` à la racine du dépôt.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Navigateur | extraction des styles calculés, captures | lecture du HTML et du CSS, annoncée comme moins précise |
