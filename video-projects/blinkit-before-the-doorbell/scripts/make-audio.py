"""Original music bed + custom SFX for "Before the Doorbell" (no licensing issues).

Music: 120 BPM light Indian-pop groove in D (dholak-style dha/na drums, shaker,
plucked-string melody, offbeat chord stabs). Hits land on the storyboard beats:
10.0s doorbell, 13.0s slogan drop, 14.5s logo resolve. Deterministic (seeded).

Run from the project folder:  python3 scripts/make-audio.py
"""
import wave
import numpy as np

SR = 44100
DUR = 18.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
OUT = "assets/audio/"


def t_arr(sec):
    return np.arange(int(SR * sec)) / SR


def place(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def env(sec, attack=0.003, decay=0.3):
    t = t_arr(sec)
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / decay)


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for k in range(len(x)):
        acc = (1 - a) * x[k] + a * acc
        y[k] = acc
    return y


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def note(name):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    pitch, octave = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[pitch] + (octave - 4) * 12) / 12)


# ---------- instruments ----------
def dha(gain=1.0):  # low dholak / kick
    t = t_arr(0.35)
    f = 55 + 70 * np.exp(-t / 0.04)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(0.35, 0.002, 0.12) * gain


def na(gain=1.0):  # high dholak slap
    t = t_arr(0.18)
    tone = np.sin(2 * np.pi * 420 * t) * env(0.18, 0.001, 0.05)
    noise = highpass(rng.standard_normal(len(t)), 1800) * env(0.18, 0.001, 0.03)
    return (0.6 * tone + 0.5 * noise) * gain


def clap(gain=1.0):
    t = t_arr(0.2)
    n = highpass(rng.standard_normal(len(t)), 1200)
    e = env(0.2, 0.001, 0.06)
    for off in (0.0, 0.012, 0.024):
        e = e + np.where(t > off, np.exp(-(t - off) / 0.01), 0) * 0.5
    return n * e * 0.35 * gain


def shaker(gain=1.0):
    t = t_arr(0.08)
    return highpass(rng.standard_normal(len(t)), 5000) * env(0.08, 0.004, 0.02) * 0.18 * gain


def bass(freq, sec=0.45, gain=1.0):
    t = t_arr(sec)
    s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * 2 * freq * t)
    return s * env(sec, 0.004, 0.25) * 0.55 * gain


def pluck(freq, sec=0.9, gain=1.0, bright=0.996):  # Karplus-Strong, sitar-ish
    n = int(SR * sec)
    period = int(SR / freq)
    buf = rng.uniform(-1, 1, period)
    out = np.empty(n)
    for k in range(n):
        out[k] = buf[k % period]
        nxt = buf[(k + 1) % period]
        buf[k % period] = bright * 0.5 * (buf[k % period] + nxt)
    buzz = np.tanh(out * 2.2) * 0.4  # a little "jawari" buzz
    return (out * 0.7 + buzz) * gain * 0.5


def stab(freqs, sec=0.22, gain=1.0):
    t = t_arr(sec)
    s = sum(np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) + 0.1 * np.sin(2 * np.pi * 3 * f * t) for f in freqs)
    return s / len(freqs) * env(sec, 0.004, 0.09) * 0.32 * gain


def pad(freqs, sec, gain=1.0, attack=0.4, decay=3.0):
    t = t_arr(sec)
    s = sum(np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * f * 1.003 * t) for f in freqs) / len(freqs)
    a = np.clip(t / attack, 0, 1)
    return s * a * np.exp(-t / decay) * 0.3 * gain


def crash(sec=1.6, gain=1.0):
    t = t_arr(sec)
    return highpass(rng.standard_normal(len(t)), 3500) * env(sec, 0.002, 0.45) * 0.25 * gain


def riser(sec, gain=1.0):
    t = t_arr(sec)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(n)
    seg = int(0.05 * SR)
    for s0 in range(0, len(n), seg):  # cutoff sweeps up
        cut = 500 + 7000 * (s0 / len(n)) ** 2
        out[s0:s0 + seg] = highpass(n[s0:s0 + seg], cut)
    return out * (t / sec) ** 2 * 0.22 * gain


def boom(gain=1.0):
    t = t_arr(1.2)
    f = 40 + 60 * np.exp(-t / 0.08)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(1.2, 0.002, 0.45) * gain


# ---------- arrangement ----------
music = np.zeros(N)
CHORDS = [  # (start, end, bass root, triad)
    (0.0, 2.0, "D2", ["D4", "F#4", "A4"]),
    (2.0, 4.0, "A1", ["C#4", "E4", "A4"]),
    (4.0, 6.0, "B1", ["D4", "F#4", "B4"]),
    (6.0, 8.0, "G1", ["D4", "G4", "B4"]),
    (8.0, 10.0, "A1", ["C#4", "E4", "A4"]),
    (10.0, 12.5, "D2", ["D4", "F#4", "A4"]),
    (12.5, 14.0, "G1", ["D4", "G4", "B4"]),
    (14.0, 15.5, "D2", ["D4", "F#4", "A4"]),
]


def chord_at(t):
    for s, e, r, tri in CHORDS:
        if s <= t < e:
            return r, tri
    return "D2", ["D4", "F#4", "A4"]


# intro 0-1.5: tense low drone (fridge moment)
place(music, pad([note("D3"), note("A3")], 1.6, 0.6, attack=0.3, decay=2.0), 0.0)

for b in range(int(DUR / 0.5)):
    t = b * 0.5
    if t < 1.5 or t >= 15.5:
        continue
    beat_in_bar = b % 4
    build = 8.0 <= t < 10.0
    full = t >= 10.0
    root, tri = chord_at(t)
    # drums
    if beat_in_bar in (0, 2):
        place(music, dha(1.0 if full else 0.85), t)
    if beat_in_bar in (1, 3):
        place(music, na(0.9), t)
        if full or t >= 3.0:
            place(music, clap(1.0), t)
    place(music, dha(0.45), t + 0.375) if beat_in_bar == 1 else None
    place(music, na(0.5), t + 0.25) if beat_in_bar == 3 else None
    for s16 in range(4):
        place(music, shaker(1.0 if s16 % 2 else 0.6), t + s16 * 0.125)
    # bass on 1 and the "and" of 2
    if beat_in_bar == 0:
        place(music, bass(note(root)), t)
    if beat_in_bar == 1:
        place(music, bass(note(root), 0.3, 0.7), t + 0.25)
    # offbeat chord stabs once the app opens
    if t >= 3.0:
        place(music, stab([note(n) for n in tri], gain=1.1 if full else 0.85), t + 0.25)

# plucked melody (D major pentatonic) from 3.0
MEL = ["A4", "B4", "D5", "B4", "A4", "F#4", "E4", "F#4"]
MEL_HI = ["D5", "E5", "F#5", "E5", "D5", "B4", "A4", "B4"]
for k in range(int((15.5 - 3.0) / 0.25)):
    t = 3.0 + k * 0.25
    if 9.75 <= t < 10.0:
        continue
    seq = MEL_HI if t >= 10.0 else MEL
    if k % 2 == 0 or t >= 10.0:
        if t >= 8.0 and t < 10.0 and k % 4:
            continue
        place(music, pluck(note(seq[k % 8]), 0.6), t, 0.55)

# build into the doorbell
place(music, riser(2.0), 8.0, 1.0)
for k in range(16):
    place(music, na(0.25 + 0.04 * k), 8.0 + k * 0.125)
music[int(9.875 * SR): int(10.0 * SR)] *= 0.15  # tiny breath before the hit
place(music, crash(1.6, 1.0), 10.0)

# mini build into the slogan drop
place(music, riser(1.0, 0.8), 13.0)
music[int(13.92 * SR): int(14.0 * SR)] *= 0.2
place(music, boom(0.9), 14.0)
place(music, crash(1.4, 1.1), 14.0)

# resolve on the logo: long D major pad + one last motif
place(music, pad([note("D3"), note("F#4"), note("A4"), note("D5")], 2.6, 1.1, attack=0.05, decay=1.6), 15.5)
place(music, crash(2.0, 0.6), 15.5)
for k, n in enumerate(["A4", "D5", "F#5", "A5"]):
    place(music, pluck(note(n), 1.6, bright=0.998), 15.5 + k * 0.125, 0.45)

# fade the tail into the end of the video
fade = np.ones(N)
fs = int(17.2 * SR)
fade[fs:] = np.linspace(1, 0, N - fs)
music *= fade


def save(name, x, peak=0.89):
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(OUT + name, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


save("music.wav", music)  # 18s: doorbell hit 10.0, slogan drop 14.0, logo resolve 15.5

# ---------- custom SFX ----------
# fridge hum (1.6s)
t = t_arr(1.6)
hum = 0.6 * np.sin(2 * np.pi * 60 * t) + 0.35 * np.sin(2 * np.pi * 120 * t) + 0.15 * lowpass(rng.standard_normal(len(t)), 400)
hum *= np.clip(t / 0.15, 0, 1) * np.clip((1.6 - t) / 0.3, 0, 1)
save("fridge-hum.wav", hum, 0.7)

# clock tick
t = t_arr(0.06)
tick = np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.006) + 0.5 * highpass(rng.standard_normal(len(t)), 3000) * np.exp(-t / 0.003)
save("tick.wav", tick, 0.8)


def bell(freq, sec):
    t = t_arr(sec)
    partials = [(1.0, 1.0, 1.4), (2.0, 0.35, 0.8), (2.76, 0.25, 0.5), (5.4, 0.1, 0.25)]
    return sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t / d) for m, a, d in partials) * np.clip(t / 0.003, 0, 1)


# doorbell ding-dong
db = np.zeros(int(SR * 2.0))
place(db, bell(659.25, 2.0), 0.0)
place(db, bell(523.25, 1.55), 0.45)
save("doorbell.wav", db, 0.85)

# cha-ching (register)
cc = np.zeros(int(SR * 1.2))
for off in (0.0, 0.07):
    tt = t_arr(0.08)
    place(cc, highpass(rng.standard_normal(len(tt)), 2500) * np.exp(-tt / 0.015), off, 0.7)
tt = t_arr(1.0)
ching = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((2093, 1.0), (2637, 0.6), (3136, 0.5), (4186, 0.3))) * np.exp(-tt / 0.35)
place(cc, ching, 0.14, 0.6)
save("cha-ching.wav", cc, 0.8)
print("wrote music.wav, fridge-hum.wav, tick.wav, doorbell.wav, cha-ching.wav")
