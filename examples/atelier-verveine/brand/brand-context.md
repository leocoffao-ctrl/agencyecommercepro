# Contexte de marque — Atelier Verveine (marque fictive)

> **Exemple.** Atelier Verveine n'existe pas. Les producteurs, prix, chiffres et adresses ci-dessous sont inventés pour montrer un contexte rempli. Le domaine `example.com` est réservé à la documentation.
>
> **Fraîcheur des faits** : état au 01/10/2026. Avant de publier un prix ou une offre, revérifie sur `https://www.example.com/products.json?limit=250`. Si ce fichier et le site divergent, le site gagne.

## 1. Qui

- Nom de marque : **Atelier Verveine** (deux mots, deux capitales).
- Ce que la marque fait : elle sélectionne des infusions et des thés en vrac chez des producteurs français et les envoie en coffret. **Elle ne cultive pas et ne transforme pas** : jamais « cultivé par Atelier Verveine », jamais « nos plantations ».
- Type de site : `ecommerce`.
- Fondatrice : Camille. Relecteur avant mise en production : Sami.
- Raison sociale : Atelier Verveine SAS, siège à Angers (49). Immatriculation : `A_COMPLETER`.
- Zone servie : France métropolitaine et Belgique.
- Signature : « Atelier Verveine — la tisane a du goût ». Slogans : « Infuse, respire » · « Cueilli ici ».
- Domaine canonique : `https://www.example.com` (l'apex redirige en 301 vers `www`).

## 2. Offre

Source de vérité : `https://www.example.com/products.json?limit=250`.

| Produit | Handle | Prix |
|---|---|---|
| Coffret mensuel (abonnement) | coffret-mensuel | 19,90 / 27,90 € par mois |
| Coffret Soir | coffret-soir | 24,90 € |
| Coffret Fruité | coffret-fruite | 24,90 € |
| Coffret Découverte | coffret-decouverte | 32,90 € |
| Atelier assemblage (2 h) | atelier-assemblage | 59 € |

- Options des coffrets : « Format » = 3 sachets / 5 sachets ; « Type » = Vrac / Infusettes (valeurs exactes).
- Abonnement : sans engagement, pause et résiliation en ligne.
- Livraison offerte dès 45 €.
- Contenus : annuaire des producteurs (`/blogs/producteurs`), guides (`/blogs/guides`).

## 3. Affirmations autorisées et interdites

Autorisées :
- Plantes cultivées en France (source : fiches producteurs).
- Un producteur différent mis en avant chaque mois.
- Sans engagement. Livraison offerte dès 45 €.

Interdites ou à vérifier :
- Aucun chiffre inventé, aucun témoignage inventé.
- **Aucune allégation de santé** (sommeil, digestion, stress, « détox ») : une infusion est une denrée alimentaire. On décrit le goût, pas un effet.
- « Bio » seulement produit par produit, avec la certification du producteur.
- Pas de promesse de retour tant que la page de politique de retour n'est pas alignée avec les CGV.

## 4. Clients (ICP)

- [hypothèse] La buveuse du soir : 30-50 ans, boit une tisane après le dîner, lassée des sachets de supermarché. Frein : « ça n'a pas de goût ». Porte d'entrée : coffret Soir.
- [hypothèse] L'offreur de cadeau : cherche un cadeau qui ne soit ni du vin ni du chocolat. Porte d'entrée : coffret Découverte, atelier.
- [hypothèse] Le curieux du végétal : jardine, cuisine, veut savoir d'où vient la plante. Porte d'entrée : annuaire des producteurs.

## 5. Ton de voix

- Calme, précis, un peu malicieux. On parle comme une herboriste de marché, pas comme une notice.
- Registre : tutoiement partout, vouvoiement dans les pages légales.
- Français de France. Prix au format `24,90 €`.
- Mots bannis : bien-être, détox, rituel, premium, naturellement bon, ancestral.
- Mots du client : « une tisane qui a du goût », « pour le soir », « pas trop amer ».
- Ordre de description d'une plante : nom de la plante → notes en bouche → producteur et département → partie utilisée → récolte → température et durée d'infusion.
- Pas de tiret cadratin. Un emoji au plus par texte court. Un point d'exclamation par page.

## 6. Direction artistique

- Palette : fond `#FBF7EE` · texte `#1F2A1C` · accent `#D9622B` · secondaire `#3E7C4F` · clair `#EFE3C8`.
- Titres : Fraunces. Texte courant : police du thème. Repli e-mail : Georgia, serif.
- Univers : planches botaniques à l'encre, aplats, papier légèrement grainé.
- À ne jamais proposer : esthétique « spa » (galets, bougies), dégradés pastel.
- Fichiers de marque : `brand/assets/`.

## 7. Stack et règles techniques

- Shopify, thème publié « Herbier 2.3 ». On travaille sur une **copie de travail**, jamais sur le thème publié. Rien n'est publié, installé ou supprimé sans demande explicite.
- Sections préfixées `av-`. Un seul pied de page global (`sections/av-footer.liquid`).
- Nouvelles versions à côté des anciennes, suffixe `-v2`.
- Métachamps : namespace `av`. JSON-LD éditorial dans `custom.schema_json_ld`.
- SKU : `AV-<COFFRET>-<FORMAT>-<V|I>`. Ils pilotent l'envoi de la fiche d'infusion : ne pas les modifier.
- Le thème émet déjà `Product`, `Article` et `BreadcrumbList`.
- Outils : application d'abonnement, application d'avis, outil d'emailing.
- Flux : maquette HTML validée → Liquid → guide d'intégration → validation de Sami.

## 8. Connecteurs disponibles

- DataForSEO : oui, payant à l'appel.
- Search Console : oui.
- Notion : base « Actions » pour ranger les sorties d'audit.
- Drive : dossier « Blog » pour les livrables.
- Zernio : Instagram et LinkedIn connectés.

## 9. Méthode de travail

- Français, direct. Enchaîner les étapes sans confirmation, signaler les désaccords.
- Audits avec pourcentages et comparaison à la période précédente.
- Sami valide tout ce qui touche au thème.

## 10. SEO

- Pays et langue : France, `fr`.
- Avantage structurel : Atelier Verveine ne cultive rien. Elle peut comparer les producteurs entre eux, ce qu'aucun producteur ne peut faire honnêtement.
- Pilier : `/blogs/guides/infusions-francaises`. Pivot : `/pages/nos-producteurs`. Satellites : les guides.
- Pages commerciales protégées : `/collections/all` (« acheter tisane en vrac »), `/products/coffret-mensuel` (« abonnement tisane », « box tisane »).
- Univers de départ : tisane en vrac · infusion française · verveine citronnée · coffret tisane cadeau · abonnement tisane.
- Concurrents validés : `A_COMPLETER`.

## 11. Réseaux sociaux

- Instagram (canal principal), LinkedIn (coulisses de la sélection).
- Piliers : Plantes · Coffret · Producteurs · Coulisses.
- Un post tous les 2 jours, 12:30 heure de Paris.
- Hashtags de marque : `#atelierverveine`.
- UTM : `utm_source=<plateforme>&utm_medium=social&utm_campaign=<AAAA-MM-sujet>`.

## 12. Conformité

- Droit français. Règlement européen sur les allégations de santé : aucune allégation non autorisée.
- Partenariat rémunéré : mention « Collaboration commerciale ».
- Ne jamais reprendre de donnée personnelle d'un producteur au-delà de ce que son propre site publie.
