"""Régénère le SRT d'un épisode depuis timing_<lang>.json, en blocs de 2 lignes max (42 car./ligne).
Usage: python3 srt.py <episode_dir> <lang>"""
import sys, os, json, re

def t(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',')

def chunks(txt, width=42):
    txt = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', txt); txt = re.sub(r' ([;:!?%])', '\u00a0\\1', txt)
    words = txt.split(' '); lines = []; cur = ''
    for w in words:
        if len(cur) + len(w) + 1 <= width: cur = (cur + ' ' + w).strip()
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return [lines[i:i + 2] for i in range(0, len(lines), 2)]

def main(ep_dir, lang):
    ep = json.load(open(os.path.join(ep_dir, 'segments.json'))); tm = json.load(open(os.path.join(ep_dir, f'timing_{lang}.json')))
    out = []; n = 1
    for a, b, s in tm['subs']:
        bl = chunks(s); tot = sum(len(' '.join(x)) for x in bl); c = a
        for x in bl:
            d = (b - a) * len(' '.join(x)) / max(1, tot)
            out.append(f'{n}\n{t(c)} --> {t(min(b, c + d) - 0.02)}\n' + '\n'.join(x).replace('\u00a0', ' ') + '\n'); n += 1; c += d
    open(os.path.join(ep_dir, f'{ep["slug"]}_{lang}.srt'), 'w', encoding='utf-8').write('\n'.join(out))
    print(lang, n - 1, 'blocs')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
