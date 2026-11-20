"""TempoBrief — assemblage ffmpeg.
Usage: python3 assemble.py <episode_dir> <lang>
episode_dir contient: segments.json, audio/<lang>/seg01.wav..., footage/*.webm (liens), music.mp3 (optionnel)
"""
import os, sys, json, subprocess, random, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx, importlib
G = gfx

FFMPEG = ['ffmpeg', '-y', '-loglevel', 'error']

def dur_of(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    return float(out)

def silences(wav, th='-35dB', mind=0.35):
    out = subprocess.run(FFMPEG[:1] + ['-i', wav, '-af', f'silencedetect=n={th}:d={mind}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    return list(zip(starts, ends))

ALIGN = {}
SHOT_T = []; SEG_T0 = [0.0]
def load_align(ep_dir):
    f = os.path.join(ep_dir, 'align.json')
    if os.path.exists(f): ALIGN.update(json.load(open(f)))

def sentence_times(wav, sentences):
    key = os.path.basename(os.path.dirname(wav)) + '_' + os.path.splitext(os.path.basename(wav))[0]
    st = ALIGN.get(key)
    if st and len(st) == len(sentences):
        D = dur_of(wav); ends = [e for s, e in silences(wav, mind=0.18)]
        snapped = [0.0]
        for t in st[1:]:
            c = min(ends, key=lambda e: abs(e - t), default=t)
            snapped.append(c - 0.05 if abs(c - t) <= 0.7 else t)
        snapped = [max(snapped[i], snapped[i - 1] + 0.3) if i else 0.0 for i in range(len(snapped))]
        bounds = snapped + [D]
        return [(bounds[i], bounds[i + 1], sentences[i]) for i in range(len(sentences))]
    return _sentence_times_dp(wav, sentences)

def _sentence_times_dp(wav, sentences):
    """Aligne les phrases sur la voix : cibles proportionnelles au nombre de caractères, mesurées en temps de parole
    (silences exclus), puis choix ordonné des coupures parmi les silences détectés (programmation dynamique)."""
    D = dur_of(wav); sil = [(s, e) for s, e in silences(wav, mind=0.18) if s > 0.2 and e < D - 0.2]
    n = len(sentences)
    if n == 1: return [(0, D, sentences[0])]
    speech = [(0.0, D)]; segs = []; last = 0.0
    for s, e in sil: segs.append((last, s)); last = e
    segs.append((last, D)); total_speech = sum(b - a for a, b in segs)
    def speech_to_real(x):
        acc = 0.0
        for a, b in segs:
            if acc + (b - a) >= x: return a + (x - acc)
            acc += b - a
        return D
    lens = [len(x) for x in sentences]; tot = sum(lens); acc = 0; targets = []
    for l in lens[:-1]: acc += l; targets.append(speech_to_real(total_speech * acc / tot))
    cands = [(s + e) / 2 for s, e in sil]
    if len(cands) >= n - 1:
        m = len(cands); INF = 1e9
        dp = [[INF] * m for _ in range(n - 1)]; bk = [[-1] * m for _ in range(n - 1)]
        for j in range(m): dp[0][j] = abs(cands[j] - targets[0])
        for i in range(1, n - 1):
            best = INF; bj = -1
            for j in range(m):
                if j > 0 and dp[i - 1][j - 1] < best: best = dp[i - 1][j - 1]; bj = j - 1
                if bj >= 0: dp[i][j] = best + abs(cands[j] - targets[i]); bk[i][j] = bj
        j = min(range(m), key=lambda j: dp[n - 2][j]); cuts = []
        for i in range(n - 2, -1, -1): cuts.append(cands[j]); j = bk[i][j]
        cuts = cuts[::-1]
    else:
        cuts = targets
    bounds = [0] + cuts + [D]
    return [(bounds[i], bounds[i + 1], sentences[i]) for i in range(n)]

def srt_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',')

def footage_clip(src, start, length, out, crop=0.06, zoom=1.0, dim=False):
    """Sous-clip recadré (retire bords/filigranes), 1920x1080, 30 fps, sans audio."""
    vf = (f"crop=iw*{1-2*crop}:ih*{1-2*crop}:iw*{crop}:ih*{crop},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
          f"zoompan=z='min(zoom+0.0006,{zoom+0.08})':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,setsar=1")
    if dim: vf += ",gblur=sigma=8,eq=brightness=-0.32:saturation=0.6"
    subprocess.run(FFMPEG + ['-ss', f'{start:.2f}', '-t', f'{length:.2f}', '-i', src, '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', out], check=True)
    return out

def concat(clips, out):
    lst = out + '.txt'
    with open(lst, 'w') as f:
        for c in clips: f.write(f"file '{os.path.abspath(c)}'\n")
    subprocess.run(FFMPEG + ['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True); os.remove(lst); return out

def build_segment_visual(seg, lang, audio_dur, ep, tmp, used, times):
    """seg: {graphic: name|None, graphic_dur, footage: [names], shot_len:[2,4]} ou {shots:[{at, fn, ...}]}"""
    if seg.get('shots'):
        st = [a for a, b, s in times]
        def t_at(at):
            at = at[lang] if isinstance(at, dict) else at; k = int(at); fr = at - k
            if k >= len(st): return audio_dur
            nxt = st[k + 1] if k + 1 < len(st) else audio_dur
            return st[k] + fr * (nxt - st[k])
        starts = [0.0 if i == 0 else t_at(sh['at']) for i, sh in enumerate(seg['shots'])] + [audio_dur]
        clips = []
        for i, sh in enumerate(seg['shots']):
            d = max(0.5, starts[i + 1] - starts[i]); args = {k: v for k, v in sh.items() if k not in ('at', 'fn')}
            rel = [max(0.0, a - starts[i]) for a in st if starts[i] <= a < starts[i + 1]]
            fn = getattr(G, sh['fn']); o = os.path.join(tmp, f"{seg['id']}_s{i}.mp4")
            if sh['fn'] in ('counters', 'scenarios_clip', 'gauges'): args['times'] = rel
            c = fn(o, d, lang, **args)
            if i > 0:
                cf = c.replace('.mp4', '_f.mp4')
                subprocess.run(FFMPEG + ['-i', c, '-vf', 'fade=t=in:st=0:d=0.2', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', cf], check=True); c = cf
            SHOT_T.append(SEG_T0[0] + starts[i]); clips.append(c)
        out = concat(clips, os.path.join(tmp, f'{seg["id"]}_v.mp4'))
        subprocess.run(FFMPEG + ['-i', out, '-t', f'{audio_dur:.3f}', '-c', 'copy', out.replace('_v.mp4', '_vt.mp4')], check=True)
        return out.replace('_v.mp4', '_vt.mp4')
    clips = []; remaining = audio_dur; k = 0
    g = seg.get('graphic'); srcs = seg['footage']
    if g:
        st = [a for a, b, s in times]
        if seg.get('graphic_until') is not None:
            gu = seg['graphic_until']; gd = (times[gu][0] if gu < len(times) else audio_dur)
        else:
            gd = seg.get('graphic_dur', 8)
        gd = min(gd, audio_dur); fn = getattr(gfx, g)
        gfx.ALPHA = True; ov = fn(os.path.join(tmp, f'{seg["id"]}_g.mov'), gd, lang, times=st); gfx.ALPHA = False
        bgsrc = seg.get('graphic_bg', srcs[0]); D = ep['footage'][bgsrc]['dur']; wins = ep['footage'][bgsrc].get('windows') or [[5, D - 5]]
        w = max(wins, key=lambda w: w[1] - w[0]); bst = random.uniform(w[0], max(w[0], w[1] - gd))
        used.setdefault(bgsrc, []).append(bst)
        bg = footage_clip(ep['footage'][bgsrc]['path'], bst, gd, os.path.join(tmp, f'{seg["id"]}_gbg.mp4'), crop=ep['footage'][bgsrc].get('crop', 0.06), dim=True)
        comp = os.path.join(tmp, f'{seg["id"]}_gc.mp4')
        subprocess.run(FFMPEG + ['-i', bg, '-i', ov, '-filter_complex', '[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]', '-map', '[v]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-r', '30', comp], check=True)
        clips.append(comp); remaining -= gd
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
    global G
    ep = json.load(open(os.path.join(ep_dir, 'segments.json'))); load_align(ep_dir)
    G = importlib.import_module(ep.get('gfx', 'gfx'))
    tmp = os.path.join(ep_dir, 'tmp_' + lang); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    random.seed(42); used = {}
    audio_parts = []; visuals = []; subs = []; t0 = 0.0; chapters = []
    for seg in ep['segments']:
        wav = os.path.join(ep_dir, 'audio', lang, f'{seg["id"]}.wav'); D = dur_of(wav)
        chapters.append((t0, seg['title'][lang]))
        st = sentence_times(wav, seg['text'][lang])
        for a, b, s in st: subs.append((t0 + a, t0 + b, s))
        SEG_T0[0] = t0; SHOT_T.append(t0)
        visuals.append(build_segment_visual(seg, lang, D, ep, tmp, used, st)); audio_parts.append(wav); t0 += D
    total = t0
    end_png = G.end_card(os.path.join(tmp, 'end.png'), lang)
    end_mp4 = os.path.join(tmp, 'end.mp4')
    subprocess.run(FFMPEG + ['-loop', '1', '-i', end_png, '-t', '8', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', end_mp4], check=True)
    video = concat(visuals + [end_mp4], os.path.join(tmp, 'video.mp4'))
    # voix concaténée + 8 s de silence
    voice = os.path.join(tmp, 'voice.wav'); lst = voice + '.txt'
    with open(lst, 'w') as f:
        for w in audio_parts: f.write(f"file '{os.path.abspath(w)}'\n")
    subprocess.run(FFMPEG + ['-f', 'concat', '-safe', '0', '-i', lst, '-af', 'apad=pad_dur=8', voice], check=True)
    # whoosh discret à chaque changement de plan
    import numpy as np, wave as _wv
    vr = _wv.open(voice); sr = vr.getframerate(); ch = vr.getnchannels(); x = np.frombuffer(vr.readframes(vr.getnframes()), np.int16).astype(np.float32); vr.close()
    if ch > 1: x = x.reshape(-1, ch).mean(axis=1)
    rng = np.random.default_rng(7); L = int(0.35 * sr); env = np.sin(np.linspace(0, np.pi, L)) ** 2
    for ts in sorted(set(round(t, 2) for t in SHOT_T if t > 0.5)):
        nz = rng.standard_normal(L); nz = np.convolve(nz, np.ones(12) / 12, mode='same') - np.convolve(nz, np.ones(60) / 60, mode='same')
        a = int(max(0, ts - 0.15) * sr); seg_ = (nz * env * 1400)[:max(0, len(x) - a)]; x[a:a + len(seg_)] += seg_
    x = np.clip(x, -32767, 32767).astype(np.int16); vw = _wv.open(voice, 'wb'); vw.setnchannels(1); vw.setsampwidth(2); vw.setframerate(sr); vw.writeframes(x.tobytes()); vw.close()
    # overlays
    lt = G.lower_third(os.path.join(tmp, 'lt.png'), ep['title'][lang], ep['date'][lang], lang)
    bd = G.badge(os.path.join(tmp, 'badge.png'), ep['badge'][lang])
    first = ep['segments'][0]; lt_a = 0.5
    if first.get('graphic'):
        gu = first.get('graphic_until'); st0 = sentence_times(os.path.join(ep_dir, 'audio', lang, first['id'] + '.wav'), first['text'][lang])
        lt_a = (st0[gu][0] if gu is not None and gu < len(st0) else first.get('graphic_dur', 8)) + 0.3
    music = os.path.join(ep_dir, 'music.mp3')
    inputs = ['-i', video, '-i', voice, '-i', lt, '-i', bd]
    fc = (f"[0:v][2:v]overlay=0:0:enable='between(t,{lt_a:.2f},{lt_a+8:.2f})'[v1];[v1][3:v]overlay=0:0:enable='lt(t,{total})'[vout];")
    if os.path.exists(music):
        inputs += ['-stream_loop', '-1', '-i', music]
        fc += (f"[4:a]atrim=0:{total+8},volume=0.5[m];[1:a]asplit[v][vs];[m][vs]sidechaincompress=threshold=0.02:ratio=8:attack=50:release=600[md];"
               f"[v][md]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
    else:
        fc += "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]"
    out = os.path.join(ep_dir, f'{ep["slug"]}_{lang}.mp4')
    subprocess.run(FFMPEG + inputs + ['-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
    with open(os.path.join(ep_dir, f'{ep["slug"]}_{lang}.srt'), 'w', encoding='utf-8') as f:
        for i, (a, b, s) in enumerate(subs, 1): f.write(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{s}\n\n')
    with open(os.path.join(ep_dir, f'chapters_{lang}.txt'), 'w', encoding='utf-8') as f:
        for t, name in chapters: f.write(f'{int(t//60):02d}:{int(t%60):02d} {name}\n')
    json.dump({'total': total, 'subs': subs, 'chapters': chapters}, open(os.path.join(ep_dir, f'timing_{lang}.json'), 'w'), ensure_ascii=False)
    # 2e passe loudness : mesurer puis corriger le gain vers -14 LUFS
    meas = subprocess.run(['ffmpeg', '-i', out, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', meas)[-1]); gain = -14.0 - I
    if abs(gain) > 0.3:
        fixed = out.replace('.mp4', '_ln.mp4')
        subprocess.run(FFMPEG + ['-i', out, '-c:v', 'copy', '-af', f'volume={gain:.2f}dB,alimiter=limit=0.72:level=false', '-c:a', 'aac', '-b:a', '192k', fixed], check=True); os.replace(fixed, out)
    print('OK', out, round(total, 1), 's', 'LUFS', I, '->', round(I + gain, 1))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
