# BriefAI #12 — Claude fait mon budget : juste au centime… et un piège (test fait le 24/11 ~00:05 Maroc)

Statut : test réel fait, chiffres vérifiés, script FR/EN écrit (episodes/briefai-12/voice/sents.json, 11 phrases, ~1 min 55). Reste : plans build.py (copier #11), miniatures, voix, rendu, mise en ligne. Mot-clé : BUDGET.

## Le test
- Relevé fictif d'octobre (episodes/briefai-12/releve-octobre.csv, gen.py seed 12) : 49 opérations, aucune marque réelle.
- Vérité terrain (Python, au centime) : entrées 2 492,30 € ; sorties 2 078,29 € ; solde +414,01 €. Logement 862,60 · Courses 429,44 · Épargne 200 · Transport 162,54 · Restos+cafés 154,29 · Abonnements 102,36 · Retrait 60 · Loisirs/shopping 73,06 · Santé 34,00.
- A = Claude dans la conversation, sans calcul par programme (3 essais : 33,5 s, 25,9 s, Haiku 22,8 s) → 3/3 justes au centime.
- B = Claude avec outils, « vrai tableur Excel » (50,8 s) → B_budget.xlsx : feuille Relevé + Catégorie, feuille Budget en SUMIF, graphique, ligne de contrôle ; totaux justes.
- RATÉ vérifié : les formules s'arrêtent à la ligne 50 ($D$2:$D$50). Ajout d'une ligne 51 (−50 € courses) → recalcul LibreOffice : Courses 429,44 et sorties 2 078,29 inchangées, sans erreur. Correction : colonnes entières ou tableau Excel.
- Manuel vs IA : pas de chrono humain mesuré (honnête : on montre « 49 lignes à classer + 1 formule par catégorie » sans inventer de temps).
- Détails : episodes/briefai-12/runs.md ; captures LibreOffice : episodes/briefai-12/caps/.

## Accroches
- Long, 1re seconde : « 49 lignes → budget en 34 s, juste au centime. » puis « mais le tableur cachait un piège ».
- Short 1 (raté) : « J'ajoute 50 € de courses… le budget Excel de Claude ne bouge pas 😬 » — phrases [7,8,9].
- Short 2 (duel) : « Claude de tête vs mon calcul : 49 lignes, 34 s » — phrases [0,3,4].

## YouTube long
Titre FR : Claude a fait mon budget au centime près… mais son Excel cachait un piège
Titre EN : Claude Did My Budget to the Cent… But Its Excel File Had a Trap
Description FR :
Mon relevé d'octobre (49 opérations, données fictives) donné à Claude : total par catégorie, entrées, sorties, solde.
Dans la conversation : 3 essais, 3 fois juste au centime (2 492,30 € / 2 078,29 € / +414,01 €), 23 à 34 s.
En vrai fichier Excel (SOMME.SI + graphique) : 51 s, totaux justes… mais formules figées à la ligne 50 : une dépense ajoutée en dessous est ignorée sans message d'erreur.

▶ La demande exacte (avec la correction) :
« Voici mon relevé bancaire du mois (CSV). Fais-moi le budget dans un vrai tableur Excel : une feuille Relevé avec une colonne Catégorie, une feuille Budget avec le total par catégorie en formules SOMME.SI vers le relevé, le total des entrées, le total des sorties et le solde en formules, et un graphique des dépenses par catégorie. Utilise des colonnes entières ou un tableau Excel pour que les lignes ajoutées plus tard soient comptées. Puis dis-moi en 3 points où je peux économiser. »

Voix générée avec Gemini TTS (Google) ; test, montage et script réalisés avec Claude (Anthropic) ; vérifié par un humain.
#IA #Claude #Excel #Budget #ClaudeAI
Description EN : traduction fidèle.

## Shorts YouTube
- S1 (13:00) : « J'ajoute 50 € de courses… le budget de Claude ne bouge pas 😬 #Shorts »
- S2 (21:00) : « 49 lignes de relevé, Claude calcule de tête : juste au centime ? #Shorts »

## Facebook (mot-clé BUDGET)
Reel 1 : « Le budget Excel fait par l'IA ignorait mes nouvelles dépenses. 💬 Commente BUDGET et je t'envoie la demande corrigée en message privé. »
Reel 2 : « 49 lignes, 34 secondes, juste au centime. 💬 Commente BUDGET et je t'envoie la demande exacte en message privé. »
Long (lendemain 18:00) : description FR + « 💬 Commente BUDGET et je t'envoie la demande exacte (avec la correction) en message privé ».
Message privé automatique = la demande exacte ; réponse publique « C'est envoyé en message privé 📩 ».
