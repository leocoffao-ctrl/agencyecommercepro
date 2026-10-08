# Skills de design recommandés (non redistribués)

Le plugin `vk-design` ne contient que `site-clone`. Pendant la construction du kit, trois skills de design écrits par d'autres ont servi à juger et à améliorer les maquettes. Ils ne sont pas copiés ici : ils appartiennent à leurs auteurs, évoluent de leur côté, et s'installent depuis leur dépôt.

| Skill | Ce qu'il apporte | Auteur et dépôt | Licence |
|---|---|---|---|
| `design-taste-frontend` | Direction artistique pour pages d'atterrissage et portfolios, liste de contrôle avant livraison | Leonxlnx — [taste-skill](https://github.com/Leonxlnx/taste-skill) | MIT |
| `redesign-existing-projects` | Audit d'une interface existante puis remise à niveau sans casser le fonctionnel | Leonxlnx — [taste-skill](https://github.com/Leonxlnx/taste-skill) (skill `redesign-skill`) | MIT |
| Synthèse « design & taste » | Typographie, couleur, mouvement, états des composants, anti-clichés | Synthèse de [emilkowalski/skill](https://github.com/emilkowalski/skill) (MIT), [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) et taste-skill (MIT) ; mode défilement dérivé de [nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft) (MIT) | MIT et Apache-2.0 |

## Comment les brancher au kit

1. Installe le skill voulu depuis son dépôt, en suivant ses instructions.
2. Dans le contexte de marque, section 6, note les directions à ne jamais proposer : ces skills ont des goûts marqués, le contexte reste prioritaire.
3. Enchaînement conseillé : `site-clone` pour la structure → un skill de design pour la finition → `copywriting` pour les textes → `shopify-liquid` ou l'adaptateur de ta plateforme pour l'intégration.

Si tu préfères un dépôt autonome, ces licences autorisent la redistribution à condition de conserver les avis de droit d'auteur et, pour la partie Apache-2.0, le fichier `NOTICE`. Range-les alors dans un dossier `third_party/` clairement séparé, sans en changer l'attribution.
