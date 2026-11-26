# BriefAI #20 — 60-second AI animated short ("Wick and the Dark")
Start 26/11 08:20 Maroc.
## Step 1 — Script (Claude.ai, Opus 5.5, default)
- 1 prompt, answer in ~45 s. Title "Wick and the Dark", character sheet + style line, 6 shots (8+10+10+12+10+10 = 60 s ✓), narration 94 words (19+13+11+17+17+17 = 94 ✓, claimed 94 ✓). Shots to animate: 3 (storm) and 6 (ending).
## Step 2 — Images (Gemini app, AI Pro, image model "Nano Banana"-type, same chat)
- Shot 2 (reference) ~20 s. Shot 1 ~25 s.
- FAILURE: first try of Shot 3 (prompt without "Create an image", "frozen in shock" + "crashing") → "I'm having a hard time fulfilling your request." (caps/02_gemini_fail_raw.jpg). Fix: start with "Create an image." + repeat the full character sheet → worked.
- Shots 3–6: ~10 / ~8 / 59 / 57 s each. 6/6 images, same character every time (dome, amber eye, scarf, antenna) ✓. Only miss: shot 3 lamp is still lit (prompt said it goes out). Shot 1 Wick is tiny.
- Display copies 1376x768 (full-size download 2752x1536). Cost $0 (AI Pro plan).
## Step 3 — Voice (Google AI Studio, Gemini 3.8 Flash TTS, preset "The Master Storyteller", voice Riko)
- 1 block, 94 words with <long pause> between shots. Generated in ~20 s. Length 51.2 s (fits under 60 s). Cost $0.
## Step 4 — Animation (Gemini app, "Créer une vidéo" = Veo, image-to-video)
- Shot 3 image pasted + motion prompt → after ~2 min: "I seem to be encountering an error." (caps/03_veo_error_raw.jpg). Retry ("Réessayer") → generating.
- Retry → ~95 s → refused: "can't generate ... due to interests of third-party content providers" (caps/03_veo_refusal_raw.jpg). Original robot, no brand — Veo's filter still blocked it. Next: try Shot 6 (calm scene).
- Shot 6 (calm ending, "Gently animate this illustration…") → video ready in ~3–5 min; NOTE the chat vanished from the page while generating and only reappeared in the sidebar ("Animated Lighthouse Illustration"). 10 s, 1280x720, beam sweeps, boat moves, robot swings legs ✓. Robot design kept ✓.
- Shot 3 retry with a softer prompt (no "lightning", "startles") → pending.
- Shot 3 third try (softer prompt, new chat) → "I seem to be encountering an error" again after ~110 s. Gave up: 1 of 2 planned animations. Shot 3 stays a still with a camera move.
## Step 5 — Edit (Claude Code in the container: python + ffmpeg, cartoon.py)
- Ken Burns moves on 5 stills + Veo clip for shot 6, crossfades, title card, narration + soft music bed, -14 LUFS. Render 77 s. Result: wick_and_the_dark.mp4, 54.0 s, 1920x1080.
## Totals
- Hands-on clock: 08:20 → 08:47 ≈ 27 min (incl. ~12 min waiting on Veo). Cost: $0 extra (Claude Pro + Google AI Pro subscriptions already paid).
