---
name: cro
description: Analyse une page (accueil, fiche produit, page de service, offre, collection, panier, formulaire de contact) et propose des améliorations de conversion classées par impact, avec variantes de texte et idées de tests. À utiliser dès que l'utilisateur parle de conversion, de taux de conversion, de pages qui ne vendent pas, de formulaire que personne ne remplit, d'abandon de panier côté page, de « pourquoi ça ne convertit pas », de test A/B, ou demande un avis sur une page existante, même sans dire CRO.
---

# Optimisation de conversion

Adapté de `coreyhaines31/marketingskills/skills/cro` (MIT). Le cadre d'analyse en sept dimensions est conservé ; les points de contrôle s'appliquent à un e-commerce comme à un site vitrine.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 1. Récupérer la page réelle

Lis la page en ligne, ou une capture fournie. Note : type de page, conversion principale (achat, abonnement, demande de devis, prise de rendez-vous), source de trafic probable. Si l'utilisateur a des chiffres (sessions, taux d'ajout au panier, taux d'envoi du formulaire, panier moyen), demande-les une fois ; sinon analyse sans et dis-le.

## 2. Grille d'analyse, par ordre d'impact

**1. Proposition de valeur en cinq secondes.** Comprend-on sans défiler ce que c'est, pour qui, à partir de quel prix ou comment obtenir un prix, et la condition qui rassure ?

**2. Titre.** Spécifique, dans les mots du client, cohérent avec la source de trafic. Une publicité sur un angle qui arrive sur une page d'un autre angle perd du monde.

**3. Bloc d'action.**
- *E-commerce* : les options sont-elles compréhensibles ? Sait-on ce qu'on reçoit pour chaque variante ? Prix visible, condition de livraison près du bouton, délai. Achat unique et achat récurrent : l'écart est-il expliqué ? Bouton unique, visible sans défiler sur mobile.
- *Vitrine* : le formulaire demande-t-il seulement ce qui sert à répondre ? Sait-on ce qui se passe après l'envoi et sous quel délai ? Téléphone cliquable sur mobile. Un seul appel à l'action par écran.

**4. Hiérarchie visuelle.** Un balayage rapide suffit-il ? Les éléments décoratifs servent-ils le message ou le couvrent-ils ?

**5. Réassurance.** Avis réels près de l'action, preuves autorisées au contexte §3, paiement sécurisé ou garanties. Aucune réassurance non vérifiée.

**6. Objections du secteur.** Liste celles des profils du contexte §4 et vérifie que la page répond à chacune : « et si ça ne me convient pas », « c'est cher », « je ne sais pas choisir », « je vais être engagé », « est-ce fiable ». Une comparaison de prix ne s'écrit que si l'utilisateur valide le calcul.

**7. Frictions.** Fenêtres empilées, chargement lent, zones cliquables trop petites sur mobile, liens morts, panier sans seuil de livraison, formulaire qui efface la saisie en cas d'erreur.

## 3. Points propres à chaque page

- **Accueil** : chemin court vers l'offre principale **et** vers une aide au choix pour les indécis.
- **Offre récurrente** : ce qui arrive à chaque période, quand on est prélevé, comment on suspend.
- **Liste d'offres** : filtrer par besoin, pas seulement par nom.
- **Page de service** : preuve, déroulé, prix ou fourchette, puis formulaire. Pas l'inverse.
- **Événement, atelier** : date, lieu, places restantes, niveau, ce qui est inclus, réservation sans rupture de parcours.
- **Panier** : progression vers le seuil de livraison, suggestion cohérente, rappel de la condition qui rassure.
- **Confirmation** : dire la suite, proposer une seule action.

## 4. Livrable

```
### Gains rapides (à faire maintenant)
### Chantiers à fort impact (à prioriser)
### Idées de tests A/B (hypothèse → changement → métrique → durée minimale)
### Variantes de texte (H1, sous-titre, appel à l'action : 2 ou 3 chacune, avec l'angle)
```

Chaque point : constat observé sur la page → recommandation précise → effort (S/M/L) → impact attendu, **qualitatif**. Aucun pourcentage de gain inventé.

Un test A/B ne se propose que si le trafic permet de conclure : sinon, recommande le changement direct et la mesure avant-après, en disant sa limite.

Sur demande, pousse les recommandations retenues dans l'outil de tâches du contexte §8. Pour réécrire une page entière, passe la main au skill `copywriting`.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Statistiques du site | priorités fondées sur les chiffres | analyse qualitative, annoncée comme telle |
| Outil de tâches | actions créées | liste dans le livrable |
