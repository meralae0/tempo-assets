# BriefAI #11 — Skill « caveman » : −65 % de tokens ? (test fait le 23/11 ~23:15 Maroc)

Statut : test réel fait, chiffres vérifiés. Reste : script final, voix, rendu, mise en ligne (bloqués par la voix, comme #10). Mot-clé : CAVEMAN.

## Le test
- Skill : JuliusBrussee/caveman v4.2.0 (commit b89752f, Apache-2.0), fichier skills/caveman/SKILL.md (copie : episodes/briefai-11/caveman-SKILL.md).
- 6 questions de la vie courante en français (episodes/briefai-11/questions.md) : formule Excel, batterie Android, prêt taux fixe/variable, supprimer un dossier Linux, erreur 404, recette de pâtes.
- A = Claude normal · B = Claude avec le skill caveman. 2 sous-agents lancés en parallèle, mêmes questions, sans outil.
- Comptage : tokenizer o200k (gpt-tokenizer), script episodes/briefai-11/count_tokens.js.

| Question | Normal | Caveman | Gain |
|---|---|---|---|
| Q1 Excel SOMME.SI | 231 | 66 | −71 % |
| Q2 batterie | 442 | 181 | −59 % |
| Q3 prêt | 373 | 151 | −60 % |
| Q4 supprimer dossier | 323 | 161 | −50 % |
| Q5 erreur 404 | 474 | 168 | −65 % |
| Q6 recette | 396 | 246 | −38 % |
| **Total** | **2 239** | **973** | **−57 %** |
Mots : 1 402 → 609.

## Constats (vérifiés)
- La promesse « −65 % » n'est atteinte que sur 1 question sur 6 (Q5) ; moyenne −57 %, de −38 % (recette) à −71 % (formule Excel).
- Le skill lui-même pèse 1 158 tokens, chargés à chaque session : sur ces 6 questions il économise 1 266 tokens de réponse → gain net ≈ 108 tokens seulement. Total des deux sessions mesuré par le harnais : 62 591 (normal) vs 62 603 (caveman), soit pareil.
- Raté / perte : sur la suppression de dossier (Q4), la version caveman garde l'avertissement mais perd l'option `rm -rI` (une seule confirmation) et la mise en garde contre l'espace/joker (`rm -rf photos_2019 /*`). Sur la recette, peu de gain (une recette = surtout des quantités).
- Ce que le skill fait bien : aucune donnée technique perdue sur Excel/404, réponse en tête, plus de « Bien sûr ! ».
- Verdict : utile pour de longues sessions de code (beaucoup de réponses), presque inutile pour quelques questions ; vérifier les commandes dangereuses.

## Accroches (méthode v2)
- Short 1 (raté) : « Le skill qui fait −65 % de tokens… ma facture n'a pas bougé » (62 591 vs 62 603).
- Short 2 (duel) : même question Excel, 231 tokens vs 66, compteur à l'écran.
- Long, 1re seconde : « 2 239 tokens → 973. Mais la facture : identique. »

## Mise à jour 24/11 ~00:30 Maroc — préparation (voix bloquée)
- Vérifié sur le dépôt : le chiffre « −65 % » venait d'un tableau de 10 questions ; l'auteur l'a retiré du README le 8 sept. 2026 (commit bb1cfc8b « retire the unmeasured savings claims »). Script ajusté : « le chiffre qui circule ».
- Script FR/EN final : episodes/briefai-11/voice/sents.json (11 phrases, ~1 min 53). Plans : episodes/briefai-11/build.py (11 plans, `python3 build.py stills` pour l'aperçu ; durées dans timing.json, à recalculer après la voix comme #10). Miniatures : thumbs/briefai-11_{fr,en}.jpg.
- Reste : voix (quota AI Studio atteint le 23/11 23:45 ; dossier Téléchargements pas relié), alignement (copier episodes/briefai-10/voice/align.py), audio.py/srt/shorts (copier #10, remplacer 10→11), mise en ligne.
- Shorts : s1 = phrases [0,7,8,6] (accroche « −57 % de tokens… et ma facture n'a pas bougé ») ; s2 = phrases [4,9,10] (accroche « Claude caveman a oublié la mise en garde qui sauve tes fichiers »).

## YouTube long
Titre FR : J'ai testé le skill « caveman » : −57 % de tokens… et la même facture
Titre EN : I Tested the "Caveman" Skill: 57% Fewer Tokens… Same Bill
Description FR :
6 questions de tous les jours posées au même Claude, sans puis avec le skill caveman (v4.2.0, Apache-2.0).
Mesuré (tokenizer o200k) : 2 239 → 973 tokens de réponse (−57 %), de −38 % (recette) à −71 % (formule Excel). Le « −65 % » n'est atteint que sur 1 question sur 6.
Mais le skill pèse 1 158 tokens rechargés à chaque session : gain net ≈ 108 tokens. Compteur de session : 62 591 sans, 62 603 avec.
Raté : sur la suppression d'un dossier, la version caveman perd la mise en garde contre « rm -rf dossier /* ».
Verdict : utile pour de longues sessions de code, inutile pour quelques questions.

▶ Installer (Claude Code) :
claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman
ou : npx skills add JuliusBrussee/caveman -g

▶ Les 6 questions utilisées :
1. Dans Excel, quelle formule pour additionner la colonne B seulement quand la colonne A vaut « Courses » ?
2. Mon téléphone Android se décharge très vite depuis une mise à jour. Qu'est-ce que je dois vérifier ?
3. Quelle différence entre un prêt immobilier à taux fixe et à taux variable ?
4. Je veux supprimer définitivement le dossier « photos_2019 » sur Linux en ligne de commande. Quelle commande ?
5. Mon site affiche « 404 Not Found » depuis que j'ai déplacé une page. Comment corriger ?
6. Donne-moi une recette rapide de pâtes pour 2 avec tomates, ail et parmesan.

Voix générée avec Gemini TTS (Google) ; test, montage et script réalisés avec Claude (Anthropic) ; vérifié par un humain.
#IA #Claude #ClaudeCode #Tokens #SkillsClaude
Description EN : traduction fidèle.

## Shorts YouTube
- S1 (13:00) : « Ce skill coupe 57 % des tokens… ma facture n'a pas bougé 😳 #Shorts »
- S2 (21:00) : « Claude version homme des cavernes a oublié LA mise en garde 😬 #Shorts »

## Facebook (mot-clé CAVEMAN)
Reel 1 : « −57 % de tokens… et la même facture. 💬 Commente CAVEMAN et je t'envoie la commande d'installation + mes 6 questions de test en message privé. »
Reel 2 : « Le skill caveman a supprimé la mauvaise phrase. 💬 Commente CAVEMAN et je t'envoie le skill en message privé. »
Long (lendemain 18:00) : description FR + « 💬 Commente CAVEMAN et je t'envoie la commande d'installation et les 6 questions en message privé ».
Message privé automatique = bloc « Installer » + « Les 6 questions » ; réponse publique « C'est envoyé en message privé 📩 ».
