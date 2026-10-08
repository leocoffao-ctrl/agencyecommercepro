---
name: ad-creative
description: Crée et itère des publicités — textes et concepts pour Meta (Instagram, Facebook), Google (Search, Performance Max, Shopping), TikTok et Pinterest — à partir d'angles, avec les limites de caractères de chaque plateforme et les règles de conformité. À utiliser dès que l'utilisateur parle de pub, d'ads, de créa, d'accroche publicitaire, de campagne Meta ou Google, de brief créatif, de variations d'annonces, ou veut relancer des pubs qui s'essoufflent, même sans dire « ad creative ». Pour auditer un compte publicitaire, voir ads-audit.
---

# Créas publicitaires

Adapté de `coreyhaines31/marketingskills/skills/ad-creative` (MIT). Méthode gardée : angles d'abord, variations par angle, validation stricte des limites de caractères, itération à partir des données.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 1. Cadrer

- Plateforme et format (Meta statique, carrousel ou vidéo verticale ; Google RSA, PMax ou Shopping ; TikTok ; Pinterest).
- Offre poussée (contexte §2).
- Audience et température (froid, visiteurs du site, clients).
- En itération : export des performances par annonce (dépense, taux de clic, coût par acquisition, retour sur dépense) sur une période comparable.

## 2. Angles

Établis trois à cinq angles avant d'écrire la moindre ligne, à partir du contexte §3 et §4. Familles utiles :

| Famille | Ce qu'elle dit |
|---|---|
| Découverte | Ce que le client ne connaît pas encore |
| Preuve concrète | Un détail vérifiable qui distingue l'offre |
| Aide au choix | « Trouve ce qui te convient » |
| Origine, fabrication | Qui fait, où, comment |
| Liberté | Sans engagement, sans risque, si c'est autorisé |
| Cadeau | Pour quelqu'un d'autre |
| Usage | Le moment où le produit sert |
| Expérience | Ce qu'on vit, pour une prestation |

Comparaison : rester sur des faits vérifiables, ne jamais dénigrer une marque nommée. La publicité comparative est encadrée (contexte §12).

## 3. Limites par plateforme — vérifier chaque ligne

**Google Ads, RSA** : titres 30 caractères (jusqu'à 15), descriptions 90 caractères (jusqu'à 4), chemins d'URL 15 caractères × 2. Chaque titre a du sens seul et combiné ; au moins un titre mot-clé, un titre bénéfice, un titre d'appel à l'action. Épingler le moins possible.

**Meta** : texte principal dont les 125 premiers caractères portent l'accroche, titre d'environ 40 caractères, description d'environ 30.

**TikTok** : 80 caractères recommandés, 100 au plus. **Pinterest** : titre 100 caractères, description 500, les 50 premiers comptent.

Compte les caractères pour de vrai, espaces et accents compris, et signale toute ligne trop longue avec une version raccourcie. Ces limites évoluent : en cas de doute, la documentation de la plateforme fait foi.

## 4. Conformité

- Aucune allégation réglementée dans le secteur (contexte §3 et §12).
- Pas de ciblage ni de formulation qui présume un attribut personnel de la personne (« Tu es épuisé ? »). Les plateformes interdisent les annonces qui sous-entendent un état de santé, une situation financière ou une caractéristique sensible.
- Prix et conditions exacts, lus sur le site, avec leur seuil.
- Aucun avis inventé ; un avis cité est réel et non modifié.
- Pas de visuel, de personnage ou de musique protégés ; seulement l'univers de la marque.
- Un slogan toléré en organique peut être exclu du payant : le contexte le précise.

## 5. Visuels

Brief par concept : format (1:1, 4:5, 9:16), message principal en six mots au plus, éléments de marque (contexte §6), produit ou prestation visible, accroche incrustée. S'appuyer sur les fichiers de marque.

## 6. Itérer à partir des données

1. Gagnantes : quels angles, formats et accroches reviennent chez les meilleures, au coût par acquisition ou au retour sur dépense, pas au taux de clic seul.
2. Perdantes : même analyse, sans conclure sur un échantillon trop petit. Dis-le quand c'est le cas.
3. Nouvelles variations : doubler ce qui gagne, tester un seul changement à la fois.
4. Journal d'itération : date, ce qui a été testé, résultat, décision.

## 7. Livrable

```
## Angle : [nom]
### Titres (limite)        → texte (nb de caractères)
### Descriptions (limite)  → texte (nb de caractères)
### Texte principal Meta   → texte (125 premiers caractères repérés)
### Brief visuel
```
Option : fichier prêt à importer dans l'éditeur de la régie.

## Dépendances

Aucun connecteur requis. Avec un outil de design connecté, les déclinaisons de formats peuvent être produites à partir du brief.
