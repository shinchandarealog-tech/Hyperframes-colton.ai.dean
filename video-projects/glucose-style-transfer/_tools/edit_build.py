import json,numpy as np,soundfile as sf,subprocess,re
FPS=24000/1001;FD=1/FPS
W=json.load(open('aroll/words_raw.json'))
a,sr=sf.read('aroll/voice.wav');N=len(a);mono=a.mean(1)
DUR=N/sr
REMOVE=[(1,2),(27,29),(88,89)]          # word index ranges (1-based, inclusive) removed as fillers
def rms_at(t,w=0.01):
    i=int(t*sr);h=int(w*sr/2);s=mono[max(0,i-h):i+h];return np.sqrt((s**2).mean()+1e-12)
def snap(t):  # quietest frame boundary within +-70ms
    c=[k*FD for k in range(int((t-0.07)/FD),int((t+0.07)/FD)+2) if abs(k*FD-t)<=0.07 and 0<=k*FD<=DUR]
    return min(c,key=rms_at) if c else round(t/FD)*FD
# removal intervals in original time
rem=[]
for i,j in REMOVE:
    s=W[i-1]['s'] if i>1 else 0.0
    e=W[j]['s']   # start of next kept word
    if i>1: s=(W[i-2]['e']+W[i-1]['s'])/2
    e=(W[j-1]['e']+W[j]['s'])/2
    rem.append((0.0 if i==1 else s,e))
# silences
out=subprocess.run(['ffmpeg','-nostats','-i','aroll/voice.wav','-af','silencedetect=noise=-30dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
ss=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',out)];se=[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',out)]
for s,e in zip(ss,se):
    if e-s>0.16:
        m=(s+e)/2;half=(e-s-0.10)/2;rem.append((m-half,m+half))
# trailing tail after last word
rem.append((W[-1]['e']+0.12,DUR))
rem=sorted(rem);merged=[]
for s,e in rem:
    if merged and s<=merged[-1][1]: merged[-1]=(merged[-1][0],max(merged[-1][1],e))
    else: merged.append((s,e))
keep=[];t=0.0
for s,e in merged:
    if s>t: keep.append((t,s))
    t=max(t,e)
if t<DUR: keep.append((t,DUR))
# snap to frames
keepf=[]
for s,e in keep:
    fs=round(snap(s)/FD) if s>0 else 0; fe=round(snap(e)/FD)
    if fe-fs>=2: keepf.append((fs,fe))
# audio assemble with 5ms equal-power crossfade
xf=int(0.005*sr);parts=[]
for fs,fe in keepf:
    seg=a[int(fs*FD*sr):int(fe*FD*sr)].copy()
    ramp=np.sin(np.linspace(0,np.pi/2,xf))[:,None]
    seg[:xf]*=ramp;seg[-xf:]*=ramp[::-1];parts.append(seg)
outa=np.concatenate(parts);sf.write('aroll/voice_edit.wav',outa,sr)
# EDL in frames: edit frame k -> original frame
EDL=[];k=0
for fs,fe in keepf: EDL.append([k,fs,fe-fs]);k+=fe-fs
EDIT_F=k
def o2e(t):
    f=t/FD
    for e0,o0,n in EDL:
        if o0<=f<o0+n: return (e0+f-o0)*FD
    return None
words=[]
for i,w in enumerate(W,1):
    if any(a_<=i<=b_ for a_,b_ in REMOVE): continue
    s=o2e(w['s']);e=o2e(min(w['e'],DUR-0.01))
    if s is None:  # starts inside a removed sliver: move to next kept frame
        nxt=[e0 for e0,o0,n in EDL if o0*FD>w['s']];s=nxt[0]*FD if nxt else None
    if e is None: e=s+0.1
    words.append(dict(w=w['w'],s=round(s,3),e=round(max(e,s+0.05),3),o=w['s']))
json.dump(dict(EDL=EDL,EDIT_F=EDIT_F,FPS=FPS),open('aroll/edl.json','w'))
open('web/edl.js','w').write(f"window.FPS={FPS};window.EDL={json.dumps(EDL)};window.EDIT_F={EDIT_F};window.EDIT_DUR={EDIT_F*FD:.4f};\n")
open('web/words.js','w').write('window.WORDS='+json.dumps(words)+';\n')
print('kept',len(keepf),'pieces; edit',EDIT_F,'frames =',round(EDIT_F*FD,2),'s (raw',round(DUR,2),')')
print(' '.join(f"{i}:{w['w']}" for i,w in enumerate(words,1)))
