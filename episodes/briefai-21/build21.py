# EN9 "5 FREE AI video tools, same horror scene" — 9 voice-over sections S1..S9, no presenter
import sys, os, json, subprocess
sys.path.insert(0, '/home/claude/tempo-assets/episodes/briefai-21')
from gfx21 import *
from PIL import Image, ImageDraw, ImageFilter
REF = Image.open(EP + '/img/hallway_1920.jpg').convert('RGB')
VEO, PIX, HAI, KLI, PIK = (66, 133, 244), (170, 90, 255), (255, 120, 80), (40, 210, 140), (255, 90, 160)
Y = 23  # vertical pad of the 705-px captures

def frames(name, w=1120):
    d = f'{B}/clip_{name}'; os.makedirs(d, exist_ok=True)
    if not os.listdir(d): subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{EP}/clips/{name}.mp4', '-vf', f'fps=30,scale={w}:-2', f'{d}/%04d.png'], check=True)
    fs = sorted(os.listdir(d)); return lambda t, loop=True: Image.open(f'{d}/{fs[min(len(fs) - 1, int(t * 30) % len(fs) if loop else int(t * 30))]}').convert('RGB')
CL = {k: frames(k) for k in ('veo', 'pixverse', 'hailuo')}
CLs = {k: frames(k, 620) for k in ('veo', 'pixverse', 'hailuo')}

def card_img(im, src, box, a=1.0, rot=0, border=6, shadow=True):
    if a <= 0: return
    x0, y0, x1, y1 = box; w, h = int(x1 - x0), int(y1 - y0)
    p = src.resize((w, h), Image.LANCZOS).convert('RGBA'); c = Image.new('RGBA', (w + 2 * border, h + 2 * border), (255, 255, 255, 255)); c.paste(p, (border, border))
    if rot: c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = 0.88 + 0.12 * eio(a); c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 25 * (1 - a)
    if shadow:
        sh = Image.new('RGBA', (c.width + 60, c.height + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((30, 40, c.width + 30, c.height + 40), fill=(0, 0, 0, int(140 * a)))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (int(cx - c.width / 2 - 30), int(cy - c.height / 2 - 30)))
    if a < 1: c.putalpha(c.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))
def head(im, t, kicker, title, col=ORANGE):
    d = ImageDraw.Draw(im); a = fin(t, 0.05)
    d.text((W / 2, 92), kicker, font=mono(32, 700), fill=col + (int(255 * a),), anchor='mm'); glow_text(im, (W / 2, 158), title, sg(62), WHITE)
def tags(im, t, d, items, y=905, t0=0.5):
    ws = [ImageDraw.Draw(im).textlength(x[0], font=sg(32, 700)) + 64 + (46 if x[2] else 0) for x in items]; gap = 24; x = W / 2 - (sum(ws) + gap * (len(ws) - 1)) / 2
    for k, (txt, col, ic) in enumerate(items):
        cx = x + ws[k] / 2; x += ws[k] + gap
        if t > t0 * d + k * 0.5: pill(im, (cx, y), txt, col, fin(t, t0 * d + k * 0.5), 32, tc=(12, 12, 16) if col in (GREEN, AMB) else WHITE, icon=ic)
def clipcard(name, col, kicker, title, items, small=False):
    def f(t, d):
        im = background(); head(im, t, kicker, title, col)
        card_img(im, CL[name](t), (W / 2 - 520, 230, W / 2 + 520, 230 + 585), fin(t, 0.1)); tags(im, t, d, items); return im
    return f

def s1():
    D = VD[0]
    def f(t, d):
        im = background(); glow_text(im, (W / 2, 110), 'Same image. Same prompt. 5 FREE tools.', sg(60), WHITE)
        cells = [('veo', 'VEO', VEO), ('pixverse', 'PIXVERSE', PIX), ('hailuo', 'HAILUO', HAI)]
        for k, (n, lab, col) in enumerate(cells):
            x = 90 + k * 600; a = fin(t, 0.3 + k * 0.35)
            card_img(im, CLs[n](t), (x, 220, x + 540, 524), a); pill(im, (x + 270, 560), lab, col, a, 34)
        for k, (lab, sub, col) in enumerate([('KLING', 'in the queue: 2+ hours', KLI), ('PIKA', '0 credits', PIK)]):
            x = 390 + k * 600; a = fin(t, 1.6 + k * 0.4); dd = ImageDraw.Draw(im)
            dd.rounded_rectangle((x, 640, x + 540, 830), radius=26, fill=(22, 24, 34, int(240 * a)), outline=col + (int(255 * a),), width=4)
            dd.text((x + 270, 700), lab, font=sg(48, 800), fill=col + (int(255 * a),), anchor='mm'); dd.text((x + 270, 770), sub, font=mono(34, 700), fill=WHITE + (int(255 * a),), anchor='mm')
        return im
    for k in range(5): SFX.append(('s1', 0.3 + k * 0.35, 'pop', -16))
    render_seg('s1', 'S1', D, [dict(img=f, w=1)])

PROMPT = 'The ceiling bulb flickers. The woman slowly turns her head toward the open door at the end of the hallway, the radio crackles in her hand. The dark shadow in the doorway slowly leans forward. Slow push-in camera. Keep the 2D animated style.'
def s2():
    D = VD[1]
    def f1(t, d):
        im = background(); head(im, t, 'THE TEST · IMAGE MADE WITH GEMINI', 'One frame, one shadow', ORANGE)
        card_img(im, REF, (W / 2 - 560, 230, W / 2 + 560, 230 + 625), fin(t, 0.2)); return im
    def f2(t, d):
        im = background(); typecard(im, t, PROMPT, t0=0.2, cps=55, label='THE SAME PROMPT FOR EVERY TOOL', a=fin(t, 0), y=300, col=ORANGE, size=40)
        tags(im, t, d, [('Free accounts', GREEN, 'check'), ('Google sign-in', VEO, None), ('Default settings', AMB, None)], y=860, t0=0.55); return im
    render_seg('s2', 'S2', D, [dict(img=f1, w=0.4), dict(img=f2, w=0.6)], seg_over=lambda im, t, D: wipe(im, t, 'THE TEST', 'Same image · same prompt', ORANGE))

def s3():
    D = VD[2]
    def ov(im, t, d, ctx):
        ring(im, ctx.R(605, 330 + Y, 1165, 375 + Y), RED, fin(t, 0.4)); pill(im, (W / 2, 150), 'Try 1: "full capacity, try again later"', RED, fin(t, 0.5), 40, icon='x')
    clip = clipcard('veo', VEO, 'TOOL 1 · VEO (INSIDE GEMINI)', 'Try 2: ready in ~3 min',
                    [('10 s · 720p', VEO, None), ('No watermark', GREEN, 'check'), ('Went beyond the prompt', AMB, None), ('Google AI Pro plan', RED, None)])
    render_seg('s3', 'S3', D, [dict(img='c_veo_capacity', w=0.25, cam=[(0, WIDE), (0.3, Z(560, 250 + Y, 1220, 420 + Y))], over=ov, sfx=[(0.3, 'buzz', -16)]),
                               dict(img=clip, w=0.75, sfx=[(0.1, 'ding', -14)])], seg_over=lambda im, t, D: wipe(im, t, 'TOOL 1', 'Veo', VEO))

def s4():
    D = VD[3]
    clip = clipcard('pixverse', PIX, 'TOOL 2 · PIXVERSE V6 · 38 OF 60 FREE CREDITS', 'Fastest: under 2 minutes',
                    [('5 s · 540p', PIX, None), ('Watermark', RED, 'x'), ('Ignored "turn her head"', RED, 'x')])
    render_seg('s4', 'S4', D, [dict(img=clip, w=1, sfx=[(0.5, 'pop', -16), (0.7, 'buzz', -18)])], seg_over=lambda im, t, D: wipe(im, t, 'TOOL 2', 'PixVerse', PIX))

def s5():
    D = VD[4]
    def notice(t, d):
        im = background(); head(im, t, 'TOOL 3 · HAILUO · 80 FREE CREDITS', 'Before upload: "I own the rights"', HAI)
        dd = ImageDraw.Draw(im); a = fin(t, 0.2)
        dd.rounded_rectangle((460, 260, 1460, 760), radius=26, fill=(24, 24, 30, int(245 * a)), outline=(80, 80, 96, int(255 * a)), width=2)
        dd.text((520, 320), 'Omni Reference Guide', font=sg(40, 700), fill=WHITE + (int(255 * a),), anchor='lm')
        for k, ln in enumerate(['You represent and warrant that all content', 'you input, submit, upload, or publish', 'is either created by you, fully owned by you,', 'or lawfully licensed to you…']):
            dd.text((520, 400 + k * 52), ln, font=sg(32, 500), fill=GREY + (int(255 * a),), anchor='lm')
        pill(im, (1330, 700), 'Confirm', WHITE, fin(t, 0.5 * d), 34, tc=(10, 10, 10))
        pill(im, (W / 2, 880), 'Default 2K ultra-wide = 60 credits → I used 768p 16:9 = 35', AMB, fin(t, 0.6 * d), 32, tc=(20, 20, 20)); return im
    clip = clipcard('hailuo', HAI, 'TOOL 3 · HAILUO (MINIMAX H3)', 'Ready in ~2.5 min',
                    [('5 s · 768p', HAI, None), ('Most faithful', GREEN, 'check'), ('Little action', AMB, None), ('Watermark', RED, 'x')])
    render_seg('s5', 'S5', D, [dict(img=notice, w=0.4, sfx=[(0.5, 'pop', -16)]), dict(img=clip, w=0.6, sfx=[(0.4, 'ding', -14)])], seg_over=lambda im, t, D: wipe(im, t, 'TOOL 3', 'Hailuo', HAI))

def s6():
    D = VD[5]
    def ov(im, t, d, ctx):
        spotlight(im, ctx.R(320, 69 + Y, 612, 233 + Y), fin(t, 0.3)); ring(im, ctx.R(325, 180 + Y, 600, 225 + Y), RED, fin(t, 0.5))
        pill(im, (W / 2, 150), '66 free credits · 1 clip = 50', KLI, fin(t, 0.3), 40, tc=(10, 30, 20))
        if t > 0.6 * d: pill(im, (W / 2, 900), '45 minutes later: still waiting', RED, fin(t, 0.6 * d), 44, icon='x')
    render_seg('s6', 'S6', D, [dict(img='c_kling_queue', w=1, cam=[(0, WIDE), (0.25, Z(300, 40 + Y, 940, 260 + Y))], over=ov, sfx=[(0.5, 'buzz', -16)])],
               seg_over=lambda im, t, D: wipe(im, t, 'TOOL 4', 'Kling', KLI))

def s7():
    D = VD[6]
    def ov(im, t, d, ctx):
        ring(im, ctx.R(1240, 18 + Y, 1345, 60 + Y), RED, fin(t, 0.4)); ring(im, ctx.R(14, 500 + Y, 152, 570 + Y), RED, fin(t, 0.7))
        pill(im, (W / 2, 900), '0 credits = nothing to test', RED, fin(t, 0.5 * d), 46, icon='x')
    render_seg('s7', 'S7', D, [dict(img='c_pika_0credits', w=1, cam=[(0, WIDE)], over=ov, sfx=[(0.4, 'buzz', -16)])], seg_over=lambda im, t, D: wipe(im, t, 'TOOL 5', 'Pika', PIK))

ROWS = [('Veo', VEO, '~3 min', '720p · 10 s', 'none', 'too much', 'AI Pro plan'),
        ('PixVerse', PIX, '<2 min', '540p · 5 s', 'yes', 'no', '456 cr'),
        ('Hailuo', HAI, '~2.5 min', '768p · 5 s', 'yes', 'yes', '420 cr'),
        ('Kling', KLI, '2 h+ queue', '720p · 5 s', '—', '—', '600 cr'),
        ('Pika', PIK, '—', '—', '—', '—', '0 free')]
def s8():
    D = VD[7]
    def f(t, d):
        im = background(); head(im, t, 'THE SCOREBOARD', 'Free tier, same prompt', ORANGE); dd = ImageDraw.Draw(im)
        cols = [150, 450, 730, 1010, 1240, 1480, 1730]; hdr = ['TOOL', 'TIME', 'OUTPUT', 'WATERMARK', 'FOLLOWED', '1 MINUTE']
        a = fin(t, 0.2)
        for k, h in enumerate(hdr): dd.text((cols[k] + (0 if k == 0 else 0), 260), h, font=mono(26, 700), fill=GREY + (int(255 * a),), anchor='lm')
        for r, row in enumerate(ROWS):
            b = fin(t, 0.5 + r * 0.4, .35)
            if b <= 0: continue
            y = 330 + r * 105; dd.rounded_rectangle((120, y - 40, W - 120, y + 40), radius=18, fill=(22, 24, 34, int(235 * b)))
            dd.rounded_rectangle((120, y - 40, 132, y + 40), radius=6, fill=row[1] + (int(255 * b),))
            for k, v in enumerate([row[0]] + list(row[2:])):
                c = WHITE
                if v in ('yes',) and k == 4: c = GREEN
                if v in ('no', 'too much') and k == 4: c = RED if v == 'no' else AMB
                if k == 3 and v == 'yes': c = RED
                if k == 3 and v == 'none': c = GREEN
                dd.text((cols[k], y), v, font=(sg(38, 800) if k == 0 else mono(30, 700)), fill=c + (int(255 * b),), anchor='lm')
        if t > 0.7 * d: pill(im, (W / 2, 900), '1 minute ≈ 12 clips · free credits = 1–2 clips', AMB, fin(t, 0.7 * d), 38, tc=(20, 20, 20))
        return im
    for k in range(5): SFX.append(('s8', 0.5 + k * 0.4, 'pop', -16))
    render_seg('s8', 'S8', D, [dict(img=f, w=1)], seg_over=lambda im, t, D: wipe(im, t, 'RESULTS', 'The scoreboard', ORANGE))

def s9():
    D = VD[8]
    def f(t, d):
        im = background(); head(im, t, 'MY ADVICE', 'Test 1 shot free → then pay 1 month', GREEN)
        for k, (n, col) in enumerate([('veo', VEO), ('pixverse', PIX), ('hailuo', HAI)]):
            x = 90 + k * 600; card_img(im, CLs[n](t), (x, 260, x + 540, 564), fin(t, 0.2 + k * 0.2))
        dd = ImageDraw.Draw(im)
        for k, ln in enumerate(['1. Use the free credits on ONE shot', '2. Keep the tool that follows your prompt', '3. Pay for one month only']):
            b = fin(t, 0.25 * d + k * 0.6); dd.text((W / 2, 700 + k * 58), ln, font=sg(42, 700), fill=WHITE + (int(255 * b),), anchor='mm')
        if t > d - 8: pill(im, (W / 2, 612), 'Prompt + image + links in the description', ORANGE, fin(t, d - 8), 34)
        if t > d - 8: dd.text((W / 2, 900), 'Some links are affiliate links · results were not changed', font=mono(24, 600), fill=GREY + (int(255 * fin(t, d - 8)),), anchor='mm')
        return im
    render_seg('s9', 'S9', D, [dict(img=f, w=1)])

if __name__ == '__main__':
    which = sys.argv[1:] or [f's{k}' for k in range(1, 10)]
    for w in which: globals()[w]()
    for w in which: json.dump([e for e in SFX if e[0] == w], open(f'{B}/sfx_{w}.json', 'w'))
