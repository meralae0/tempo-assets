# EN4 Short (9:16, ~41 s): A1 hook + Gemini's "no hidden instructions" moment, cut from the finished long video
import sys, subprocess
sys.path.insert(0, '/home/claude/tempo-assets/tools')
from gfx_ai import sg, mono
from PIL import Image, ImageDraw
L = '/home/claude/tempo-assets/pub/b17/b17_long.mp4'; B = '/home/claude/b17'; OUT = '/home/claude/tempo-assets/pub/b17/b17_short.mp4'
parts = [(0.0, 29.93), (237.6, 248.4)]
def card(lines, sub, path, col=(255, 214, 0)):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = 170
    for ln in lines:
        f = sg(92, 700)
        while d.textlength(ln, font=f) > 1000: f = sg(f.size - 4, 700)
        b = d.textbbox((540, y), ln, font=f, anchor='mm'); d.rounded_rectangle((b[0] - 26, b[1] - 16, b[2] + 26, b[3] + 16), radius=20, fill=col + (255,))
        d.text((540, y), ln, font=f, fill=(12, 13, 20, 255), anchor='mm'); y += 135
    d.text((540, 1520), sub, font=sg(46, 700), fill=(255, 255, 255, 255), anchor='mm')
    d.text((540, 1800), 'BRIEF AI · full test on the channel', font=mono(34, 700), fill=(180, 186, 200, 255), anchor='mm')
    im.save(path)
card(['I hid a secret note', 'in this PDF'], 'Which AI will notice?', B + '/sh1.png')
card(['Then I asked Gemini', '"anything hidden?"'], 'Spoiler: page 16.', B + '/sh2.png', (255, 77, 90))
segs = []
for i, (a, b) in enumerate(parts):
    o = f'{B}/shp{i}.mp4'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(a), '-t', str(b - a), '-i', L, '-i', f'{B}/sh{i + 1}.png', '-filter_complex',
                    "[0:v]crop=1520:1080:200:0,scale=1080:-2,setsar=1[v];color=c=0x090a0f:s=1080x1920:d=%.3f[bg];[bg][v]overlay=0:520[x];[x][1:v]overlay=0:0,format=yuv420p[o]" % (b - a),
                    '-map', '[o]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-r', '30', o], check=True)
    segs.append(o)
open(B + '/shl.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', B + '/shl.txt', '-c', 'copy', '-movflags', '+faststart', OUT], check=True)
print(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', OUT]).decode())
