import json, re, wave
seg = json.load(open('segments.json'))['segments']; al = json.load(open('align.json'))
tl = {s['id']: s for s in json.load(open('/home/claude/remotion-test/src/tl4.json'))['segs']}
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
def fmt(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; ms = int(round((s % 1) * 1000)); ms = min(ms, 999); return f"{h:02}:{m:02}:{int(s):02},{ms:03}"
def chunks(txt, mx=84):
    if len(txt) <= mx: return [txt]
    parts = re.split(r'(?<=[,:;.»])\s+', txt); out = ['']
    for p in parts:
        if out[-1] and len(out[-1]) + 1 + len(p) > mx: out.append(p)
        else: out[-1] = (out[-1] + ' ' + p).strip()
    return out
def wrap(c, w=42):
    if len(c) <= w: return c
    i = c.rfind(' ', 0, len(c) // 2 + 8); i = i if i > 0 else c.find(' ', len(c) // 2)
    return c[:i] + '\n' + c[i + 1:]
for l in ['fr', 'en']:
    cues = []
    for s in seg:
        sid = s['id']; o = tl[sid]['t0']; st = al[f'{l}_{sid}']; D = dur(f'audio/{l}/{sid}.wav')
        for k, txt in enumerate(s['text'][l]):
            a = o + st[k]; b = o + (st[k + 1] if k + 1 < len(st) else D - 0.2)
            cs = chunks(txt); tot = sum(len(c) for c in cs); t = a
            for c in cs:
                e = t + (b - a) * len(c) / tot; cues.append((t, e - 0.05, wrap(c))); t = e
    with open(f'out/briefai-04_{l}.srt', 'w') as f:
        for i, (a, b, c) in enumerate(cues, 1): f.write(f"{i}\n{fmt(a)} --> {fmt(b)}\n{c}\n\n")
    print(l, len(cues))
print({s['id']: round(tl[s['id']]['t0']) for s in seg})
