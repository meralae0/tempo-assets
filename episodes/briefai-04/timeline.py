import json, wave
FPS = 30; END = 5.0
ep = json.load(open('segments.json'))['segments']; al = json.load(open('align.json'))
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
t = 0.0; segs = []
for s in ep:
    D = dur(f"audio/fr/{s['id']}.wav")
    segs.append({'id': s['id'], 'from': round(t * FPS), 'dur': round(D * FPS), 'st': [round(x * FPS) for x in al['fr_' + s['id']]], 't0': round(t, 2)})
    t += D
total = round((t + END) * FPS)
json.dump({'segs': segs, 'total': total, 'endFrom': round(t * FPS)}, open('/home/claude/remotion-test/src/tl4.json', 'w'), indent=1)
print('total', round(t + END, 1), 's')
