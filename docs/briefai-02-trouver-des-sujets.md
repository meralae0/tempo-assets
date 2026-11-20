# BriefAI #2 — « J'ai demandé à une IA de trouver les vidéos qui vont marcher »

Sujet validé par Alae le 20/11 (8,5/10). Format : résultat d'abord, puis la vraie démo, puis le prompt offert.
Mise en ligne : UNE vidéo (voix française) + piste audio anglaise, titre, description et sous-titres EN.
Cadeau : prompts/prompt-sujets-fr.md et prompts/topic-finder-prompt-en.md.

## Faits utilisés (relevés le 20/11/2026 vers 20 h, données dans episodes/briefai-02/)
- Suggestions YouTube réelles : « claude mcp » → connectors, roblox, higgsfield, figma, unreal, n8n, tradingview… ; « ai youtube automation » → « with claude », « step by step », « 2026 »…
- 13 recherches YouTube, filtre « Ce mois-ci », 10 premières vidéos de chacune (research.json).
- Médiane des vues par jour : chaîne sans visage avec Claude ≈ 17 000 ; montage avec Claude ≈ 6 500 ; Claude + Blender ≈ 6 400 (meilleure vidéo : 277 858 vues en 4 jours) ; Claude Cowork ≈ 110.
- Classement : ranking.json (n°1 Claude + Blender 8,7/10).
- Coût de la recherche : 0 € en plus (outils gratuits), quelques minutes.

## Script FR
[RÉSULTAT]
Voici les dix vidéos que mon IA veut que je fasse. Classées, notées sur dix, avec des chiffres. La première, un autre créateur l'a déjà tentée : deux cent soixante-dix-sept mille vues en quatre jours. Dans cette vidéo, je te montre comment l'IA a trouvé ces sujets, en trois étapes. Et à la fin, je te donne le prompt.

[POURQUOI]
Dans la vidéo un, l'IA avait choisi un sujet toute seule. Et c'était raté. Depuis, la règle numéro un, c'est : le sujet d'abord. Mais choisir un sujet au feeling, c'est jouer au loto. Alors j'ai demandé à l'IA de ne rien deviner. Chaque note doit venir d'un chiffre qu'elle a relevé elle-même.

[ÉTAPE 1]
Étape un : écouter ce que les gens tapent. Quand tu commences une recherche sur YouTube, il te propose la suite. Ces suggestions viennent de vraies recherches. L'IA a tapé une dizaine de mots-clés. Par exemple, Claude MCP. YouTube propose : connecteurs, Roblox, Figma, Higgsfield, TradingView. Et pour l'automatisation YouTube, il propose : avec Claude, étape par étape, deux mille vingt-six. Ça, c'est une liste de sujets que les gens cherchent déjà.

[ÉTAPE 2]
Étape deux : mesurer la demande. Pour chaque sujet, l'IA lance la recherche avec le filtre « ce mois-ci ». Elle relève les vues et la date des dix premières vidéos. Puis elle calcule les vues par jour. Et elle garde la médiane, pas la moyenne. Pourquoi ? Parce qu'une seule vidéo à un million de vues fausse tout. Résultat : une chaîne sans visage avec Claude, c'est dix-sept mille vues par jour en médiane. Le montage vidéo avec Claude, six mille cinq cents. Claude Cowork, à peine cent dix.

[ÉTAPE 3]
Étape trois : noter chaque sujet sur dix, avec trois critères. L'intérêt, c'est la demande qu'on vient de mesurer. La fraîcheur : est-ce que les meilleures vidéos ont moins de deux semaines ? Et la valeur : est-ce que tu repars avec quelque chose que tu peux refaire, et est-ce que je peux le montrer pour de vrai ? La note finale, c'est la moyenne des trois.

[LE CLASSEMENT]
Et voilà le classement. Claude contre ChatGPT finit presque dernier. Le sujet est usé : tout le monde l'a déjà fait. La chaîne sans visage a la plus forte demande. Mais elle arrive troisième, parce que c'est déjà très chargé. Deuxième, le montage vidéo avec Claude. Et numéro un, avec huit virgule sept : Claude qui pilote Blender pour créer un personnage en trois dimensions. Les vidéos sont toutes récentes, et la meilleure a fait deux cent soixante-dix-sept mille vues en quatre jours.

[LE GAGNANT]
Alors c'est décidé. La prochaine vidéo, c'est celle-là. Je vais relier Claude à Blender, et lui demander de créer le personnage de cette chaîne, avec un seul prompt. Tu verras le résultat, les ratés, et combien ça coûte.

[LES LIMITES]
Attention, deux limites. Les vues des autres ne garantissent pas les miennes. Et l'échantillon est petit : dix vidéos par recherche. C'est pour ça qu'il faut refaire cette recherche avant chaque vidéo. Les sujets changent vite.

[LE CADEAU]
Le prompt complet est gratuit, en français et en anglais, dans la description. Remplace ton thème entre crochets, colle-le dans ton IA, et tu auras ton propre classement en quelques minutes. Pour cette recherche, ça m'a coûté zéro euro de plus. Abonne-toi pour voir si le numéro un tient sa promesse.

## Script EN (piste audio)
[RESULT]
These are the ten videos my AI wants me to make. Ranked, scored out of ten, with numbers. Another creator already tried the first one: two hundred seventy-seven thousand views in four days. In this video, I'll show you how the AI found these topics, in three steps. And at the end, I'll give you the prompt.

[WHY]
In video one, the AI picked a topic on its own. And it failed. Since then, rule number one is: topic first. But picking a topic on a hunch is like playing the lottery. So I asked the AI not to guess anything. Every score has to come from a number it collected itself.

[STEP 1]
Step one: listen to what people type. When you start a search on YouTube, it suggests the rest. Those suggestions come from real searches. The AI typed about ten keywords. For example, Claude MCP. YouTube suggests: connectors, Roblox, Figma, Higgsfield, TradingView. And for YouTube automation, it suggests: with Claude, step by step, twenty twenty-six. That's a list of topics people are already searching for.

[STEP 2]
Step two: measure demand. For each topic, the AI runs the search with the "this month" filter. It writes down the views and the date of the first ten videos. Then it works out views per day. And it keeps the median, not the average. Why? Because a single video with a million views skews everything. The result: a faceless channel with Claude gets seventeen thousand views per day on median. Video editing with Claude, six thousand five hundred. Claude Cowork, barely one hundred ten.

[STEP 3]
Step three: score each topic out of ten, on three criteria. Interest is the demand we just measured. Freshness: are the best videos less than two weeks old? And value: do you leave with something you can redo, and can I actually show it for real? The final score is the average of the three.

[THE RANKING]
And here's the ranking. Claude versus ChatGPT ends up almost last. The topic is worn out: everyone has done it. The faceless channel has the strongest demand. But it comes third, because it's already very crowded. Second, video editing with Claude. And number one, with eight point seven: Claude driving Blender to create a 3D character. The videos are all recent, and the best one got two hundred seventy-seven thousand views in four days.

[THE WINNER]
So it's decided. The next video is that one. I'm going to connect Claude to Blender, and ask it to create this channel's character, from a single prompt. You'll see the result, the failures, and what it costs.

[THE LIMITS]
Careful, two limits. Other people's views don't guarantee mine. And the sample is small: ten videos per search. That's why you need to redo this research before every video. Topics change fast.

[THE GIFT]
The full prompt is free, in English and French, in the description. Put your theme in the brackets, paste it into your AI, and you'll have your own ranking in a few minutes. This research cost me zero extra. Subscribe to see if number one lives up to its promise.

## Plan visuel (texte neutre en langue autant que possible)
Résultat : tableau des 10 sujets qui se remplit (notes animées) → compteur « 277 858 vues · 4 jours ». Pourquoi : rappel tampon « REFUSÉ » de la vidéo 1. Étape 1 : barre de recherche recréée qui tape « claude mcp » + vraies suggestions qui tombent. Étape 2 : 10 lignes de résultats (vues, date) sans miniatures + calcul vues/jour + barre médiane vs moyenne. Étape 3 : 3 jauges. Classement : tableau final, n°1 surligné. Gagnant : logos génériques « Claude ↔ MCP ↔ Blender » (sans logos de marques : texte). Cadeau : le fichier prompt dans l'éditeur.
