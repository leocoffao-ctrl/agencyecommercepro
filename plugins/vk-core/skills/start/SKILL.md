---
name: start
description: Routeur du kit — regarde où en est le projet (contexte, site, contenus, trafic, réseaux) et propose la prochaine étape utile avec le skill qui la réalise. À utiliser dès que l'utilisateur demande « par où je commence », « et maintenant », « quelle est la suite », « qu'est-ce qu'il me reste à faire », veut un plan de lancement ou une feuille de route pour son site, même sans nommer le kit.
---

# Start — quelle est la prochaine étape ?

Tu ne produis pas de livrable de fond ici. Tu lis l'état du projet et tu orientes vers le bon skill.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Introuvable : la prochaine étape est le skill `setup`, dis-le et arrête-toi là.

## 1. Lire l'état

- **Contexte** : sections encore en `A_COMPLETER`, hypothèses non validées.
- **Site** : existe-t-il ? `robots.txt`, `sitemap.xml`, nombre de pages par type, pages commerciales présentes.
- **Contenus** : blog, annuaire, guides ; date du dernier article.
- **Mesure** : Search Console ou équivalent branché ? Suivi de conversion en place ?
- **Diffusion** : comptes sociaux actifs, email, campagnes en cours.

Dis ce que tu n'as pas pu vérifier plutôt que de le supposer.

## 2. Le parcours

| Phase | But | Skills | Passe à la suivante quand |
|---|---|---|---|
| 0. Cadrage | Savoir ce qu'on vend, à qui, sur quel ton | `setup`, `brand-context` | Sections 1 à 7 du contexte remplies |
| 1. Construire | Des pages qui expliquent et qui vendent | `site-clone`, `copywriting`, `shopify-liquid` (Shopify) | Accueil, offre principale et pages légales en ligne |
| 2. Être trouvé | Un site indexable, compris des moteurs et des IA | `seo-audit`, `seo-schema`, `seo-pages`, `seo-geo`, `seo-data` | Aucun point critique ouvert dans l'audit |
| 3. Publier | Du contenu régulier qui amène du trafic qualifié | `seo-writer`, `blog-pipeline`, `directory-pages` | Un rythme tenu quatre semaines de suite |
| 4. Convertir | Transformer les visites en demandes ou en ventes | `cro`, `email-flows` | Parcours principal mesuré et testé |
| 5. Diffuser | Faire circuler ce qui existe | `social-plan`, `social-publish`, `mascot-reels`, `ad-creative`, `ads-audit` | En continu |

Les phases ne sont pas étanches : un site déjà en ligne commence souvent par la phase 2.

## 3. Adapter au type de site

**E-commerce** : fiches produit, collections et panier passent avant le blog. Le schema Product et le flux marchand comptent tôt. `email-flows` commence par le panier abandonné et le post-achat.

**Vitrine** : la page de service, la preuve (réalisations, avis, certifications) et le formulaire de contact tiennent le rôle de la fiche produit. Le schema utile est `Organization`, `LocalBusiness` si la marque reçoit du public, `Service`. La conversion à mesurer est la prise de contact. `email-flows` commence par la réponse à une demande et la relance de devis.

**Hybride** : traite la partie qui rapporte aujourd'hui en premier.

## 4. Répondre

```
Où en est le projet : 3 à 5 constats, chacun avec sa source
Prochaine étape     : une seule, avec le skill et ce qu'il produira
Ensuite             : les deux suivantes, en une ligne chacune
Ce qui bloque       : faits manquants dans le contexte, accès à obtenir
```

Une seule prochaine étape. Si deux se valent, choisis celle qui débloque les autres et dis pourquoi.

## Dépendances

- Aucun connecteur requis. Avec un connecteur de données SEO ou la Search Console, l'état « être trouvé » est mesuré au lieu d'être estimé.
- Les skills cités appartiennent aux plugins `vk-seo`, `vk-content`, `vk-marketing`, `vk-ads`, `vk-shopify`, `vk-design`, `vk-social`, `vk-reels`. Un plugin absent se signale, avec la commande d'installation.
