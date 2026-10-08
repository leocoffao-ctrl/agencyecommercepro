# Passe anti-IA des textes courts

Adaptation française du skill **humanizer** de Siqi Chen (https://github.com/blader/humanizer, MIT, v3.0.0, tiré de la page Wikipédia « Signs of AI writing »). Original complet : `reference/humanizer/humanizer-original.md`. Licence : `reference/humanizer/LICENSE`.

Pourquoi ce fichier existe : des légendes peuvent respecter tous les mots bannis d'une charte et « faire IA » quand même. Le problème vient presque toujours de la structure : même squelette d'un post à l'autre, même mise en scène, mêmes tournures de chute. Le vocabulaire compte peu, la structure beaucoup.

Les motifs listés ici sont ceux du français. Pour une autre langue, repars de l'original anglais et adapte la liste.

## Le principe

Un modèle écrit la suite la plus probable, donc la tournure qui passe partout. Une personne écrit pour quelqu'un et sur un sujet précis : ses choix sont inégaux, concrets, parfois un peu de travers. Chaque phrase gardée apporte quelque chose que le lecteur n'avait pas. Une phrase qui ne fait que souligner l'importance de la précédente saute.

## Ce que la passe couvre

Tout le texte que le public lit : légende, premier commentaire, **texte des slides d'un carrousel et du PDF qui en est tiré**, **titres et bulles d'une vidéo**, texte incrusté. Sur un visuel, les titres courts et les étiquettes sont normaux ; les tics à chasser restent les mêmes.

## Comment faire la passe — obligatoire avant de montrer un texte ou de rendre un visuel

1. **Écris le premier jet** en suivant `voix-reseaux.md` et le contexte de marque.
2. **Repère les tics**, du plus fort au plus faible (liste ci-dessous). Regarde aussi la forme d'ensemble : même squelette que le texte d'avant ? même chute ?
3. **Réécris le paragraphe entier** autour de son idée, au lieu de rapiécer mot par mot. Garde tous les faits sourcés. N'ajoute **aucun** fait, chiffre, date, nom ou citation qui ne vient pas de la source du jour ou de l'utilisateur. Une réaction (« ça nous a surpris ») est permise, un fait nouveau non.
4. **Relis à voix haute.** Puis cherche les cinq tics qui survivent le plus souvent : le « pas X, c'est Y », la chute d'une ligne, le tiret, le triplet, le gras ou l'emoji décoratif.
5. **Lance le contrôle automatique** : `python3 scripts/check_anti_ia.py legende.txt --config brand/kit.config.json` (ou `--json posts.json`). Il attrape les motifs mécaniques, pas le reste : la relecture reste obligatoire.
6. **Test final** : la personne qui tient le compte aurait-elle pu écrire ça sur son téléphone, entre deux tâches ? Si non, réécris.

## A. La mise en scène au lieu du fait — un seul cas suffit pour corriger

### 1. « Ce n'est pas X, c'est Y » et ses cousins
Formes : *ce n'est pas X, c'est Y* · *pas seulement X, mais Y* · *X plutôt que Y* · *bien plus que* · la version en deux phrases (« Même couleur. Pas le même produit. »).
Pourquoi c'est un tic : la moitié négative répond à quelqu'un qui n'a rien dit, pour faire paraître l'autre moitié plus grande.
Garde le contraste seulement s'il corrige une idée que le lecteur a vraiment.
> Avant : « Au fond, c'est la méthode qui fait le résultat, bien plus que l'outil. »
> Après : « Le résultat dépend surtout de la façon de s'en servir. L'outil joue peu. »

### 2. Chutes d'une ligne et fragments dramatiques
Formes : une phrase seule en fin de paragraphe qui redit ce qui précède (« Il y a de la marge. ») · rangée de fragments (« Trois gestes. Dix minutes. Zéro outil. ») · même chute à chaque post.
Une phrase courte a le droit d'exister si elle apporte un fait. Sinon on coupe, ou on la fusionne.

### 3. Formules qui font profond
Formes : *au fond*, *en réalité*, *ce qui compte vraiment*, *le vrai sujet*, *le chiffre qui compte*, *c'est peut-être le chiffre le plus parlant*, *X est le langage de Y*.
Remplace par l'affirmation concrète.

### 4. Élan avant le point
Formes : *Le détail qui surprend :* · *Petit bonus :* · *Ce qui aide vraiment :* · *Autre point rarement dit :* · *Ça vaut le coup de savoir…* · *Spoiler :* · *Voilà le truc :* · *On t'explique.* · « Honnêtement ? » seul en début de phrase.
Supprime l'annonce, donne l'information.
> Avant : « Le détail qui surprend : la garantie ne s'applique que si… »
> Après : « La garantie ne s'applique que si… » (si c'est surprenant, le lecteur le verra)

### 5. Répondre à personne
Formes : *pas de panique* · *on ne va pas se mentir* · *non, ce n'est pas réservé aux experts* · *attention, on ne dit pas que…*
Coupe, sauf si l'objection est réelle et vient des commentaires ou de l'utilisateur.

## B. Le rythme mécanique

### 6. Triplets forcés
Trois adjectifs, trois exemples, trois phrases parallèles puis une morale. Vérifie que chaque élément apporte une idée différente. Deux suffisent souvent ; quatre, c'est parfois plus vrai. Garde trois quand la source donne vraiment trois choses.

### 7. Débuts de phrase répétés
Trois phrases de suite qui commencent par « Le… », « Ce… », « Tu… ». Fusionne ou commence par l'action.

### 8. Tirets
Aucun tiret cadratin (—) ni demi-cadratin (–) dans un texte court, ni « -- ». Virgule, point, deux-points, parenthèses. Les tirets dans les URL restent. (Règle levée si le contexte de marque autorise le tiret.)

### 9. Précautions empilées (faible seul)
*pourrait potentiellement*, *dans certains cas il se peut que*. Une seule précaution si la source la justifie.

### 10. Squelette identique d'un post à l'autre
Le squelette « accroche choc / explication / « Glisse pour… » / « Le lien est en bio » / hashtags » répété sur tous les posts est le tic le plus visible sur un fil. Varie :
- l'ordre (parfois l'histoire d'abord, parfois la question, parfois le chiffre) ;
- la longueur (un texte de 60 mots de temps en temps, c'est très bien) ;
- la formule vers le carrousel ou la vidéo ;
- l'appel à l'action ;
- sur LinkedIn, la phrase d'annonce du document joint.

Avant d'écrire, relis les trois derniers textes publiés sur la même plateforme et évite leur première phrase type et leur chute.

## C. L'enflure

### 11. Vocabulaire d'IA en français
À surveiller surtout quand il y en a plusieurs : *crucial*, *essentiel*, *incontournable*, *véritable*, *au cœur de*, *riche* (au figuré), *subtil*, *sublimer*, *révéler* (« révéler le potentiel »), *plonger*, *découvre*, *explorer*, *mettre en lumière*, *souligner*, *témoigner de*, *s'inscrire dans*, *dans un monde où*, *de plus en plus*, *que tu sois… ou…*, *pépite*, *expérience* (« une expérience X »), *univers* (« l'univers de X »), *voyage sensoriel*, *parfait équilibre*, *à la fois X et Y*, *typiquement*.
Plus les mots bannis du contexte de marque (§5).

### 12. Importance gonflée
*marque un tournant*, *joue un rôle clé*, *change la donne*, *l'avenir s'annonce*. Garde le fait, jette l'emballage. Finis sur le dernier fait concret.

### 13. Participes qui décorent
« …, ce qui permet de… », « …, garantissant… », « …, offrant… » accrochés à un fait simple. Coupe ou fais une vraie phrase.

### 14. Langage de brochure
*niché*, *au cœur de*, *à couper le souffle*, *un cadre idyllique*, *d'exception*. Dis ce que c'est : un lieu, une mesure, une méthode.

### 15. Autorité empruntée
« Les experts disent », « selon les spécialistes ». Nomme la source ou coupe.

### 16. Verbes détournés
*se positionne comme*, *représente*, *constitue*, *s'impose comme*, *propose* à la place de *est*, *a*. Utilise *est*, *a*, *fait*.

## D. La mise en forme

### 17. Emojis et gras décoratifs
Le plafond d'emojis vient du contexte (un au plus par défaut), jamais en début de ligne comme puce. Pas de listes à puces décoratives dans une légende.

### 18. Guillemets
Guillemets de la langue du projet, cohérents d'un bout à l'autre.

## E. Les restes de conversation

### 19. Résidus de chatbot
*N'hésite pas à…*, *Dis-nous tout en commentaire !*, *Et toi, tu en penses quoi ?* collé en fin de légende sans rapport. Le premier commentaire porte la question ; la légende n'a pas à la répéter.

### 20. Questions d'engagement génériques
Premier commentaire : une question à laquelle on répond en trois mots et qui dépend du sujet du jour. Pas « Et toi, qu'en penses-tu ? ».

## Ce qu'il faut garder : une voix de personne

- Le registre du contexte, des phrases courtes mêlées à des plus longues.
- Les détails précis et un peu inattendus : un chiffre de la source, un nom propre, une date.
- Un avis ou une réaction à la première personne quand c'est vrai, y compris l'aveu d'un intérêt (« on en vend, donc on est juges et parties »).
- Une parenthèse, une autocorrection, une pointe d'humour.
- Un peu d'irrégularité : un texte n'a pas besoin d'être parfaitement construit.

## Quand ne pas corriger

Une citation exacte, un nom propre, un slogan de la marque, une mention recopiée d'une étiquette ou d'une fiche technique : on n'y touche pas. Un tic isolé marqué « faible seul » ne justifie pas une réécriture ; plusieurs tics ensemble, si.

## Exemple complet (marque fictive, carrousel sur l'entretien d'un plan de travail en bois)

Avant :
> Même essence. Pas le même plan de travail.
>
> Deux plans de travail en chêne peuvent vieillir de façon bien différente. […] Au fond, c'est la finition qui fait la durée, bien plus que le bois.
>
> Petit bonus : « huile naturelle » sur un bidon, ça ne dit rien de sa composition. […]
>
> Glisse pour la suite : les erreurs de la première semaine, l'entretien annuel et quoi regarder sur l'étiquette. Le guide complet est en bio 🔥

Tics : fragments en contraste (§1, §2), « au fond… bien plus que » (§1, §3), « Petit bonus : » (§4), triplet final (§6), squelette « Glisse / guide en bio » identique aux autres posts (§10).

Après :
> Deux plans de travail taillés dans le même chêne peuvent ne pas vieillir pareil.
>
> La différence se joue la première semaine : une huile qui n'a pas eu ses 72 heures de séchage marque à la première casserole. Le bois compte moins que la patience.
>
> Sur le bidon, « huile naturelle » ne renseigne pas sur la composition. Cherche plutôt la liste des composants et le temps de séchage.
>
> Le carrousel reprend l'entretien année par année. Les sources sont dans le guide (lien en bio).

(Les chiffres de cet exemple sont inventés pour la démonstration : dans un vrai post, chacun vient de la source du jour.)
