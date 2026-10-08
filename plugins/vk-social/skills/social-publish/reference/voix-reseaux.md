# Voix sur les réseaux — ton, piliers, cadence, liens

Ce fichier donne la méthode. Les valeurs propres à la marque (registre, mots bannis, slogans, piliers, hashtags, UTM, plateformes) sont au contexte de marque, sections 3, 5, 11 et 12, qui font foi. Ce qui manque au contexte se propose à l'utilisateur, marqué « à valider », et ne devient pas une décision tant qu'il ne l'a pas confirmé.

## 1. Voix commune

- **Registre et ton** : ceux du contexte §5, sans mélange dans un même texte.
- **Précision plutôt que superlatif** : un détail concret vaut mieux qu'un adjectif. Les détails viennent d'une source (fiche produit, étiquette, guide, utilisateur), jamais de l'imagination.
- **Mots bannis** : ceux du contexte, plus les superlatifs creux (incroyable, révolutionnaire).
- **Écrire comme une personne, pas comme une IA** : chaque texte passe par `anti-ia.md`.
- **Emojis** : le plafond du contexte, en ponctuation, jamais en liste à puces décorative.
- **Slogans de la marque** : utilisables en accroche ou en fin de légende, à doser. Certains sont réservés à l'organique et exclus du payant : le contexte le précise.

## 2. Ce qu'on peut affirmer

Seulement les affirmations autorisées du contexte §3. Interdit partout : chiffres inventés, faux témoignages, promesse que la marque ne peut pas tenir, allégation réglementée. Un prix se revérifie sur la source de vérité avant d'être écrit.

## 3. Ton par plateforme

| Plateforme | Longueur | Structure | Hashtags | Premier commentaire |
|---|---|---|---|---|
| Instagram | 80 à 200 mots | Accroche en ligne 1 · deux à quatre lignes de fond · un appel à l'action · lien en bio ou mot-clé | 3 à 5, sur la dernière ligne | Question d'engagement ou détail technique |
| TikTok | 1 à 3 phrases | Accroche qui reprend le texte à l'écran · appel court | 3 à 5 | Non pris en charge par l'API |
| Facebook | Reprise d'Instagram, un peu plus explicative | Lien cliquable direct avec UTM | 0 à 3 | Lien ou question |
| Pinterest | Titre de 100 caractères au plus, description d'une à trois phrases | Le titre est la recherche que ferait quelqu'un | 0 à 2 | — |
| YouTube Shorts | Titre de 60 caractères utiles, description de deux ou trois lignes et lien | Le titre est une promesse concrète | 3 au plus | Question épinglée |
| LinkedIn | 100 à 220 mots | Variante professionnelle du sujet du jour : ce que ça change pour une équipe, un acheteur, ou les coulisses d'une décision | 0 à 3 | Lien |

Accroche : une situation, un détail concret ou une question. Jamais « Nouveau post ! », jamais deux fragments en miroir. Formules et contrôle chiffré : `accroches.md`.

LinkedIn n'est jamais le copier-coller d'Instagram.

## 4. Piliers et cadence

Les piliers et leur rotation sont au contexte §11. À défaut, propose quatre à six piliers à partir de l'offre et des contenus existants, par exemple : pédagogie · produit ou prestation · coulisses · communauté · actualité du secteur · offre professionnelle.

Règles de rotation qui tiennent dans tous les cas :
- les piliers s'enchaînent dans l'ordre, puis on recommence ;
- jamais deux posts de conversion d'affilée ; deux sur sept au plus ;
- si un asset ne rentre dans aucun pilier prévu, on intervertit l'ordre plutôt que de forcer.

Les créneaux horaires par défaut sont des hypothèses tant que les statistiques du compte ne les confirment pas : dis-le.

## 5. Hashtags

Pioche dans la banque du contexte, sans jamais tout coller : un de marque, un de catégorie, un à trois de niche. Les plafonds par plateforme sont dans `social.hashtags_max`.

## 6. Liens et UTM

Toujours le domaine canonique du contexte §1. Paramètres : `utm_source={plateforme}` · `utm_medium={social|dm|bio}` · `utm_campaign={AAAA-MM-sujet}`, ou la convention du contexte §11 si elle diffère.

## 7. Visuels

- Respecter la direction artistique du contexte §6 et ses interdits.
- Un produit ou une étiquette montrés restent lisibles après recadrage.
- Texte incrusté sur une vidéo : court, dans la zone sûre (éviter le tiers bas et la marge droite où l'interface se superpose).

## 8. Règles légales

Elles dépendent du pays (contexte §12). Points à vérifier partout :

- **Partenariat ou affiliation** : toute contrepartie (produit offert, commission) s'affiche clairement, avec l'étiquette de partenariat de la plateforme. Dans le doute, demander.
- **Jeu-concours** : règlement accessible, conditions claires, pas d'obligation d'achat, mention que la plateforme n'est pas associée. Proposer le texte, ne jamais le lancer seul.
- **Republication d'un contenu de client** : seulement avec l'accord de l'auteur, crédit dans la légende.
- **Musique** : sons libres de droits ou bibliothèque de la plateforme au moment de la publication native ; pas de morceau commercial incrusté dans un fichier envoyé par l'API.
