#!/usr/bin/env python3
"""Exécute chaque script du kit sur les exemples fictifs.

  python3 tests/run_tests.py            # tout, rendu vidéo compris si les dépendances sont là
  python3 tests/run_tests.py --no-video # sans le rendu vidéo

Chaque cas vérifie le code de sortie attendu, et parfois un fragment de la sortie.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(ROOT, "tests", "fixtures")
TMP = os.path.join(ROOT, "tests", "_tmp")
CFG = os.path.join(ROOT, "examples", "atelier-verveine", "brand", "kit.config.json")
P = lambda *a: os.path.join(ROOT, "plugins", *a)

results = []


def run(label, cmd, expect=0, contains=None):
    proc = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=ROOT)
    out = proc.stdout + proc.stderr
    ok = proc.returncode == expect and (contains is None or all(c in out for c in contains))
    results.append((ok, label))
    print(("✔" if ok else "✖"), label)
    if not ok:
        print(f"    code {proc.returncode} (attendu {expect})")
        print("    " + "\n    ".join(out.strip().splitlines()[-12:]))
    return out


shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(TMP)

# Configuration d'essai : seuils abaissés pour la fiche d'exemple, volontairement courte.
cfg = json.load(open(CFG, encoding="utf-8"))
cfg["directory"]["types"]["producteur"].update(min_words=300, target_words=[300, 2600])
CFG_TEST = os.path.join(TMP, "kit.config.json")
json.dump(cfg, open(CFG_TEST, "w", encoding="utf-8"), ensure_ascii=False)

# --- articles
checks = P("vk-seo", "skills", "seo-writer", "scripts", "article_checks.py")
run("article conforme", [checks, os.path.join(FIX, "article-ok.html"), "--config", CFG, "--no-network",
                          "--handle", "infuser-verveine-citronnee", "--title", "Un titre affiché",
                          "--seo-title", "Infuser la verveine citronnée"], expect=0, contains=["aucun bloquant"])
run("article fautif bloqué", [checks, os.path.join(FIX, "article-fautif.html"), "--config", CFG, "--no-network",
                               "--handle", "guide-2026"], expect=1,
    contains=["millésime", "commentaire HTML", "<h1>", "tiret cadratin", "prix en dur", "mots bannis", "déjà émis", "reponse-rapide"])

build = P("vk-content", "skills", "blog-pipeline", "scripts", "build_articles.py")
run("lot d'articles → CSV Matrixify", [build, os.path.join(FIX, "manifest-lot.json"),
                                       os.path.join(TMP, "Blog Posts - test.csv"), "--config", CFG, "--no-network"], expect=0)
run("lot d'articles → JSON neutre", [build, os.path.join(FIX, "manifest-lot.json"), os.path.join(TMP, "lot.json"),
                                     "--config", CFG, "--format", "json", "--no-network"], expect=0)

# --- pages d'annuaire
D = P("vk-content", "skills", "directory-pages")
run("fiche d'annuaire générée", [os.path.join(D, "scripts", "build_fiche.py"),
                                 os.path.join(D, "references", "exemple-contenu.json"),
                                 os.path.join(TMP, "fiche"), "--config", CFG_TEST], expect=0)
fiche = os.path.join(TMP, "fiche", "fiche-ferme-des-courtils.html")
schema = os.path.join(TMP, "fiche", "schema-ferme-des-courtils.json")
run("fiche d'annuaire conforme", [os.path.join(D, "scripts", "check_fiche.py"), fiche, schema,
                                  "--config", CFG_TEST, "--type", "producteur"], expect=0, contains=["0 bloquant(s)"])
run("fiche trop courte bloquée au seuil réel", [os.path.join(D, "scripts", "check_fiche.py"), fiche, schema,
                                               "--config", CFG, "--type", "producteur"], expect=1, contains=["plancher 1500"])

# --- réseaux
S = P("vk-social", "skills", "social-publish", "scripts")
run("légende sans tic d'IA", [os.path.join(S, "check_anti_ia.py"), "--json", os.path.join(FIX, "posts-ok.json"),
                             "--config", CFG], expect=0)
run("légende avec tics bloquée", [os.path.join(S, "check_anti_ia.py"), "--json", os.path.join(FIX, "posts-fautifs.json"),
                                 "--config", CFG], expect=1, contains=["tiret cadratin", "mot banni"])
run("forme de légende conforme", [os.path.join(S, "check_legende.py"), "--json", os.path.join(FIX, "posts-ok.json"),
                                 "--config", CFG], expect=0)
run("trop de hashtags bloqué", [os.path.join(S, "check_legende.py"), "--json", os.path.join(FIX, "posts-fautifs.json"),
                               "--config", CFG], expect=1, contains=["maximum 5"])
run("accroches classées", [os.path.join(S, "score_accroche.py"), os.path.join(FIX, "accroches.txt"), "--config", CFG],
    expect=0, contains=["CLASSEMENT", "rédhibitoire"])
run("audit des posts", [P("vk-social", "skills", "social-plan", "scripts", "audit.py"), os.path.join(FIX, "analytics.json")],
    expect=0, contains=["2 posts publiés", "trop peu pour conclure"])

# --- vidéo
if "--no-video" not in sys.argv:
    try:
        import numpy  # noqa: F401
        import PIL  # noqa: F401
        has_deps = shutil.which("ffmpeg") is not None
    except ImportError:
        has_deps = False
    if has_deps:
        R = P("vk-reels", "skills", "mascot-reels")
        spec = json.load(open(os.path.join(R, "specs", "demo-carre-colis.json"), encoding="utf-8"))
        spec["scenes"] = spec["scenes"][:1]
        spec["scenes"][0]["dur"] = 1.5
        short = os.path.join(TMP, "reel-court.json")
        json.dump(spec, open(short, "w", encoding="utf-8"), ensure_ascii=False)
        run("rendu vidéo court", [os.path.join(R, "scripts", "reel_engine.py"), short, os.path.join(TMP, "reel"), "--no-audio"],
            expect=0, contains=["OK "])
        ok = all(os.path.exists(os.path.join(TMP, "reel", f)) for f in ("demo-carre-colis.mp4", "cover.jpg", "storyboard.png"))
        results.append((ok, "fichiers vidéo produits"))
        print(("✔" if ok else "✖"), "fichiers vidéo produits")
    else:
        print("– rendu vidéo ignoré (Pillow, numpy ou ffmpeg absent)")

shutil.rmtree(TMP, ignore_errors=True)
failed = [label for ok, label in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} cas réussis")
sys.exit(1 if failed else 0)
