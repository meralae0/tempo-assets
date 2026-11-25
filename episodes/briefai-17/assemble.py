# EN4 assembly: a1 + v1..v10 + a2, voice = Vids export spans, synthetic SFX, -14 LUFS
import subprocess, json, os, sys
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from leap import sfx_track
EP = '/home/claude/tempo-assets/episodes/briefai-17'; B = '/home/claude/b17'; S = B + '/seg'; OUT = '/home/claude/tempo-assets/pub/b17'; os.makedirs(OUT, exist_ok=True)
T = json.load(open(EP + '/timing.json')); SRC = EP + '/vids/vids_export.mp4'
spans = [T['A1']] + T['V'] + [T['A2']]; segs = ['a1'] + [f'v{k}' for k in range(1, 11)] + ['a2']
open(B + '/list.txt', 'w').write(''.join(f"file '{S}/{s}.mp4'\n" for s in segs))
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', B + '/list.txt', '-c', 'copy', B + '/video.mp4'], check=True)
flt = ''.join(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i, (a, b) in enumerate(spans)) + ''.join(f'[a{i}]' for i in range(len(spans))) + f'concat=n={len(spans)}:v=0:a=1[v]'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', SRC, '-filter_complex', flt, '-map', '[v]', '-ar', '48000', '-ac', '2', B + '/voice.wav'], check=True)
dur = sum(b - a for a, b in spans)
off = {}; t = 0
for s, (a, b) in zip(segs, spans): off[s] = t; t += b - a
ev = [(max(0, off[s] - 0.15), 'whoosh', -14) for s in segs[1:]]
ev += [(off['a1'] + x, 'pop', -12) for x in (3.0, 16.8, 17.3, 17.8, 20.2, 21.8)] + [(off['a1'] + 5.2, 'riser', -18), (off['a1'] + 24.4, 'buzz', -18)]
ev += [(off['a2'] + x, 'pop', -13) for x in (1.3, 6.0, 14.8)]
for s in segs[1:-1]:
    f = f'{B}/sfx_{s}.json'
    if os.path.exists(f): ev += [(off[s] + e[1], e[2], e[3]) for e in json.load(open(f))]
sfx_track(ev, dur, B + '/sfx.wav')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', B + '/voice.wav', '-i', B + '/sfx.wav', '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', B + '/audio.m4a'], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', B + '/video.mp4', '-i', B + '/audio.m4a', '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', '-movflags', '+faststart', OUT + '/b17_long.mp4'], check=True)
print(len(ev), 'sfx;', subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', OUT + '/b17_long.mp4']).decode().strip())
