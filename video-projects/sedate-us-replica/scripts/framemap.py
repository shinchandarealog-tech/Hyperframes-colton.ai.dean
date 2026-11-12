import cv2,numpy as np,sys,math,json
W=sys.argv[1]; f0,f1=int(sys.argv[2]),int(sys.argv[3]); zoom=sys.argv[4]=="zoom"
def circ(x): x=min(max(x,0),1); return math.sqrt(1-(x-1)**2)
rawc={}
def raw(k):
    if k not in rawc: rawc[k]=cv2.imread(f"{W}/work/raw/f{k+1:04d}.png",0)
    return rawc[k]
out={}
for f in range(f0,f1+1):
    s=1+0.15*(1-circ(f/31)) if zoom else 1.0
    M=np.float64([[1.8*s,0,0],[0,1.8*s,0]]); M[0,2]=540-s*(540+940); M[1,2]=960-s*(960+11)
    a=cv2.imread(f"{W}/work/ref/f{f+1:04d}.png",0).astype(np.float32)[:880]
    k0=int(f/30*24000/1001); res=[]
    for k in range(max(0,k0-2),k0+5):
        r=cv2.warpAffine(raw(k),M,(1080,1920),flags=cv2.INTER_LINEAR).astype(np.float32)[:880]
        res.append((float(np.abs(a-r).mean()),k))
    res.sort(); out[f]=res[0][1]; print(f,k0,res[0][1],"%.2f"%res[0][0],"2nd %d %.2f"%(res[1][1],res[1][0]))
json.dump(out,open(sys.argv[5],"w"))
