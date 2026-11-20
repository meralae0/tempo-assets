"""TempoBrief — assemblage ffmpeg.
Usage: python3 assemble.py <episode_dir> <lang>
episode_dir contient: segments.json, audio/<lang>/seg01.wav..., footage/*.webm (liens), music.mp3 (optionnel)
"""
import os, sys, json, subprocess, random, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx

FFMPEG = ['ffmpeg', '-y', '-loglevel', 'error']

def dur_of(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    return float(out)

def silences(wav, th='-35dB', mind=0.35):
    out = subprocess.run(FFMPEG[:1] + ['-i', wav, '-af', f'silencedetect=n={th}:d={mind}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    return list(zip(starts, ends))

def sentence_times(wav, sentences):
    """Répartit les phrases sur la durée du wav en s'appuyant sur les silences détectés."""
    D = dur_of(wav); sil = silences(wav)
    cuts = [ (s + e) / 2 for s, e in sil if s > 0.3 and e < D - 0.3 ]
    n = len(sentences)
    if len(cuts) >= n - 1:
        # choisir les n-1 coupures les plus proches des positions proportionnelles
        lens = [len(x) for x in sentences]; tot = sum(lens); acc = 0; targets = []
        for l in lens[:-1]: acc += l; targets.append(D * acc / tot)
        chosen = []
        for t in targets:
            c = min((c for c in cuts if c not in chosen), key=lambda c: abs(c - t), default=t); chosen.append(c)
        bounds = [0] + sorted(chosen) + [D]
    else:
        lens = [len(x) for x in sentences]; tot = sum(lens); acc = 0; bounds = [0]
        for l in lens: acc += l; bounds.append(D * acc / tot)
    return [(bounds[i], bounds[i + 1], sentences[i]) for i in range(n)]

def srt_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',')

def footage_clip(src, start, length, out, crop=0.06, zoom=1.0):
    """Sous-clip recadré (retire bords/filigranes), 1920x1080, 30 fps, sans audio."""
    vf = (f"crop=iw*{1-2*crop}:ih*{1-2*crop}:iw*{crop}:ih*{crop},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
          f"zoompan=z='min(zoom+0.0006,{zoom+0.08})':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,setsar=1")
    subprocess.run(FFMPEG + ['-ss', f'{start:.2f}', '-t', f'{length:.2f}', '-i', src, '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', out], check=True)
    return out

def concat(clips, out):
    lst = out + '.txt'
    with open(lst, 'w') as f:
        for c in clips: f.write(f"file '{os.path.abspath(c)}'\n")
    subprocess.run(FFMPEG + ['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True); os.remove(lst); return out

def build_segment_visual(seg, lang, audio_dur, ep, tmp, used):
    """seg: {graphic: name|None, graphic_dur, footage: [names], shot_len:[2,4]}"""
    clips = []; remaining = audio_dur; k = 0
    g = seg.get('graphic')
    if g:
        gd = min(seg.get('graphic_dur', 8), audio_dur); fn = getattr(gfx, g)
        clips.append(fn(os.path.join(tmp, f'{seg["id"]}_g.mp4'), gd, lang)); remaining -= gd
    srcs = seg['footage']
    while remaining > 0.4:
        L = min(remaining, random.uniform(2.2, 4.0)); src = srcs[k % len(srcs)]; k += 1
        D = ep['footage'][src]['dur']; wins = ep['footage'][src].get('windows') or [[5, D - 5]]
        for _ in range(20):
            w = random.choice(wins); st = random.uniform(w[0], max(w[0], w[1] - L))
            if all(abs(st - u) > 6 for u in used.get(src, [])): break
        used.setdefault(src, []).append(st)
        clips.append(footage_clip(ep['footage'][src]['path'], st, L, os.path.join(tmp, f'{seg["id"]}_{k:02d}.mp4'), crop=ep['footage'][src].get('crop', 0.06)))
        remaining -= L
    out = concat(clips, os.path.join(tmp, f'{seg["id"]}_v.mp4'))
    # ajuster à la durée exacte de l'audio
    subprocess.run(FFMPEG + ['-i', out, '-t', f'{audio_dur:.3f}', '-c', 'copy', out.replace('_v.mp4', '_vt.mp4')], check=True)
    return out.replace('_v.mp4', '_vt.mp4')

def main(ep_dir, lang):
    ep = json.load(open(os.path.join(ep_dir, 'segments.json')))
    tmp = os.path.join(ep_dir, 'tmp_' + lang); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    random.seed(42); used = {}
    audio_parts = []; visuals = []; subs = []; t0 = 0.0; chapters = []
    for seg in ep['segments']:
        wav = os.path.join(ep_dir, 'audio', lang, f'{seg["id"]}.wav'); D = dur_of(wav)
        chapters.append((t0, seg['title'][lang]))
        for a, b, s in sentence_times(wav, seg['text'][lang]): subs.append((t0 + a, t0 + b, s))
        visuals.append(build_segment_visual(seg, lang, D, ep, tmp, used)); audio_parts.append(wav); t0 += D
    total = t0
    end_png = gfx.end_card(os.path.join(tmp, 'end.png'), lang)
    end_mp4 = os.path.join(tmp, 'end.mp4')
    subprocess.run(FFMPEG + ['-loop', '1', '-i', end_png, '-t', '8', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', end_mp4], check=True)
    video = concat(visuals + [end_mp4], os.path.join(tmp, 'video.mp4'))
    # voix concaténée + 8 s de silence
    voice = os.path.join(tmp, 'voice.wav'); lst = voice + '.txt'
    with open(lst, 'w') as f:
        for w in audio_parts: f.write(f"file '{os.path.abspath(w)}'\n")
    subprocess.run(FFMPEG + ['-f', 'concat', '-safe', '0', '-i', lst, '-af', 'apad=pad_dur=8', voice], check=True)
    # overlays
    lt = gfx.lower_third(os.path.join(tmp, 'lt.png'), ep['title'][lang], ep['date'][lang], lang)
    bd = gfx.badge(os.path.join(tmp, 'badge.png'), ep['badge'][lang])
    music = os.path.join(ep_dir, 'music.mp3')
    inputs = ['-i', video, '-i', voice, '-i', lt, '-i', bd]
    fc = (f"[0:v][2:v]overlay=0:0:enable='between(t,1,9)'[v1];[v1][3:v]overlay=0:0:enable='lt(t,{total})'[vout];")
    if os.path.exists(music):
        inputs += ['-stream_loop', '-1', '-i', music]
        fc += (f"[4:a]atrim=0:{total+8},volume=0.5[m];[1:a]asplit[v][vs];[m][vs]sidechaincompress=threshold=0.02:ratio=8:attack=50:release=600[md];"
               f"[v][md]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    else:
        fc += "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
    out = os.path.join(ep_dir, f'{ep["slug"]}_{lang}.mp4')
    subprocess.run(FFMPEG + inputs + ['-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
    with open(os.path.join(ep_dir, f'{ep["slug"]}_{lang}.srt'), 'w', encoding='utf-8') as f:
        for i, (a, b, s) in enumerate(subs, 1): f.write(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{s}\n\n')
    with open(os.path.join(ep_dir, f'chapters_{lang}.txt'), 'w', encoding='utf-8') as f:
        for t, name in chapters: f.write(f'{int(t//60):02d}:{int(t%60):02d} {name}\n')
    json.dump({'total': total, 'subs': subs, 'chapters': chapters}, open(os.path.join(ep_dir, f'timing_{lang}.json'), 'w'), ensure_ascii=False)
    print('OK', out, round(total, 1), 's')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
