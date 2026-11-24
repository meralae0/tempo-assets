# Montage EN2 : a1 + v1..v8 + a2, voix = extraits de l'export Vids, effets sonores (pas de musique), -14 LUFS
import subprocess, json, os, sys
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from leap import sfx_track
EP = '/home/claude/tempo-assets/episodes/briefai-15'; S = '/home/claude/b15/seg'; OUT = '/home/claude/tempo-assets/pub/b15'; os.makedirs(OUT, exist_ok=True)
T = json.load(open(EP + '/timing.json')); SRC = EP + '/vids/vids_export.mp4'
spans = [T['A1']] + T['V'] + [T['A2']]; segs = ['a1'] + [f'v{k}' for k in range(1, 9)] + ['a2']
open('/home/claude/b15/list.txt', 'w').write(''.join(f"file '{S}/{s}.mp4'\n" for s in segs))
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', '/home/claude/b15/list.txt', '-c', 'copy', '/home/claude/b15/video.mp4'], check=True)
# voix : mêmes intervalles que les plans, concaténés
flt = ''.join(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i, (a, b) in enumerate(spans)) + ''.join(f'[a{i}]' for i in range(len(spans))) + f'concat=n={len(spans)}:v=0:a=1[v]'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', SRC, '-filter_complex', flt, '-map', '[v]', '-ar', '48000', '-ac', '2', '/home/claude/b15/voice.wav'], check=True)
dur = sum(b - a for a, b in spans)
# effets : whoosh à chaque changement de plan, pops sur les cartes de l'accroche, buzz sur les 4 « FAKE », ding sur le score
ev = []; t = 0
for i, (a, b) in enumerate(spans):
    if i: ev.append((max(0, t - 0.15), 'whoosh', -14))
    t += b - a
ev += [(0.6, 'pop', -12), (1.0, 'pop', -12), (1.4, 'pop', -12)]
t7 = sum(b - a for a, b in spans[:6]); D7 = spans[6][1] - spans[6][0]
ev += [(t7 + 1.0 + k * D7 * .2 + 1.6, 'buzz', -20) for k in range(4)]
t9 = sum(b - a for a, b in spans[:8]); D9 = spans[8][1] - spans[8][0]
ev += [(t9 + D9 * .55, 'ding', -14)]
sfx_track(ev, dur, '/home/claude/b15/sfx.wav')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/home/claude/b15/voice.wav', '-i', '/home/claude/b15/sfx.wav', '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', '/home/claude/b15/audio.m4a'], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/home/claude/b15/video.mp4', '-i', '/home/claude/b15/audio.m4a', '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', OUT + '/b15_long.mp4'], check=True)
print(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', OUT + '/b15_long.mp4']).decode().strip())
