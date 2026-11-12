# audio_build.py — skill chapter 9. Voice -15 LUFS | bed 25 LU under, from frame 0 | markers | thinned pops | risers on shot-type changes | master -14 LUFS / -1.5 dBTP
import json,glob,subprocess,numpy as np,soundfile as sf,random
SR=48000;FPS=24000/1001;A='../../assets/'
def load(p,rate=1.0):
    af=f'asetrate={int(SR*rate)},aresample={SR}' if rate!=1 else 'anull'
    a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-af',af,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32).reshape(-1,2).copy();return a
def lufs(x):
    sf.write('audio/_m.wav',x,SR);o=subprocess.run(['ffmpeg','-nostats','-i','audio/_m.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float([l for l in o.splitlines() if l.strip().startswith('I:')][-1].split()[1])
voice,_=sf.read('audio/voice_tpl.wav',dtype='float32')            # voice chain (hp 70, afftdn, comp 3:1 @-22, +2.5 dB @3k) + loudnorm -15
if voice.ndim==1: voice=np.stack([voice,voice],1)
# raw tail after the last kept frame (the picture runs on 13 frames): same chain + same linear gain as the voice
EDLJ=json.load(open('aroll/edl.json'));lo=EDLJ['EDL'][-1];o_end=(lo[1]+lo[2])/FPS;TAIL=13
subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{o_end:.4f}','-t',f'{TAIL/FPS:.4f}','-i','aroll/voice.wav','-af','highpass=f=70,afftdn=nr=10,acompressor=threshold=-22dB:ratio=3:attack=5:release=80,equalizer=f=3000:t=q:w=1:g=2.5','-ar',str(SR),'-ac','2','audio/_tail.wav'],check=True)
vc,_=sf.read('audio/voice_chain.wav',dtype='float32');vc=vc if vc.ndim==2 else np.stack([vc,vc],1)
g=np.sqrt((voice**2).mean()/((vc[:len(voice)]**2).mean()+1e-12))
tail,_=sf.read('audio/_tail.wav',dtype='float32');tail=tail*g;x=int(.005*SR)
ramp=np.sin(np.linspace(0,np.pi/2,x))[:,None];voice[-x:]*=ramp[::-1];tail[:x]*=ramp
voice=np.concatenate([voice,tail])
N=len(voice);out=voice.copy();VL=lufs(voice)
segs=[json.load(open(f)) for f in sorted(glob.glob('vid/S*/meta.json'))]
ev=sorted([e for s in segs for e in s['ev']])
def put(x,frame,gain_db,align=0.0):
    i=int(round(frame/FPS*SR-align*SR));g=10**(gain_db/20)
    a,b=max(0,i),min(N,i+len(x));
    if b>a: out[a:b]+=x[a-i:b-i]*g
log=[]
# --- music bed: 25 LU under the voice, from frame 0 (10 ms fade-in), 1 s fade-out at the end
bed=load(A+'music/chamber-music/es-a-delightful-evening-francis-wells.mp3')[:N]
bed=bed*10**(((VL-25)-lufs(bed))/20);fi=int(.01*SR);fo=SR
bed[:fi]*=np.linspace(0,1,fi)[:,None];bed[-fo:]*=np.linspace(1,0,fo)[:,None];out[:len(bed)]+=bed
# --- risers: only on the shot-type changes speaker -> b-roll (3-4), every other cut dry
riser=load(A+'sfx/kit/transitions/low-whoosh.mp3');pk=np.abs(riser).mean(1);peak=np.argmax(np.convolve(pk,np.ones(960)/960,'same'))/SR
risers=[s['E0'] for i,s in enumerate(segs) if s['type']=='broll' and i>0 and segs[i-1]['type']=='speaker']
for f in risers: put(riser,f,-17,align=peak);log.append((f,'riser'))
# --- markers: every bar / underline / stroke that grows
mk=load(A+'sfx/transitions/swipe.mp3');mpk=np.argmax(np.abs(mk).mean(1))/SR
markers=[]
for f in sorted(set(f for f,t in ev if t=='marker')):
    if markers and f-markers[-1]<18: continue          # no fast series of the same sound
    if any(abs(f-r)<12 for r in risers): continue
    markers.append(f)
for f in markers: put(mk,f+2,-21,align=mpk);log.append((f+2,'marker'))
# --- pops: priority graphic > new group > word; >=18 f apart; >=12 f from riser/marker; none -25..+30 f around a marker
pri={'pill':0,'chip':0,'tag':0,'group':1}
cand=sorted([(f+(2 if t=='pill' else 3),pri[t],t) for f,t in ev if t in pri],key=lambda x:(x[1],x[0]))
pops=[]
for f,p,t in cand:
    if any(abs(f-q)<18 for q in pops): continue
    if any(abs(f-r)<12 for r in risers): continue
    if any(-25<=f-m<=30 for m in markers): continue
    pops.append(f)
random.seed(3)
for f in sorted(pops):
    pp=load(A+'sfx/kit/ui/pop-low.mp3',rate=2**(random.uniform(-0.7,0.7)/12));put(pp,f,-13);log.append((f,'pop'))
# --- master -14 LUFS, -1.5 dBTP
sf.write('audio/premaster.wav',out,SR)
L=json.loads((lambda t:t[t.rindex('{'):])(subprocess.run(['ffmpeg','-nostats','-i','audio/premaster.wav','-af','loudnorm=I=-14:TP=-1.5:print_format=json','-f','null','-'],capture_output=True,text=True).stderr))
subprocess.run(['ffmpeg','-y','-v','error','-i','audio/premaster.wav','-af',f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}:measured_thresh={L['input_thresh']}:linear=true",'-ar',str(SR),'audio/mix.wav'],check=True)
json.dump(sorted(log),open('an/sfx_log.json','w'))
print('voice',VL,'LUFS | SFX',len(log),':',sum(1 for l in log if l[1]=='pop'),'pops',len(markers),'markers',len(risers),'risers')
print(sorted(log))
