import subprocess, json, os, sys
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from leap import sfx_track
EP = '/home/claude/tempo-assets/episodes/briefai-21'; B = '/home/claude/b21'; S = B + '/seg'; OUT = '/home/claude/tempo-assets/pub/b21'; os.makedirs(OUT, exist_ok=True)
T = json.load(open(EP + '/timing.json'))['S']
def run(a): subprocess.run(a, check=True)
segs = [f's{k}' for k in range(1, 10)]
open(B + '/list.txt', 'w').write(''.join(f"file '{S}/{s}.mp4'\n" for s in segs))
run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', B + '/list.txt', '-c', 'copy', B + '/video.mp4'])
total = T[-1][1]; off = {s: T[i][0] for i, s in enumerate(segs)}
ev = [(max(0, off[s] - 0.15), 'whoosh', -14) for s in segs[1:]]
for s in segs:
    f = f'{B}/sfx_{s}.json'
    if os.path.exists(f): ev += [(off[s] + e[1], e[2], e[3]) for e in json.load(open(f))]
sfx_track(ev, total, B + '/sfx.wav')
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', EP + '/voice/vo.wav', '-i', B + '/sfx.wav', '-filter_complex',
     '[0:a]aresample=48000,aformat=channel_layouts=stereo[v];[v][1:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
     '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', B + '/audio.m4a'])
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', B + '/video.mp4', '-i', B + '/audio.m4a', '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', '-movflags', '+faststart', OUT + '/b21_long.mp4'])
json.dump(off, open(B + '/offsets.json', 'w')); print('ok', total, len(ev))
