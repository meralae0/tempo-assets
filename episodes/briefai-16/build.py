# EN3 "I gave Gemini 4 Neon 3 real jobs" — real screen recording (clean1/clean2 = recording without border/pill, 1840x716)
# Each voice-over segment = list of shots; a shot = slice of the recording + camera keys + overlays.
import sys, os, json, math, subprocess
import numpy as np
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from gfx_ai import *
from leap import *
from PIL import Image, ImageDraw, ImageFilter
EP = '/home/claude/tempo-assets/episodes/briefai-16'; B = '/home/claude/b16'; O = B + '/seg'; os.makedirs(O, exist_ok=True)
T = json.load(open(EP + '/timing.json')); VD = [b - a for a, b in T['V']]
SRC = {1: B + '/clean1.mp4', 2: B + '/clean2.mp4'}
SW, SH = 1840, 716; PH = 1035; PAD = (PH - SH) // 2
GEM = (66, 133, 244); AMB = (255, 190, 60); NEON = (0, 230, 200)
SFX = []  # (segment, t, name, gain)

def fin(t, a, d=.4): return max(0., min(1., ease((t - a) / d)))
def fout(t, b, d=.3): return 1 - fin(t, b - d, d)

def read(src, t0, t1, n):
    """n frames uniformly over [t0, t1] (t1==t0 → frozen frame)"""
    if t1 - t0 < 0.05:
        p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t0:.3f}', '-i', SRC[src], '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        f = Image.frombytes('RGB', (SW, SH), p[:SW * SH * 3]); return [f] * n
    sp = (t1 - t0) / (n / 30)
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', f'{t0:.3f}', '-t', f'{t1 - t0 + 0.2:.3f}', '-i', SRC[src], '-vf', f'setpts=PTS/{sp:.5f},fps=30', '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    out = []
    while len(out) < n:
        b = p.stdout.read(SW * SH * 3)
        if len(b) < SW * SH * 3: break
        out.append(Image.frombytes('RGB', (SW, SH), b))
    p.wait()
    while len(out) < n: out.append(out[-1])
    return out

def padded(fr):
    bgi = fr.resize((92, 36)).filter(ImageFilter.GaussianBlur(3)).resize((SW, PH), Image.BILINEAR)
    bgi = Image.blend(bgi, Image.new('RGB', (SW, PH), (6, 7, 12)), 0.55)
    bgi.paste(fr, (0, PAD)); return bgi

WIDE = (0, 0, SW, PH)
def Z(x0, y0, x1, y1):
    """box in recording coords → padded coords, 16:9, clamped"""
    y0 += PAD; y1 += PAD
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; w = max(x1 - x0, (y1 - y0) * 16 / 9); h = w * 9 / 16
    w = min(w, SW); h = w * 9 / 16
    x0 = max(0, min(SW - w, cx - w / 2)); y0 = max(0, min(PH - h, cy - h / 2))
    return (x0, y0, x0 + w, y0 + h)

def boxat(t, keys):
    box = keys[0][1]
    for i, (tk, b) in enumerate(keys):
        if t >= tk:
            prev = keys[i - 1][1] if i else b
            k = eio((t - tk) / 0.7); box = tuple(lerp(p, q, k) for p, q in zip(prev, b))
    return box

class Ctx:
    def __init__(s, box): s.box = box
    def P(s, x, y):
        x0, y0, x1, y1 = s.box; k = W / (x1 - x0); return ((x - x0) * k, (y + PAD - y0) * k)
    def R(s, x0, y0, x1, y1):
        a = s.P(x0, y0); b = s.P(x1, y1); return (a[0], a[1], b[0], b[1])

# ---------- overlay primitives ----------
def pill(im, xy, txt, col=ORANGE, a=1.0, size=40, tc=WHITE, anchor='mm', icon=None):
    if a <= 0: return
    f = sg(size, 700); d0 = ImageDraw.Draw(im)
    b = d0.textbbox((0, 0), txt, font=f); tw, th = b[2] - b[0], size
    ic = size + 14 if icon else 0
    w, h = tw + 64 + ic, int(size * 1.9)
    p = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((15, 21, w + 15, h + 21), radius=h // 2, fill=(0, 0, 0, 110))
    p = p.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((15, 15, w + 15, h + 15), radius=h // 2, fill=col + (255,))
    x = 15 + 32
    if icon == 'check':
        cx, cy, r = x + size // 2, 15 + h // 2, size // 2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
        d.line((cx - r * .45, cy, cx - r * .1, cy + r * .38, cx + r * .5, cy - r * .38), fill=col + (255,), width=max(4, r // 4), joint='curve')
        x += ic
    elif icon == 'x':
        cx, cy, r = x + size // 2, 15 + h // 2, size // 2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255)); k = r * .42
        d.line((cx - k, cy - k, cx + k, cy + k), fill=col + (255,), width=6); d.line((cx - k, cy + k, cx + k, cy - k), fill=col + (255,), width=6)
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

def ring(im, r, col=ORANGE, a=1.0, w=6, pad=10):
    if a <= 0: return
    x0, y0, x1, y1 = r; x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    # draw-on effect: grow from 0.9 scale
    s = 0.9 + 0.1 * a; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0, x1 = cx - (cx - x0) * s, cx + (x1 - cx) * s; y0, y1 = cy - (cy - y0) * s, cy + (y1 - cy) * s
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    d.rounded_rectangle((x0, y0, x1, y1), radius=18, outline=col + (int(200 * a),), width=w + 8)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).rounded_rectangle((x0, y0, x1, y1), radius=18, outline=col + (int(255 * a),), width=w)

def ffbadge(im, a, real):
    """top-right 'fast-forward' badge: ▶▶ 2 min 28 s"""
    if a <= 0: return
    d = ImageDraw.Draw(im); f = mono(34, 700); txt = f'{real} · sped up'
    b = d.textbbox((0, 0), txt, font=f); w = b[2] - b[0] + 120; x = W - w - 50; y = 46
    d.rounded_rectangle((x, y, x + w, y + 74), radius=37, fill=(12, 13, 20, int(230 * a)), outline=(255, 255, 255, int(60 * a)), width=2)
    for k in range(2):
        tx = x + 28 + k * 22; d.polygon([(tx, y + 22), (tx, y + 52), (tx + 22, y + 37)], fill=AMB + (int(255 * a),))
    d.text((x + 86, y + 37), txt, font=f, fill=WHITE + (int(255 * a),), anchor='lm')

def topcard(im, a, kicker, title, col=GEM):
    """chapter card top-left"""
    if a <= 0: return
    d = ImageDraw.Draw(im); x = 50 - int(40 * (1 - a)); f1 = mono(28, 700); f2 = sg(46, 700)
    w = max(d.textbbox((0, 0), title, font=f2)[2], d.textbbox((0, 0), kicker, font=f1)[2]) + 70
    d.rounded_rectangle((x, 40, x + w, 172), radius=24, fill=(12, 13, 20, int(232 * a)))
    d.rounded_rectangle((x, 40, x + 10, 172), radius=5, fill=col + (int(255 * a),))
    d.text((x + 36, 78), kicker, font=f1, fill=col + (int(255 * a),), anchor='lm')
    d.text((x + 36, 128), title, font=f2, fill=WHITE + (int(255 * a),), anchor='lm')

def wrapt(d, txt, f, maxw):
    out, line = [], ''
    for w in txt.split():
        t = (line + ' ' + w).strip()
        if d.textbbox((0, 0), t, font=f)[2] > maxw and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out

def typecard(im, t, txt, t0=0.2, cps=55, label='MY PROMPT', a=1.0, y=540):
    """dim + big card with the prompt typed out"""
    if a <= 0: return
    im.alpha_composite(Image.new('RGBA', im.size, (6, 7, 12, int(165 * a))))
    d = ImageDraw.Draw(im); f = sg(50, 600); lines = wrapt(d, txt, f, 1280)
    h = 120 + 70 * len(lines); x0, y0 = W / 2 - 720, y - h / 2 + 30 * (1 - a)
    d.rounded_rectangle((x0, y0, x0 + 1440, y0 + h), radius=36, fill=(24, 26, 36, int(250 * a)), outline=GEM + (int(255 * a),), width=3)
    d.text((x0 + 70, y0 + 52), label, font=mono(28, 700), fill=GEM + (int(255 * a),), anchor='lm')
    n = int(max(0, t - t0) * cps); shown = 0
    for k, ln in enumerate(lines):
        part = ln[:max(0, n - shown)]; shown += len(ln) + 1
        d.text((x0 + 70, y0 + 110 + k * 70), part, font=f, fill=WHITE + (int(255 * a),), anchor='lm')
        if 0 < n - (shown - len(ln) - 1) <= len(ln) and int(t * 3) % 2 == 0:
            bx = d.textbbox((x0 + 70, y0 + 110 + k * 70), part, font=f, anchor='lm')[2]
            d.rectangle((bx + 6, y0 + 85 + k * 70, bx + 10, y0 + 135 + k * 70), fill=WHITE + (int(255 * a),))
    return min(1, n / max(1, len(txt)))

# ---------- shot rendering ----------
def render_seg(name, D, shots, seg_over=None):
    """shots: dict(src, t0, t1, w, cam=[(rel 0..1 or abs s, box)], over=fn(im, t, d, ctx), sfx=[(t,name,gain)])"""
    tot = sum(s['w'] for s in shots); N = int(round(D * 30))
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/{name}.mp4'], stdin=subprocess.PIPE)
    done = 0; tseg = 0.0
    for i, s in enumerate(shots):
        n = int(round(N * s['w'] / tot)) if i < len(shots) - 1 else N - done
        d = n / 30; frs = read(s['src'], s['t0'], s['t1'], n)
        keys = [(k * d if isinstance(k, float) and k <= 1 and s.get('rel', True) else k, b) for k, b in s.get('cam', [(0, WIDE)])]
        for t_, nm, g in s.get('sfx', []): SFX.append((name, tseg + (float(t_) * d if isinstance(t_, str) else t_), nm, g))
        if i: SFX.append((name, max(0, tseg - 0.15), 'whoosh', -20))
        for j, fr in enumerate(frs):
            t = j / 30; box = boxat(t, keys); ctx = Ctx(box)
            can = padded(fr); im = can.crop(tuple(int(v) for v in box)).resize((W, H), Image.BILINEAR).convert('RGBA')
            if s.get('over'): s['over'](im, t, d, ctx)
            if seg_over: seg_over(im, tseg + t, D)
            enc.stdin.write(im.convert('RGB').tobytes())
        done += n; tseg += d
    enc.stdin.close(); enc.wait(); print(name, round(D, 2), flush=True)

# ===================== segments =====================
P1 = 'Build me a playable Snake game in one HTML file: neon style, score, speed that increases, and a restart button. Show it running.'
P1b = 'Add an Autopilot button: the snake plays by itself, chasing the food and avoiding walls and its own tail.'
P1c = "The preview shows a runtime error and Start / Autopilot don't respond. Please fix the code."
P2 = 'This is my bank statement for October. Find anything unusual: duplicate charges, hidden fees, subscriptions I might forget. Then tell me how much I spent in total, not counting savings.'
P3 = 'Plan a 3-day weekend in Lisbon for two people with a $700 budget (not counting flights): where to stay, a day-by-day plan with free things to do, and a cost table that adds up.'

def v1():
    def o1(im, t, d, c):
        ring(im, c.R(1120, 325, 1205, 362), GEM, fin(t, 1.6));
        if t > 1.9: pill(im, (c.P(1162, 420)[0], c.P(1162, 420)[1] + 40), 'Model picker → Neon', GEM, fin(t, 1.9))
        topcard(im, fin(t, .2) * fout(t, d), 'GEMINI APP · AI PRO / ULTRA', 'Gemini 4 Neon')
    def o2(im, t, d, c):
        topcard(im, fin(t, .1), 'JOB 1', 'Build a game from one sentence', NEON)
        typecard(im, t, P1, t0=.5, cps=32, a=fin(t, .1))
    render_seg('v1', VD[0], [
        dict(src=1, t0=1, t1=15, w=6.5, cam=[(0, WIDE), (.25, Z(560, 190, 1330, 470))], over=o1, sfx=[(1.6, 'pop', -14), (1.9, 'pop', -14)]),
        dict(src=1, t0=20, t1=30, w=9.8, cam=[(0, WIDE)], over=o2, sfx=[(0.4, 'click', -16)]),
    ])

def v2():
    def o1(im, t, d, c): ffbadge(im, fin(t, .1), '2 min 28 s')
    def o2(im, t, d, c):
        ring(im, c.R(905, 305, 1255, 350), AMB, fin(t, d * .45))
        pill(im, (W / 2, 990), 'Code  ·  Live preview  ·  Export', AMB, fin(t, d * .45), tc=(20, 20, 20))
    def o3(im, t, d, c):
        for k, (x0, x1) in enumerate([(670, 840), (855, 1025), (1040, 1210)]):
            ring(im, c.R(x0, 92, x1, 168), NEON, fin(t, .4 + .25 * k), w=5, pad=4)
        pill(im, (W / 2, 1000), 'Score · Best · Speed meter', NEON, fin(t, 1.2), tc=(10, 20, 20))
    def o4(im, t, d, c):
        k = d / 6.5
        if t > 2.2 * k: pill(im, (W / 2, 160), 'Crashed in 2 seconds (my fault)', RED, fin(t, 2.2 * k), icon='x')
        if t > 4.2 * k: pill(im, (W / 2, 960), 'Restart works', GREEN, fin(t, 4.2 * k), icon='check', tc=(10, 30, 20))
    render_seg('v2', VD[1], [
        dict(src=1, t0=22, t1=166, w=4.2, cam=[(0, WIDE)], over=o1),
        dict(src=1, t0=168, t1=176, w=5.5, cam=[(0, WIDE), (.15, Z(470, 280, 1420, 716))], over=o2, sfx=[(2.4, 'pop', -14)]),
        dict(src=1, t0=182, t1=188.6, w=4.6, cam=[(0, Z(600, 0, 1280, 300))], over=o3, sfx=[(1.2, 'pop', -14)]),
        dict(src=1, t0=188.6, t1=195.4, w=8.6, cam=[(0, Z(560, 0, 1320, 716))], over=o4, sfx=[('0.34', 'buzz', -20), ('0.66', 'ding', -16)]),
    ])

def v3():
    def o1(im, t, d, c):
        topcard(im, fin(t, .1), 'JOB 1 · UPGRADE', 'Make it play by itself', NEON)
        typecard(im, t, P1b, t0=.3, cps=38, label='FOLLOW-UP', a=fin(t, .1))
    def o2(im, t, d, c): ffbadge(im, fin(t, .1), '2 min')
    def o3(im, t, d, c):
        ring(im, c.R(30, 590, 420, 716), RED, fin(t, .5)); ring(im, c.R(680, 648, 900, 690), RED, fin(t, 1.3), w=4)
        pill(im, (W / 2, 150), 'Runtime error · Start does nothing', RED, fin(t, .6), icon='x')
    def o4(im, t, d, c):
        ring(im, c.R(1490, 590, 1840, 640), RED, fin(t, d * .5))
        pill(im, (W / 2, 150), 'One-click fix: failed', RED, fin(t, d * .5), icon='x')
    render_seg('v3', VD[2], [
        dict(src=1, t0=208, t1=214, w=5.6, cam=[(0, WIDE)], over=o1, sfx=[(.3, 'click', -16)]),
        dict(src=1, t0=216, t1=336, w=3.0, cam=[(0, WIDE)], over=o2),
        dict(src=1, t0=342, t1=356, w=4.4, cam=[(0, WIDE), (.15, Z(0, 300, 1250, 716))], over=o3, sfx=[(.6, 'buzz', -18)]),
        dict(src=1, t0=358, t1=372, w=3.7, cam=[(0, Z(1100, 180, 1840, 716))], over=o4, sfx=[(1.9, 'buzz', -18)]),
    ])

def v4():
    def o1(im, t, d, c):
        typecard(im, t, P1c, t0=.3, cps=36, label='PLAIN WORDS', a=fin(t, .1))
    def o2(im, t, d, c): ffbadge(im, fin(t, .1), '2 min 52 s')
    def o3(im, t, d, c):
        ring(im, c.R(1490, 385, 1830, 485), AMB, fin(t, .6))
        pill(im, (W / 2, 150), 'Bug found: placeholder comments in its own code', AMB, fin(t, .7), tc=(20, 20, 20))
    def o4(im, t, d, c):
        ring(im, c.R(1048, 195, 1150, 225), AMB, fin(t, .5), w=4, pad=6)
        pill(im, (W / 2, 1000), 'Autopilot ON · it plans its own path', AMB, fin(t, .6), tc=(20, 20, 20))
    def o5(im, t, d, c):
        pill(im, (W / 2, 1000), 'Autopilot ON · it plans its own path', AMB, 1, tc=(20, 20, 20))
        if t > d - 2.6:
            ring(im, c.R(670, 90, 1210, 168), GREEN, fin(t, d - 2.6), w=5, pad=6)
            pill(im, (W / 2, 160), '200 points · hands-free', GREEN, fin(t, d - 2.6), icon='check', tc=(10, 30, 20))
    render_seg('v4', VD[3], [
        dict(src=1, t0=372, t1=378, w=4.2, cam=[(0, WIDE)], over=o1, sfx=[(.3, 'click', -16)]),
        dict(src=1, t0=378, t1=546, w=2.4, cam=[(0, WIDE)], over=o2),
        dict(src=1, t0=546.0, t1=546.0, w=4.0, cam=[(0, Z(1150, 180, 1840, 640))], over=o3, sfx=[(.7, 'pop', -14)]),
        dict(src=1, t0=566, t1=574, w=4.0, cam=[(0, Z(560, 0, 1320, 716))], over=o4, sfx=[(.6, 'pop', -14)]),
        dict(src=1, t0=574, t1=600, w=5.0, cam=[(0, Z(560, 0, 1320, 716))], over=o5, sfx=[('0.5', 'ding', -14)]),
    ])

def v5():
    def o1(im, t, d, c):
        topcard(im, fin(t, .2), 'JOB 2', 'Audit my bank statement', GREEN)
    def o2(im, t, d, c):
        topcard(im, 1, 'JOB 2', 'Audit my bank statement', GREEN)
        ring(im, c.R(625, 322, 740, 435), GREEN, fin(t, .3))
        pill(im, (W / 2, 990), '68 transactions · I worked out every answer first', GREEN, fin(t, .9), tc=(10, 30, 20))
    def o3(im, t, d, c):
        typecard(im, t, P2, t0=.2, cps=48, a=fin(t, .1))
    render_seg('v5', VD[4], [
        dict(src=2, t0=3, t1=19, w=3.0, cam=[(0, WIDE)], over=o1),
        dict(src=2, t0=20, t1=27, w=6.0, cam=[(0, Z(560, 230, 1340, 560))], over=o2, sfx=[(.3, 'pop', -14), (.9, 'pop', -14)]),
        dict(src=2, t0=28, t1=34, w=8.9, cam=[(0, WIDE)], over=o3, sfx=[(.2, 'click', -16)]),
    ])

CHK = [('Duplicate: Luna Trattoria $56.40 ×2', 0), ('Foreign transaction fee $2.99', 0), ('5 subscriptions · $85.96 / month', 0), ('Total spent: $3,589.58', 0), ('Café on Oct 14 = two visits, not a duplicate', 0), ('Refund $23.48 → net $3,566.10', 0)]
def checklist(im, t, times, a=1.0):
    if a <= 0: return
    d = ImageDraw.Draw(im); x0, y0 = 1250, 250; f = sg(30, 600)
    d.rounded_rectangle((x0, y0, x0 + 630, y0 + 90 + 92 * len(CHK)), radius=28, fill=(14, 16, 24, int(238 * a)), outline=GREEN + (int(160 * a),), width=3)
    d.text((x0 + 40, y0 + 50), 'MY ANSWER KEY', font=mono(28, 700), fill=GREEN + (int(255 * a),), anchor='lm')
    for k, (txt, _) in enumerate(CHK):
        b = fin(t, times[k], .35) * a; y = y0 + 120 + 92 * k
        if b <= 0: continue
        r = 22; cx = x0 + 60
        d.ellipse((cx - r, y - r, cx + r, y + r), fill=GREEN + (int(255 * b),))
        d.line((cx - r * .45, y, cx - r * .1, y + r * .38, cx + r * .5, y - r * .38), fill=BG + (int(255 * b),), width=5, joint='curve')
        for j, ln in enumerate(wrapt(d, txt, f, 500)[:2]):
            d.text((cx + 44, y - 16 * (len(wrapt(d, txt, f, 500)[:2]) - 1) + 34 * j), ln, font=f, fill=WHITE + (int(255 * b),), anchor='lm')

def v6():
    D = VD[5]; tk = [D * f for f in (.12, .27, .37, .50, .64, .80)]
    def seg_over(im, t, D_):
        if t > 2.0: checklist(im, t, tk, fin(t, 2.0))
        if t > D_ * .9: pill(im, (W / 2 - 300, 1000), 'All correct', GREEN, fin(t, D_ * .9), icon='check', tc=(10, 30, 20), size=46)
    def o1(im, t, d, c): ffbadge(im, fin(t, .1), '44 s')
    def o2(im, t, d, c):
        ring(im, c.R(470, 425, 1290, 470), AMB, fin(t, .4), w=4, pad=6); ring(im, c.R(470, 490, 1290, 530), GREY, fin(t, d * .55), w=3, pad=6)
    def o3(im, t, d, c):
        ring(im, c.R(630, 0, 1300, 40), AMB, fin(t, .2), w=4, pad=6); ring(im, c.R(590, 600, 1300, 630), AMB, fin(t, d * .5), w=4, pad=6)
    def o4(im, t, d, c):
        ring(im, c.R(590, 300, 1300, 330), AMB, fin(t, .3), w=4, pad=6); ring(im, c.R(590, 400, 1300, 445), AMB, fin(t, d * .45), w=4, pad=6)
    # recording: answer appears ~78 (rec2), scroll 1 ~88, 2 ~97, 3 ~106
    render_seg('v6', D, [
        dict(src=2, t0=34, t1=77, w=2.2, cam=[(0, WIDE)], over=o1),
        dict(src=2, t0=78, t1=88, w=7.0, cam=[(0, Z(420, 280, 1820, 716))], over=o2, sfx=[(.4, 'ding', -18)]),
        dict(src=2, t0=95, t1=101, w=7.6, cam=[(0, Z(420, 0, 1820, 640))], over=o3, sfx=[(.2, 'ding', -18), (3.5, 'ding', -18)]),
        dict(src=2, t0=104, t1=112, w=11.8, cam=[(0, Z(420, 150, 1820, 660))], over=o4, sfx=[(.3, 'ding', -18), (4.0, 'ding', -18), (8.5, 'ding', -18)]),
    ], seg_over=seg_over)

def v7():
    def o1(im, t, d, c):
        topcard(im, fin(t, .2), 'JOB 3 · NEW TASK MODE', 'Plan a whole trip on a budget', AMB)
        ring(im, c.R(950, 555, 1040, 600), AMB, fin(t, d * .5))
    def o2(im, t, d, c):
        typecard(im, t, P3, t0=.2, cps=50, a=fin(t, .1))
    def o3(im, t, d, c):
        ffbadge(im, fin(t, .1), '4 min 48 s')
        for k, (txt, ta) in enumerate([('Searches the web', .15), ('Checks what is closed right now', .38), ('Converts € at this month\'s rate', .6), ('Re-checks the budget', .8)]):
            pill(im, (90, 400 + k * 120), txt, AMB, fin(t, d * ta), tc=(20, 20, 20), anchor='lm', icon='check', size=36)
    render_seg('v7', VD[6], [
        dict(src=2, t0=124, t1=131, w=3.6, cam=[(0, WIDE)], over=o1, sfx=[(1.0, 'click', -16)]),
        dict(src=2, t0=133, t1=137, w=6.6, cam=[(0, WIDE)], over=o2),
        dict(src=2, t0=140, t1=420, w=10.4, cam=[(0, Z(300, 0, 1400, 430))], over=o3, sfx=[(1.5, 'pop', -14), (4.4, 'pop', -14), (7.0, 'pop', -14), (9.3, 'pop', -14)]),
    ])

def v8():
    def o0(im, t, d, c): pill(im, (W / 2, 990), 'A full travel guide, not a chat answer', AMB, fin(t, d * .4), tc=(20, 20, 20))
    def o1(im, t, d, c):
        ring(im, c.R(1110, 210, 1450, 420), AMB, fin(t, .3))
        pill(im, (W / 2, 990), '$657 planned · $43 buffer', AMB, fin(t, .5), tc=(20, 20, 20))
    def o2(im, t, d, c):
        pill(im, (W / 2, 990), '$288 + $260 + $63 + $46 = $657', GREEN, fin(t, .5), icon='check', tc=(10, 30, 20))
    def o3(im, t, d, c):
        pill(im, (W / 2, 990), '3 places to stay · from Chiado to Rossio', AMB, fin(t, .3), tc=(20, 20, 20))
    def o4(im, t, d, c):
        pill(im, (W / 2, 990), 'Day-by-day · mostly free things to do', AMB, fin(t, .3), tc=(20, 20, 20))
    def o5(im, t, d, c):
        pill(im, (W / 2, 990), 'Double-check opening hours', RED, fin(t, d * .35))
    render_seg('v8', VD[7], [
        dict(src=2, t0=420, t1=444, w=4.0, cam=[(0, WIDE)], over=o0),
        dict(src=2, t0=446, t1=452, w=2.6, cam=[(0, Z(60, 0, 1333, 716))]),
        dict(src=2, t0=482, t1=484, w=4.4, cam=[(0, WIDE), (.1, Z(40, 180, 1600, 640))], over=o1, sfx=[(.5, 'pop', -14)]),
        dict(src=2, t0=484.3, t1=485.8, w=4.6, cam=[(0, Z(200, 0, 1650, 716))], over=o2, sfx=[(.5, 'ding', -16)]),
        dict(src=2, t0=498, t1=501, w=4.4, cam=[(0, Z(80, 120, 1780, 600))], over=o3, sfx=[(.3, 'pop', -14)]),
        dict(src=2, t0=502, t1=506, w=4.2, cam=[(0, Z(60, 0, 1333, 716))], over=o4, sfx=[(.3, 'pop', -14)]),
        dict(src=2, t0=524, t1=531, w=4.2, cam=[(0, Z(283, 0, 1556, 716))], over=o5),
    ])

def v9():
    D = VD[8]; N = int(round(D * 30))
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/v9.mp4'], stdin=subprocess.PIPE)
    cards = [('JOB 1', 'Snake game', NEON, 'Worked first try', 'Upgrade broke · fixed in 1 message', '2 min 28 s', 148), ('JOB 2', 'Bank statement', GREEN, '6 / 6 checks correct', 'Duplicate, fee, subscriptions, totals', '44 s', 44), ('JOB 3', 'Lisbon trip', AMB, 'Budget adds up to the dollar', 'Guide + hotels + day-by-day plan', '4 min 48 s', 288)]
    tm = [D * f for f in (.14, .40, .60)]
    for i in range(N):
        t = i / 30; im = background().copy().convert('RGBA'); d = ImageDraw.Draw(im)
        a = fin(t, 0); d.text((W / 2, 130 - 20 * (1 - a)), 'SCORECARD', font=mono(34, 700), fill=ORANGE + (int(255 * a),), anchor='mm')
        glow_text(im, (W / 2, 205), 'Gemini 4 Neon · 3 real jobs', sg(72), WHITE)
        for k, (kk, ti, col, l1, l2, tt, sec) in enumerate(cards):
            b = fin(t, tm[k], .45);
            if b <= 0: continue
            x = 120 + k * 580; y = 320 + 40 * (1 - b)
            d.rounded_rectangle((x, y, x + 520, y + 560), radius=32, fill=PANEL + (int(250 * b),), outline=col + (int(255 * b),), width=4)
            d.text((x + 40, y + 60), kk, font=mono(30, 700), fill=col + (int(255 * b),), anchor='lm')
            d.text((x + 40, y + 125), ti, font=sg(54, 700), fill=WHITE + (int(255 * b),), anchor='lm')
            r = 26; cx, cy = x + 66, y + 230
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN + (int(255 * b),)); d.line((cx - r * .45, cy, cx - r * .1, cy + r * .38, cx + r * .5, cy - r * .38), fill=BG + (int(255 * b),), width=6, joint='curve')
            for j, ln in enumerate(wrapt(d, l1, sg(36, 700), 380)): d.text((x + 112, cy - 2 + 44 * j), ln, font=sg(36, 700), fill=WHITE + (int(255 * b),), anchor='lm')
            for j, ln in enumerate(wrapt(d, l2, sg(30, 500), 440)): d.text((x + 40, y + 350 + 40 * j), ln, font=sg(30, 500), fill=GREY + (int(255 * b),), anchor='lm')
            L = 440 * min(1, sec / 300) * fin(t, tm[k] + .5, 1.0)
            d.rounded_rectangle((x + 40, y + 470, x + 480, y + 500), radius=15, fill=(40, 44, 60, int(255 * b)))
            d.rounded_rectangle((x + 40, y + 470, x + 40 + max(L, 30), y + 500), radius=15, fill=col + (int(255 * b),))
            d.text((x + 480, y + 440), tt, font=mono(28, 700), fill=WHITE + (int(255 * b),), anchor='rm')
        enc.stdin.write(im.convert('RGB').tobytes())
    for k in range(3): SFX.append(('v9', tm[k], 'pop', -12))
    enc.stdin.close(); enc.wait(); print('v9', D)

if __name__ == '__main__':
    which = sys.argv[1:] or ['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9']
    for w in which: globals()[w]()
    for w in which: json.dump([e for e in SFX if e[0] == w], open(f'{B}/sfx_{w}.json', 'w'))
