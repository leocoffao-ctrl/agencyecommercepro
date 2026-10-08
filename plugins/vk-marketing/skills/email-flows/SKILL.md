---
name: email-flows
description: Conçoit et rédige les emails et séquences automatisées d'une marque — bienvenue, panier ou formulaire abandonné, post-achat, demande d'avis, vie d'un abonnement, relance de devis, réactivation, campagnes saisonnières — pour l'outil d'emailing en place. À utiliser dès que l'utilisateur parle d'email, de newsletter, de flow, de séquence, de relance, de panier abandonné, de fidélisation, de churn, de win-back ou d'une campagne saisonnière, même sans dire « séquence ».
---

# Emails et séquences

Adapté de `coreyhaines31/marketingskills/skills/emails` (MIT). Principes gardés : un email = un objectif, de la valeur avant la demande, la pertinence plutôt que le volume, une prochaine étape évidente.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 1. Avant d'écrire

- Quelle séquence ou campagne, quel déclencheur, quel segment ?
- Qu'est-ce qui tourne déjà dans l'outil d'emailing (contexte §7) ? **Ne crée pas un doublon d'un envoi automatique existant : complète-le.**
- Consentement : les envois marketing ne partent qu'aux contacts qui y ont consenti, selon le droit du pays (contexte §12). Les emails de service restent informatifs.

## 2. Carte des séquences

**E-commerce**

| Séquence | Déclencheur | Nb | Objectif |
|---|---|---|---|
| Bienvenue | Inscription | 3-4 | Expliquer la catégorie, orienter vers la bonne offre |
| Navigation abandonnée | Vue d'un produit sans ajout | 1-2 | Aider à choisir |
| Panier abandonné | Paiement commencé | 2-3 | Lever l'objection, sans remise par défaut |
| Post-achat | Première commande | 3 | Réussir la première utilisation, proposer la suite |
| Demande d'avis | Quelques jours après la livraison | 1-2 | Avis réel |
| Bienvenue abonné | Premier abonnement | 2-3 | Rassurer (suspension, calendrier) |
| Avant renouvellement | Quelques jours avant le prélèvement | 1 | Annoncer, rappeler la date |
| Sauvetage | Clic sur résilier ou suspendre | 1-2 | Proposer une pause ou un ajustement |
| Réactivation | Inactif ou résilié depuis N semaines | 2-3 | Nouveauté, retour sans friction |

**Site vitrine**

| Séquence | Déclencheur | Nb | Objectif |
|---|---|---|---|
| Réponse à une demande | Formulaire envoyé | 1 | Confirmer, dire le délai et la suite |
| Préparation du rendez-vous | Rendez-vous pris | 1-2 | Ce qu'il faut préparer, rappel |
| Relance de devis | Devis envoyé sans réponse | 2 | Répondre à l'objection probable, proposer un échange |
| Après prestation | Prestation terminée | 2 | Entretien ou usage, demande d'avis |
| Réactivation | Ancien client | 1-2 | Nouveauté, saison |
| Recommandation | Client satisfait | 1 | Demander une recommandation, simplement |

Délais : bienvenue immédiat, un à deux jours d'écart en début de séquence, puis hebdomadaire ou bimensuel. Le jour et l'heure se testent sur la liste, ils ne se décrètent pas.

## 3. Règles de rédaction

- **Objet** : 30 à 50 caractères, clair avant malin, un emoji au plus et pas systématique.
- **Préheader** : 60 à 110 caractères, complète l'objet sans le répéter.
- **Corps** : court, une idée, un appel à l'action principal. Contenu utile d'abord.
- **Ton et registre** : contexte §5.
- **Remises** : aucun code inventé. Si une incitation semble utile, propose-la en option à valider, avec son coût.
- **Données dynamiques** : les balises de l'outil d'emailing seulement si l'utilisateur confirme qu'elles existent ; sinon texte générique.
- **Rendu** : pour du HTML à coller, une seule colonne en tableau, couleurs de fond doublées en attribut et en style, pas de tableaux imbriqués ni de positionnement absolu, polices de repli du contexte §6.
- **Désinscription** : présente et fonctionnelle dans tout envoi marketing.

## 4. Livrable

**Vue d'ensemble** : nom de la séquence, déclencheur, conditions de sortie (a acheté, a répondu), nombre d'emails, calendrier, métrique principale.

**Pour chaque email** :
```
N° / délai / déclencheur
Objectif (une phrase)
Objet (+ 2 variantes à tester)
Préheader
Corps (texte final)
Appel à l'action → URL de destination
Segment / condition
Métrique de succès
```

**Plan de mesure** : ouverture et clic à titre indicatif ; surtout la conversion attribuée à la séquence, et la métrique propre à chaque flux (taux de sauvetage, taux de réponse au devis).

Livraison en Markdown et, sur demande, en HTML prêt à coller dans l'outil d'emailing.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Outil d'emailing | lecture de l'existant, balises réelles | l'utilisateur décrit l'existant ; balises laissées génériques |
