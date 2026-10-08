#!/usr/bin/env python3
"""Moteur de vidéos verticales en pixel art.

Usage : python3 reel_engine.py specs/mon-reel.json dossier_sortie [--theme themes/demo.json] [--no-audio]

Produit : <filename>.mp4 (1080×1920, 30 i/s, son 8-bit), cover.jpg, storyboard.png, kf*.png
Le scénario (JSON) est décrit dans references/spec-format.md, le thème dans references/theme-format.md.
Dépendances : Pillow, numpy, ffmpeg.
"""
import argparse
import json
import math
import os
import random
import re
import subprocess
import sys
import urllib.request
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sprites import MASCOTS, NO_OUTLINE  # noqa: E402

W_, H_ = 1080, 1920
LS = 4                       # 1 pixel « basse déf » = 4 px réels
LW, LH = W_ // LS, H_ // LS  # 270 × 480
FPS = 30
CPS = 32                     # vitesse d'écriture des bulles (caractères par seconde)
HOLD = 1.8                   # temps de lecture après la fin d'une bulle (s)
SAFE_BOTTOM = 1560           # rien d'important sous cette ligne (interface des applications)
FONT_DIR = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------- thème
# Palette d'illustration par défaut. Un thème peut redéfinir n'importe quelle clé.
C = {"sable": "#F4D58D", "sable_c": "#FAE8B4", "sable_f": "#D9B25F", "corail": "#EE6C4D", "corail_f": "#C4512F",
     "rouge": "#C8553D", "rouge_f": "#9C3D29", "vert": "#2A9D8F", "vert_f": "#1F776C", "vert_c": "#57BFB2",
     "nuit": "#1D3557", "rose": "#F4ACB7", "rose_f": "#D98AA8", "brun": "#8D6E4C", "brun_f": "#6B5137",
     "brun_c": "#B7956F", "brun_p": "#463420", "creme": "#FFF8F0", "creme_f": "#E9DFD0", "bleu": "#457B9D",
     "bleu_f": "#2C5672", "encre": "#14213D", "pierre": "#EFE3CC", "pierre_f": "#E3D3B6", "vapeur": NO_OUTLINE,
     "ardoise": "#16302B", "ardoise_c": "#1F4039"}
# Rôles : ce que le moteur utilise quand le scénario ne précise pas de couleur.
ROLES = {"fond": "sable", "accent": "corail", "texte": "encre", "papier": "creme", "sombre": "nuit",
         "ombre_bulle": "corail"}
FONTS = {
    "titre": {"file": "TitanOne.ttf",
              "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/titanone/TitanOne-Regular.ttf"},
    "pix": {"file": "PixelifySans.ttf", "variation": "SemiBold",
            "url": "https://raw.githubusercontent.com/google/fonts/main/ofl/pixelifysans/PixelifySans%5Bwght%5D.ttf"},
}
MASCOT_COLORS = {
    "rond": {"base": "corail", "shade": "corail_f", "light": "sable", "detail": "vert_f", "blush": "rose", "voice": 640},
    "carre": {"base": "vert", "shade": "vert_f", "light": "vert_c", "detail": "sable", "blush": "rose", "voice": 430},
}
MUSIC = {  # tempo et accords (fondamentale, arpège) par univers
    "rayures": (112, [(130.81, [261.63, 329.63, 392.0]), (110.0, [220.0, 261.63, 329.63]), (87.31, [174.61, 220.0, 261.63]), (98.0, [196.0, 246.94, 293.66])]),
    "collines": (96, [(98.0, [196.0, 246.94, 293.66]), (130.81, [261.63, 329.63, 392.0]), (110.0, [220.0, 261.63, 329.63]), (130.81, [261.63, 329.63, 392.0])]),
    "tableau": (104, [(110.0, [220.0, 261.63, 329.63]), (87.31, [174.61, 220.0, 261.63]), (130.81, [261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66])]),
    "carte": (120, [(146.83, [293.66, 369.99, 440.0]), (123.47, [246.94, 293.66, 369.99]), (98.0, [196.0, 246.94, 293.66]), (110.0, [220.0, 277.18, 329.63])]),
}


def load_theme(path):
    """Applique un thème : palette, rôles, polices, couleurs et voix des mascottes."""
    if not path:
        return
    theme = json.load(open(path, encoding="utf-8"))
    C.update(theme.get("palette", {}))
    ROLES.update(theme.get("roles", {}))
    for kind, spec in theme.get("fonts", {}).items():
        FONTS[kind] = spec
    for name, spec in theme.get("mascots", {}).items():
        MASCOT_COLORS.setdefault(name, {}).update(spec)


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def col(name):
    """Résout un rôle, un nom de palette ou un code hexadécimal en RVB."""
    name = ROLES.get(name, name)
    return hx(C.get(name, name))


def fill(name):
    return col(name) + (255,)


# ---------------------------------------------------------------- polices
_fc = {}
_warned = set()
NOLIG = ["-liga"]  # la ligature « fi » de certaines polices pixel est illisible


def font_path(kind):
    spec = FONTS[kind]
    if spec.get("path"):
        p = spec["path"]
        return p if os.path.isabs(p) else os.path.join(ROOT, p)
    os.makedirs(FONT_DIR, exist_ok=True)
    p = os.path.join(FONT_DIR, spec["file"])
    if not os.path.exists(p) and spec.get("url"):
        try:
            urllib.request.urlretrieve(spec["url"], p)
        except Exception as exc:  # hors ligne : on continue avec la police intégrée
            if kind not in _warned:
                print(f"  ! police « {kind} » introuvable ({exc}) : police intégrée utilisée à la place")
                _warned.add(kind)
            return None
    return p if os.path.exists(p) else None


def font(kind, size):
    kind = kind if kind in FONTS else "titre"
    key = (kind, size)
    if key not in _fc:
        path = font_path(kind)
        if path:
            f = ImageFont.truetype(path, size)
            variation = FONTS[kind].get("variation")
            if variation:
                try:
                    f.set_variation_by_name(variation)
                except Exception:
                    pass
        else:
            f = ImageFont.load_default(size)
        _fc[key] = f
    return _fc[key]


_features_ok = {}


def text_kwargs(fnt):
    """Désactive les ligatures quand la police et le moteur de mise en forme le permettent."""
    key = id(fnt)
    if key not in _features_ok:
        try:
            fnt.getlength("fi", features=NOLIG)
            _features_ok[key] = True
        except Exception:
            _features_ok[key] = False
    return {"features": NOLIG} if _features_ok[key] else {}


# ---------------------------------------------------------------- utilitaires pixel
def outlined(im, color="encre"):
    """Ajoute un contour d'un pixel autour de tout pixel opaque."""
    w, h = im.size
    out = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    out.paste(im, (1, 1))
    p = out.load()
    add = []
    skip = hx(NO_OUTLINE)
    for y in range(h + 2):
        for x in range(w + 2):
            if p[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w + 2 and 0 <= yy < h + 2 and p[xx, yy][3] > 0 and p[xx, yy][:3] != skip:
                        add.append((x, y))
                        break
    for x, y in add:
        p[x, y] = fill(color)
    return out


def canvas(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


# ---------------------------------------------------------------- icônes (basse déf)
def ic_drop():
    im, d = canvas(16, 22)
    d.polygon([(8, 0), (14, 12), (2, 12)], fill=fill("bleu"))
    d.ellipse([2, 7, 14, 21], fill=fill("bleu"))
    d.point([(5, 12), (5, 13), (6, 11)], fill=fill("creme"))
    return outlined(im)


def ic_sun():
    im, d = canvas(28, 28)
    for a in range(0, 360, 45):
        x = 14 + 12 * math.cos(math.radians(a))
        y = 14 + 12 * math.sin(math.radians(a))
        d.line([14, 14, x, y], fill=fill("corail"), width=3)
    d.ellipse([6, 6, 21, 21], fill=fill("sable"))
    return outlined(im)


def ic_moon():
    im, d = canvas(20, 20)
    d.ellipse([0, 0, 19, 19], fill=fill("creme"))
    d.ellipse([6, -2, 23, 15], fill=(0, 0, 0, 0))
    return outlined(im)


def ic_star():
    im, d = canvas(22, 22)
    pts = []
    for i in range(10):
        r = 10.5 if i % 2 == 0 else 4.5
        a = math.radians(-90 + i * 36)
        pts.append((11 + r * math.cos(a), 11 + r * math.sin(a)))
    d.polygon(pts, fill=fill("sable"))
    return outlined(im)


def ic_heart():
    im, d = canvas(16, 14)
    d.ellipse([0, 0, 8, 8], fill=fill("rose"))
    d.ellipse([7, 0, 15, 8], fill=fill("rose"))
    d.polygon([(0, 5), (15, 5), (8, 13)], fill=fill("rose"))
    return outlined(im)


def ic_check():
    im, d = canvas(22, 18)
    d.line([2, 9, 8, 15], fill=fill("vert"), width=4)
    d.line([8, 15, 19, 3], fill=fill("vert"), width=4)
    return outlined(im)


def ic_leaf():
    im, d = canvas(22, 26)
    d.ellipse([2, 0, 19, 20], fill=fill("vert"))
    d.polygon([(2, 10), (11, 25), (19, 10)], fill=fill("vert"))
    d.line([11, 4, 11, 25], fill=fill("vert_f"))
    for y in (9, 14):
        d.line([11, y, 6, y - 3], fill=fill("vert_f"))
        d.line([11, y, 16, y - 3], fill=fill("vert_f"))
    return outlined(im)


def ic_doc():
    im, d = canvas(20, 26)
    d.rectangle([0, 0, 19, 25], fill=fill("creme"))
    d.polygon([(13, 0), (19, 6), (13, 6)], fill=fill("creme_f"))
    d.rectangle([3, 4, 10, 6], fill=fill("corail"))
    for y in range(10, 23, 3):
        d.line([3, y, 16, y], fill=fill("creme_f"))
    return outlined(im)


def ic_plane():
    im, d = canvas(30, 18)
    d.polygon([(0, 8), (29, 0), (12, 17)], fill=fill("corail"))
    d.polygon([(12, 17), (29, 0), (15, 10)], fill=fill("corail_f"))
    return outlined(im)


def ic_box():
    im, d = canvas(24, 22)
    d.rectangle([1, 6, 22, 21], fill=fill("brun_c"))
    d.rectangle([0, 1, 23, 6], fill=fill("brun"))
    d.rectangle([10, 1, 13, 21], fill=fill("sable"))
    return outlined(im)


def ic_trophy():
    im, d = canvas(22, 26)
    d.rectangle([4, 0, 17, 10], fill=fill("sable"))
    d.ellipse([4, 4, 17, 16], fill=fill("sable"))
    d.arc([0, 1, 7, 9], 90, 270, fill=fill("sable"), width=2)
    d.arc([14, 1, 21, 9], 270, 90, fill=fill("sable"), width=2)
    d.line([6, 2, 6, 9], fill=fill("sable_c"), width=2)
    d.rectangle([9, 16, 12, 20], fill=fill("sable_f"))
    d.rectangle([5, 20, 16, 25], fill=fill("brun"))
    return outlined(im)


def ic_cup():
    im, d = canvas(20, 18)
    for x in (4, 8, 12):
        d.point([(x, 0), (x + 1, 1), (x, 2)], fill=fill("vapeur"))
    d.rectangle([1, 5, 14, 13], fill=fill("creme"))
    d.ellipse([12, 6, 18, 12], outline=fill("creme"), width=2)
    d.rectangle([0, 15, 18, 16], fill=fill("sable"))
    d.rectangle([3, 13, 12, 14], fill=fill("creme_f"))
    return outlined(im)


def ic_basket():
    im, d = canvas(30, 22)
    for i, x in enumerate(range(4, 26, 5)):
        d.ellipse([x, 0, x + 6, 6], fill=fill("rouge" if i % 2 else "corail"))
    d.polygon([(0, 5), (29, 5), (25, 21), (4, 21)], fill=fill("brun"))
    for y in (9, 13, 17):
        d.line([2, y, 27, y], fill=fill("brun_f"))
    for x in range(6, 26, 5):
        d.line([x, 6, x, 20], fill=fill("brun_c"))
    return outlined(im)


def ic_mountain():
    im, d = canvas(96, 52)
    d.polygon([(0, 51), (30, 8), (62, 51)], fill=fill("vert_f"))
    d.polygon([(30, 51), (62, 0), (95, 51)], fill=fill("brun_f"))
    d.polygon([(55, 11), (62, 0), (69, 11), (65, 9), (62, 12), (58, 9)], fill=fill("creme"))
    d.polygon([(25, 15), (30, 8), (35, 15), (30, 13)], fill=fill("creme"))
    d.line([(62, 0), (95, 51)], fill=fill("brun_p"))
    return outlined(im)


def ic_shop():
    """Devanture 220×190. Son enseigne se remplit avec un texte « pix » de 44 px vers y ≈ 1050."""
    w, h = 220, 190
    im, d = canvas(w, h)
    d.rectangle([0, 0, w - 1, h - 1], fill=fill("pierre"))
    for y in range(8, h - 80, 6):
        d.line([0, y, w, y], fill=fill("pierre_f"))
    for row in range(2):
        for i in range(5):
            x = 10 + i * 42
            y = 10 + row * 46
            d.rectangle([x, y, x + 26, y + 34], fill=fill("bleu"), outline=fill("encre"))
            d.line([x + 13, y, x + 13, y + 34], fill=fill("encre"))
            d.line([x, y + 14, x + 26, y + 14], fill=fill("encre"))
            d.rectangle([x - 3, y + 34, x + 29, y + 37], fill=fill("encre"))
    d.rectangle([0, 100, w - 1, 106], fill=fill("pierre_f"), outline=fill("encre"))
    d.rectangle([4, 108, w - 5, h - 1], fill=fill("sombre"), outline=fill("encre"))
    d.rectangle([12, 112, w - 13, 126], fill=fill("encre"))
    for x0 in (12, 150):
        d.rectangle([x0, 132, x0 + 58, h - 8], fill=fill("sable"), outline=fill("encre"))
        d.rectangle([x0 + 3, 160, x0 + 55, h - 10], fill=fill("sable_c"))
    d.rectangle([82, 132, 138, h - 1], fill=fill("vert"), outline=fill("encre"))
    d.rectangle([88, 138, 132, 176], fill=fill("sable_c"), outline=fill("encre"))
    d.rectangle([0, 0, w - 1, h - 1], outline=fill("encre"))
    return im


ICONS = {"drop": ic_drop, "sun": ic_sun, "moon": ic_moon, "star": ic_star, "heart": ic_heart, "check": ic_check,
         "leaf": ic_leaf, "doc": ic_doc, "plane": ic_plane, "box": ic_box, "trophy": ic_trophy, "cup": ic_cup,
         "basket": ic_basket, "mountain": ic_mountain, "shop": ic_shop}
_ic = {}


def icon(name):
    if name not in ICONS:
        raise SystemExit(f"Icône inconnue : {name}. Disponibles : {', '.join(sorted(ICONS))}")
    if name not in _ic:
        _ic[name] = ICONS[name]()
    return _ic[name]


def stamp(w, h, color="sable"):
    """Timbre dentelé."""
    im, d = canvas(w, h)
    d.rectangle([0, 0, w - 1, h - 1], fill=fill("creme"))
    for x in range(0, w, 4):
        d.rectangle([x, 0, x + 1, 1], fill=(0, 0, 0, 0))
        d.rectangle([x, h - 2, x + 1, h - 1], fill=(0, 0, 0, 0))
    for y in range(0, h, 4):
        d.rectangle([0, y, 1, y + 1], fill=(0, 0, 0, 0))
        d.rectangle([w - 2, y, w - 1, y + 1], fill=(0, 0, 0, 0))
    d.rectangle([4, 4, w - 5, h - 5], fill=fill(color), outline=fill("encre"))
    return im


# ---------------------------------------------------------------- univers (fonds basse déf)
def bg(universe, tone, f):
    base = col(tone) if tone else col("fond")
    im = Image.new("RGB", (LW, LH), base)
    d = ImageDraw.Draw(im)
    if universe == "rayures":
        dark = tuple(max(0, v - 10) for v in base)
        off = int(f * 0.5) % 24
        for k in range(-LH, LW + LH, 24):
            x = k + off
            d.polygon([(x, 0), (x + 10, 0), (x + 10 - LH, LH), (x - LH, LH)], fill=dark)
    elif universe == "collines":
        cy = 30 + int(2 * math.sin(f / 40))
        d.ellipse([228, cy - 18, 264, cy + 18], fill=col("sable_c"))
        for (y0, amp, name, ph) in ((300, 14, "vert_c", 0), (340, 12, "vert", 1.7), (390, 10, "vert_f", 3.1)):
            pts = [(x, y0 + amp * math.sin(x / 38 + ph)) for x in range(0, LW + 1, 3)] + [(LW, LH), (0, LH)]
            d.polygon(pts, fill=col(name))
        for row, (y0, name) in enumerate(((318, "vert_f"), (358, "sombre"))):
            for x in range(8 + row * 11, LW, 22):
                y = y0 + int((12 if row == 0 else 10) * math.sin(x / 38 + (0 if row == 0 else 1.7)))
                d.ellipse([x - 5, y - 9, x + 5, y + 2], fill=col(name))
    elif universe == "tableau":
        im.paste(col("brun"), [0, 0, LW, LH])
        d.rectangle([6, 6, LW - 7, LH - 7], fill=col("ardoise"))
        for x in range(6, LW - 6, 18):
            d.line([x, 6, x, LH - 7], fill=col("ardoise_c"))
        for y in range(6, LH - 6, 18):
            d.line([6, y, LW - 7, y], fill=col("ardoise_c"))
        d.rectangle([0, LH - 14, LW, LH], fill=col("brun_f"))
        for x in (40, 60, 200):
            d.rectangle([x, LH - 18, x + 12, LH - 15], fill=col("creme"))
    elif universe == "carte":
        blob = tuple(max(0, v - 14) for v in base)
        for (x, y, rx, ry) in ((40, 90, 50, 26), (200, 150, 60, 30), (70, 300, 70, 34), (230, 390, 50, 24)):
            d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=blob)
        off = (f // 3) % 8
        for i in range(0, 60):
            t = i / 60
            x = 20 + t * 230
            y = 440 - t * 380 + 60 * math.sin(t * math.pi)
            if (i + off) % 4 < 2:
                d.rectangle([x, y, x + 1, y + 1], fill=col("creme"))
        for (x, y) in ((30 + (f // 2) % 300 - 20, 60), (180 - (f // 3) % 260 + 60, 250)):
            d.ellipse([x, y, x + 24, y + 10], fill=col("creme"))
            d.ellipse([x + 8, y - 5, x + 20, y + 6], fill=col("creme"))
    else:
        raise SystemExit(f"Univers inconnu : {universe}. Disponibles : rayures, collines, tableau, carte")
    return im


# ---------------------------------------------------------------- mascottes
_sc = {}


def mascot_img(name, expr, talk, blink, t, wave):
    if name not in MASCOTS:
        raise SystemExit(f"Mascotte inconnue : {name}. Disponibles : {', '.join(sorted(MASCOTS))}")
    key = (name, expr, talk, blink, wave)
    if key not in _sc:
        spec = MASCOT_COLORS.get(name, MASCOT_COLORS["rond"])
        colors = {k: "#%02X%02X%02X" % col(v) for k, v in spec.items() if isinstance(v, str)}
        grid = MASCOTS[name](colors, expr=expr, talk=talk, blink=blink, t=t, wave=wave,
                             ink="#%02X%02X%02X" % col("encre"), paper="#%02X%02X%02X" % col("papier"))
        im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        p = im.load()
        for y in range(32):
            for x in range(32):
                if grid[y][x]:
                    p[x, y] = hx(grid[y][x]) + (255,)
        _sc[key] = im
    return _sc[key]


# ---------------------------------------------------------------- texte haute déf
def nbsp(text):
    """Espaces insécables à la française : pas de « ! » ni d'unité orphelins en début de ligne."""
    nb = " "
    text = re.sub(r" ([!?:;»%])", lambda m: nb + m.group(1), text)
    text = text.replace("« ", "«" + nb)
    text = re.sub(r"(\d) (\d{3})", lambda m: m.group(1) + nb + m.group(2), text)
    text = re.sub(r"(\d) (m|g|kg|°C|min|s|h|€)\b", lambda m: m.group(1) + nb + m.group(2), text)
    return text


def wrap(d, text, fnt, maxw):
    text = nbsp(text)
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt, **text_kwargs(fnt)) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


BUBBLE_FONT = 62
BUBBLE_LH = 82


def draw_bubble(d, text, shown, y, tail_x, shadow):
    fnt = font("pix", BUBBLE_FONT)
    x0, x1 = 70, 1010
    lines = wrap(d, text, fnt, x1 - x0 - 96)
    h = len(lines) * BUBBLE_LH + 72
    ink, paper = col("encre"), col("papier")
    d.rectangle([x0 + 14, y + 14, x1 + 14, y + h + 14], fill=col(shadow))
    d.rectangle([x0, y, x1, y + h], fill=paper, outline=ink, width=8)
    for i in range(4):
        wd = 8 * (3 - i)
        yt = y - 8 * (i + 1)
        d.rectangle([tail_x - wd - 8, yt, tail_x + wd + 8, yt + 8], fill=ink)
        if wd > 0:
            d.rectangle([tail_x - wd, yt, tail_x + wd, yt + 8], fill=paper)
    d.rectangle([tail_x - 24, y, tail_x + 24, y + 8], fill=paper)
    n = shown
    for i, line in enumerate(lines):
        seg = line[:max(0, n)]
        n -= len(line) + 1
        d.text((x0 + 48, y + 34 + i * BUBBLE_LH), seg, font=fnt, fill=ink, **text_kwargs(fnt))
    return h


def draw_text(d, it):
    fnt = font(it.get("font", "titre"), it["size"])
    kw = text_kwargs(fnt)
    color = col(it.get("color", "texte"))
    tw = d.textlength(it["t"], font=fnt, **kw)
    x = it.get("x", "c")
    if "cx" in it:
        x = it["cx"] - tw / 2
    elif x == "c":
        x = (W_ - tw) / 2
    y = it["y"]
    if "bg" in it:
        pad = it.get("pad", 20)
        if it.get("shadow"):
            d.rectangle([x - pad + 10, y - pad * 0.6 + 10, x + tw + pad + 10, y + it["size"] + pad * 0.9 + 10],
                        fill=col(it["shadow"]))
        d.rectangle([x - pad, y - pad * 0.6, x + tw + pad, y + it["size"] + pad * 0.9], fill=col(it["bg"]),
                    outline=col("encre") if it.get("border") else None, width=6 if it.get("border") else 0)
    st = it.get("stroke")
    d.text((x, y), it["t"], font=fnt, fill=color, stroke_width=it.get("stroke_w", 6) if st else 0,
           stroke_fill=col(st) if st else None, **kw)


# ---------------------------------------------------------------- scène
def scene_duration(sc):
    if "dur" in sc:
        return sc["dur"]
    bubbles = sc.get("bubbles", [])
    if not bubbles:
        return 3.5
    return round(sum(0.3 + len(t) / CPS + HOLD for t in bubbles) + 0.2, 2)


def bubble_state(sc, t):
    """(index de bulle, caractères affichés, en train de parler)"""
    acc = 0.0
    bubbles = sc.get("bubbles", [])
    for i, txt in enumerate(bubbles):
        seg = 0.3 + len(txt) / CPS + HOLD
        if t < acc + seg or i == len(bubbles) - 1:
            shown = int(max(0, t - acc - 0.3) * CPS)
            return i, min(shown, len(txt)), shown < len(txt)
        acc += seg
    return None, 0, False


def mascot_x(m):
    s = m.get("scale", 3)
    x = m.get("x", "c")
    return (LW - 32 * s) // 2 if x == "c" else x


def render(sc, f, gf, is_first, warnings):
    t = f / FPS
    low = bg(sc.get("universe", "rayures"), sc.get("tone"), gf).convert("RGBA")
    bi, shown, talking = bubble_state(sc, t)
    for p in sc.get("props", []):
        im = stamp(p["w"], p["h"], p.get("color", "sable")) if p.get("type") == "stamp" else icon(p["icon"])
        s = p.get("scale", 1)
        if s != 1:
            im = im.resize((im.width * s, im.height * s), Image.NEAREST)
        bob = int(round(p.get("bob", 0) * math.sin(t * 5 + p.get("phase", 0))))
        x = p["x"] if p["x"] != "c" else (LW - im.width) // 2
        low.alpha_composite(im, (int(x), int(p["y"] + bob)))
    m = sc.get("mascot")
    if m:
        s = m.get("scale", 3)
        blink = (not talking) and (f % 90) in (60, 61, 62)
        wave_now = m.get("wave", False) and (f // 8) % 2 == 0
        expr = m.get("expr", "normal")
        if m.get("expr_after") and not talking and bi == len(sc.get("bubbles", [])) - 1:
            expr = m["expr_after"]
        im = mascot_img(m["name"], expr, talking and (f // 3) % 2 == 0, blink, t, wave_now)
        im = im.resize((32 * s, 32 * s), Image.NEAREST)
        y = m["y"] + int(round(2 * math.sin(t * 5)))
        if is_first and t < 0.5:
            y += int((1 - t / 0.5) ** 2 * 260)
        low.alpha_composite(im, (int(mascot_x(m)), int(y)))
    hi = low.convert("RGB").resize((W_, H_), Image.NEAREST)
    d = ImageDraw.Draw(hi)
    for it in sc.get("texts", []):
        draw_text(d, it)
    if bi is not None and m:
        txt = sc["bubbles"][bi]
        s = m.get("scale", 3)
        by = sc.get("bubble_y") or (m["y"] + 32 * s) * LS + 70
        tail = sc.get("bubble_tail") or (mascot_x(m) + 16 * s) * LS
        h = draw_bubble(d, txt, shown, by, tail, sc.get("bubble_shadow", "ombre_bulle"))
        if by + h > SAFE_BOTTOM and f == 0:
            warnings.append(f"bulle sous la zone sûre ({by + h} px > {SAFE_BOTTOM}) : « {txt[:40]}… »")
    return hi, bi, shown


# ---------------------------------------------------------------- audio
def make_audio(path, total, blips, transitions, universe, voice):
    sr = 44100
    a = np.zeros(int(sr * (total + 6)))

    def note(freq, start, dur, amp, kind="sq"):
        n = int(dur * sr)
        tt = np.arange(n) / sr
        w = np.sign(np.sin(2 * np.pi * freq * tt)) if kind == "sq" else 2 * np.abs(2 * ((freq * tt) % 1) - 1) - 1
        env = np.minimum(1, np.linspace(1, 0, n) * 3) * np.minimum(1, tt * 200)
        s = int(start * sr)
        a[s:s + n] += w * env * amp

    bpm, chords = MUSIC.get(universe, MUSIC["rayures"])
    beat = 60 / bpm
    tt = 0
    bar = 0
    while tt < total:
        root, arp = chords[bar % 4]
        for b in range(4):
            note(root, tt + b * beat, beat * 0.9, 0.05, "sq")
            for e in range(2):
                note(arp[(b * 2 + e) % 3] * 2, tt + b * beat + e * beat / 2, beat / 2 * 0.8, 0.035, "tri")
        tt += 4 * beat
        bar += 1
    rng = np.random.default_rng(1)
    for bt in blips:
        note(voice + rng.integers(-50, 50), bt, 0.04, 0.09, "sq")
    for tr in transitions:
        n = int(0.18 * sr)
        s = int(tr * sr)
        a[s:s + n] += rng.uniform(-1, 1, n) * np.linspace(0.08, 0, n)
    fade = int(1.2 * sr)
    a[int(total * sr) - fade:int(total * sr)] *= np.linspace(1, 0, fade)
    a = np.clip(a[:int(total * sr)], -1, 1)
    with wave.open(path, "wb") as wv:
        wv.setnchannels(1)
        wv.setsampwidth(2)
        wv.setframerate(sr)
        wv.writeframes((a * 32767 * 0.9).astype(np.int16).tobytes())


# ---------------------------------------------------------------- rendu complet
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("sortie")
    ap.add_argument("--theme", default=os.path.join(ROOT, "themes", "demo.json"))
    ap.add_argument("--no-audio", action="store_true", help="vidéo muette (utile pour un test rapide)")
    a = ap.parse_args()

    load_theme(a.theme if os.path.exists(a.theme) else None)
    spec = json.load(open(a.spec, encoding="utf-8"))
    os.makedirs(a.sortie, exist_ok=True)
    scenes = spec["scenes"]
    voice = MASCOT_COLORS.get(spec.get("mascot", "rond"), {}).get("voice", 560)
    vid = os.path.join(a.sortie, "video.mp4")
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W_}x{H_}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                             "-crf", "18", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    random.seed(4)
    blocks = [(x, y) for x in range(0, W_, 60) for y in range(0, H_, 60)]
    gf = 0
    prev = None
    keyframes, blips, transitions, warnings = [], [], [], []
    cover = None
    for si, sc in enumerate(scenes):
        n = int(scene_duration(sc) * FPS)
        order = blocks[:]
        random.shuffle(order)
        if si:
            transitions.append(gf / FPS)
        last = {}
        hi = None
        for f in range(n):
            hi, bi, shown = render(sc, f, gf, si == 0, warnings)
            if bi is not None:
                txt = sc["bubbles"][bi]
                for c in range(last.get(bi, 0), shown):
                    if txt[c] not in " ,.!?'’…:;«»" and c % 2 == 0:
                        blips.append(gf / FPS)
                last[bi] = shown
                if si == 0 and bi == 0 and shown == len(txt) and cover is None:
                    cover = hi.copy()
            if prev is not None and f < 8:  # transition en mosaïque
                k = int(len(order) * (f + 1) / 8)
                out_im = prev.copy()
                for (x, y) in order[:k]:
                    out_im.paste(hi.crop((x, y, x + 60, y + 60)), (x, y))
            else:
                out_im = hi
            if f == n - int(0.6 * FPS):
                keyframes.append(out_im.copy())
            proc.stdin.write(out_im.tobytes())
            gf += 1
        prev = hi
    proc.stdin.close()
    proc.wait()
    total = gf / FPS
    final = os.path.join(a.sortie, spec.get("filename", "reel") + ".mp4")
    if a.no_audio:
        os.replace(vid, final)
    else:
        wav = os.path.join(a.sortie, "audio.wav")
        make_audio(wav, total, blips, transitions, scenes[0].get("universe", "rayures"), voice)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac",
                        "-b:a", "160k", "-shortest", final], check=True)
        os.remove(vid)
        os.remove(wav)
    (cover or keyframes[0]).save(os.path.join(a.sortie, "cover.jpg"), quality=92)
    cw, ch = 270, 480
    sheet = Image.new("RGB", (cw * len(keyframes) + 20 * (len(keyframes) + 1), ch + 40), col("papier"))
    for i, k in enumerate(keyframes):
        sheet.paste(k.resize((cw, ch), Image.LANCZOS), (20 + i * (cw + 20), 20))
    sheet.save(os.path.join(a.sortie, "storyboard.png"))
    for i, k in enumerate(keyframes):
        k.resize((540, 960), Image.LANCZOS).save(os.path.join(a.sortie, f"kf{i}.png"))
    for w in dict.fromkeys(warnings):
        print("  !", w)
    print(f"OK {final} · {total:.1f} s · {len(scenes)} scènes")


if __name__ == "__main__":
    main()
