# v2 sound design: impactful + premium, from the creator's own library (assets/sfx/pack, reel-pack).
# Every cue sits on a graphic event from vid/events.json; each moment uses a different sound.
# python _tools/audio_build_v2.py <tag>
import json, subprocess, numpy as np, sys, os
SR = 48000; FPS = 24; DUR = 9.0; LIB = '../../assets/sfx/'; tag = sys.argv[1] if len(sys.argv) > 1 else 'v2'
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
# (sound, its peak time in the file, where the peak lands, peak dBFS, max length s, fade-out s)
P = 'pack/'; PM = P + 'pec-premium/am-sfx/'
hook, brands, click1, premium, nxt, connect, click2 = T('big', 0), T('big', 1), T('click', 1), T('big', 2), T('big', 3), T('big', 4), T('click', 4)
swap2, swap4 = T('group', 1), T('group', 3)
CUES = [
 # HOOK: suck-in whoosh into "A.R.S STUDIO" -> sub hall stinger + punch
 ('hook whoosh in',   PM + 'hard-whoosh.mp3', 0.20, hook, -11, 0.6, 0.05),
 ('hook sub stinger', P + 'evolve-audio-essential-transitions-free/evo-transitions-57-hit-stinger-hall.mp3', 0.06, hook, -5, 1.4, 0.5),
 ('hook punch',       P + 'hits/hit.mp3', 0.08, hook, -9, 0.9, 0.4),
 # page 2 swap
 ('swap whoosh 2',    PM + 'fast-whoosh.mp3', 0.30, swap2, -13, 0.9, 0.3),
 # "Brands" lands, then the cursor click
 ('Brands hit',       P + 'hits/05-impact.mp3', 0.33, brands, -10, 0.8, 0.35),
 ('click Brands',     PM + 'ui-click.mp3', 0.13, click1, -11, 0.5, 0.15),
 # page 3: whoosh flows into "Feels premium" -> textured cave hit
 ('whoosh into premium', PM + 'slowmo-whoosh.mp3', 0.41, premium, -12, 0.8, 0.2),
 ('premium cave hit', P + 'pec-premium/all-use/855710-855637-textured-cinematic-hit-cave-02-sfo-23-000521-mastered-2496.mp3', 0.17, premium, -7, 1.6, 0.6),
 # page 4 swap, "next level" heavy hit + sub drop
 ('swap whoosh 4',    PM + 'windy-woosh.mp3', 0.87, swap4, -14, 1.2, 0.3),
 ('next level hit',   P + 'hits/medium-cinematic-boom-04.mp3', 0.53, nxt, -8, 1.1, 0.5),
 ('next level sub',   P + 'cinematic-hub/cinematic-sub-drop/cinematic-sub-drop-03.mp3', 0.06, nxt, -9, 1.2, 0.5),
 # CTA: riser builds from "brand" into "connect", grand hit + weighty click
 ('CTA riser',        PM + 'riser-2.mp3', 1.49, connect, -15, 1.6, 0.03),
 ('connect grand hit', P + 'hits/03-grand-hit-a.mp3', 0.60, connect, -6, 1.2, 0.25),
 ('click connect',    PM + 'ui-click.mp3', 0.13, click2, -10, 0.5, 0.1),
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
m = m * env[:, None]; save('audio/bed_v2.wav', m)

mix = voice + sfx + m; save(f'audio/_premix_{tag}.wav', mix)
r = subprocess.run(['ffmpeg', '-i', f'audio/_premix_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(r[r.rfind('{'):r.rfind('}') + 1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'audio/_premix_{tag}.wav', '-af',
    f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000",
    '-c:a', 'pcm_s24le', f'audio/mix_{tag}.wav'], check=True)
for l in log: print(' ', *l)
print('voice', lufs('audio/voice.wav'), 'sfx', lufs(f'audio/sfx_{tag}.wav'), 'bed', lufs('audio/bed_v2.wav'), 'mix', lufs(f'audio/mix_{tag}.wav'))
