#!/usr/bin/env python3
"""Audit des posts publiés à partir de l'API Zernio (GET /v1/analytics).
Adapté de ig-audit (https://github.com/Jakeschincariol/instagram-agent-skill,
MIT, (c) 2026 Jake Schincariol) : on classe par multiple de portée et par partages +
enregistrements, pas par vues.

Usage : python3 audit.py analytics-instagram.json [analytics-linkedin.json ...] [--json]
  (fichiers = réponses brutes de GET /v1/analytics?accountId=...&fromDate=...&limit=100)
Imprime, par plateforme : médiane, tableau classé, moyennes par format, et l'avertissement
d'échantillon. N'invente aucune conclusion : c'est à toi de lire le tableau."""
import json, statistics, sys

def charge(fichiers):
    posts = []
    for f in fichiers:
        d = json.load(open(f, encoding='utf-8'))
        for p in d.get('posts', []):
            if p.get('status') != 'published':
                continue
            a = p.get('analytics') or {}
            reach = a.get('reach') or 0
            first = (p.get('content') or '').strip().split('\n')[0]
            posts.append(dict(
                id=p.get('_id'), zernio=p.get('latePostId'), plateforme=p.get('platform'),
                date=(p.get('publishedAt') or '')[:10], heure=(p.get('publishedAt') or '')[11:16],
                format=p.get('mediaType') or '?', url=p.get('platformPostUrl'),
                accroche=first[:90], portee=reach, vues=a.get('views') or a.get('impressions') or 0,
                likes=a.get('likes') or 0, coms=a.get('comments') or 0, partages=a.get('shares') or 0,
                enreg=a.get('saves') or 0, abonnes=a.get('follows') or 0, clics=a.get('websiteClicks') or a.get('clicks') or 0,
                visites_profil=a.get('profileViews') or 0, taux=a.get('engagementRate') or 0,
                completion=a.get('completionRate') or 0, duree_moy=a.get('igReelsAvgWatchTime') or 0))
    return posts

def pour100(x, r): return round(100 * x / r, 1) if r else 0.0

def audit(posts):
    out = {}
    for pf in sorted({p['plateforme'] for p in posts}):
        ps = [p for p in posts if p['plateforme'] == pf]
        med = statistics.median([p['portee'] for p in ps]) if ps else 0
        for p in ps:
            p['multiple'] = round(p['portee'] / med, 2) if med else 0
            p['envois_enreg_100'] = pour100(p['partages'] + p['enreg'], p['portee'])
            p['abonnes_100'] = pour100(p['abonnes'], p['portee'])
        ps.sort(key=lambda p: (-p['multiple'], -p['envois_enreg_100']))
        fmts = {}
        for p in ps:
            fmts.setdefault(p['format'], []).append(p)
        par_format = {f: dict(n=len(l), multiple_moy=round(statistics.mean(x['multiple'] for x in l), 2),
                              envois_enreg_100=round(statistics.mean(x['envois_enreg_100'] for x in l), 1)) for f, l in fmts.items()}
        out[pf] = dict(n=len(ps), mediane_portee=med, posts=ps, par_format=par_format,
                       fiable=len(ps) >= 10,
                       avertissement=None if len(ps) >= 10 else f"{len(ps)} post(s) publié(s) : trop peu pour conclure (il en faut au moins 10). On décrit, on ne tranche pas.")
    return out

def affiche(res):
    for pf, r in res.items():
        print(f"\nAUDIT {pf.upper()}  ·  {r['n']} posts publiés  ·  portée médiane {r['mediane_portee']}")
        if r['avertissement']: print('  ! ' + r['avertissement'])
        print(f"  {'mult':>5} {'portée':>6} {'env+enr/100':>11} {'abo/100':>7} {'taux%':>6}  date        format    accroche")
        for p in r['posts']:
            print(f"  {p['multiple']:>5} {p['portee']:>6} {p['envois_enreg_100']:>11} {p['abonnes_100']:>7} {p['taux']:>6}  {p['date']}  {p['format']:<9} {p['accroche'][:60]}")
        print('  Par format : ' + ' · '.join(f"{f} n={v['n']} mult={v['multiple_moy']} env+enr/100={v['envois_enreg_100']}" for f, v in r['par_format'].items()))

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if x != '--json']
    res = audit(charge(a))
    if '--json' in sys.argv: print(json.dumps(res, ensure_ascii=False, indent=1))
    else: affiche(res)
