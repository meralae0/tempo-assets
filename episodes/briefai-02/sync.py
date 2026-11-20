"""Synchro FR/EN phrase par phrase : chaque phrase dure max(fr, en) + 0,25 s ; la langue la plus courte reçoit du silence après sa phrase."""
import sys, json, wave, numpy as np
sys.path.insert(0, '../../tools'); import assemble as A
ep = json.load(open('segments.json')); GROUPS = {'seg04': [[3, 4]]}; SR = 24000; align = {}
def rd(p): w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16)
def wr(p, a):
    w = wave.open(p, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.astype(np.int16).tobytes()); w.close()
for seg in ep['segments']:
    sid = seg['id']; ch = {}
    for l in ['fr', 'en']:
        src = f'audio/{l}/t_{sid}.wav'; a = rd(src); st = A._sentence_times_dp(src, seg['text'][l])
        ch[l] = (a, st)
    n_s = len(seg['text']['fr']); units = []; i = 0; G = GROUPS.get(sid, [])
    while i < n_s:
        g = next((g for g in G if g[0] == i), None); j = g[-1] if g else i; units.append((i, j)); i = j + 1
    out = {'fr': [], 'en': []}; starts = {'fr': [], 'en': []}; t = 0.0
    for (i, j) in units:
        cs = {}
        for l in ['fr', 'en']:
            a, st = ch[l]; cs[l] = a[int(st[i][0] * SR):int(st[j][1] * SR)]
        n = max(len(cs['fr']), len(cs['en'])) + int(0.25 * SR)
        for l in ['fr', 'en']:
            c = cs[l]; out[l].append(np.concatenate([c, np.zeros(n - len(c), np.int16)]))
            txt = seg['text'][l][i:j + 1]; tot = sum(len(x) for x in txt); acc = 0
            for x in txt: starts[l].append(t + len(c) / SR * acc / tot); acc += len(x)
        t += n / SR
    for l in ['fr', 'en']:
        wr(f'audio/{l}/{sid}.wav', np.concatenate(out[l])); align[f'{l}_{sid}'] = starts[l]
    print(sid, round(t, 2))
json.dump(align, open('align.json', 'w'))
