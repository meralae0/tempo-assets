"""Raccourcit les blancs d'un short (vidéo + audio) : tout silence > 0,7 s est ramené à 0,35 s. La carte de fin (3 dernières s) est gardée.
Usage: python3 deadair.py in.mp4 out.mp4"""
import sys, re, subprocess
src, dst = sys.argv[1], sys.argv[2]
D = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
o = subprocess.run(['ffmpeg', '-i', src, '-af', 'highpass=f=120,silencedetect=n=-38dB:d=0.7', '-f', 'null', '-'], capture_output=True, text=True).stderr
S = list(zip(map(float, re.findall(r'silence_start: ([\d.]+)', o)), map(float, re.findall(r'silence_end: ([\d.]+)', o))))
keep = []; t = 0.0
for a, b in S:
    if b > D - 3.2: break
    keep.append((t, a + 0.2)); t = b - 0.15
keep.append((t, D))
fc = ''.join(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}];" for i, (a, b) in enumerate(keep))
fc += ''.join(f'[v{i}][a{i}]' for i in range(len(keep))) + f'concat=n={len(keep)}:v=1:a=1[v][a]'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', '-b:a', '160k', dst], check=True)
print(dst, round(D, 1), '->', round(sum(b - a for a, b in keep), 1), 's', len(keep) - 1, 'blancs raccourcis')
