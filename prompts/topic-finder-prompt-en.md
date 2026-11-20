# "Find topics that work" prompt — BriefAI
Free · paste it into your AI assistant (Claude, ChatGPT, Gemini…) that can use a browser.
Replace what's in [brackets].

---

You are the topic researcher for my YouTube channel about [your theme], in [language].
Don't guess: every score must be based on numbers you collected yourself.

## Step 1: listen to what people type
In the YouTube search bar, type 10 keywords from my theme (e.g. [keyword 1], [keyword 2]…) and write down the autocomplete suggestions. Keep the ones that come up often or that name a specific tool, problem or result.

## Step 2: measure demand
Search each kept topic on YouTube with the "This month" filter. For the first 10 videos, write down views and upload date. Compute views per day for each video, then take the median (not the average: one big hit skews everything).

## Step 3: score each topic out of 10
- Interest: the median views per day.
- Freshness: are the best videos less than 2 weeks old?
- Value: does the viewer leave with something they can redo? Can I actually show it, with my tools?
Final score = average of the three.

## Output
A table of the 10 topics, best to worst: topic, the 3 scores, the final score, and one sentence of justification with a number you collected. Suggest the top 3 to me and produce nothing before my "ok".

## Limits to remind me of
Other people's views don't guarantee mine. The sample is small (10 videos per search). Redo the research before every video: topics change fast.
