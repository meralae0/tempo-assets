# EN5 avatar shots: A1 hook (3 AI tiles, 22 tests, 3 behaviours), A2 takeaway (rules = test cases) + CTA
import sys, os, json, subprocess, shutil
sys.path.insert(0, '/home/claude/tempo-assets/tools'); sys.path.insert(0, '/home/claude/tempo-assets/episodes/briefai-18')
from gfx_ai import *
from leap import *
from build import pill, fin, wrapt, captions, GPT, CLA, GEM, AMB
from PIL import Image, ImageDraw
EP = '/home/claude/tempo-assets/episodes/briefai-18'; O = '/home/claude/b18/seg'; SRC = EP + '/vids/vids_export.mp4'
T = json.load(open(EP + '/timing.json'))
def over_a1(im, t):
    D = T['A1'][1] - T['A1'][0]; f = lambda x: x * D
    pill(im, (W / 2, 90), 'Same app · 3 AIs · 1 prompt', (12, 13, 20), fin(t, 0.3) * (1 - fin(t, f(.36))), size=50)
    if t < f(.36): tiles(im, t, [(1.2, (300, 300), 'ChatGPT', GPT, 'G'), (1.6, (1620, 300), 'Claude', CLA, 'C'), (2.0, (1620, 660), 'Gemini', GEM, 'G')])
    if t > f(.22): pill(im, (330, 640), 'Right to the cent', AMB, fin(t, f(.22)) * (1 - fin(t, f(.36))), tc=(20, 20, 20), size=38)
    if t > f(.38): pill(im, (W / 2, 150), '22 tests', RED, fin(t, f(.38)), size=64)
    for k, (txt, col, fr) in enumerate([('1 tested its own work', GREEN, .66), ("1 said it hadn't", AMB, .76), ('1 just dumped the code', GEM, .85)]):
        if t > f(fr): pill(im, (1880, 420 + k * 130), txt, col, fin(t, f(fr)), size=38, tc=(10, 12, 20), anchor='rm')
    captions(im, t, D, 'A1')
def over_a2(im, t):
    D = T['A2'][1] - T['A2'][0]; f = lambda x: x * D
    if t > f(.06): pill(im, (1880, 230), 'All 3 shipped working code', GREEN, fin(t, f(.06)), icon='check', tc=(10, 30, 20), size=36, anchor='rm')
    if t > f(.3):
        a = fin(t, f(.3)); d = ImageDraw.Draw(im); x0, y0 = 1060, 350 + 20 * (1 - a)
        d.rounded_rectangle((x0, y0, x0 + 820, y0 + 260), radius=28, fill=(24, 26, 36, int(240 * a)), outline=ORANGE + (int(255 * a),), width=4)
        d.text((x0 + 40, y0 + 45), 'THE REAL SECRET', font=mono(26, 700), fill=ORANGE + (int(255 * a),), anchor='lm')
        for j, ln in enumerate(wrapt(d, 'Write your rules like test cases: exact names, “must add up to the cent”.', sg(40, 600), 740)):
            d.text((x0 + 40, y0 + 110 + j * 52), ln, font=sg(40, 600), fill=WHITE + (int(255 * a),), anchor='lm')
    if t > f(.55): pill(im, (1880, 700), 'vague rule → apps disagree', AMB, fin(t, f(.55)), size=34, tc=(20, 20, 20), anchor='rm')
    cta(im, fin(t, f(.78)), 'Prompt + the 3 apps in the description')
    if t < f(.78): captions(im, t, D, 'A2')
def make(name, ss, dur, fn):
    tmp = f'/home/claude/b18/{name}_f'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ss:.3f}', '-t', f'{dur:.3f}', '-i', SRC, '-vf', 'fps=30', f'{tmp}/%05d.png'], check=True)
    for i, f in enumerate(sorted(os.listdir(tmp))):
        im = Image.open(f'{tmp}/{f}').convert('RGBA'); fn(im, i / 30); im.convert('RGB').save(f'{tmp}/{f}', compress_level=1)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '30', '-i', f'{tmp}/%05d.png', '-frames:v', str(int(round(dur * 30))), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/{name}.mp4'], check=True)
    shutil.rmtree(tmp); print(name)
if __name__ == '__main__':
    for w in sys.argv[1:] or ['a1', 'a2']:
        make(w, T[w.upper()][0], T[w.upper()][1] - T[w.upper()][0], {'a1': over_a1, 'a2': over_a2}[w])
