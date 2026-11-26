# EN6 "I made a cartoon from one sentence with AI" — VO scenes V1..V10 (graphics over real captures / real outputs)
import sys, os, json, subprocess, wave, struct
sys.path.insert(0, '/home/claude/tempo-assets/episodes/briefai-20')
from gfx20 import *
from PIL import Image, ImageDraw, ImageFilter
IMG = EP + '/img'; CLA = (217, 119, 87); GEM = (66, 133, 244); STU = (120, 200, 255)
STILLS = {k: Image.open(f'{IMG}/s{k}.png').convert('RGB') for k in range(1, 7)}

def card_img(im, src, box, a=1.0, rot=0, shadow=True, border=6):
    if a <= 0: return
    x0, y0, x1, y1 = box; w, h = int(x1 - x0), int(y1 - y0)
    p = src.resize((w, h), Image.LANCZOS).convert('RGBA')
    c = Image.new('RGBA', (w + 2 * border, h + 2 * border), (255, 255, 255, 255)); c.paste(p, (border, border))
    if rot: c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = 0.85 + 0.15 * eio(a); c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 30 * (1 - a)
    if shadow:
        sh = Image.new('RGBA', (c.width + 60, c.height + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((30, 40, c.width + 30, c.height + 40), fill=(0, 0, 0, int(140 * a)))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (int(cx - c.width / 2 - 30), int(cy - c.height / 2 - 30)))
    if a < 1: c.putalpha(c.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))

def head(im, t, kicker, title, col=ORANGE):
    a = fin(t, 0.1); d = ImageDraw.Draw(im)
    d.text((W / 2, 95), kicker, font=mono(32, 700), fill=col + (int(255 * a),), anchor='mm')
    glow_text(im, (W / 2, 160), title, sg(64), WHITE)

# ---------- V1: Claude writes the script ----------
def v1():
    D = VD[0]
    def ov(im, t, d, ctx):
        if t > 1.2: ring(im, ctx.R(578, 67, 1085, 188), CLA, fin(t, 1.2))
        badge(im, fin(t, 0.4 * d), 'Claude · ~45 s')
    def ov2(im, t, d, ctx):
        ring(im, ctx.R(486, 250, 615, 270), ORANGE, fin(t, 0.6)); pill(im, (W / 2, 150), 'Title: Wick and the Dark', (12, 13, 20), fin(t, 0.8), 44)
    render_seg('v1', 'V1', D, [
        dict(img='01_claude_script_a', w=0.55, cam=[(0, WIDE), (0.15, Z(560, 60, 1100, 200))], over=ov,
             sfx=[(0.2, 'pop', -14)]),
        dict(img='01_claude_script_a', w=0.45, cam=[(0, Z(470, 240, 1050, 400)), (0.4, Z(470, 230, 900, 290))], over=ov2, sfx=[(0.1, 'pop', -14)])],
        seg_over=lambda im, t, D: wipe(im, t, 'STEP 1', 'The script', CLA))
    SFX.append(('v1', 0.0, 'whoosh', -12))

def v2():
    D = VD[1]
    def ov(im, t, d, ctx):
        spotlight(im, ctx.R(486, 280, 1035, 395), fin(t, 0.3))
        ring(im, ctx.R(486, 300, 1035, 352), ORANGE, fin(t, 0.35 * d)); ring(im, ctx.R(486, 362, 1035, 395), CYAN, fin(t, 0.55 * d))
        pill(im, (W / 2, 140), 'Paste this into EVERY prompt', ORANGE, fin(t, 0.2 * d), 44)
    def ov2(im, t, d, ctx):
        pill(im, (W / 2, 140), '6 shots · 60 s · 94 words', GREEN, fin(t, 0.3 * d), 46, tc=(10, 30, 20), icon='check')
    render_seg('v2', 'V2', D, [
        dict(img='01_claude_script_a', w=0.62, cam=[(0, Z(470, 270, 1050, 400))], over=ov, sfx=[(0.2, 'pop', -14), (0.55, 'pop', -14)]),
        dict(img='01_claude_script_b', w=0.38, cam=[(0, Z(470, 60, 1050, 580)), (0.5, Z(470, 60, 1050, 340))], over=ov2, sfx=[(0.3, 'ding', -14)])])

# ---------- V3-V5: Gemini images ----------
def v3():
    D = VD[2]
    def frame(t, d):
        im = background(); head(im, t, 'STEP 2 · GEMINI (AI PRO)', 'Make the reference shot first', GEM)
        card_img(im, STILLS[2], (W / 2 - 620, 240, W / 2 + 620, 240 + 692), fin(t, 0.4))
        pill(im, (W / 2 + 470, 300), 'Shot 2 · ~20 s', (12, 13, 20), fin(t, 0.55 * d), 38)
        if t > 0.75 * d: pill(im, (W / 2 - 400, 880), '8 s → 1 min per image', GEM, fin(t, 0.75 * d), 40)
        return im
    SFX.append(('v3', 0.4, 'pop', -14)); SFX.append(('v3', 0.55 * D, 'pop', -14))
    render_seg('v3', 'V3', D, [dict(img=frame, w=1)], seg_over=lambda im, t, D: wipe(im, t, 'STEP 2', 'The drawings', GEM))

def v4():
    D = VD[3]
    order = [1, 2, 3, 4, 5, 6]
    def frame(t, d):
        im = background(); head(im, t, 'SAME CHAT · SAME CHARACTER SHEET', '6 images, 1 robot', GEM)
        cw, chh = 560, 313
        for k, s in enumerate(order):
            r, c = divmod(k, 3); x = 110 + c * (cw + 40); y = 250 + r * (chh + 60)
            a = fin(t, 0.4 + k * 0.35, .35); card_img(im, STILLS[s], (x, y, x + cw, y + chh), a, rot=[-2, 1, -1, 2, -1, 1][k])
        if t > 0.6 * d:
            for k in range(6):
                r, c = divmod(k, 3); x = 110 + c * (cw + 40) + cw - 40; y = 250 + r * (chh + 60) + 10
                pill(im, (x, y), 'OK', GREEN, fin(t, 0.6 * d + k * 0.12), 26, tc=(10, 30, 20), icon='check')
        return im
    for k in range(6): SFX.append(('v4', 0.4 + k * 0.35, 'pop', -16))
    SFX.append(('v4', 0.6 * D, 'ding', -14))
    render_seg('v4', 'V4', D, [dict(img=frame, w=1)])

FIXP = 'Create an image. 2D cartoon, flat colors, thick clean dark outlines… Character Wick: a tiny robot with a round brass-yellow dome head, one big glowing amber eye, a mint-teal body, a short red knitted scarf… Scene: a stormy night at the lighthouse…'
def v5():
    D = VD[4]
    def ov(im, t, d, ctx):
        ring(im, ctx.R(516, 620, 1052, 645), RED, fin(t, 0.6)); pill(im, (W / 2, 150), 'Gemini refused shot 3', RED, fin(t, 0.8), 44, icon='x')
    def fix(t, d):
        im = background(); typecard(im, t, FIXP, t0=0.3, cps=70, label='THE FIX: "CREATE AN IMAGE." + FULL SHEET AGAIN', a=fin(t, 0), y=420, col=GREEN, size=40)
        card_img(im, STILLS[3], (W / 2 - 330, 690, W / 2 + 330, 1060), fin(t, 0.55 * d))
        pill(im, (W / 2 + 420, 760), 'Worked', GREEN, fin(t, 0.6 * d), 40, tc=(10, 30, 20), icon='check')
        return im
    render_seg('v5', 'V5', D, [
        dict(img='02_gemini_fail', w=0.45, cam=[(0, WIDE), (0.25, Z(500, 470, 1100, 660))], over=ov, sfx=[(0.3, 'buzz', -16)]),
        dict(img=fix, w=0.55, sfx=[(0.6, 'ding', -14)])])

# ---------- V6: AI Studio voice (real waveform of the file we got) ----------
def read_wave(p, n=900):
    import wave as wavmod
    import numpy as np
    w = wavmod.open(p); fr = w.readframes(w.getnframes()); a = np.frombuffer(fr, dtype=np.int16).astype(float)
    if w.getnchannels() == 2: a = a[::2]
    seg = np.array_split(np.abs(a), n); v = np.array([s.max() for s in seg]); return v / v.max(), w.getnframes() / w.getframerate()
WV, WD = read_wave(EP + '/voice/narr.wav')
def v6():
    D = VD[5]
    def frame(t, d):
        im = background(); head(im, t, 'STEP 3 · GOOGLE AI STUDIO · TEXT TO SPEECH', 'Preset: The Master Storyteller', STU)
        dd = ImageDraw.Draw(im); a = fin(t, 0.3)
        x0, y0, x1, y1 = 160, 300, W - 160, 760
        dd.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=(20, 22, 32, int(245 * a)), outline=STU + (int(200 * a),), width=3)
        dd.text((x0 + 50, y0 + 55), '“On a rock at the edge of the sea, tiny Wick kept the lighthouse lamp burning…”', font=sg(36, 600), fill=WHITE + (int(255 * a),), anchor='lm')
        prog = min(1, max(0, (t - 0.8) / (0.55 * d))); n = len(WV); mid = (y0 + y1) / 2 + 40; bw = (x1 - x0 - 100) / n
        for i, v in enumerate(WV):
            x = x0 + 50 + i * bw; h = max(2, v * 150); col = STU if i / n <= prog else (70, 78, 100)
            dd.line((x, mid - h, x, mid + h), fill=col + (int(255 * a),), width=1)
        dd.text((x1 - 50, y1 - 40), f'{prog * WD:04.1f} s / {WD:.1f} s', font=mono(32, 700), fill=WHITE + (int(255 * a),), anchor='rm')
        if t > 0.7 * d: pill(im, (W / 2 - 300, 870), 'Generated in ~20 s', STU, fin(t, 0.7 * d), 42, tc=(10, 20, 30))
        if t > 0.8 * d: pill(im, (W / 2 + 330, 870), 'No re-take', GREEN, fin(t, 0.8 * d), 42, tc=(10, 30, 20), icon='check')
        return im
    SFX.append(('v6', 0.7 * D, 'pop', -14)); SFX.append(('v6', 0.8 * D, 'ding', -14))
    render_seg('v6', 'V6', D, [dict(img=frame, w=1)], seg_over=lambda im, t, D: wipe(im, t, 'STEP 3', 'The voice', STU))

# ---------- V7-V8: Veo ----------
def v7():
    D = VD[6]
    def ov1(im, t, d, ctx):
        ring(im, ctx.R(516, 335, 935, 360), RED, fin(t, 0.5)); pill(im, (W / 2, 150), 'Try 1: error', RED, fin(t, 0.6), 44, icon='x')
    def ov2(im, t, d, ctx):
        spotlight(im, ctx.R(516, 330, 1060, 370), fin(t, 0.3)); ring(im, ctx.R(516, 330, 1060, 370), RED, fin(t, 0.5))
        pill(im, (W / 2, 150), 'Try 2: refused', RED, fin(t, 0.6), 44, icon='x')
        if t > 0.55 * d: pill(im, (W / 2, 900), 'An original robot. No brand. No real person.', (12, 13, 20), fin(t, 0.55 * d), 40)
    render_seg('v7', 'V7', D, [
        dict(img='03_veo_error', w=0.45, cam=[(0, WIDE), (0.3, Z(500, 60, 1100, 380))], over=ov1, sfx=[(0.3, 'buzz', -16)]),
        dict(img='03_veo_refusal', w=0.55, cam=[(0, Z(500, 60, 1100, 400))], over=ov2, sfx=[(0.2, 'buzz', -16)])],
        seg_over=lambda im, t, D: wipe(im, t, 'STEP 4', 'The animation', RED))

def veo_frames():
    tmp = B + '/veo'; os.makedirs(tmp, exist_ok=True)
    if not os.listdir(tmp): subprocess.run(['ffmpeg', '-v', 'error', '-i', EP + '/clips/s6.mp4', '-vf', 'fps=30,scale=1120:630', f'{tmp}/%04d.png'], check=True)
    return sorted(os.listdir(tmp))
def v8():
    D = VD[7]; fr = veo_frames()
    def ov(im, t, d, ctx):
        ring(im, ctx.R(600, 330, 750, 360), GREEN, fin(t, 0.5)); pill(im, (W / 2, 150), 'Try 4 (calm ending): it worked', GREEN, fin(t, 0.6), 44, tc=(10, 30, 20), icon='check')
    def clip(t, d):
        im = background(); head(im, t, 'VEO · IMAGE → VIDEO · 10 s', 'Shot 6, animated', GREEN)
        k = min(len(fr) - 1, int(t * 30) % len(fr)); f = Image.open(f'{B}/veo/{fr[k]}')
        card_img(im, f, (W / 2 - 515, 235, W / 2 + 515, 815), fin(t, 0.1))
        if t > 0.55 * d: pill(im, (W / 2, 890), '1 animation out of 2', AMB, fin(t, 0.55 * d), 44, tc=(20, 20, 20))
        if t > 0.25 * d: pill(im, (W - 300, 300), 'Chat vanished · found in history', RED, fin(t, 0.25 * d), 30)
        return im
    render_seg('v8', 'V8', D, [
        dict(img='03_veo_error', w=0.25, cam=[(0, Z(500, 60, 1100, 380))], over=lambda im, t, d, ctx: (ring(im, ctx.R(516, 335, 935, 360), RED, fin(t, 0.3)), pill(im, (W / 2, 150), 'Try 3: error again', RED, fin(t, 0.4), 44, icon='x')), sfx=[(0.2, 'buzz', -16)]),
        dict(img='04_veo_ready', w=0.15, cam=[(0, Z(580, 300, 1220, 720))], over=ov, sfx=[(0.3, 'ding', -14)]),
        dict(img=clip, w=0.6)])

# ---------- V9: the edit (Claude Code script) ----------
CODE = open(EP + '/cartoon.py').read().split('\n')
def v9():
    D = VD[8]
    def frame(t, d):
        im = background(); dd = ImageDraw.Draw(im); head(im, t, 'STEP 5 · CLAUDE WRITES THE EDIT', 'python + ffmpeg, 80 s render', CLA)
        a = fin(t, 0.2); x0, y0 = 120, 230
        dd.rounded_rectangle((x0, y0, x0 + 1000, y0 + 620), radius=24, fill=(14, 16, 24, int(250 * a)), outline=(60, 66, 90, int(255 * a)), width=2)
        lines = [l for l in CODE if l.strip() and not l.startswith('"""')][:22]; n = int(max(0, t - 0.5) * 9)
        for i, l in enumerate(lines[:n]):
            dd.text((x0 + 30, y0 + 30 + i * 26), l[:78], font=mono(19, 500), fill=(170, 200, 255, int(255 * a)) if l.lstrip().startswith('#') is False else (110, 120, 140, int(255 * a)))
        # shot timeline
        cuts = [0, 8.75, 17.2, 23.6, 31.75, 41.9, 53.5]; tl_x0, tl_x1, ty = 1170, W - 110, 300
        dd.text((tl_x0, ty - 40), 'TIMELINE · 54 s', font=mono(26, 700), fill=ORANGE + (int(255 * a),), anchor='lm')
        for k in range(6):
            b = fin(t, 0.35 * d + k * 0.3, .3)
            if b <= 0: continue
            y = ty + k * 95; card_img(im, STILLS[k + 1], (tl_x0, y, tl_x0 + 150, y + 84), b, shadow=False, border=3)
            lab = ['zoom in', 'zoom in', 'zoom out', 'pan', 'tilt up', 'VEO clip'][k]
            dd.text((tl_x0 + 175, y + 25), f'Shot {k + 1} · {cuts[k + 1] - cuts[k]:.1f} s', font=sg(28, 700), fill=WHITE + (int(255 * b),), anchor='lm')
            dd.text((tl_x0 + 175, y + 60), lab, font=mono(22, 600), fill=(GREEN if k == 5 else GREY) + (int(255 * b),), anchor='lm')
        return im
    for k in range(6): SFX.append(('v9', 0.35 * D + k * 0.3, 'pop', -18))
    render_seg('v9', 'V9', D, [dict(img=frame, w=1)], seg_over=lambda im, t, D: wipe(im, t, 'STEP 5', 'The edit', CLA))

ROWS = [('Script', 'Claude', '~45 s', '$0', GREEN), ('6 images', 'Gemini', '~3 min', '$0', GREEN), ('Voice', 'AI Studio', '~20 s', '$0', GREEN),
        ('Animation', 'Veo', '~12 min · 1 of 2', '$0', RED), ('Edit', 'Claude Code', '~80 s', '$0', GREEN)]
def v10():
    D = VD[9]
    def frame(t, d):
        im = background(); dd = ImageDraw.Draw(im); head(im, t, 'THE RECEIPT', '27 minutes · $0 extra', ORANGE)
        x0 = 260; y = 270
        for k, (a1, b1, c1, d1, col) in enumerate(ROWS):
            a = fin(t, 0.4 + k * 0.45, .35)
            if a <= 0: continue
            yy = y + k * 108 + 20 * (1 - a)
            dd.rounded_rectangle((x0, yy, W - x0, yy + 88), radius=20, fill=(20, 22, 32, int(240 * a)))
            dd.rounded_rectangle((x0, yy, x0 + 10, yy + 88), radius=5, fill=col + (int(255 * a),))
            dd.text((x0 + 40, yy + 44), a1, font=sg(40, 700), fill=WHITE + (int(255 * a),), anchor='lm')
            dd.text((x0 + 430, yy + 44), b1, font=sg(36, 600), fill=GREY + (int(255 * a),), anchor='lm')
            dd.text((x0 + 820, yy + 44), c1, font=mono(34, 700), fill=(AMB if col == RED else WHITE) + (int(255 * a),), anchor='lm')
            dd.text((W - x0 - 40, yy + 44), d1, font=mono(38, 700), fill=GREEN + (int(255 * a),), anchor='rm')
        if t > 0.7 * d: pill(im, (W / 2, 900), 'Paid plans I already had: Claude + Google AI Pro', (12, 13, 20), fin(t, 0.7 * d), 36)
        return im
    for k in range(5): SFX.append(('v10', 0.4 + k * 0.45, 'pop', -16))
    render_seg('v10', 'V10', D, [dict(img=frame, w=1)])

if __name__ == '__main__':
    which = sys.argv[1:] or [f'v{k}' for k in range(1, 11)]
    for w in which: globals()[w]()
    for w in which: json.dump([e for e in SFX if e[0] == w], open(f'{B}/sfx_{w}.json', 'w'))
