#!/usr/bin/env python3
"""Construit une page d'annuaire : fiche-<slug>.html, schema-<slug>.json, livraison-<slug>.md.

Usage : python3 build_fiche.py contenu-<slug>.json dossier_sortie/ --config brand/kit.config.json

Le format du contenu est décrit dans references/format-contenu.md.
Les textes peuvent contenir du HTML en ligne (<a>, <strong>, <br>).
Le corps produit ne contient ni balise <style> ni commentaire : la feuille de style
(assets/fiche.css) est chargée par le gabarit, les notes d'intégration vont dans livraison-<slug>.md.
"""
import argparse
import html
import json
import os
import re

EXT = 'rel="nofollow noopener" target="_blank"'

# Libellés par défaut. Surchargés par directory.labels (configuration) puis par "labels" (contenu).
LABELS = {
    "accueil": "Accueil",
    "en_bref": "{n} en {k} points",
    "infos_aria": "Informations pratiques {n}",
    "maps": "Voir sur Google Maps",
    "sommaire": "Sommaire",
    "som_identite": "Présentation",
    "som_specialite": "Spécialité",
    "som_offre": "Offre et prix",
    "som_decision": "Que choisir",
    "som_test": "Notre test",
    "som_prix": "Ce que ça vaut",
    "som_transparence": "À qui ça ne convient pas",
    "som_acces": "Où et comment",
    "som_comparatif": "Comparatif",
    "som_avis": "Avis",
    "som_faq": "FAQ",
    "jauge_aria": "Prix comparés, relevé du {date}",
    "jauge_echelle": "Échelle de 0 à {mx} {unite}.",
    "avis_invitation": "Un avis sur {n} ? Il aidera les prochains lecteurs à choisir.",
    "faq_h2": "Questions fréquentes sur {n}",
    "alternatives_h2": "Quelles alternatives à {n} ?",
    "encart_a_h2": "Vous êtes {n} ?",
    "encart_a_p": ("Cette fiche est rédigée par l'équipe {brand} à partir de sources publiques. Vous pouvez la "
                   "revendiquer gratuitement pour corriger les informations, ajouter vos photos et vos références actuelles."),
    "encart_a_cta": "Revendiquer cette fiche",
    "encart_b_h2": "Fiche revendiquée par {n}",
    "encart_c_h2": "{n} est partenaire de {brand}",
    "encart_correction": ("Vous êtes {n} et une information a changé ? <a href=\"{contact}?sujet=fiche-{slug}\">Écrivez-nous</a> : "
                          "nous corrigeons sous 7 jours."),
    "sources_h2": "Sources et date de relevé de cette fiche",
    "sources_p": ("Fiche rédigée par l'équipe {brand} à partir de sources publiques, vérifiées le {date}. "
                  "Contenu éditorial indépendant : {n} n'a pas relu ce texte."),
    "sources_revision": "Prochaine révision prévue : {revision}.",
    "decouvre_h2": "À découvrir aussi chez {brand}",
    "itemlist": "Offre de {n} relevée le {date}",
}


def vt(x):
    """Texte visible d'un fragment HTML."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()


def paras(lst):
    return "\n".join(f"<p>{p}</p>" for p in lst)


def table(cls, head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = []
    for r in rows:
        tds = "".join(f'<td data-label="{html.escape(vt(h))}">{c}</td>' for h, c in zip(head, r))
        body.append(f"<tr>{tds}</tr>")
    c = f" {cls}" if cls else ""
    return f'<table class="vk-table{c}">\n<thead><tr>{th}</tr></thead>\n<tbody>\n' + "\n".join(body) + "\n</tbody>\n</table>"


def maps_link(pid, label):
    return f'<a href="https://www.google.com/maps/place/?q=place_id:{pid}" {EXT}>{label}</a>'


def build(c, cfg):
    brand = cfg["brand"]["name"]
    site = cfg["brand"]["domain"].rstrip("/")
    d = cfg.get("directory", {})
    t = d["types"][c["type"]]
    lab = dict(LABELS)
    lab.update(d.get("labels", {}))
    lab.update(c.get("labels", {}))
    n, slug, date = c["nom"], c["slug"], c["date_releve"]  # date au format JJ/MM/AAAA
    contact = d.get("contact_path", "/contact")
    fmt = dict(n=n, brand=brand, date=date, slug=slug, contact=contact, k=len(c["reponse_rapide"]))
    L = lambda key, **kw: lab[key].format(**{**fmt, **kw})
    S = c["sections"]
    notes = []

    out = ['<div class="vk-fiche">']
    out.append(f'<nav class="vk-breadcrumb" aria-label="Fil d\'Ariane"><a href="/">{L("accueil")}</a> › '
               f'<a href="{t["hub"]}">{t["label"]}</a> › {n}</nav>')

    # 02 HERO
    badges = "".join(f'<li class="vk-badge {cls}">{txt}</li>' for txt, cls in c.get("badges", []))
    data = "".join(f"<li>{x}</li>" for x in c.get("ligne_donnees", []))
    hero = ""
    if c.get("hero_url"):
        hero = (f'<img src="{c["hero_url"]}" width="1200" height="630" fetchpriority="high" decoding="async" '
                f'alt="{html.escape(c["alt_hero"])}">\n')
    else:
        notes.append(f"Image d'en-tête absente : ajouter `{slug}.webp` (1200×630, moins de 150 Ko), texte alternatif « {c.get('alt_hero', '')} », "
                     "puis renseigner `hero_url` et régénérer.")
    out.append(f'<header class="vk-hero">\n<p class="vk-sous-titre">{c["sous_titre"]}</p>\n'
               f'<ul class="vk-data">{data}</ul>\n<ul class="vk-badges">{badges}</ul>\n{hero}</header>')

    # 03 RÉPONSE RAPIDE
    lis = "\n".join(f"<li>{x}</li>" for x in c["reponse_rapide"])
    out.append(f'<section class="reponse-rapide" id="en-bref" aria-label="{html.escape(L("en_bref"))}">\n'
               f'<p>{L("en_bref")}</p>\n<ul>\n{lis}\n</ul>\n</section>')

    # 04 INFOS PRATIQUES
    cards = []
    for card in c.get("infos", []):
        lines = "".join(f"<p>{x}</p>" for x in card["lignes"])
        if card.get("place_id"):
            lines += f'<p>{maps_link(card["place_id"], card.get("maps_label", L("maps")))}</p>'
        cards.append(f'<div>\n<h3>{card["titre"]}</h3>\n{lines}\n</div>')
    out.append(f'<section class="vk-infos" aria-label="{html.escape(L("infos_aria"))}">\n' + "\n".join(cards) + "\n</section>")

    # 05 SOMMAIRE
    som = [("presentation", "som_identite"), ("specialite", "som_specialite"), ("offre", "som_offre"), ("choisir", "som_decision")]
    if c.get("test_maison"):
        som.append(("test", "som_test"))
    som += [("prix", "som_prix"), ("pour-qui", "som_transparence"), ("acces", "som_acces"),
            ("comparatif", "som_comparatif"), ("avis", "som_avis"), ("faq", "som_faq")]
    out.append(f'<div class="vk-layout">\n<nav class="vk-sommaire" aria-label="{L("sommaire")}">\n'
               f'<p class="vk-sommaire-titre">{L("sommaire")}</p>\n<ol>'
               + "".join(f'<li><a href="#{a}">{L(b)}</a></li>' for a, b in som) + '</ol>\n</nav>\n<div class="vk-contenu">')

    # 06 PRÉSENTATION
    out.append(f'<section id="presentation">\n<h2>{S["identite"]["h2"]}</h2>\n{paras(S["identite"]["p"])}\n</section>')

    # 07 SPÉCIALITÉ (échelle à trois segments, facultative)
    sp = S["specialite"]
    echelle = ""
    if sp.get("echelle_labels"):
        active = sp.get("actif")
        act = active if isinstance(active, list) else ([] if active is None else [active])
        segs = "".join(f'<span class="vk-actif">{x}</span>' if i in act else f"<span>{x}</span>"
                       for i, x in enumerate(sp["echelle_labels"]))
        echelle = (f'<div class="vk-echelle" aria-hidden="true">{segs}</div>\n'
                   f'<p class="vk-echelle-note">{sp.get("note_echelle", "")}</p>\n')
    out.append(f'<section id="specialite">\n<h2>{sp["h2"]}</h2>\n<p>{sp["p"][0]}</p>\n{echelle}{paras(sp["p"][1:])}\n</section>')

    # 08 OFFRE
    g = S["offre"]
    out.append(f'<section id="offre">\n<h2>{g["h2"]}</h2>\n{paras(g["p"])}\n'
               f'{table("vk-offre", g["entetes"], g["lignes"])}\n<p class="vk-releve">{g["releve"]}</p>\n</section>')

    # 09 DÉCISION
    de = S["decision"]
    out.append(f'<section id="choisir">\n<h2>{de["h2"]}</h2>\n{paras(de["p"])}\n'
               f'{table("vk-decision", de["entetes"], de["lignes"])}\n</section>')

    # 10 TEST MAISON (contenu propriétaire, facultatif)
    if c.get("test_maison"):
        tm = c["test_maison"]
        out.append(f'<section id="test">\n<h2>{tm["h2"]}</h2>\n{paras(tm["p"])}\n</section>')
    else:
        notes.append(f"Bloc 10 (test maison) supprimé : {brand} n'a pas de relevé avec protocole sur {n}.")

    # 11 CE QUE ÇA VAUT
    p = S["prix"]
    jauge = ""
    if p.get("jauge"):
        mx = p.get("echelle_max", 100)
        lines = []
        for i, (label, lo, hi, txt) in enumerate(p["jauge"]):
            left = round(lo / mx * 100, 1)
            width = max(round((hi - lo) / mx * 100, 1), 1.5)
            cls = "" if i == 0 else ' class="vk-autre"'
            lines.append(f'<div class="vk-jauge-ligne"><span>{label}</span><div class="vk-jauge-barre">'
                         f'<i{cls} style="left:{left}%;width:{width}%"></i></div><span>{txt}</span></div>')
        jauge = (f'<div class="vk-jauge" aria-label="{html.escape(L("jauge_aria"))}">\n' + "\n".join(lines) +
                 f'\n</div>\n<p class="vk-releve">{L("jauge_echelle", mx=mx, unite=p.get("unite", ""))} {p.get("note_jauge", "")}</p>\n')
    out.append(f'<section id="prix">\n<h2>{p["h2"]}</h2>\n<p>{p["p"][0]}</p>\n{jauge}{paras(p["p"][1:])}\n</section>')

    # 12 TRANSPARENCE (obligatoire)
    tr = S["transparence"]
    items = "\n".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in tr["items"])
    out.append(f'<section id="pour-qui">\n<h2>{tr["h2"]}</h2>\n<div class="vk-transparence">\n'
               f'<p>{tr["intro"]}</p>\n<ul>\n{items}\n</ul>\n</div>\n</section>')

    # 13 ACCÈS
    a = S["acces"]
    items = "\n".join(f"<li><strong>{x}</strong> {y}</li>" for x, y in a["items"])
    out.append(f'<section id="acces">\n<h2>{a["h2"]}</h2>\n<p>{a["intro"]}</p>\n'
               f'<ol class="vk-achat">\n{items}\n</ol>\n{paras(a.get("outro", []))}\n</section>')

    # 14 COMPARATIF
    cp = S["comparatif"]
    out.append(f'<section id="comparatif">\n<h2>{cp["h2"]}</h2>\n<p>{cp["intro"]}</p>\n'
               f'{table("", cp["entetes"], cp["lignes"])}\n<p>{cp["outro"]}</p>\n</section>')

    # 15 AVIS
    av = S["avis"]
    out.append(f'<section id="avis">\n<h2>{av["h2"]}</h2>\n<p class="vk-avis-note">{av["note"]}</p>\n'
               f'{paras(av["p"])}\n<p>{L("avis_invitation")}</p>\n</section>')
    notes.append("Module d'avis du site : à conserver, masqué tant qu'aucun avis n'est publié. Pas d'aggregateRating.")

    # 16 FAQ
    faq = "\n".join(f"<details><summary>{q}</summary><p>{r}</p></details>" for q, r in c["faq"])
    out.append(f'<section id="faq" class="vk-faq">\n<h2>{L("faq_h2")}</h2>\n{faq}\n</section>')

    # 17 ALTERNATIVES
    al = S["alternatives"]
    lis = "\n".join(f'<li><a href="{t["path_prefix"]}{s}"><strong>{nm}</strong></a><span>{ds}</span></li>'
                    for s, nm, ds in al["liste"])
    out.append(f'<section id="alternatives">\n<h2>{al.get("h2") or L("alternatives_h2")}</h2>\n<p>{al["intro"]}</p>\n'
               f'<ul class="vk-alternatives">\n{lis}\n</ul>\n</section>')

    # 18 ENCART MARQUE (A non revendiquée / B revendiquée / C partenaire)
    etat = c.get("etat_encart", "A")
    cta = c.get("encart_cta")
    cta_html = f'<p><a class="vk-cta" href="{cta[0]}">{cta[1]}</a></p>\n' if cta else ""
    if etat == "C":
        enc = (f'<aside class="vk-encart-marque" aria-label="{html.escape(L("encart_c_h2"))}">\n<h2>{L("encart_c_h2")}</h2>\n'
               f'<p>{c.get("encart_texte", "")}</p>\n{cta_html}<p>{L("encart_correction")}</p>\n</aside>')
    elif etat == "B":
        enc = (f'<aside class="vk-encart-marque" aria-label="{html.escape(L("encart_b_h2"))}">\n<h2>{L("encart_b_h2")}</h2>\n'
               f'<p>{c.get("encart_texte", "")}</p>\n{cta_html}<p>{L("encart_correction")}</p>\n</aside>')
    else:
        enc = (f'<aside class="vk-encart-marque" aria-label="{html.escape(L("encart_a_h2"))}">\n<h2>{L("encart_a_h2")}</h2>\n'
               f'<p>{L("encart_a_p")}</p>\n'
               f'<p><a class="vk-cta" href="{contact}?sujet=revendiquer-{slug}">{L("encart_a_cta")}</a></p>\n'
               + (f'<p>{c["encart_texte"]}</p>\n' if c.get("encart_texte") else "") + "</aside>")
    out.append(enc)
    notes.append(f"Encart marque : état {etat} (A non revendiquée, B revendiquée, C partenaire).")

    # 19 SOURCES
    src = "\n".join(f"<li>{s}</li>" for s in c["sources"])
    revision = c.get("prochaine_revision") or d.get("next_review", "")
    out.append(f'<section class="vk-sources" aria-label="Sources">\n<h2>{L("sources_h2")}</h2>\n'
               f'<p>{L("sources_p")}</p>\n<ol>\n{src}\n</ol>\n'
               + (f'<p class="vk-mention">{L("sources_revision", revision=revision)}</p>\n' if revision else "") + "</section>")

    # 20 À DÉCOUVRIR
    btns = "\n".join(f'<a class="vk-cta" href="{u}">{label}</a>' for u, label in c.get("decouvre_boutons", []))
    out.append(f'<section aria-label="{html.escape(L("decouvre_h2"))}">\n<h2>{L("decouvre_h2")}</h2>\n'
               f'<p>{c.get("decouvre_texte", "")}</p>\n<div class="vk-decouvre">\n{btns}\n</div>\n</section>')
    out.append("</div>\n</div>\n</div>\n")
    page = "\n\n".join(out)

    # SCHEMA : Article dont `about` décrit l'entité. Le site écrit sur elle, il n'est pas elle.
    url = f"{site}{t['path_prefix']}{slug}"
    about = {"@type": t.get("about_type", "Organization"), "name": n}
    about.update(c.get("schema_about", {}))
    faq_s = [{"@type": "Question", "name": vt(q), "acceptedAnswer": {"@type": "Answer", "text": vt(r)}} for q, r in c["faq"]]
    items = []
    for i, row in enumerate(g["lignes"], 1):
        cells = [vt(x) for x in row]
        items.append({"@type": "ListItem", "position": i, "name": cells[0],
                      "description": " · ".join(cells[1:]) + f" (relevé du {date})"})
    iso = "-".join(reversed(date.split("/")))
    org = {"@type": "Organization", "name": brand, "url": site}
    publisher = dict(org)
    if cfg["brand"].get("logo_url"):
        publisher["logo"] = {"@type": "ImageObject", "url": cfg["brand"]["logo_url"]}
    article = {"@type": "Article", "@id": url + "#article", "headline": c["schema_headline"],
               "description": c["meta_description"], "datePublished": c.get("date_publication_iso", iso),
               "dateModified": iso, "inLanguage": cfg["brand"].get("locale", "fr-FR"), "mainEntityOfPage": url,
               "author": org, "publisher": publisher}
    if c.get("hero_url"):
        article["image"] = c["hero_url"]
    article["about"] = about
    article["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": [".reponse-rapide"]}
    graph = {"@context": "https://schema.org", "@graph": [
        article,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L("accueil"), "item": site + "/"},
            {"@type": "ListItem", "position": 2, "name": t["label"], "item": site + t["hub"]},
            {"@type": "ListItem", "position": 3, "name": n, "item": url}]},
        {"@type": "FAQPage", "mainEntity": faq_s},
        {"@type": "ItemList", "name": L("itemlist"), "numberOfItems": len(items), "itemListElement": items}]}

    title, meta = c["meta_title"], c["meta_description"]
    livraison = [f"# Livraison — {n}", "",
                 f"- URL cible : `{url}`", f"- Titre de l'article (H1) : {n}",
                 f"- Title ({len(title)} car.) : {title}", f"- Meta description ({len(meta)} car.) : {meta}",
                 f"- Données relevées le {date}", "",
                 "## Intégration", "",
                 "- Coller `fiche-" + slug + ".html` dans le corps de l'article, en mode HTML.",
                 "- La feuille `fiche.css` est chargée par le gabarit : aucune balise de style dans le corps.",
                 "- Coller `schema-" + slug + ".json` dans le champ de données structurées de l'article.",
                 f"- Ajouter la fiche à la page pivot `{t['hub']}` si elle est tenue à la main.", "",
                 "## Notes", ""] + [f"- {x}" for x in notes]
    if len(title) > 60 or len(meta) > 155:
        livraison += ["", "**Alerte** : title ou meta description trop long."]
    return page, graph, "\n".join(livraison) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("contenu")
    ap.add_argument("sortie")
    ap.add_argument("--config", required=True)
    a = ap.parse_args()
    c = json.load(open(a.contenu, encoding="utf-8"))
    cfg = json.load(open(a.config, encoding="utf-8"))
    os.makedirs(a.sortie, exist_ok=True)
    page, graph, livraison = build(c, cfg)
    slug = c["slug"]
    open(os.path.join(a.sortie, f"fiche-{slug}.html"), "w", encoding="utf-8").write(page)
    open(os.path.join(a.sortie, f"schema-{slug}.json"), "w", encoding="utf-8").write(
        json.dumps(graph, ensure_ascii=False, indent=2))
    open(os.path.join(a.sortie, f"livraison-{slug}.md"), "w", encoding="utf-8").write(livraison)
    print(f"title {len(c['meta_title'])} car. | meta {len(c['meta_description'])} car. | sortie : {a.sortie}")


if __name__ == "__main__":
    main()
