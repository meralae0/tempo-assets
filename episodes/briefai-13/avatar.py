# Plans avatar (Google Vids) avec habillage : A1 = intro (0 → A1), A2 = conclusion (A2_start → fin)
import sys, os, json, subprocess, shutil
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from gfx_ai import *
from PIL import Image, ImageDraw
EP = '/home/claude/tempo-assets/episodes/briefai-13'; O = '/home/claude/b13/seg'; SRC = EP + '/vids/vids_export.mp4'
T = json.load(open(EP + '/timing.json'))
GPT = (16, 163, 127); CLA = (217, 119, 87); GEM = (66, 133, 244); AMBER = (255, 190, 60)
def fin(t, a, b=None):
    b = a + .4 if b is None else b; return max(0., min(1., ease((t - a) / (b - a))))
def pill(d, xy, txt, col, font, anchor='mm', pad=(24, 14), tc=WHITE, alpha=255):
    b = d.textbbox(xy, txt, font=font, anchor=anchor)
    d.rounded_rectangle((b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]), radius=18, fill=col + (alpha,))
    d.text(xy, txt, font=font, fill=tc + (alpha,), anchor=anchor)
def over_a1(im, t):
    d = ImageDraw.Draw(im)
    # 0-3 s : le résultat d'abord
    a = fin(t, 0.0, .35) * (1 - fin(t, 3.4, 3.8))
    if a > 0:
        pill(d, (W / 2, 120), 'Same bank statement · 3 AIs · 1 wrong number', RED, sg(54), alpha=int(255 * a))
    # 3.6 s → : les trois noms
    for k, (nm, col) in enumerate([('ChatGPT', GPT), ('Claude', CLA), ('Gemini', GEM)]):
        b = fin(t, 3.8 + .25 * k)
        if b > 0: pill(d, (1530, 330 + k * 120 - 20 * (1 - b)), nm, col, sg(48), alpha=int(255 * b))
    c = fin(t, 7.2)
    if c > 0: pill(d, (W / 2, 960), '68 transactions  ·  3 questions  ·  3 tries each', PANEL, mono(36, 600), alpha=int(235 * c))
def over_a2(im, t):
    d = ImageDraw.Draw(im)
    for k, txt in enumerate(['1. Ask for the line items', '2. Ask twice']):
        a = fin(t, 2.0 + 1.6 * k)
        if a > 0: pill(d, (1570, 330 + k * 130 + 20 * (1 - a)), txt, GREEN if k == 0 else CYAN, sg(54), tc=BG, alpha=int(255 * a))
    b = fin(t, 5.6)
    if b > 0: pill(d, (W / 2, 960), 'Exact prompt in the description', PANEL, sg(40), alpha=int(235 * b))
def make(name, ss, dur, fn):
    tmp = f'/home/claude/b13/{name}_f'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ss:.3f}', '-t', f'{dur:.3f}', '-i', SRC, '-vf', 'fps=30', f'{tmp}/%05d.png'], check=True)
    fs = sorted(os.listdir(tmp))
    for i, f in enumerate(fs):
        im = Image.open(f'{tmp}/{f}').convert('RGBA'); fn(im, i / FPS); im.convert('RGB').save(f'{tmp}/{f}', compress_level=1)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '30', '-i', f'{tmp}/%05d.png', '-frames:v', str(int(round(dur * 30))), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/{name}.mp4'], check=True)
    shutil.rmtree(tmp); print(name, len(fs))
if __name__ == '__main__':
    tot = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SRC]))
    make('a1', 0, T['A1'], over_a1)
    make('a2', T['A2_start'], tot - T['A2_start'], over_a2)
