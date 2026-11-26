# EN4 "I hid a secret instruction in a PDF" — screenshots of the real chats (caps/*.jpg, 1568x751) with camera moves,
# rings, pills, chapter wipes and word-by-word captions. timing.json = {"A1":[a,b], "V":[[a,b] x10], "A2":[a,b]} in vids_export.mp4
import sys, os, json, math, subprocess, re
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from gfx_ai import *
from leap import *
from PIL import Image, ImageDraw, ImageFilter
EP = '/home/claude/tempo-assets/episodes/briefai-21'; B = '/home/claude/b21'; O = B + '/seg'; os.makedirs(O, exist_ok=True)
T = json.load(open(EP + '/timing.json')) if os.path.exists(EP + '/timing.json') else {}; VD = [b - a for a, b in T.get('S', [])]
GPT = (16, 163, 127); CLA = (217, 119, 87); GEM = (66, 133, 244); AMB = (255, 190, 60)
AIS = [('ChatGPT', GPT), ('Claude', CLA), ('Gemini', GEM)]
SFX = []

def fin(t, a, d=.4): return max(0., min(1., ease((t - a) / d)))

# ---------- captures ----------
CW, CH = 1568, 751; PH = int(CW * 9 / 16) + 1; PAD = (PH - CH) // 2
def load(name):
    im = Image.open(f'{EP}/caps/{name}.jpg').convert('RGB')
    if name.startswith('02') or name.startswith('03') or name.startswith('04'):  # Gemini: profile photo bottom-left, sidebar with name/history
        sb = 236 if name.startswith('04') else 48
        reg = im.crop((0, 0, sb, im.height)).filter(ImageFilter.GaussianBlur(16)); im.paste(reg, (0, 0))
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
for blk in re.split(r'\n\n(?=[AVS]\d+ \[)', open(f'{EP}/script_vids.md').read())[1:]:
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

# ===================== segments =====================
