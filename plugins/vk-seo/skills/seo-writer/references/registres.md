# Registres éditoriaux et gabarit de brief

Un même blog peut publier dans deux registres. On choisit le registre selon l'intention et la page de référence qui ressort en tête des résultats, pas selon l'humeur. Le registre change la structure, la longueur et le ton ; il ne change jamais les règles de preuve de `seo-writer` (Phase 0.4 et suivantes).

## 1. Choisir le registre

| | Documentaire | Pratique (recette, mode d'emploi) |
|---|---|---|
| Intention | informationnelle, corriger une idée reçue, trancher | informationnelle à forte composante « faire chez soi » |
| Ce que veut le lecteur | comprendre, comparer, décider | réussir du premier coup |
| Longueur | 1 600 à 2 200 mots | 1 100 à 1 400 mots |
| Ouverture | chapeau de 150 à 200 mots qui pose la question réelle et dit ce que l'article tranche | chapeau de 200 à 250 mots qui plante le contexte et le matériel |
| Corps | H2 thématiques, H3 au même gabarit pour une série d'objets comparables | un bloc par objet (boisson, recette, geste), instructions en prose, quantités dans la phrase |
| Tableau | tableau comparatif | rarement |
| FAQ | 5 à 7 questions | 4 à 6 questions |
| Première personne | seulement sur une expérience réelle | souhaitée, seulement sur une expérience réelle |
| Schema | `Article` + `FAQPage` | `Article` + `FAQPage` ; `Recipe` seulement si la page porte une recette unique |

Les deux registres gardent la réponse rapide (`id="reponse-rapide"`) : en registre pratique, trois à cinq puces juste après le chapeau, une par objet ou par règle clé.

**Hiérarchie des titres.** Le gabarit affiche le titre en H1 : le corps commence au H2. Une série d'objets (sept boissons, cinq plantes) se range sous un H2 qui les annonce, puis un H3 par objet. Ne jamais passer du H1 aux H3 : `scripts/article_checks.py` le bloque.

**Page de référence.** On peut caler la forme sur un article qui se classe bien (longueur, structure, ton). On ne reprend ni son texte ni ses tournures. Si son `robots.txt` interdit la lecture, on ne la contourne pas : on le dit, on travaille sur le registre typique du genre, et on demande le texte à l'utilisateur pour un calage précis.

## 2. Terme pivot et cible atteignable

Un mot générique à très fort volume (le nom de la catégorie, seul) se gagne rarement : résultats locaux, encyclopédies, acteurs historiques. Si la Search Console ne montre aucune impression sur la requête nue, l'article ne la vise pas.

- **Cible réelle** : une requête de longue traîne que l'autorité actuelle du site peut atteindre (`remplacer X`, `X sans Y`, `X froid italien`).
- **Terme pivot** : le mot générique, placé dans le H1, le title, le slug et le champ sémantique, sans en faire la cible.

Inscris les deux dans les variables (`MOT_CLE_PRINCIPAL` = la cible réelle, `TERME_PIVOT` = le générique) et justifie le choix par les données dans le brief.

## 3. Faits fournis, incertitudes, interdictions

Quand l'utilisateur fournit une liste de faits vérifiés, elle est **fermée** : rien n'entre dans l'article qui n'y figure pas ou qui n'a pas sa propre source vérifiée le jour même.

- **Incertitudes assumées.** Une origine discutée, une date que personne ne prouve, une appellation contestée s'écrivent comme telles (« les sources la situent vaguement… », « le nom est contesté par… »). On ne tranche pas à la place des historiens.
- **Récit contredit.** Une légende reprise partout mais contredite par les dates se présente comme une légende, avec ce qui la contredit.
- **Quantités manquantes.** Pas de gramme, de température, de ratio ou de durée inventés : la consigne reste qualitative (« un doigt généreux », « une dose »).
- **Plantes, cueillette, préparation à risque.** Aucun protocole sans source botanique ou institutionnelle identifiable et citée. Une phrase de sécurité sobre (confusion d'espèce, traitement préalable), pas un paragraphe alarmiste.
- **Santé.** Aucune allégation (« détoxifiant », « bon pour… »), même reprise d'une autre source. Grossesse, traitement, pathologie : renvoi au professionnel de santé, sans conseil.
- **Attributions.** On n'attribue pas une décision, une invention ou une citation à une personne si la source ne le dit pas nommément.
- **Matériel.** On peut nommer un objet (une cafetière, un shaker), pas une marque présentée comme indispensable.

Contrôle avant de rendre : chaque chiffre, date et attribution de l'article est-il dans la liste fournie ou accompagné de sa source ? Sinon, il sort.

## 4. Liens

**Internes.** Une ancre descriptive dans une phrase, jamais « cliquez ici ». Un seul lien vers la page commerciale, dans la section qui y ramène. Chaque destination répond **200 sans redirection** : quand deux URL proches existent (`/page` et `/page-1`, deux slugs pour le même sujet), on vise celle qui reste, celle qui a des impressions, et on signale la paire dans le brief pour une 301. `scripts/article_checks.py` refuse un lien qui redirige.

**Externes.** Deux à quatre, vers des sources de référence (organismes publics, encyclopédies, publications scientifiques ou botaniques, presse spécialisée identifiable), jamais vers un concurrent qui vend la même chose. L'attribut `rel` suit la configuration (`blog.external_rel`, par exemple `nofollow`) ; le nombre maximal aussi (`blog.external_max`).

## 5. Gabarit de brief

Un brief de rédaction, écrit à la main ou par un autre outil, se range dans cet ordre. Les blocs vides se suppriment ; aucun ne s'invente.

```
RÔLE                 qui écrit, pour quel site, quelle ligne éditoriale
SUJET                ce que l'article couvre, en deux phrases
ANGLE IMPOSÉ         la question concrète tranchée, et ce que la conclusion n'est pas
CIBLE SEO            cible réelle, secondaires, terme pivot, intention, pages exclues
LECTEUR              qui, dans quelle situation, avec quelle question
REGISTRE             documentaire | pratique, page de référence éventuelle
LONGUEUR             fourchette, et « pas de remplissage »
STRUCTURE            H2 et H3, dans l'ordre, avec la section qui ramène à l'offre
TON                  registre de politesse du contexte de marque, première personne, ponctuation exclue
FAITS VÉRIFIÉS       liste fermée, source et date de relevé
INCERTITUDES         ce qui s'écrit comme incertain
INTERDICTIONS        ce qui ne s'écrit pas, et pourquoi
MAILLAGE INTERNE     URL vérifiées sans redirection, ancre, section, maximum
LIENS EXTERNES       nombre, type de source, attribut rel
LIVRABLES            title, meta, slug, article, tableau, JSON-LD, textes alternatifs, sources
CONTRÔLE             questions de fin, puis scripts/article_checks.py
```

Le registre de politesse (tutoiement ou vouvoiement) vient du contexte de marque, pas du brief. Un brief qui le contredit se signale avant d'écrire.
