---
name: brand-context
description: Localise, lit et met à jour le contexte de marque (brand-context.md et kit.config.json) que tous les skills vk-* consultent avant d'écrire, d'auditer ou de coder. À utiliser avant toute rédaction, page, email, pub, audit SEO, schema ou code pour le projet, dès que l'utilisateur parle de son offre, de ses prix, de son ton, de sa charte ou de sa stack, et chaque fois qu'un autre skill dit « charge le contexte de marque », même si le mot contexte n'est pas prononcé.
---

# Contexte de marque — source unique

Un seul fichier décrit la marque. Les autres skills le lisent au moment de s'exécuter au lieu de recopier son contenu : quand l'offre change, on corrige un fichier et tout le reste suit.

## 1. Où il se trouve

Cherche dans cet ordre et arrête-toi au premier trouvé :

1. `./brand/brand-context.md`, puis `./brand-context.md` (dossier de travail) ;
2. le dossier donné par la variable d'environnement `VK_BRAND_DIR` ;
3. `/mnt/project/brand-context.md` (fichier d'un Project claude.ai).

```bash
for p in ./brand/brand-context.md ./brand-context.md "${VK_BRAND_DIR:-/nonexistent}/brand-context.md" /mnt/project/brand-context.md; do
  [ -f "$p" ] && { echo "$p"; break; }
done
```

`kit.config.json` vit dans le même dossier. Les skills lisent le Markdown ; les scripts lisent le JSON (`--config chemin/kit.config.json`).

**Introuvable** : ne l'invente pas. Propose de lancer le skill `setup`. Si l'utilisateur veut avancer tout de suite, pose au plus trois questions (offre, cible, ton), travaille avec les réponses et marque dans le livrable ce qui reste à confirmer.

## 2. Comment le lire

- Lis-le en entier une fois par conversation, puis reviens à la section utile.
- La date de fraîcheur en tête fait foi. Un prix, une offre ou un chiffre se revérifie sur la source de vérité du §2 avant publication.
- `[hypothèse]` : utilisable pour avancer, à signaler dans le livrable.
- `A_COMPLETER` : fait manquant. Le livrable qui en dépend garde le marqueur visible, il ne le remplace pas par une supposition.
- Le fichier et le site divergent : le site gagne. Signale l'écart et propose la correction du fichier.

## 3. Ce que chaque section commande

| Section | Skills qui s'en servent |
|---|---|
| 1 Qui · 2 Offre | tous |
| 3 Affirmations | copywriting, ad-creative, email-flows, seo-writer, social-publish, mascot-reels |
| 4 Clients | copywriting, cro, email-flows, ad-creative, seo-geo |
| 5 Ton · 6 Direction artistique | tout ce qui produit du texte ou du visuel |
| 7 Stack | shopify-liquid, site-clone, seo-schema, seo-audit, blog-pipeline |
| 8 Connecteurs | seo-data, seo-audit, blog-pipeline, social-publish, social-plan |
| 10 SEO | seo-*, blog-pipeline, directory-pages |
| 11 Réseaux | social-plan, social-publish, mascot-reels |
| 12 Conformité | ad-creative, ads-audit, social-publish, directory-pages |

## 4. Le mettre à jour

- Une correction de fait (prix, offre, outil) : modifie la ligne, mets à jour la date de fraîcheur, dis ce qui a changé.
- Une réponse de l'utilisateur à une question d'ICP, de ton ou de règle : propose de l'ajouter dans la section concernée, en une ligne.
- Une décision de l'utilisateur remplace une hypothèse : retire le marqueur `[hypothèse]`.
- Ne range jamais dans ce fichier une clé d'API, un mot de passe ou une donnée personnelle de client.

## 5. Gabarits

- `references/brand-context.template.md` : les douze sections, vides.
- `references/kit.config.template.json` : la configuration des scripts.

Des contextes remplis pour deux marques fictives (une boutique en ligne, un site vitrine) sont dans le dossier `examples/` du dépôt.
