#!/usr/bin/env python3
"""Contrôle de forme d'une légende (Instagram ou LinkedIn), en français.
Complète check_anti_ia.py (qui chasse les tics d'écriture) : ici on vérifie ce que
voit le lecteur avant le « ... plus », le nombre de hashtags, l'appel à l'action,
les liens, les emojis et les caractères invisibles.

Adapté de ig-caption/caption.py et ig-human/humanize.py
(https://github.com/Jakeschincariol/instagram-agent-skill, MIT, (c) 2026 Jake Schincariol).
Différence volontaire : les espaces insécables U+00A0 et U+202F sont GARDÉES
(typographie française avant : ; ! ? et dans « »).

Usage : python3 check_legende.py legende.txt [--plateforme instagram|linkedin] [--config brand/kit.config.json]
        python3 check_legende.py --json posts.json [--config ...]   (liste de {id, platform, content, firstComment})
        python3 check_legende.py legende.txt --nettoie legende-propre.txt   (retire les invisibles)

La configuration fournit le domaine de la marque (liens et UTM), les plafonds de hashtags
et le plafond d'emojis. Code retour 1 si un contrôle est en ÉCHEC."""
import argparse, json, re, sys, textwrap

FENETRE = 125           # caractères visibles dans le fil Instagram avant « ... plus »
FENETRE_LINKEDIN = 210  # environ, sur ordinateur, avant « ... voir plus »
MAX_HASHTAGS = {'instagram': 5, 'linkedin': 2}   # plafonds par défaut, surchargés par social.hashtags_max
MAX_EMOJIS = 1
HOST = ''                # domaine de la marque sans protocole, lu dans brand.domain
MOTS = {'instagram': (100, 170), 'linkedin': (100, 180)}

INVISIBLES = re.compile('[​‌‍⁠﻿­᠎؜‎‏⁡-⁤\U000E0000-\U000E007F]')
HASHTAG = re.compile(r'(?:^|\s)#[\wÀ-ÿ]+')
LIEN = re.compile(r'https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|fr|co|io)/\S*', re.I)
EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿]')
CTA = [  # (motif, étiquette)
    (r'\blien (en|dans (la|ma|notre)) bio\b|\bdans la bio\b|\bprofil\b.{0,20}\blien\b', 'lien en bio'),
    (r'\b(commente|écris|réponds)\b.{0,30}\b(en commentaire|en com|sous ce post)\b|\bcommente « ?[A-Z]{3,}', 'commentaire'),
    (r'\b(enregistre|sauvegarde|garde)[- ](le|la|ce|ces|les)\b', 'enregistrer'),
    (r'\b(envoie|écris)[- ]nous\b.{0,20}\b(dm|message|mp)\b|\ben (dm|mp|message privé)\b', 'DM'),
    (r'\b(abonne-toi|suis-nous)\b', "s'abonner"),
    (r'\b(réserve|commande|demande ton devis|demandez votre devis|prends rendez-vous|prenez rendez-vous)\b', 'action site'),
    (r'\b(le guide|le pdf|tout est|la suite est)\b.{0,40}\b(sur le site|en lien)\b', 'lien guide'),
]


def configure(path):
    """Charge le domaine, les plafonds de hashtags et d'emojis depuis kit.config.json."""
    global HOST, MAX_EMOJIS
    cfg = json.load(open(path, encoding='utf-8'))
    HOST = re.sub(r'^https?://(www\.)?', '', cfg.get('brand', {}).get('domain', '')).rstrip('/')
    MAX_HASHTAGS.update(cfg.get('social', {}).get('hashtags_max', {}))
    MAX_EMOJIS = cfg.get('voice', {}).get('max_emojis', 1)
CONCRET = re.compile(r'\d|\b(deux|trois|quatre|cinq|six|sept|huit|neuf|dix|douze|quinze|vingt|trente|cent|mille|moitié|double|triple)\b', re.I)
PROPRE = re.compile(r'(?<![.!?]\s)(?<!^)\b[A-ZÉÈÀÂÎÔÛ][a-zéèêëàâîïôûç]{2,}')


def nettoie(txt):
    return INVISIBLES.sub('', txt)


def boite(visible, coupe, out):
    lignes = []
    for para in visible.split('\n'):
        lignes += textwrap.wrap(para, 54) or ['']
    print('  CE QUE MONTRE LE FIL', file=out)
    print('  +' + '-' * 56 + '+', file=out)
    for l in lignes:
        print(f'  | {l:<54} |', file=out)
    print('  +' + '-' * (44 if coupe else 56) + (' ... plus +' if coupe else '+'), file=out)


def analyse(raw, plateforme='instagram', label='', out=sys.stdout):
    res = []
    add = lambda st, nom, det: res.append((st, nom, det))
    inv = INVISIBLES.findall(raw)
    txt = nettoie(raw).strip()
    add('ÉCHEC' if inv else 'OK', 'INVISIBLES',
        f'{len(inv)} caractère(s) invisible(s) : relance avec --nettoie' if inv else 'aucun caractère invisible')

    corps = '\n'.join(l for l in txt.split('\n') if not re.fullmatch(r'\s*(#[\wÀ-ÿ]+\s*)+', l))
    fen = FENETRE if plateforme == 'instagram' else FENETRE_LINKEDIN
    visible, coupe = corps[:fen], len(corps) > fen
    premiere = corps.split('\n')[0]
    if len(premiere) <= fen:
        add('OK', '1re LIGNE', f'{len(premiere)} caractères, entière avant la coupe ({fen})')
    else:
        add('ALERTE', '1re LIGNE', f'{len(premiere)} caractères : coupée à {fen}. Acceptable si la coupe tombe sur une question ouverte, pas au milieu d\'une subordonnée')
    marqueurs = CONCRET.findall(visible) + PROPRE.findall(visible)
    add('OK' if marqueurs else 'ALERTE', 'ACCROCHE CONCRÈTE',
        f'{len(marqueurs)} chiffre(s) ou nom(s) avant la coupe' if marqueurs else 'rien de vérifiable avant la coupe (ni chiffre, ni nom, ni lieu)')

    tags = [t.strip() for t in HASHTAG.findall(txt)]
    mx = MAX_HASHTAGS.get(plateforme, 5)
    if len(tags) > mx:
        add('ÉCHEC', 'HASHTAGS', f'{len(tags)} hashtags, maximum {mx} sur {plateforme}')
    else:
        add('OK', 'HASHTAGS', f'{len(tags)} : {" ".join(tags)}' if tags else '0 hashtag')
    if tags and plateforme == 'instagram':
        fin = txt.split('\n')[-1]
        dans_corps = [t for t in tags if t in corps]
        add('ALERTE' if dans_corps else 'OK', 'PLACE DES HASHTAGS',
            'hashtags au milieu du texte, mets-les sur la dernière ligne' if dans_corps else 'regroupés en fin de légende')

    liens = LIEN.findall(txt)
    if plateforme == 'instagram':
        add('ALERTE' if liens else 'OK', 'LIENS', f'{len(liens)} lien(s) : non cliquable(s) dans une légende Instagram, renvoie au lien en bio' if liens else 'aucun lien mort dans la légende')
    else:
        utm = [l for l in liens if (not HOST or HOST in l) and f'utm_source={plateforme}' in l]
        cible = f'lien {HOST or "du site"} avec utm_source={plateforme}'
        add('OK' if utm else 'ALERTE', 'LIEN UTM', cible if utm else 'pas de ' + cible)

    appels = {lab for pat, lab in CTA if re.search(pat, txt, re.I)}
    if HOST and re.search(rf'https?://(www\.)?{re.escape(HOST)}', txt, re.I):
        appels.add('lien cliquable')
    appels = sorted(appels)
    if len(appels) == 1 or (plateforme == 'linkedin' and 'lien cliquable' in appels and len(appels) <= 2):
        add('OK', 'UN SEUL APPEL', ', '.join(appels))
    elif not appels:
        add('ALERTE', 'UN SEUL APPEL', "aucun appel à l'action repéré : que doit faire le lecteur ?")
    else:
        add('ALERTE', 'UN SEUL APPEL', f"{len(appels)} appels ({', '.join(appels)}) : deux appels valent zéro")

    em = EMOJI.findall(txt)
    add('ALERTE' if len(em) > MAX_EMOJIS else 'OK', 'EMOJIS', f'{len(em)} ({MAX_EMOJIS} au plus)')

    n = len(re.sub(r'#\S+|https?://\S+', '', txt).split())
    lo, hi = MOTS.get(plateforme, (0, 10 ** 6))
    add('OK' if lo <= n <= hi else 'ALERTE', 'LONGUEUR', f'{n} mots (cible {lo}-{hi})')

    print(f'\n=== {label} [{plateforme}] {len(txt)} / 2200 caractères', file=out)
    boite(visible, coupe, out)
    for st, nom, det in res:
        print(f'  {st:<6} {nom:<19} {det}', file=out)
    ech = sum(1 for r in res if r[0] == 'ÉCHEC')
    al = sum(1 for r in res if r[0] == 'ALERTE')
    print(f'  VERDICT  {"À CORRIGER" if ech else ("À RELIRE" if al else "PRÊT")}', file=out)
    return ech


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichier', nargs='?')
    ap.add_argument('--plateforme', default='instagram', choices=['instagram', 'linkedin'])
    ap.add_argument('--json')
    ap.add_argument('--nettoie', metavar='SORTIE')
    ap.add_argument('--config')
    a = ap.parse_args()
    if a.config:
        configure(a.config)
    bad = 0
    if a.json:
        for p in json.load(open(a.json, encoding='utf-8')):
            pf = p.get('platform', 'instagram')
            if pf not in ('instagram', 'linkedin'):
                continue
            bad += analyse(p['content'], pf, p.get('id', ''))
            if p.get('firstComment') and INVISIBLES.search(p['firstComment']):
                print('  ÉCHEC  1er commentaire : caractères invisibles'); bad += 1
    elif a.fichier:
        raw = open(a.fichier, encoding='utf-8').read()
        if a.nettoie:
            open(a.nettoie, 'w', encoding='utf-8').write(nettoie(raw))
            print(f'{len(INVISIBLES.findall(raw))} caractère(s) invisible(s) retiré(s) -> {a.nettoie}')
            raw = nettoie(raw)
        bad += analyse(raw, a.plateforme, a.fichier)
    else:
        ap.print_help(); sys.exit(2)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
