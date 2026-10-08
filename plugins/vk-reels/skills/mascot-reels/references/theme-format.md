# Format du thème (JSON)

Un thème habille le moteur aux couleurs d'une marque sans toucher au code. Il se passe au rendu avec `--theme themes/<nom>.json`. Tout est facultatif : ce qui manque garde la valeur par défaut.

```json
{
  "palette": {"accent_marque": "#D9622B"},
  "roles": {"fond": "sable", "accent": "accent_marque", "texte": "encre", "papier": "creme", "sombre": "nuit", "ombre_bulle": "accent_marque"},
  "fonts": {
    "titre": {"file": "MaPolice.ttf", "url": "https://…/MaPolice.ttf"},
    "pix":   {"file": "PixelifySans.ttf", "variation": "SemiBold", "url": "https://…"}
  },
  "mascots": {
    "rond": {"base": "accent_marque", "shade": "corail_f", "light": "sable", "detail": "vert_f", "blush": "rose", "voice": 640}
  }
}
```

## `palette`

Ajoute des couleurs nommées ou redéfinit celles du moteur. Les icônes utilisent les noms de la palette d'illustration (`sable`, `corail`, `rouge`, `vert`, `bleu`, `rose`, `brun`, `creme`, `encre`, avec leurs variantes `_f` foncée et `_c` claire) : les redéfinir recolore les accessoires.

## `roles`

| Rôle | Utilisé pour |
|---|---|
| `fond` | fond d'une scène sans `tone` |
| `accent` | couleur d'appel dans les scénarios |
| `texte` | couleur de texte par défaut |
| `encre` | contours et texte des bulles (redéfinir ce nom dans `roles` ou `palette`) |
| `papier` | fond des bulles, reflets, fond du storyboard |
| `sombre` | étiquettes, devantures, second plan des collines |
| `ombre_bulle` | ombre portée des bulles |

## `fonts`

Deux familles : `titre` (titres) et `pix` (bulles et étiquettes). Pour chacune : `file` et `url` (téléchargée une fois dans `scripts/fonts/`), ou `path` vers un fichier local (relatif au dossier du skill, ou absolu). `variation` choisit une graisse dans une police variable.

Vérifie la licence de la police avant de l'utiliser. Les polices par défaut sont sous licence libre (SIL Open Font License).

## `mascots`

Pour chaque mascotte : `base`, `shade`, `light`, `detail`, `blush` (noms de palette ou codes hexadécimaux) et `voice` (hauteur des bips, en hertz : plus haut pour un personnage vif, plus bas pour un personnage posé).

## Vérifier un thème

Rends un scénario de `specs/` avec le thème et regarde `storyboard.png` : contraste des titres, lisibilité des bulles, accessoires qui ne se fondent pas dans le fond.
