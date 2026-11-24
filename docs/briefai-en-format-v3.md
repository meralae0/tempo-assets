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

## Publishing without Chrome (24/11)
- **Facebook = API** : Meta app "BriefAI Publisher" (id 1833397627781759, mode dev, no business portfolio), permanent page token for "Brief AI" only. Script `tools/fb_publish.py` (reel / video / list), videos pulled by Facebook from raw.githubusercontent URL @SHA. Allowed domains on claude.ai: graph.facebook.com, graph-video.facebook.com, rupload.facebook.com.
- Token is NEVER in the repo or project: container file /home/claude/.secrets/fb_page_token (lost when the container resets). Copy kept by Alae: `briefai_fb_secrets.json` (sent in chat 24/11; to be saved in Downloads) → next runs: device_stage_files from Downloads, then write page_token into /home/claude/.secrets/fb_page_token.
- "Comment to message" automations stay in Meta Business Suite (not in the API).
- **YouTube** : API uploads from an unverified project are locked private → keep Studio via Chrome (scripted helpers) until a YouTube API audit is approved.

## EN1 published 24/11 (test "2 videos per day")
- YouTube: long UPkeIM0ZgZs 24/11 15:00 (thumbnail, altered content = yes, EN auto-captions; SRT in pub/b13/b13_en.srt not uploaded yet); Short 1 J-A5NYcZG_8 24/11 19:00; Short 2 Gp4ThcIiBQ8 25/11 19:00. To do: "Vidéo similaire" of both Shorts → UPkeIM0ZgZs after 15:00.
- Facebook (API, first use): long video 1759041218504741 24/11 15:30; Reel 1174469108441978 24/11 19:00; Reel 3410772685780861 25/11 19:30. Automation "BANK - bank statement prompt" saved (reply "Sent you a message!").
- tools/yt_studio.js = helpers to paste in Studio (__up/__fill/__kids/__altered/__thumb). Time field: click it, ctrl+a, type, Enter, then VERIFY (Short 2 first got 00:00 and was fixed in the video edit page).

## EN2 "I Tried to Make ChatGPT, Claude and Gemini Lie (10 Tests)" — scheduled 25/11
- YouTube: long 2sv-E1Qza2E 25/11 17:00 (3:09, thumbnail, altered = yes); Short piekQPxSOIE 25/11 20:00 (description starts with the long's link). To do after 17:00: "Vidéo similaire" → 2sv-E1Qza2E.
- Facebook (API): long 1126000840271102 25/11 17:00; Reel 1171934408565112 25/11 20:00; automation "PROMPTS - make AI lie test".
- Vids: custom avatars exist only inside the Vids file where they were created → always work in file 1n4uHvUkk1MO0ZKAtur1HWFiX_ahGnAsYjh5Bqhlcauc (add scenes at the end, cut from the export by time). Avatar scene script max 800 characters → avatar for hook + outro only, Vids voice-over (Elio) for the middle.
- Chrome tips: tabs freeze when many are open → close extra tabs; save_to_disk screenshots keep the `scale` you pass (use zoom without scale for real captures).
