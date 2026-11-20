"""TempoBrief — graphiques animés (charte style C). Rend des clips MP4 1920x1080 via PIL + ffmpeg."""
import os, subprocess, math, shutil
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
NOIR = (11, 11, 13); GRIS = (43, 39, 36); CREME = (245, 241, 234); GCL = (217, 210, 199); OR = (201, 162, 74)
ROUGE = (190, 80, 70); VERT = (110, 160, 110)
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, '..', 'brand')

def pf(sz, w=900):
    f = ImageFont.truetype(os.path.join(BRAND, 'PlayfairDisplay.ttf'), sz); f.set_variation_by_axes([w]); return f
def inter(sz, w=600):
    f = ImageFont.truetype(os.path.join(BRAND, 'Inter.ttf'), sz); f.set_variation_by_axes([14, w]); return f

def ease(t):  # ease-out cubic, t in [0,1]
    t = max(0, min(1, t)); return 1 - (1 - t) ** 3

def spaced(d, xy, txt, font, fill, sp, anchor='mm'):
    w = sum(d.textlength(c, font=font) for c in txt) + sp * (len(txt) - 1)
    x = xy[0] - w / 2 if anchor[0] == 'm' else xy[0]
    for c in txt:
        d.text((x, xy[1]), c, font=font, fill=fill, anchor='l' + anchor[1]); x += d.textlength(c, font=font) + sp

def render(frames_fn, dur, out, alpha=None):
    alpha = ALPHA if alpha is None else alpha
    """frames_fn(i, n) -> PIL Image. Encode to out (mp4 yuv420p, or .mov prores4444 if alpha)."""
    n = int(round(dur * FPS)); tmp = out + '_frames'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i in range(n):
        frames_fn(i, n).save(os.path.join(tmp, f'{i:05d}.png'), compress_level=1)
    if alpha:
        out = os.path.splitext(out)[0] + '.mov'
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%05d.png'), '-c:v', 'qtrle', '-pix_fmt', 'argb', out]
    else:
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%05d.png'), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', out]
    subprocess.run(cmd, check=True); shutil.rmtree(tmp); return out

ALPHA = False
def base():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0)) if ALPHA else Image.new('RGB', (W, H), NOIR)

def fmt(v, lang):
    s = f'{v:,.2f}'
    return s.replace(',', ' ').replace('.', ',') if lang == 'fr' else s

# ---------- 1. Compteur 83 -> 111,50 -> 97,17 ----------
def counter_clip(out, dur, lang, times=None):
    labels = {'fr': ['PRIX D’INTRODUCTION', 'OUVERTURE', 'CLÔTURE'], 'en': ['IPO PRICE', 'OPEN', 'CLOSE']}[lang]
    vals = [83.0, 111.5, 97.17]; seg = dur / 3
    big = pf(260); small = inter(40, 700); unit = pf(110)
    st = (times[:3] if times and len(times) >= 3 else [0, seg, 2 * seg])
    def f(i, n):
        t = i / FPS; k = max([j for j in range(3) if t >= st[j]] or [0]); nxt = st[k + 1] if k < 2 else dur
        u = ease((t - st[k]) / max(0.4, (nxt - st[k]) * 0.6))
        v0 = vals[k - 1] if k else 0.0; v = v0 + (vals[k] - v0) * u
        im = base(); d = ImageDraw.Draw(im)
        col = CREME if k != 2 else OR
        txt = fmt(v, lang); tw = d.textlength(txt, font=big); uw = d.textlength('$', font=unit); gap = 40
        x0 = W / 2 - (tw + gap + uw) / 2
        d.text((x0, H / 2 - 40), txt, font=big, fill=col, anchor='lm')
        d.text((x0 + tw + gap, H / 2 - 40), '$', font=unit, fill=GCL, anchor='lm')
        spaced(d, (W / 2, H / 2 + 150), labels[k], small, GCL, 8)
        d.rectangle((W / 2 - 100, H / 2 + 215, W / 2 + 100, H / 2 + 221), fill=OR)
        return im
    return render(f, dur, out)

# ---------- 2. Graphique de séance ----------
def session_chart(out, dur, lang, times=None):
    pts = [(0, 111.5), (1, 103.0), (2, 96.66), (3, 95.79), (4, 95.89), (5, 97.17)]  # 11:48, 12:30, 13:00, 14:00, 15:00, 16:00
    xl = ['11:48', '12:30', '13:00', '14:00', '15:00', '16:00']
    ipo = 83.0; lo, hi = 78, 118; x0, x1, y0, y1 = 260, 1700, 200, 880
    def X(k): return x0 + (x1 - x0) * k / 5
    def Y(v): return y1 - (y1 - y0) * (v - lo) / (hi - lo)
    title = {'fr': 'ANT — SÉANCE DU 19 NOVEMBRE', 'en': 'ANT — NOVEMBER 19 SESSION'}[lang]
    ipol = {'fr': 'Prix d’introduction 83 $', 'en': 'IPO price $83'}[lang]
    def f(i, n):
        u = ease(i / (n * 0.55)); im = base(); d = ImageDraw.Draw(im)
        spaced(d, (x0, 110), title, inter(34, 700), GCL, 6, anchor='lm')
        for v in (80, 90, 100, 110):
            d.line((x0, Y(v), x1, Y(v)), fill=GRIS, width=2); d.text((x0 - 30, Y(v)), f'{v} $' if lang == 'fr' else f'${v}', font=inter(28), fill=GCL, anchor='rm')
        d.line((x0, Y(ipo), x1, Y(ipo)), fill=OR, width=3); d.text((x1, Y(ipo) - 22), ipol, font=inter(28, 600), fill=OR, anchor='rm')
        for k, lab in enumerate(xl): d.text((X(k), y1 + 40), lab, font=inter(28), fill=GCL, anchor='mm')
        total = 5 * u; poly = []
        for k in range(6):
            if k <= total: poly.append((X(k), Y(pts[k][1])))
        if total < 5 and len(poly):
            k = int(total); fr = total - k
            if k < 5: poly.append((X(k) + (X(k + 1) - X(k)) * fr, Y(pts[k][1] + (pts[k + 1][1] - pts[k][1]) * fr)))
        if len(poly) > 1: d.line(poly, fill=CREME, width=7, joint='curve')
        if poly:
            px, py = poly[-1]; d.ellipse((px - 14, py - 14, px + 14, py + 14), fill=OR)
        if u >= 1:
            d.text((X(0) + 20, Y(111.5) - 50), fmt(111.5, lang) + ' $', font=pf(54), fill=CREME, anchor='lm')
            d.text((X(5) - 20, Y(97.17) - 60), fmt(97.17, lang) + ' $', font=pf(54), fill=OR, anchor='rm')
        return im
    return render(f, dur, out)

# ---------- 3. Barres valorisation ----------
def bars_clip(out, dur, lang, times=None):
    rows = {'fr': [('ANTHROPIC — actions en circulation', 1270), ('ANTHROPIC — entièrement dilué', 1770), ('META', 1550)],
            'en': [('ANTHROPIC — shares outstanding', 1270), ('ANTHROPIC — fully diluted', 1770), ('META', 1550)]}[lang]
    unit = {'fr': 'milliards $', 'en': 'billion $'}[lang]
    title = {'fr': 'VALORISATION À LA CLÔTURE DU 19/11', 'en': 'VALUATION AT NOV. 19 CLOSE'}[lang]
    def f(i, n):
        im = base(); d = ImageDraw.Draw(im); spaced(d, (260, 150), title, inter(34, 700), GCL, 6, anchor='lm')
        for r, (lab, v) in enumerate(rows):
            u = ease((i / FPS - r * 0.35) / 1.2); y = 300 + r * 200
            d.text((260, y), lab, font=inter(34, 600), fill=CREME, anchor='lm')
            wmax = 1200 * v / 1800; col = OR if r == 1 else (GCL if r < 2 else GRIS)
            d.rectangle((260, y + 40, 260 + wmax * u, y + 110), fill=col)
            if u > 0.95: d.text((260 + wmax + 30, y + 75), f'{v:,}'.replace(',', ' ') + ' ' + unit, font=pf(48), fill=CREME, anchor='lm')
        return im
    return render(f, dur, out)

# ---------- 4. Courbe Nvidia -20 % ----------
def nvidia_clip(out, dur, lang, times=None):
    title = {'fr': 'NVIDIA — 3 DERNIÈRES SEMAINES', 'en': 'NVIDIA — LAST 3 WEEKS'}[lang]
    sub = {'fr': 'environ −20 % depuis fin octobre · démission du PDG Jensen Huang', 'en': 'about −20% since late October · CEO Jensen Huang resigned'}[lang]
    import random; random.seed(7); ys = [100]
    for k in range(1, 22): ys.append(ys[-1] - 1.0 + random.uniform(-1.4, 1.0))
    ys = [100 - (100 - y) * (20 / (100 - ys[-1])) for y in ys]
    x0, x1, y0, y1 = 260, 1700, 260, 860
    def f(i, n):
        u = ease(i / (n * 0.6)); im = base(); d = ImageDraw.Draw(im)
        spaced(d, (x0, 130), title, inter(34, 700), GCL, 6, anchor='lm')
        for v in (80, 90, 100): yy = y1 - (y1 - y0) * (v - 75) / 30; d.line((x0, yy, x1, yy), fill=GRIS, width=2); d.text((x0 - 30, yy), f'{v}', font=inter(28), fill=GCL, anchor='rm')
        m = max(1, int(21 * u)); pts = [(x0 + (x1 - x0) * k / 21, y1 - (y1 - y0) * (ys[k] - 75) / 30) for k in range(m + 1)]
        if len(pts) > 1: d.line(pts, fill=ROUGE, width=7, joint='curve')
        if u >= 1:
            d.text((x1, pts[-1][1] - 60), '−20 %', font=pf(72), fill=ROUGE, anchor='rm')
            d.text((x0, 940), sub, font=inter(30), fill=GCL, anchor='lm')
        return im
    return render(f, dur, out)

# ---------- 5. Cartes scénarios ----------
def scenarios_clip(out, dur, lang, times=None):
    cards = {'fr': [('1', 'LA CONFIANCE REVIENT', 'Le titre se stabilise au-dessus de 83 $'), ('2', 'LA VOLATILITÉ CONTINUE', 'Les particuliers prennent leurs bénéfices'), ('3', 'L’EFFET DOMINO', 'D’autres acteurs de l’IA entrent en bourse')],
             'en': [('1', 'CONFIDENCE RETURNS', 'The stock settles above $83'), ('2', 'VOLATILITY CONTINUES', 'Retail investors take profits'), ('3', 'THE DOMINO EFFECT', 'Other AI players rush to list')]}[lang]
    title = {'fr': 'TROIS SCÉNARIOS', 'en': 'THREE SCENARIOS'}[lang]
    def f(i, n):
        im = base(); d = ImageDraw.Draw(im); spaced(d, (W / 2, 130), title, inter(34, 700), GCL, 8)
        for k, (num, t, s) in enumerate(cards):
            t0 = times[k] if times and len(times) > k else k * (dur / 3) * 0.9
            u = ease((i / FPS - t0) / 0.8)
            if u <= 0: continue
            x = 160 + k * 560; y = 300 + (1 - u) * 60
            d.rectangle((x, y, x + 480, y + 560), fill=GRIS); d.rectangle((x, y, x + 6, y + 560), fill=OR)
            d.text((x + 40, y + 90), num, font=pf(140), fill=OR, anchor='lm')
            yy = y + 230
            for line in wrap(d, t, pf(40), 400): d.text((x + 40, yy), line, font=pf(40), fill=CREME, anchor='lm'); yy += 52
            yy += 20
            for line in wrap(d, s, inter(28), 400): d.text((x + 40, yy), line, font=inter(28), fill=GCL, anchor='lm'); yy += 38
        return im
    return render(f, dur, out)

def wrap(d, txt, font, maxw):
    words = txt.split(); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

# ---------- Overlays (PNG alpha) ----------
def lower_third(out, title, date, lang):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = pf(44); lines = wrap(d, title, f, 900); h = 60 + 54 * len(lines) + 50
    x, y = 60, H - 70 - h
    d.rectangle((x, y, x + 1000, y + h), fill=(11, 11, 13, 217)); d.rectangle((x, y, x + 8, y + h), fill=OR + (255,))
    yy = y + 50
    for l in lines: d.text((x + 40, yy), l, font=f, fill=CREME + (255,), anchor='lm'); yy += 54
    spaced(d, (x + 40, y + h - 32), 'TEMPOBRIEF', inter(22, 800), OR + (255,), 5, anchor='lm')
    d.text((x + 40 + 190, y + h - 32), '·  ' + date, font=inter(22), fill=GCL + (255,), anchor='lm')
    im.save(out); return out

def badge(out, label):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = inter(24, 800)
    w = sum(d.textlength(c, font=f) for c in label) + 5 * (len(label) - 1) + 60
    d.rounded_rectangle((60, 50, 60 + w, 104), radius=27, fill=(11, 11, 13, 180), outline=OR + (255,), width=4)
    spaced(d, (90, 77), label, f, CREME + (255,), 5, anchor='lm'); im.save(out); return out

def end_card(out, lang, short=False, w=W, h=H):
    im = Image.new('RGB', (w, h), NOIR); d = ImageDraw.Draw(im)
    if short:
        spaced(d, (w / 2, h * 0.42), 'TEMPOBRIEF', pf(110), CREME, 14); d.rectangle((w / 2 - 100, h * 0.42 + 90, w / 2 + 100, h * 0.42 + 96), fill=OR)
        spaced(d, (w / 2, h * 0.42 + 170), {'fr': 'VIDÉO COMPLÈTE SUR YOUTUBE', 'en': 'FULL VIDEO ON YOUTUBE'}[lang], inter(40, 700), GCL, 6)
    else:
        spaced(d, (w / 2, 150), 'TEMPOBRIEF', pf(100), CREME, 14); d.rectangle((w / 2 - 100, 230, w / 2 + 100, 236), fill=OR)
        for x in (330, 1010): d.rectangle((x, 330, x + 580, 656), outline=GRIS, width=3)
        d.rounded_rectangle((w / 2 - 160, 780, w / 2 + 160, 850), radius=8, outline=OR, width=4)
        spaced(d, (w / 2, 815), {'fr': 'S’ABONNER', 'en': 'SUBSCRIBE'}[lang], inter(28, 800), OR, 6)
    im.save(out); return out

def thumbnail(out, big, gold, bg_frame, big2=None):
    im = Image.new('RGB', (1280, 720), NOIR)
    if bg_frame and os.path.exists(bg_frame):
        pic = Image.open(bg_frame).convert('RGB'); pic = pic.resize((int(pic.width * 720 / pic.height), 720))
        cx = pic.width // 2; pic = pic.crop((cx - 310, 0, cx + 310, 720))
        mask = Image.new('L', (620, 720), 0); md = ImageDraw.Draw(mask); md.polygon([(80, 0), (620, 0), (620, 720), (0, 720)], fill=255)
        im.paste(pic, (660, 0), mask)
    d = ImageDraw.Draw(im); lines = [(big, CREME)] + ([(big2, CREME)] if big2 else []) + [(gold, OR)]
    maxw = 640; sz = 170
    while sz > 60 and max(d.textlength(t, font=pf(sz)) for t, _ in lines) > maxw: sz -= 4
    f = pf(sz); lh = sz * 1.05; y = 360 - lh * (len(lines) - 1) / 2
    for t, c in lines: d.text((50, y), t, font=f, fill=c, anchor='lm'); y += lh
    fl = pf(26); tw = sum(d.textlength(c, font=fl) for c in 'TEMPOBRIEF') + 5 * 9
    d.rectangle((1280 - tw - 50, 650, 1280, 710), fill=NOIR)
    spaced(d, (1280 - tw - 30, 680), 'TEMPOBRIEF', fl, CREME, 5, anchor='lm'); im.save(out, quality=92); return out
