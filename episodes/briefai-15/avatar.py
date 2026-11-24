# Plans avatar EN2 : A1 = accroche (cartes IA qui apparaissent + titre), A2 = conclusion (3 conseils + bouton orange)
import sys, os, json, subprocess, shutil
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from gfx_ai import *
from leap import *
from PIL import Image, ImageDraw
EP = '/home/claude/tempo-assets/episodes/briefai-15'; O = '/home/claude/b15/seg'; SRC = EP + '/vids/vids_export.mp4'
T = json.load(open(EP + '/timing.json'))
GPT = (16, 163, 127); CLA = (217, 119, 87); GEM = (66, 133, 244)
def fin(t, a, d=.4): return max(0., min(1., ease((t - a) / d)))
def pillx(d, xy, txt, col, f, tc=WHITE, a=1.0):
    b = d.textbbox(xy, txt, font=f, anchor='mm'); d.rounded_rectangle((b[0] - 24, b[1] - 14, b[2] + 24, b[3] + 14), radius=18, fill=col + (int(255 * a),)); d.text(xy, txt, font=f, fill=tc + (int(255 * a),), anchor='mm')
def over_a1(im, t):
    tiles(im, t, [(0.6, (300, 300), 'ChatGPT', GPT, 'G'), (1.0, (1620, 300), 'Claude', CLA, 'C'), (1.4, (1620, 640), 'Gemini', GEM, 'G')])
    d = ImageDraw.Draw(im); a = fin(t, 0.0)
    pillx(d, (W / 2, 80), 'I tried to make 3 AIs lie', (12, 13, 20), sg(56), a=a * 0.92)
    for k, (txt, t0) in enumerate([('A book that doesn’t exist', 4.2), ('A Nobel Prize that doesn’t exist', 5.8), ('A court case I made up', 7.4)]):
        b = fin(t, t0) * (1 - fin(t, 9.4))
        if b > 0: pillx(d, (380, 620 + k * 100), txt, RED, sg(38), a=b)
def over_a2(im, t):
    d = ImageDraw.Draw(im)
    for k, (txt, col, t0) in enumerate([('ChatGPT · quick answers', GPT, 3.0), ('Claude · explained & checked', CLA, 4.6), ('Gemini · alternatives (slower)', GEM, 6.2)]):
        a = fin(t, t0)
        if a > 0: pillx(d, (1540, 300 + k * 120), txt, col, sg(40), a=a)
    if t > 9.5: pillx(d, (1540, 700), 'Money · law · health → ask for the source', (12, 13, 20), sg(34), a=fin(t, 9.5))
    cta(im, fin(t, 12.0), 'All prompts in the description')
def make(name, ss, dur, fn):
    tmp = f'/home/claude/b15/{name}_f'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ss:.3f}', '-t', f'{dur:.3f}', '-i', SRC, '-vf', 'fps=30', f'{tmp}/%05d.png'], check=True)
    for i, f in enumerate(sorted(os.listdir(tmp))):
        im = Image.open(f'{tmp}/{f}').convert('RGBA'); fn(im, i / FPS); im.convert('RGB').save(f'{tmp}/{f}', compress_level=1)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '30', '-i', f'{tmp}/%05d.png', '-frames:v', str(int(round(dur * 30))), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/{name}.mp4'], check=True)
    shutil.rmtree(tmp); print(name)
if __name__ == '__main__':
    make('a1', T['A1'][0], T['A1'][1] - T['A1'][0], over_a1)
    make('a2', T['A2'][0], T['A2'][1] - T['A2'][0], over_a2)
