# EN6 avatar shots: A1 hook (one sentence → cartoon, $0, 3 refusals), A2 verdict + CTA
import sys, os, json, subprocess, shutil
sys.path.insert(0, '/home/claude/tempo-assets/episodes/briefai-20')
from gfx20 import *
from build20 import card_img, STILLS, CLA, GEM
from PIL import Image, ImageDraw
SRC = EP + '/vids/vids_export.mp4'
def over_a1(im, t):
    D = T['A1'][1] - T['A1'][0]
    pill(im, (W / 2, 90), '“A tiny lighthouse robot afraid of the dark”', (12, 13, 20), fin(t, 0.3) * (1 - fin(t, 5.5)), size=46)
    if 4.0 < t < 15.5:
        a = fin(t, 4.0) * (1 - fin(t, 15.0)); card_img(im, STILLS[6], (1180, 200, 1840, 571), a, rot=3)
        card_img(im, STILLS[3], (1240, 560, 1820, 886), fin(t, 4.6) * (1 - fin(t, 15.0)), rot=-3)
    if t > 7.5: pill(im, (330, 300), 'Script · drawings · voice · edit', CLA, fin(t, 7.5) * (1 - fin(t, 15.5)), size=34)
    if t > 11.0: pill(im, (300, 420), '$0 extra', GREEN, fin(t, 11.0), icon='check', tc=(10, 30, 20), size=44)
    if t > 13.5: pill(im, (300, 540), '27 minutes', AMB, fin(t, 13.5), tc=(20, 20, 20), size=44)
    if t > 16.5: pill(im, (1580, 420), 'AI refused me 3×', RED, fin(t, 16.5), icon='x', size=44)
    captions(im, t, D, 'A1')
def over_a2(im, t):
    D = T['A2'][1] - T['A2'][0]
    if t > 4.0: pill(im, (1880, 260), 'Drawings: same robot every shot', GREEN, fin(t, 4.0), icon='check', tc=(10, 30, 20), size=34, anchor='rm')
    if t > 9.0: pill(im, (1880, 380), 'Animation: Veo blocked the storm', RED, fin(t, 9.0), icon='x', size=34, anchor='rm')
    if t > 15.0:
        a = fin(t, 15.0); d = ImageDraw.Draw(im); x0, y0 = 1060, 480 + 20 * (1 - a)
        d.rounded_rectangle((x0, y0, x0 + 820, y0 + 250), radius=28, fill=(24, 26, 36, int(240 * a)), outline=ORANGE + (int(255 * a),), width=4)
        d.text((x0 + 40, y0 + 45), 'MY RECIPE', font=mono(26, 700), fill=ORANGE + (int(255 * a),), anchor='lm')
        for j, ln in enumerate(['1. Character sheet first', '2. Reference shot first', '3. Sheet in EVERY prompt']):
            d.text((x0 + 40, y0 + 100 + j * 52), ln, font=sg(40, 600), fill=WHITE + (int(255 * a),), anchor='lm')
    cta(im, fin(t, D - 5.5), 'Comment CARTOON for the prompt pack')
    if t < D - 5.7: captions(im, t, D, 'A2')
def make(name, ss, dur, fn):
    tmp = f'{B}/{name}_f'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ss:.3f}', '-t', f'{dur:.3f}', '-i', SRC, '-vf', 'fps=30', f'{tmp}/%05d.png'], check=True)
    for i, f in enumerate(sorted(os.listdir(tmp))):
        im = Image.open(f'{tmp}/{f}').convert('RGBA'); fn(im, i / 30); im.convert('RGB').save(f'{tmp}/{f}', compress_level=1)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '30', '-i', f'{tmp}/%05d.png', '-frames:v', str(int(round(dur * 30))), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/{name}.mp4'], check=True)
    shutil.rmtree(tmp); print(name)
if __name__ == '__main__':
    for w in sys.argv[1:] or ['a1', 'a2']:
        make(w, T[w.upper()][0], T[w.upper()][1] - T[w.upper()][0], {'a1': over_a1, 'a2': over_a2}[w])
