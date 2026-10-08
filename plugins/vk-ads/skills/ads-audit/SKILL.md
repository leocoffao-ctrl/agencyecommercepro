---
name: ads-audit
description: Audit en lecture seule des campagnes publicitaires d'une marque (Meta et Instagram, Google Ads, et au besoin TikTok, Pinterest, YouTube) — suivi des conversions, attribution, structure, créas, budgets, rentabilité face au panier et à la valeur client — à partir d'exports, de captures ou d'un connecteur. Ne modifie jamais une campagne. À utiliser dès que l'utilisateur parle d'audit pub, de ROAS, de CPA, de campagnes qui ne rentabilisent pas, de pixel, de conversions qui remontent mal, de budget pub, ou avant de relancer de la publicité, même sans dire « audit ».
---

# Audit publicitaire, lecture seule

Adapté de `AgriciDaniel/claude-ads` (skills `ads-audit`, `ads-meta`, `ads-google`, MIT). Principes gardés : lecture seule par défaut, constats séparés des diagnostics et des recommandations, aucune règle universelle (« coupe tout ce qui dépasse tel coût »), transparence sur les données manquantes. Les scripts de score du dépôt d'origine ne sont pas repris : on travaille sur exports, captures ou connecteur.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 0. Garde-fou

**Aucune modification de compte.** Toute action proposée (pause, budget, enchère, audience) est un brouillon que l'utilisateur applique lui-même. Même si un connecteur donne un accès en écriture, ne l'utilise pas.

## 1. Collecter

Demande ce qui manque, en une fois :

- Plateformes actives et période (30 ou 90 jours, plus la période précédente comparable).
- **Meta** : export au niveau annonce (dépense, impressions, clics, conversions, valeur, fréquence), capture du gestionnaire d'événements (pixel, API de conversions, qualité de correspondance, déduplication).
- **Google Ads** : rapport campagnes et groupes d'annonces, termes de recherche, liste des actions de conversion (principales, secondaires, source).
- **Site** : commandes ou demandes et chiffre d'affaires de la même période, part récurrente, panier moyen, part attribuée à la publicité.
- **Économie**, à fournir par l'utilisateur et jamais supposée : marge brute, coût de livraison ou de réalisation, durée moyenne d'un abonnement ou taux de retour des clients ; pour un site vitrine, taux de transformation d'une demande en vente et valeur moyenne d'une vente.

Chaque constat garde la trace de sa source (fichier, capture, date).

## 2. Contrôles

**Mesure — priorité 1**
- Pixel et API de conversions, événement d'achat ou de demande dédupliqué, qualité de correspondance.
- Google : une seule conversion principale par objectif, pas de double comptage avec un import d'analytique.
- **Revenus récurrents** : les renouvellements ne doivent pas remonter comme de nouvelles conversions publicitaires, sinon le retour sur dépense est gonflé. Vérifie ce que reçoivent les régies à chaque prélèvement.
- **Site vitrine** : la conversion suivie est-elle une vraie demande (formulaire envoyé, appel d'une durée minimale), et non une simple visite de la page contact ?
- Valeur de conversion : première commande seulement, ou valeur client ? Le dire explicitement.

**Rentabilité**
- Coût par acquisition sur la première commande, face à la marge de cette commande.
- Coût par acquisition d'un client récurrent, face à la marge cumulée sur la durée moyenne, si elle est fournie. Sinon, dire que la rentabilité réelle ne peut pas être jugée.
- Effet des seuils (livraison offerte, minimum de commande) sur le panier des visiteurs payants.

**Structure et créas**
- Consolidation suffisante pour sortir de la phase d'apprentissage au vu du volume de conversions, sans seuil universel.
- Fatigue : fréquence, évolution du taux de clic et du coût par acquisition par annonce.
- Diversité d'angles et de formats.
- Cohérence entre l'annonce et la page d'arrivée.
- Google Search : marque séparée du hors-marque, termes de recherche non pertinents, Shopping ou PMax alimentés par un flux propre.

**Conformité**
- Aucune allégation réglementée (contexte §3 et §12).
- Prix et conditions identiques à ceux du site.

Catalogues de contrôles détaillés : `references/meta-audit.md`, `references/google-audit.md`, `references/conversion-tracking.md`, `references/compliance.md`. Repères chiffrés : `references/benchmarks.md`, pour une comparaison directionnelle, jamais comme note de passage.

## 3. Lecture

Sépare toujours quatre couches :

1. **Constats** : ce que les données montrent.
2. **Diagnostics** : ce qu'on en déduit, avec un niveau de confiance (élevée, moyenne, faible).
3. **Recommandations** : action, priorité, effort, effet attendu, indicateur de réussite.
4. **Changements proposés** : brouillons, à appliquer par l'utilisateur.

Tiens compte du délai de conversion, de la taille de l'échantillon et de la saisonnalité avant toute conclusion. Si une plateforme manque de données, l'audit est « partiel » et le dit : pas de score inventé pour elle.

## 4. Livrable

- `AUDIT-ADS-<marque>-<date>.md` : synthèse, état de la mesure, rentabilité, constats par plateforme, contradictions et données manquantes, plan d'action priorisé, plan de mesure.
- Statut de complétude : complet, provisoire, partiel ou données insuffisantes.
- Sur demande : actions dans l'outil de tâches du contexte §8.
- Nouvelles créas à produire : skill `ad-creative`.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Régies (lecture) | données tirées directement | exports et captures fournis par l'utilisateur |
| Outil de tâches | actions créées | liste dans le livrable |
