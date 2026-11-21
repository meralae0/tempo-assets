import json, wave, sys
FPS = 30
al = json.load(open('align.json')); ep = json.load(open('segments.json'))
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
S = lambda img, **k: dict(kind='shot', img=img, **k)
T = lambda lines, **k: dict(kind='title', lines=lines, **k)
P = '02_produit.jpg'; V = '05_verdict.jpg'; Q = '03_question.jpg'; O = '01_offres.jpg'
PRICE = [780, 505, 420, 110]; FULL = [0, 0, 1568, 705]
plan = {
 'seg01': [(0, S('grid_tall.jpg', ih=1440, url='amazon.fr', cam0=[0, 0, 1568, 705], cam=[0, 735, 1568, 705], scroll=True)),
           (1.55, S(O, url='amazon.fr', cam0=FULL, cam=[270, 215, 440, 330], hl=[283, 417, 190, 42]))],
 'seg02': [(0, S(P, url='amazon.fr', cam0=[780, 250, 420, 200], cam=PRICE, scroll=True, contNext=True)),
           (2, S(P, url='amazon.fr', cam=PRICE, cam0=PRICE, cont=True, contNext=True, hl=[794, 573, 245, 18], label='« prix conseillé »')),
           (3, S(P, url='amazon.fr', cam=PRICE, cam0=PRICE, cont=True, hl=[794, 590, 250, 18], label='prix le plus bas · 30 jours')),
           (4, T([['−14 %', 'g']]))],
 'seg03': [(0, S('qc1.jpg', url='quechoisir.org', cam0=FULL, cam=[320, 180, 640, 100], hl=[326, 210, 605, 40])),
           (1, S('qc2.jpg', url='quechoisir.org', cam0=[320, 80, 630, 300], cam=[320, 190, 630, 160], scroll=True, contNext=True, hl=[326, 204, 218, 22], label='314 commerçants')),
           (2, S('qc2.jpg', url='quechoisir.org', cam0=[320, 190, 630, 160], cam=[320, 190, 630, 160], cont=True, hl=[326, 204, 560, 46], label='30 % des promos'))],
 'seg04': [(0, S(P, url='amazon.fr/dp/B094WLFGD3', cam0=FULL, cam=[160, 170, 1250, 520])),
           (1, S(P, url='amazon.fr/dp/B094WLFGD3', urlHl='Ctrl + C', cam0=[160, 170, 1250, 520], cam=[160, 170, 1250, 520])),
           (1.55, S(Q, cam0=FULL, cam=[505, 280, 560, 130], typing=True))],
 'seg05': [(0, S('04_recherche.jpg', cam0=FULL, cam=[470, 60, 640, 220])),
           (1, S(V, cam0=[478, 60, 570, 200], cam=[478, 270, 570, 70], scroll=True, contNext=True, hl=[486, 298, 550, 28])),
           (2, S(V, cam0=[478, 270, 570, 70], cam=[478, 335, 570, 75], cont=True, contNext=True, hl=[486, 341, 550, 30])),
           (3, S(V, cam0=[478, 335, 570, 75], cam=[478, 410, 570, 65], cont=True, hl=[486, 419, 550, 48], label='attendre'))],
 'seg06': [(0, S(V, cam0=[478, 410, 570, 65], cam=[478, 470, 570, 50], hl=[486, 480, 510, 30])),
           (1, S(V, cam0=[478, 470, 570, 50], cam=[478, 270, 590, 210], hl=[872, 312, 128, 18], cursor=[[800, 420], [936, 321]], click=True))],
 'seg07': [(0, S(O, url='amazon.fr', cam0=[270, 215, 440, 330], cam=FULL)), (1, dict(kind='end'))]}
out = []; t0 = 0.0; segsout = []
for seg in ep['segments']:
    sid = seg['id']; D = dur(f'audio/fr/{sid}.wav'); st = al[f'fr_{sid}']
    def at(a):
        k = int(a); f = a - k; s0 = st[k]; s1 = st[k + 1] if k + 1 < len(st) else D; return s0 + f * (s1 - s0)
    items = plan[sid]; starts = [0.0 if i == 0 else at(a) for i, (a, _) in enumerate(items)] + [D]
    for i, (a, spec) in enumerate(items):
        d = dict(spec); d['from'] = round((t0 + starts[i]) * FPS); d['dur'] = round((starts[i + 1] - starts[i]) * FPS)
        out.append(d)
    segsout.append([sid, round(t0, 2)]); t0 += D
END = 4.0
out[-1]['dur'] += round(END * FPS)
total = round((t0 + END) * FPS)
json.dump({'shots': out, 'total': total, 'segs': segsout}, open('/home/claude/remotion-test/src/tl7.json', 'w'), ensure_ascii=False, indent=1)
print('total', total / FPS, 's', len(out), 'plans')
