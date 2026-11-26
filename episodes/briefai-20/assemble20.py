# EN6 assembly: a1 + v1..v10 + full cartoon (own audio) + a2, voice = Vids export spans, SFX, -14 LUFS
import subprocess, json, os, sys
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from leap import sfx_track
EP = '/home/claude/tempo-assets/episodes/briefai-20'; B = '/home/claude/b20'; S = B + '/seg'; OUT = '/home/claude/tempo-assets/pub/b20'; os.makedirs(OUT, exist_ok=True)
T = json.load(open(EP + '/timing.json')); SRC = EP + '/vids/vids_export.mp4'; CART = OUT + '/wick_and_the_dark.mp4'
def run(a): subprocess.run(a, check=True)
def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
# cartoon segment: re-encode to match (30 fps, same codec), keep its audio separately
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', CART, '-an', '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', S + '/cart.mp4'])
CD = dur(S + '/cart.mp4')
spans = [T['A1']] + T['V'] + [T['A2']]; segs = ['a1'] + [f'v{k}' for k in range(1, 11)] + ['cart', 'a2']
open(B + '/list.txt', 'w').write(''.join(f"file '{S}/{s}.mp4'\n" for s in segs))
run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', B + '/list.txt', '-c', 'copy', B + '/video.mp4'])
pre = spans[:-1]; post = spans[-1]
flt = ''.join(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a{i}];' for i, (a, b) in enumerate(pre))
flt += f'[1:a]atrim=0:{CD},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=0.9[c];'
flt += f'[0:a]atrim={post[0]}:{post[1]},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[z];'
flt += ''.join(f'[a{i}]' for i in range(len(pre))) + '[c][z]' + f'concat=n={len(pre) + 2}:v=0:a=1[v]'
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', SRC, '-i', CART, '-filter_complex', flt, '-map', '[v]', '-ar', '48000', '-ac', '2', B + '/voice.wav'])
lens = [b - a for a, b in pre] + [CD, post[1] - post[0]]; total = sum(lens)
off = {}; t = 0
for s, L in zip(segs, lens): off[s] = t; t += L
ev = [(max(0, off[s] - 0.15), 'whoosh', -14) for s in segs[1:]]
ev += [(off['a1'] + x, 'pop', -13) for x in (0.3, 4.0, 7.5, 11.0, 13.5)] + [(off['a1'] + 16.5, 'buzz', -18)]
ev += [(off['a2'] + x, 'pop', -13) for x in (4.0, 9.0, 15.0)]
for s in segs:
    f = f'{B}/sfx_{s}.json'
    if os.path.exists(f): ev += [(off[s] + e[1], e[2], e[3]) for e in json.load(open(f))]
ev = [e for e in ev if not (off['cart'] - 0.1 < e[0] < off['cart'] + CD - 0.2)]  # nothing over the cartoon
sfx_track(ev, total, B + '/sfx.wav')
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', B + '/voice.wav', '-i', B + '/sfx.wav', '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', B + '/audio.m4a'])
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', B + '/video.mp4', '-i', B + '/audio.m4a', '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', '-movflags', '+faststart', OUT + '/b20_long.mp4'])
json.dump(off, open(B + '/offsets.json', 'w'))
print(len(ev), 'sfx; total', round(total, 2), 'file', dur(OUT + '/b20_long.mp4'), 'offsets', {k: round(v, 1) for k, v in off.items()})
