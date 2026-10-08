# Contexte de marque — source unique

> Ce fichier est la seule source de contexte des skills `vk-*`. Ils le lisent au moment de s'exécuter (référence, pas copie). Quand l'offre change, on modifie ce fichier et rien d'autre.
>
> **Fraîcheur des faits** : état au `JJ/MM/AAAA`. Avant de publier un prix, une offre ou un chiffre, revérifie sur la source de vérité indiquée au §2. Si ce fichier et le site divergent, le site gagne, et l'écart est signalé pour mise à jour.
>
> Une ligne marquée `[hypothèse]` est un point de départ à valider, pas un fait. Une ligne marquée `A_COMPLETER` bloque tout livrable qui en dépend.

## 1. Qui

- Nom de marque (graphie exacte) :
- Ce que la marque fait, en une phrase, et ce qu'elle **ne fait pas** (la confusion la plus fréquente à éviter) :
- Type de site : `ecommerce` | `vitrine` | `hybride`
- Fondateur·rice, relecteur·rice qui valide avant mise en production :
- Raison sociale, immatriculation, siège (pour les mentions et le schema Organization) :
- Zone servie (pays, régions, livraison ou déplacement) :
- Signature, slogans utilisables :
- Domaine canonique (avec ou sans `www`) et règle de redirection :

## 2. Offre

Source de vérité des prix et de l'offre : `<URL ou fichier, ex. /products.json, grille tarifaire, page tarifs>`

| Produit ou prestation | Identifiant (handle, slug) | Prix ou « sur devis » |
|---|---|---|
| | | |

- Options et variantes (valeurs exactes, sensibles à la casse) :
- Conditions qui comptent : livraison, délais, engagement, garantie, zone d'intervention :
- Contenus éditoriaux existants (blog, annuaire, guides, réalisations) :

## 3. Affirmations autorisées et interdites

Autorisées (chacune avec sa source) :
-

Interdites ou à vérifier avant usage :
- Aucun chiffre inventé (clients, taux de satisfaction, « le meilleur »). Aucun témoignage inventé : uniquement des avis réels, cités tels quels, avec leur source.
- Promesses que la marque ne peut pas tenir aujourd'hui (retours, délais, résultats) :
- Allégations réglementées dans le secteur (santé, finance, environnement…) :
- Formulations qui prêteraient à la marque une activité qu'elle n'a pas :

## 4. Clients (ICP)

- Profil 1 — qui, dans quelle situation, ce qu'il cherche, ses freins, sa porte d'entrée sur le site :
- Profil 2 :
- B2B / B2C : parcours séparés ?

Quand un skill a besoin d'un ICP plus précis, il pose au plus deux questions, puis propose d'ajouter la réponse ici.

## 5. Ton de voix

- Trois adjectifs, et ce que chacun veut dire concrètement :
- Registre : `tu` | `vous`, et exceptions (pages légales, B2B) :
- Langue et variante (ex. français de France), format des prix et des dates :
- Mots et tournures bannis :
- Mots du client (ceux qu'il emploie vraiment) et jargon à expliquer :
- Hiérarchie d'information d'un produit ou d'une prestation (dans quel ordre on décrit) :
- Ponctuation et typographie (tiret cadratin, emojis, points d'exclamation) :

## 6. Direction artistique

- Palette (rôle → hex) : fond · texte · accent / CTA · secondaire · alerte
- Typographies (titres, texte courant, repli e-mail) :
- Univers visuel (formes, illustrations, photo, textures) :
- À ne jamais proposer (directions déjà écartées) :
- Emplacement des fichiers de marque (logos, charte, visuels) :

## 7. Stack et règles techniques

- Plateforme : `shopify` | `woocommerce` | `wordpress` | `webflow` | `static` | autre. Thème ou gabarit en production :
- On travaille sur : thème publié | copie de travail | dépôt Git. Ce qui est interdit sans demande explicite (publier, installer une extension payante, supprimer) :
- Architecture des pages (sections, gabarits, en-tête et pied de page, conventions de nommage) :
- Versionnement : nouvelles versions à côté des anciennes ? convention de suffixe :
- Champs personnalisés, métachamps, où vit le JSON-LD éditorial :
- Identifiants à ne jamais modifier (SKU, slugs, options) et pourquoi :
- Données structurées déjà émises par le thème ou des extensions (à ne pas doubler) :
- Outils branchés (avis, abonnement, réservation, email, automatisation) :
- Flux de travail : maquette → intégration → guide → validation :

## 8. Connecteurs disponibles

Liste ce qui est réellement branché ; chaque skill fonctionne en mode dégradé sans.

- Données SEO (DataForSEO, Search Console, autre) et limites du plan :
- Gestion de tâches (Notion, autre) et base qui reçoit les actions d'audit :
- Stockage des livrables (Drive, dossier local) :
- Publication réseaux (Zernio, autre), email, design :

Les identifiants de comptes, de dossiers et de bases se rangent dans `kit.config.json`, jamais dans un skill. Les clés d'API restent dans des variables d'environnement.

## 9. Méthode de travail

- Langue et niveau de formalité des échanges :
- Enchaîner les étapes sans confirmation, ou valider à chaque étape :
- Format attendu des audits (pourcentages, comparaisons, tableaux) :
- Qui valide quoi, et à quel moment :

## 10. SEO

- Pays et langue de référence (paramètres des outils de données) :
- **Avantage structurel** : ce que la marque peut écrire honnêtement et que ses concurrents ne peuvent pas (indépendance, données propres, position d'intermédiaire, métier de terrain) :
- Architecture des contenus : pilier → pivots → satellites (URL) :
- **Pages commerciales à protéger** et requêtes qui leur sont réservées (le blog ne les vise jamais) :
- Faux volumes à ne pas poursuivre (requêtes homonymes hors sujet) :
- Univers de mots-clés de départ (à valider par les volumes) :
- Concurrents organiques validés :
- Horizon de trafic réaliste, s'il a été fixé :

## 11. Réseaux sociaux

- Plateformes actives et rôle de chacune :
- Piliers éditoriaux et rotation :
- Cadence et heure de publication par défaut :
- Hashtags de marque et banque de hashtags :
- Paramètres UTM (source, medium, convention de campagne) :
- Mots-clés d'automatisation commentaire → message privé :
- Mascottes ou personnages récurrents (rôle, sujets, voix) :

## 12. Conformité

- Pays dont le droit s'applique, obligations sectorielles :
- Mentions obligatoires (partenariat commercial, jeu-concours, médiation, rétractation) :
- Données personnelles à ne jamais reprendre dans un contenu :
