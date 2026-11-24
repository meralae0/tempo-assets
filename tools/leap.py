"""BriefAI v3 — habillage façon tutoriel tech (vraie interface plein écran + visage en rond).
Briques (toutes renvoient une image RGBA 1920x1080) :
  cam(img, t, keys)            vraie capture, caméra qui zoome/panote entre des cadres  keys=[(t, (x0,y0,x1,y1)), ...]
  cursor(im, xy)               flèche de souris
  dim_callout(im, a, lines)    interface assombrie + gros texte animé (« A messy plan → Something useful »)
  pip(im, face)                visage de l'avatar dans un rond à contour blanc, en bas à gauche
  cta(im, a, txt)              bouton orange en bas à droite (« Prompt in the description »)
  tiles(im, t, items)          cartes d'applis qui apparaissent autour du présentateur (intro)
  chapter(im, a, n, title)     carte de chapitre en haut à gauche
Effets sonores : tools/sfx/*.wav (make_sfx.py) ; sfx_track(events, dur, out) les place dans le temps."""
import os, math, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np
from gfx_ai import sg, mono, ease, W, H, FPS, WHITE, GREY, BG, RED, GREEN, CYAN
ORANGE = (255, 112, 67); HERE = os.path.dirname(os.path.abspath(__file__))

def lerp(a, b, k): return a + (b - a) * k
def eio(k): k = max(0, min(1, k)); return k * k * (3 - 2 * k)
def pop(t, t0, d=0.35):
    """échelle avec léger rebond (0 → 1.08 → 1)"""
    k = (t - t0) / d
    if k <= 0: return 0
    if k >= 1: return 1
    return 1 + 0.08 * math.sin(k * math.pi) if k > .6 else ease(k / .6) * 1.08

def cam(img, t, keys, out=(W, H)):
    """keys triées ; entre deux clés, transition de 0,6 s puis tenue."""
    box = keys[0][1]
    for i, (tk, b) in enumerate(keys):
        if t >= tk:
            prev = keys[i - 1][1] if i else b
            k = eio((t - tk) / 0.6)
            box = tuple(lerp(p, q, k) for p, q in zip(prev, b))
    x0, y0, x1, y1 = box
    # garder le ratio 16:9
    cx, cy, w = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, (y1 - y0) * 16 / 9)
    h = w * 9 / 16; x0, y0 = cx - w / 2, cy - h / 2
    x0 = max(0, min(img.width - w, x0)); y0 = max(0, min(img.height - h, y0))
    return img.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize(out, Image.LANCZOS).convert('RGBA')

def cursor(im, xy, s=1.0):
    x, y = xy; d = ImageDraw.Draw(im)
    pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (27, 24)]
    P = [(x + px * s, y + py * s) for px, py in pts]
    d.polygon([(a + 2, b + 2) for a, b in P], fill=(0, 0, 0, 120)); d.polygon(P, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))

def dim_callout(im, a, lines, accent=ORANGE):
    if a <= 0: return
    ov = Image.new('RGBA', im.size, (8, 9, 14, int(170 * a))); im.alpha_composite(ov)
    d = ImageDraw.Draw(im); y = H / 2 - (len(lines) - 1) * 70
    for k, (txt, big) in enumerate(lines):
        f = sg(92 if big else 54, 700); s = pop(a * 0.35 + 0.0001, 0) if a < 1 else 1
        col = (accent if big else WHITE) + (int(255 * a),)
        d.text((W / 2, y + k * 140), txt, font=f, fill=col, anchor='mm')

def pip(im, face, r=150, xy=(60, None), ring=8):
    """face : image RGB du présentateur (cadrage visage centré)"""
    x0 = xy[0]; y0 = H - 2 * r - 50 if xy[1] is None else xy[1]
    f = ImageOps.fit(face.convert('RGB'), (2 * r, 2 * r), centering=(0.5, 0.35))
    m = Image.new('L', (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((x0 - ring + 6, y0 - ring + 10, x0 + 2 * r + ring + 6, y0 + 2 * r + ring + 10), fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    ImageDraw.Draw(im).ellipse((x0 - ring, y0 - ring, x0 + 2 * r + ring, y0 + 2 * r + ring), fill=(255, 255, 255, 255))
    im.paste(f, (x0, y0), m)

def cta(im, a, txt):
    if a <= 0: return
    d = ImageDraw.Draw(im); f = sg(38, 700)
    b = d.textbbox((0, 0), txt, font=f); w, h = b[2] - b[0] + 110, 84
    x = W - w - 50 + int(60 * (1 - a)); y = H - h - 60
    d.rounded_rectangle((x, y, x + w, y + h), radius=42, fill=ORANGE + (int(255 * a),))
    d.ellipse((x + 18, y + 18, x + 66, y + 66), fill=(255, 255, 255, int(255 * a)))
    d.text((x + 42, y + 42), '+', font=sg(40, 800), fill=ORANGE + (255,), anchor='mm')
    d.text((x + 84, y + h / 2), txt, font=f, fill=(255, 255, 255, int(255 * a)), anchor='lm')

def tile(label, col, glyph):
    t = Image.new('RGBA', (230, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((6, 10, 224, 224), radius=34, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, 218, 214), radius=34, fill=col + (235,), outline=(255, 255, 255, 60), width=3)
    d.text((109, 88), glyph, font=sg(84, 700), fill=(255, 255, 255, 235), anchor='mm')
    d.text((109, 178), label, font=sg(36, 700), fill=(255, 255, 255, 255), anchor='mm')
    return t

def tiles(im, t, items):
    """items=[(t0, (cx,cy), label, col, glyph)]"""
    for t0, (cx, cy), lab, col, g in items:
        s = pop(t, t0)
        if s <= 0: continue
        tl = tile(lab, col, g); tl = tl.resize((max(1, int(tl.width * s)), max(1, int(tl.height * s))), Image.LANCZOS)
        im.alpha_composite(tl, (int(cx - tl.width / 2), int(cy - tl.height / 2)))

def chapter(im, a, n, title):
    if a <= 0: return
    d = ImageDraw.Draw(im); x = 60 - int(40 * (1 - a))
    d.rounded_rectangle((x, 50, x + 120 + 24 * len(title), 130), radius=20, fill=(12, 13, 20, int(225 * a)))
    d.text((x + 28, 90), f'{n:02d}', font=mono(40, 700), fill=ORANGE + (int(255 * a),), anchor='lm')
    d.text((x + 100, 90), title, font=sg(40, 700), fill=WHITE + (int(255 * a),), anchor='lm')

def sfx_track(events, dur, out):
    """events=[(t, 'whoosh'|'pop'|'click'|'ding'|'buzz'|'riser', gain_db)] → wav stéréo 48 kHz"""
    if not events:
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', f'{dur:.3f}', out], check=True); return out
    args = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=stereo:d={dur:.3f}']
    fl = []
    for i, (t, n, g) in enumerate(events):
        args += ['-i', f'{HERE}/sfx/{n}.wav']
        fl.append(f'[{i + 1}:a]adelay={int(t * 1000)}|{int(t * 1000)},volume={g}dB[s{i}]')
    mix = ''.join(f'[s{i}]' for i in range(len(events)))
    fl.append(f'[0:a]{mix}amix=inputs={len(events) + 1}:duration=first:normalize=0[o]')
    args += ['-filter_complex', ';'.join(fl), '-map', '[o]', out]
    subprocess.run(args, check=True); return out
