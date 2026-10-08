---
name: social-publish
description: Publie et gère les réseaux sociaux d'une marque via l'API Zernio (Instagram, TikTok, Facebook, Pinterest, YouTube Shorts, LinkedIn), de l'asset brut au post programmé et vérifié — légendes par plateforme dans le ton de la marque, passe anti-IA obligatoire, conversion des médias, upload, validation, programmation, vérification, et automatisations commentaire → message privé. Gère le mode lot. À utiliser dès que l'utilisateur veut poster, publier, programmer ou planifier une vidéo, un carrousel, une story ou une épingle, répondre aux commentaires, ou parle d'Instagram, de réseaux sociaux, de calendrier de posts, de lot ou de Zernio. Publicité payante : ad-creative.
---

# Publication et gestion des réseaux sociaux (Zernio)

Tu publies via l'API REST Zernio, de bout en bout : asset → analyse → légendes → conversion → upload → validation → programmation → vérification → journal. L'utilisateur donne un asset et une intention ; tu fais le reste et tu lui présentes le paquet fini.

Workflow et références `reference/zernio/` repris de `zernio-library-skills` (MIT, Enrique Marquez). Passe anti-IA adaptée de `humanizer` (MIT, Siqi Chen). Contrôles de légende et d'accroche adaptés de `instagram-agent-skill` (MIT, Jake Schincariol). Voir `NOTICE`.

## Étape 0 — Charger le contexte de marque

Lis `brand-context.md` avant tout. Cherche-le dans cet ordre et arrête-toi au premier trouvé : `./brand/brand-context.md`, `./brand-context.md`, le dossier `VK_BRAND_DIR`, `/mnt/project/brand-context.md`. Offre, prix, ton, direction artistique, stack et règles viennent de là ; rien de tout cela n'est recopié dans ce skill.

Introuvable : propose le skill `setup` (plugin `vk-core`). Pour avancer sans attendre, pose au plus trois questions (offre, cible, ton) et marque dans le livrable ce qui reste à confirmer. Écris dans la langue et le registre du contexte. Si le contexte et le site divergent, le site gagne : signale l'écart.

## 0. Avant tout

1. **Lis `reference/voix-reseaux.md`** : la méthode de ton, de piliers, de liens et les règles légales. Les valeurs propres à la marque sont au contexte §11.
2. **Clé d'API Zernio** : demande-la une seule fois par conversation si elle n'est pas dans l'environnement. Garde-la dans une variable shell (`export ZERNIO_API_KEY=...`), ne la réaffiche jamais, ne l'écris jamais dans un fichier livré, un outil de notes ou une mémoire. Test :
   ```bash
   curl -s -o /dev/null -w "HTTP %{http_code}\n" -H "Authorization: Bearer $ZERNIO_API_KEY" https://zernio.com/api/v1/accounts
   ```
   200 : correct · 401 : clé fausse (une question à l'utilisateur) · autre : réseau ou service.
3. **Comptes connectés** : ne suppose jamais qu'un compte existe. Résous-les à chaque session :
   ```bash
   curl -s https://zernio.com/api/v1/accounts -H "Authorization: Bearer $ZERNIO_API_KEY" \
     | python3 -c "import sys,json;d=json.load(sys.stdin);d=d.get('accounts',d) if isinstance(d,dict) else d;[print(a.get('platform'),a.get('_id') or a.get('id'),a.get('username','')) for a in d]"
   ```
   Une plateforme absente se connecte dans le tableau de bord du service : c'est une action de l'utilisateur.

## 1. Plateformes et formats

Les plateformes actives et le rôle de chacune sont au contexte §11. **Décide, ne demande pas** le format quand la plateforme et l'asset le dictent (matrice complète : `reference/zernio/platforms.md`) :

| Asset | Instagram | TikTok | YouTube | Pinterest | Facebook | LinkedIn |
|---|---|---|---|---|---|---|
| Vidéo 9:16 | Reel | Vidéo | Short | Épingle vidéo + couverture | Reel | Vidéo native |
| Vidéo 16:9 | Recadrer en 9:16 | Recadrer en 9:16 | Vidéo classique | Épingle vidéo | Vidéo du fil | Vidéo native |
| Carrousel d'images | Carrousel (2 à 10) | Carrousel photo | Diaporama vidéo | Meilleure image en épingle | Multi-image | Document PDF |
| Image seule | Post 4:5 | Post photo | — | Épingle 2:3 | Post image | Post image |

## 2. Le workflow en dix étapes

**1. Réception.** Récupère l'asset sur disque (`./media/`) : fichier fourni, fichier de marque, lien public, stockage connecté. Vérifie les types avec `file`.

**2. Analyse.** Regarde chaque image. Pour une vidéo, transcris si un outil est disponible ; sinon extrais trois ou quatre images clés et décris-les. Repère l'accroche, ce qui est montré, le geste, le pilier éditorial. Pour un produit, relève les mentions de l'étiquette dans l'ordre de la hiérarchie d'information du contexte §5. N'invente rien que l'asset ou l'utilisateur ne dit pas.

**3. Rédaction.** Une légende par plateforme, jamais le même copier-coller : accroche en première ligne, registre du contexte, détails précis, un seul appel à l'action, lien avec UTM, hashtags selon la plateforme, premier commentaire là où il est pris en charge.

**Accroche** (`reference/accroches.md`) : écris trois versions de la première ligne (et du titre de couverture ou de la première scène), avec des formules différentes de celles des trois derniers posts, puis `python3 scripts/score_accroche.py accroches.txt --config brand/kit.config.json`. Garde la mieux notée qui passe aussi `check_anti_ia.py` sans FORT ; en cas de conflit, anti-ia gagne.

**3 bis. Passe anti-IA — obligatoire, avant toute présentation ou tout envoi.** Elle couvre **tout** le texte du post : légende, premier commentaire, texte des slides (donc le PDF qui en est tiré), titres et bulles d'une vidéo, texte incrusté. Un média dont le texte n'est pas passé par cette étape ne se programme pas.
1. relis les trois dernières légendes publiées ou programmées sur la même plateforme (`GET /v1/posts`) et évite leur squelette, leur première phrase type et leur chute ;
2. repère les tics (`reference/anti-ia.md`) et réécris le paragraphe entier, sans ajouter aucun fait ;
3. `python3 scripts/check_anti_ia.py --json posts.json --config brand/kit.config.json` (liste de `{id, platform, content, firstComment}`) : zéro « FORT » exigé, les « faible » se jugent à la relecture. Pour le texte d'un visuel, mets `platform: "visuel"` : les titres courts y sont normaux ;
4. `python3 scripts/check_legende.py --json posts.json --config brand/kit.config.json` : fenêtre visible avant « ... plus », nombre de hashtags, caractères invisibles (à retirer avec `--nettoie`), liens morts dans une légende Instagram, lien UTM sur LinkedIn, appels à l'action multiples, emojis, longueur. Zéro ÉCHEC exigé ; les ALERTES se jugent ;
5. test final : la personne qui tient le compte aurait-elle pu l'écrire elle-même ? Sinon, réécris.

En tâche planifiée sans relecteur, cette passe remplace la relecture : ne la saute jamais.

**4. Conversion** (ffmpeg, sans demander) :
```bash
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy -y out-9x16.mp4          # 16:9 → 9:16
ffmpeg -framerate 1/4 -i "slide_%02d.jpg" -c:v libx264 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" -pix_fmt yuv420p -r 30 -y slides.mp4  # carrousel → vidéo
ffmpeg -i in.jpg -vf "scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350" -q:v 2 -y feed-4x5.jpg   # fil 4:5
ffmpeg -i in.jpg -vf "scale=1000:1500:force_original_aspect_ratio=increase,crop=1000:1500" -q:v 2 -y pin-2x3.jpg    # épingle 2:3
ffmpeg -i video.mp4 -ss 00:00:03 -vframes 1 -q:v 2 -y cover.jpg                              # couverture (JPEG)
```
Regarde le résultat : un recadrage qui coupe le logo, le produit ou un visage se refait.

**5. Upload** (détails et cas des gros fichiers : `reference/zernio/zernio-upload.md`) :
```bash
PRESIGN=$(curl -s -X POST https://zernio.com/api/v1/media/presign -H "Authorization: Bearer $ZERNIO_API_KEY" -H "Content-Type: application/json" -d '{"filename":"reel.mp4","contentType":"video/mp4"}')
UPLOAD_URL=$(echo "$PRESIGN" | python3 -c "import sys,json;print(json.load(sys.stdin)['uploadUrl'])")
PUBLIC_URL=$(echo "$PRESIGN" | python3 -c "import sys,json;print(json.load(sys.stdin)['publicUrl'])")
curl -s -X PUT "$UPLOAD_URL" -H "Content-Type: video/mp4" -T ./media/reel.mp4 --tls-max 1.2 -o /dev/null -w "%{http_code}\n"
curl -s -o /dev/null -w "%{http_code}\n" -I "$PUBLIC_URL"   # doit valoir 200
```

**6. Paquet.** Corps de la requête : `reference/zernio/zernio-post.md`, modèle `templates/post-body.json`. Règles qui cassent un post en silence :
- `content` = légende de base ; les variantes vont dans `platforms[].customContent` ;
- `platformSpecificData` est **plat**, jamais imbriqué par plateforme ;
- `tags` = chaîne séparée par des virgules, jamais un tableau ;
- `mediaItems[].thumbnail` = URL en chaîne simple ;
- `firstComment` se met à la création, impossible à ajouter après ;
- une URL de média temporaire = un envoi ; si l'envoi échoue, ré-uploade ;
- **supprimer un post supprime aussi ses médias.** Pour réécrire un post : télécharge d'abord tous ses médias sous des noms uniques préfixés par l'identifiant du post, ré-uploade, crée le nouveau post, vérifie chaque média, et seulement ensuite supprime l'ancien ;
- `scheduledFor` en ISO 8601 avec fuseau. Les heures se discutent au fuseau du contexte et se convertissent, changement d'heure compris.

**7. Validation.** Montre tout le paquet d'un bloc, sans résumé :
```
## Prêt à publier — valide ou corrige
Plateformes : instagram, facebook
Programmé   : <date et heure locales> → <ISO 8601 UTC>
Média       : ./media/reel.mp4 → uploadé ✓   Couverture : ./media/cover.jpg → uploadée ✓

— Instagram (Reel) —
Légende : [texte intégral]
Hashtags : …
1er commentaire : …
Lien : https://…?utm_source=instagram&utm_medium=social&utm_campaign=…

— Facebook — …
Réponds « go », « publie » ou « valide » pour programmer, ou dis ce qu'il faut changer.
```
Seul un accord explicite vaut validation. Après une correction, remontre le bloc complet.

**8. Envoi.** `curl -s -X POST https://zernio.com/api/v1/posts -H "Authorization: Bearer $ZERNIO_API_KEY" -H "Content-Type: application/json" -d @post.json`. Récupère l'identifiant, le statut et l'URL par plateforme.

**9. Vérification** à `scheduledFor + 60 s` (nouvel essai à +120 s) : `GET /v1/posts/{id}`, requête HEAD sur l'URL publique de chaque plateforme. Nomme tout champ perdu (légende tronquée, couverture ignorée, premier commentaire absent) et propose la correction. Un post programmé loin dans le futur se vérifie plus tard : donne l'identifiant et la commande.

**10. Journal.** Donne dans la réponse le récapitulatif (date, plateformes, identifiants, statut). Si le projet tient un journal de publication (contexte §8), ajoute-y la ligne. Jamais de clé d'API dans le journal.

**Invariants** : passe anti-IA avant de montrer · validation avant publication · programmer plutôt que pousser (`scheduledFor` quelques minutes devant pour du multi-plateforme, des jours devant en lot ; jamais `publishNow: true` en multi) · vérifier après. Intériorise-les, ne les récite pas.

## 3. Mode lot

Rythme lu au contexte §11 (`social.cadence_days`, `social.default_time`). Par défaut : blocs de quatorze jours. Déclencheurs : « lot réseaux », « prépare les deux prochaines semaines », « planning du X au Y ».

1. **Bilan du lot précédent** si des identifiants sont fournis : statut de chaque post, liste de ce qui est publié, en échec ou tronqué. Un post en échec se reprogramme.
2. **Dates** : espacées de la cadence à partir du jour de départ, à l'heure retenue, converties en UTC.
3. **Rotation des piliers** (`reference/voix-reseaux.md` §4).
4. **Assets** : fournis par l'utilisateur. S'il en manque, propose lesquels réutiliser sous un autre angle ou lesquels créer, sans inventer de photo de produit.
5. **Déclinaison par asset** sur chaque plateforme active, avec des `customContent` différents ; un envoi séparé si le média diffère.
6. **Validation en un bloc** : tableau récapitulatif (date · pilier · sujet · visuel · lien), puis toutes les légendes. Pas de programmation partielle sans accord explicite.
7. **Programmation** dans l'ordre chronologique, puis vérification de chaque post.
8. **Récapitulatif final** à conserver : date · pilier · sujet · identifiants · statut. C'est ce que la session suivante utilisera pour le bilan.

**Autre voie : la file d'attente du service.** Chaque post est alors créé avec la file du profil et **sans** `scheduledFor`. Ne lis jamais le prochain créneau pour le recopier dans `scheduledFor` : cela contourne le verrouillage de la file.

## 4. Gestion : commentaire → message privé

Pour Instagram et Facebook. Recette : `reference/zernio/zernio-automations-api.md`, modèle `templates/automation.json`.

- Il faut le profil, le compte, l'identifiant du post, un mot-clé, le message privé et la réponse publique.
- Mots-clés : ceux du contexte §11. Un mot-clé par automatisation, en majuscules.
- Le message privé : registre du contexte, une phrase utile, le lien avec `utm_medium=dm`, puis une seule question. La réponse publique reste courte.
- Crée avec `isActive: false`, montre, active après accord.
- Suppression seulement sur demande explicite.

**Répondre aux commentaires et messages** : tu peux lire la boîte de réception et proposer des réponses. Tu n'envoies rien sans validation. Une réclamation ne se règle pas en public : réponse courte qui invite en message privé, sans promettre de condition que le contexte §3 n'autorise pas.

## 5. Ce que ce skill ne fait pas

- Publicité payante, boosts, audiences : `ad-creative` et `ads-audit`. Aucune dépense déclenchée d'ici.
- Emails : `email-flows`.
- Création de visuels : il publie des assets existants.
- Aucun achat d'abonnement, aucune connexion de compte à la place de l'utilisateur.

## 6. Références

| Fichier | Quand le lire |
|---|---|
| `reference/voix-reseaux.md` | Toujours, avant d'écrire |
| `reference/anti-ia.md` + `scripts/check_anti_ia.py` | Toujours, après le premier jet |
| `reference/accroches.md` + `scripts/score_accroche.py` | Avant la première ligne, le titre de couverture ou la première scène |
| `scripts/check_legende.py` | Après la passe anti-IA |
| `reference/humanizer/humanizer-original.md` | Version anglaise d'origine, en cas de doute sur un motif |
| `reference/zernio/platforms.md` + `platforms/{plateforme}.md` | Spécifications, limites, pièges d'une plateforme |
| `reference/zernio/zernio-post.md` | Forme exacte du corps de la requête |
| `reference/zernio/zernio-upload.md` | Upload, gros fichiers, erreurs |
| `reference/zernio/zernio-api.md` | Points d'accès, comptes, profils |
| `reference/zernio/principles.md` | Protocole de vérification, pratiques à éviter |
| `reference/zernio/zernio-automations-api.md` | Commentaire → message privé, boîte de réception |

Les fichiers de `reference/zernio/` viennent du dépôt d'origine, en anglais, et parlent de « zernio-publish » : cela désigne ce skill. La spécification OpenAPI officielle n'est pas redistribuée ici ; elle fait foi en cas de doute et se consulte sur https://docs.zernio.com/.

## Dépendances

| Connecteur | Avec | Sans |
|---|---|---|
| Clé d'API Zernio | upload, programmation, vérification, statistiques | étapes 1 à 4 et 7 seulement : le paquet est livré prêt à publier à la main |
| ffmpeg | conversions de formats | l'utilisateur fournit les médias au bon format |
| Stockage connecté | récupération directe des assets | fichiers joints à la conversation |

Un autre service de programmation peut remplacer Zernio : les étapes 1 à 4, 3 bis et 7 ne changent pas, seules les étapes 5, 6, 8 et 9 sont à réécrire pour son API.
