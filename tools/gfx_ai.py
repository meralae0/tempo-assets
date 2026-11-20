"""BriefAI — graphiques au style tech. Même interface que gfx.py (lower_third, badge, end_card, thumbnail)
plus des plans dédiés : window, terminal, handles, stamp, rename, counters, title, wave, code."""
import os, subprocess, shutil, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
BG = (9, 10, 15); CYAN = (0, 212, 255); VIOLET = (124, 92, 255); WHITE = (240, 244, 250); GREY = (130, 140, 160)
DIM = (60, 68, 88); RED = (255, 77, 90); GREEN = (40, 220, 140); PANEL = (17, 19, 28)
HERE = os.path.dirname(os.path.abspath(__file__)); BRAND = os.path.join(HERE, '..', 'brand')
ALPHA = False

def sg(sz, w=700):
    f = ImageFont.truetype(os.path.join(BRAND, 'SpaceGrotesk.ttf'), sz); f.set_variation_by_axes([w]); return f
def mono(sz, w=500):
    f = ImageFont.truetype(os.path.join(BRAND, 'JetBrainsMono.ttf'), sz); f.set_variation_by_axes([w]); return f
def ease(t):
    t = max(0, min(1, t)); return 1 - (1 - t) ** 3

_BG = None
def background():
    global _BG
    if _BG is None:
        im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
        for x in range(0, W, 64): d.line((x, 0, x, H), fill=(20, 23, 34, 255))
        for y in range(0, H, 64): d.line((0, y, W, y), fill=(20, 23, 34, 255))
        gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        gd.ellipse((W / 2 - 600, H / 2 - 380, W / 2 + 600, H / 2 + 380), fill=VIOLET + (55,))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(170))); _BG = im
    return _BG.copy()

def glow_text(im, xy, txt, font, fill, anchor='mm', r=14):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, txt, font=font, fill=fill + (255,), anchor=anchor)
    g = lay.filter(ImageFilter.GaussianBlur(r)); im.alpha_composite(g); im.alpha_composite(lay)

def render(frames_fn, dur, out):
    n = max(1, int(round(dur * FPS))); tmp = out + '_frames'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i in range(n): frames_fn(i, n).convert('RGB').save(os.path.join(tmp, f'{i:05d}.png'), compress_level=1)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%05d.png'), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', out], check=True)
    shutil.rmtree(tmp); return out

def still_motion(img, dur, out, zoom=0.05):
    """Plan fixe avec léger zoom (Ken Burns) via ffmpeg — rapide."""
    png = out + '.png'; img.convert('RGB').save(png)
    n = int(round(dur * FPS))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', png, '-vf',
                    f"scale=3840:-1,zoompan=z='1+{zoom}*on/{n}':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,format=yuv420p",
                    '-t', f'{dur:.3f}', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', out], check=True)
    os.remove(png); return out

# ---------- briques ----------
def window_frame(shot_path, title='', width=1240, blur_boxes=()):
    """Fenêtre de navigateur sombre contenant une capture réelle (sans flou d'agrandissement excessif)."""
    shot = Image.open(shot_path).convert('RGB')
    for (x0, y0, x1, y1) in blur_boxes:  # masquer e-mails / infos perso (coords dans la capture d'origine)
        reg = shot.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(9)); shot.paste(reg, (x0, y0))
    scale = width / shot.width; shot = shot.resize((width, int(shot.height * scale)), Image.LANCZOS)
    bar = 44; win = Image.new('RGBA', (width + 2, shot.height + bar + 2), (40, 44, 58, 255)); d = ImageDraw.Draw(win)
    d.rectangle((1, 1, width, bar), fill=(24, 27, 38, 255))
    for k, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse((18 + k * 26, 15, 32 + k * 26, 29), fill=c + (255,))
    d.rounded_rectangle((width / 2 - 260, 9, width / 2 + 260, 35), radius=8, fill=(14, 16, 24, 255))
    d.text((width / 2, 22), title, font=mono(17), fill=GREY + (255,), anchor='mm')
    win.paste(shot, (1, bar + 1)); return win

def place_window(win, y_off=0):
    im = background(); sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); x = (W - win.width) // 2; y = (H - win.height) // 2 + y_off
    ImageDraw.Draw(sh).rounded_rectangle((x - 6, y + 20, x + win.width + 6, y + win.height + 30), radius=18, fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
    edge = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(edge).rounded_rectangle((x - 2, y - 2, x + win.width + 2, y + win.height + 2), radius=14, outline=CYAN + (90,), width=2)
    im.alpha_composite(edge); im.alpha_composite(win, (x, y)); return im

# ---------- plans ----------
def window(out, dur, lang, times=None, shot=None, title='', blur=(), width=1240, label=None):
    title = title[lang] if isinstance(title, dict) else title
    im = place_window(window_frame(shot, title, width, blur), y_off=20 if label else 0)
    if label:
        d = ImageDraw.Draw(im); glow_text(im, (W / 2, 70), label[lang] if isinstance(label, dict) else label, mono(34, 600), CYAN, r=10)
    return still_motion(im, dur, out, zoom=0.04)

def terminal(out, dur, lang, times=None, lines=None, title='brief.txt'):
    lines = lines[lang] if isinstance(lines, dict) else lines; f = mono(40, 500); total = sum(len(l) for l in lines)
    def fr(i, n):
        t = i / FPS; shown = int(min(total, t / max(0.1, dur * 0.75) * total)); im = background(); d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = 260, 220, W - 260, H - 220
        d.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=PANEL + (240,), outline=(40, 46, 64, 255), width=2)
        d.rounded_rectangle((x0, y0, x1, y0 + 48), radius=18, fill=(24, 27, 38, 255)); d.rectangle((x0, y0 + 30, x1, y0 + 48), fill=(24, 27, 38, 255))
        for k, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse((x0 + 20 + k * 26, y0 + 17, x0 + 34 + k * 26, y0 + 31), fill=c)
        d.text(((x0 + x1) / 2, y0 + 24), title, font=mono(18), fill=GREY, anchor='mm')
        y = y0 + 110; left = shown
        for l in lines:
            part = l[:max(0, left)]; left -= len(l)
            d.text((x0 + 60, y), ('> ' if l else '') + part, font=f, fill=(CYAN if l.startswith('#') else WHITE), anchor='lm')
            if 0 <= left + len(l) - len(part) and left < 0 and (i // 15) % 2 == 0:
                cx = x0 + 60 + d.textlength('> ' + part, font=f) + 4; d.rectangle((cx, y - 22, cx + 20, y + 22), fill=CYAN)
            y += 64
            if left < 0: break
        return im
    return render(fr, dur, out)

def code(out, dur, lang, times=None, path=None, start=1, n=26, title=''):
    title = title[lang] if isinstance(title, dict) else title
    src = open(path, encoding='utf-8').read().splitlines()[start - 1:start - 1 + n * 2]; f = mono(26, 400)
    def fr(i, nn):
        u = i / max(1, nn - 1); off = int(u * (len(src) - n) * 34) if len(src) > n else 0; im = background(); d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = 200, 120, W - 200, H - 120
        d.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=PANEL + (245,), outline=(40, 46, 64, 255), width=2)
        d.text((x0 + 30, y0 + 28), title, font=mono(20), fill=GREY, anchor='lm')
        lay = Image.new('RGBA', (x1 - x0 - 40, y1 - y0 - 80), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        for k, line in enumerate(src):
            yy = 10 + k * 34 - off
            if -40 < yy < lay.height + 40:
                ld.text((10, yy), f'{start + k:>3}', font=f, fill=DIM); col = (CYAN if line.strip().startswith(('def ', 'import', 'from')) else (GREY if line.strip().startswith(('#', '"""')) else WHITE))
                ld.text((80, yy), line[:110], font=f, fill=col)
        im.alpha_composite(lay, (x0 + 20, y0 + 60)); return im
    return render(fr, dur, out)

def handles(out, dur, lang, times=None, items=None, ok=None, title=None):
    items = items or []; f = mono(44, 600); per = (dur * 0.8) / (len(items) + 1)
    def fr(i, n):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im)
        if title: glow_text(im, (W / 2, 120), title[lang], sg(56, 700), WHITE, r=10)
        cols = 2; rows = math.ceil(len(items) / cols)
        for k, h in enumerate(items):
            a = ease((t - k * per) / 0.35)
            if a <= 0: continue
            cx = W / 2 - 430 + (k // rows) * 860; y = 250 + (k % rows) * 92
            d.text((cx - 300, y), '@' + h, font=f, fill=GREY, anchor='lm')
            d.line((cx + 312, y - 18, cx + 348, y + 18), fill=RED, width=7); d.line((cx + 312, y + 18, cx + 348, y - 18), fill=RED, width=7)
            if a > 0.6: d.line((cx - 300, y + 2, cx - 300 + d.textlength('@' + h, font=f), y + 2), fill=RED, width=3)
        a = ease((t - len(items) * per) / 0.5)
        if ok and a > 0:
            y = H - 150; glow_text(im, (W / 2 - 40, y), '@' + ok, sg(84, 700), GREEN, r=18)
            tw = ImageDraw.Draw(im).textlength('@' + ok, font=sg(84, 700)); cx = W / 2 - 40 + tw / 2 + 60
            ImageDraw.Draw(im).line((cx - 26, y, cx - 6, y + 22, cx + 34, y - 26), fill=GREEN, width=10, joint='curve')
        return im
    return render(fr, dur, out)

def stamp(out, dur, lang, times=None, frame=None, text=None, color=RED, sub=None):
    base = Image.open(frame).convert('RGBA').resize((W, H)) if frame else background()
    base = Image.alpha_composite(base.filter(ImageFilter.GaussianBlur(6)), Image.new('RGBA', (W, H), (0, 0, 0, 150)))
    txt = text[lang] if isinstance(text, dict) else text
    def fr(i, n):
        t = i / FPS; im = base.copy(); a = ease((t - 0.5) / 0.25)
        if a > 0:
            s = 1.6 - 0.6 * a; f = sg(int(150 * s), 700); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
            tw = ld.textlength(txt, font=f); ld.rounded_rectangle((W / 2 - tw / 2 - 40, H / 2 - 110 * s, W / 2 + tw / 2 + 40, H / 2 + 110 * s), radius=16, outline=color + (255,), width=int(10 * s))
            ld.text((W / 2, H / 2), txt, font=f, fill=color + (255,), anchor='mm'); lay = lay.rotate(-8, center=(W / 2, H / 2)); im.alpha_composite(lay)
            if sub and a >= 1: glow_text(im, (W / 2, H - 130), sub[lang], mono(36, 600), WHITE, r=6)
        return im
    return render(fr, dur, out)

def wave(out, dur, lang, times=None, wav=None, quote=None):
    import wave as wv, numpy as np
    w = wv.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; w.close()
    q = quote[lang]
    def fr(i, n):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im); bars = 64
        for b in range(bars):
            c = int((t + (b - bars / 2) * 0.02) * sr); seg = x[max(0, c - 400):c + 400]; amp = float(np.sqrt((seg ** 2).mean())) if len(seg) else 0
            h = 20 + min(300, amp * 2200); xx = W / 2 - bars * 14 + b * 28
            d.rounded_rectangle((xx, H / 2 - 120 - h / 2, xx + 16, H / 2 - 120 + h / 2), radius=8, fill=(CYAN if abs(b - bars / 2) < 20 else VIOLET))
        glow_text(im, (W / 2, 120), {'fr': '[ EXTRAIT ORIGINAL ]', 'en': '[ ORIGINAL CLIP ]'}[lang], mono(34, 700), RED, r=8)
        words = q.split(); lines = []; cur = ''
        for wd in words:
            if len(cur) + len(wd) + 1 <= 46: cur = (cur + ' ' + wd).strip()
            else: lines.append(cur); cur = wd
        if cur: lines.append(cur)
        for k, l in enumerate(lines[:3]): d.text((W / 2, H - 260 + k * 60), l, font=sg(46, 500), fill=WHITE, anchor='mm')
        return im
    return render(fr, dur, out)

def rename(out, dur, lang, times=None, old='TempoBrief', avatar=None):
    av = Image.open(avatar).convert('RGBA').resize((300, 300)) if avatar else None
    def fr(i, n):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im); f = sg(150, 700)
        a = ease((t - 0.3) / 0.4); b = ease((t - 1.2) / 0.6)
        y = H / 2 - 40 - 140 * b
        col = tuple(int(WHITE[k] + (DIM[k] - WHITE[k]) * b) for k in range(3))
        d.text((W / 2, y), old, font=sg(int(150 - 60 * b), 700), fill=col, anchor='mm')
        if a > 0:
            tw = d.textlength(old, font=sg(int(150 - 60 * b), 700)); d.line((W / 2 - tw / 2, y, W / 2 - tw / 2 + tw * a, y), fill=RED, width=8)
        if b > 0:
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); w1 = ld.textlength('Brief', font=f); w2 = ld.textlength('AI', font=f)
            x = W / 2 - (w1 + w2) / 2 + (170 if av else 0); yy = H / 2 + 120
            ld.text((x, yy), 'Brief', font=f, fill=WHITE + (int(255 * b),), anchor='lm'); ld.text((x + w1, yy), 'AI', font=f, fill=CYAN + (int(255 * b),), anchor='lm')
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(lay)
            if av:
                avb = av.copy(); avb.putalpha(av.getchannel('A').point(lambda p: int(p * b))); im.alpha_composite(avb, (int(x - 340), int(yy - 150)))
        return im
    return render(fr, dur, out)

def counters(out, dur, lang, times=None, items=None):
    items = items[lang]; st = (times or [])
    def fr(i, n):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im); cw = 400
        for k, (val, lab, col) in enumerate(items):
            t0 = 0.3 + k * min(0.9, dur / (len(items) + 1)); a = ease((t - t0) / 0.6)
            if a <= 0: continue
            x = W / 2 - (len(items) * cw + (len(items) - 1) * 30) / 2 + k * (cw + 30); y = 300 + (1 - a) * 40
            d.rounded_rectangle((x, y, x + cw, y + 420), radius=22, fill=PANEL + (235,), outline=(tuple(col) + (200,)), width=3)
            glow_text(im, (x + cw / 2, y + 170), val, sg(110, 700), tuple(col), r=12)
            for kk, l in enumerate(lab.split('\n')): d.text((x + cw / 2, y + 300 + kk * 44), l, font=mono(32, 500), fill=GREY, anchor='mm')
        return im
    return render(fr, dur, out)

def title(out, dur, lang, times=None, lines=None):
    ls = lines[lang]
    def fr(i, n):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im); y = H / 2 - (len(ls) - 1) * 70
        for k, (txt, col) in enumerate(ls):
            sh = int(min(len(txt), max(0, (t - k * 0.6)) * 28))
            if sh <= 0: continue
            glow_text(im, (W / 2, y + k * 140), txt[:sh] + ('_' if sh < len(txt) else ''), sg(96, 700), tuple(col), r=14)
        return im
    return render(fr, dur, out)


def _wrap(txt, font, maxw, d):
    words = txt.split(' '); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def prompt(out, dur, lang, times=None, path=None, start=1, end=None, title=None, hl=(), plus=False, hl_at=0.45):
    """Fichier prompt affiché dans un éditeur : lignes qui s'écrivent, titres ## en cyan, lignes hl surlignées,
    plus=True : lignes ajoutées (diff vert)."""
    p = path[lang] if isinstance(path, dict) else path
    src = open(p, encoding='utf-8').read().splitlines(); end = min(end or len(src), len(src))
    title = (title[lang] if isinstance(title, dict) else title) or os.path.basename(p)
    hl = hl[lang] if isinstance(hl, dict) else hl
    x0, y0, x1, y1 = 150, 90, W - 150, H - 90
    probe = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    for fs in (46, 42, 38, 34, 31):
        fb = mono(fs, 500); fh = sg(int(fs * 1.4), 700); rows = []
        for ln in range(start, end + 1):
            raw = src[ln - 1].replace('**', '')
            if not raw.strip() or raw.strip() == '---': rows.append((ln, '', 'gap')); continue
            if raw.startswith('#'): rows.append((ln, raw.lstrip('#').strip(), 'h')); continue
            for k, w in enumerate(_wrap(raw, fb, x1 - x0 - 200, probe)): rows.append((ln, w, 'b' if k == 0 else 'c'))
        hgt = {'gap': int(fs * 0.7), 'h': int(fs * 2.3), 'b': int(fs * 1.48), 'c': int(fs * 1.48)}
        if sum(hgt[r[2]] for r in rows) <= (y1 - y0 - 120): break
    vis = [r for r in rows]; nrev = len([r for r in vis if r[2] != 'gap']); step = min(0.35, dur * 0.55 / max(1, nrev))
    def fr(i, n):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im)
        d.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=PANEL + (248,), outline=(40, 46, 64, 255), width=2)
        for k, c in enumerate([RED, (255, 190, 60), GREEN]): d.ellipse((x0 + 26 + k * 30, y0 + 22, x0 + 42 + k * 30, y0 + 38), fill=c)
        d.text((x0 + 140, y0 + 30), title, font=mono(22), fill=GREY, anchor='lm'); d.line((x0, y0 + 60, x1, y0 + 60), fill=(40, 46, 64), width=2)
        lay = Image.new('RGBA', (x1 - x0 - 4, y1 - y0 - 66), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ys = []; y = 18; kk = 0; shown = []
        for r in vis:
            if r[2] == 'gap': ys.append(y); y += hgt['gap']; shown.append(1); continue
            a = ease((t - kk * step) / 0.25); kk += 1; ys.append(y); y += hgt[r[2]]; shown.append(a)
        last = max([ys[j] + hgt['b'] + 10 for j in range(len(vis)) if shown[j] > 0] + [0]); off = max(0, last - (lay.height - 30))
        ha = ease((t - dur * hl_at) / 0.4)
        for j, (ln, txt, kind) in enumerate(vis):
            a = shown[j]; yy = ys[j] - off
            if kind == 'gap' or a <= 0 or yy < -60 or yy > lay.height + 10: continue
            al = int(255 * a)
            if (ln in hl and ha > 0) or plus:
                bg = (GREEN if plus else CYAN); g = int((70 if plus else 60) * (1 if plus else ha) * a)
                ld.rectangle((60, yy - 4, lay.width - 20, yy + hgt[kind] - 4), fill=bg + (g,))
                if not plus: ld.rectangle((60, yy - 4, 66, yy + hgt[kind] - 4), fill=CYAN + (int(255 * ha),))
            if kind != 'c': ld.text((12, yy + (int(fs*0.45) if kind == 'h' else 6)), ('+' if plus else f'{ln:>2}'), font=mono(24), fill=(GREEN if plus else DIM) + (al,))
            if kind == 'h': ld.text((84, yy), txt, font=fh, fill=CYAN + (al,))
            else:
                col = WHITE if (ln in hl and ha > 0) or plus or not hl else tuple(int(WHITE[q] * 0.55 + GREY[q] * 0.1) for q in range(3))
                ld.text((84, yy + 4), txt, font=fb, fill=col + (al,))
        im.alpha_composite(lay, (x0 + 2, y0 + 64)); return im
    return render(fr, dur, out)

def _arg(x, lang):
    return x[lang] if isinstance(x, dict) else x

def ranking(out, dur, lang, times=None, rows=None, title=None, hl=1, reveal=0.6, count=None):
    """Tableau de classement : lignes (texte, note) qui apparaissent du bas vers le haut ou du haut ; n°hl surligné."""
    import json as _j
    rws = _j.load(open(rows)) if isinstance(rows, str) else rows
    rws = rws[:count] if count else rws
    fT = sg(40, 700); fr_ = sg(34, 500); fn = mono(34, 700)
    n = len(rws); step = min(0.45, dur * reveal / max(1, n))
    def fr(i, nn):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im)
        if title: glow_text(im, (W / 2, 80), _arg(title, lang), sg(52, 700), WHITE, r=10)
        x0, x1 = 230, W - 230; y0 = 150; rh = min(84, (H - 200) // max(n, 1))
        for k, r in enumerate(rws):
            a = ease((t - (n - 1 - k) * step) / 0.35)
            if a <= 0: continue
            y = y0 + k * rh + (1 - a) * 30; top = (k + 1) == hl
            ha = ease((t - n * step - 0.2) / 0.4) if top else 0
            col = PANEL if not top else tuple(int(PANEL[q] + (0 - PANEL[q]) * 0) for q in range(3))
            d.rounded_rectangle((x0, y, x1, y + rh - 12), radius=14, fill=PANEL + (int(235 * a),), outline=((CYAN if top and ha > 0 else (40, 46, 64)) + (int(255 * a),)), width=3 if top and ha > 0 else 2)
            d.text((x0 + 30, y + (rh - 12) / 2), f"{k + 1:>2}", font=fn, fill=(CYAN if top else GREY) + (int(255 * a),), anchor='lm')
            d.text((x0 + 120, y + (rh - 12) / 2), r[lang] if lang in r else r['fr'], font=fr_, fill=WHITE + (int(255 * a),), anchor='lm')
            note = r['note']; nc = GREEN if note >= 8 else (CYAN if note >= 6.5 else (RED if note < 5 else GREY))
            d.text((x1 - 40, y + (rh - 12) / 2), f"{note:.1f}".replace('.', ',' if lang == 'fr' else '.'), font=fn, fill=nc + (int(255 * a),), anchor='rm')
        return im
    return render(fr, dur, out)

def search(out, dur, lang, times=None, query='', suggestions=None, title=None):
    """Barre de recherche recréée : la requête se tape, puis les vraies suggestions tombent."""
    sug = _arg(suggestions, lang) if suggestions else []
    f = sg(46, 500); fs = sg(40, 400)
    def fr(i, nn):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im)
        if title: glow_text(im, (W / 2, 90), _arg(title, lang), mono(30, 600), GREY, r=6)
        bx0, bx1, by = 360, W - 360, 170
        d.rounded_rectangle((bx0, by, bx1, by + 90), radius=45, fill=(22, 25, 36, 255), outline=(60, 68, 88, 255), width=2)
        d.ellipse((bx0 + 36, by + 28, bx0 + 66, by + 58), outline=GREY, width=4); d.line((bx0 + 62, by + 54, bx0 + 76, by + 68), fill=GREY, width=4)
        n = int(min(len(query), max(0, t - 0.2) * 14)); txt = query[:n] + ('|' if int(t * 2) % 2 == 0 else '')
        d.text((bx0 + 100, by + 45), txt, font=f, fill=WHITE, anchor='lm')
        t0 = 0.2 + len(query) / 14 + 0.3
        for k, s_ in enumerate(sug):
            a = ease((t - t0 - k * 0.22) / 0.3)
            if a <= 0: continue
            y = by + 110 + k * 66
            d.rounded_rectangle((bx0, y, bx1, y + 58), radius=10, fill=(17, 19, 28, int(240 * a)))
            q = query.lower(); disp = s_
            if disp.lower().startswith(q):
                d.text((bx0 + 100, y + 29), disp[:len(q)], font=fs, fill=GREY + (int(255 * a),), anchor='lm')
                w0 = d.textlength(disp[:len(q)], font=fs)
                d.text((bx0 + 100 + w0, y + 29), disp[len(q):], font=sg(40, 700), fill=CYAN + (int(255 * a),), anchor='lm')
            else:
                d.text((bx0 + 100, y + 29), disp, font=fs, fill=WHITE + (int(255 * a),), anchor='lm')
        return im
    return render(fr, dur, out)

def results(out, dur, lang, times=None, rows=None, title=None, show_vpd=True):
    """Liste de résultats (vues, âge) sans miniatures + calcul vues/jour."""
    rws = rows; f = sg(32, 500); fm = mono(30, 600)
    def fr(i, nn):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im)
        if title: glow_text(im, (W / 2, 80), _arg(title, lang), mono(30, 600), GREY, r=6)
        x0, x1 = 200, W - 200
        d.text((x1 - 420, 140), {'fr': 'vues', 'en': 'views'}[lang], font=mono(24), fill=DIM, anchor='rm')
        d.text((x1 - 250, 140), {'fr': 'âge', 'en': 'age'}[lang], font=mono(24), fill=DIM, anchor='rm')
        if show_vpd: d.text((x1 - 20, 140), {'fr': 'vues / jour', 'en': 'views / day'}[lang], font=mono(24), fill=CYAN, anchor='rm')
        for k, (ttl, v, age, vpd) in enumerate(rws):
            a = ease((t - 0.2 - k * 0.18) / 0.3)
            if a <= 0: continue
            y = 180 + k * 82
            d.rounded_rectangle((x0, y, x1, y + 70), radius=10, fill=PANEL + (int(235 * a),))
            d.text((x0 + 24, y + 35), ttl[:44] + ('…' if len(ttl) > 44 else ''), font=f, fill=WHITE + (int(255 * a),), anchor='lm')
            d.text((x1 - 420, y + 35), v, font=fm, fill=WHITE + (int(255 * a),), anchor='rm')
            d.text((x1 - 250, y + 35), age, font=fm, fill=GREY + (int(255 * a),), anchor='rm')
            b = ease((t - 0.2 - len(rws) * 0.18 - 0.3 - k * 0.12) / 0.3)
            if show_vpd and b > 0: d.text((x1 - 20, y + 35), vpd, font=fm, fill=CYAN + (int(255 * b),), anchor='rm')
        return im
    return render(fr, dur, out)

def median(out, dur, lang, times=None, values=None, unit=None, title=None):
    """Barres de vues/jour + ligne médiane vs moyenne."""
    import statistics as stt
    vals = values; med = stt.median(vals); avg = sum(vals) / len(vals); mx = max(vals)
    def fr(i, nn):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im)
        if title: glow_text(im, (W / 2, 90), _arg(title, lang), sg(52, 700), WHITE, r=10)
        bx0, by0, bw, bh = 300, H - 170, (W - 600) / len(vals), 650
        for k, v in enumerate(sorted(vals)):
            a = ease((t - 0.2 - k * 0.1) / 0.4); h = bh * (v / mx) * a
            d.rounded_rectangle((bx0 + k * bw + 10, by0 - h, bx0 + (k + 1) * bw - 10, by0), radius=8, fill=(VIOLET if v != mx else RED))
        c = ease((t - 1.6) / 0.5)
        if c > 0:
            for val, col, lab in [(avg, RED, {'fr': 'moyenne', 'en': 'average'}), (med, GREEN, {'fr': 'médiane', 'en': 'median'})]:
                y = by0 - bh * val / mx
                d.line((bx0, y, bx0 + (W - 600) * c, y), fill=col, width=5)
                d.text((bx0 + (W - 600) + 20, y), lab[lang], font=sg(40, 700), fill=col, anchor='lm')
        return im
    return render(fr, dur, out)

def gauges(out, dur, lang, times=None, items=None, total=None):
    """3 critères en jauges + note finale."""
    its = items[lang]
    def fr(i, nn):
        t = i / FPS; im = background(); d = ImageDraw.Draw(im)
        for k, (lab, val, col) in enumerate(its):
            t0 = 0.3 + k * (dur * 0.22); a = ease((t - t0) / 0.6)
            if a <= 0: continue
            y = 260 + k * 170
            d.text((360, y), lab, font=sg(54, 700), fill=WHITE, anchor='lm')
            d.rounded_rectangle((900, y - 22, 1560, y + 22), radius=22, fill=(30, 34, 48))
            d.rounded_rectangle((900, y - 22, 900 + 660 * val / 10 * a, y + 22), radius=22, fill=tuple(col))
            d.text((1600, y), f"{val * a:.0f}/10", font=mono(44, 700), fill=tuple(col), anchor='lm')
        if total:
            b = ease((t - dur * 0.8) / 0.5)
            if b > 0: glow_text(im, (W / 2, H - 140), _arg(total, lang), sg(64, 700), CYAN, r=12)
        return im
    return render(fr, dur, out)

# ---------- habillage (même interface que gfx.py) ----------
def lower_third(out, title, date, lang):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = sg(42, 700)
    tw = d.textlength(title, font=f); w = max(700, tw + 100); x, y, h = 60, H - 200, 120
    d.rounded_rectangle((x, y, x + w, y + h), radius=14, fill=(9, 10, 15, 225), outline=CYAN + (180,), width=2)
    d.text((x + 40, y + 46), title, font=f, fill=WHITE + (255,), anchor='lm')
    d.text((x + 40, y + 92), '> BriefAI · ' + date, font=mono(22, 500), fill=CYAN + (255,), anchor='lm'); im.save(out); return out

def badge(out, label):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = mono(24, 700); w = d.textlength(label, font=f) + 60
    d.rounded_rectangle((60, 50, 60 + w, 104), radius=10, fill=(9, 10, 15, 200), outline=CYAN + (255,), width=3)
    d.text((90, 77), label, font=f, fill=CYAN + (255,), anchor='lm'); im.save(out); return out

def end_card(out, lang, short=False, w=W, h=H):
    im = Image.new('RGBA', (w, h), BG + (255,)); d = ImageDraw.Draw(im)
    for x in range(0, w, 64): d.line((x, 0, x, h), fill=(20, 23, 34, 255))
    for y in range(0, h, 64): d.line((0, y, w, y), fill=(20, 23, 34, 255))
    f = sg(120 if not short else 110, 700); w1 = d.textlength('Brief', font=f); w2 = d.textlength('AI', font=f); cy = 150 if not short else h * 0.42
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); x = w / 2 - (w1 + w2) / 2
    ld.text((x, cy), 'Brief', font=f, fill=WHITE + (255,), anchor='lm'); ld.text((x + w1, cy), 'AI', font=f, fill=CYAN + (255,), anchor='lm')
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(16))); im.alpha_composite(lay)
    if short:
        d.text((w / 2, cy + 140), {'fr': '> vidéo complète sur YouTube_', 'en': '> full video on YouTube_'}[lang], font=mono(40, 600), fill=GREY, anchor='mm')
    else:
        for xx in (330, 1010): d.rounded_rectangle((xx, 330, xx + 580, 656), radius=14, outline=(40, 46, 64, 255), width=3)
        d.rounded_rectangle((w / 2 - 170, 780, w / 2 + 170, 850), radius=12, outline=CYAN + (255,), width=3)
        d.text((w / 2, 815), {'fr': "S'ABONNER", 'en': 'SUBSCRIBE'}[lang], font=mono(28, 700), fill=CYAN, anchor='mm')
    im.convert('RGB').save(out); return out

def thumbnail(out, big, gold, bg_frame=None, big2=None, avatar=None):
    im = background().resize((1280, 720)); d = ImageDraw.Draw(im)
    lines = [(big, WHITE)] + ([(big2, WHITE)] if big2 else []) + [(gold, CYAN)]; sz = 150
    while sz > 60 and max(d.textlength(t, font=sg(sz)) for t, _ in lines) > 700: sz -= 4
    y = 360 - sz * 1.05 * (len(lines) - 1) / 2
    for t, c in lines: glow_text(im, (60, y), t, sg(sz, 700), c, anchor='lm', r=12); y += sz * 1.05
    if avatar:
        av = Image.open(avatar).convert('RGBA').resize((380, 380)); m = av.convert('L').point(lambda p: 0 if p < 40 else min(255, (p - 40) * 4))
        av.putalpha(m); im.alpha_composite(av, (840, 170))
    im.convert('RGB').save(out, quality=92); return out
