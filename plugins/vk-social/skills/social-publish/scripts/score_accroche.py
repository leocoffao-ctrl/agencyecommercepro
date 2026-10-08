#!/usr/bin/env python3
"""Note une accroche (1re ligne de légende, titre de couverture de carrousel, titre de vidéo)
sur 5 critères, et classe plusieurs versions entre elles. Motifs livrés pour le français.

Adapté de ig-reel/hookscore.py
(https://github.com/Jakeschincariol/instagram-agent-skill, MIT, (c) 2026 Jake Schincariol).

Ce que ça fait : repérer les accroches creuses (salutation, préambule, rien de concret,
trop longue à lire, personne à qui parler). Ce que ça ne fait pas : prédire les vues.
L'original distingue bien une vraie accroche d'une mauvaise, mais presque pas deux
accroches correctes entre elles. Entre deux versions à plus de 70, choisis à la relecture.

Une accroche bien notée doit AUSSI passer check_anti_ia.py : deux fragments en miroir
font un bon score ici et un FORT là-bas.

Usage : python3 score_accroche.py accroches.txt [--config brand/kit.config.json]   (une par ligne, classées)
        python3 score_accroche.py --accroche "Arrête de laver ton plan de travail à grande eau."
Le registre (tu ou vous) est lu dans brand.register ; tutoiement par défaut.
Code retour 1 si la meilleure accroche est sous 55."""
import argparse, re, sys

MOT = re.compile(r"[\wÀ-ÿ$%€°'’-]+")
CHIFFRE = re.compile(r"\d[\d  .,]*\s?(%|€|g|kg|ml|cl|l|°c|°|s|sec|min|h|ans?|jours?|mois|m)?\b", re.I)
NOMBRES = {'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze',
           'quinze', 'vingt', 'trente', 'quarante', 'cinquante', 'cent', 'mille', 'moitié', 'double',
           'triple', 'zéro', 'demi'}
PROPRE = re.compile(r"(?<!^)\b[A-ZÉÈÀÂÎÔÛ][a-zéèêëàâîïôûç]{2,}")
ENJEU = {'jamais', 'rien', 'erreur', 'erreurs', 'faux', 'fausse', 'trop', 'perdu', 'perd', 'perds', 'rate',
         'raté', 'arrête', 'oublie', 'évite', 'abîme', 'abîmé', 'gâche', 'casse', 'cassé', 'usé',
         'sans', 'avant', 'seul', 'seule', 'déjà', 'encore', 'personne', 'aucun', 'aucune', 'interdit',
         'cher', 'coûte', 'gratuit', 'mythe', 'idée', 'reçue', 'piège', 'mauvais', 'mauvaise', 'pire',
         'meilleur', 'différence', 'pourquoi', 'vieux', 'périmé', 'moins', 'plus', 'pas', 'ne', "n'"}
FAIBLES = ['alors', 'bon', 'bonjour', 'coucou', 'hello', 'salut à', 'aujourd', 'nouveau', 'petit', 'vous',
           'est-ce', 'il y a', 'c\'est', 'voici', 'on va', 'dans cette', 'dans ce', 'je voulais', 'on voulait',
           'en ce moment', 'saviez', 'tu savais']
IMPERATIFS = {'arrête', 'oublie', 'essaie', 'regarde', 'garde', 'teste', 'range', 'lis', 'compare', 'évite',
              'prends', 'fais', 'change', 'mesure', 'vérifie', 'choisis',
              'arrêtez', 'oubliez', 'essayez', 'regardez', 'gardez', 'testez', 'comparez', 'évitez',
              'prenez', 'faites', 'changez', 'mesurez', 'vérifiez', 'choisissez'}
REGISTRE = 'tu'
REDHIBITOIRES = [
    (re.compile(r"(?i)^\s*(arrête de scroller|stop scroll|ne scrolle pas)"), 'Demande l\'attention au lieu de la gagner.'),
    (re.compile(r"(?i)\b(dans cette vidéo|dans ce post|aujourd'hui on va|je vais te montrer|on va voir)\b"), 'Préambule : ouvre directement sur le fond.'),
    (re.compile(r"(?i)^\s*(bonjour|coucou|hello|salut à tous|salut tout le monde)\b"), 'Salutation : personne ne vient sur le fil pour être salué.'),
    (re.compile(r"(?i)\bnouveau post\b"), 'Annonce le post au lieu de dire quelque chose.'),
    (re.compile(r"(?i)^\s*(vous connaissez|tu connais)\b"), 'Question creuse en ouverture.'),
    (re.compile(r"(?:^|\s)#\w+"), 'Hashtag dans l\'accroche.'),
    (re.compile('[\U0001F300-\U0001FAFF☀-➿]'), 'Emoji dans l\'accroche.'),
]

borne = lambda n: max(0.0, min(100.0, n))
mots = lambda t: MOT.findall(t)


def longueur(t):
    n, c = len(mots(t)), len(t.strip())
    s = 100 if 5 <= n <= 12 else (100 - (5 - n) * 20 if n < 5 else 100 - (n - 12) * 11)
    if c > 60: s -= 12
    return borne(s), f'{n} mots, {c} caractères, ~{n / 3.3:.1f} s à lire (cible 5-12 mots)'


def concret(t):
    ch = [m.group(0).strip() for m in CHIFFRE.finditer(t)]
    pr = PROPRE.findall(t)
    nb = [w for w in (x.lower() for x in mots(t)) if w in NOMBRES]
    h = len(ch) + len(set(pr)) + len(nb)
    return (15.0 if not h else borne(45 + 30 * h)), (f'{h} marqueur(s) : ' + ', '.join((ch + pr + nb)[:4]) if h else 'ni chiffre, ni nom, ni lieu')


def enjeu(t):
    w = {x.lower().strip("'’") for x in mots(t)} | ({"n'"} if re.search(r"\bn['’]", t) else set())
    h = sorted(w & ENJEU)
    if t.strip().endswith('?'): h.append('question')
    return {0: 20.0, 1: 70.0}.get(len(h), 100.0), (f'{len(h)} tension(s) : ' + ', '.join(h[:4]) if h else 'rien en jeu pour le lecteur')


def devant(t):
    w = mots(t)
    if not w: return 0.0, 'vide'
    low = [x.lower() for x in w]
    deb = ' '.join(low[:2])
    pen, faible = 0, next((f for f in FAIBLES if deb.startswith(f)), None)
    if faible: pen = 30
    pos = next((i for i, x in enumerate(low) if x.strip("'’") in ENJEU or x in NOMBRES or CHIFFRE.match(w[i]) or (i and PROPRE.match(w[i]))), None)
    if pos is None: b, o = 30.0, "aucun mot fort dans la ligne"
    elif pos <= 3: b, o = 100.0, f'mot fort en position {pos + 1}'
    elif pos <= 6: b, o = 70.0, f'mot fort en position {pos + 1}, à avancer'
    else: b, o = 40.0, f'mot fort en position {pos + 1}, trop tard'
    return borne(b - pen), o + (f' ; ouverture faible « {faible} »' if faible else '')


def adresse(t):
    low = t.lower(); w = [x.lower() for x in mots(t)]
    tu = re.search(r"\b(tu|ton|ta|tes|toi|te)\b|\bt['’]", low)
    vous = re.search(r"\b(vous|votre|vos)\b", low)
    attendu, autre = (tu, vous) if REGISTRE == 'tu' else (vous, tu)
    if attendu: return 100.0, f'parle au lecteur ({"tutoiement" if REGISTRE == "tu" else "vouvoiement"})'
    if w and w[0] in IMPERATIFS: return 90.0, f'impératif en tête (« {w[0]} »)'
    if autre: return 50.0, f'registre contraire au contexte de marque (attendu : {REGISTRE})'
    if re.search(r"\b(on|nous|je|j['’]|notre|mon)\b", low): return 70.0, 'première personne, lecteur absent'
    return 35.0, 'troisième personne, personne dans la pièce'


CRITERES = [('LONGUEUR', longueur), ('CONCRET', concret), ('ENJEU', enjeu), ('DEVANT', devant), ('ADRESSE', adresse)]


def note(t):
    r = {k: f(t) for k, f in CRITERES}
    s = [v[0] for v in r.values()]
    total = 0.6 * sum(s) / len(s) + 0.4 * min(s)
    red = [m for p, m in REDHIBITOIRES if p.search(t)]
    if red: total = min(total, 40.0)
    return round(total, 1), r, red


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichier', nargs='?')
    ap.add_argument('--accroche')
    ap.add_argument('--config')
    a = ap.parse_args()
    if a.config:
        import json
        global REGISTRE
        REGISTRE = json.load(open(a.config, encoding='utf-8')).get('brand', {}).get('register', 'tu')
    lst = [a.accroche] if a.accroche else [l.strip() for l in (sys.stdin if a.fichier in (None, '-') else open(a.fichier, encoding='utf-8')) if l.strip()]
    res = sorted(((note(t), t) for t in lst), key=lambda x: -x[0][0])
    print('\nCLASSEMENT DES ACCROCHES\n' + '=' * 72)
    for i, ((tot, r, red), t) in enumerate(res):
        verdict = 'FORTE' if tot >= 70 else ('CORRECTE' if tot >= 55 else 'FAIBLE')
        pire = min(r, key=lambda k: r[k][0])
        print(f"{'->' if i == 0 else '  '} {tot:5.1f} {verdict:<8} {t[:62]}")
        print(f'        point faible : {pire} ({r[pire][0]:.0f}) {r[pire][1]}')
        for m in red: print(f'        rédhibitoire : {m}')
    print('-' * 72 + '\nRappel : relance check_anti_ia.py sur l\'accroche retenue.')
    sys.exit(0 if res and res[0][0][0] >= 55 else 1)


if __name__ == '__main__':
    main()
