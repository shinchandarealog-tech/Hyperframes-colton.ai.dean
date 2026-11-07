"""Original devotional music bed for the Janhit ad: tanpura-style drone + soft tabla pulse (keherwa) + gentle pluck melody.
Deterministic (seeded). Writes assets/music-bed.wav. Usage: python3 -I edit-data/music_bed.py [seconds]"""
import sys, wave, numpy as np
SR=44100; DUR=float(sys.argv[1]) if len(sys.argv)>1 else 42.6
n=int(SR*DUR); t=np.arange(n)/SR; rng=np.random.default_rng(7)
out=np.zeros((n,2))
SA=138.59  # C#3
def env(L,a,d):
    x=np.arange(L)/SR; return np.minimum(1,x/a)*np.exp(-x/d)
def add(sig,start,pan=0.5,g=1.0):
    i=int(start*SR); j=min(n,i+len(sig)); s=sig[:j-i]*g
    out[i:j,0]+=s*(1-pan)*1.4; out[i:j,1]+=s*pan*1.4
# tanpura: plucked rich tones Pa, Sa', Sa', Sa cycling every 2.4s, long decay with jawari-like buzz
def tanpura(f,L=4.5):
    x=np.arange(int(L*SR))/SR; s=np.zeros_like(x)
    for h in range(1,14):
        s+= (0.9**h)*np.sin(2*np.pi*f*h*x*(1+0.0008*h)+rng.uniform(0,6.28))*(1+0.3*np.sin(2*np.pi*0.7*h*x))
    return s*env(len(x),0.02,1.8)*0.05
cyc=[SA*1.5/2, SA, SA, SA/2]
k=0; tt=0.0
while tt<DUR:
    add(tanpura(cyc[k%4]),tt,pan=0.35+0.3*(k%2)); tt+=0.6; k+=1
# tabla: keherwa  dha ge na ti | na ka dhi na  at 96 bpm eighths
bpm=96; e=60/bpm/2
def dha(): L=int(0.5*SR); x=np.arange(L)/SR; f=95*np.exp(-x*6)+70; ph=2*np.pi*np.cumsum(f)/SR; return (np.sin(ph)*env(L,0.002,0.18)*0.5+na()[:L]*0.5)
def ge(): L=int(0.4*SR); x=np.arange(L)/SR; f=85*np.exp(-x*8)+65; ph=2*np.pi*np.cumsum(f)/SR; return np.sin(ph)*env(L,0.002,0.15)*0.55
def na(): L=int(0.5*SR); x=np.arange(L)/SR; return (np.sin(2*np.pi*520*x)+0.5*np.sin(2*np.pi*1040*x+1))*env(L,0.001,0.12)*0.22+rng.normal(0,1,L)*env(L,0.0005,0.01)*0.08
def ti(): L=int(0.2*SR); return rng.normal(0,1,L)*env(L,0.0005,0.02)*0.1
pat=[dha,ge,na,ti,na,ti,dha,na]
start=1.2; i=0; tt=start
while tt<DUR-0.5:
    s=pat[i%8](); g=0.9 if i%8 in (0,6) else 0.7
    if tt<6.5: g*=0.45   # quieter in the sad opening
    add(s,tt,pan=0.45,g=g); tt+=e; i+=1
# pluck melody (santoor-ish), enters at the turn (9.4s): bhupali notes
scale=[1,9/8,5/4,3/2,5/3,2]
def pluck(f):
    L=int(1.2*SR); x=np.arange(L)/SR; s=sum((0.6**h)*np.sin(2*np.pi*f*h*x) for h in range(1,6)); return s*env(L,0.003,0.35)*0.08
mel=[0,2,3,4,3,2,1,0, 2,3,4,5,4,3,2,3]
tt=9.4; i=0
while tt<DUR-1.5:
    add(pluck(SA*2*scale[mel[i%16]]),tt,pan=0.6); tt+=e*2; i+=1
# fades
fi=np.minimum(1,t/1.5); fo=np.minimum(1,(DUR-t)/2.0)
out*= (fi*fo)[:,None]
out/=np.abs(out).max()*1.05
w=wave.open('assets/music-bed.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close(); print('ok',DUR)
