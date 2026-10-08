#!/usr/bin/env python3
"""Contrôle mécanique des tics d'écriture IA dans un texte court (légende, slide, bulle).

Usage : python3 check_anti_ia.py fichier.txt [...] [--config brand/kit.config.json]
        python3 check_anti_ia.py --json posts.json [--config brand/kit.config.json]
        (posts.json : liste de {id, platform, content, firstComment})

Les motifs livrés sont ceux du français. Les mots bannis propres à la marque viennent de
voice.banned_words dans la configuration. Ne remplace pas la relecture : voir reference/anti-ia.md.
Code retour 1 si un tic fort est trouvé.

Adaptation française du skill humanizer de Siqi Chen (https://github.com/blader/humanizer, MIT)."""
import re, sys, json

FORT = [  # (motif, explication) : un seul cas justifie une réécriture
    (r"[—–]|\s--\s", "tiret cadratin / demi-cadratin (§8)"),
    (r"\b(ce n'est pas|c'est pas|ça n'est pas|ce ne sont pas)\b[^.!?\n]{0,80}[,;:.]\s*(c'est|ce sont|mais)\b", "« ce n'est pas X, c'est Y » (§1)"),
    (r"\bpas (seulement|juste|uniquement)\b[^.!?\n]{0,80}\bmais\b", "« pas seulement X, mais Y » (§1)"),
    (r"\bbien plus que\b", "« bien plus que » (§1)"),
    (r"\b(ne|n')\s*\w+\s+pas plus\b[^.!?\n]{0,40},\s*(ils|elles|on|tu|il|elle)\b", "contraste « ne … pas plus, ils … » (§1)"),
    (r"\b(au fond|en réalité|en vrai|ce qui compte vraiment|le vrai sujet|le chiffre qui compte|le plus parlant)\b", "formule qui fait profond (§3)"),
    (r"^(le détail qui \w+|petit bonus|bonus|spoiler|voilà le truc|ce qui aide vraiment|autre point|on t'explique|honnêtement \?)\b", "élan avant le point (§4)"),
    (r"\b(le détail qui surprend|petit bonus|ça vaut le coup de savoir|rarement dit)\b", "élan avant le point (§4)"),
    (r"\b(pas de panique|on ne va pas se mentir|soyons honnêtes)\b", "répondre à personne (§5)"),
    (r"\b(incroyable|révolutionnaire|game changer|savoir-faire unique)\b", "superlatif creux"),
    (r"\b(plonge(z)? dans (l'univers|le monde|l'histoire)|voyage sensoriel|pépite|sublimer?|dans un monde où|n'hésite(z)? pas)\b", "vocabulaire d'IA (§11, §19)"),
    (r"\b(nouveau post)\b", "accroche interdite"),
]
FAIBLE = [
    (r"\b(crucial|essentiel|incontournable|véritable|au cœur de|subtil|mettre en lumière|souligne|témoigne|s'inscrit|typiquement|parfait équilibre)\w*", "vocabulaire d'IA, faible seul (§11)"),
    (r"\b(se positionne comme|constitue|s'impose comme)\b", "verbe détourné (§16)"),
    (r", (garantissant|offrant|permettant|soulignant|reflétant)\b", "participe décoratif (§13)"),
    (r"\b(découvre(z)?|explore(z)?)\b", "verbe passe-partout, faible seul (§11)"),
    (r"\b(glisse)\b", "« Glisse… » : varier d'un post à l'autre (§10)"),
    (r"\b(le guide complet est)\b", "CTA identique aux autres posts (§10)"),
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
BANNED, MAX_EMOJIS = [], 1

def load_config(path):
    """Ajoute les mots bannis et le plafond d'emojis du contexte de marque."""
    global BANNED, MAX_EMOJIS
    voice = json.load(open(path, encoding='utf-8')).get('voice', {})
    BANNED = voice.get('banned_words', [])
    MAX_EMOJIS = voice.get('max_emojis', 1)

def check(txt, label='', visuel=False):
    fort, faible = [], []
    body = re.sub(r"https?://\S+", "", txt)
    for line in body.split('\n'):
        l = line.strip()
        for pat, why in FORT:
            if re.search(pat, l, re.I | re.M): fort.append(f"{why} :: {l[:90]}")
        for pat, why in FAIBLE:
            if re.search(pat, l, re.I): faible.append(f"{why} :: {l[:90]}")
        for w in BANNED:
            if re.search(rf"(?<![\w-]){re.escape(w)}(?![\w-])", l, re.I): fort.append(f"mot banni par le contexte de marque « {w} » :: {l[:90]}")
    paras = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    frag = [p for p in paras if len(p.split()) <= 6 and not p.endswith('?')]
    if len(frag) >= 2 and not visuel: faible.append(f"{len(frag)} paragraphes-fragments (§2) : {frag[:3]}")
    n_emoji = len(EMOJI.findall(body))
    if n_emoji > MAX_EMOJIS: faible.append(f"{n_emoji} emojis ({MAX_EMOJIS} au plus, §17)")
    words = len(re.sub(r"#\S+", "", body).split())
    fort, faible = list(dict.fromkeys(fort)), list(dict.fromkeys(faible))
    print(f"--- {label} ({words} mots) : {len(fort)} fort, {len(faible)} faible")
    for x in fort: print("  FORT  ", x)
    for x in faible: print("  faible", x)
    return len(fort)

if __name__ == '__main__':
    a = sys.argv[1:]; bad = 0
    if '--config' in a:
        i = a.index('--config'); load_config(a[i + 1]); del a[i:i + 2]
    if not a:
        print(__doc__); sys.exit(2)
    if a[0] == '--json':
        for p in json.load(open(a[1], encoding='utf-8')):
            bad += check(p['content'], f"{p.get('id','')} {p.get('platform','')}", visuel=p.get('platform') in ('visuel','slides','reel'))
            if p.get('firstComment'): bad += check(p['firstComment'], '  1er commentaire')
    else:
        for f in a: bad += check(open(f, encoding='utf-8').read(), f)
    sys.exit(1 if bad else 0)
