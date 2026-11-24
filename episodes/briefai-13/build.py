# BriefAI EN #1 (épisode 13) — "I gave 3 AIs my bank statement". Plans V1..V8 (entre les deux avatars).
# usage : python3 build.py <idx|all>   ;  timing.json : {"V":[durées V1..V8]}
import sys, os, json, csv, math
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from gfx_ai import *
from PIL import Image, ImageDraw, ImageFilter
EP = '/home/claude/tempo-assets/episodes/briefai-13'; O = '/home/claude/b13/seg'; os.makedirs(O, exist_ok=True)
V = json.load(open(EP + '/timing.json'))['V']
GPT = (16, 163, 127); CLA = (217, 119, 87); GEM = (66, 133, 244); AMBER = (255, 190, 60)
ROWS = list(csv.DictReader(open(EP + '/statement-october.csv')))
CAPS = EP + '/caps/'

def fin(t, a, b=None):
    b = a + 0.45 if b is None else b
    return max(0.0, min(1.0, ease((t - a) / (b - a))))
def money(v): return f'${v:,.2f}'
def pill(d, xy, txt, col, font, anchor='mm', pad=(22, 12), tc=None):
    x, y = xy; b = d.textbbox((x, y), txt, font=font, anchor=anchor)
    d.rounded_rectangle((b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]), radius=16, fill=col + (255,))
    d.text((x, y), txt, font=font, fill=(tc or BG) + (255,), anchor=anchor)
def check(d, c, r, col, ok=True, w=9):
    x, y = c; d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,))
    if ok: d.line((x - r * .45, y + r * .02, x - r * .1, y + r * .38, x + r * .5, y - r * .38), fill=BG + (255,), width=w, joint='curve')
    else:
        k = r * .4; d.line((x - k, y - k, x + k, y + k), fill=WHITE + (255,), width=w); d.line((x - k, y + k, x + k, y - k), fill=WHITE + (255,), width=w)
def header(im, d, t, round_txt, title, col=CYAN):
    a = fin(t, 0, .5)
    if round_txt: pill(d, (W / 2, 70 - 40 * (1 - a)), round_txt, col, sg(30, 700))
    glow_text(im, (W / 2, 150), title, sg(64), WHITE)
def shot(path, box, scale_to=None):
    im = Image.open(CAPS + path).convert('RGB').crop(box)
    if scale_to: im = im.resize((int(im.width * scale_to / im.height), scale_to), Image.LANCZOS) if isinstance(scale_to, int) else im
    return im
def card(im, img, cx, cy, w, col, a=1.0, label=None, dy=0):
    """capture réelle posée dans un cadre arrondi, avec fondu/glissement"""
    h = int(img.height * w / img.width); img = img.resize((w, h), Image.LANCZOS)
    pad = 18; fr = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); fd = ImageDraw.Draw(fr)
    fd.rounded_rectangle((0, 0, w + 2 * pad - 1, h + 2 * pad - 1), radius=22, fill=(22, 22, 24, 255), outline=col + (255,), width=4)
    fr.paste(img, (pad, pad))
    if a < 1: fr.putalpha(fr.getchannel('A').point(lambda p: int(p * a)))
    x = int(cx - fr.width / 2); y = int(cy - fr.height / 2 + 40 * (1 - a) + dy)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x + 10, y + 16, x + fr.width + 10, y + fr.height + 16), radius=22, fill=(0, 0, 0, int(120 * a)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(fr, (x, y))
    if label: d = ImageDraw.Draw(im); pill(d, (x + 30, y - 6), label, col, sg(28), anchor='lm', tc=WHITE)
    return (x + pad, y + pad)
def mapbox(org, crop, w, box):
    """box (coords capture d'origine) -> coords écran, pour une capture recadrée `crop` affichée en largeur w à l'origine org"""
    s = w / (crop[2] - crop[0]); ox, oy = org
    return (ox + (box[0] - crop[0]) * s, oy + (box[1] - crop[1]) * s, ox + (box[2] - crop[0]) * s, oy + (box[3] - crop[1]) * s)
def hl(d, box, col, prog, w=5):
    """rectangle de surlignage qui se dessine (prog 0..1)"""
    x0, y0, x1, y1 = box; per = 2 * ((x1 - x0) + (y1 - y0)); L = per * prog
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        seg = abs(bx - ax) + abs(by - ay)
        if L <= 0: break
        f = min(1, L / seg); d.line((ax, ay, ax + (bx - ax) * f, ay + (by - ay) * f), fill=col + (255,), width=w); L -= seg

# ---- relevé (tableau) ----
def statement(d, box, rows, hl_idx=(), hl_col=AMBER, dim_others=False, fs=24, scroll=0.0):
    x0, y0, x1, y1 = box; rh = fs + 16
    d.rounded_rectangle(box, radius=18, fill=(246, 247, 250, 255))
    d.rounded_rectangle((x0, y0, x1, y0 + rh + 6), radius=18, fill=(225, 229, 238, 255)); d.rectangle((x0, y0 + rh - 10, x1, y0 + rh + 6), fill=(225, 229, 238, 255))
    cols = [x0 + 24, x0 + 200, x1 - 24]
    for k, h in enumerate(['Date', 'Description', 'Amount']):
        d.text((cols[k], y0 + rh / 2 + 3), h, font=sg(fs, 700), fill=(40, 44, 56, 255), anchor='rm' if k == 2 else 'lm')
    y = y0 + rh + 6 - scroll; vis_top = y0 + rh + 6
    for i, r in enumerate(rows):
        if y > y1 - rh: break
        if y >= vis_top - 2:
            on = i in hl_idx
            if on: d.rectangle((x0 + 4, y, x1 - 4, y + rh), fill=hl_col + (255,))
            c = (30, 34, 44, 255) if (on or not dim_others) else (150, 155, 168, 255)
            v = float(r['Amount'])
            d.text((cols[0], y + rh / 2), r['Date'][5:].replace('-', '/'), font=mono(fs - 4), fill=c, anchor='lm')
            d.text((cols[1], y + rh / 2), r['Description'][:30], font=sg(fs, 500), fill=c, anchor='lm')
            vc = c if (dim_others and not on) else ((20, 140, 80, 255) if v > 0 else (200, 40, 50, 255))
            d.text((cols[2], y + rh / 2), f'{v:,.2f}', font=mono(fs - 2, 600), fill=vc, anchor='rm')
        y += rh

# V1 — le test : relevé qui défile + 3 questions
def v1(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'THE TEST', 'Same statement. Same 3 questions.')
    sc = max(0, (t - 1.0)) * 120
    statement(d, (110, 250, 900, 1030), ROWS, fs=24, scroll=min(sc, 68 * 40 - 720))
    a = fin(t, .4, 1.0); d.text((505, 232), '68 transactions · October', font=mono(26), fill=GREY + (int(255 * a),), anchor='md')
    qs = [('1', 'Groceries spent, net of refunds?'), ('2', 'Any duplicate charge?'), ('3', 'Subscriptions per year?')]
    for k, (nn, q) in enumerate(qs):
        a = fin(t, 2.0 + k * 1.6, 2.5 + k * 1.6); y = 330 + k * 170
        if a <= 0: continue
        x = 1000 + 60 * (1 - a)
        d.rounded_rectangle((x, y, x + 800, y + 130), radius=22, fill=PANEL + (int(255 * a),), outline=CYAN + (int(255 * a),), width=3)
        d.ellipse((x + 30, y + 30, x + 100, y + 100), fill=CYAN + (int(255 * a),)); d.text((x + 65, y + 65), nn, font=sg(40), fill=BG + (255,), anchor='mm')
        d.text((x + 130, y + 65), q, font=sg(40, 600), fill=WHITE + (int(255 * a),), anchor='lm')
    a = fin(t, D * 0.72, D * 0.72 + .5)
    if a > 0: pill(d, (1400, 900), 'Real answers: checked line by line', GREEN, sg(36))
    for k, (name, col) in enumerate([('ChatGPT', GPT), ('Claude', CLA), ('Gemini', GEM)]):
        a = fin(t, .6 + .2 * k, 1.1 + .2 * k); pill(d, (1170 + k * 230, 250), name, col, sg(30), tc=WHITE) if a > 0.5 else None
    return im

def three_ticks(im, d, t, start, oks, sub=None, y=860):
    for k, (name, col) in enumerate([('ChatGPT', GPT), ('Claude', CLA), ('Gemini', GEM)]):
        a = fin(t, start + k * .35, start + k * .35 + .35)
        if a <= 0: continue
        x = 560 + k * 400
        d.rounded_rectangle((x - 170, y - 60, x + 170, y + 60), radius=24, fill=PANEL + (255,), outline=col + (255,), width=4)
        d.text((x - 40, y), name, font=sg(40), fill=WHITE + (255,), anchor='mm')
        check(d, (x + 115, y), 32 * a, GREEN if oks[k] else RED, oks[k])

# V2 — doublon
def v2(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'ROUND 1', 'The duplicate charge', VIOLET)
    idx = [k for k, r in enumerate(ROWS) if r['Date'] == '2026-10-17' and 'LUNA' in r['Description']]
    sub = ROWS[idx[0] - 4: idx[1] + 4]; hi = [k - (idx[0] - 4) for k in idx]
    statement(d, (360, 230, 1560, 700), sub, hl_idx=hi if t > 1.2 else (), dim_others=t > 1.2, fs=30)
    a = fin(t, 2.0, 2.6)
    if a > 0: pill(d, (W / 2, 735), 'Luna Trattoria · Oct 17 · $56.40 × 2', AMBER, sg(38))
    three_ticks(im, d, t, D * .45, [1, 1, 1], y=900)
    return im

# V3 — abonnements
def v3(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'ROUND 2', 'Subscriptions per year', VIOLET)
    subs = [r for r in ROWS if r['Description'].startswith('RECURRING')]
    for k, r in enumerate(subs):
        a = fin(t, .5 + k * .3)
        y = 250 + k * 78; d.rounded_rectangle((520, y, 1400, y + 64), radius=14, fill=PANEL + (int(255 * a),))
        d.text((550, y + 32), r['Description'].replace('RECURRING ', ''), font=sg(32, 600), fill=WHITE + (int(255 * a),), anchor='lm')
        d.text((1370, y + 32), money(-float(r['Amount'])), font=mono(32, 600), fill=WHITE + (int(255 * a),), anchor='rm')
    a = fin(t, 2.4, 3.6); m = 85.96 * a
    d.text((W / 2, 690), f'{money(m)} / month  ×12  =', font=sg(40, 500), fill=GREY + (255,), anchor='mm')
    glow_text(im, (W / 2, 770), money(1031.52 * fin(t, 3.0, 4.2)), sg(84), GREEN)
    three_ticks(im, d, t, D * .5, [1, 1, 1], y=925)
    return im

# V4 — courses : la vraie réponse
def v4(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'ROUND 3', 'Groceries — the real number', RED)
    parts = [('FreshMart', 606.96), ('Corner Market', 71.54), ('Green Basket', 39.33), ('FreshMart refund', -23.48)]
    for k, (lab, v) in enumerate(parts):
        a = fin(t, .6 + k * .45); y = 280 + k * 100
        d.rounded_rectangle((560, y, 1360, y + 80), radius=16, fill=PANEL + (int(255 * a),))
        d.text((600, y + 40), lab, font=sg(38, 600), fill=WHITE + (int(255 * a),), anchor='lm')
        d.text((1320, y + 40), ('−' if v < 0 else '+') + money(abs(v)), font=mono(38, 600), fill=(GREEN if v < 0 else WHITE) + (int(255 * a),), anchor='rm')
    a = fin(t, 2.6, 4.0)
    d.line((560, 700, 1360, 700), fill=GREY + (255,), width=3)
    glow_text(im, (W / 2, 800), money(694.35 * a), sg(110), GREEN)
    if t > 4.2: pill(d, (W / 2, 940), 'MegaMart online orders = shopping, not groceries', DIM, sg(30), tc=WHITE)
    return im

# V5 — ChatGPT : 3 essais
CGC = {1: (655, 330, 1290, 435), 2: (670, 300, 1360, 395), 3: (670, 300, 1280, 395)}
CG = {k: shot(f'chatgpt_run{k}.jpg', c) for k, c in CGC.items()}
def v5(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'CHATGPT', 'Same question, 3 fresh chats', GPT)
    marks = []
    for k, (run, at) in enumerate([(1, .3), (2, D * .28), (3, D * .72)]):
        a = fin(t, at, at + .5)
        if a <= 0: continue
        cy = 330 + k * 240
        org = card(im, CG[run], 1010, cy, 1300, GPT, a)
        d = ImageDraw.Draw(im); d.text((150, cy), f'Try {run}', font=sg(40), fill=WHITE + (int(255 * a),), anchor='lm')
        ok = run != 2
        if t > at + .6: check(d, (1760, cy), 40, GREEN if ok else RED, ok)
        if run == 2 and t > at + .9:
            # encadré rouge autour de « $684.31 »
            bx = mapbox(org, CGC[2], 1300, (786, 306, 862, 334)); bx = (bx[0] - 8, bx[1] - 6, bx[2] + 8, bx[3] + 6)
            hl(d, bx, RED, fin(t, at + .9, at + 1.6), 6)
            if t > at + 1.7: d.text((140, cy + 50), '$10.04 short', font=sg(28, 600), fill=RED + (255,), anchor='lm')
    return im

# V6 — Claude
CLC = (270, 300, 1200, 500); CL = shot('claude_run2.jpg', CLC)
def v6(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'CLAUDE', '$874.21 — all three times', CLA)
    a = fin(t, .3, .9); org = card(im, CL, W / 2, 470, 1500, CLA, a); d = ImageDraw.Draw(im)
    if t > D * .45:
        bx = mapbox(org, CLC, 1500, (318, 340, 492, 366)); hl(d, (bx[0] - 6, bx[1] - 4, bx[2] + 6, bx[3] + 4), AMBER, fin(t, D * .45, D * .45 + .7), 6)
    a = fin(t, D * .6, D * .6 + .5)
    if a > 0:
        d.text((W / 2, 800), '$694.35  +  $179.86 MegaMart online  =  $874.21', font=sg(46, 600), fill=WHITE + (int(255 * a),), anchor='mm')
        pill(d, (W / 2, 900), 'Math: correct · Definition: its own call', AMBER, sg(36))
    return im

# V7 — Gemini
GZC = (30, 18, 1225, 122); GZ = shot('gemini_run2_line.png', GZC); GS = shot('gemini_stall.jpg', (480, 50, 1110, 250))
def v7(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'GEMINI', 'Right, with receipts', GEM)
    a = fin(t, .3, .9); org = card(im, GZ, W / 2, 330, 1600, GEM, a); d = ImageDraw.Draw(im)
    if t > 1.2:
        bx = mapbox(org, GZC, 1600, (104, 34, 216, 66)); hl(d, (bx[0] - 6, bx[1] - 4, bx[2] + 6, bx[3] + 4), GREEN, fin(t, 1.2, 1.8), 6)
    b = fin(t, D * .45, D * .45 + .5)
    if b > 0:
        d.rounded_rectangle((160, 540, 820, 700), radius=22, fill=PANEL + (255,), outline=GEM + (255,), width=3)
        d.text((490, 585), 'Time to answer', font=sg(32, 500), fill=GREY + (255,), anchor='mm')
        glow_text(im, (490, 650), f'~{int(50 * b)} s', sg(64), WHITE); d = ImageDraw.Draw(im)
    c = fin(t, D * .62, D * .62 + .5)
    if c > 0:
        card(im, GS, 1330, 720, 820, RED, c, label='Try 3'); d = ImageDraw.Draw(im)
        if t > D * .7: pill(d, (1330, 960), '2+ minutes · no answer', RED, sg(34), tc=WHITE)
    return im

# V8 — tableau des scores
def v8(i, n):
    t = i / FPS; D = n / FPS; im = background(); d = ImageDraw.Draw(im)
    header(im, d, t, 'FINAL SCORE', 'Same statement, 3 tries each')
    cols = [('ChatGPT', GPT), ('Claude', CLA), ('Gemini', GEM)]
    rows = [('Duplicate', ['3/3', '3/3', '2/2']), ('Subscriptions', ['3/3', '3/3', '2/2']), ('Groceries', ['2/3', '0/3*', '2/2']), ('Speed', ['< 15 s', '~13 s', '~50 s'])]
    x0 = 300; cw = 420
    for k, (nm, col) in enumerate(cols):
        a = fin(t, .3 + .15 * k); pill(d, (x0 + 380 + k * cw, 270), nm, col, sg(40), tc=WHITE) if a > .5 else None
    for r, (lab, vals) in enumerate(rows):
        a = fin(t, .9 + r * .5); y = 380 + r * 120
        if a <= 0: continue
        d.rounded_rectangle((x0 - 40, y - 48, x0 + 1340, y + 48), radius=16, fill=PANEL + (int(255 * a),))
        d.text((x0, y), lab, font=sg(40, 600), fill=WHITE + (int(255 * a),), anchor='lm')
        for k, v in enumerate(vals):
            good = v.startswith(('3/3', '2/2', '< 15', '~13'))
            colr = GREEN if good else (AMBER if '*' in v else (RED if v.startswith('2/3') else GREY))
            if v.startswith('~50'): colr = RED
            d.text((x0 + 380 + k * cw, y), v, font=sg(46), fill=colr + (int(255 * a),), anchor='mm')
    if t > D * .6: d.text((W / 2, 900), '* counted MegaMart online orders as groceries   ·   Gemini: 3rd try never answered', font=sg(28, 500), fill=GREY + (255,), anchor='mm')
    return im

FN = [v1, v2, v3, v4, v5, v6, v7, v8]
if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    idx = range(8) if which == 'all' else [int(x) for x in which.split(',')]
    for k in idx:
        render(FN[k], V[k], f'{O}/v{k + 1}.mp4'); print('ok', k + 1, V[k])
