#!/usr/bin/env python3
"""Contrôles de cohérence du dépôt. Code de sortie 1 à la première famille d'erreurs.

  python3 scripts/lint_repo.py

Vérifie :
  1. marketplace.json et chaque plugin.json (JSON valide, noms alignés, dossier présent) ;
  2. chaque SKILL.md (en-tête name + description, nom = dossier, bloc de contexte) ;
  3. tous les fichiers JSON du dépôt ;
  4. les copies de modules partagés, qui doivent rester identiques ;
  5. l'absence de traces du projet d'origine, d'identifiants et de secrets dans plugins/ et examples/ ;
  6. la compilation de chaque script Python.
"""
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []


def err(msg):
    errors.append(msg)


def walk(top, exts=None):
    for base, dirs, files in os.walk(os.path.join(ROOT, top)):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "fonts", "_tmp")]
        for f in files:
            if exts is None or f.endswith(exts):
                yield os.path.join(base, f)


def rel(p):
    return os.path.relpath(p, ROOT)


# 1. Manifestes
mk_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
market = json.load(open(mk_path, encoding="utf-8"))
for key in ("name", "owner", "plugins"):
    if key not in market:
        err(f"marketplace.json : champ {key} manquant")
entries = {}
for entry in market.get("plugins", []):
    name, source = entry.get("name"), entry.get("source", "")
    entries[name] = source
    if ".." in source:
        err(f"marketplace.json : chemin avec « .. » pour {name}")
    pj = os.path.join(ROOT, source, ".claude-plugin", "plugin.json")
    if not os.path.exists(pj):
        err(f"{name} : plugin.json introuvable ({source})")
        continue
    manifest = json.load(open(pj, encoding="utf-8"))
    if manifest.get("name") != name:
        err(f"{name} : nom du manifeste différent ({manifest.get('name')})")
    if not os.path.isdir(os.path.join(ROOT, source, "skills")):
        err(f"{name} : dossier skills/ absent")
for d in sorted(os.listdir(os.path.join(ROOT, "plugins"))):
    if d not in entries:
        err(f"plugins/{d} n'est pas déclaré dans marketplace.json")

# 2. Skills
CONTEXT_MARK = "brand-context.md"
skills = []
for path in walk("plugins", ("SKILL.md",)):
    src = open(path, encoding="utf-8").read()
    folder = os.path.basename(os.path.dirname(path))
    m = re.match(r"---\n(.*?)\n---\n", src, re.S)
    if not m:
        err(f"{rel(path)} : en-tête YAML absent")
        continue
    head = m.group(1)
    name = re.search(r"^name:\s*\"?([\w-]+)\"?\s*$", head, re.M)
    desc = re.search(r"^description:\s*(.+)$", head, re.M)
    if not name or name.group(1) != folder:
        err(f"{rel(path)} : name doit valoir « {folder} »")
    if not desc or len(desc.group(1)) < 80:
        err(f"{rel(path)} : description absente ou trop courte pour déclencher le skill")
    elif len(desc.group(1)) > 1024:
        err(f"{rel(path)} : description de plus de 1024 caractères")
    if CONTEXT_MARK not in src:
        err(f"{rel(path)} : aucun renvoi au contexte de marque")
    if "<!--" in src:
        err(f"{rel(path)} : marqueur de gabarit non remplacé")
    for ref in re.findall(r"`((?:scripts|references|reference|assets|templates|themes|specs)/[\w./<>{}*-]+)`", src):
        if any(ch in ref for ch in "<>{}*"):
            continue
        here = os.path.exists(os.path.join(os.path.dirname(path), ref))
        elsewhere = glob.glob(os.path.join(ROOT, "plugins", "*", "skills", "*", ref))  # fichier d'un autre skill du kit
        if not here and not elsewhere:
            err(f"{rel(path)} : fichier cité introuvable ({ref})")
    skills.append(folder)
if len(skills) != len(set(skills)):
    err("deux skills portent le même nom")

# 3. JSON
for path in walk(".", (".json",)):
    try:
        json.load(open(path, encoding="utf-8"))
    except Exception as exc:
        err(f"{rel(path)} : JSON invalide ({exc})")

# 4. Copies synchronisées
SYNCED = [("plugins/vk-seo/skills/seo-writer/scripts/article_checks.py",
           "plugins/vk-content/skills/blog-pipeline/scripts/article_checks.py")]
for a, b in SYNCED:
    ha, hb = (hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest() for p in (a, b))
    if ha != hb:
        err(f"copies désynchronisées : {a} et {b}")

# 5. Fuites : projet d'origine, identifiants, secrets
LEAKS = [
    (r"coffao", "nom du projet d'origine"),
    (r"\bL[ée]o\b|\bMathis\b", "prénom d'une personne du projet d'origine"),
    (r"\b[0-9a-f]{24}\b", "identifiant de compte (24 caractères hexadécimaux)"),
    (r"\b1[A-Za-z0-9_-]{32,43}\b", "identifiant de fichier ou de dossier de stockage"),
    (r"gid://shopify/\w+/\d{6,}", "identifiant Shopify"),
    (r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", "identifiant de base"),
    (r"[\w.+-]+@(gmail|outlook|yahoo|hotmail)\.\w+", "adresse e-mail personnelle"),
    (r"\bFR\d{11}\b|\bRCS\s+\w+\s+\d{3}", "identifiant légal d'entreprise"),
    (r"(sk|pk|rk)_(live|test)_[A-Za-z0-9]{10,}|Bearer\s+[A-Za-z0-9_-]{24,}|AKIA[0-9A-Z]{16}", "clé ou jeton"),
]
SKIP_LEAK = ("reference/humanizer/", "LICENSE", "NOTICE")
# Fichiers repris tels quels d'un projet tiers, ou manifestes qui portent le nom de l'auteur :
# seul le nom du projet d'origine y est recherché.
NAME_ONLY = ("reference/zernio/", ".claude-plugin/")
for top in ("plugins", "examples", "tests"):
    for path in walk(top, (".md", ".json", ".py", ".css", ".html", ".txt", ".yaml", ".yml")):
        if any(s in rel(path) for s in SKIP_LEAK):
            continue
        src = open(path, encoding="utf-8", errors="replace").read()
        name_only = any(s in rel(path) for s in NAME_ONLY)
        for pattern, label in LEAKS:
            if name_only and not label.startswith("nom du projet"):
                continue
            flags = re.I if label.startswith("nom du projet") else 0
            hit = re.search(pattern, src, flags)
            if hit:
                err(f"{rel(path)} : {label} → « {hit.group(0)[:40]} »")

# 6. Scripts Python
for path in walk(".", (".py",)):
    try:
        compile(open(path, encoding="utf-8").read(), path, "exec")
    except SyntaxError as exc:
        err(f"{rel(path)} : ne compile pas (ligne {exc.lineno} : {exc.msg})")

print(f"{len(entries)} plugins, {len(skills)} skills contrôlés")
if errors:
    for e in errors:
        print("✖", e)
    print(f"\n{len(errors)} erreur(s)")
    sys.exit(1)
print("✔ dépôt cohérent")
