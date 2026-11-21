import json, wave, sys, os
FPS = 30
ep = json.load(open('segments.json'))
FAKE = '--fake' in sys.argv
if FAKE:
    al = {}; durs = {}
    for s in ep['segments']:
        tx = s['text']['fr']; ch = [len(t) for t in tx]; tot = sum(ch); D = tot / 14.5 + 0.6; acc = 0; st = []
        for c in ch: st.append(acc / tot * (D - 0.4)); acc += c
        al['fr_' + s['id']] = st; durs[s['id']] = D
else:
    al = json.load(open('align.json'))
def dur(sid):
    if FAKE: return durs[sid]
    w = wave.open(f'audio/fr/{sid}.wav'); return w.getnframes() / w.getframerate()
S = lambda img, **k: dict(kind='shot', img=img, **k)
T = lambda lines, **k: dict(kind='title', lines=lines, **k)
ST = lambda **k: dict(kind='stat', **k)
L = lambda **k: dict(kind='list', **k)
P = '02_produit.jpg'; V = '05_verdict.jpg'; Q = '03_question.jpg'; PRICE = [780, 505, 420, 110]
EU = 'Commission européenne · DGCCRF (via UFC-Que Choisir)'
plan = {
 'seg01': [(0, dict(kind='cal')),
           (1, ST(value='151', unit=' €', c='c', label='budget moyen prévu par les Français', src='Custplace, 6 nov. 2026')),
           (2, ST(value='1 / 3', c='r', label='des promos en ligne hors des règles', over='Black Friday 2025', src=EU)),
           (3, T([['vraie promo ?', 'g'], ['ou fausse ?', 'r']])),
           (4, T([['30 secondes', 'c'], ["avec l'IA", 'w']]))],
 'seg02': [(0, T([['Black Friday · Cyber Monday 2025', 'w'], ["l'enquête européenne", 'c']])),
           (1, ST(count=314, c='c', label='vendeurs en ligne contrôlés', src=EU)),
           (2, ST(value='≈ 30', unit=' %', c='r', ring=0.3, label="des promos hors des règles d'affichage", src=EU)),
           (3, L(title='18 % des vendeurs : des pièges', c='w', ic='r', mark='!', items=['faux compte à rebours', 'faux « stock presque épuisé »'], src=EU))],
 'seg03': [(0, L(title='Les techniques', c='w', ic='r', items=['un prix de référence gonflé', 'un prix monté juste avant la promo', 'un prix de comparaison sans source'], reveal_at=[1, 2, 3], src='UFC-Que Choisir'))],
 'seg04': [(0, L(title='La règle', c='g', ic='g', mark='✓', items=['réduction = prix le plus bas des 30 derniers jours', 'autre prix de comparaison : source obligatoire'], reveal_at=[1, 2], src='DGCCRF'))],
 'seg05': [(0, S('01_offres.jpg', url='amazon.fr', cam=[270, 215, 440, 330], src='Amazon.fr, 21 nov. 2026')),
           (1, S('01_offres.jpg', url='amazon.fr', cam=[270, 215, 440, 330], hl=[283, 417, 190, 42], label='−29 %')),
           (2, S(P, url='amazon.fr', cam=PRICE)),
           (3, S(P, url='amazon.fr', cam=PRICE, hl=[794, 590, 250, 18], label='30 derniers jours : −14 %')),
           (4, S(P, url='amazon.fr', cam=PRICE, hl=[794, 573, 335, 18], label='−29 % = sur le prix conseillé'))],
 'seg06': [(0, T([['historique du prix', 'w'], ['+ autres vendeurs', 'c']])),
           (1, T([['à la main', 'w'], ['ça prend du temps', 'r']])),
           (2, T([["avec l'IA", 'c'], ['30 secondes', 'g']])),
           (3, ST(value='46', unit=' %', c='v', ring=0.46, label="des acheteurs du Black Friday ont déjà utilisé l'IA", src='Custplace, 6 nov. 2026'))],
 'seg07': [(0, S(P, url='amazon.fr/dp/B094WLFGD3', urlHl='Ctrl + C', cam=[160, 170, 1250, 520])),
           (1, T([['Claude · ChatGPT · Gemini', 'c'], ['une IA qui cherche sur le web', 'w']])),
           (2, S(Q, cam=[505, 280, 560, 130], typing=True)),
           (3, S(Q, cam=[505, 280, 560, 130], hl=[525, 315, 485, 52], label='historique + autres vendeurs + sources', cursor=[[800, 400], [1033, 382]], click=True))],
 'seg08': [(0, S(V, cam=[478, 270, 570, 70], hl=[486, 281, 550, 15], label='vraie promo, mais pas la meilleure')),
           (1, S(V, cam=[478, 270, 570, 70], hl=[486, 298, 550, 28], label='54,99 € au Black Friday 2024')),
           (2, S(V, cam=[478, 335, 570, 75], hl=[486, 341, 550, 30], label='un autre site : 54,99 €')),
           (3, S(V, cam=[478, 410, 570, 65], hl=[486, 419, 550, 48], label='conseil : attendre'))],
 'seg09': [(0, T([["l'IA peut", 'w'], ['se tromper', 'r']])),
           (1, S(V, cam=[478, 470, 570, 50], hl=[486, 480, 510, 30], label="« je n'ai pas pu ouvrir la page »")),
           (2, S(P, url='amazon.fr', cam=[780, 255, 400, 170], hl=[794, 365, 355, 50], label='même modèle, même couleur'))],
 'seg10': [(0, T([['Black Friday', 'w'], ['quelques jours', 'c']])),
           (1, T([['fausses promos', 'r'], ["toute l'année", 'w']])),
           (2, dict(kind='summary')), (3, dict(kind='gift')), (4, dict(kind='end'))]}
out = []; t0 = 0.0; segsout = []
for seg in ep['segments']:
    sid = seg['id']; D = dur(sid); st = al[f'fr_{sid}']
    def at(a):
        k = int(a); f = a - k; s0 = st[k]; s1 = st[k + 1] if k + 1 < len(st) else D; return s0 + f * (s1 - s0)
    items = plan[sid]; starts = [0.0 if i == 0 else at(a) for i, (a, _) in enumerate(items)] + [D]
    for i, (a, spec) in enumerate(items):
        d = dict(spec); d['from'] = round((t0 + starts[i]) * FPS); d['dur'] = round((starts[i + 1] - starts[i]) * FPS)
        if 'reveal_at' in d: d['reveal'] = [round((at(k) - starts[i]) * FPS) for k in d.pop('reveal_at')]
        out.append(d)
    segsout.append([sid, round(t0, 2)]); t0 += D
END = 5.0
out[-1]['dur'] += round(END * FPS)
total = round((t0 + END) * FPS)
json.dump({'shots': out, 'total': total, 'segs': segsout}, open('/home/claude/remotion-test/src/tl6.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(total / FPS, 1), 's', len(out), 'plans')
