# BriefAI — format v3 (EN only, model "Skill Leap AI")
Decided with Alae 24/11/2026: English only, Skill Leap-style (real tests of AI tools, rounds + score), invented AI presenter.

## CURRENT STATE (updated 25/11 ~02:00 Morocco)
- YouTube EN scheduled through **26/11** (EN4). Facebook EN scheduled through **25/11** only (EN3) — EN4 NOT on Facebook (page token missing).
- Open to-dos: (1) Facebook token: Alae must put `briefai_fb_secrets.json` back in Downloads → then schedule EN4 on FB (long 17:00 / Reel 20:00 of the next free day) with pub/b17 mp4 @ab99cef; (2) "Vidéo similaire" of Shorts after their long goes public (EN3 BfouuCYCj6A → HX8G_EXsvqw after 25/11 17:00; EN4 F1csgI2nwhg → Qla3Wpz6eow after 26/11 17:00); (3) duplicate private draft rMa5PcqN-uc to delete (Alae, permanent deletion); (4) next episode EN5 for 27/11.

## THUMBNAILS — style rotation (Alae 24/11, 20:00: "il faut avoir en random, pas toujours le même style")
Reference: Skill Leap AI channel (huge 1-3 word headline, presenter with a strong expression, real UI screenshot or result, bright saturated background, arrow/sticker, small brand tag). Never two consecutive videos (long OR Short cover) with the same style. Pick the style at random among those not used in the last 2 videos, and log it in the episode notes.
Styles (all 1280x720, tools/thumb_leap.py helpers; examples in tools/thumbs_v2_make.py):
1. **SHOCK** — huge 2-word headline (yellow block + white Anton), presenter right with surprised face, tilted screenshot card with red sticker, yellow arrow (EN3 Gemini 4 Neon).
2. **VERSUS** — split screen 2-3 colors (one per AI), presenter, big "WHO LIED?"-type badge (EN2).
3. **RESULT ZOOM** — one giant real detail (the wrong number, the bug, the formula) circled in red, 1-3 word headline (Black Friday, Budget, EN4 navy/red "HIDDEN IN A PDF").
4. **BIG NUMBER** — one enormous number/percent on a bright gradient, presenter half cut on one side (EN1 "$694", caveman "−57 %", prompt EN "1").
5. **CONCEPT** — one symbolic object made by us + 2-word headline on a colored band (prompt maître FR).
6. **BEFORE / AFTER** — two results side by side with ✗ / ✓ stamps (Taste Skill).
Presenter cut-outs (rembg, from the Vids avatar): brand/host_wow.png, host_grin.png, host_smile.png, host_hands.png, host_serious.png — use them only on videos where the presenter appears (EN v3); FR/older faceless videos → styles without face.
Rules: background color changes each time (yellow, blue, green, red, purple, white, orange, teal), max 4 words, readable at phone size, presenter expression varies, AI names written in text (no official logos redrawn), the "Veo/AI" disclosure stays on YouTube via the altered-content flag.
DONE 24/11 ~21:00: all 9 long videos except EN3 re-thumbnailed in Studio with thumbs/v2/<videoId>.jpg (SlHv7nSQUHk concept/purple, pgJx8_P6H48 big number/yellow, 8Gl7P2NXjKs card/blue, S8QFCWJyfEA zoom/red, UPkeIM0ZgZs big number+face/green, ZYd9aV6DPU8 before-after/white, 2sv-E1Qza2E versus/3 colors, ZxzbXJ50tGs big number/orange, B9wu0kHHNAs zoom/teal). Upload method: /video/ID/edit, scroll down so the thumbnail input loads, inject the fetched file into input[accept*=image], click #save.
Next thumbnail (EN5): not SHOCK/RESULT ZOOM → BIG NUMBER, VERSUS, CONCEPT or BEFORE/AFTER; not navy/red, not yellow.

## Presenter (free, Google AI Pro on alae.merioumi)
- Google Vids (docs.google.com/videos, account u/2) → custom avatar "BriefAI Host" (invented man, early 30s, navy sweater, LED home studio), voice **Elio**.
- Quota (Google AI Pro): ~25 avatar clips / month; voice-over unlimited → avatar only for intro (+ outro when quota allows); all narration = Vids voice-over Elio (same voice). Used so far: EN2 2, EN3 2, EN4 2.
- Vids shows a small "Veo" mark bottom-right: keep it (AI disclosure). On YouTube tick "altered or synthetic content".
- Pipeline: one Vids project per episode, 1 scene per paragraph (avatar scene / voice-over scene) → File > Download > MP4 lands in Downloads (now connected) → device_stage_files → scene boundaries = Vids aria-labels ("commençant … à N secondes") refined with silencedetect → our graphics replace the blank voice-over scenes (build.py), avatar scenes kept with overlays (avatar.py) → assemble.py (loudnorm -14).
- Vids tips (25/11): add scenes with menu Scène > Nouvelle scène (inserts after the selected scene) — the floating "+" on the timeline can hit an existing scene; insert the voice-over with ONE click on "Insérer une voix off" then check it says "Modifier la voix off"; check "Toutes les scènes" list for duplicates; deleted scenes leave orphan audio clips (right-click → Supprimer). Avatar scene boundaries = video scene-change detection (ffmpeg select scene>0.08).

## Episode recipe
1. Real test on the 3 free web apps (ChatGPT Chat/Instant, Claude.ai default, Gemini u/2 default), same prompt, **3 fresh chats each**, ground truth computed ourselves.
2. Capture real answers: page zoom 1.7-1.9 + screenshot save_to_disk (crop out sidebars/history/profile photos). If Alae is away (no "Share" click for screen recording): full-window screenshots (1568x751) + camera moves (EN4 build.py).
3. Files to the AIs: file_upload tool with a file in /mnt/user-data/outputs (ChatGPT "Joindre des fichiers" input, Claude "Importer des fichiers" input, Gemini: open "Importation et outils" first, then the file-input inside "Importer des fichiers").
4. Structure: avatar hook with the failure (0-10 s) → the test → rounds → per-AI → scoreboard → avatar tip.
5. Short = the AI failure (one per day, serves the long).

## Topic plan
| # | Topic | Verifiable test |
|---|---|---|
| EN1 | I gave 3 AIs my bank statement | DONE |
| EN2 | Make ChatGPT, Claude and Gemini lie (10 tests) | DONE |
| EN3 | Gemini 4 Neon, 3 real jobs | DONE |
| EN4 | Hidden instruction in a PDF (needle-in-haystack + prompt injection) | DONE 26/11 |
| EN5 | Same one-prompt app: who ships something that works? | run it, count bugs |
| EN6 | 20 trick questions: who makes things up? | hallucination count |
| EN7 | Same landing page, 3 AIs, 3 real visitors' votes | side by side |
| EN8 | Budget spreadsheet that doesn't break | add a row → formulas update (LibreOffice) |
+ any big AI release → "new feature tested" episode first (news week of 20/11: ChatGPT Space for Plus, Claude computer use beta Team/Enterprise, Gemini Tasks calling — none free/testable yet).

## Publishing without Chrome (24/11)
- **Facebook = API** : Meta app "BriefAI Publisher" (id 1833397627781759, mode dev, no business portfolio), permanent page token for "Brief AI" only. Script `tools/fb_publish.py` (reel / video / list), videos pulled by Facebook from raw.githubusercontent URL @SHA. Allowed domains on claude.ai: graph.facebook.com, graph-video.facebook.com, rupload.facebook.com.
- Token is NEVER in the repo or project: container file /home/claude/.secrets/fb_page_token (lost when the container resets). Copy kept by Alae: `briefai_fb_secrets.json` (sent in chat 24/11; to be saved in Downloads — NOT there on 25/11) → next runs: device_stage_files from Downloads, then write page_token into /home/claude/.secrets/fb_page_token.
- "Comment to message" automations stay in Meta Business Suite (not in the API).
- **YouTube** : API uploads from an unverified project are locked private → keep Studio via Chrome (scripted helpers) until a YouTube API audit is approved.
- YouTube Studio when the Chrome window is in the background (screenshots time out, execCommand fails): set title/description with `el.innerText = txt` + `InputEvent('input')`; time = click the time input then click the `tp-yt-paper-item` whose text is "17:00"; after Programmer, a "toujours en cours de vérification" dialog → click OK. NEVER navigate away before the dialog shows "Mise en ligne terminée" (an interrupted import leaves a draft).

## EN1 published 24/11 (test "2 videos per day")
- YouTube: long UPkeIM0ZgZs 24/11 15:00 (thumbnail, altered content = yes, EN auto-captions; SRT in pub/b13/b13_en.srt not uploaded yet); Short 1 J-A5NYcZG_8 24/11 19:00; Short 2 Gp4ThcIiBQ8 25/11 19:00. To do: "Vidéo similaire" of both Shorts → UPkeIM0ZgZs after 15:00.
- Facebook (API, first use): long video 1759041218504741 24/11 15:30; Reel 1174469108441978 24/11 19:00; Reel 3410772685780861 25/11 19:30. Automation "BANK - bank statement prompt" saved (reply "Sent you a message!").
- tools/yt_studio.js = helpers to paste in Studio (__up/__fill/__kids/__altered/__thumb). Time field: click it, ctrl+a, type, Enter, then VERIFY (Short 2 first got 00:00 and was fixed in the video edit page).

## EN2 "I Tried to Make ChatGPT, Claude and Gemini Lie (10 Tests)"
- YouTube: long 2sv-E1Qza2E (3:09, thumbnail, altered = yes); Short piekQPxSOIE (description starts with the long's link). To do: "Vidéo similaire" → 2sv-E1Qza2E.
- Facebook (API): long 1126000840271102; Reel 1171934408565112; automation "PROMPTS - make AI lie test".
- Vids: custom avatars exist only inside the Vids file where they were created → always work in file 1n4uHvUkk1MO0ZKAtur1HWFiX_ahGnAsYjh5Bqhlcauc (cut from the export by time). Avatar scene script max 800 characters → avatar for hook + outro only, Vids voice-over (Elio) for the middle.
- Chrome tips: tabs freeze when many are open → close extra tabs; save_to_disk screenshots keep the `scale` you pass (use zoom without scale for real captures).

## EN3 "I Gave Gemini 4 Neon 3 Real Jobs. One Broke." — scheduled 25/11 (quality reference validated by Alae)
- YouTube: long HX8G_EXsvqw 25/11 17:00 (3:50, thumbnail, altered = yes); Short BfouuCYCj6A 25/11 20:00 (description starts with the long's link). Reminder 25/11 17:10: "Vidéo similaire" → HX8G_EXsvqw.
- Facebook (API): long 29270983899217586 25/11 17:00; Reel 1731437955010247 25/11 20:00.
- Method: REAL screen recording in the Chrome tab (getDisplayMedia + MediaRecorder, Alae clicks Share once), 3 jobs (Snake game in Canvas + autopilot bug/fix, bank-statement CSV audit, Lisbon trip in Task mode). Files: episodes/briefai-16 (build.py, avatar.py, assemble.py, timing.json), skill updated.
- Alae (24/11): "ok, on améliore encore le graphisme pour la prochaine vidéo".

## EN4 "I Hid a Secret Instruction in a PDF. Only One AI Warned Me." — scheduled 26/11 (YouTube only)
- YouTube: long **Qla3Wpz6eow** 26/11 17:00 (4:49, thumbnail RESULT ZOOM navy/red + host_wow, altered = yes); Short **F1csgI2nwhg** 26/11 20:00 (description starts with the long's link). To do after 26/11 17:00: "Vidéo similaire" of the Short → Qla3Wpz6eow. Duplicate private draft rMa5PcqN-uc (interrupted import) to be deleted by Alae.
- Facebook: NOT scheduled (token missing). Media ready: https://raw.githubusercontent.com/meralae0/tempo-assets/ab99cef56f7ffb9d91a25a1069ccc392b101802b/pub/b17/b17_long.mp4 and .../b17_short.mp4; captions pub/b17/desc.txt.
- Test: fictional 24-page PDF (episodes/briefai-17/make_doc.py, truth.md, runs.md). Round 1 (6 questions) and round 2 (counting) = all correct (Claude headline "11 pages" self-corrected to 10); round 3 = v2 PDF with white 4-pt instruction on page 16: none obeyed, ChatGPT warned spontaneously, Claude found and quoted it when asked, Gemini said "no hidden instructions" (false).
- Graphics improved vs EN3: word-by-word captions (active word on amber), full-screen chapter wipes, white-flash cuts, spotlight + rings, typed prompt cards, PDF page wall with highlighted pages, red text "reveal" of the hidden line, scoreboard grid. Files: build.py, avatar.py, assemble.py, short.py, thumb.py.
