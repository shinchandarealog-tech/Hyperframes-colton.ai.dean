# Probe SFX for premium sound design: length, peak time, centroid, % energy <150 Hz (weight), % >6 kHz (hiss), crest.
import subprocess, numpy as np, sys
def load(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True)
    return np.frombuffer(r.stdout, np.float32)
for f in sys.argv[1:]:
    x = load(f)
    if len(x) < 100: print('??', f); continue
    S = np.abs(np.fft.rfft(x)) ** 2; fr = np.fft.rfftfreq(len(x), 1 / 48000); T = S.sum()
    cen = (np.sqrt(S) * fr).sum() / np.sqrt(S).sum()
    env = np.convolve(np.abs(x), np.ones(480) / 480, 'same'); pk = env.argmax() / 48000
    rms = np.sqrt((x ** 2).mean()); crest = 20 * np.log10(np.abs(x).max() / (rms + 1e-9))
    print(f'{f.split("pack/")[-1].split("assets/")[-1][:70]:70s} {len(x)/48000:5.2f}s pk{pk:5.2f} cen{cen:6.0f} low{S[fr<150].sum()/T*100:5.1f}% hi{S[fr>6000].sum()/T*100:5.1f}% crest{crest:5.1f}')
