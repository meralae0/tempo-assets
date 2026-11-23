# BriefAI #10 — Taste Skill : même page demandée à Claude, sans / avec le skill

Statut (23/11 ~19:40 Maroc) : test fait, captures faites, script FR/EN + métadonnées prêts.
BLOQUÉ : voix (le conteneur ne peut pas récupérer l'audio d'AI Studio : dossier Téléchargements non connecté, pas de clé API Gemini côté conteneur). Rendu + programmation à faire dès que la voix est disponible.
Créneau visé : YouTube mar 24/11 (Short 1 13:00, long 17:00, Short 2 21:00) ; Facebook Reels 24/11 13:00 + 21:00, long 25/11 18:00. Mot-clé : TASTE.

## Le test (réel, 23/11)
- Même demande, mot pour mot : « page d'accueil d'un café de quartier fictif à Casablanca, Café Nour (café de spécialité, pâtisseries maison, ouvert 7h-20h, quartier Maârif), une seule page en français ».
- A = Claude sans skill · B = Claude avec Taste Skill 2.5.1 (Leonxlnx/taste-skill, licence MIT, skill « design-taste-frontend »).
- Pages : docs/briefai-10-taste/sans-skill/ et avec-skill/ · captures : episodes/briefai-10/caps/ (desktop 1440×900, mobile 390, défilement vidéo).
- Rendu des captures : Google Fonts et photos externes bloquées par le proxy du conteneur → servies en local (mêmes polices demandées ; pour A, les 6 photos Unsplash remplacées par les 3 photos de café du skill, pour que les deux pages aient les mêmes photos).

| Mesure (vérifiée) | Sans skill | Avec skill |
|---|---|---|
| Temps de génération | 2 min 16 s | 23 min 01 s |
| Tokens consommés (agent) | ~75 000 | ~185 000 (×2,5) |
| Hauteur page desktop | 6 184 px ≈ 7 écrans | 2 700 px = 3 écrans |
| Mots visibles | 670 | 165 |
| Faux avis client inventé | 1 (« Le meilleur flat white du Maârif… ») | 0 |
| Chiffre inventé mis en avant | « 100 % de nos pâtisseries faites sur place, dès 5h » | 0 |
| Vérification dans un vrai navigateur | non | oui (copy-lint, cohérence, captures, gate : 1 échec contraste restant sur mobile) |

Verdict honnête : le skill ne rend pas la page « plus jolie » d'office. La page sans skill a le look « IA » classique (grand titre serif avec italique doré, photo assombrie, badges, faux avis). Avec le skill : page courte, sobre, qui dit quoi et où, sans rien inventer — mais 10× plus lente et 2,5× plus chère en tokens. Pour un vrai commerce : avec. Pour une démo rapide : sans suffit.
Ce que la source annonce (« anti-slop », niveau figma.com / x.ai) : l'anti-slop est confirmé par le test (0 faux avis, 0 chiffre inventé) ; le niveau figma.com n'est pas atteint ici (photos de banque limitées à 3, page courte imposée).

## Script long FR (≈2 min 30, voix fr-fr-assistant-7, style en speechMetadata : « posé, complice, rythme rapide »)
[0:00 écran partagé A | B, gros texte « 2 min vs 23 min — laquelle n'est pas faite par une IA ? »]
1. Même demande, même Claude. À gauche, deux minutes. À droite, vingt-trois minutes, avec un skill qui fait le buzz sur GitHub : Taste Skill.
2. Sa promesse : fini les sites qui sentent l'IA. J'ai vérifié.
[demande tapée, zoom]
3. La demande : la page d'un café de quartier à Casablanca. Café Nour, pâtisseries maison, ouvert de sept heures à vingt heures.
[A hero zoom]
4. Sans skill, Claude livre en deux minutes seize. Grand titre avec un mot en italique doré, photo assombrie, petits badges. Joli… mais c'est exactement le look qu'on reconnaît en une seconde.
[A défilement, entourer l'avis]
5. Et en descendant : un avis client. « Le meilleur flat white du Maârif. » Ce client n'existe pas. Claude l'a inventé. Pareil pour « cent pour cent des pâtisseries faites dès cinq heures ».
[B hero zoom]
6. Avec le skill : vingt-trois minutes. Titre simple qui dit quoi et où. Une vraie photo de métier, pas de filtre.
[B terminal : checks]
7. Pourquoi si long ? Le skill ouvre la page dans un vrai navigateur, relit le texte, mesure les contrastes, et fait corriger. Il restait une seule erreur à la fin : un contraste sur mobile.
[comparatif longueur 7 écrans vs 3]
8. Résultat : trois écrans au lieu de sept. Cent soixante-cinq mots au lieu de six cent soixante-dix. Zéro avis inventé.
[compteur tokens]
9. Le prix : deux fois et demie plus de tokens, et dix fois plus de temps.
[verdict carte]
10. Mon verdict : il ne rend pas la page plus jolie d'office. Il la rend honnête. Pour un vrai commerce, je le garde. Pour une maquette rapide, pas besoin.
[installation, commande à l'écran]
11. Pour l'installer : une seule commande, npx skills add, puis le nom du dépôt. Il faut Node vingt-deux et Chrome. C'est gratuit.
[fin : retour sur l'écran partagé, coupe sèche]

## Script long EN (voix en-us-podcaster-7)
1. Same request, same Claude. Left: two minutes. Right: twenty-three minutes, with a skill that's blowing up on GitHub: Taste Skill.
2. Its promise: no more websites that scream "AI". I checked.
3. The request: a homepage for a neighborhood café in Casablanca. Café Nour, homemade pastries, open seven to eight.
4. Without the skill, Claude delivers in two minutes sixteen. Big serif headline with one gold italic word, darkened photo, little badges. Pretty… but it's the look you spot in one second.
5. Scroll down: a customer review. "The best flat white in Maârif." That customer doesn't exist. Claude made it up. Same for "one hundred percent of pastries baked from five a.m."
6. With the skill: twenty-three minutes. A plain headline that says what and where. A real trade photo, no filter.
7. Why so long? The skill opens the page in a real browser, rereads the copy, measures contrast, and forces fixes. One issue was left at the end: a contrast check on mobile.
8. Result: three screens instead of seven. One hundred sixty-five words instead of six hundred seventy. Zero fake reviews.
9. The cost: two and a half times the tokens, ten times the time.
10. My verdict: it doesn't make the page prettier by default. It makes it honest. For a real business, I keep it. For a quick mockup, you don't need it.
11. To install: one command, npx skills add, then the repo name. You need Node twenty-two and Chrome. It's free.

## Shorts 9:16 (30-40 s)
- Short 1 « Claude a inventé un client » (FR) / « Claude made up a customer » (EN) : 0-1 s avis entouré en rouge + « Ce client n'existe pas » → phrases 5, 4, 6, 8. Titre YT : « J'ai demandé un site à Claude… il a inventé un client 😳 #Shorts ».
- Short 2 « 2 min vs 23 min » : 0-1 s écran partagé + chronos → phrases 1, 7, 9, 10. Titre YT : « Le même site en 2 min ou en 23 min : lequel est fait par une IA ? #Shorts ».

## YouTube long
Titre FR : J'ai testé Taste Skill : le même site fait par Claude, sans et avec (2 min vs 23 min)
Titre EN : I Tested Taste Skill: Same Website by Claude, Without vs With (2 min vs 23 min)
Description FR :
Même demande, même Claude : la page d'un café fictif à Casablanca, sans skill puis avec Taste Skill 2.5 (skill gratuit, licence MIT, par Leonxlnx).
Résultats mesurés : 2 min 16 s vs 23 min · ~75 k vs ~185 k tokens · 7 écrans vs 3 · 1 faux avis client inventé sans skill, 0 avec.
Verdict : le skill ne rend pas la page plus jolie d'office, il la rend honnête et vérifiée dans un vrai navigateur.

▶ Installer le skill (Claude Code, Codex…) — Node 22+ et Chrome requis :
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
ou dans Claude Code : /plugin install taste-skill@taste-skill

▶ La demande utilisée (copie-la) :
Crée la page d'accueil d'un café de quartier à Casablanca nommé « Café Nour » (café de spécialité, pâtisseries maison, ouvert 7h-20h, quartier Maârif). Une seule page web en français. N'invente ni avis client, ni adresse, ni chiffre : marque ce qui est supposé.

Note : photos des deux pages identiques (bibliothèque Wikimedia Commons du skill) pour un test équitable.
Voix générée avec Gemini TTS (Google) ; test, montage et script réalisés avec Claude (Anthropic) ; vérifié par un humain.
#IA #Claude #SkillsClaude #WebDesign #ClaudeCode
Description EN : traduction fidèle de la description FR.

## Facebook
Reel 1 (24/11 13:00) : « J'ai demandé un site à Claude… il a inventé un client. 💬 Commente TASTE et je t'envoie la commande d'installation + la demande exacte en message privé. »
Reel 2 (24/11 21:00) : « 2 min sans skill, 23 min avec. Lequel tu gardes ? 💬 Commente TASTE et je t'envoie le skill en message privé. »
Long (25/11 18:00) : description FR ci-dessus + « 💬 Commente TASTE et je t'envoie la commande d'installation et la demande exacte en message privé ».
Automatisation Inbox > Automations > Comment to message, mot-clé TASTE : message privé = bloc « Installer le skill » + « La demande utilisée » ; réponse publique « C'est envoyé en message privé 📩 ».
