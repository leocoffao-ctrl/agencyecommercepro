# Prompt master — pages d'annuaire

Objectif double : devenir la meilleure page du web sur une entité tierce (une marque, un artisan, un lieu, un prestataire), puis ouvrir une relation commerciale avec elle.

Le vocabulaire est volontairement neutre. « Entité » désigne ce que la fiche décrit ; « la marque » désigne le site qui publie. Le type d'entité, sa page pivot et ses seuils sont dans `kit.config.json`, bloc `directory.types`.

---

## 0. Le raisonnement, à lire avant d'écrire

### Pourquoi une fiche tierce peut se classer sur le nom d'une entité

Une requête sur un nom de marque ou de lieu appelle des réponses que le site officiel ne donne presque jamais. Une fiche tierce qui les donne se classe à côté du site officiel, parfois devant.

Vérifie-le sur le projet avant de produire en volume : positions actuelles des fiches existantes sur les noms d'entités (Search Console ou outil de données). Sans preuve interne, commence par cinq fiches et mesure.

### Pourquoi une fiche mince n'y arrive pas

Les défauts habituels d'un annuaire généré par gabarit, à chercher sur les fiches existantes :

1. Une centaine de mots uniques, le reste étant du gabarit partagé.
2. Descriptions tronquées par un filtre de longueur.
3. Variables de gabarit affichées brutes.
4. Chaînes concaténées sans accord grammatical.
5. Sections vides.
6. Lien de carte vers une recherche par nom, sans identifiant de lieu stable.
7. Aucun lien vers le site officiel ni vers les comptes de l'entité.
8. Module d'avis vide sur toutes les fiches.
9. Title et H1 identiques.

### Le contrat de la fiche

**La fiche doit être la meilleure page du web sur cette entité, y compris meilleure que la sienne.**

C'est atteignable parce que le site d'une entité ne fait jamais trois choses :
- il ne se compare pas à ses concurrents ;
- il ne dit pas à qui son offre ne convient pas ;
- il ne publie pas de prix ramenés à une unité comparable, ni de données d'offre structurées.

Ces trois angles sont le cœur de la fiche. Ce sont aussi ceux qui la rendent citable par les moteurs génératifs.

### La mécanique de partenariat

La fiche est l'argumentaire. Séquence :

1. Publication, sans accord préalable, sur données publiques et factuelles.
2. La fiche se positionne sur « [entité] avis », « [entité] prix », « [entité] + ville ».
3. Prise de contact : « votre fiche est en position X sur votre nom, elle a reçu Y visites ce mois-ci, voici ce qu'on peut en faire ensemble ».
4. Offres possibles : référencement dans l'offre de la marque, lien affilié suivi, encart revendiqué avec contenu fourni par l'entité.

Conséquence de rédaction : **la fiche est factuelle et défendable, jamais dénigrante.** Une fiche agressive tue la négociation et crée un risque juridique. Une fiche élogieuse et creuse ne se classe pas. La ligne : rigoureuse, comparative, honnête, utile au lecteur.

---

## 1. Ce qui doit exister avant la rédaction

Aucune fiche n'est rédigée sans ce bloc rempli. Champ vide = champ absent de la fiche, jamais champ inventé.

### 1.1 Fiche de données

```yaml
identite:
  nom_canonique:            # exactement la graphie officielle
  variantes_nom:            # autres graphies rencontrées
  slug:                     # convention unique, voir 1.3
  annee_creation:           # + source
  dirigeants:               # noms complets si publics et utiles
  statut:                   # nature de l'activité, en clair
  ville:
  region:
  adresse_complete:
  identifiant_de_lieu:      # identifiant stable de la fiche de carte, pas une URL de recherche
  site_officiel:
  comptes_sociaux:

specialite:                 # ce qui distingue l'entité sur son métier
  positionnement:           # + justification sourcée
  moyens:                   # équipement, méthode, si publics
  approvisionnement:        # fournisseurs, circuits, si publics
  certifications:           # avec l'organisme, si affiché

offre:
  nb_references:            # relevé à une date précise
  formats:
  prix_min:
  prix_max:
  prix_unitaire_comparable: # calculé, pas estimé (au kilo, à l'heure, au m²…)
  date_releve_prix:         # obligatoire
  references_phares:        # 2 à 3
  disponibilite:            # sur place, en ligne, revendeurs, chez la marque

usage:                      # pour un lieu qui reçoit du public
  horaires:                 # source + date
  acces:
  reservation:
  accessibilite:
  paiement:

preuves:
  distinctions:             # concours, années, source
  presse:                   # 2 à 3 citations avec URL et date
  note_en_ligne:            # note + nombre d'avis + date de relevé
  autres_notes:

relation:
  partenaire:               # oui / non
  present_dans_l_offre:     # oui / non, où
  lien_affilie:
  statut_fiche:             # A non revendiquée / B revendiquée / C partenaire

assets:
  photo_principale:         # source + droits
  photos_secondaires:
  logo:                     # droits d'usage
```

### 1.2 Sources autorisées, par ordre de fiabilité

1. Site officiel de l'entité (prix, offre, histoire).
2. Fiche d'établissement publique (adresse, horaires, note, volume d'avis), toujours datée.
3. Comptes officiels (actualité, équipe).
4. Registre des entreprises (année de création, forme juridique).
5. Presse locale ou spécialisée datée.
6. Relevés internes de la marque, datés (test, achat, visite).

**Interdits comme source** : les autres annuaires, les agrégateurs, les fiches concurrentes. Reprendre leur chiffre propage leur erreur et fait perdre l'avantage.

**Données personnelles** : le parcours privé d'un dirigeant tiré de la presse (santé, situation administrative, vie familiale) ne va pas dans la fiche. Nom, rôle et ce que l'entité revendique elle-même suffisent.

### 1.3 Convention de slug, une seule

`<préfixe du type>/<nom-sans-article-sans-accent>`

- Pas de ville, pas de suffixe de catégorie, pas de millésime.
- Une entité qui relève de deux types (par exemple un fabricant qui tient aussi une boutique) : **une seule fiche**, dans le type principal. Un doublon fragmente l'autorité : fusion et redirection 301 avant toute nouvelle production.

### 1.4 Qualification préalable (lieux)

- L'établissement existe-t-il encore, sous la même enseigne ? Une fermeture ou une reprise se dit dès le sous-titre.
- Un domaine officiel a-t-il été racheté ? Contrôler chaque lien sortant.
- Ce qu'on ne sait pas se dit (« non communiqué »). On ne suppose ni horaire, ni prix, ni fournisseur.

---

## 2. Le fan-out de la requête de nom

Une requête sur un nom se décompose. La fiche répond à chaque sous-question dans un bloc autonome.

| Sous-requête | Bloc qui y répond | Format |
|---|---|---|
| qui est [entité] | Présentation | Paragraphe de réponse en tête |
| [entité] avis | Avis agrégés et lecture | Note sourcée |
| [entité] prix | Tableau de l'offre avec prix unitaire | Tableau |
| que choisir chez [entité] | Tableau de décision par profil | Tableau |
| [entité] où acheter / comment y aller | Accès | Liste ordonnée |
| [entité] adresse horaires | Infos pratiques | Données et carte |
| [entité] spécialité, méthode | Spécialité expliquée | Échelle et texte |
| [entité] vs [concurrent] | Comparatif à trois | Tableau |
| [entité] certification | Certifications | Liste factuelle |
| [entité] visite, atelier | Accès du public | Paragraphe |
| alternatives à [entité] | Alternatives | Maillage |

**Règle** : une sous-requête, un bloc autonome, une seule page. Jamais une page par sous-requête.

---

## 3. Architecture de page

Ordre imposé. Chaque bloc est extractible seul.

```
01  FIL D'ARIANE                 Accueil > [Type] > [Entité]
02  EN-TÊTE                      H1 + badges + photo + ligne de données
03  RÉPONSE RAPIDE               6 puces, encadré, toute la thèse
04  INFOS PRATIQUES              adresse, horaires, carte, site, comptes, note
05  SOMMAIRE ANCRÉ
06  PRÉSENTATION                 histoire, dates, chiffres
07  SPÉCIALITÉ                   échelle à trois segments + ce que ça implique
08  OFFRE                        tableau références, formats, prix unitaire daté
09  TABLEAU DE DÉCISION          profil > référence > pourquoi
10  NOTRE TEST                   contenu propriétaire, incopiable
11  CE QUE ÇA VAUT               prix comparé au marché, verdict
12  À QUI ÇA NE CONVIENT PAS     bloc de transparence, obligatoire
13  ACCÈS                        où acheter, comment y aller
14  COMPARATIF                   [entité] face à deux entités proches
15  AVIS                         agrégés sourcés + module d'avis du site
16  FAQ                          8 questions issues du fan-out
17  ALTERNATIVES                 6 fiches du même ensemble
18  ENCART MARQUE                « vous êtes [entité] ? » (voir §9)
19  SOURCES + DATE DE RELEVÉ
20  À DÉCOUVRIR                  maillage commercial
```

### Volumétrie cible

| Bloc | Mots |
|---|---|
| Réponse rapide | 90 à 120 |
| Présentation | 250 à 400 |
| Spécialité | 200 à 300 |
| Offre (hors tableau) | 120 à 180 |
| Notre test | 250 à 400 |
| Ce que ça vaut | 200 à 300 |
| À qui ça ne convient pas | 120 à 180 |
| Accès | 150 à 250 |
| Comparatif (hors tableau) | 100 à 150 |
| FAQ | 8 × 50 à 80 |
| **Total rédactionnel unique** | **1 800 à 2 600** |

Sous le plancher du type (`min_words`), la fiche ne bat pas le site de l'entité. Au-dessus du plafond, la densité factuelle se dilue. Un lieu a moins de matière qu'un fabricant : son type peut avoir un plancher plus bas.

### Spécification des blocs qui comptent

**02 En-tête.** H1 = le nom exact, seul. Sous-titre de 15 à 25 mots avec un fait chiffré. Ligne de données courte. Badges : partenaire, présent dans l'offre, « fiche vérifiée le [date] » (un signal de fraîcheur gratuit). Photo 1200 × 630, WebP, moins de 150 Ko, dimensions déclarées, priorité de chargement haute, pas de chargement différé.

**03 Réponse rapide.** Le bloc le plus rentable. Six puces, chacune vraie et complète isolément :
1. Ce que c'est : lieu, année, statut, spécialité.
2. Ce qui la distingue et ce que ça donne à l'usage.
3. La fourchette de prix unitaire, avec la date de relevé.
4. Pour qui c'est fait.
5. Pour qui ce ne l'est pas.
6. Où on la trouve.

Chaque puce renomme son sujet. Marquer le bloc `speakable` dans le schema.

**07 Spécialité.** Ne pas s'arrêter à l'échelle visuelle : expliquer la conséquence pour l'utilisateur. L'échelle ne s'active qu'avec une source.

**08 Offre.** Tableau aux en-têtes autoportants. Prix unitaire calculé : c'est la donnée que personne ne publie. Une ligne de relevé sous le tableau. Jamais de prix en dur dans le texte, seulement dans ce tableau daté.

**09 Tableau de décision.** Six à huit lignes, par profil d'utilisateur. C'est le bloc qui convertit et le plus extrait par les moteurs.

**10 Notre test.** Le seul contenu qu'aucun concurrent ne peut copier. Si la marque a testé : relevé réel et protocole (méthode, conditions, date). Sinon, **le bloc est supprimé**. Un bloc absent vaut mieux qu'un bloc inventé.

**11 Ce que ça vaut.** Situer le prix unitaire dans le marché, avec la fourchette de référence et sa source. Verdict argumenté : cher et justifié, aligné, ou agressif. Sans fourchette de marché sourcée, calibrer avec les prix relevés le même jour chez les deux entités du comparatif, et signaler le manque.

**12 À qui ça ne convient pas.** Obligatoire, jamais négociable, même pour un partenaire. Formulations factuelles, tirées de l'offre réelle. C'est le signal de sérieux le plus fort, et ce qui fait croire le reste.

**13 Accès.** Ordre imposé : site officiel de l'entité (nofollow), lieu physique (carte), **la marque** (lien suivi, appel à l'action), revendeurs. Mettre le site officiel en premier rend la fiche crédible et le partenariat possible.

**14 Comparatif.** Deux entités réellement proches, présentes dans l'annuaire, choisies sur la spécialité ou la région. Colonnes : spécialité, prix unitaire, offre, distribution, point fort, point faible. Liens vers leurs fiches.

**15 Avis.** Note en ligne : valeur, nombre d'avis, **date de relevé**. Jamais de citation textuelle d'un avis tiers : les thèmes se résument. `aggregateRating` seulement si des avis sont réellement affichés sur la page.

**16 FAQ.** Huit questions tirées du fan-out, réponses de 50 à 80 mots, autonomes. FAQ visible strictement identique au schema.

---

## 4. Règles de rédaction pour les moteurs génératifs

| Règle | Application |
|---|---|
| Autonomie référentielle | Chaque bloc renomme l'entité. Jamais de pronom en ouverture |
| Réponse en tête | Conclusion d'abord, explication ensuite |
| H2 = question ou affirmation complète | « Que choisir chez [entité] ? » plutôt que « L'offre » |
| Densité factuelle | Un chiffre, une date, un nom ou une condition par bloc |
| Longueur d'atome | 40 à 80 mots par bloc-réponse |
| Qualification | « selon le site officiel », « relevé le [date] » |
| Lexique canonique | Une seule graphie de l'entité ; les variantes rattachées une fois |
| Cohérence entre pages | Le même fait ne s'énonce pas différemment sur deux fiches |

**Test avant publication** : trois blocs copiés au hasard dans un document vierge. S'ils restent vrais, complets et attribuables, la fiche est bonne.

**À proscrire** : superlatifs non étayés, vocabulaire banni du contexte de marque, chiffres décoratifs, « selon les experts », bourrage du nom.

Paraphrase les descriptions officielles : ne recopie pas leurs phrases.

---

## 5. Assets : tout en HTML et CSS servis

Les robots d'IA ont des budgets de temps courts et ne voient pas ce qui est injecté après chargement.

**Autorisés, sans JavaScript** : échelle à trois segments, jauge de prix en barres CSS, badges, tableaux qui basculent en cartes sous 640 px (`data-label`), sommaire collant, FAQ en `<details>`/`<summary>`, carte statique avec lien, grille de photos en chargement différé.

**Interdits** : bibliothèque JavaScript tierce, texte injecté par script, information critique dans une image seule, image de tableau, widget d'avis bloquant, police web supplémentaire.

**Carte** : le lien utilise toujours un identifiant de lieu stable (`https://www.google.com/maps/place/?q=place_id:[ID]`). Une URL de recherche par nom casse dès qu'un homonyme apparaît.

**Images** : dimensions déclarées, texte alternatif descriptif, nom de fichier égal au slug. **Droits** : photo fournie par l'entité, photo de la marque, ou libre de droits. Jamais une capture du site de l'entité sans accord écrit.

**Performance** : le HTML servi contient tout le texte de la fiche.

---

## 6. Liens

| Destination | Attributs |
|---|---|
| Site officiel de l'entité | `rel="nofollow noopener"` `target="_blank"` |
| Comptes sociaux, carte, fiche d'établissement | `rel="nofollow noopener"` `target="_blank"` |
| Presse, institution, concours, registre | `rel="noopener"` (source d'autorité) |
| Lien affilié | `rel="sponsored noopener"`, obligatoire dès qu'il y a rémunération |
| Lien déposé par un utilisateur | `rel="ugc"` |
| Interne | aucun attribut, ancre contextualisée |

### Maillage interne, minimum par fiche

| Sens | Nombre | Cible |
|---|---|---|
| Fiche → pivot | 2 | la page pivot du type |
| Fiche → autres fiches | 6 à 8 | même spécialité ou même région, proximité géographique d'abord |
| Fiche → commercial | 3 | pages de vente de la marque |
| Fiche → guide | 1 à 2 | guides liés |
| Pivot → fiche | 1 | la fiche est listée sur la page pivot |

Trois variantes d'ancre au moins vers la page pivot, à l'échelle du site. S'il existe deux pages pivot concurrentes : fusion et redirection avant de poser le maillage.

---

## 7. Données structurées

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Nom] : [nature] à [Ville]",
  "datePublished": "[ISO]",
  "dateModified": "[ISO, réel]",
  "author": {"@type": "Organization", "name": "[marque]"},
  "publisher": {"@type": "Organization", "name": "[marque]"},
  "image": "[URL exacte de l'image d'en-tête affichée]",
  "about": {"@type": "[type du contexte]", "name": "[Nom exact]", "url": "[site officiel]", "sameAs": ["…"]},
  "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".reponse-rapide"]}
}
```

`about` rattache la page à l'entité : c'est le levier de désambiguïsation le plus direct sur une requête de nom.

À ajouter : `BreadcrumbList` dont l'échelon intermédiaire pointe vers la page pivot ; `FAQPage` identique à la FAQ visible ; `ItemList` sur le tableau de l'offre.

Interdits : `aggregateRating` sans avis affichés ; le type commercial de l'entité (`LocalBusiness`, `Restaurant`…) en racine, puisque la marque n'est pas cet établissement ; `Product` sur des références que la marque ne vend pas ; `image` différente de celle affichée ; `dateModified` mise à jour sans modification réelle.

---

## 8. Métadonnées

| Élément | Règle |
|---|---|
| Title | `[Nom] : avis et prix \| [marque]` ou `[Nom], [nature] à [Ville] \| [marque]`. Moins de 60 caractères. Contient le nom exact |
| H1 | `[Nom]` seul, différent du title |
| Meta description | Moins de 155 caractères. Une information que le site de l'entité ne donne pas |
| Slug | Voir 1.3 |
| Image de partage | Identique à l'image d'en-tête |

Le title travaille dans la page de résultats contre le site officiel : il porte ce que l'entité ne promet pas (« avis », « prix »). Le H1 porte le contrat de lecture.

---

## 9. La couche partenariat

### 9.1 L'encart marque (bloc 18)

Présent sur toutes les fiches. Trois états :

- **A, non revendiquée** : « Vous êtes [Nom] ? Cette fiche est rédigée à partir de sources publiques. Vous pouvez la revendiquer gratuitement pour corriger les informations… » et un lien de contact.
- **B, revendiquée** : mention datée, contenu fourni par l'entité dans un bloc identifié.
- **C, partenaire** : mention et appel à l'action commercial.

L'encart génère des prises de contact, signale la nature éditoriale de la fiche (protection juridique) et alimente la fraîcheur.

### 9.2 Suivi

- Un paramètre de suivi sur chaque lien sortant vers l'entité, pour chiffrer le trafic envoyé.
- Un code dédié par partenaire, seul moyen d'attribuer une vente sans outil d'affiliation.
- Relevé mensuel : position de la fiche sur le nom, vues, clics sortants.

### 9.3 Ordre d'attaque

1. Entités déjà partenaires : conversion immédiate, aucun risque relationnel.
2. Entités à fort volume de recherche sur leur nom.
3. Entités sans site performant : elles ont le plus à gagner.
4. Le reste, en volume.

### 9.4 Garde-fous juridiques

- Usage du nom : licite dans un contexte éditorial et informatif. Pas dans le title d'une page de vente ni en achat de mots-clés sans accord.
- Mention de nature éditoriale visible sur la fiche.
- Aucune allégation négative non sourcée.
- Photos : jamais reprises sans accord écrit.
- Procédure de retrait documentée : une entité qui demande une correction ou un retrait obtient une réponse sous 7 jours. Le conflit coûte plus cher que la fiche.
- Mention de partenariat commercial quand il y a rémunération, selon le droit du pays (contexte §12).

Ces garde-fous sont des pratiques de prudence, pas un avis juridique : pour un secteur réglementé, fais valider le modèle par un professionnel du droit.

---

## 10. Anti-cannibalisation

| Situation | Décision |
|---|---|
| Deux fiches pour la même entité | Fusion dans le type principal et 301 |
| Une page de vente de la marque porte le nom de l'entité | Fiche = informationnel et comparatif ; page de vente = transactionnel ; lien croisé dans les deux sens |
| Une fiche produit se classe sur le nom de l'entité | La fiche d'annuaire devient le pivot du nom, le produit reste sur sa requête produit |
| L'entité est citée dans un guide | Le guide lie la fiche, la fiche ne vise pas la requête du guide |

La fiche ne vise jamais une requête transactionnelle générique. Elle vise le nom et ses dérivés.

---

## 11. Contrôles avant publication

### 11.1 Automatiques

`scripts/check_fiche.py` vérifie : densité rédactionnelle, variables non résolues, troncatures, vocabulaire banni, équilibre des balises, attributs des liens sortants, lien de carte par identifiant de lieu, maillage (pivot, ensemble, commercial), variété des ancres, dimensions et texte alternatif des images, blocs obligatoires, nombre de puces et de questions, FAQ visible identique au schema, types interdits, fil d'Ariane du schema.

Ensuite, à la main : chaque URL interne répond 200 ; le contenu apparaît dans le HTML servi.

### 11.2 Checklist humaine

Données
- [ ] Chaque chiffre a une source
- [ ] Les prix portent une date de relevé
- [ ] Aucun champ inventé
- [ ] Graphie de l'entité identique partout
- [ ] L'identifiant de lieu est le bon établissement, homonymes vérifiés

Contenu
- [ ] Au-dessus du plancher de mots uniques
- [ ] Réponse rapide : six puces autonomes
- [ ] Chaque H2 est une question ou une affirmation complète
- [ ] Bloc « à qui ça ne convient pas » présent
- [ ] Bloc de test présent **ou supprimé**, jamais rempli d'adjectifs
- [ ] Prix unitaire calculé et comparé
- [ ] Comparatif avec deux entités réellement proches
- [ ] Test d'autonomie passé sur trois blocs

Technique
- [ ] Title différent du H1, moins de 60 caractères
- [ ] Meta description non tronquée
- [ ] Images avec dimensions ; image d'en-tête sans chargement différé
- [ ] Aucun script tiers ajouté
- [ ] Schema cohérent avec l'affichage, testé

Maillage
- [ ] Deux liens vers le pivot, ancres variées
- [ ] Six à huit fiches du même ensemble
- [ ] Trois liens commerciaux
- [ ] La fiche est listée sur la page pivot

Partenariat
- [ ] Encart présent, état correct
- [ ] Lien officiel en nofollow, lien affilié en sponsored
- [ ] Mention de nature éditoriale visible

---

## 12. Grille de score

Une fiche se publie à 80 sur 100 au moins.

| Critère | Points |
|---|---|
| Mots uniques hors gabarit (plancher = 15, haut de la cible = 25) | 25 |
| Faits vérifiables sourcés (2 points par fait, plafonné) | 20 |
| Contenu propriétaire (test, prix unitaire comparé, comparatif) | 15 |
| Atomisation : blocs autonomes, réponse en tête | 10 |
| Bloc de transparence présent et substantiel | 5 |
| Schema complet et cohérent | 8 |
| Maillage conforme | 7 |
| Assets conformes et légers | 5 |
| Métadonnées conformes | 5 |
| Encart de partenariat opérationnel | 5 |

---

## 13. Ce qui est facile à oublier

- **La date de relevé.** Sans elle, tout chiffre devient faux en silence.
- **La fiche sans le pivot.** Quarante fiches sans page pivot unique se battent seules.
- **Les homonymes.** Une similarité de nom n'est pas une duplication.
- **Le calendrier de révision.** Une fiche avec des prix se révise chaque trimestre.
- **Les avis vides.** Un module vide sur toutes les fiches est un signal négatif : l'amorcer ou le masquer.
- **Le cul-de-sac.** Trois liens internes sortants au moins.
- **La profondeur de clic.** Le pivot est accessible depuis le menu.
- **L'ordre de publication.** Les fiches à fort volume d'abord, pour mesurer le modèle avant de le dupliquer.
- **La cohérence entre fiches.** Un lexique canonique par spécialité, écrit une fois.
- **Le lien retour.** Une entité satisfaite de sa fiche la relaie : c'est le lien externe le plus naturel à obtenir.
