# v3 sound design: SFX only from the creator's Drive pack (assets/sfx/drive-ui-pack); voice, bed, ducking, master as v2.
# Every cue sits on a graphic event from vid/events.json; each moment uses a different sound.
# python _tools/audio_build_v3.py <tag>
import json, subprocess, numpy as np, sys, os
SR = 48000; FPS = 24; DUR = 9.0; LIB = '../../assets/sfx/'; tag = sys.argv[1] if len(sys.argv) > 1 else 'v3'
os.makedirs('audio', exist_ok=True); n = int(DUR * SR)
def load(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy(); return x / (np.abs(x).max() + 1e-9)
def save(p, x):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_s24le', p], input=x.astype(np.float32).tobytes(), check=True)
def lufs(p):
    r = subprocess.run(['ffmpeg', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(r.split('Summary:')[1].split('I:')[1].split('LUFS')[0])
db = lambda d: 10 ** (d / 20)

ev = json.load(open('vid/events.json'))
def T(typ, b): return next(e['t'] for e in ev if e['type'] == typ and e['b'] == b)
# (sound, the point in the file that lands on the event, event time, peak dBFS, max length s, fade-out s)
# v3: every SFX comes from the creator's Drive pack (assets/sfx/drive-ui-pack). Skipped as too hissy: digital, text [layer1].
P = 'drive-ui-pack/'
E = lambda typ, b: T(typ, b); connect = T('big', 4)
CUES = [
 # page 1: card opens, script writes on, "A.R.S STUDIO" lands
 ('card open',          P + 'interface open [small].mp3', 0.22, E('card', 0), -16, 0.6, 0.15),
 ('script write 1',     P + 'text [layer2, long].mp3',    0.16, E('script', 0), -17, 0.5, 0.2),
 ('hook whoosh in',     P + 'whoosh 3.mp3',               0.22, E('big', 0), -6, 0.42, 0.1),
 ('hook text hit',      P + 'text [layer4, short].mp3',   0.11, E('big', 0), -5, 0.9, 0.3),
 ('hook granular tail', P + 'granular 3.mp3',             0.11, E('big', 0), -11, 1.0, 0.5),
 # page 2: swap, script, "Brands" + click
 ('swap whoosh 2',      P + 'whoosh 2.mp3',               0.47, E('group', 1), -11, 0.63, 0.15),
 ('script write 2',     P + 'text [layer3, long].mp3',    0.14, E('script', 1), -17, 0.85, 0.3),
 ('Brands whoosh',      P + 'whoosh 5.mp3',               0.51, E('big', 1), -11, 0.66, 0.1),
 ('Brands count hit',   P + 'count [all layers].mp3',     0.16, E('big', 1), -8, 0.68, 0.2),
 ('click Brands',       P + 'click 3 [all layers].mp3',   0.19, E('click', 1), -9, 0.38, 0.1),
 # page 3: granular whoosh flows into "Feels premium", card settles with paper
 ('premium whoosh in',  P + 'granular whoosh.mp3',        1.02, E('big', 2), -9, 1.47, 0.3),
 ('premium granular',   P + 'granular 2.mp3',             0.32, E('big', 2), -11, 1.4, 0.5),
 ('premium card',       P + 'paper.mp3',                  0.08, E('card', 2), -18, 0.9, 0.3),
 # page 4: swap, script, "next level"
 ('swap whoosh 4',      P + 'whoosh 6.mp3',               1.05, E('group', 3), -11, 1.73, 0.3),
 ('script write 4',     P + 'text [all layers].mp3',      0.71, E('script', 3), -16, 1.25, 0.25),
 ('next level whoosh',  P + 'whoosh 1.mp3',               0.54, E('big', 3), -10, 0.78, 0.1),
 ('next level data',    P + 'data [long].mp3',            0.08, E('big', 3), -14, 1.2, 0.4),
 ('next level granular', P + 'granular 1.mp3',            0.23, E('big', 3), -9, 1.2, 0.4),
 # CTA: reverb rise swells into "connect", heavy count hit + weighty click
 ('CTA rise',           P + 'rise [reverb].mp3',          0.59, E('big', 4), -14, 1.4, 0.4),
 ('connect hit',        P + 'count [layer 2].mp3',        0.13, E('big', 4), -8, 0.74, 0.2),
 ('connect whoosh',     P + 'whoosh 4.mp3',               0.96, E('big', 4), -12, 1.4, 0.4),
 ('click connect',      P + 'click 4.mp3',                0.28, E('click', 4), -9, 0.44, 0.1),
]
sfx = np.zeros((n, 2), np.float32); log = []
for name, f, pk, t, g, ln, fo in CUES:
    x = load(LIB + f); s0 = max(0, int((pk - 0) * SR) - int(pk * SR))
    a_src = 0; start = int(round((t - pk) * SR))
    if start < 0: a_src = -start; start = 0
    x = x[a_src:a_src + int(ln * SR)].copy(); k = int(fo * SR)
    if k and len(x) > k: x[-k:] *= np.linspace(1, 0, k)[:, None] ** 2
    b = min(n, start + len(x)); sfx[start:b] += x[:b - start] * db(g)
    log.append((name, round(t, 3), round(t * FPS, 1), f.split('/')[-1][:44], g))
k = int(0.25 * SR); sfx[-k:] *= np.linspace(1, 0, k)[:, None]

# voice (same chain as v1)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'aroll/rough.mp4', '-vn', '-ac', '2', '-ar', str(SR), '-af',
    'highpass=f=70,afftdn=nf=-30,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=1,'
    'equalizer=f=3000:width_type=o:width=1:g=2.5,loudnorm=I=-15:TP=-2:LRA=7', '-c:a', 'pcm_s24le', 'audio/voice.wav'], check=True)
r = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'audio/voice.wav', '-f', 'f32le', '-'], capture_output=True, check=True)
voice = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy(); voice = np.pad(voice, ((0, max(0, n - len(voice))), (0, 0)))[:n]

# voice-keyed ducking of the SFX bus: hits play full within +-0.2 s of their landing; tails duck 7 dB under speech
DUCK = -7.0; w = int(0.03 * SR)
venv = np.sqrt(np.convolve(voice.mean(1) ** 2, np.ones(w) / w, 'same'))
talk = (20 * np.log10(venv + 1e-9) > -38).astype(np.float32)
hitwin = np.zeros(n, np.float32)
for _, _, _, t, *_ in CUES:
    a, b = max(0, int((t - 0.2) * SR)), min(n, int((t + 0.2) * SR)); hitwin[a:b] = 1
g = np.where(hitwin > 0, 1.0, np.where(talk > 0, db(DUCK), 1.0)).astype(np.float32)
sm = int(0.06 * SR); g = np.convolve(g, np.ones(sm) / sm, 'same')   # 60 ms smoothing, no pumping clicks
sfx *= g[:, None]
save(f'audio/sfx_{tag}.wav', sfx)

# music bed: 21 LU under the voice; drops out 0.15 s before the CTA hit, back under the hit's tail
m = load('../../assets/music/music-bed-cinematic-tech.mp3')[:n]
save('audio/_bed_raw.wav', m); m = m * db((lufs('audio/voice.wav') - 21) - lufs('audio/_bed_raw.wav'))
env = np.ones(n, np.float32); a = int((connect - 0.15) * SR); b = int((connect + 0.02) * SR)
env[a:b] = np.linspace(1, 0, b - a) ** 2; env[b:] = 0
c = int((connect + 0.25) * SR); env[c:] = np.minimum(1, np.linspace(0, 0.7, n - c))
fi = int(0.01 * SR); env[:fi] *= np.linspace(0, 1, fi); fo = int(0.6 * SR); env[-fo:] *= np.linspace(1, 0, fo)
m = m * env[:, None]; save(f'audio/bed_{tag}.wav', m)

mix = voice + sfx + m; save(f'audio/_premix_{tag}.wav', mix)
r = subprocess.run(['ffmpeg', '-i', f'audio/_premix_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(r[r.rfind('{'):r.rfind('}') + 1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'audio/_premix_{tag}.wav', '-af',
    f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000",
    '-c:a', 'pcm_s24le', f'audio/mix_{tag}.wav'], check=True)
for l in log: print(' ', *l)
print('voice', lufs('audio/voice.wav'), 'sfx', lufs(f'audio/sfx_{tag}.wav'), 'bed', lufs(f'audio/bed_{tag}.wav'), 'mix', lufs(f'audio/mix_{tag}.wav'))
