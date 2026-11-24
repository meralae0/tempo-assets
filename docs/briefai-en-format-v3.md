# BriefAI — format v3 (EN only, model "Skill Leap AI")
Decided with Alae 24/11/2026: English only, Skill Leap-style (real tests of AI tools, rounds + score), invented AI presenter.

## Presenter (free, Google AI Pro on alae.merioumi)
- Google Vids (docs.google.com/videos, account u/2) → custom avatar "BriefAI Host" (invented man, early 30s, navy sweater, LED home studio), voice **Elio**.
- Quota (Google AI Pro): ~25 avatar clips / month; voice-over unlimited → avatar only for intro (+ outro when quota allows); all narration = Vids voice-over Elio (same voice).
- Vids shows a small "Veo" mark bottom-right: keep it (AI disclosure). On YouTube tick "altered or synthetic content".
- Pipeline: one Vids project per episode, 1 scene per paragraph (avatar scene / voice-over scene) → File > Download > MP4 lands in Downloads (now connected) → device_stage_files → scene boundaries = Vids aria-labels ("commençant … à N secondes") refined with silencedetect → our graphics replace the blank voice-over scenes (build.py), avatar scenes kept with overlays (avatar.py) → assemble.py (music 0.10, loudnorm -14).

## Episode recipe
1. Real test on the 3 free web apps (ChatGPT Chat/Instant, Claude.ai default, Gemini u/2 default), same prompt, **3 fresh chats each**, ground truth computed ourselves.
2. Capture real answers: page zoom 1.7-1.9 + screenshot save_to_disk (crop out sidebars/history/profile photos).
3. Structure: avatar hook with the failure (0-10 s) → the test → rounds → per-AI → scoreboard → avatar tip.
4. Short 1 = the AI failure; Short 2 = the duel/scoreboard.

## Topic plan (to confirm)
| # | Topic | Verifiable test |
|---|---|---|
| EN1 | I gave 3 AIs my bank statement (DEMO done) | groceries / duplicate / subscriptions, 3 tries |
| EN2 | Which AI builds a budget spreadsheet that doesn't break? | add a row → do formulas update (LibreOffice check) |
| EN3 | 3 AIs read the same 5 crumpled receipts | totals, tax, date vs truth |
| EN4 | I hid 5 facts in a 30-page PDF — who finds them? | recall /5, invented facts |
| EN5 | Same one-prompt app: who ships something that works? | run it, count bugs |
| EN6 | 20 trick questions: who makes things up? | hallucination count |
| EN7 | Same landing page, 3 AIs, 3 real visitors' votes | side by side |
+ any big AI release → "new feature tested" episode first.
