import subprocess, sys, json, numpy as np, cv2
SRC, OUT = sys.argv[1], sys.argv[2]
W, Y0, BH = 720, 128, 116
p = subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf",f"crop={W}:{BH}:0:{Y0}","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
n=W*BH*3; ms=[]; crops=[]
while True:
    b=p.stdout.read(n)
    if len(b)<n: break
    f=np.frombuffer(b,np.uint8).reshape(BH,W,3).astype(np.int16)
    m=(f.min(2)>222)&((f.max(2)-f.min(2))<30)
    ms.append(m); crops.append(f.astype(np.uint8))
segs=[]; cur=None
def iou(a,b):
    u=(a|b).sum(); return 1.0 if u==0 else (a&b).sum()/u
for i,m in enumerate(ms):
    has=m.sum()>150
    if cur is None:
        if has: cur=[i,i,m]
        continue
    if has and iou(cur[2],m)>0.5:
        cur[1]=i
    else:
        if cur[1]-cur[0]>=3: segs.append((cur[0],cur[1]))
        cur=[i,i,m] if has else None
if cur and cur[1]-cur[0]>=3: segs.append((cur[0],cur[1]))
json.dump([{"i":k,"start":round(a/30,3),"end":round((b+1)/30,3)} for k,(a,b) in enumerate(segs)],open(OUT+"/segs.json","w"),indent=0)
# tile crops: 2 cols, 16 rows per sheet
tiles=[]
for k,(a,b) in enumerate(segs):
    c=cv2.cvtColor(crops[(a+b)//2][10:100],cv2.COLOR_RGB2BGR).copy()
    cv2.rectangle(c,(0,0),(70,26),(0,0,0),-1); cv2.putText(c,str(k),(4,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
    tiles.append(c)
per=32
for s in range(0,len(tiles),per):
    t=tiles[s:s+per]
    while len(t)%2: t.append(np.zeros_like(tiles[0]))
    rows=[np.hstack(t[r:r+2]) for r in range(0,len(t),2)]
    cv2.imwrite(f"{OUT}/caps-{s//per:02d}.jpg",np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
print(len(segs))
