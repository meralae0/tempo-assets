import json, wave
FPS = 30
al = json.load(open('align.json')); ep = json.load(open('segments.json'))
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
S = lambda img, **k: dict(kind='shot', img=img, **k)
V = lambda src, **k: dict(kind='clip', src=src, **k)
T = lambda lines, **k: dict(kind='title', lines=lines, **k)
CH = lambda n, who, budget, method: dict(kind='chapter', n=n, who=who, budget=budget, method=method)
F = [0, 0, 1568, 751]
FL = 'google.com/travel/flights'; BK = 'booking.com'
plan = {
 'seg01': [(0, V('mcr_10883708.mp4', tag='Paris → ?')), (1, T([['By hand', 'w'], ['vs AI agent', 'c']]))],
 'seg02': [(0, S('07_ai_prompt.jpg', cam0=F, cam=[560, 55, 540, 120], hl=[575, 68, 510, 88], label='chatbot: answers')),
           (2, S('01_explore.jpg', url='google.com/travel/explore', cam0=F, cam=[420, 90, 1000, 560], label='agent: acts', hl=[700, 300, 400, 200]))],
 'seg03': [(0, S('02_vols.jpg', url=FL, cam0=F, cam=[340, 60, 880, 470])), (0.35, S('03_booking_solo.jpg', url=BK, cam0=F, cam=[320, 150, 930, 600])),
           (0.7, S('06_maps_halal.jpg', url='google.com/maps', cam0=F, cam=[0, 0, 1250, 751])), (1, S('08_ai_activites.jpg', cam0=F, cam=[470, 30, 640, 330]))],
 'seg04': [(0, T([['Mission', 'c'], ['Paris · Dec 26–31', 'w']])), (1, T([['3 plans', 'w'], ['solo · couple · family', 'c']]))],
 'seg05': [(0, S('01_explore.jpg', url='google.com/travel/explore', cam0=[340, 60, 1228, 691], cam=[560, 150, 900, 430], scroll=True)),
           (1, S('02_vols.jpg', url=FL, cam0=F, cam=[355, 320, 845, 210], hl=[362, 328, 832, 72], label='€66 return')),
           (2, S('02_vols.jpg', url=FL, cam0=[355, 320, 845, 210], cam=[355, 320, 845, 210], hl=[670, 348, 100, 22], label='Beauvais · no cabin bag')),
           (3, S('02_vols.jpg', url=FL, cam0=[355, 320, 845, 210], cam=[355, 320, 845, 210], hl=[362, 405, 832, 58], label='€92 from CDG'))],
 'seg06': [(0, S('02_vols.jpg', url=FL, cam0=F, cam=[880, 530, 330, 120], hl=[912, 548, 265, 85], label='€41 on the 27th'))],
 'seg07': [(0, S('03_booking_solo.jpg', url=BK, cam0=F, cam=[540, 180, 700, 380], hl=[560, 228, 245, 28], label='sorted by price')),
           (1, S('03_booking_solo.jpg', url=BK, cam0=[540, 180, 700, 380], cam=[555, 325, 680, 235], hl=[1100, 440, 115, 45], label='€228 · 5 nights · 8.6')),
           (2, S('05_booking_famille.jpg', url=BK, cam0=F, cam=[555, 325, 680, 290], hl=[788, 488, 425, 82], label='9.2 · kids stay free'))],
 'seg08': [(0, S('06_maps_halal.jpg', url='google.com/maps', cam0=F, cam=[0, 0, 1250, 751], hl=[70, 110, 325, 560], label='halal restaurants')),
           (1, S('07_ai_prompt.jpg', cam0=F, cam=[560, 55, 540, 120], hl=[575, 68, 510, 88], label='AI assistant + web search')),
           (2, S('08_ai_activites.jpg', cam0=F, cam=[480, 470, 600, 130], hl=[510, 548, 525, 30], label='closed all holiday'))],
 'seg09': [(0, T([['Where AI wins', 'c']])), (1, S('08_ai_activites.jpg', cam0=F, cam=[470, 30, 640, 250], hl=[486, 62, 600, 205], label='combos · fees · hours · math'))],
 'seg10': [(0, T([['The honest part', 'r']])), (1, S('07_ai_prompt.jpg', cam0=F, cam=[470, 270, 600, 90], hl=[486, 282, 555, 60], label='"estimates"')),
           (2, S('04_booking_couple.jpg', url=BK, cam0=F, cam=[555, 325, 680, 265], hl=[1050, 455, 165, 75], label='real price')),
           (3, T([['It never pays', 'w'], ['you decide', 'c']]))],
 'seg11': [(0, T([['€500 · €1,000 · €2,500', 'g'], ['3 complete plans', 'w']])), (1, dict(kind='end'))]}
out = []; t0 = 0.0; segsout = []
for seg in ep['segments']:
    sid = seg['id']; D = dur(f'audio/en/{sid}.wav'); st = al[f'en_{sid}']
    def at(a):
        k = int(a); f = a - k; s0 = st[k]; s1 = st[k + 1] if k + 1 < len(st) else D; return s0 + f * (s1 - s0)
    items = plan[sid]; starts = [0.0 if i == 0 else at(a) for i, (a, _) in enumerate(items)] + [D]
    for i, (a, spec) in enumerate(items):
        d = dict(spec); d['from'] = round((t0 + starts[i]) * FPS); d['dur'] = round((starts[i + 1] - starts[i]) * FPS)
        out.append(d)
    segsout.append([sid, round(t0, 2)]); t0 += D
out[-1]['dur'] += round(4.0 * FPS)
json.dump({'shots': out, 'total': round((t0 + 4.0) * FPS), 'segs': segsout}, open('/home/claude/remotion-test/src/tl9.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(t0 + 4, 1), 's', len(out))
