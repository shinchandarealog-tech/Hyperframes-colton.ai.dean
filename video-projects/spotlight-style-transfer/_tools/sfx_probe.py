# Measure candidate SFX: spectral centroid (warmth), peak time, length, energy above 6 kHz (hiss).
import subprocess, numpy as np, sys, glob
def load(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True)
    return np.frombuffer(r.stdout, np.float32)
for p in sys.argv[1:]:
    for f in sorted(glob.glob(p)):
        x = load(f)
        if len(x) < 100: continue
        S = np.abs(np.fft.rfft(x * np.hanning(len(x)))); fr = np.fft.rfftfreq(len(x), 1 / 48000)
        cen = (S * fr).sum() / S.sum(); hi = S[fr > 6000].sum() / S.sum()
        env = np.convolve(np.abs(x), np.ones(480) / 480, 'same'); pk = env.argmax() / 48000
        print(f'{f.split("assets/")[-1]:55s} len {len(x)/48000:5.2f}s  peak {pk:5.2f}s  centroid {cen:6.0f} Hz  >6k {hi*100:4.1f}%  peakdB {20*np.log10(np.abs(x).max()+1e-9):5.1f}')
