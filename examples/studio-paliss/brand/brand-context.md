# Contexte de marque — Studio Paliss (marque fictive)

> **Exemple.** Studio Paliss n'existe pas : activité, prix et adresses sont inventés pour montrer un contexte de **site vitrine**. Le domaine `example.org` est réservé à la documentation.
>
> **Fraîcheur des faits** : état au 01/10/2026. La source de vérité des tarifs est la grille `brand/tarifs-2026.md`. Si ce fichier et le site divergent, le site gagne.

## 1. Qui

- Nom de marque : **Studio Paliss**.
- Ce que la marque fait : menuiserie sur mesure pour particuliers (bibliothèques, dressings, cuisines) autour de Lyon. **Elle ne vend pas de meubles en ligne et ne fait pas de pose de cuisine d'une autre marque.**
- Type de site : `vitrine`.
- Fondateur et seul relecteur : Noé.
- Raison sociale : `A_COMPLETER`. Atelier à Villeurbanne (69).
- Zone d'intervention : Lyon et 40 km autour.
- Signature : « Studio Paliss — du sur-mesure qui tombe juste ».
- Domaine canonique : `https://www.example.org` (sans redirection `www` particulière).

## 2. Offre

Source de vérité : `brand/tarifs-2026.md`.

| Prestation | Slug | Prix |
|---|---|---|
| Bibliothèque sur mesure | bibliotheque-sur-mesure | à partir de 2 400 € |
| Dressing sur mesure | dressing-sur-mesure | à partir de 3 100 € |
| Cuisine sur mesure | cuisine-sur-mesure | sur devis |
| Visite et relevé de cotes | visite | offerte dans la zone |

- Délai moyen entre devis signé et pose : 8 à 10 semaines (à redater à chaque mise à jour).
- Garantie décennale : assureur et numéro `A_COMPLETER` avant toute mention.
- Contenus : page Réalisations, trois guides.

## 3. Affirmations autorisées et interdites

Autorisées :
- Fabrication à l'atelier de Villeurbanne.
- Bois issus de scieries de la région (source : factures fournisseurs, à citer par essence).

Interdites ou à vérifier :
- Aucun nombre de chantiers, aucune note moyenne tant qu'une source d'avis n'est pas branchée.
- « Garantie décennale » : pas avant le numéro de contrat.
- « Écologique », « durable » : seulement avec la certification de l'essence concernée.
- Pas de délai ferme dans un texte : toujours « en moyenne », avec la date.

## 4. Clients (ICP)

- Le propriétaire qui aménage : vient d'acheter, a un mur ou une sous-pente impossible à meubler. Frein : le prix face au meuble en kit. Porte d'entrée : page Bibliothèque, Réalisations.
- [hypothèse] L'architecte d'intérieur : cherche un atelier fiable pour sous-traiter. Porte d'entrée : page Professionnels (à créer).

## 5. Ton de voix

- Posé, concret, sans effet. On parle en millimètres et en essences, pas en « espaces de vie ».
- Registre : vouvoiement partout.
- Mots bannis : sublimer, cocon, haut de gamme, sur-mesure d'exception, artisan passionné.
- Mots du client : « un meuble qui rentre pile », « sous l'escalier », « jusqu'au plafond ».
- Ordre de description d'une réalisation : pièce et contrainte → solution → essence et finition → dimensions → durée du chantier.
- Pas de tiret cadratin, pas d'emoji sur le site.

## 6. Direction artistique

- Palette : fond `#F4F1EC` · texte `#22201D` · accent `#B4532A` · secondaire `#5C6B5A`.
- Titres : Instrument Serif. Texte : Inter.
- Univers : photos de chantiers réels en lumière naturelle, plans cotés en filigrane.
- À ne jamais proposer : photos de banque d'images, rendus 3D présentés comme des réalisations.
- Fichiers : `brand/assets/`.

## 7. Stack et règles techniques

- WordPress, thème enfant maison. On travaille sur un environnement de préproduction, mise en ligne par Noé.
- Gabarits : `page-service.php`, `single-realisation.php`. Champs personnalisés via ACF.
- Aucune extension payante sans accord.
- Le thème émet `Organization` et `BreadcrumbList`. Pas de `LocalBusiness` pour l'instant.
- Formulaire de contact : extension de formulaires, envoi vers la boîte de l'atelier.
- Flux : maquette HTML → gabarit PHP → test en préproduction → mise en ligne.

## 8. Connecteurs disponibles

- Search Console : oui. DataForSEO : non (les skills SEO tournent en mode dégradé).
- Pas d'outil de tâches : les actions d'audit sortent en CSV.
- Pas d'outil de publication réseaux.

## 9. Méthode de travail

- Français, vouvoiement. Valider à chaque étape.
- Les audits tiennent sur une page, avec les trois actions prioritaires en tête.

## 10. SEO

- Pays et langue : France, `fr`. Requêtes locales (Lyon, Villeurbanne, Rhône).
- Avantage structurel : l'atelier fabrique lui-même. Il peut publier des temps de fabrication, des sections de bois et des photos d'étapes qu'un revendeur n'a pas.
- Pages commerciales protégées : `/bibliotheque-sur-mesure` (« bibliothèque sur mesure lyon »), `/dressing-sur-mesure` (« dressing sur mesure lyon »), `/cuisine-sur-mesure`.
- Faux volume : « paliss » renvoie surtout à des palissades de jardin. Ne pas viser ces requêtes.
- Univers de départ : menuisier sur mesure lyon · bibliothèque sous escalier · dressing sous pente · prix bibliothèque sur mesure.

## 11. Réseaux sociaux

- Instagram seulement, un chantier par semaine. `A_COMPLETER` pour le reste.

## 12. Conformité

- Droit français. Mentions d'assurance obligatoires sur devis et factures.
- Photos de chantiers : accord écrit du client, aucune adresse ni nom de famille.
