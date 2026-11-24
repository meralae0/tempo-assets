---
name: briefai-producer
description: Produces and schedules one BriefAI episode end to end (English AI-tools channel @briefai + Facebook page "Brief AI"): pick a fresh AI feature, really test it on screen, record presenter (Google Vids avatar), build a Skill-Leap-style video (real UI full screen, face in a circle, zooms, kinetic callouts, SFX), 1 long + 1 Short/Reel, schedule YouTube (Studio via Chrome) and Facebook (Graph API). Use whenever Alae or a scheduled run asks for the next BriefAI video.
---

# BriefAI producer (format v3, decided with Alae 24/11/2026)

Daily output: **1 long video (6–10 min, English) + 1 Short/Reel (30–45 s)** on YouTube AND Facebook. No validation asked; reply to Alae in French, 3 lines max (scheduled, links, problem).
Repo: github.com/meralae0/tempo-assets → /home/claude/tempo-assets. Project docs: claude/14-briefai-en-format-v3.md (state, IDs), claude/11-tempobrief-log.md (log).
Never touch Rawi Zone, Quiz Rush, ClipRush, ShopyDaba accounts/repos. Spend nothing. No real people, no brand logos shown big (blur them in AI outputs). Ask Alae only for passwords/keys or a permanent deletion. Never delete anything in Downloads.

## 1. Topic (5 min max)
- One WebSearch "new AI feature this week <month year> ChatGPT Claude Gemini". Pick a **consumer feature we can demo for free** with the logged-in apps (Gemini u/2 = alae.merioumi AI Pro, ChatGPT, Claude.ai). Big launch > anything else.
- Angle (Skill Leap style): "X can now do Y — I tested it" / "N ways to use X" / "X vs Y vs Z, same task". The Short = the most surprising result or the AI's failure.
- Read docs/style/skill-leap-grammar.md (structure, pacing, visual grammar).

## 2. Real test (Chrome, claude-in-chrome) — cheap mode
- One new chat per test; send prompts with `javascript_tool` paste (DataTransfer paste event) or type + Enter; never wait with screenshots, poll with JS (text/`img.naturalWidth`) every 10 s.
- Measure time (performance.now at send, stop-button gone) and check every number yourself (python/Decimal). Log in episodes/briefai-NN/runs.md.
- Captures: `document.documentElement.style.zoom='1.7'`, scroll the answer into view, `screenshot save_to_disk` (full scale) → copy from /tmp/claude-chrome-screenshots-*/ to episodes/briefai-NN/caps/. Crop out sidebars, chat history, profile photos. Media outputs (images/GIF/video): Download button → C:\Users\Family\Downloads → `device_stage_files`.

## 3. Script (English, ~150 wpm for our voice, 6–10 min = 900–1500 words)
Hook 0–15 s (what's new + 3 things it can do + who gets it) → where to find it (zoom on the button) → demos one by one ("First…", "Next…") each with a concrete result and one number → the failure/limit → verdict + "prompt in the description". Write scenes in script.md: `S1 [AVATAR]` intro, `Vn [SCREEN: caps/file, zoom boxes]`, `S9 [AVATAR]` outro.

## 4. Presenter + voice (Google Vids, docs.google.com/videos, account alae.merioumi = u/2)
- Avatar "BriefAI Host" (invented man, navy sweater, LED studio), voice **Elio**. Quota ≈ 25 avatar clips/month → **1 avatar scene per video containing the whole narration** (gives a lip-synced face for the circle the whole time). If the script is too long for one scene, intro+outro avatar scenes and Vids voice-over (Elio) for the rest.
- New video → scene 1 → Avatar panel → paste script → Aperçu → Générer (wait until 100 %). Fichier > Télécharger > Vidéo MP4 → lands in Downloads → device_stage_files → episodes/briefai-NN/vids/vids_export.mp4.
- Paragraph timings: Vids aria-labels "… commençant dans la scène N à X secondes" (JS on the page) + `silencedetect` refine.

## 5. Build (container, Python/PIL + ffmpeg)
- tools/leap.py: `cam` (real capture with smooth zoom/pan between boxes), `cursor`, `pip` (avatar face in white-ringed circle bottom-left, from the Vids export frames), `dim_callout` (kinetic text over dimmed UI), `tiles` (app tiles popping around the presenter in the hook), `chapter`, `cta` (orange pill "Prompt in the description"), `sfx_track`.
- tools/sfx/*.wav (make_sfx.py): whoosh on cuts/zooms, pop on tiles/callouts, ding on correct, buzz on failure. **No music bed** (reference has none); voice at −14 LUFS, SFX −12 to −18 dB under voice.
- Template: copy episodes/briefai-13 (build.py, avatar.py, assemble.py, shorts.py) and switch scenes to leap.py components. Render 2 processes in parallel, then assemble.py. Check one frame per scene in a contact sheet before publishing.
- Short: the best 30–45 s (failure or wow result), 9:16, hook text top (font auto-fit), video crop 1520×1080 scaled to width 1080.
- Thumbnail 1280×720: presenter face left (crop from export), big 2–4 word claim right, one number in amber. Title ≤ 70 chars, curiosity + concrete.

## 6. Publish
Push the repo first; media URL = https://raw.githubusercontent.com/meralae0/tempo-assets/<SHA>/pub/bNN/<file>.
- **YouTube (Chrome, Studio)**: open `studio.youtube.com/channel/UCTUbZU2wKVlVbMPy80yha5A/videos/upload?d=ud` (if "not allowed": youtube.com/channel_switcher → BriefAI). Paste tools/yt_studio.js, then `await __up(url,name)`, `__fill(title,desc)`, `await __thumb(url)`, `__kids(false)`, `#toggle-button` click, `__altered(true)` (avatar = synthetic), Next ×3 via `#next-button`, expand "Programmer", date picker click day, time field: click, ctrl+a, type HH:MM, Enter, **zoom to verify**, Programmer, OK. Times (Morocco), **same day on both platforms**: long 17:00, Short 20:00 (the Short serves the long: description starts with the long's link, and "Vidéo similaire" = the long, set right after 17:00 or at upload if the long is already public).
- **Facebook (API, no Chrome)**: page token in /home/claude/.secrets/fb_page_token; if missing, stage C:\Users\Family\Downloads\briefai_fb_secrets.json and write its page_token there (chmod 600, never commit). `python3 tools/fb_publish.py video <url> "<title>" "<caption>" "YYYY-MM-DD 17:00"` and `... reel <url> "<caption>" "YYYY-MM-DD 20:00"` (Reel caption: "Full test on our page/YouTube"); `list` to verify. Caption ends with "💬 Comment KEYWORD and I'll send you the exact prompt in a private message."
- Facebook automation (Chrome, Business Suite): `business.facebook.com/latest/inbox/automated_responses?asset_id=1468799139649767&automation_template=comment_to_inbox_v2` → name, keyword + Enter, private message = the prompt, Save changes.

## 7. Close
Update claude/14-briefai-en-format-v3.md (IDs, times), append to claude/11-tempobrief-log.md, push repo, close the Chrome tabs you opened, answer Alae in 3 French lines.
