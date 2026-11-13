# Audio QC image: momentary (400 ms) K-weighted-ish loudness of voice / sfx / bed + mix spectrogram, cue markers.
import subprocess, numpy as np, json, cv2, sys
SR = 48000; tag = sys.argv[1]
def load(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-af', 'highpass=f=100:poles=2,treble=g=4:f=1500', '-f', 'f32le', '-'], capture_output=True)
    return np.frombuffer(r.stdout, np.float32)
def mom(x):
    w = int(0.4 * SR); h = int(0.05 * SR); out = []
    for i in range(0, len(x) - w, h): out.append(10 * np.log10((x[i:i + w] ** 2).mean() + 1e-12) - 0.691)
    return np.array(out)
V, S, B = mom(load('audio/voice.wav')), mom(load(f'audio/sfx_{tag}.wav')), mom(load(f'audio/bed_{tag}.wav'))
W, H = 1800, 700; im = np.full((H, W, 3), 18, np.uint8); n = min(len(V), len(S), len(B))
X = lambda i: int(60 + i / n * (W - 80)); Y = lambda d: int(40 + (-10 - d) / 60 * 360)
for d in range(-10, -71, -10): cv2.line(im, (60, Y(d)), (W - 20, Y(d)), (50, 50, 50), 1); cv2.putText(im, str(d), (10, Y(d) + 5), 0, .45, (150, 150, 150), 1)
for arr, col in ((B, (200, 120, 60)), (S, (60, 200, 255)), (V, (120, 255, 120))):
    for i in range(1, n): cv2.line(im, (X(i - 1), Y(arr[i - 1])), (X(i), Y(arr[i])), col, 2)
# voice minus sfx margin while voice is active
act = V[:n] > -40; marg = (V[:n] - S[:n])[act]
cv2.putText(im, f'voice(green) sfx(yellow) bed(blue)  | voice-sfx margin when talking: min {marg.min():.1f} dB, 10th pct {np.percentile(marg,10):.1f} dB', (60, 25), 0, .55, (230, 230, 230), 1)
# spectrogram of the mix
x = load(f'audio/mix_{tag}.wav'); nf = 2048; hop = 512
fr = np.array([np.abs(np.fft.rfft(x[i:i + nf] * np.hanning(nf))) for i in range(0, len(x) - nf, hop)]).T
fr = 20 * np.log10(fr + 1e-6); fr = fr[:int(nf / 2 * 8000 / 24000)]  # 0-8 kHz
img = np.clip((fr - fr.max() + 80) / 80 * 255, 0, 255).astype(np.uint8)[::-1]
img = cv2.applyColorMap(cv2.resize(img, (W - 80, 260)), cv2.COLORMAP_MAGMA); im[430:690, 60:W - 20] = img
for c in json.load(open('vid/events.json')):
    xx = int(60 + c['t'] / 9.0 * (W - 80)); cv2.line(im, (xx, 410), (xx, 425), (255, 255, 255), 2)
for s in range(10): xx = int(60 + s / 9.0 * (W - 80)); cv2.putText(im, f'{s}s', (xx - 8, 425), 0, .4, (180, 180, 180), 1)
cv2.imwrite(f'an/audio_qc_{tag}.png', im); print('margin min', marg.min(), 'p10', np.percentile(marg, 10))
