"""Skill-Leap-style thumbnail kit (1280x720): huge Anton words with black stroke + yellow block,
presenter cut-out with white outline, tilted screenshot card with sticker, thick curved arrow, brand tag."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
W, H = 1280, 720
YEL = (255, 214, 0); RED = (235, 38, 52); WHITE = (255, 255, 255); BLACK = (10, 10, 12)
ANTON = '/usr/share/fonts/truetype/anton/Anton-Regular.ttf'

def font(sz):
    import subprocess
    global ANTON
    try: return ImageFont.truetype(ANTON, sz)
    except OSError:
        ANTON = subprocess.check_output(['fc-match', '-f', '%{file}', 'Anton']).decode(); return ImageFont.truetype(ANTON, sz)

def word(txt, sz, fill=WHITE, stroke=10, box=None, pad=(26, 8), skew=0):
    """render one line → RGBA (optionally inside a colored block)"""
    f = font(sz); d0 = ImageDraw.Draw(Image.new('L', (1, 1))); b = d0.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    w, h = b[2] - b[0] + 2 * pad[0] + 20, b[3] - b[1] + 2 * pad[1] + 20
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if box: d.rectangle((10, 10, w - 10, h - 10), fill=box + (255,))
    d.text((10 + pad[0] - b[0], 10 + pad[1] - b[1]), txt, font=f, fill=fill + (255,), stroke_width=0 if box else stroke, stroke_fill=BLACK + (255,))
    if skew: im = im.transform((w + int(abs(skew) * h), h), Image.AFFINE, (1, skew, -abs(skew) * h if skew > 0 else 0, 0, 1, 0), Image.BICUBIC)
    return im

def shadow(im, r=14, off=(8, 10), a=160):
    s = Image.new('RGBA', (im.width + 4 * r, im.height + 4 * r), (0, 0, 0, 0))
    m = im.getchannel('A').point(lambda v: int(v * a / 255)); blk = Image.new('RGBA', im.size, (0, 0, 0, 255)); blk.putalpha(m)
    s.alpha_composite(blk, (2 * r, 2 * r)); return s.filter(ImageFilter.GaussianBlur(r)), (off[0] - 2 * r, off[1] - 2 * r)

def place(base, im, xy, rot=0, sh=True):
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if sh:
        s, o = shadow(im); base.alpha_composite(s, (int(xy[0] + o[0]), int(xy[1] + o[1])))
    base.alpha_composite(im, (int(xy[0]), int(xy[1]))); return im.size

def outline(cut, px=8, col=WHITE):
    a = cut.getchannel('A'); big = a.filter(ImageFilter.MaxFilter(px * 2 + 1))
    o = Image.new('RGBA', cut.size, col + (0,)); o.putalpha(big); o.alpha_composite(cut); return o

def card(shot, w, border=8, col=WHITE, radius=18):
    h = int(shot.height * w / shot.width); s = shot.resize((w, h), Image.LANCZOS).convert('RGBA')
    c = Image.new('RGBA', (w + 2 * border, h + 2 * border), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=radius + border, fill=col + (255,))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    c.paste(s, (border, border), m); return c

def sticker(txt, sz=46, col=RED, tc=WHITE):
    return word(txt, sz, fill=tc, box=col, pad=(18, 6))

def arrow(base, p0, p1, bend=0.35, col=YEL, w=22, head=58):
    (x0, y0), (x1, y1) = p0, p1; mx, my = (x0 + x1) / 2, (y0 + y1) / 2; nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in [i / 40 for i in range(41)]]
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ang = math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
    tip = (x1 + math.cos(ang) * head * .2, y1 + math.sin(ang) * head * .2)
    hp = [tip, (tip[0] - head * math.cos(ang - .5), tip[1] - head * math.sin(ang - .5)), (tip[0] - head * math.cos(ang + .5), tip[1] - head * math.sin(ang + .5))]
    for c, ww, hh in ((BLACK, w + 10, 1.0), (col, w, 0.0)):
        d.line(pts[:-2], fill=c + (255,), width=ww, joint='curve')
        for p in (pts[0],): d.ellipse((p[0] - ww / 2, p[1] - ww / 2, p[0] + ww / 2, p[1] + ww / 2), fill=c + (255,))
        if hh: d.polygon([(hp[0][0] + 7 * math.cos(ang), hp[0][1] + 7 * math.sin(ang)), (hp[1][0] - 6 * math.cos(ang - 1.57), hp[1][1] - 6 * math.sin(ang - 1.57)), (hp[2][0] + 6 * math.cos(ang - 1.57), hp[2][1] + 6 * math.sin(ang - 1.57))], fill=c + (255,))
        else: d.polygon(hp, fill=c + (255,))
    s, o = shadow(lay, 10, (6, 8), 120); base.alpha_composite(s, o); base.alpha_composite(lay)

def sparkle(sz, c1=(66, 133, 244), c2=(180, 120, 255)):
    """generic 4-point AI sparkle (not a brand logo)"""
    im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = sz / 2; k = sz * .12
    pts = [(r, 0), (r + k, r - k), (sz, r), (r + k, r + k), (r, sz), (r - k, r + k), (0, r), (r - k, r - k)]
    g = Image.new('RGBA', (sz, sz)); gd = ImageDraw.Draw(g)
    for y in range(sz): t = y / sz; gd.line((0, y, sz, y), fill=tuple(int(a + (b - a) * t) for a, b in zip(c1, c2)) + (255,))
    m = Image.new('L', (sz, sz), 0); ImageDraw.Draw(m).polygon(pts, fill=255); im.paste(g, (0, 0), m); return im

def brand(base, txt='BRIEF AI', xy=(34, 664)):
    f = font(34); d = ImageDraw.Draw(base); d.text(xy, txt, font=f, fill=WHITE + (235,), stroke_width=3, stroke_fill=BLACK + (255,), anchor='lm')
