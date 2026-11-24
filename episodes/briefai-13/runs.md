# #13 test — same statement, 3 AIs (2026-11-24 ~10:xx Morocco)
Truth (Decimal): groceries net $694.35 (FreshMart+Corner Market+Green Basket − refund 23.48; gross 717.83). Duplicate: Luna Trattoria $56.40 on 10/17. Subscriptions $85.96/mo = $1,031.52/yr.
## Run 1 (timer unreliable)
- ChatGPT (chat, "Instantané"): 694.35 (excl. MegaMart, says "unverified") / Luna 56.40 / 1,031.52 → 3/3.
- Claude (Opus 5.5 Moyen, claude.ai, ran code): 874.21 incl. MegaMart online (+179.86), "without Corner Market 802.67" / Luna 56.40 / 1,031.52 (+ without gym 563.52). Math right, assumption different. 12.2 s.
- Gemini (Neon, u/2, ran code): 694.35 (717.83 − 23.48) / Luna 56.40 / 1,031.52 → 3/3. ~35-50 s.
## Run 2 (fresh chats)
- ChatGPT Instant: **684.31** (WRONG, −10.04; "excluding ambiguous MegaMart") / Luna 56.40 / 1,031.52.
- Claude: 874.21 again (897.69 gross over 18 charges incl. MegaMart − 23.48; "didn't count restaurants, cafés, delivery") / Luna / 1,031.52 (+563.52 w/o gym). 14.3 s (stop-button timer).
- Gemini Neon: 694.35 (606.96 FreshMart + 71.54 Corner + 39.33 Green Basket − 23.48 — all subtotals verified) / Luna / 1,031.52. 50.9 s.
## Run 3
- ChatGPT Instant: 694.35 / Luna / 1,031.52 (correct).
- Claude run 3: 874.21 (897.69 at FreshMart, Corner Market, MegaMart online, Green Basket − 23.48) / Luna / 1,031.52 (+563.52 w/o gym).
- Gemini run 3: no answer — spinner for 4+ min, conversation never created (stalled).
## Summary
Duplicate: 3/3 everywhere. Subscriptions: 3/3 everywhere. Groceries: ChatGPT 2/3 (684.31 once, −10.04, no warning); Claude 0/3 by definition (874.21 incl. MegaMart, math correct, says what it included); Gemini 2/2 answered + subtotals, ~50 s, 3rd try stalled.
