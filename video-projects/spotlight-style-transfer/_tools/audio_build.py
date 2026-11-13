# Sound design (EDITA skill ch.9): voice chain, thinned SFX on graphic events, music bed 25 LU under, master -14 LUFS / -1.5 dBTP.
# python _tools/audio_build.py [--no-music]
import json, subprocess, numpy as np, sys, os
SR = 48000; FPS = 24; DUR = 9.0; LIB = '../../assets/'
os.makedirs('audio', exist_ok=True)
def load(p, sr=SR):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
def save(p, x):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_s24le', p], input=x.astype(np.float32).tobytes(), check=True)
def lufs(p):
    r = subprocess.run(['ffmpeg', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(r.split('Summary:')[1].split('I:')[1].split('LUFS')[0])
db = lambda d: 10 ** (d / 20)

# ---- 1. voice chain
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'aroll/rough.mp4', '-vn', '-ac', '2', '-ar', str(SR), '-af',
    'highpass=f=70,afftdn=nf=-30,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=1,'
    'equalizer=f=3000:width_type=o:width=1:g=2.5,loudnorm=I=-15:TP=-2:LRA=7', '-c:a', 'pcm_s24le', 'audio/voice.wav'], check=True)
voice = load('audio/voice.wav'); n = int(DUR * SR); voice = np.pad(voice, ((0, max(0, n - len(voice))), (0, 0)))[:n]

# ---- 2. SFX on graphic events, thinned
S = {'pop': ('sfx/ui/pop.mp3', 0.20), 'click': ('sfx/kit/ui/click-07.wav', 0.01), 'whoosh': ('sfx/kit/transitions/low-whoosh.mp3', 0.82),
     'sub': ('sfx/kit/impact/deep-bass.mp3', 0.06)}
SND = {k: (load(LIB + p), pk) for k, (p, pk) in S.items()}
for k, (x, pk) in SND.items(): SND[k] = (x / (np.abs(x).max() + 1e-9), pk)   # peak-normalise, gains below are peak dBFS
ev = json.load(open('vid/events.json'))
PRI = {'click': 4, 'big': 3.5, 'card': 3, 'group': 2, 'script': 1}
MAP = {'click': ('click', -15), 'big': ('pop', -13), 'card': ('whoosh', -19), 'group': ('pop', -18)}  # script = emphasis only, no sound
cand = sorted([e for e in ev if e['type'] in MAP], key=lambda e: (-PRI[e['type']], e['t']))
acc = []
for e in cand:
    f = e['t'] * FPS; isw = e['type'] == 'card'
    ok = True
    for a in acc:
        gap = abs(f - a['t'] * FPS); aw = a['type'] == 'card'
        if (isw or aw) and gap < 12: ok = False      # >= 12 f from a whoosh
        if not isw and not aw and gap < 18: ok = False  # >= 18 f between pops/clicks
    if ok: acc.append(e)
acc.sort(key=lambda e: e['t'])
rng = np.random.default_rng(7); sfx = np.zeros_like(voice); log = []
def place(x, pk, t, g, semis=0.0):
    if semis:
        r = 2 ** (semis / 12); idx = np.arange(0, len(x) - 1, r)
        x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1); pk /= r
    s = int(round((t - pk) * SR)); a = max(0, s); b = min(n, s + len(x))
    if b > a: sfx[a:b] += x[a - s:b - s] * db(g)
for e in acc:
    k, g = MAP[e['type']]; x, pk = SND[k]
    st = float(rng.uniform(-0.7, 0.7)) if k == 'pop' else 0.0
    place(x, pk, e['t'], g, st); log.append((round(e['t'], 3), round(e['t'] * FPS, 1), e['type'], k, g, round(st, 2)))
    if e['b'] == 0 and e['type'] == 'big':  # hook: one warm sub under the opening hit
        place(*SND['sub'], e['t'], -17); log.append((round(e['t'], 3), round(e['t'] * FPS, 1), 'hook', 'sub', -17, 0))
sfx[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))[:, None]
save('audio/sfx.wav', sfx)

# ---- 3. music bed: 25 LU under the voice, from frame 0 (10 ms fade in), 1 s fade out
use_music = '--no-music' not in sys.argv
mix = voice + sfx
if use_music:
    m = load(LIB + 'music/music-bed-cinematic-tech.mp3')[:n]
    save('audio/_bed_raw.wav', m); g = (lufs('audio/voice.wav') - 25) - lufs('audio/_bed_raw.wav'); m = m * db(g)
    fi, fo = int(0.01 * SR), int(1.0 * SR); m[:fi] *= np.linspace(0, 1, fi)[:, None]; m[-fo:] *= np.linspace(1, 0, fo)[:, None]
    save('audio/bed.wav', m); mix = mix + m
save('audio/_premix.wav', mix)

# ---- 4. master -14 LUFS, -1.5 dBTP (two-pass loudnorm)
r = subprocess.run(['ffmpeg', '-i', 'audio/_premix.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(r[r.rfind('{'):r.rfind('}') + 1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'audio/_premix.wav', '-af',
    f"loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000",
    '-c:a', 'pcm_s24le', 'audio/mix.wav'], check=True)
print('SFX placed (t s, frame, event, sound, peak dBFS, pitch st):'); [print(' ', *l) for l in log]
print('dropped by thinning:', [(round(e['t'], 2), e['type']) for e in cand if e not in acc])
print('voice', lufs('audio/voice.wav'), 'sfx', lufs('audio/sfx.wav'), 'bed', lufs('audio/bed.wav') if use_music else '-', 'mix', lufs('audio/mix.wav'))
