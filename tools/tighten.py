"""Raccourcit les pauses d'une voix TTS : toute pause > max_pause est ramenée à max_pause.
Usage: python3 tighten.py in.wav out.wav [max_pause=0.38] [tail=0.35]"""
import sys, wave, numpy as np

def main(src, dst, max_pause=0.38, tail=0.35, th_db=-40):
    w = wave.open(src); sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32); w.close()
    if ch > 1: x = x.reshape(-1, ch).mean(axis=1)
    win = int(sr * 0.02); n = len(x) // win
    rms = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-9) / 32768
    silent = 20 * np.log10(rms + 1e-9) < th_db
    keep = np.ones(n, bool); maxw = int(max_pause / 0.02); i = 0
    # silence initial : garder 0.08 s
    while i < n and silent[i]: i += 1
    keep[:max(0, i - 4)] = False
    while i < n:
        if silent[i]:
            j = i
            while j < n and silent[j]: j += 1
            if j < n and j - i > maxw:  # pause interne trop longue
                cut = (j - i) - maxw; a = i + maxw // 2; keep[a:a + cut] = False
            elif j >= n:  # silence final : supprimé, on ajoute tail ensuite
                keep[i + 2:] = False
            i = j
        else: i += 1
    # reconstruire avec petits fondus aux coupures (5 ms)
    out = []; fade = int(sr * 0.005); k = 0
    while k < n:
        if keep[k]:
            m = k
            while m < n and keep[m]: m += 1
            seg = x[k * win:m * win].copy()
            if len(seg) > 2 * fade:
                seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
            out.append(seg); k = m
        else: k += 1
    y = np.concatenate(out + [np.zeros(int(sr * tail), np.float32)])
    wo = wave.open(dst, 'wb'); wo.setnchannels(1); wo.setsampwidth(2); wo.setframerate(sr)
    wo.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes()); wo.close()
    return len(y) / sr

if __name__ == '__main__':
    a = sys.argv
    print(round(main(a[1], a[2], float(a[3]) if len(a) > 3 else 0.38, float(a[4]) if len(a) > 4 else 0.35), 2))
