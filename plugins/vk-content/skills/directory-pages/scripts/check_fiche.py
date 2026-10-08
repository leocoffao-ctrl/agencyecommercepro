#!/usr/bin/env python3
"""Contrôles automatiques d'une page d'annuaire avant publication.

Usage : python3 check_fiche.py fiche.html [schema.json] --config brand/kit.config.json --type <type>

<type> est une clé de directory.types dans la configuration (hub, préfixe, seuils).
Code de sortie 1 s'il reste une alerte bloquante.
"""
import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser

BLOQUANT, ALERTE, OK = "BLOQUANT", "ALERTE", "OK"


class TagBalance(HTMLParser):
    VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr", "col"}

    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"</{tag}> inattendu (pile : {self.stack[-3:]})")


def visible_text(src):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", src, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def run(src, schema_raw, cfg, type_key):
    results = []
    add = lambda level, msg: results.append((level, msg))
    d = cfg.get("directory", {})
    t = d["types"][type_key]
    host = re.sub(r"^https?://(www\.)?", "", cfg["brand"]["domain"]).rstrip("/")
    text = visible_text(src)

    # Densité
    count = lambda x: len(re.findall(r"[\wÀ-ÿ'’-]+", x))
    prose = count(visible_text(re.sub(r"<table.*?</table>|<nav.*?</nav>", " ", src, flags=re.S)))
    lo, hi = t.get("target_words", [1800, 2600])
    floor, ceil = t.get("min_words", 1500), t.get("max_words", 3000)
    add(OK, f"Mots visibles, tableaux compris : {count(text)}")
    add(OK if prose >= floor else BLOQUANT, f"Mots rédactionnels hors tableaux et navigation : {prose} (cible {lo}-{hi}, plancher {floor})")
    if prose > ceil:
        add(ALERTE, f"Rédactionnel au-delà de {ceil} mots : densité diluée")

    # Corps propre
    if re.search(r"<style", src):
        add(BLOQUANT, "balise <style> dans le corps : la feuille de style appartient au gabarit")
    if "<!--" in src:
        add(BLOQUANT, "commentaire HTML dans le corps : les notes vont dans le fichier de livraison")
    raw_vars = re.findall(r"\{\{[^}]*\}\}|\{%[^%]*%\}", src)
    add(BLOQUANT if raw_vars else OK, f"Variables de gabarit non résolues : {len(raw_vars)}")
    trunc = re.findall(r"\w(?:\.\.\.|…)", text)
    add(ALERTE if trunc else OK, f"Troncatures suspectes : {len(trunc)}")

    # Vocabulaire interdit par le contexte
    banned = cfg.get("voice", {}).get("banned_words", [])
    found = sorted({w for w in banned if re.search(rf"(?i)(?<![\w-]){re.escape(w)}(?![\w-])", text)})
    add(BLOQUANT if found else OK, f"Vocabulaire interdit : {found or 'aucun'}")
    if cfg.get("voice", {}).get("no_em_dash", True) and "—" in text:
        add(BLOQUANT, "tiret cadratin dans le texte visible")

    # Balises
    tb = TagBalance()
    tb.feed(re.sub(r"<(script|style)[^>]*>.*?</\1>", "", src, flags=re.S | re.I))
    tb.close()
    if tb.errors or tb.stack:
        add(BLOQUANT, f"Balises déséquilibrées : {tb.errors[:3]} reste {tb.stack}")
    else:
        add(OK, "Balises équilibrées")

    # Liens
    ext_bad, internal, maps_place, maps_search = [], [], 0, 0
    for a in re.findall(r"<a\b[^>]*>", src):
        href = re.search(r'href="([^"]+)"', a)
        if not href:
            continue
        h = href.group(1)
        rel = re.search(r'rel="([^"]*)"', a)
        rel = rel.group(1) if rel else ""
        if h.startswith("#"):
            continue
        if h.startswith("/") or (host and host in h):
            internal.append(re.sub(rf"^https?://(www\.)?{re.escape(host)}", "", h) if host else h)
            continue
        if "maps/place/?q=place_id:" in h:
            maps_place += 1
        if "maps/search/" in h:
            maps_search += 1
        if not re.search(r"nofollow|sponsored", rel):
            ext_bad.append(h)
        if "noopener" not in rel:
            add(ALERTE, f"Lien sortant sans noopener : {h}")
    add(ALERTE if ext_bad else OK,
        f"Sortants sans nofollow ni sponsored : {len(ext_bad)} (tolérés seulement pour la presse et les registres) {ext_bad}")
    if t.get("require_place_id", True):
        add(OK if maps_place >= 1 else BLOQUANT, f"Liens de carte par identifiant de lieu : {maps_place}")
    add(BLOQUANT if maps_search else OK, f"Liens de carte par recherche de nom : {maps_search}")

    hub = t["hub"].rstrip("/")
    strip = lambda h: h.split("?")[0].split("#")[0].rstrip("/")
    pivot = [h for h in internal if strip(h) == hub]
    cluster = {strip(h) for h in internal if any(p in h for p in t.get("cluster_patterns", [t["path_prefix"]]))}
    commercial = {strip(h) for h in internal if any(p in h for p in d.get("commercial_patterns", []))}
    add(OK if len(pivot) >= 2 else ALERTE, f"Liens vers la page pivot {hub} : {len(pivot)} (2 au moins)")
    add(OK if len(cluster) >= 6 else ALERTE, f"Fiches et guides du même ensemble liés : {len(cluster)} (6 au moins)")
    add(OK if len(commercial) >= 3 else ALERTE, f"URL commerciales distinctes : {len(commercial)} (3 au moins)")
    anchors = [visible_text(x).lower() for x in
               re.findall(rf'<a[^>]+href="[^"]*{re.escape(hub)}/?"[^>]*>(.*?)</a>', src, flags=re.S)]
    if len(anchors) != len(set(anchors)):
        add(ALERTE, f"Ancres répétées vers la page pivot : {anchors}")

    # Images
    for img in re.findall(r"<img\b[^>]*>", src):
        if not re.search(r'\bwidth="', img) or not re.search(r'\bheight="', img):
            add(BLOQUANT, f"Image sans dimensions : {img[:80]}")
        if not re.search(r'\balt="[^"]+"', img):
            add(BLOQUANT, f"Image sans texte alternatif : {img[:80]}")

    # Blocs obligatoires
    for cls, label in [("reponse-rapide", "Réponse rapide"), ("vk-transparence", "À qui ça ne convient pas"),
                       ("vk-decision", "Tableau de décision"), ("vk-offre", "Tableau de l'offre"),
                       ("vk-encart-marque", "Encart marque"), ("vk-sources", "Sources datées")]:
        add(OK if cls in src else BLOQUANT, f"Bloc {label} présent : {cls in src}")
    block = re.search(r'class="[^"]*reponse-rapide[^"]*".*?</ul>', src, flags=re.S)
    n_items = len(re.findall(r"<li", block.group(0))) if block else 0
    want = t.get("quick_answer_items", 6)
    add(OK if n_items == want else BLOQUANT, f"Puces de la réponse rapide : {n_items} ({want} attendues)")

    # Titres
    h2 = [visible_text(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", src, flags=re.S)]
    short = [x for x in h2 if len(x.split()) < 3]
    add(ALERTE if short else OK, f"H2 trop courts pour être une question ou une affirmation : {short}")

    # FAQ
    faq_visible = [visible_text(q) for q in re.findall(r"<summary[^>]*>(.*?)</summary>", src, flags=re.S)]
    want_faq = t.get("faq_items", 8)
    add(OK if len(faq_visible) == want_faq else ALERTE, f"Questions de FAQ visibles : {len(faq_visible)} ({want_faq} attendues)")

    # Schema
    if schema_raw:
        if "aggregateRating" in schema_raw:
            add(BLOQUANT, "aggregateRating présent dans le schema")
        data = json.loads(schema_raw)
        graph = data.get("@graph", [data])
        forbidden = set(t.get("forbidden_schema_types", []))
        roots = {g.get("@type") for g in graph}
        hit = sorted(forbidden & roots)
        add(BLOQUANT if hit else OK, f"Types interdits en racine du schema : {hit or 'aucun'}")
        faq = next((g for g in graph if g.get("@type") == "FAQPage"), None)
        if faq:
            names = [q["name"] for q in faq["mainEntity"]]
            add(OK if names == faq_visible else BLOQUANT, "FAQ du schema identique à la FAQ visible" if names == faq_visible
                else "FAQ du schema différente de la FAQ visible (ordre ou libellé)")
            for q in faq["mainEntity"]:
                if q["acceptedAnswer"]["text"] not in text:
                    add(BLOQUANT, f"Réponse de FAQ absente mot pour mot de la page : {q['name']}")
        else:
            add(BLOQUANT, "Pas de FAQPage dans le schema")
        bc = next((g for g in graph if g.get("@type") == "BreadcrumbList"), None)
        if not bc or not any(hub in str(i.get("item", "")) for i in bc["itemListElement"]):
            add(BLOQUANT, f"Fil d'Ariane du schema sans échelon {hub}")
        art = next((g for g in graph if g.get("@type") == "Article"), None)
        if art and art.get("image") and art["image"] not in src:
            add(ALERTE, "Image du schema absente du HTML (image d'en-tête à aligner)")
        if art and art.get("about", {}).get("@type") != t.get("about_type", "Organization"):
            add(ALERTE, f"about.@type attendu : {t.get('about_type', 'Organization')}")
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("fiche")
    ap.add_argument("schema", nargs="?")
    ap.add_argument("--config", required=True)
    ap.add_argument("--type", required=True, dest="type_key")
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    src = open(a.fiche, encoding="utf-8").read()
    schema_raw = open(a.schema, encoding="utf-8").read() if a.schema else None
    results = run(src, schema_raw, cfg, a.type_key)
    for level, msg in results:
        print(f"[{level:8}] {msg}")
    blocking = sum(1 for lv, _ in results if lv == BLOQUANT)
    alerts = sum(1 for lv, _ in results if lv == ALERTE)
    print(f"\n{blocking} bloquant(s), {alerts} alerte(s)")
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
