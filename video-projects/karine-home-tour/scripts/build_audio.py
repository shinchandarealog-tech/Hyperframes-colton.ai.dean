"""Assemble the reel's audio: voice stem cut to the segment plan (-14 LUFS),
continuous quiet music bed, sparse whooshes + soft ticks. Writes renders/mix.wav."""
import subprocess, numpy as np, pyloudnorm as pyln, soundfile as sf, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
SR, FPS, DUR = 48000, 24, 888 / 24

def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def fade(x, ms=10):
    k = int(SR * ms / 1000); r = np.linspace(0, 1, k)[:, None]
    x[:k] *= r; x[-k:] *= r[::-1]; return x

meter = pyln.Meter(SR)
def gain_to(x, lufs): return x * 10 ** ((lufs - meter.integrated_loudness(x)) / 20)

voc = load(R / "assets/stems/htdemucs/raw/vocals.wav")
mus = load(R / "assets/stems/htdemucs/raw/no_vocals.wav")
N = int(round(DUR * SR))
voice = np.zeros((N, 2), np.float32)
# (src_start_s, src_end_s, out_start_s)  -- from the segment plan
pieces = [(0, 173/FPS, 0), (14.0, 14.0 + 127/FPS, 173/FPS), (593/FPS, 840/FPS, 300/FPS),
          (1509/FPS, 1659/FPS, 547/FPS), (2172/FPS, 2269/FPS, 791/FPS)]
for a, b, o in pieces:
    seg = fade(voc[int(round(a*SR)):int(round(b*SR))].copy())
    i = int(round(o*SR)); voice[i:i+len(seg)] += seg[:N-i]
voice = gain_to(voice, -14.0)
bed = mus[:N].copy()
bed = gain_to(bed, -31.0)
env = np.ones((N, 1), np.float32); f_in, f_out = int(.25*SR), int(2.0*SR)
env[:f_in, 0] = np.linspace(0, 1, f_in); env[-f_out:, 0] = np.linspace(1, 0, f_out)
bed *= env
sfx = np.zeros((N, 2), np.float32)
woosh = load(R / "../../assets/sfx/transitions/whoosh.mp3"); woosh = woosh / np.abs(woosh).max()
tick = load(R / "../../assets/sfx/ui/click.wav"); tick = tick / np.abs(tick).max()
def place(snd, t, db):
    i = max(0, int(t*SR)); seg = snd[:N-i] * 10 ** (db/20); sfx[i:i+len(seg)] += seg
for t in [2.2917, 7.2083, 12.5, 17.5833, 25.0, 29.0417]:
    place(woosh, t - 0.18, -22)
for t in [1.0, 3.16, 4.50, 5.95, 8.35, 20.87, 23.10, 26.15, 26.55, 27.50, 29.40, 35.45]:
    place(tick, t, -30)
mix = voice + bed + sfx
tmp = R / "renders/mix_raw.wav"; sf.write(tmp, mix, SR, subtype="FLOAT")
# brick-wall peak limiter (touches only the loudest transients), ceiling -1.5 dBFS
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af",
                "alimiter=limit=0.84:attack=2:release=60:level=false", "-c:a", "pcm_s24le",
                str(R / "renders/mix.wav")], check=True)
out = load(R / "renders/mix.wav")
print("voice LUFS %.2f | bed %.2f | final mix %.2f LUFS | peak %.2f dBFS" % (
    meter.integrated_loudness(voice), meter.integrated_loudness(bed[f_in:-f_out]),
    meter.integrated_loudness(out), 20*np.log10(np.abs(out).max())))
