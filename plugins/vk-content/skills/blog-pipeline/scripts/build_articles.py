#!/usr/bin/env python3
"""Contrôle un lot d'articles et produit le fichier d'import.

Usage :
  python3 build_articles.py manifest-lot.json SORTIE [--config brand/kit.config.json]
          [--format matrixify|json] [--no-network]

manifest-lot.json :
  [{"handle": "...", "title": "Titre affiché", "body_file": "<handle>.html",
    "summary_html": "<p>Deux phrases.</p>", "tags": "guides, theme",
    "seo_title": "≤ 60 car.", "seo_description": "≤ 155 car.",
    "published_at_prevu": "AAAA-MM-JJ HH:MM"}]

Formats :
  matrixify  CSV UTF-8 « Blog Posts » pour l'application Matrixify (Shopify), Command NEW, non publié.
  json       lot neutre, un objet par article, pour une API de CMS (WordPress, autre).

Code de sortie 1 si un article porte une erreur bloquante : rien ne doit être publié dans ce cas.
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_checks import check, load_config, report  # noqa: E402

MATRIXIFY_COLS = ["Handle", "Command", "Title", "Author", "Body HTML", "Summary HTML", "Tags",
                  "Tags Command", "Published", "Template Suffix", "Blog: Handle",
                  "Metafield: title_tag [string]", "Metafield: description_tag [string]"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifest")
    ap.add_argument("sortie")
    ap.add_argument("--config")
    ap.add_argument("--format", choices=["matrixify", "json"], default="matrixify")
    ap.add_argument("--no-network", action="store_true", help="ne teste pas les liens internes")
    a = ap.parse_args()

    cfg = load_config(a.config)
    blog = cfg["blog"]
    base_dir = os.path.dirname(os.path.abspath(a.manifest))
    articles = json.load(open(a.manifest, encoding="utf-8"))
    pending = {art["handle"] for art in articles}

    ok, rows, bundle = True, [], []
    for art in articles:
        body = open(os.path.join(base_dir, art["body_file"]), encoding="utf-8").read().strip()
        errs, warns, stats = check(art, body, cfg, pending_handles=pending, network=not a.no_network)
        if a.format == "matrixify" and len(body) > 32000:
            warns.append(f"corps de {len(body)} caractères : correct en CSV, trop long pour une cellule de tableur")
        report(art["handle"], errs, warns, stats)
        ok = ok and not errs
        author = art.get("author") or blog.get("author", "")
        tags = art.get("tags", blog.get("handle", ""))
        rows.append({"Handle": art["handle"], "Command": "NEW", "Title": art["title"], "Author": author,
                     "Body HTML": body, "Summary HTML": art.get("summary_html", ""), "Tags": tags,
                     "Tags Command": "REPLACE", "Published": "FALSE",
                     "Template Suffix": blog.get("template_suffix", ""), "Blog: Handle": blog.get("handle", ""),
                     "Metafield: title_tag [string]": art.get("seo_title", ""),
                     "Metafield: description_tag [string]": art.get("seo_description", "")})
        bundle.append({"handle": art["handle"], "title": art["title"], "author": author, "body_html": body,
                       "summary_html": art.get("summary_html", ""),
                       "tags": [t.strip() for t in tags.split(",") if t.strip()],
                       "seo_title": art.get("seo_title", ""), "seo_description": art.get("seo_description", ""),
                       "scheduled_for": art.get("published_at_prevu", ""), "status": "draft"})

    if a.format == "matrixify":
        with open(a.sortie, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=MATRIXIFY_COLS, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(rows)
        back = list(csv.DictReader(open(a.sortie, encoding="utf-8")))
        assert len(back) == len(rows) and all(back[i]["Body HTML"] == rows[i]["Body HTML"] for i in range(len(rows)))
    else:
        json.dump(bundle, open(a.sortie, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"\n{a.format} écrit : {a.sortie} ({len(rows)} article(s)) — {'OK' if ok else 'ÉCHEC, corriger avant livraison'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
