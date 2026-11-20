"""TempoBrief — shorts 9:16 depuis la vidéo longue.
Usage: python3 shorts.py <episode_dir> <lang>
segments.json: "shorts": [{"id":"s1","hook":{fr,en},"from":"seg01","to":"seg02","max":45}]
"""
import os, sys, json, subprocess, shutil, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx, importlib
FFMPEG = ['ffmpeg', '-y', '-loglevel', 'error']

def esc(s):
    return s.replace('\\', '\\\\').replace("'", "’").replace(':', '\\:').replace(',', '\\,')

def _subs_dt(a, b, subs, font):
    L = b - a; dt = ''
    for (s, e, txt) in subs:
        if e <= a or s >= b: continue
        txt = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', txt)
        txt = re.sub(r' ([;:!?%])', '\u00a0\\1', txt)
        txt = re.sub(r'(\d) ([^\W\d_]|\$)', '\\1\u00a0\\2', txt)
        words = txt.split(' '); lines = []; cur = ''
        for w in words:
            if len(cur) + len(w) + 1 <= 26: cur = (cur + ' ' + w).strip()
            else: lines.append(cur); cur = w
        if cur: lines.append(cur)
        blocks = [lines[i:i + 2] for i in range(0, len(lines), 2)]
        tot = sum(len(' '.join(bl)) for bl in blocks); t = s
        for bl in blocks:
            d_ = (e - s) * len(' '.join(bl)) / max(1, tot); bs, be = t, t + d_; t = be
            if be <= a + 0.05 or bs >= b - 0.05: continue
            for li, line in enumerate(bl):
                dt += (f",drawtext=fontfile='{font}':expansion=none:text='{esc(line)}':fontsize=62:fontcolor=0xF5F1EA:borderw=5:bordercolor=black"
                       f":x=(w-text_w)/2:y=h*0.5+260+{li*82}:enable='between(t,{max(0,bs-a):.2f},{min(L,be-a):.2f})'")
    return dt

def _body(a, b, out, subs, font, ep, clean, src, hook=None):
    L = b - a; dt = _subs_dt(a, b, subs, font)
    if hook:
        for li, line in enumerate(hook):
            dt += (f",drawtext=fontfile='{font}':expansion=none:text='{esc(line)}':fontsize=84:fontcolor=0x00D4FF:borderw=6:bordercolor=black"
                   f":x=(w-text_w)/2:y=230+{li*104}:enable='lt(t,4.5)'")
    fc = (f"[0:v]split[bg][fg];[bg]scale=-2:1920,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.3[b];[fg]scale=1188:-2,crop=1080:ih[f];"
          f"[b][f]overlay=0:(H-h)/2-180" + dt + ",setsar=1,fps=30,format=yuv420p[v];[1:a]aresample=48000,aformat=channel_layouts=stereo[a]")
    subprocess.run(FFMPEG + ['-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', clean, '-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', src, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '160k', out], check=True)

def _finish(ep_dir, ep, sh, lang, body, L, end_png):
    bar = '0x00D4FF' if ep.get('gfx') == 'gfx_ai' else '0xC9A24A'
    b2 = body.replace('_body', '_bar')
    subprocess.run(FFMPEG + ['-i', body, '-vf', f"drawbox=x=0:y=0:w='iw*t/{L:.2f}':h=14:color={bar}@1:t=fill", '-c:v', 'libx264', '-crf', '19', '-c:a', 'copy', b2], check=True)
    endc = os.path.join(ep_dir, 'shorts', f'{sh["id"]}_{lang}_end.mp4')
    subprocess.run(FFMPEG + ['-loop', '1', '-i', end_png, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', '3', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', endc], check=True)
    out = os.path.join(ep_dir, 'shorts', f'{ep["slug"]}_{sh["id"]}_{lang}.mp4')
    subprocess.run(FFMPEG + ['-i', b2, '-i', endc, '-filter_complex',
                    f"[0:v]setsar=1,fps=30,format=yuv420p[v0];[1:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a];anoisesrc=d=0.5:c=pink:a=0.6:r=48000,aformat=channel_layouts=stereo,highpass=f=300,afade=t=in:d=0.1,afade=t=out:st=0.1:d=0.4,adelay={int(L*1000)}|{int(L*1000)}[w];[a][w]amix=inputs=2:duration=first[ao]",
                    '-map', '[v]', '-map', '[ao]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', out], check=True)
    subprocess.run(FFMPEG + ['-ss', '1', '-i', out, '-frames:v', '1', out.replace('.mp4', '_cover.jpg')], check=True)
    for x in (body, b2, endc): os.remove(x)
    print('short', out, round(L + 3, 1), 's')

def main(ep_dir, lang):
    ep = json.load(open(os.path.join(ep_dir, 'segments.json'))); G = importlib.import_module(ep.get('gfx', 'gfx')); tm = json.load(open(os.path.join(ep_dir, f'timing_{lang}.json')))
    src = os.path.join(ep_dir, f'{ep["slug"]}_{lang}.mp4'); clean = os.path.join(ep_dir, f'tmp_{lang}', 'video.mp4'); subs = tm['subs']
    # bornes des segments
    bounds = {}; t = 0.0
    for seg in ep['segments']:
        wav = os.path.join(ep_dir, 'audio', lang, f'{seg["id"]}.wav')
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
        bounds[seg['id']] = (t, t + d); t += d
    font = os.path.join(gfx.BRAND, 'SpaceGrotesk.ttf' if ep.get('gfx') == 'gfx_ai' else 'Inter.ttf'); os.makedirs(os.path.join(ep_dir, 'shorts'), exist_ok=True)
    end_png = G.end_card(os.path.join(ep_dir, 'shorts', f'end_{lang}.png'), lang, short=True, w=1080, h=1920)
    only = os.environ.get('ONLY')
    for sh in ep['shorts']:
        if only and sh['id'] != only: continue
        if sh.get('parts'):
            pieces = []
            for k, (pa, pb) in enumerate(sh['parts'][lang]):
                po = os.path.join(ep_dir, 'shorts', f'{sh["id"]}_{lang}_p{k}.mp4')
                hook = sh.get('hook', {}).get(lang) if k == 0 else None
                _body(pa, pb, po, subs, font, ep, clean, src, hook); pieces.append(po)
            body = os.path.join(ep_dir, 'shorts', f'{sh["id"]}_{lang}_body.mp4'); n = len(pieces)
            ins = sum([['-i', x] for x in pieces], [])
            fcat = ''.join(f'[{i}:v][{i}:a]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]'
            subprocess.run(FFMPEG + ins + ['-filter_complex', fcat, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', '-b:a', '160k', body], check=True)
            for x in pieces: os.remove(x)
            L = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', body], capture_output=True, text=True).stdout)
            _finish(ep_dir, ep, sh, lang, body, L, end_png); continue
        a = bounds[sh['from']][0]; b = min(bounds[sh['to']][1], a + sh.get('max', 45) - 3)
        # finir sur une fin de phrase
        ends = [e for (s, e, _) in subs if a < e <= b]; b = ends[-1] if ends else b
        L = b - a
        # sous-titres incrustés (drawtext par phrase, 2 lignes max)
        dt = ''
        for (s, e, txt) in subs:
            if e <= a or s >= b: continue
            txt = re.sub(r'(\d) (\d{3})', '\\1\u00a0\\2', txt)
            txt = re.sub(r' ([;:!?%])', '\u00a0\\1', txt)
            txt = re.sub(r'(\d) ([^\W\d_]|\$)', '\\1\u00a0\\2', txt)
            words = txt.split(' '); lines = []; cur = ''
            for w in words:
                if len(cur) + len(w) + 1 <= 26: cur = (cur + ' ' + w).strip()
                else: lines.append(cur); cur = w
            if cur: lines.append(cur)
            blocks = [lines[i:i + 2] for i in range(0, len(lines), 2)]
            tot = sum(len(' '.join(bl)) for bl in blocks); t = s
            for bl in blocks:
                d_ = (e - s) * len(' '.join(bl)) / max(1, tot); bs, be = t, t + d_; t = be
                if be <= a + 0.05 or bs >= b - 0.05: continue
                for li, line in enumerate(bl):
                    dt += (f",drawtext=fontfile='{font}':expansion=none:text='{esc(line)}':fontsize=62:fontcolor=0xF5F1EA:borderw=5:bordercolor=black"
                           f":x=(w-text_w)/2:y=h*0.5+260+{li*82}:enable='between(t,{max(0,bs-a):.2f},{min(L,be-a):.2f})'")
        bar = '0x00D4FF' if ep.get('gfx') == 'gfx_ai' else '0xC9A24A'
        fc = (f"[0:v]split[bg][fg];[bg]scale=-2:1920,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.3[b];[fg]scale=1188:-2,crop=1080:ih[f];"
              f"[b][f]overlay=0:(H-h)/2-180[o];[o]drawbox=x=0:y=0:w='iw*t/{L:.2f}':h=14:color={bar}@1:t=fill" + dt + "[v]")
        body = os.path.join(ep_dir, 'shorts', f'{sh["id"]}_{lang}_body.mp4')
        subprocess.run(FFMPEG + ['-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', clean, '-ss', f'{a:.3f}', '-t', f'{L:.3f}', '-i', src, '-filter_complex', fc, '-map', '[v]', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '160k', '-r', '30', body], check=True)
        endc = os.path.join(ep_dir, 'shorts', f'{sh["id"]}_{lang}_end.mp4')
        subprocess.run(FFMPEG + ['-loop', '1', '-i', end_png, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', '3', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', endc], check=True)
        out = os.path.join(ep_dir, 'shorts', f'{ep["slug"]}_{sh["id"]}_{lang}.mp4')
        # whoosh synthétique sur la transition vers la carte de fin
        subprocess.run(FFMPEG + ['-i', body, '-i', endc, '-filter_complex',
                        f"[0:v]setsar=1,fps=30,format=yuv420p[v0];[1:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a];anoisesrc=d=0.5:c=pink:a=0.6:r=48000,aformat=channel_layouts=stereo,highpass=f=300,afade=t=in:d=0.1,afade=t=out:st=0.1:d=0.4,adelay={int(L*1000)}|{int(L*1000)}[w];[a][w]amix=inputs=2:duration=first[ao]",
                        '-map', '[v]', '-map', '[ao]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', out], check=True)
        # couverture = image à 1 s
        subprocess.run(FFMPEG + ['-ss', '1', '-i', out, '-frames:v', '1', out.replace('.mp4', '_cover.jpg')], check=True)
        os.remove(body); os.remove(endc); print('short', out, round(L + 3, 1), 's')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
