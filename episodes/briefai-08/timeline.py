import json, wave
FPS = 30
al = json.load(open('align.json')); ep = json.load(open('segments.json'))
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
S = lambda img, **k: dict(kind='shot', img=img, **k)
V = lambda src, **k: dict(kind='clip', src=src, **k)
T = lambda lines, **k: dict(kind='title', lines=lines, **k)
CH = lambda n, who, budget, method: dict(kind='chapter', n=n, who=who, budget=budget, method=method)
FULL = [0, 0, 1568, 751]
plan = {
 'seg01': [(0, S('01_explore.jpg', url='google.com/travel/explore', cam0=[340, 60, 1228, 691], cam=[560, 150, 900, 430], scroll=True))],
 'seg02': [(0, V('mcr_10883708.mp4', tag='Manchester')),
           (1, S('02_vols.jpg', url='google.com/travel/flights', cam0=FULL, cam=[355, 320, 845, 210], hl=[362, 328, 832, 72], label='66 € aller-retour')),
           (2, S('02_vols.jpg', url='google.com/travel/flights', cam0=[355, 320, 845, 210], cam=[355, 320, 845, 210], hl=[670, 348, 100, 22], label='Beauvais · sans bagage cabine')),
           (3, S('02_vols.jpg', url='google.com/travel/flights', cam0=[355, 320, 845, 210], cam=[355, 320, 845, 210], hl=[362, 405, 832, 58], label='92 € depuis CDG'))],
 'seg03': [(0, T([['3 voyages', 'w'], ['3 méthodes', 'c']]))],
 'seg04': [(0, CH(1, 'Solo', '< 500 €', 'trier par prix · note 8+')),
           (1, S('03_booking_solo.jpg', url='booking.com', cam0=FULL, cam=[540, 180, 700, 380], hl=[560, 228, 245, 28], label='prix le plus bas')),
           (2, S('03_booking_solo.jpg', url='booking.com', cam0=[540, 180, 700, 380], cam=[555, 325, 680, 235], hl=[1100, 440, 115, 45], label='228 € · 5 nuits · 8,6'))],
 'seg05': [(0, CH(2, 'Couple', '1 000 €', 'une seule question à une IA')),
           (1, S('07_ai_prompt.jpg', cam0=FULL, cam=[560, 55, 540, 120], hl=[575, 68, 510, 88]))],
 'seg06': [(0, S('08_ai_activites.jpg', cam0=FULL, cam=[470, 30, 640, 250], hl=[486, 62, 600, 205])),
           (2, S('08_ai_activites.jpg', cam0=[470, 30, 640, 250], cam=[480, 470, 600, 130], hl=[510, 548, 525, 30], label='fermée l\'an dernier')),
           (3, S('08_ai_activites.jpg', cam0=[480, 470, 600, 130], cam=[480, 390, 600, 90], hl=[510, 400, 525, 64], label='jour sans match'))],
 'seg07': [(0, S('09_ai_total.jpg', cam0=FULL, cam=[470, 160, 640, 260], hl=[486, 377, 600, 24], label='955 € pour deux')),
           (1, S('07_ai_prompt.jpg', cam0=FULL, cam=[470, 270, 600, 90], hl=[486, 282, 555, 60], label='« estimations »')),
           (2, S('04_booking_couple.jpg', url='booking.com', cam0=FULL, cam=[555, 325, 680, 265], hl=[1050, 455, 165, 75], label='prix réel, à vérifier'))],
 'seg08': [(0, CH(3, 'Famille de 4', '2 500 €', 'la carte d\'abord')),
           (2, S('06_maps_halal.jpg', url='google.com/maps', cam0=FULL, cam=[0, 0, 1200, 751], hl=[70, 110, 325, 560], label='restaurants halal')),
           (3, S('05_booking_famille.jpg', url='booking.com', cam0=FULL, cam=[555, 325, 680, 290], hl=[1150, 340, 70, 40], label='9,2 · 450 m du centre')),
           (4, S('05_booking_famille.jpg', url='booking.com', cam0=[555, 325, 680, 290], cam=[555, 325, 680, 290], hl=[788, 488, 425, 82], label='1 059 € · enfants gratuits'))],
 'seg09': [(0, V('mcr_10883708.mp4', start=300, tag='Manchester'))],
 'seg10': [(0, S('02_vols.jpg', url='google.com/travel/flights', cam0=FULL, cam=[880, 530, 330, 120], hl=[912, 548, 265, 85], label='41 € le 27')),
           (2, dict(kind='end'))]}
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
out[-1]['dur'] += round(4.0 * FPS)
json.dump({'shots': out, 'total': round((t0 + 4.0) * FPS), 'segs': segsout}, open('/home/claude/remotion-test/src/tl8.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(t0 + 4, 1), 's', len(out), 'plans')
