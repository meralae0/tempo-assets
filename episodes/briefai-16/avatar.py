# EN3 avatar shots: A1 hook (3 job tiles), A2 verdict pills + CTA
import sys, os, json, subprocess, shutil
sys.path.insert(0, '/home/claude/tempo-assets/tools'); sys.path.insert(0, '/home/claude/tempo-assets/episodes/briefai-16')
from gfx_ai import *
from leap import *
from build import pill, fin, GEM, AMB, NEON
from PIL import Image, ImageDraw
EP = '/home/claude/tempo-assets/episodes/briefai-16'; O = '/home/claude/b16/seg'; SRC = EP + '/vids/vids_export.mp4'
T = json.load(open(EP + '/timing.json'))
def over_a1(im, t):
    pill(im, (W / 2, 90), 'I gave Gemini 4 Neon 3 real jobs', (12, 13, 20), fin(t, 0.3), size=50)
    tiles(im, t, [(8.0, (330, 330), 'Game', NEON, '1'), (10.1, (1590, 330), 'Statement', GREEN, '2'), (11.7, (1590, 690), 'Trip', AMB, '3')])
    if t > 13.6: pill(im, (330, 640), '2 went perfectly', GREEN, fin(t, 13.6), icon='check', tc=(10, 30, 20), size=38)
    if t > 15.9: pill(im, (330, 760), '1 broke halfway', RED, fin(t, 15.9), icon='x', size=38)
def over_a2(im, t):
    for k, (txt, col, t0, ic, tc) in enumerate([('Small apps: yes · expect a bug', NEON, 2.3, 'check', (10, 20, 20)), ('Files & money: perfect on my test', GREEN, 9.5, 'check', (10, 30, 20)), ('Task mode: the real surprise', AMB, 12.9, 'check', (20, 20, 20))]):
        if t > t0: pill(im, (1880, 300 + k * 130), txt, col, fin(t, t0), icon=ic, tc=tc, size=36, anchor='rm')
    if t > 16.7: pill(im, (1880, 700), 'Tonight: upload last month\'s statement', (12, 13, 20), fin(t, 16.7), size=34, anchor='rm')
    cta(im, fin(t, 21.2), 'All 3 prompts in the description')
def make(name, ss, dur, fn):
    tmp = f'/home/claude/b16/{name}_f'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ss:.3f}', '-t', f'{dur:.3f}', '-i', SRC, '-vf', 'fps=30', f'{tmp}/%05d.png'], check=True)
    for i, f in enumerate(sorted(os.listdir(tmp))):
        im = Image.open(f'{tmp}/{f}').convert('RGBA'); fn(im, i / 30); im.convert('RGB').save(f'{tmp}/{f}', compress_level=1)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '30', '-i', f'{tmp}/%05d.png', '-frames:v', str(int(round(dur * 30))), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{O}/{name}.mp4'], check=True)
    shutil.rmtree(tmp); print(name)
if __name__ == '__main__':
    make('a1', T['A1'][0], T['A1'][1] - T['A1'][0], over_a1)
    make('a2', T['A2'][0], T['A2'][1] - T['A2'][0], over_a2)
