"""Ré-encode une vidéo pour tenir sous une taille cible (GitHub < 100 Mo), en 2 passes.
Usage: python3 export.py in.mp4 out.mp4 [target_mb=90]"""
import sys, subprocess, os

def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)

def main(src, dst, target_mb=90):
    if os.path.getsize(src) <= target_mb * 1e6:
        subprocess.run(['cp', src, dst], check=True); return os.path.getsize(dst)
    d = dur(src); total_kbps = target_mb * 8e3 / d; v = int(total_kbps - 192 - 60)
    log = dst + '.log'
    base = ['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-c:v', 'libx264', '-preset', 'slow', '-b:v', f'{v}k', '-maxrate', f'{int(v*1.6)}k', '-bufsize', f'{v*3}k', '-pix_fmt', 'yuv420p', '-passlogfile', log]
    subprocess.run(base + ['-pass', '1', '-an', '-f', 'mp4', '/dev/null'], check=True)
    subprocess.run(base + ['-pass', '2', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', dst], check=True)
    for f in os.listdir(os.path.dirname(os.path.abspath(dst))):
        if f.startswith(os.path.basename(log)): os.remove(os.path.join(os.path.dirname(os.path.abspath(dst)), f))
    return os.path.getsize(dst)

if __name__ == '__main__':
    print(round(main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 90) / 1e6, 1), 'MB')
