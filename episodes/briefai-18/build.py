# EN5 "Same app, 3 AIs" — screenshots of the real chats + app renders, camera moves, rings, pills, wipes, captions
# rings, pills, chapter wipes and word-by-word captions. timing.json = {"A1":[a,b], "V":[[a,b] x10], "A2":[a,b]} in vids_export.mp4
import sys, os, json, math, subprocess, re
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from gfx_ai import *
from leap import *
from PIL import Image, ImageDraw, ImageFilter
EP = '/home/claude/tempo-assets/episodes/briefai-18'; B = '/home/claude/b18'; O = B + '/seg'; os.makedirs(O, exist_ok=True)
T = json.load(open(EP + '/timing.json')); VD = [b - a for a, b in T['V']]
GPT = (16, 163, 127); CLA = (217, 119, 87); GEM = (66, 133, 244); AMB = (255, 190, 60)
AIS = [('ChatGPT', GPT), ('Claude', CLA), ('Gemini', GEM)]
SFX = []

def fin(t, a, d=.4): return max(0., min(1., ease((t - a) / d)))

# ---------- captures ----------
CW, CH = 1568, 705; PH = int(CW * 9 / 16) + 1; PAD = (PH - CH) // 2
def load(name):
    im = Image.open(f'{EP}/caps/{name}.jpg').convert('RGB')
    if name.startswith('chatgpt'):  # hide chat history sidebar
        reg = im.crop((0, 0, 208, CH)).filter(ImageFilter.GaussianBlur(14)); im.paste(reg, (0, 0))
    if name.startswith('gemini'):   # profile photo bottom-left
        reg = im.crop((0, 630, 60, CH)).filter(ImageFilter.GaussianBlur(12)); im.paste(reg, (0, 630))
    bgi = im.resize((98, 47)).filter(ImageFilter.GaussianBlur(3)).resize((CW, PH), Image.BILINEAR)
    bgi = Image.blend(bgi, Image.new('RGB', (CW, PH), (6, 7, 12)), 0.6); bgi.paste(im, (0, PAD)); return bgi
_C = {}
def C(n):
    if n not in _C: _C[n] = load(n)
    return _C[n]
WIDE = (0, 0, CW, PH)
def Z(x0, y0, x1, y1, m=30):
    x0 -= m; x1 += m; y0 += PAD - m; y1 += PAD + m
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; w = max(x1 - x0, (y1 - y0) * 16 / 9); w = min(w, CW); h = w * 9 / 16
    x0 = max(0, min(CW - w, cx - w / 2)); y0 = max(0, min(PH - h, cy - h / 2)); return (x0, y0, x0 + w, y0 + h)
def boxat(t, keys):
    box = keys[0][1]
    for i, (tk, b) in enumerate(keys):
        if t >= tk:
            prev = keys[i - 1][1] if i else b; k = eio((t - tk) / 0.8); box = tuple(lerp(p, q, k) for p, q in zip(prev, b))
    return box
class Ctx:
    def __init__(s, box): s.box = box
    def P(s, x, y):
        x0, y0, x1, y1 = s.box; k = W / (x1 - x0); return ((x - x0) * k, (y + PAD - y0) * k)
    def R(s, x0, y0, x1, y1):
        a = s.P(x0, y0); b = s.P(x1, y1); return (a[0], a[1], b[0], b[1])

# ---------- overlays ----------
def pill(im, xy, txt, col=ORANGE, a=1.0, size=40, tc=WHITE, anchor='mm', icon=None):
    if a <= 0: return
    f = sg(size, 700); d0 = ImageDraw.Draw(im); b = d0.textbbox((0, 0), txt, font=f); tw = b[2] - b[0]
    ic = size + 14 if icon else 0; w, h = tw + 64 + ic, int(size * 1.9)
    p = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((15, 21, w + 15, h + 21), radius=h // 2, fill=(0, 0, 0, 110)); p = p.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((15, 15, w + 15, h + 15), radius=h // 2, fill=col + (255,)); x = 47
    if icon:
        cx, cy, r = x + size // 2, 15 + h // 2, size // 2; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
        if icon == 'check': d.line((cx - r * .45, cy, cx - r * .1, cy + r * .38, cx + r * .5, cy - r * .38), fill=col + (255,), width=max(4, r // 4), joint='curve')
        else:
            k = r * .42; d.line((cx - k, cy - k, cx + k, cy + k), fill=col + (255,), width=6); d.line((cx - k, cy + k, cx + k, cy - k), fill=col + (255,), width=6)
        x += ic
    d.text((x, 15 + h / 2), txt, font=f, fill=tc + (255,), anchor='lm')
    s = pop(a * 0.35 + 0.0001, 0) if a < 1 else 1
    if s <= 0: return
    if s != 1: p = p.resize((max(1, int(p.width * s)), max(1, int(p.height * s))), Image.LANCZOS)
    if a < 1: p.putalpha(p.getchannel('A').point(lambda v: int(v * min(1, a * 2))))
    x, y = xy
    if anchor == 'mm': x -= p.width / 2; y -= p.height / 2
    elif anchor == 'lm': y -= p.height / 2
    elif anchor == 'rm': x -= p.width; y -= p.height / 2
    im.alpha_composite(p, (int(x), int(y)))
def ring(im, r, col=ORANGE, a=1.0, w=6, pad=12):
    if a <= 0: return
    x0, y0, x1, y1 = r; x0 -= pad; y0 -= pad; x1 += pad; y1 += pad; s = 0.9 + 0.1 * a; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0, x1 = cx - (cx - x0) * s, cx + (x1 - cx) * s; y0, y1 = cy - (cy - y0) * s, cy + (y1 - cy) * s
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((x0, y0, x1, y1), radius=18, outline=col + (int(200 * a),), width=w + 8)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(8))); ImageDraw.Draw(im).rounded_rectangle((x0, y0, x1, y1), radius=18, outline=col + (int(255 * a),), width=w)
def spotlight(im, r, a=1.0, pad=14):
    """dim everything except the box r"""
    if a <= 0: return
    m = Image.new('L', im.size, int(150 * a)); ImageDraw.Draw(m).rounded_rectangle((r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad), radius=20, fill=0)
    im.alpha_composite(Image.merge('RGBA', [Image.new('L', im.size, 6)] * 3 + [m.filter(ImageFilter.GaussianBlur(6))]))
def badge(im, a, txt, col=AMB, icon='clock'):
    if a <= 0: return
    d = ImageDraw.Draw(im); f = mono(34, 700); b = d.textbbox((0, 0), txt, font=f); w = b[2] - b[0] + 110; x = W - w - 50; y = 46
    d.rounded_rectangle((x, y, x + w, y + 74), radius=37, fill=(12, 13, 20, int(230 * a)), outline=(255, 255, 255, int(60 * a)), width=2)
    cx, cy = x + 44, y + 37; d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=col + (int(255 * a),), width=4); d.line((cx, cy, cx, cy - 10, cx, cy, cx + 8, cy + 4), fill=col + (int(255 * a),), width=4)
    d.text((x + 78, y + 37), txt, font=f, fill=WHITE + (int(255 * a),), anchor='lm')
def topcard(im, a, kicker, title, col=ORANGE):
    if a <= 0: return
    d = ImageDraw.Draw(im); x = 50 - int(40 * (1 - a)); f1 = mono(28, 700); f2 = sg(46, 700)
    w = max(d.textbbox((0, 0), title, font=f2)[2], d.textbbox((0, 0), kicker, font=f1)[2]) + 70
    d.rounded_rectangle((x, 40, x + w, 172), radius=24, fill=(12, 13, 20, int(232 * a))); d.rounded_rectangle((x, 40, x + 10, 172), radius=5, fill=col + (int(255 * a),))
    d.text((x + 36, 78), kicker, font=f1, fill=col + (int(255 * a),), anchor='lm'); d.text((x + 36, 128), title, font=f2, fill=WHITE + (int(255 * a),), anchor='lm')
def wrapt(d, txt, f, maxw):
    out, line = [], ''
    for w in txt.split():
        t = (line + ' ' + w).strip()
        if d.textbbox((0, 0), t, font=f)[2] > maxw and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out
def typecard(im, t, txt, t0=0.2, cps=60, label='MY PROMPT', a=1.0, y=540, col=GEM, size=48):
    if a <= 0: return
    im.alpha_composite(Image.new('RGBA', im.size, (6, 7, 12, int(170 * a))))
    d = ImageDraw.Draw(im); f = sg(size, 600); lines = wrapt(d, txt, f, 1300); lh = int(size * 1.4)
    h = 130 + lh * len(lines); x0, y0 = W / 2 - 740, y - h / 2 + 30 * (1 - a)
    d.rounded_rectangle((x0, y0, x0 + 1480, y0 + h), radius=36, fill=(24, 26, 36, int(250 * a)), outline=col + (int(255 * a),), width=3)
    d.text((x0 + 70, y0 + 52), label, font=mono(28, 700), fill=col + (int(255 * a),), anchor='lm')
    n = int(max(0, t - t0) * cps); shown = 0
    for k, ln in enumerate(lines):
        part = ln[:max(0, n - shown)]; shown += len(ln) + 1
        d.text((x0 + 70, y0 + 115 + k * lh), part, font=f, fill=WHITE + (int(255 * a),), anchor='lm')
# word-by-word captions (timing ∝ characters, Vids voice is steady)
SCRIPT = {}
for blk in re.split(r'\n\n(?=[AV]\d+ \[)', open(f'{EP}/script.md').read())[1:]:
    h, b = blk.split('\n', 1); SCRIPT[h.split()[0]] = ' '.join(b.split())
def captions(im, t, D, key, lead=0.15, tail=0.35):
    words = SCRIPT[key].split(); L = sum(len(w) + 1 for w in words); span = D - lead - tail
    pos = (t - lead) / span * L
    if pos < 0 or t > D - 0.05: return
    acc = 0; idx = len(words) - 1
    for i, w in enumerate(words):
        if acc + len(w) + 1 > pos: idx = i; break
        acc += len(w) + 1
    g0 = (idx // 6) * 6; grp = words[g0:g0 + 6]
    d = ImageDraw.Draw(im); f = sg(46, 700)
    tw = sum(d.textlength(w + ' ', font=f) for w in grp); x = W / 2 - tw / 2; y = H - 92
    d.rounded_rectangle((x - 28, y - 42, x + tw + 14, y + 40), radius=22, fill=(8, 9, 14, 205))
    for i, w in enumerate(grp):
        on = g0 + i == idx; col = WHITE
        if on:
            ww = d.textlength(w, font=f); d.rounded_rectangle((x - 8, y - 32, x + ww + 8, y + 30), radius=12, fill=AMB + (255,)); col = (12, 13, 20)
        d.text((x, y), w, font=f, fill=col + (255,), anchor='lm'); x += d.textlength(w + ' ', font=f)
def wipe(im, t, kicker, title, col=ORANGE, dur=1.3):
    """full-screen chapter card that slides in then out at segment start"""
    if t > dur: return
    k_in = eio(t / 0.35); k_out = eio((t - (dur - 0.35)) / 0.35) if t > dur - 0.35 else 0
    x = int(-W * (1 - k_in) + W * k_out); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((x, 0, x + W, H), fill=(12, 13, 20, 245)); d.rectangle((x + W - 26, 0, x + W, H), fill=col + (255,))
    d.text((x + W / 2, H / 2 - 80), kicker, font=mono(44, 700), fill=col + (255,), anchor='mm')
    d.text((x + W / 2, H / 2 + 20), title, font=sg(120, 700), fill=WHITE + (255,), anchor='mm'); im.alpha_composite(lay)

# ---------- shot renderer (stills + camera) ----------
def enc_open(name):
    return subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/{name}.mp4'], stdin=subprocess.PIPE)
def render_seg(name, key, D, shots, seg_over=None):
    """shots: dict(img=name|callable(t,d)->RGBA, w, cam=[(frac, box)], over=fn(im,t,d,ctx), sfx=[(frac,name,gain)])"""
    tot = sum(s['w'] for s in shots); N = int(round(D * 30)); enc = enc_open(name); done = 0; tseg = 0.0
    for i, s in enumerate(shots):
        n = int(round(N * s['w'] / tot)) if i < len(shots) - 1 else N - done; d = n / 30
        keys = [(k * d, b) for k, b in s.get('cam', [(0, WIDE)])]
        for fr_, nm, g in s.get('sfx', []): SFX.append((name, tseg + fr_ * d, nm, g))
        if i: SFX.append((name, max(0, tseg - 0.12), 'whoosh', -18))
        for j in range(n):
            t = j / 30
            if callable(s['img']): im = s['img'](t, d)
            else:
                box = boxat(t, keys); im = C(s['img']).crop(tuple(int(v) for v in box)).resize((W, H), Image.BICUBIC).convert('RGBA')
                if s.get('over'): s['over'](im, t, d, Ctx(box))
            if i and t < 0.25:  # quick flash/zoom transition between shots
                im.alpha_composite(Image.new('RGBA', im.size, (255, 255, 255, int(90 * (1 - t / 0.25)))))
            if seg_over: seg_over(im, tseg + t, D)
            captions(im, tseg + t, D, key)
            enc.stdin.write(im.convert('RGB').tobytes())
        done += n; tseg += d
    enc.stdin.close(); enc.wait(); print(name, round(D, 2), flush=True)

# ===================== segments (EN5) =====================
PHONE = {a: Image.open(f'{EP}/caps/app_{a}_{v}.png'.replace('_{v}', '')) for a in []}
def phone(a, v='phone', h=860):
    im = Image.open(f'{EP}/caps/app_{a}_{v}.png').convert('RGB'); w = int(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS); fr = Image.new('RGBA', (w + 28, h + 28), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    d.rounded_rectangle((0, 0, w + 27, h + 27), radius=46, fill=(20, 22, 30, 255)); m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=255); fr.paste(im, (14, 14), m); return fr
def shadow_paste(im, p, xy, a=1.0):
    if a <= 0: return
    s = Image.new('RGBA', (p.width + 80, p.height + 80), (0, 0, 0, 0)); ImageDraw.Draw(s).rounded_rectangle((40, 52, p.width + 40, p.height + 52), radius=46, fill=(0, 0, 0, 150))
    s = s.filter(ImageFilter.GaussianBlur(18)); x, y = int(xy[0]), int(xy[1] + 40 * (1 - a))
    if a < 1: p = p.copy(); p.putalpha(p.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(s, (x - 40, y - 40)); im.alpha_composite(p, (x, y))

P1 = 'Build me a bill-splitting web app as ONE single HTML file. Use exactly these ids: #total #tip #people #calc #result. Shares must add up EXACTLY to the total, to the cent. Nonsense input → "Invalid input".'
def v1():
    D = VD[0]
    def frame(t, d):
        im = background(); tiles(im, t, [(0.2, (420, 200), 'ChatGPT', GPT, 'G'), (0.45, (960, 200), 'Claude', CLA, 'C'), (0.7, (1500, 200), 'Gemini', GEM, 'G')])
        typecard(im, t, P1, t0=1.2, cps=55, label='SAME PROMPT · FRESH CHAT · FREE VERSIONS', a=fin(t, 1.0), y=560, size=44)
        for k, (txt, t0) in enumerate([('1 HTML file', .30), ('5 fixed ids → a robot can test it', .42), ('4 rules', .52)]):
            if t > t0 * d: pill(im, (W / 2, 790) if k == 1 else (430 if k == 0 else 1490, 790), txt, ORANGE if k != 1 else CYAN, fin(t, t0 * d), 34, tc=BG)
        if t > .62 * d:
            for k, txt in enumerate(['Tip on the bill', '1 line per person', 'Adds up to the cent', 'Nonsense → "Invalid input"']):
                e = fin(t, (.62 + .08 * k) * d)
                if e > 0: pill(im, (300 + k * 440, 895), txt, GREEN if k != 3 else RED, e, 30, tc=BG if k != 3 else WHITE)
        return im
    SFX.extend([('v1', .2, 'pop', -14), ('v1', .45, 'pop', -14), ('v1', .7, 'pop', -14)] + [('v1', (.62 + .08 * k) * D, 'pop', -16) for k in range(4)])
    render_seg('v1', 'V1', D, [dict(img=frame, w=1)])

def v2():
    D = VD[1]; split = .45
    def a(t, d):
        im = background(); dd = ImageDraw.Draw(im); e = fin(t, 0)
        dd.text((W / 2, 120), 'WHY IT IS HARDER THAN IT LOOKS', font=mono(32, 700), fill=ORANGE + (int(255 * e),), anchor='mm')
        glow_text(im, (W / 2, 230), '$10.00 ÷ 3 people', sg(96), WHITE)
        for k, v in enumerate(['$3.34', '$3.33', '$3.33']):
            if t > .18 * d + k * .35: pill(im, (560 + k * 400, 430), v, GREEN, fin(t, .18 * d + k * .35), 60, tc=BG)
        if t > .3 * d: dd.text((W / 2, 540), 'the first person pays 1 cent more  →  $10.00 ✓', font=sg(40, 600), fill=GREEN + (int(255 * fin(t, .3 * d)),), anchor='mm')
        if t > .55 * d:
            b = fin(t, .55 * d)
            for k in range(3): pill(im, (560 + k * 400, 720), '$3.33', GREY, b, 54, tc=BG)
            pill(im, (W / 2, 860), 'naive split = $9.99 · 1 cent vanished', RED, fin(t, .7 * d), 42, icon='x')
        wipe(im, t, 'THE TRAP', 'Money is hard')
        return im
    CODE = [('> 4.35 * 100', WHITE), ('434.99999999999994', AMB), ('> Math.floor(4.35 * 100) / 100', WHITE), ('4.34', RED)]
    def b(t, d):
        im = background(); dd = ImageDraw.Draw(im); e = fin(t, 0)
        dd.text((W / 2, 140), 'COMPUTERS VS MONEY', font=mono(32, 700), fill=ORANGE + (int(255 * e),), anchor='mm')
        glow_text(im, (W / 2, 230), 'JavaScript, in the browser console', sg(64), WHITE)
        x0, y0 = 360, 330; dd.rounded_rectangle((x0, y0, W - x0, y0 + 470), radius=28, fill=(14, 15, 22, int(250 * e)), outline=(70, 76, 100, int(255 * e)), width=3)
        for k in range(3): dd.ellipse((x0 + 30 + k * 34, y0 + 26, x0 + 50 + k * 34, y0 + 46), fill=[(255, 95, 87), (255, 189, 46), (40, 200, 64)][k] + (int(255 * e),))
        for k, (ln, col) in enumerate(CODE):
            tk = (.08 + .2 * k) * d
            if t > tk:
                n = int((t - tk) * 40); dd.text((x0 + 60, y0 + 120 + k * 90), ln[:n], font=mono(52, 600), fill=col + (255,), anchor='lm')
        if t > .75 * d: pill(im, (W / 2, 900), 'your app charges $4.34 instead of $4.35', RED, fin(t, .75 * d), 44, icon='x')
        return im
    SFX.extend([('v2', split * D + (.08 + .2 * 3) * (1 - split) * D, 'buzz', -16), ('v2', .55 * split * D, 'pop', -16), ('v2', .7 * split * D, 'buzz', -18)])
    render_seg('v2', 'V2', D, [dict(img=a, w=split), dict(img=b, w=1 - split)])

QUOTE_GPT = '“The file has been created, but I haven\'t run browser-based tests.”'
def v3():
    D = VD[2]
    def o1(im, t, d, c):
        topcard(im, fin(t, .1), 'CHATGPT · INSTANT', 'A file, ready to download', GPT); badge(im, fin(t, .3), '< 10 s')
        if t > .35 * d: ring(im, c.R(872, 558, 1560, 668), GPT, fin(t, .35 * d), 6, 8); pill(im, (c.P(1200, 560)[0], c.P(1200, 560)[1] - 50), 'bill-splitter.html · 3.8 KB', GPT, fin(t, .35 * d), 34)
    def q(t, d):
        im = background(); dd = ImageDraw.Draw(im); e = fin(t, 0)
        dd.text((W / 2, 150), 'ALSO IN THE ANSWER', font=mono(32, 700), fill=GPT + (int(255 * e),), anchor='mm')
        pill(im, (W / 2, 300), '“Exact integer arithmetic using JavaScript BigInt”', (24, 26, 36), fin(t, .1), 40)
        if t > .35 * d:
            b = fin(t, .35 * d); x0, y0 = 260, 430; dd.rounded_rectangle((x0, y0, W - x0, y0 + 260), radius=30, fill=(24, 26, 36, int(250 * b)), outline=AMB + (int(255 * b),), width=4)
            for j, ln in enumerate(wrapt(dd, QUOTE_GPT, sg(54, 600), W - 2 * x0 - 120)): dd.text((W / 2, y0 + 95 + j * 72), ln, font=sg(54, 600), fill=WHITE + (int(255 * b),), anchor='mm')
            dd.text((W / 2, y0 + 300), 'last line of ChatGPT\'s answer', font=mono(28, 600), fill=GREY + (int(255 * b),), anchor='mm')
        if t > .75 * d: pill(im, (W / 2, 900), 'Honest. So I tested it myself.', AMB, fin(t, .75 * d), 44, tc=BG)
        return im
    render_seg('v3', 'V3', D, [dict(img='chatgpt_card', w=.45, cam=[(0, WIDE), (.2, Z(860, 440, 1568, 680))], over=o1, sfx=[(.35, 'pop', -14)]),
                                dict(img=q, w=.55, sfx=[(.1, 'pop', -16), (.35, 'whoosh', -16), (.75, 'ding', -16)])])
def v4():
    D = VD[3]
    def o1(im, t, d, c):
        topcard(im, fin(t, .1), 'CLAUDE · OPUS 5.5', 'It tested its own app', CLA); badge(im, fin(t, .3), '40 s')
        if t > .2 * d:
            e = fin(t, .2 * d); ring(im, c.R(486, 305, 832, 325), AMB, e, 5, 8)
            pill(im, (c.P(486, 315)[0], c.P(486, 315)[1] - 62), 'created a file · shared a file · RAN A COMMAND', AMB, e, 30, tc=BG, anchor='lm')
        if t > .5 * d:
            e = fin(t, .5 * d); spotlight(im, c.R(486, 338, 1035, 405), e); ring(im, c.R(486, 338, 1035, 405), GREEN, e, 5, 6)
    def o2(im, t, d, c):
        badge(im, 1, '40 s')
        for k, (r, tk, col) in enumerate([((514, 415, 1025, 450), .05, GREEN), ((514, 547, 1035, 582), .5, CLA)]):
            if t > tk * d: ring(im, c.R(*r), col, fin(t, tk * d), 5, 6)
        if t > .55 * d: pill(im, (W / 2, 140), 'even thought about iPhone zoom', CLA, fin(t, .55 * d), 40)
    render_seg('v4', 'V4', D, [dict(img='claude_answer', w=.6, cam=[(0, WIDE), (.15, Z(486, 290, 1035, 410))], over=o1, sfx=[(.2, 'pop', -14), (.5, 'ding', -14)]),
                                dict(img='claude_answer', w=.4, cam=[(0, Z(486, 400, 1035, 590))], over=o2, sfx=[(.05, 'pop', -16), (.5, 'pop', -16)])])
def v5():
    D = VD[4]
    def o1(im, t, d, c):
        topcard(im, fin(t, .1), 'GEMINI · NEON', 'Just code. No words.', GEM)
        if t > .3 * d: ring(im, c.R(505, 230, 1105, 700), GEM, fin(t, .3 * d), 6, 4); pill(im, (W - 300, 140), '112 lines', GEM, fin(t, .3 * d), 44)
    def ph(t, d):
        im = background(); dd = ImageDraw.Draw(im); p = phone('gemini', h=900); x = W / 2 - p.width / 2
        shadow_paste(im, p, (x, 90), fin(t, 0)); a = fin(t, .25 * d)
        if a > 0:
            k = 900 / 1560  # grand total row measured in the render: y 958-1017 px
            ring(im, (x + 14 + 70 * k, 104 + 958 * k, x + 14 + 710 * k, 104 + 1017 * k), AMB, a, 5, 8)
            pill(im, (x - 40, 104 + 987 * k), 'Bonus: a grand total line', AMB, a, 36, tc=BG, anchor='rm')
        if t > .6 * d: pill(im, (x + p.width + 40, 600), 'but: what do I do with this code?', (24, 26, 36), fin(t, .6 * d), 32, anchor='lm')
        return im
    render_seg('v5', 'V5', D, [dict(img='gemini_code', w=.55, cam=[(0, WIDE), (.25, Z(505, 220, 1105, 690))], over=o1, sfx=[(.3, 'pop', -14)]),
                                dict(img=ph, w=.45, sfx=[(.25, 'pop', -14), (.6, 'pop', -16)])])
def v6():
    D = VD[5]
    def frame(t, d):
        im = background(); dd = ImageDraw.Draw(im)
        dd.text((W / 2, 70), 'THE 3 APPS · ON A PHONE · $10 ÷ 3', font=mono(32, 700), fill=ORANGE + (int(255 * fin(t, 0)),), anchor='mm')
        for k, (nm, col) in enumerate(AIS):
            p = phone(nm.lower(), h=760); x = 330 + k * 630 - p.width / 2; e = fin(t, .15 + k * .35)
            ang = (k - 1) * 3 * (1 - eio(t / 2.5)); q = p.rotate(ang, resample=Image.BICUBIC, expand=True) if abs(ang) > .05 else p
            shadow_paste(im, q, (x, 175), e); pill(im, (330 + k * 630, 135), nm, col, e, 30)
        if t > .45 * d: dim_callout(im, fin(t, .45 * d) * (1 - fin(t, .72 * d)), [('Weirdly similar.', False), ('Same layout, same idea', True)], ORANGE)
        return im
    SFX.extend([('v6', .15 + k * .35, 'pop', -14) for k in range(3)] + [('v6', .45 * D, 'whoosh', -16)])
    render_seg('v6', 'V6', D, [dict(img=frame, w=1)])
TESTS = ['$100 · 15 % · 2', '$10 · 3 people', '$19.99 · 20 % · 3', '5¢ · 7 people', '$33.33 · 15 % · 1', '$1,234.56 · 12.5 % · 6', 'defaults · $80', '$4.35 float trap', '10¢ · 3 people',
         'empty bill', 'negative bill', '2.5 people', '0 people', 'negative tip']
def v7():
    D = VD[6]; R = json.load(open(f'{EP}/apps/results.json'))
    def frame(t, d):
        im = background(); dd = ImageDraw.Draw(im); a = fin(t, 0)
        dd.text((W / 2, 70), 'THE TEST ROBOT · 14 CHECKS × 3 APPS', font=mono(32, 700), fill=ORANGE + (int(255 * a),), anchor='mm')
        for k, (nm, col) in enumerate(AIS):
            dd.rounded_rectangle((900 + k * 320, 110, 1180 + k * 320, 170), radius=20, fill=col + (int(255 * a),)); dd.text((1040 + k * 320, 140), nm, font=sg(34, 700), fill=WHITE + (int(255 * a),), anchor='mm')
        for r, lab in enumerate(TESTS):
            y = 215 + r * 57; tk = (.06 + r * .042) * d; b = fin(t, tk, .25)
            if b <= 0: continue
            dd.rounded_rectangle((180, y - 24, 1780, y + 24), radius=14, fill=PANEL + (int(230 * b),))
            dd.text((210, y), ('MONEY  ' if r < 9 else 'NONSENSE  '), font=mono(22, 700), fill=(GREEN if r < 9 else RED) + (int(255 * b),), anchor='lm')
            dd.text((370, y), lab, font=sg(32, 600), fill=WHITE + (int(255 * b),), anchor='lm')
            for k, (nm, col) in enumerate(AIS):
                ok = R[nm.lower()][r]; cx = 1040 + k * 320
                dd.ellipse((cx - 18, y - 18, cx + 18, y + 18), fill=(GREEN if ok else RED) + (int(255 * b),))
                dd.line((cx - 8, y, cx - 2, y + 7, cx + 9, y - 7), fill=BG + (int(255 * b),), width=5)
        if t > .8 * d:
            for k, (nm, col) in enumerate(AIS): pill(im, (1040 + k * 320, 140), '14 / 14', GREEN, fin(t, .8 * d + k * .25), 40, tc=BG)
        return im
    SFX.extend([('v7', (.06 + r * .042) * D, 'ding', -22) for r in range(14)] + [('v7', .8 * D + k * .25, 'pop', -12) for k in range(3)])
    render_seg('v7', 'V7', D, [dict(img=frame, w=1)])
TORT = [('1,000 people', '1,000 × $0.10'), ('bill typed as 1e2', '$50 + $50'), ('3.0 people', 'OK'), ('$99,999,999.99 + 20 % ÷ 7', '$17,142,857.15 …'), ('tie: $10.70 + 15 %', '$12.31'), ('0.5 % tip', '$33.50 / 33.50 / 33.49'), ('$0.001 bill', '$0.00')]
def v8():
    D = VD[7]; sp = .55
    def a(t, d):
        im = background(); dd = ImageDraw.Draw(im); e = fin(t, 0)
        dd.text((W / 2, 110), 'TORTURE ROUND · INPUTS MY PROMPT NEVER MENTIONED', font=mono(30, 700), fill=ORANGE + (int(255 * e),), anchor='mm')
        for r, (lab, res) in enumerate(TORT):
            y = 220 + r * 100; b = fin(t, (.1 + r * .09) * d, .3)
            if b <= 0: continue
            dd.rounded_rectangle((200, y - 38, 1720, y + 38), radius=20, fill=PANEL + (int(235 * b),))
            dd.text((240, y), lab, font=sg(38, 600), fill=WHITE + (int(255 * b),), anchor='lm'); dd.text((1100, y), res, font=mono(32, 600), fill=GREY + (int(255 * b),), anchor='lm')
            pill(im, (1640, y), 'same ×3', GREEN, b, 26, tc=BG)
        wipe(im, t, 'ROUND 2', 'Weird inputs')
        return im
    def b(t, d):
        im = background(); dd = ImageDraw.Draw(im)
        dd.text((W / 2, 70), 'ONE DIFFERENCE: I DELETED THE TIP', font=mono(32, 700), fill=AMB + (int(255 * fin(t, 0) * (1 - fin(t, .82 * d))),), anchor='mm')
        for k, (nm, col) in enumerate(AIS):
            p = phone(nm.lower(), 'emptytip', h=740); x = 330 + k * 630 - p.width / 2; e = fin(t, .05 + k * .3)
            shadow_paste(im, p, (x, 120), e)
            if t > (.15 + k * .25) * d:
                ok = k < 2; pill(im, (330 + k * 630, 905), '"Invalid input"' if ok else 'splits it: tip = 0 %', GREEN if ok else AMB, fin(t, (.15 + k * .25) * d), 32, tc=BG)
        if t > .82 * d: pill(im, (W / 2, 70), 'Not wrong. Not right. My prompt didn\'t say.', (24, 26, 36), fin(t, .82 * d), 40)
        return im
    SFX.extend([('v8', (.1 + r * .09) * sp * D, 'pop', -18) for r in range(7)] + [('v8', sp * D + (.15 + k * .25) * (1 - sp) * D, 'pop' if k < 2 else 'buzz', -14) for k in range(3)])
    render_seg('v8', 'V8', D, [dict(img=a, w=sp), dict(img=b, w=1 - sp)])
def v9():
    D = VD[8]; rows = ['Working code', 'My 14 tests', 'Speed', 'Tested its own work']
    cells = [[('yes', GREEN), ('yes', GREEN), ('yes', GREEN)], [('14/14', GREEN), ('14/14', GREEN), ('14/14', GREEN)], [('< 10 s', GREEN), ('40 s', AMB), ('code only', AMB)], [('said it hadn\'t', AMB), ('YES', GREEN), ('no word', AMB)]]
    tm = [.1, .3, .5, .68]
    def frame(t, d):
        im = background(); dd = ImageDraw.Draw(im); a = fin(t, 0)
        dd.text((W / 2, 100), 'FINAL SCORE', font=mono(34, 700), fill=ORANGE + (int(255 * a),), anchor='mm'); glow_text(im, (W / 2, 175), 'Who shipped?', sg(72), WHITE)
        for k, (nm, col) in enumerate(AIS):
            dd.rounded_rectangle((640 + k * 420, 260, 1020 + k * 420, 340), radius=24, fill=col + (int(255 * a),)); dd.text((830 + k * 420, 300), nm, font=sg(44, 700), fill=WHITE + (int(255 * a),), anchor='mm')
        for r, lab in enumerate(rows):
            b = fin(t, tm[r] * d)
            if b <= 0: continue
            y = 420 + r * 150; dd.rounded_rectangle((120, y - 55, 1820, y + 55), radius=26, fill=PANEL + (int(240 * b),), outline=(60, 66, 88, int(255 * b)), width=2)
            dd.text((160, y), lab, font=sg(42, 700), fill=WHITE + (int(255 * b),), anchor='lm')
            for k, (txt, col) in enumerate(cells[r]):
                e = fin(t, tm[r] * d + .2 + .15 * k)
                if e > 0: pill(im, (830 + k * 420, y), txt, col, e, 34, tc=BG)
        return im
    for r in range(4):
        for k in range(3): SFX.append(('v9', tm[r] * D + .2 + .15 * k, 'pop', -16))
    render_seg('v9', 'V9', D, [dict(img=frame, w=1)])

if __name__ == '__main__':
    which = sys.argv[1:] or [f'v{k}' for k in range(1, 10)]
    for w in which: globals()[w]()
    for w in which: json.dump([e for e in SFX if e[0] == w], open(f'{B}/sfx_{w}.json', 'w'))
