# EN3 — "I Gave Gemini 4 Neon 3 Real Jobs. One Broke." (real screen recording, voice Elio)
Recording: Downloads/neon_demo.webm (19 min, 1920x806) → neon_p1.webm (0–622 s) + neon_p2.webm (625–1157 s). events.json = recorder clock.

A1 [AVATAR — hook]
Google just released Gemini 4 Neon, and everyone says it's their best model yet. So I skipped the benchmarks and gave it three real jobs. Build a game from one sentence. Audit my bank statement. Plan a whole trip on a budget. Two went perfectly. One broke halfway, and the way it fixed itself surprised me. Let's go.

V1 [picker + Snake prompt typed]
Here's Neon. It's in the model picker in the Gemini app if you're on AI Pro or Ultra. Nothing staged, these are the exact prompts. Job one: I asked for a playable Snake game in a single file, neon style, with a score, rising speed and a restart button.

V2 [canvas generating (timelapse) → result → my crash → restart]
It opens a canvas and writes the whole thing. About two and a half minutes later, this. Title, score, best score, speed meter, glowing grid. Up top, you can flip between the code and the live preview, or export the file. I hit start and crashed into the wall in two seconds. That one's on me. The restart button works.

V3 [follow-up autopilot → error toast → fix button fails]
So I pushed it. Add an autopilot: the snake plays by itself, chases the food, and avoids the walls and its own tail. It rewrote the file, and the new version broke. Start didn't respond, and a runtime error popped up. Even the one-click fix button failed.

V4 [plain-words fix → autopilot running]
So I described the problem in plain words. It found the bug itself: it had pasted placeholder comments into its own code. Three minutes later, autopilot on. And look at it go. It plans a path to the food, you can see the dotted line, and it speeds up as the score climbs. Two hundred points without me touching anything.

V5 [new chat, CSV attached, prompt]
Job two is the one most people will actually use. I gave it my October bank statement as a spreadsheet file: sixty-eight transactions, and I had already worked out every answer myself. I asked: find anything unusual, then tell me how much I spent, not counting savings.

V6 [answer scroll]
It took about forty seconds. It caught the double charge at Luna Trattoria, fifty-six forty, twice on the same day. It flagged the foreign transaction fee, and found all five subscriptions: eighty-five ninety-six a month. Total spending: three thousand five hundred eighty-nine dollars. It also noticed Daily Grind Cafe twice on October fourteenth, but for different amounts, and said that's two visits, not a mistake. Then it subtracted a twenty-three dollar refund to give me a net figure. I checked every number. All correct.

V7 [Task mode, prompt, reasoning steps timelapse]
Job three uses the new Task mode. Plan a three-day weekend in Lisbon for two, seven hundred dollars, not counting flights, with a cost table that adds up. This one works on its own: it searched the web, checked which sights are closed right now, converted euros at this month's rate, and kept recalculating the budget.

V8 [guide fullscreen scroll]
Almost five minutes later, it built a full travel guide, not just a chat answer. Six hundred fifty-seven dollars planned, a forty-three dollar buffer. I added up the chart: two eighty-eight, two sixty, sixty-three, forty-six. It's exact. It compares three places to stay, from a classic hotel in Chiado to a hostel inside Rossio station. Then a day-by-day plan, built mostly around free viewpoints, markets and a sunset ferry. Just double-check opening hours before you go.

V9 [scorecard graphic]
Here's the scorecard. The Snake game worked on the first try; the upgrade broke, and one plain message fixed it. The bank statement: every check correct. The Lisbon trip: the budget adds up to the dollar. Speed ranged from forty seconds to five minutes, depending on the job.

A2 [AVATAR — verdict + CTA]
So, is Gemini 4 Neon worth it? For building small apps, yes, but expect a bug or two, and explaining the problem works better than the fix button. For your files and your money, it was perfect on my test. And Task mode is the real surprise: give it a goal and walk away. Try this tonight: upload last month's statement and ask what's unusual. All three prompts are in the description.
