# Runs du test #12 (24/11/2026 ~00:05 Maroc) — durées = durée de l'agent (harnais)
A1 Claude (défaut) sans outil, relevé collé : 33,5 s — Entrées 2 492,30 / Sorties 2 078,29 / Solde +414,01 — toutes catégories justes.
A2 Claude (défaut), lecture du fichier seule, sans calcul par programme : 25,9 s — mêmes totaux, catégories justes.
A3 Claude Haiku, idem : 22,8 s — mêmes totaux, catégories justes (dit « 50 lignes » = en-tête compté).
B  Claude avec outils, classeur Excel demandé : 50,8 s — B_budget.xlsx, SUMIF, graphique, contrôle ; totaux justes.
Raté vérifié (LibreOffice recalcul, chk/) : plages figées $D$2:$D$50 / $C$2:$C$50 → ligne 51 ajoutée (−50 € Courses) ignorée : Courses 429,44 et Sorties 2 078,29 inchangées.
Remarque mineure A1/A2 : « deux pleins le 30 octobre, vérifie un double prélèvement » alors que les montants diffèrent (61,55 / 46,52).
Vérité terrain : gen.py (seed 12) + calcul Python au centime.
