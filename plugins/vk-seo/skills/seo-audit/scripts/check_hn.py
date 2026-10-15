#!/usr/bin/env python3
"""Plan des titres Hn d'une page, et titres parasites injectés par le gabarit.

  python3 check_hn.py page.html                       # fichier local
  python3 check_hn.py https://exemple.fr/ https://exemple.fr/pages/offre
  python3 check_hn.py https://exemple.fr/ --cart-variant 123456789   # Shopify : refait la page panier plein
  python3 check_hn.py page.html --json                # sortie machine

Le gabarit d'une boutique (tiroir panier, liste de souhaits, notification d'ajout,
pop-up de remise, blocage par pays, bandeau cookies) pose souvent des <h1>/<h2>/<h3>
sur toutes les pages. Ils cassent la hiérarchie et ajoutent un second H1. Plusieurs
n'apparaissent qu'avec un article dans le panier : d'où --cart-variant, qui ajoute
un article par /cart/add.js puis recharge la page avec le même cookie.

Bloquants (code de sortie 1) : zéro ou plusieurs H1, H1 de gabarit, H1 qui n'est pas
le premier titre de la page.
Avertissements : titre de gabarit (H2 à H6), titre vide, emoji dans un titre, niveau
sauté (H2 puis H4), titre identique répété, chaîne d'interface en anglais.
"""
import argparse
import http.cookiejar
import json
import re
import sys
import time
import unicodedata
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; kit-seo-check-hn/1.0)"

# Lexique de l'interface de boutique, FR et EN. Un titre qui ne contient que ça
# n'est pas du contenu : il vient du gabarit.
CHROME = [
    r"\b(votre |mon |ton )?panier\b", r"\bpanier est vide\b", r"\bajout[ée]e? (au|à votre) panier\b",
    r"\btotal (estim[ée]|provisoire)\b", r"\bsous-total\b",
    r"\bvous avez un compte\b", r"\bse connecter\b", r"\bconnexion\b", r"\bmon compte\b",
    r"\bliste de (souhaits|favoris)\b", r"\bfavoris\b",
    r"\bremplacer la remise\b", r"\bcode (promo|de r[ée]duction)\b",
    r"\bcookies?\b", r"\bnewsletter\b", r"\bmenu\b", r"\brecherche\b",
    r"\bfiltrer\b", r"\btrier par\b", r"\baucun(e)? (r[ée]sultat|adresse|produit|article)\b",
    r"\byour cart\b", r"\bcart\b", r"\bwishlist\b", r"\bsubtotal\b", r"\bsign in\b",
    r"\bnot available in your country\b", r"\badded to (your )?cart\b", r"\bno results?\b",
]
CHROME_RE = re.compile("|".join(CHROME), re.I)
EN_UI_RE = re.compile(r"\b(sorry|your|store|cart|country|available|added|account|close)\b", re.I)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅❌]")
# Conteneurs typiques d'interface : un titre à l'intérieur est probablement du gabarit.
CHROME_CONTAINERS = re.compile(r"(cart|drawer|wishlist|notification|modal|popup|cookie|country|newsletter|search)", re.I)


class Outline(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, attrs) des éléments ouverts
        self.current = None      # titre en cours
        self.headings = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if re.fullmatch(r"h[1-6]", tag):
            ctx = " ".join(f"{t} {d.get('class', '')} {d.get('id', '')}" for t, d in self.stack[-8:])
            self.current = {"level": int(tag[1]), "text": "", "class": a.get("class", "") or "",
                            "container": bool(CHROME_CONTAINERS.search(ctx)), "data_title": a.get("data-title")}
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source", "wbr"):
            self.stack.append((tag, a))

    def handle_endtag(self, tag):
        if self.current and tag == f"h{self.current['level']}":
            self.current["text"] = " ".join(self.current["text"].split())
            self.headings.append(self.current)
            self.current = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data


def fetch(url, opener):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
    with opener.open(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def add_to_cart(url, variant, opener):
    base = re.match(r"https?://[^/]+", url).group(0)
    body = json.dumps({"items": [{"id": int(variant), "quantity": 1}]}).encode()
    req = urllib.request.Request(base + "/cart/add.js", data=body, method="POST",
                                 headers={"User-Agent": UA, "Content-Type": "application/json"})
    opener.open(req, timeout=30).read()


def is_chrome(h):
    t = h["text"] or (h["data_title"] or "")
    return bool(t) and bool(CHROME_RE.search(t)) and (h["container"] or len(t.split()) <= 8)


def analyse(html):
    p = Outline()
    p.feed(html)
    hs = p.headings
    issues = []
    h1 = [h for h in hs if h["level"] == 1]
    if not h1:
        issues.append(("bloquant", "aucun H1"))
    if len(h1) > 1:
        issues.append(("bloquant", f"{len(h1)} H1 : " + " | ".join(h["text"][:50] for h in h1)))
    for h in h1:
        if is_chrome(h):
            issues.append(("bloquant", f"H1 de gabarit : « {h['text'][:60]} »"))
    content_h1 = [h for h in h1 if not is_chrome(h)]
    if content_h1 and h1[0] is not content_h1[0]:
        issues.append(("bloquant", "un H1 de gabarit précède le H1 de contenu dans le code"))
    seen, prev = {}, 0
    for h in hs:
        label = f"H{h['level']} « {(h['text'] or h['data_title'] or '')[:60]} »"
        if h["level"] > 1 and is_chrome(h):
            issues.append(("gabarit", label + " : interface, à passer en <p>/<div> en gardant la classe"))
        if not h["text"]:
            issues.append(("avert", f"H{h['level']} vide" + (f" (rempli en JS : {h['data_title'][:50]})" if h["data_title"] else "")))
        if EMOJI_RE.search(h["text"]):
            issues.append(("avert", label + " : emoji dans un titre"))
        if h["text"] and EN_UI_RE.search(h["text"]) and not re.search(r"[àâçéèêëîïôûùœ]", h["text"].lower()) \
                and len(re.findall(r"\b(the|your|is|not|in|to|of)\b", h["text"], re.I)) >= 2:
            issues.append(("avert", label + " : chaîne d'interface en anglais"))
        if prev and h["level"] > prev + 1:
            issues.append(("avert", label + f" : niveau sauté (H{prev} → H{h['level']})"))
        key = unicodedata.normalize("NFKC", h["text"].lower())
        if key:
            seen[key] = seen.get(key, 0) + 1
        prev = h["level"]
    for k, n in seen.items():
        if n > 1:
            issues.append(("avert", f"titre répété {n} fois : « {k[:60]} »"))
    return hs, issues


def report(source, hs, issues, show_outline=True):
    print(f"\n== {source}")
    if show_outline:
        for h in hs:
            flag = " ⟵ gabarit" if is_chrome(h) else ""
            print(f"  {'  ' * (h['level'] - 1)}H{h['level']} {(h['text'] or '∅ ' + (h['data_title'] or ''))[:90]}{flag}")
    for sev, msg in issues:
        mark = {"bloquant": "✖", "gabarit": "▲", "avert": "·"}[sev]
        print(f"  {mark} {msg}")
    n_block = sum(1 for s, _ in issues if s == "bloquant")
    n_chrome = sum(1 for s, _ in issues if s == "gabarit")
    print(f"  → {len(hs)} titres, {n_block} bloquant(s), {n_chrome} titre(s) de gabarit")
    return n_block


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="URL ou fichier HTML")
    ap.add_argument("--cart-variant", help="Shopify : id de variante à mettre au panier pour un second passage")
    ap.add_argument("--delay", type=float, default=10, help="secondes entre deux requêtes (défaut 10, évite les 429)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="sans le plan, seulement les constats")
    a = ap.parse_args()

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    out, blocking, first = [], 0, True
    passes = [("panier vide", False)] + ([("panier plein", True)] if a.cart_variant else [])
    for state, full in passes:
        for src in a.sources:
            remote = src.startswith("http")
            if full and not remote:
                continue
            if remote and not first:
                time.sleep(a.delay)
            if full and remote and not any(c.name == "cart" for c in jar):
                add_to_cart(src, a.cart_variant, opener)
                time.sleep(a.delay)
            html = fetch(src, opener) if remote else open(src, encoding="utf-8", errors="replace").read()
            first = False
            hs, issues = analyse(html)
            label = f"{src} ({state})" if a.cart_variant else src
            if a.json:
                out.append({"source": src, "etat": state, "titres": hs,
                            "constats": [{"severite": s, "message": m} for s, m in issues]})
                blocking += sum(1 for s, _ in issues if s == "bloquant")
            else:
                blocking += report(label, hs, issues, not a.quiet)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
