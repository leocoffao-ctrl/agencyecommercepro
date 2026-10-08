# Format du scénario (JSON)

Coordonnées : `x` et `y` des mascottes et des accessoires en **basse définition** (270 × 480, 1 px = 4 px réels) ; `x`, `y` et `cx` des textes en **haute définition** (1080 × 1920).

```json
{
  "mascot": "rond",
  "filename": "mon-reel",
  "scenes": [ { "…": "une scène" } ]
}
```

`mascot` fixe la voix des bips ; `filename` le nom du MP4.

## Scène

| Clé | Rôle |
|---|---|
| `universe` | `rayures` · `collines` · `tableau` · `carte` (la musique suit l'univers de la première scène) |
| `tone` | couleur de fond : rôle du thème, nom de palette ou code hexadécimal. Par défaut, le rôle `fond` |
| `dur` | durée forcée en secondes ; sinon calculée depuis les bulles (0,3 s + texte à 32 caractères par seconde + 1,8 s de lecture) |
| `mascot` | `{name, expr, scale (2 ou 3), x ('c' par défaut), y, wave, expr_after}` ; `expr_after` = expression après la dernière bulle |
| `bubbles` | liste de phrases, écrites l'une après l'autre sous la mascotte (80 caractères au plus chacune) |
| `bubble_shadow` | couleur de l'ombre de la bulle (par défaut, le rôle `ombre_bulle`) |
| `props` | accessoires : `{icon, scale, x ('c' possible), y, bob, phase}`, ou timbre `{type: "stamp", w, h, x, y, color}` |
| `texts` | `{t, font: "titre" ou "pix", size, y, x ou cx ou centré, color, bg, border, shadow, stroke}` |

Expressions : `normal`, `joie`, `surpris`, `clin`. La bouche qui parle et le clignement sont gérés par le moteur.

Icônes : `drop`, `sun`, `moon`, `star`, `heart`, `check`, `leaf`, `doc`, `plane`, `box`, `trophy`, `cup`, `basket`, `mountain` (96 × 52), `shop` (devanture 220 × 190, à placer en `x: "c", y: 150` ; son enseigne se remplit avec un texte `pix` de 44 px vers y ≈ 1050).

## Repères de placement

- Mascotte en `scale 3` : 96 px de côté en basse définition.
- La bulle se place à `(y + 96) × 4 + 70` px réels. Pour trois lignes, garder `y ≤ 195`.
- Titres : zone y 190 à 640 (réels). Mascotte : y 165 à 195 (basse définition).
- Rien d'important sous 1560 px réels.

## Couleurs

Une couleur s'écrit de trois façons, résolues dans cet ordre : un **rôle** du thème (`fond`, `accent`, `texte`, `papier`, `sombre`, `ombre_bulle`), un **nom de palette** (`sable`, `corail`, `vert`, `nuit`, `rose`, `creme`, `encre`…), ou un **code hexadécimal**. Préfère les rôles : le même scénario se rend alors dans n'importe quel thème.

Exemples complets : `specs/demo-rond-trois-idees.json`, `specs/demo-carre-colis.json`.
