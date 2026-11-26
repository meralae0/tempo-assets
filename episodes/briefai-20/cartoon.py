"""Assemble the 60 s cartoon 'Wick and the Dark' from 6 Gemini stills (+ optional Veo clips) and the AI Studio narration."""
import subprocess, os, json, sys
W, H, FPS = 1920, 1080, 30
# shot boundaries from silencedetect on voice/narr.wav (mid-silence), last shot gets a 2.3 s tail
CUTS = [0, 8.75, 17.2, 23.6, 31.75, 41.9, 53.5]
MOVES = ['in', 'in', 'out', 'pan', 'up', 'out']  # camera move per still
CLIPS = {k: f'clips/s{k}.mp4' for k in (3, 6) if os.path.exists(f'clips/s{k}.mp4')}
os.makedirs('seg', exist_ok=True)
def run(a): subprocess.run(a, check=True)

def still(i, d, mv):
    n = int(round(d * FPS)); src = f'img/s{i}.png'
    z = {'in': f"1+0.12*on/{n}", 'out': f"1.12-0.12*on/{n}", 'pan': "1.10", 'up': "1.10"}[mv]
    x = {'pan': f"(iw-iw/zoom)*on/{n}", 'up': "(iw-iw/zoom)/2"}.get(mv, "(iw-iw/zoom)/2")
    y = {'up': f"(ih-ih/zoom)*(1-on/{n})"}.get(mv, "(ih-ih/zoom)/2")
    vf = (f"scale=3840:2144,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS},"
          f"format=yuv420p")
    run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-vf', vf, '-frames:v', str(n), '-c:v', 'libx264',
         '-preset', 'veryfast', '-crf', '18', f'seg/{i}.mp4'])

def clip(i, d):
    # Veo clip (8 s) then hold on the still with a slow zoom for the remainder
    c = CLIPS[i]; cd = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', c]))
    cd = min(cd, d)
    run(['ffmpeg', '-y', '-v', 'error', '-i', c, '-t', str(cd), '-an', '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', f'seg/{i}a.mp4'])
    rest = d - cd
    if rest > 0.1:
        # freeze last frame of the clip with a slow push-in
        run(['ffmpeg', '-y', '-v', 'error', '-sseof', '-0.1', '-i', c, '-frames:v', '1', f'seg/{i}last.png'])
        n = int(round(rest * FPS))
        run(['ffmpeg', '-y', '-v', 'error', '-i', f'seg/{i}last.png', '-vf',
             f"scale=3840:2160,zoompan=z='1+0.06*on/{n}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={n}:s={W}x{H}:fps={FPS},format=yuv420p",
             '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', f'seg/{i}b.mp4'])
        open(f'seg/{i}.txt', 'w').write(f"file '{i}a.mp4'\nfile '{i}b.mp4'\n")
        run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'seg/{i}.txt', '-c', 'copy', f'seg/{i}.mp4'])
    else:
        os.replace(f'seg/{i}a.mp4', f'seg/{i}.mp4')

XF = 0.4; DEL = 0.5
DUR = [CUTS[k + 1] - CUTS[k] + (DEL if k == 0 else 0) + (XF if k < 5 else 0) for k in range(6)]
for k in range(6):
    i = k + 1; d = DUR[k]
    (clip if i in CLIPS else still)(*( (i, d) if i in CLIPS else (i, d, MOVES[k]) ))
    print('shot', i, round(d, 2), 'veo' if i in CLIPS else MOVES[k])

# crossfade chain
inputs = []; [inputs.extend(['-i', f'seg/{k}.mp4']) for k in range(1, 7)]
fc = []; prev = '[0:v]'
for k in range(1, 6):
    out = f'[x{k}]'; fc.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={CUTS[k] + DEL:.3f}{out}"); prev = out
T = sum(DUR) - 5 * XF
# title card on the first 3 s, end card on the last 2 s
font = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
fc.append(f"{prev}drawtext=fontfile={font}:text='Wick and the Dark':fontsize=110:fontcolor=white:borderw=6:bordercolor=0x1a1030:"
          f"x=(w-tw)/2:y=h*0.14:alpha='if(lt(t,0.4),t/0.4,if(lt(t,2.6),1,if(lt(t,3.2),(3.2-t)/0.6,0)))',"
          f"fade=t=in:st=0:d=0.6,fade=t=out:st={T - 0.8:.2f}:d=0.8[v]")
# audio: narration delayed so it lines with cuts (cuts were measured on the narration itself, so offset grows by XF per cut)
# simpler: narration starts at 0.5 s, soft music bed under it
run(['ffmpeg', '-y', '-v', 'error', *inputs, '-i', 'voice/narr.wav', '-stream_loop', '-1', '-i', '../briefai-01/music.mp3',
     '-filter_complex', ';'.join(fc) + f";[6:a]adelay=500|500,apad[n];[7:a]volume=0.10,atrim=0:{T:.2f},afade=t=in:d=1.5,afade=t=out:st={T - 2.5:.2f}:d=2.5[m];"
     f"[n][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:{T:.2f},loudnorm=I=-14:TP=-1.5[a]",
     '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-c:a', 'aac', '-b:a', '192k',
     '-r', str(FPS), 'wick_and_the_dark.mp4'])
print('total', round(T, 2))
