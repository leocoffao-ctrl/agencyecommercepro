#!/usr/bin/env python3
"""Contrôles automatiques d'un article HTML avant publication.

Usage :
  python3 article_checks.py article.html [--config brand/kit.config.json]
          [--handle mon-article] [--title "Titre affiché"] [--seo-title "..."]
          [--seo-description "..."] [--no-network]

Code de sortie 1 s'il reste une erreur bloquante.

Le même module est importé par build_articles.py (skill blog-pipeline).
Les deux copies doivent rester identiques : scripts/lint_repo.py le vérifie.
"""
import argparse
import html
import json
import re
import subprocess
import sys
from collections import Counter

DEFAULTS = {
    "brand": {"domain": "", "currency": "EUR"},
    "voice": {"banned_words": [], "no_em_dash": True},
    "blog": {
        "theme_renders_h1": True,
        "theme_emits_jsonld": [],
        "forbid_hardcoded_prices": True,
        "required_ids": ["reponse-rapide"],
        "faq_range": [6, 8],
        "min_internal_destinations": 4,
    },
}
CURRENCY_SIGNS = {"EUR": "€", "USD": r"\$", "GBP": "£", "CHF": "CHF", "CAD": r"\$"}
EM_DASH = "—"


def load_config(path=None):
    """Fusionne kit.config.json avec les valeurs par défaut."""
    cfg = json.loads(json.dumps(DEFAULTS))
    if path:
        user = json.load(open(path, encoding="utf-8"))
        for section, values in user.items():
            if isinstance(values, dict) and isinstance(cfg.get(section), dict):
                cfg[section].update(values)
            else:
                cfg[section] = values
    return cfg


def visible_text(src):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", src, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def http_status(url):
    try:
        out = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-A", "Mozilla/5.0", "-L", "-m", "15", url],
            capture_output=True, text=True)
        return out.stdout.strip() or "ERR"
    except Exception:
        return "ERR"


def price_pattern(currency):
    sign = CURRENCY_SIGNS.get(currency, "€")
    return re.compile(rf"\d+[,.]\d{{2}}\s?{sign}|{sign}\s?\d+[,.]\d{{2}}")


def check(article, body, cfg, pending_handles=(), network=True):
    """Retourne (erreurs, alertes, statistiques).

    article : dict avec handle, title, seo_title, seo_description, summary_html (tous optionnels).
    pending_handles : handles du même lot, pas encore en ligne (leurs liens ne sont pas testés).
    """
    errs, warns = [], []
    blog, voice, brand = cfg["blog"], cfg["voice"], cfg["brand"]
    handle = article.get("handle", "")
    title = article.get("title", "")
    seo_title = article.get("seo_title", "")
    seo_desc = article.get("seo_description", "")

    if handle:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", handle):
            errs.append(f"handle invalide : {handle}")
        if re.search(r"(19|20)\d\d", handle):
            errs.append("millésime dans le handle")
    if seo_title and len(seo_title) > 60:
        errs.append(f"title SEO {len(seo_title)} car. > 60")
    if seo_desc and len(seo_desc) > 155:
        errs.append(f"meta description {len(seo_desc)} car. > 155")
    if seo_title and title and seo_title.strip().lower() == title.strip().lower():
        errs.append("title SEO identique au titre affiché (H1)")
    if voice.get("no_em_dash", True):
        for field in ("title", "seo_title", "seo_description", "summary_html"):
            if EM_DASH in article.get(field, ""):
                errs.append(f"tiret cadratin dans {field}")

    b = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    if "<!--" in body:
        errs.append("commentaire HTML dans le corps : le brief va dans un fichier à part, pas dans le code public")
    if blog.get("theme_renders_h1", True) and re.search(r"<h1[ >]", b):
        errs.append("<h1> dans le corps alors que le gabarit affiche déjà le titre en H1")
    if voice.get("no_em_dash", True) and EM_DASH in b:
        errs.append(f"tiret cadratin x{b.count(EM_DASH)}")
    if blog.get("forbid_hardcoded_prices", True):
        prices = price_pattern(brand.get("currency", "EUR")).findall(b)
        if prices:
            errs.append(f"prix en dur : {prices[:6]}")
    if "aggregateRating" in b:
        errs.append("aggregateRating présent sans avis affichés")
    if re.findall(r"\{\{[^}]+\}\}", b):
        errs.append("variable de gabarit {{ }} non résolue")
    for required in blog.get("required_ids", []):
        if f'id="{required}"' not in b:
            errs.append(f"section #{required} absente")

    text = visible_text(b)
    banned = [w for w in voice.get("banned_words", []) if re.search(rf"(?i)(?<![\w-]){re.escape(w)}(?![\w-])", text)]
    if banned:
        errs.append(f"mots bannis par le contexte de marque : {banned}")

    faq_visible = b.count("<summary")
    faq_schema = len(re.findall(r'"@type"\s*:\s*"Question"', b))
    if faq_schema and faq_visible != faq_schema:
        errs.append(f"FAQ visible {faq_visible} ≠ FAQ du schema {faq_schema}")
    lo, hi = blog.get("faq_range", [0, 99])
    if faq_visible and not lo <= faq_visible <= hi:
        warns.append(f"FAQ : {faq_visible} questions (attendu {lo} à {hi})")

    theme_types = set(blog.get("theme_emits_jsonld", []))
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', b, re.S):
        try:
            data = json.loads(m.group(1))
            nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
            types = [n.get("@type") for n in nodes if isinstance(n, dict)]
            dup = theme_types & {t for t in types if isinstance(t, str)}
            if dup:
                errs.append(f"JSON-LD {sorted(dup)} déjà émis par le gabarit")
        except Exception as exc:
            errs.append(f"JSON-LD invalide : {exc}")

    for tag in ("section", "table", "details", "ul", "ol", "p", "article", "aside", "nav"):
        opened = len(re.findall(rf"<{tag}[ >]", b))
        closed = len(re.findall(rf"</{tag}>", b))
        if opened != closed:
            errs.append(f"<{tag}> non fermé ({opened}/{closed})")

    links = re.findall(r'href="(/[^"#?]*)', b)
    dest = Counter(links)
    if len(dest) < blog.get("min_internal_destinations", 4):
        warns.append(f"seulement {len(dest)} destinations internes")
    domain = brand.get("domain", "").rstrip("/")
    if network and domain:
        bad = []
        for path in dest:
            if path.rstrip("/").split("/")[-1] in pending_handles:
                continue
            status = http_status(domain + path)
            if status != "200":
                bad.append(f"{path} → {status}")
        if bad:
            errs.append("liens internes cassés : " + ", ".join(bad))
    elif not domain:
        warns.append("brand.domain absent de la configuration : liens internes non testés")
    if domain:
        host = re.escape(re.sub(r"^https?://(www\.)?", "", domain))
        if re.search(rf'href="https?://(www\.)?{host}', b):
            warns.append("lien absolu vers le site : préférer un chemin relatif")

    words = len(text.split())
    stats = {"mots": words, "liens": len(links), "destinations": len(dest), "faq": faq_visible,
             "top_liens": dest.most_common(12), "caracteres": len(body)}
    return errs, warns, stats


def report(label, errs, warns, stats, out=sys.stdout):
    print(f"\n=== {label} ===\n  {stats}", file=out)
    for w in warns:
        print("  ⚠", w, file=out)
    for e in errs:
        print("  ✖", e, file=out)
    if not errs:
        print("  ✔ aucun bloquant", file=out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("fichier")
    ap.add_argument("--config")
    ap.add_argument("--handle", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--seo-title", default="")
    ap.add_argument("--seo-description", default="")
    ap.add_argument("--no-network", action="store_true", help="ne teste pas les liens internes")
    a = ap.parse_args()
    cfg = load_config(a.config)
    body = open(a.fichier, encoding="utf-8").read().strip()
    article = {"handle": a.handle, "title": a.title, "seo_title": a.seo_title, "seo_description": a.seo_description}
    errs, warns, stats = check(article, body, cfg, network=not a.no_network)
    report(a.fichier, errs, warns, stats)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
