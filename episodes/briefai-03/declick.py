"""Supprime les pops isolés (rafales < 130 ms entourées de silence) et adoucit les bords de chaque phrase (fondu 6 ms)."""
import wave, numpy as np, glob, sys, scipy.signal as ss
TPL = np.load('pop_tpl.npy'); TPL = TPL / np.linalg.norm(TPL); LT = len(TPL)
SR = 24000; W = 120  # 5 ms
def proc(f):
    w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64); w.close()
    c = ss.fftconvolve(a, TPL[::-1], 'valid'); cs = np.concatenate([[0], np.cumsum(a ** 2)]); r = c / np.sqrt(np.maximum(cs[LT:] - cs[:-LT], 1))
    for h in np.where(r > 0.55)[0]: a[max(0, h - 480):h + LT + 480] = 0  # artefact de fin d'appel TTS
    n = len(a) // W; env = np.sqrt(np.mean(a[:n * W].reshape(n, W) ** 2, 1))
    act = env > 120
    runs = []; i = 0
    while i < n:
        if act[i]:
            j = i
            while j < n and act[j]: j += 1
            runs.append([i, j]); i = j
        else: i += 1
    # fusionner les runs séparés de < 60 ms
    m = []
    for r in runs:
        if m and r[0] - m[-1][1] < 12: m[-1][1] = r[1]
        else: m.append(r)
    out = np.zeros_like(a); removed = []
    for k, (s, e) in enumerate(m):
        gap_b = s - (m[k - 1][1] if k else -999); gap_a = (m[k + 1][0] if k + 1 < len(m) else n + 999) - e
        if (e - s) * 5 < 130 and gap_b > 24 and gap_a > 24: removed.append(round(s * W / SR, 2)); continue
        s0, e0 = max(0, s * W - 240), min(len(a), e * W + 240)
        seg = a[s0:e0].copy(); fl = min(144, len(seg) // 2); r = np.linspace(0, 1, fl)
        seg[:fl] *= r; seg[-fl:] *= r[::-1]; out[s0:e0] = seg
    pk = np.abs(out).max()
    if pk > 29000: out *= 29000 / pk
    w = wave.open(f, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.astype(np.int16).tobytes()); w.close()
    print(f, 'pops supprimés', removed, 'pic', int(pk))
for f in sorted(glob.glob('audio/*/seg0*.wav')): proc(f)
