"""Sprites des mascottes, dessinés sur une grille 32×32.

Chaque mascotte est une fonction qui reçoit ses couleurs (base, ombre, lumière, détail) et
son état (expression, bouche qui parle, clignement, geste) et renvoie la grille de pixels.

Les deux mascottes livrées, « rond » et « carre », sont des personnages de démonstration.
Pour ajouter la tienne : écris une fonction sur le même modèle, ajoute-la à MASCOTS, et
déclare ses couleurs et sa voix dans le thème (themes/*.json).
"""
N = 32
INK = "#14213D"     # contour et yeux, remplacé par le rôle « encre » du thème
PAPER = "#FFF8F0"   # reflets, remplacé par le rôle « papier » du thème
NO_OUTLINE = "#E8DCC9"  # couleur jamais cernée (vapeur, fumée)


class Spr:
    """Grille de pixels et primitives de dessin."""

    def __init__(self, ink=INK, paper=PAPER):
        self.g = [[None] * N for _ in range(N)]
        self.ink, self.paper = ink, paper

    def px(self, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            self.g[y][x] = c

    def ell(self, cx, cy, rx, ry, base, shade=None, light=None):
        """Ellipse pleine, avec ombre en bas à droite et lumière en haut à gauche."""
        for y in range(N):
            for x in range(N):
                nx = (x + 0.5 - cx) / rx
                ny = (y + 0.5 - cy) / ry
                d = nx * nx + ny * ny
                if d <= 1:
                    c = base
                    if shade and nx * 0.55 + ny * 0.83 > 0.5 and d > 0.45:
                        c = shade
                    if light and (-nx * 0.6 - ny * 0.8) > 0.45 and 0.35 < d < 0.8:
                        c = light
                    self.g[y][x] = c

    def rect(self, x0, y0, x1, y1, base, shade=None, light=None):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = base
                if shade and (x >= x1 - 1 or y >= y1 - 1):
                    c = shade
                if light and (x == x0 + 1 and y0 + 1 < y < y0 + 4):
                    c = light
                self.px(x, y, c)

    def outline(self):
        """Cerne d'un pixel tout ce qui est dessiné."""
        add = []
        for y in range(N):
            for x in range(N):
                if self.g[y][x] is None:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < N and 0 <= yy < N and self.g[yy][xx] not in (None, self.ink, NO_OUTLINE):
                            add.append((x, y))
                            break
        for x, y in add:
            self.g[y][x] = self.ink

    # ------------------------------------------------------------ visage
    def eye(self, x, y, kind):
        k, w = self.ink, self.paper
        if kind == "open":
            for yy in range(3):
                self.px(x, y + yy, k)
                self.px(x + 1, y + yy, k)
            self.px(x, y, w)
        elif kind == "closed":
            for dx in (-1, 0, 1, 2):
                self.px(x + dx, y + 2, k)
        elif kind == "happy":
            self.px(x - 1, y + 2, k)
            self.px(x, y + 1, k)
            self.px(x + 1, y + 1, k)
            self.px(x + 2, y + 2, k)
        elif kind == "big":
            for yy in range(4):
                for xx in range(3):
                    self.px(x - 1 + xx, y - 1 + yy, k)
            self.px(x - 1, y - 1, w)
            self.px(x, y - 1, w)

    def mouth(self, mx, my, kind, inner="#8C1F10", tongue="#F4ACB7"):
        k = self.ink
        if kind == "smile":
            self.px(mx - 2, my, k)
            self.px(mx + 2, my, k)
            for d in (-1, 0, 1):
                self.px(mx + d, my + 1, k)
        elif kind == "open":
            for d in range(-2, 3):
                self.px(mx + d, my, k)
            self.px(mx - 2, my + 1, k)
            self.px(mx + 2, my + 1, k)
            for d in (-1, 0, 1):
                self.px(mx + d, my + 1, inner)
            self.px(mx, my + 1, tongue)
            for d in (-1, 0, 1):
                self.px(mx + d, my + 2, k)
        elif kind == "o":
            for d in (-1, 0, 1):
                self.px(mx + d, my, k)
                self.px(mx + d, my + 2, k)
            self.px(mx - 1, my + 1, k)
            self.px(mx + 1, my + 1, k)
            self.px(mx, my + 1, inner)

    def face(self, ex1, ex2, ey, mx, my, expr, talk=False, blink=False, blush=None, brow=None):
        """Expressions : normal, joie, surpris, clin."""
        e1 = e2 = "open"
        m = "smile"
        if expr == "joie":
            e1 = e2 = "happy"
            m = "open"
        if expr == "surpris":
            e1 = e2 = "big"
            m = "o"
        if expr == "clin":
            e2 = "closed"
        if blink and expr in ("normal", "surpris"):
            e1 = e2 = "closed"
        if talk and m != "o":
            m = "open"
        self.eye(ex1, ey, e1)
        self.eye(ex2, ey, e2)
        if blush:
            for x in (ex1 - 3, ex1 - 2, ex2 + 3, ex2 + 4):
                self.px(x, ey + 4, blush)
        if expr == "surpris" and brow:
            for x in (ex1 - 1, ex1, ex1 + 1, ex2 - 1, ex2, ex2 + 1):
                self.px(x, ey - 3, brow)
        self.mouth(mx, my, m)


def rond(col, expr="normal", talk=False, blink=False, t=0, wave=False, ink=INK, paper=PAPER):
    """Personnage rond, avec deux petites oreilles et deux pieds."""
    s = Spr(ink, paper)
    s.ell(8.5, 9.5, 3.2, 3.2, col["base"], col["shade"])
    s.ell(23.5, 9.5, 3.2, 3.2, col["base"], col["shade"])
    s.ell(8.5, 9.8, 1.4, 1.4, col["detail"])
    s.ell(23.5, 9.8, 1.4, 1.4, col["detail"])
    s.ell(16, 19.5, 11.5, 10.5, col["base"], col["shade"], col["light"])
    s.ell(12, 30.3, 2.6, 1.6, col["shade"])
    s.ell(20, 30.3, 2.6, 1.6, col["shade"])
    if wave:
        s.px(27, 15, col["base"])
        s.px(28, 14, col["base"])
        s.px(28, 13, col["base"])
    s.outline()
    s.px(9, 13, paper)
    s.px(10, 13, paper)
    s.px(9, 14, paper)
    s.face(11, 19, 17, 16, 21, expr, talk, blink, col.get("blush"), col["detail"])
    return s.g


def carre(col, expr="normal", talk=False, blink=False, t=0, wave=False, ink=INK, paper=PAPER):
    """Personnage carré, avec un bandeau, des bras et des jambes."""
    s = Spr(ink, paper)
    s.rect(6, 9, 25, 26, col["base"], col["shade"], col["light"])
    s.rect(6, 9, 25, 11, col["detail"])
    for y in (27, 28):
        s.px(11, y, col["shade"])
        s.px(20, y, col["shade"])
    s.rect(9, 29, 12, 30, col["shade"])
    s.rect(19, 29, 22, 30, col["shade"])
    s.px(4, 17, col["base"])
    s.px(3, 18, col["base"])
    s.px(3, 19, col["base"])
    if wave:
        s.px(27, 15, col["base"])
        s.px(28, 14, col["base"])
        s.px(28, 13, col["base"])
    else:
        s.px(27, 17, col["base"])
        s.px(28, 18, col["base"])
        s.px(28, 19, col["base"])
    s.outline()
    s.face(10, 19, 15, 15, 20, expr, talk, blink, col.get("blush"), ink)
    return s.g


MASCOTS = {"rond": rond, "carre": carre}
