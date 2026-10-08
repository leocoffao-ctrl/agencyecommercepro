---
name: shopify-liquid
description: Écrit, corrige et relit le code Liquid d'un thème Shopify en production (sections, snippets, schéma de section, gabarits JSON, métachamps, assets CSS et JS) en suivant l'architecture du thème en place et des règles de sécurité strictes. À utiliser dès que l'utilisateur parle de Liquid, de section, de snippet, de gabarit, de thème, de personnalisateur, de métachamp, de code Shopify, d'un bug d'affichage sur sa boutique, ou de convertir une maquette validée en Shopify, même sans dire Liquid.
---

# Liquid pour un thème en production

Adapté de `Shopify/Shopify-AI-Toolkit` (skill `shopify-liquid`, MIT). La référence Liquid officielle est dans `references/liquid-officiel.md`. Les étapes obligatoires du skill d'origine (recherche dans la documentation, validation et retour d'usage par scripts Node) ne sont pas reprises : elles ne tournent pas partout et envoient la requête, le code et un extrait du message de l'utilisateur à `shopify.dev`.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

La section 7 du contexte décrit le thème : nom, base, où l'on travaille, architecture, conventions de nommage, champs personnalisés, identifiants à ne pas toucher. Elle prime sur la documentation générale.

## Règles de sécurité

Le cas le plus risqué est le travail direct sur le thème publié. Dans tous les cas :

- Nouvelle fonctionnalité = **nouveaux fichiers** à côté des anciens, avec le suffixe de version du contexte, bascule par le gabarit JSON en dernier. L'ancien reste en place pour revenir en arrière.
- Modifier un fichier existant : livrer le fichier complet, un diff lisible et la version d'origine à garder de côté.
- Ne jamais publier un thème, installer une application, supprimer un fichier ou un réglage sans demande explicite.
- Ne jamais toucher aux références, aux slugs ni aux options de produit signalés comme sensibles au contexte §7 : ils pilotent souvent des automatisations.

## Architecture

Avant d'écrire, repère dans le thème :

- la génération du thème : blocs de section classiques, ou dossier `blocks/` des thèmes récents. Suis les conventions en place avant celles de la documentation ;
- la gestion de l'en-tête et du pied de page : groupes de sections globaux, ou navigation incluse dans chaque section. N'ajoute jamais un second pied de page ;
- les gabarits : `templates/<type>.<suffixe>.json`, et lequel est réellement utilisé pour chaque page ;
- l'espace de noms des métachamps et le champ qui porte le JSON-LD éditorial ;
- les données structurées déjà émises par le thème ou les applications (skill `seo-schema` avant d'en ajouter).

## Façon d'écrire

- CSS et JS par page dans `assets/`, classes préfixées pour ne rien casser ailleurs.
- Tout contenu éditable passe par `{% schema %}` : `settings` essentiels seulement, `blocks` pour les répétitions, `presets` pour que la section apparaisse dans le personnalisateur. Libellés et valeurs par défaut dans la langue du projet.
- Réglages de ressource (`product`, `collection`, `page`, `image_picker`, `url`) : ils renvoient l'objet, pas un identifiant texte.
- Images : `image_url` et `image_tag` avec `widths` et `sizes`, chargement différé sauf l'image principale.
- Prix : filtre `money` à l'affichage ; dans un JSON-LD, valeur sans devise avec un point décimal.
- Toujours `| escape` pour du texte dans un attribut, `| json` pour une valeur dans un `<script>`.
- Couleurs depuis la palette du contexte §6, exposées en variables CSS.
- Accessibilité : HTML sémantique (`<details>`/`<summary>` pour une FAQ, `<button>` pour une action), contraste de 4,5:1 au moins, focus visible.

## Contrôles avant livraison

1. JSON du `{% schema %}` valide : extrais-le et analyse-le.
   ```bash
   python3 - <<'EOF'
   import json, re, sys
   src = open(sys.argv[1] if len(sys.argv) > 1 else "sections/ma-section.liquid", encoding="utf-8").read()
   json.loads(re.search(r"{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}", src, re.S).group(1))
   print("schema valide")
   EOF
   ```
2. Balises Liquid équilibrées (`if`, `for`, `capture`) et aucun filtre inventé : en cas de doute sur un objet, un filtre ou une propriété, vérifie dans `references/liquid-officiel.md`, puis dans la documentation officielle.
3. Sélecteurs CSS et JS alignés avec les classes et les `id` du HTML.
4. Rendu vérifié pour : valeurs vides (réglage non rempli, métachamp absent), mobile à 390 px, produit sans image.

## Livrable

- Fichiers complets, rangés selon l'arborescence du thème (`sections/`, `snippets/`, `assets/`, `templates/`).
- `INTEGRATION.md` : chaque fichier à créer ou à modifier (chemin exact), ordre des opérations, test à faire, retour arrière.
- Validation par le relecteur du contexte §1 avant mise en production.

## Dans un éditeur de code

Le toolkit officiel de Shopify apporte la recherche dans la documentation et un validateur. Il transmet à Shopify, quand un de ses skills s'active, le dernier message (tronqué) et le code validé. Sa documentation indique la variable d'environnement qui coupe cette télémétrie : vérifie-la avant de l'installer sur un projet client.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Accès au thème (CLI, connecteur) | lecture des fichiers réels | l'utilisateur colle les fichiers concernés |
