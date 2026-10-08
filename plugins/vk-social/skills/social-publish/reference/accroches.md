# Accroches : formules, contrôle, pièges

Adapté de `ig-reel/hooks.json`, `ig-caption` et `ig-carousel` du dépôt instagram-agent-skill (https://github.com/Jakeschincariol/instagram-agent-skill, MIT, (c) 2026 Jake Schincariol). Sur 26 formules d'origine, 14 sont gardées. Les autres sont écartées parce qu'elles supposent une vidéo face caméra, un chiffre personnel qu'une marque n'a pas le droit d'inventer (« ça m'a coûté tant »), ou parce qu'elles recoupent un tic de `anti-ia.md`.

**L'accroche** est ce que le lecteur voit en premier : la première ligne de la légende, le titre de la couverture d'un carrousel, le titre de la première scène d'une vidéo.

## 1. Ce qui se voit avant « ... plus »

Instagram affiche environ **125 caractères** d'une légende dans le fil, puis coupe. LinkedIn en montre un peu plus (autour de 210 sur ordinateur, moins sur mobile). Presque tout se joue dans cette fenêtre :

- la première ligne tient dans la fenêtre, ou bien la coupe tombe sur une question ouverte (jamais au milieu d'une subordonnée) ;
- il y a au moins une chose vérifiable avant la coupe : un chiffre, un nom, un lieu ;
- jamais de salutation, de hashtag ou d'emoji en premier caractère.

`python3 scripts/check_legende.py legende.txt` imprime cette fenêtre telle que le fil la montre. Lis la boîte avant le reste.

**Deux cas de figure** :
- **Vidéo** : elle porte déjà l'accroche (titre à l'écran, première réplique). La légende ne refait pas une deuxième accroche concurrente : elle donne le contexte, l'appel à l'action et les mots que les gens cherchent.
- **Carrousel** : la couverture accroche, mais la légende est lue par ceux qui ne font pas encore défiler. Sa première ligne fonctionne comme une accroche à part entière, et elle ne recopie pas le titre de la couverture.

## 2. Contrôle chiffré des accroches

Écris **trois versions**, une par ligne, dans `accroches.txt`, puis :

```bash
python3 scripts/score_accroche.py accroches.txt --config brand/kit.config.json
```

Cinq critères notés de 0 à 100 : LONGUEUR (5 à 12 mots, 60 caractères au plus), CONCRET (chiffre, nom, lieu), ENJEU (quelque chose que le lecteur peut rater ou corriger), DEVANT (le mot fort dans les quatre premiers mots), ADRESSE (le lecteur est dans la phrase, au registre du contexte). Rédhibitoires : salutation, préambule (« dans cette vidéo »), « nouveau post », question creuse, hashtag ou emoji dans l'accroche.

Garde la mieux notée **si elle passe aussi `check_anti_ia.py` sans FORT**. Le script récompense la concision et le contraste, donc deux fragments en miroir peuvent bien noter ici alors que `anti-ia.md` les bannit. En cas de conflit, anti-ia gagne. Entre deux accroches au-dessus de 70, choisis à la relecture : l'outil sépare bien le creux du concret, pas le bon du très bon.

## 3. Les 14 formules gardées

Les gabarits se remplissent avec des faits. Chaque chiffre, lieu ou nom vient de la source du jour ou de l'utilisateur, jamais de toi.

| # | Formule | Gabarit | Ce qui la gâche |
|---|---|---|---|
| 1 | Ordre à contre-pied | « Arrête de {geste courant}. {Alternative}. » | Un geste que personne ne fait vraiment |
| 2 | Tu le fais de travers | « Ton {objet} est {défaut} ? {Le réglage}. » | Culpabiliser (« tu fais tout faux ») |
| 3 | La question telle qu'on la pose | « “{Question entendue}” » | Une question inventée qui sonne marketing |
| 4 | Face à face | « {A} ou {B} : {ce qu'on a comparé}. » | Annoncer un vainqueur que la source ne donne pas |
| 5 | La liste avec une préférée | « {N} {choses} pour {résultat}. La {k}e est celle qu'on oublie. » | N gonflé pour faire rond |
| 6 | Le chiffre | « {N} {unité} : {ce que ça change}. » | Un chiffre sans source |
| 7 | La permission | « Pas besoin de {équipement cher} pour {résultat}. » | Promettre plus que la source |
| 8 | La date | « {Chose} change le {date}. » | Une date approximative |
| 9 | L'appel à un groupe | « Si tu {situation précise}, garde ce post. » | Un groupe trop large |
| 10 | Si ceci, alors cela | « Si ton {objet} {symptôme}, {cause probable}. » | Deux causes possibles présentées comme une seule |
| 11 | Le démarrage en plein geste | Première scène déjà en action | Une scène d'introduction avant l'action |
| 12 | Avant / après | Deux états montrés, une phrase sur le levier | Un « après » qui n'est pas dans la source |
| 13 | L'objection | « “{Objection réelle}.” D'accord, voilà ce qui marche quand même. » | Une objection que personne ne fait |
| 14 | L'origine concrète | « {Lieu}, {détail} : {ce que ça donne}. » | Accumuler trois fragments en rangée |

**Écartées** : « Personne ne te dit que… » et « La révélation » (mise en scène, §4 d'anti-ia), « Le contre-pied d'un proverbe » (miroir, §1), « Ça m'a coûté X », « Mes 10 premiers essais », « J'ai testé pendant 30 jours », « Le témoignage d'un autre » (chiffres personnels ou témoignages qu'une marque n'a pas le droit d'inventer), « Le superlatif ».

**Varier** : ne pas reprendre la formule des trois derniers posts de la même plateforme.

## 4. Carrousels

- La couverture fait l'essentiel du résultat : titre court, lisible en vignette, loin des bords.
- La deuxième slide tient seule : un carrousel peut être remontré en commençant plus loin.
- Une idée par slide, 25 mots au plus sous le titre. Si une slide demande un paragraphe, ce sont deux slides.
- La slide « checklist » est celle qu'on capture et qu'on envoie : lisible sans contexte.
- Numérotation visible (« 3/8 »).

## 5. Hashtags

Instagram ne compte plus les hashtags au-delà de cinq par post. Le plafond par plateforme se règle dans `social.hashtags_max` ; trois à cinq en pratique, sur la dernière ligne : un de marque, un de catégorie, un à trois de niche liés au sujet du jour. LinkedIn : zéro à deux.

Les plafonds et les fenêtres d'affichage changent : en cas de doute, vérifie dans la documentation de la plateforme.
