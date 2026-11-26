# EN5 — "I Made ChatGPT, Claude and Gemini Build the Same App. Then I Tried to Break It." (screenshots + app renders, voice Elio)

A1 [AVATAR — hook]
I gave ChatGPT, Claude and Gemini the exact same job: build me a working app, in one prompt. A bill splitter, with tips, that has to be right to the cent. Then I attacked all three apps with twenty two tests, including the classic money bug that breaks a lot of real code. One AI tested its own work. One told me it hadn't. And one just dumped the code. Let's see who shipped.

V1 [the prompt card: 5 ids + 4 rules]
Here's the prompt. One HTML file, no libraries. Five element names I chose, so I can test the apps with a robot. And four rules. The tip is on the bill. One line per person. The shares must add up exactly to the total, and if the cents don't divide evenly, the first people pay one cent more. And anything nonsense, like zero people or a negative bill, must show "Invalid input".

V2 [why this is hard: $10 / 3, float trap $4.34]
Sounds easy. It isn't. Ten dollars between three people is three thirty four, three thirty three, three thirty three. Most calculators say three thirty three three times, and a cent disappears. And computers are bad at money: in JavaScript, four thirty five times a hundred is four hundred thirty four point nine nine nine. Round it down and your app charges four thirty four.

V3 [ChatGPT answer: file card, under 10 s]
ChatGPT first. Under ten seconds. It handed me a downloadable file, three point eight kilobytes, with an example and a checklist. It even used exact integer math, which is the right call for money. And then, at the bottom, this line: the file has been created, but I haven't run browser based tests. Honest. But that's my job now.

V4 [Claude answer: ran a command, 40 s]
Claude took forty seconds. Look at the top: created a file, ran a command. Before answering, it ran its own test cases, and it says so: I ran a few test cases, and the results were correct. It works in whole cents, and it even made the text big enough that an iPhone doesn't zoom in when you tap a box.

V5 [Gemini answer: code only]
Gemini, in Neon mode, did the opposite. No intro, no explanation. Just one big block of code, a hundred and twelve lines. It added one thing I didn't ask for: a grand total line above the shares. Nice touch. But you'd better know what to do with an HTML file.

V6 [the three apps side by side on a phone]
Here are the three apps, opened on a phone screen. All three look clean and modern, and weirdly similar. ChatGPT and Claude even picked almost the same indigo button. Gemini went blue. Same layout: bill, tip, people, one big button.

V7 [test robot running: 14 checks x 3, green ticks]
Now the robot. Fourteen checks per app. Nine money cases, like the ten dollars, the five cents split between seven people, a thousand two hundred dollar bill with a twelve and a half percent tip, and the four thirty five trap. Then five nonsense inputs: an empty bill, a negative bill, two and a half people, zero people, a negative tip. Result: ChatGPT fourteen out of fourteen. Claude fourteen out of fourteen. Gemini fourteen out of fourteen. Not a single cent lost.

V8 [torture round: 8 weird inputs, one difference]
So I went further, with eight weird inputs my prompt never mentioned. A thousand people. A bill written as one e two. Three point zero people. A ninety nine million dollar bill split seven ways. All three gave the same answers, every time. Except one. When I deleted the tip, ChatGPT and Claude said "Invalid input". Gemini quietly treated it as zero percent and split the bill. Not wrong, not right. My prompt simply didn't say.

V9 [scoreboard]
Final score. Working code: three out of three. My tests: forty two out of forty two. Fastest: ChatGPT. Most careful: Claude, the only one that tested its own app before answering. Least talkative: Gemini.

A2 [AVATAR — verdict + CTA]
So here's what I learned. For a small app, all three can ship working code in one prompt. The secret wasn't the AI. It was the prompt: exact names, and rules you can test, like "must add up to the cent". Where my prompt was vague, the apps disagreed. So write your rules like test cases. My exact prompt and the three apps are in the description. Tell me what I should make them build next.
