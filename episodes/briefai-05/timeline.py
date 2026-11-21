import json, wave
FPS = 30
al = json.load(open('align.json')); ep = json.load(open('segments.json'))
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
S = lambda img, **k: dict(kind='shot', img=img, **k)
T = lambda lines, **k: dict(kind='title', lines=lines, **k)
P = '02_produit.jpg'; V = '05_verdict.jpg'; Q = '03_question.jpg'
PRICE = [780, 505, 420, 110]
plan = {
 'seg01': [(0, S('01_offres.jpg', url='amazon.fr', cam=[270, 215, 440, 330], hl=[283, 417, 190, 42], label='−29 % ?')),
           (1, S(P, url='amazon.fr', cam=PRICE, hl=[794, 590, 250, 18], label='En vrai : −14 %')),
           (2, S(V, cam=[478, 330, 570, 85], hl=[486, 341, 550, 62], label='Moins chère ailleurs')),
           (3, T([['30 secondes', 'c'], ['pour vérifier une promo', 'w']]))],
 'seg02': [(0, S(P, url='amazon.fr', cam=PRICE)),
           (1, S(P, url='amazon.fr', cam=PRICE, hl=[794, 573, 335, 18], label='calculé sur le « prix conseillé »')),
           (2, S(P, url='amazon.fr', cam=PRICE, hl=[794, 590, 250, 18], label='la règle : prix le plus bas des 30 jours')),
           (3, S(P, url='amazon.fr', cam=PRICE, hl=[990, 590, 54, 18], label='65 €')),
           (4, T([['−14 %', 'g'], ['la vraie remise', 'w']]))],
 'seg03': [(0, S(P, url='amazon.fr/dp/B094WLFGD3', urlHl='Ctrl + C', cam=[160, 170, 1250, 520]))],
 'seg04': [(0, T([['Claude · ChatGPT · Gemini', 'c'], ['une IA qui cherche sur le web', 'w']])),
           (1, S(Q, cam=[505, 280, 560, 130], typing=True)),
           (2, S(Q, cam=[505, 280, 560, 130], hl=[525, 315, 485, 34], label='historique + autres vendeurs')),
           (3, S(Q, cam=[505, 280, 560, 130], hl=[525, 333, 485, 33], label='3 lignes + sources', cursor=[[800, 400], [1033, 382]], click=True))],
 'seg05': [(0, S('04_recherche.jpg', cam=[470, 60, 640, 220], hl=[486, 248, 200, 18], label='elle cherche sur le web')),
           (1, S(V, cam=[478, 270, 570, 70], hl=[486, 281, 550, 15], label='vraie promo, mais pas la meilleure')),
           (2, S(V, cam=[478, 270, 570, 70], hl=[486, 298, 550, 28], label='54,99 € au Black Friday 2024')),
           (3, S(V, cam=[478, 335, 570, 75], hl=[486, 341, 550, 30], label='un autre site : 54,99 €')),
           (4, S(V, cam=[478, 410, 570, 65], hl=[486, 419, 550, 48], label='Verdict : attendre'))],
 'seg06': [(0, T([['2 pièges', 'r']])),
           (1, T([["1 · l'IA peut", 'w'], ['se tromper', 'r']])),
           (2, S(V, cam=[478, 470, 570, 50], hl=[486, 480, 510, 30], label="elle n'a pas pu ouvrir la page")),
           (3, S(V, cam=[478, 270, 590, 210], hl=[872, 312, 128, 18], label='clique sur les sources')),
           (4, S(P, url='amazon.fr', cam=[780, 255, 400, 170], hl=[794, 365, 355, 50], label='même modèle, même couleur')),
           (5, T([['sinon', 'w'], ['ça ne vaut rien', 'r']]))],
 'seg07': [(0, dict(kind='summary')), (1, dict(kind='gift')), (2, dict(kind='end'))]}
steps = {'seg03': 1, 'seg04': 2, 'seg05': 3}
titles = {'seg03': 'Copie le lien', 'seg04': "Demande à l'IA", 'seg05': 'Lis le verdict'}
out = []; t0 = 0.0; segsout = []
for seg in ep['segments']:
    sid = seg['id']; D = dur(f'audio/fr/{sid}.wav'); st = al[f'fr_{sid}']
    def at(a):
        k = int(a); f = a - k; s0 = st[k]; s1 = st[k + 1] if k + 1 < len(st) else D; return s0 + f * (s1 - s0)
    items = plan[sid]; starts = [0.0 if i == 0 else at(a) for i, (a, _) in enumerate(items)] + [D]
    for i, (a, spec) in enumerate(items):
        d = dict(spec); d['from'] = round((t0 + starts[i]) * FPS); d['dur'] = round((starts[i + 1] - starts[i]) * FPS)
        if sid in steps: d['step'] = steps[sid]; d['stepTitle'] = titles[sid]
        out.append(d)
    segsout.append([sid, round(t0, 2)]); t0 += D
END = 5.0
out[-1]['dur'] += round(END * FPS)
total = round((t0 + END) * FPS)
json.dump({'shots': out, 'total': total, 'segs': segsout}, open('/home/claude/remotion-test/src/tl5.json', 'w'), ensure_ascii=False, indent=1)
print('total', total / FPS, 's', len(out), 'plans')
