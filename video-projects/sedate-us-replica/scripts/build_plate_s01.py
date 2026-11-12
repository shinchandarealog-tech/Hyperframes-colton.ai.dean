"""Build the S01 speaker plate (ref frames 0-69) from raw.mp4.
Measured: rest crop = raw scaled 1.800, offset (-940,-11); zoom 1.15->1 circ.out 31f about (540,960);
per-frame raw index from best-match search vs reference (residual 2.0-2.2 luma);
white strobe on f1,3,5 = hole-filled person matte, gaussian sigma 40, gain 1.6 (fit MAE 0.03)."""
import cv2,numpy as np,sys,math,json,subprocess
rawdir,blobdir,mapjson,out=sys.argv[1:5]
fmap={int(k):v for k,v in json.load(open(mapjson)).items()}
fmap.update({1:2,3:4,5:5})            # strobe frames: neighbours (matcher can't see her under the white)
def circ(x): x=min(max(x,0),1); return math.sqrt(1-(x-1)**2)
def M_for(f):
    s=1+0.15*(1-circ(f/31)); M=np.float64([[1.8*s,0,0],[0,1.8*s,0]]); M[0,2]=540-s*(540+940); M[1,2]=960-s*(960+11); return M
p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","1080x1920","-r","30","-i","-",
  "-c:v","libx264","-preset","slow","-crf","12","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
for f in range(70):
    raw=cv2.imread(f"{rawdir}/f{fmap[f]+1:04d}.png")
    fr=cv2.warpAffine(raw,M_for(f),(1080,1920),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REFLECT)
    if f in (1,3,5):
        B=np.load(f"{blobdir}/blob_{f}.npy"); a=np.clip(cv2.GaussianBlur(B,(0,0),40)*1.6,0,1)[...,None]
        fr=(fr*(1-a)+255*a).astype(np.uint8)
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
