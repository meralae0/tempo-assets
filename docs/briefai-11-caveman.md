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
