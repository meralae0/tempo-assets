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
