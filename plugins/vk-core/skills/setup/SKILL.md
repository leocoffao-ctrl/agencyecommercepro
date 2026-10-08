---
name: setup
description: Installe le kit sur un nouveau projet — interviewe l'utilisateur, lit son site s'il existe, puis écrit brand/brand-context.md et brand/kit.config.json que tous les autres skills vk-* utilisent. À utiliser au premier lancement, quand un skill signale que le contexte de marque est introuvable, ou dès que l'utilisateur dit « on démarre », « nouveau projet », « configure le kit », « je lance un site », « je veux créer une boutique », même sans dire setup.
---

# Setup — cadrer un projet

Tu produis deux fichiers : `brand/brand-context.md` (lu par les skills) et `brand/kit.config.json` (lu par les scripts). Rien d'autre ne démarre proprement sans eux.

## Principe

Ce qu'un site dit déjà ne se demande pas. Ce que seul l'utilisateur sait se demande une fois. Ce que personne ne sait encore reste marqué `A_COMPLETER` ou `[hypothèse]` : un contexte incomplet et honnête vaut mieux qu'un contexte plein de suppositions.

## 1. Lire avant de demander

Si un site existe, lis-le d'abord :

- Accueil, page d'offre principale, deux fiches produit ou prestation, À propos, mentions légales, CGV, `robots.txt`, `sitemap.xml`.
- Boutique : flux public de produits s'il existe (Shopify `/products.json?limit=250`, WooCommerce `/wp-json/wc/store/v1/products`).
- Relève : graphie de la marque, offre et prix, conditions, registre (tu ou vous), couleurs et typographies du CSS, plateforme, outils visibles dans la source (avis, abonnement, réservation, email).

Tout ce que tu en tires porte sa source et sa date dans le fichier.

Si aucun site n'existe, passe directement à l'interview et note en tête que le contexte décrit un projet, pas un existant.

## 2. Interview

Quatre blocs, dans cet ordre. Pose un bloc à la fois, propose des réponses quand le site en suggère, accepte « je ne sais pas encore ».

**Bloc A — l'activité**
- Que vends-tu ou que proposes-tu, à qui, où ?
- Qu'est-ce qu'on te prête à tort ? (Ce que la marque ne fait pas : c'est la source des erreurs les plus coûteuses dans les textes.)
- Site e-commerce, site vitrine, ou les deux ?

**Bloc B — les clients et les preuves**
- Deux ou trois profils de clients : situation, frein principal, porte d'entrée.
- Qu'as-tu le droit d'affirmer, et d'où vient chaque chiffre ?
- Qu'est-ce que tu ne peux pas promettre aujourd'hui ?

**Bloc C — la voix et l'image**
- Tutoiement ou vouvoiement ? Trois adjectifs pour le ton.
- Mots que tu ne veux jamais lire.
- Couleurs, typographies, univers visuel. Directions déjà écartées.

**Bloc D — la technique et la méthode**
- Plateforme, thème, où l'on travaille (thème publié ou copie), ce qui est interdit sans demande.
- Outils branchés. Connecteurs disponibles dans Claude.
- Qui valide avant mise en ligne. Enchaîner les étapes ou valider à chaque fois.

Ne pose pas les questions de SEO, de réseaux ou de conformité si l'utilisateur n'en est pas là : laisse les sections 10 à 12 en `A_COMPLETER` avec une phrase qui dit quel skill les remplira.

## 3. Écrire les fichiers

1. Pars de `brand-context.template.md` et de `kit.config.template.json` (dossier `references/` du skill `brand-context`).
2. Remplis chaque section avec des faits. Une supposition utile s'écrit `[hypothèse]`. Un fait manquant s'écrit `A_COMPLETER`.
3. Date de fraîcheur en tête, au jour de l'interview.
4. Dans `kit.config.json` : nom, domaine canonique, langue, pays, devise, registre, type de site, plateforme, mots bannis, puis les blocs `blog`, `directory`, `social` seulement s'ils servent.
5. Aucune clé d'API, aucun mot de passe. Les identifiants de comptes et de dossiers vont dans `kit.config.json` ; les secrets dans des variables d'environnement.
6. Si le projet est versionné, vérifie que `brand/` n'est pas ignoré par Git et que rien de confidentiel (marges, listes de prospects) n'y entre sans accord.

## 4. Relire avec l'utilisateur

Montre le résultat en trois parties courtes :

- **Ce que je tiens pour sûr** : cinq à dix lignes, avec leur source.
- **Mes hypothèses** : à confirmer ou à corriger.
- **Ce qui manque** : par ordre de gêne, avec le skill bloqué par chaque manque.

Corrige, puis donne la suite : le skill `start` propose la première étape adaptée au type de site.

## 5. Mettre à jour plus tard

Relance ce skill en mode « mise à jour » quand l'offre, les prix ou la stack changent : relis le site, compare au fichier, liste les écarts, applique ceux que l'utilisateur valide, mets à jour la date de fraîcheur.
