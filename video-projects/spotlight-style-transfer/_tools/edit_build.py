# Shorten every pause >0.16s to 0.10s (cut in its middle), lead-in to 0.10s. Cuts snap to 24fps frames.
import json, subprocess, re
FPS=24; SRC='src/aroll_raw.mp4'
log=subprocess.run(['ffmpeg','-i','aroll/voice16.wav','-af','silencedetect=noise=-30dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
DUR=10.0; snap=lambda t: round(t*FPS)/FPS
cuts=[]  # removed intervals (orig time)
for s,e in zip(st,en):
    d=e-s
    if s<0.01: cuts.append((0.0, snap(e-0.10))); continue
    if e>=DUR-0.2: continue
    if d>0.16:
        m=(s+e)/2; rem=d-0.10; a=snap(m-rem/2); b=snap(m+rem/2)
        if b>a: cuts.append((a,b))
keep=[]; t=0.0
for a,b in cuts:
    if a>t: keep.append((t,a))
    t=b
keep.append((t,DUR))
print('cuts',cuts); print('keep',keep)
# EDL: list of [orig_start, orig_end, edit_start]
edl=[]; acc=0.0
for a,b in keep: edl.append([round(a,4),round(b,4),round(acc,4)]); acc+=b-a
json.dump(dict(edl=edl,dur=round(acc,4)),open('aroll/edl.json','w'))
# build rough.mp4
fc=''; n=len(keep)
for i,(a,b) in enumerate(keep):
    fc+=f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.4f}:d=0.005[a{i}];'
fc+=''.join(f'[v{i}][a{i}]' for i in range(n))+f'concat=n={n}:v=1:a=1[v][a]'
subprocess.run(['ffmpeg','-v','error','-y','-i',SRC,'-filter_complex',fc,'-map','[v]','-map','[a]','-r','24','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','aroll/rough.mp4'],check=True)
def o2e(t):
    for a,b,e in edl:
        if t<a: return e
        if t<=b: return e+(t-a)
    return acc
W=json.load(open('aroll/words.json'))
W[0]['s']=max(W[0]['s'],0.48)  # whisper put "Hey" at 0.0; voice starts at 0.48 (silencedetect)
WE=[dict(w=w['w'],s=round(o2e(w['s']),3),e=round(o2e(w['e']),3)) for w in W]
json.dump(WE,open('aroll/words_edit.json','w'),indent=0)
print('edit dur',acc)
