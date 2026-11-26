# EN5 runs (26/11/2026 ~00:45-01:00 Morocco) — same prompt (prompt.txt), fresh chat each, free/default web versions
Ground truth: Decimal ROUND_HALF_UP (see test_app.js CASES, reference.html = 14/14).
## ChatGPT (Instant) — < 10 s
Answer = downloadable file card "bill-splitter.html · 3.8 KB" + example $100/15%/3 → 38.34/38.33/38.33 + checklist ("Exact integer arithmetic using JavaScript BigInt") + "The file has been created, but I haven't run browser-based tests."
Code obtained with follow-up "Paste the exact same file here as a single code block, unchanged." → apps/chatgpt.html (90 lines). Tests: 14/14.
## Claude (Opus 5.5, Moyen) — 39.7 s
"Créé un fichier, partagé un fichier, exécuté une commande" — "I ran a few test cases through the splitting code and the results were correct" + 5 bullets (cents, invalid input, rounding $1.005 → $1.01, Enter key, iPhone zoom). Same follow-up for the code → apps/claude.html (189 lines). Tests: 14/14.
## Gemini (Neon, u/2) — time not measured (stop button not detected; < 45 s)
Answer = code block only, no explanation → apps/gemini.html (112 lines), adds a "Grand Total" line. Tests: 14/14.
## Torture (torture.js, 8 unspecified inputs) — identical results on 7/8
empty tip: ChatGPT + Claude "Invalid input", Gemini treats it as 0 % ($80 → 40/40). Same: tie $10.70+15% → $12.31, 1,000 people → 1,000 lines of $0.10, "1e2" → 50/50, $0.001 → $0.00, "3.0" people OK, 0.5 % tip, $99,999,999.99 + 20 % / 7 → 17,142,857.15 + 6 × .14 ✓.
Naive code for contrast: Math.floor(4.35*100) = 434 → "$4.34" (float trap). All three avoided it.
