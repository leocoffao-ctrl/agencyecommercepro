---
name: copywriting
description: Rédige ou réécrit les textes d'un site (accueil, fiche produit, page de service, page d'offre ou d'abonnement, collection, réalisation, bannière) dans le ton et le vocabulaire du contexte de marque. À utiliser dès que l'utilisateur demande d'écrire, réécrire, améliorer ou raccourcir un texte de page, un titre, un hero, un appel à l'action, une accroche, une description de produit ou de prestation, une proposition de valeur, ou dit « ce texte est mou », même sans parler de copywriting. Pour les emails voir email-flows, pour les pubs ad-creative, pour les pages d'annuaire directory-pages.
---

# Copywriting de pages

Adapté de `coreyhaines31/marketingskills/skills/copywriting` (MIT). La logique d'origine (clarté, bénéfices, spécificité, langage du client, une idée par section) est gardée ; les exemples sont remplacés par des règles qui se remplissent avec le contexte de marque.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 1. Cadrer, sans reposer ce que le contexte dit déjà

- Quelle page, quelle action unique attendue (ajout au panier, demande de devis, prise de rendez-vous, inscription) ?
- D'où vient le visiteur et que sait-il déjà ?
- Quel profil du contexte §4 vise-t-on en priorité ?

Pour une réécriture, récupère d'abord le texte en ligne pour partir du réel.

## 2. Principes

**Clair avant malin.** En cinq secondes, le visiteur comprend ce que c'est, pour qui, et pourquoi c'est mieux que ce qu'il fait aujourd'hui. Vérifie en particulier la confusion à éviter notée au contexte §1.

**Bénéfice avant caractéristique.** La caractéristique dit ce que c'est ; le bénéfice dit ce que ça change pour le client. L'idéal : le bénéfice d'abord, la preuve ensuite.

**Concret et précis.** Un détail vérifiable vaut dix adjectifs. Décris dans l'ordre de la hiérarchie d'information du contexte §5.

**Langage du client.** Emploie les mots relevés au contexte §5. Le jargon du métier s'explique en une demi-phrase la première fois.

**Honnête.** Seulement les affirmations autorisées du contexte §3. Pas de faux compteur, pas de faux avis, pas de superlatif sans preuve.

## 3. Règles d'écriture

1. Simple : le mot courant plutôt que le mot administratif.
2. Actif : un sujet qui fait quelque chose.
3. Pas de remplissage : supprime « vraiment », « très », « véritable », « unique ».
4. Ponctuation et emojis selon le contexte §5.
5. L'humour de marque, s'il existe, ne passe jamais avant l'information de prix, de délai ou d'engagement.
6. Chiffres en chiffres, prix et dates au format du pays.

## 4. Structure par type de page

**Accueil** — Hero : promesse, preuve, appel à l'action principal, appel secondaire pour les indécis. Puis : comment ça marche en trois étapes, l'offre par besoin, les preuves réelles, la FAQ des objections, l'appel final.

**Fiche produit** — H1 = nom du produit. Sous-titre = à quoi il sert, en une phrase. Au-dessus du bouton : ce qu'on reçoit, variante par variante, et la condition qui rassure (livraison, retour, garantie) si elle est autorisée. Puis : pour qui, pour qui pas, détails, FAQ.

**Page de service** (site vitrine) — H1 = la prestation dans les mots du client. Puis : le problème traité, le déroulé avec des délais datés, le prix ou ce qui fait varier le devis, deux réalisations chiffrées, les preuves autorisées, la FAQ, un seul appel à l'action.

**Offre récurrente ou abonnement** — Lever les trois peurs : l'engagement, l'adéquation (« et si ça ne me convient pas »), le prix. Montrer ce qui arrive et quand.

**Collection, liste d'offres** — Une phrase d'introduction qui aide à choisir, pas un texte de référencement plaqué.

**Réalisation, étude de cas** — Contrainte de départ, solution, chiffres, durée. Pas d'adjectifs.

**Contenu éditorial** — Informatif d'abord ; le lien vers l'offre vient en fin de section quand il est pertinent.

## 5. Titres et appels à l'action

Formules, à remplir avec des faits du contexte :
- « [Catégorie] [bénéfice], [modalité] »
- « [Question sur la douleur, dans les mots du client] »
- « [Résultat] sans [frein] »

Appel à l'action : verbe et ce qu'on obtient. Oui : « Recevoir mon devis », « Choisir mon format », « Réserver ma place ». Non : « Valider », « En savoir plus », « Cliquez ici ».

## 6. Livrable

Pour chaque section :
```
[Section] — rôle
Texte proposé
Pourquoi : 1 ligne
```
Pour le H1, le sous-titre et l'appel principal : deux ou trois variantes avec l'angle de chacune.

En fin de livrable : `title` (60 caractères au plus) et `meta description` (155 au plus), à confirmer avec le skill `seo-pages` ; la liste des affirmations utilisées et leur source ; les points à valider (chiffre, avis, prix).

Relis le tout : jargon non expliqué ? phrase qui fait deux choses ? superlatif sans preuve ? Corrige avant de livrer.

## Dépendances

Aucun connecteur requis. Avec l'accès au site, la réécriture part du texte réellement en ligne.
