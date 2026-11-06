# Original soft, warm music bed: slow major-7th pad + gentle kalimba-like arpeggio.
# Deterministic (fixed seed). Writes 48 kHz stereo WAV.
import sys, wave
import numpy as np
SR = 48000
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 52.0
BPM = 76.0
beat = 60.0 / BPM
bar = 4 * beat
rng = np.random.default_rng(7)
t = np.arange(int(DUR * SR)) / SR
L = np.zeros_like(t); R = np.zeros_like(t)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
# F major, cozy: Fmaj9 - Am7 - Dm9 - Bbmaj7(add9)
chords = [[53, 60, 64, 67, 69], [57, 60, 64, 67, 71], [50, 57, 60, 64, 65], [46, 57, 62, 65, 69]]
bass   = [41, 45, 38, 46]

def env(n, a, r):
    e = np.ones(n)
    na, nr = min(int(a * SR), n // 2), min(int(r * SR), n // 2)
    e[:na] = np.linspace(0, 1, na) ** 2
    e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e

# Pad: each chord one bar, overlapping crossfades
k = 0; start = 0.0
while start < DUR:
    ch = chords[k % 4]; b = bass[k % 4]
    s = int(start * SR); n = int((bar + 1.6) * SR); n = min(n, len(t) - s)
    if n <= 0: break
    tt = np.arange(n) / SR
    e = env(n, 1.4, 1.6)
    for i, m in enumerate(ch):
        f = hz(m)
        for det, pan in ((-0.12, 0.35), (0.12, 0.65)):
            ph = rng.uniform(0, 2 * np.pi)
            w = np.sin(2 * np.pi * (f + det) * tt + ph) + 0.18 * np.sin(2 * np.pi * 2 * (f + det) * tt + ph)
            w *= 0.055 * e * (1 + 0.04 * np.sin(2 * np.pi * 0.21 * tt + i))
            L[s:s + n] += w * (1 - pan); R[s:s + n] += w * pan
    fb = hz(b)
    w = (np.sin(2 * np.pi * fb * tt) + 0.25 * np.sin(2 * np.pi * 2 * fb * tt)) * 0.09 * e
    L[s:s + n] += w * 0.5; R[s:s + n] += w * 0.5
    start += bar; k += 1

# Kalimba-ish arpeggio: soft plucks on eighth notes, sparse pattern
pattern = [0, 2, 3, 4, 3, 2, 1, 2]
step = beat / 2
k = 0; start = 0.0
while start < DUR:
    ch = chords[(k // 8) % 4]
    idx = pattern[k % 8]
    if (k % 8) not in (5,):                      # leave a little air
        m = ch[idx] + 12
        f = hz(m)
        s = int(start * SR); n = min(int(1.6 * SR), len(t) - s)
        if n > 0:
            tt = np.arange(n) / SR
            dec = np.exp(-tt * 3.2) * np.minimum(1, tt / 0.006)
            w = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2.01 * f * tt) * np.exp(-tt * 9)) * dec
            w *= 0.05 * (0.85 + 0.15 * rng.random())
            pan = 0.3 + 0.4 * ((k * 3) % 5) / 4
            L[s:s + n] += w * (1 - pan); R[s:s + n] += w * pan
    start += step; k += 1

# Simple stereo reverb: multi-tap feedback delays
def reverb(x, taps=((0.031, .5), (0.047, .42), (0.071, .35), (0.113, .28), (0.167, .2), (0.229, .14))):
    y = x.copy()
    for d, g in taps:
        n = int(d * SR); z = np.zeros_like(x); z[n:] = x[:-n] * g; y += z
    return y
L, R = reverb(L), reverb(R)
# Gentle low-pass (one-pole) for warmth
def lp(x, fc=3200):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y
L, R = lp(L), lp(R)
# Fades
fi, fo = int(1.5 * SR), int(3.0 * SR)
for ch in (L, R):
    ch[:fi] *= np.linspace(0, 1, fi); ch[-fo:] *= np.linspace(1, 0, fo) ** 1.5
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.8, R / peak * 0.8
st = np.stack([L, R], 1)
with wave.open(sys.argv[1], 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((st * 32767).astype('<i2').tobytes())
print('ok', DUR)
