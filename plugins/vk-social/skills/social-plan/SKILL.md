---
name: social-plan
description: Audit hebdomadaire des posts publiés (données Zernio) puis plan de la semaine suivante — quel jour, quel format, quel contenu source, quelle formule d'accroche, quel angle par plateforme — écrit dans un document de consignes que la tâche de publication suit. Conçu pour tourner en tâche planifiée. À utiliser dès que l'utilisateur parle d'audit des réseaux, de ce qui marche sur Instagram ou LinkedIn, de statistiques de posts, de plan de la semaine, de calendrier éditorial, de « quoi poster », de cohérence ou d'ordre des publications, même sans dire « audit ».
---

# Audit et plan de la semaine sur les réseaux

Ce skill décide ; `social-publish` exécute. Il tourne une fois par semaine et produit un document de consignes que la tâche de publication lit avant chaque post.

Adapté de `ig-audit` et `ig-plan` (https://github.com/Jakeschincariol/instagram-agent-skill, MIT, (c) 2026 Jake Schincariol). Voir `NOTICE`.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 0. Avant tout

1. Lis, dans le skill `social-publish` : `reference/voix-reseaux.md` (piliers, cadence), `reference/accroches.md` (les 14 formules numérotées) et `reference/anti-ia.md`.
2. Clé d'API Zernio : même règle que `social-publish` §0, jamais réaffichée. Les identifiants de comptes sont dans `kit.config.json`, bloc `social.accounts`, ou se résolvent par `GET /v1/accounts`. JSON lu avec python3, un appel par seconde environ.
3. Dossier des consignes : `social.plan_folder` (stockage connecté ou dossier local).

## 1. Audit — sur les données du compte, pas sur des règles générales

```bash
curl -s "https://zernio.com/api/v1/analytics?accountId=<ID>&fromDate=<J-90>&limit=100" \
  -H "Authorization: Bearer $ZERNIO_API_KEY" -o an-instagram.json
python3 scripts/audit.py an-instagram.json [an-linkedin.json ...]
```

Ce qu'on regarde, dans cet ordre. Les vues brutes dépendent surtout du nombre d'abonnés : elles comptent peu.

| Mesure | Calcul | Ce qu'elle dit |
|---|---|---|
| Multiple | portée ÷ portée médiane du compte | vrai succès ou journée normale |
| Envois + enregistrements pour 100 de portée | (partages + enregistrements) × 100 ÷ portée | le signal le plus fort : quelqu'un a gardé ou transmis le post |
| Abonnés pour 100 de portée | nouveaux abonnés × 100 ÷ portée | le profil a-t-il converti l'attention |
| Taux d'engagement | fourni par l'API | secondaire |
| Complétion, durée moyenne (vidéos) | fournis par l'API s'ils ne sont pas nuls | le milieu de la vidéo tient-il |

Compare ensuite les cinq meilleurs et les cinq moins bons (moins s'il y a moins de posts) sur : format, sujet, pilier, formule d'accroche (lue dans les documents de consignes précédents), longueur. **Le jour et l'heure en dernier**, et seulement si rien d'autre ne ressort.

Règles d'honnêteté :
- **Moins de dix posts publiés sur une plateforme : on décrit, on ne conclut pas**, et on garde les règles par défaut. Le dire en une phrase.
- Chaque conclusion = une affirmation, les chiffres qui la portent, le nombre de posts (n).
- Beaucoup de portée hors abonnés mais peu d'abonnés gagnés : c'est un problème de profil ou de bio, pas d'accroche. Le signaler, ne pas réécrire les accroches pour ça.
- Posts en échec ou non publiés : les lister. C'est souvent le point le plus utile de l'audit.

## 2. Plan de la semaine

Fenêtre : les sept jours qui suivent la date du run.

1. **Dates** : un post tous les `social.cadence_days` jours. Pars du dernier post présent (publié, programmé ou brouillon) et ajoute la cadence. Une date déjà occupée n'est pas replanifiée : note-la « déjà programmé » avec son identifiant. Heure : `social.default_time` ; ne la change que si la recommandation de l'API s'appuie sur vingt posts publiés au moins, et dis-le.
2. **Format** : alternance stricte entre les formats que la marque produit, en partant de l'opposé du dernier post. Exception seulement si l'audit est fiable (dix posts ou plus), avec quatre posts au moins de chaque format et un écart d'au moins ×2 : deux fois de suite le format gagnant, jamais trois. Justifie dans `note`.
3. **Contenu source** : liste les contenus publiés du site (flux du blog, sitemap). Exclus ceux déjà traités dans un post et ceux déjà planifiés dans les consignes des quatre semaines précédentes. Jamais deux fois le même sujet d'affilée, trois sujets différents au moins sur la semaine. Vérifie que la page répond 200.
4. **Personnage** (si la marque en a, contexte §11) : attribué selon le sujet, pas deux fois de suite le même si le sujet le permet.
5. **Pilier** : rotation du contexte §11. Un post de conversion au plus par semaine.
6. **Formule d'accroche** : un numéro de `accroches.md` §3, différent pour chaque post de la semaine et des trois derniers posts. L'angle dit **quoi** raconter à partir d'un fait précis du contenu source, pas un thème.
7. **Angle par plateforme** : la variante propre à chaque réseau, jamais le copier-coller.
8. **Hashtags** : dans les plafonds de `social.hashtags_max`.
9. Passe `check_anti_ia.py` (platform `"visuel"`) sur les angles et les notes : ils seront recopiés dans les posts, donc pas de tic dès le plan.

## 3. Le document de consignes

Crée dans le dossier des consignes un document intitulé **« Consignes semaine du JJ/MM/AAAA »**. Un nouveau document chaque semaine : la tâche de publication lit toujours le plus récent.

Contenu, dans cet ordre :

1. `PLAN VALABLE DU AAAA-MM-JJ AU AAAA-MM-JJ` (première ligne, repère pour la tâche de publication).
2. Une ligne par date planifiée, champs séparés par « ; » :
```
CONSIGNE ; date=2026-10-11 ; heure=12:30 ; format=CARROUSEL ; source=<slug> ; sujet=<sujet> ; pilier=<pilier> ; personnage=<nom ou -> ; formule=<n° + nom> ; angle=<fait précis à mettre en avant> ; angle_linkedin=<variante> ; hashtags=<3 à 5> ; note=<justification courte ou ->
```
   Dates déjà occupées : `DÉJÀ PROGRAMMÉ ; date=... ; id=...`.
3. L'audit en clair : tableau de `audit.py`, conclusions avec n, posts en échec.
4. Deux contenus de réserve (`RÉSERVE ; source=<slug> ; sujet=...`).

Aucun caractère `;` à l'intérieur d'un champ. Pas de clé d'API dans le document.

L'utilisateur peut modifier une ligne à la main, ou remplacer « CONSIGNE » par « ANNULÉ ». La tâche de publication respecte ses changements.

## 4. Compte rendu

Envoie le compte rendu par le canal du contexte §9 (email à `social.report_email` si un connecteur de messagerie existe, sinon réponse du run) : le lien du document, le tableau de la semaine, les trois à cinq constats de l'audit avec leurs chiffres et n, les posts en échec, et la phrase qui explique comment modifier ou annuler une consigne. En cas d'échec d'un outil, envoie quand même le plan dans le corps, avec l'erreur exacte.

## 5. Ce que ce skill ne fait pas

Il ne crée aucun post, aucun brouillon, aucun upload, et ne supprime rien. Il ne modifie pas les tâches planifiées.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Clé d'API Zernio | audit sur les statistiques réelles | plan établi sur les règles par défaut, annoncé comme tel |
| Stockage connecté | document de consignes partagé | fichier local |
| Messagerie | compte rendu envoyé | compte rendu dans la réponse |
