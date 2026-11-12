import cv2,numpy as np,glob,json
fs=sorted(glob.glob('aroll/f/a_*.jpg'))
C=[cv2.CascadeClassifier('_tools/models/'+n) for n in ['haarcascade_frontalface_default.xml','haarcascade_profileface.xml']]
raw=[]
for i,f in enumerate(fs):
    g=cv2.cvtColor(cv2.resize(cv2.imread(f),(540,960)),cv2.COLOR_BGR2GRAY);best=None
    for c in C:
        for flip in [0,1]:
            gg=cv2.flip(g,1) if flip else g
            r=c.detectMultiScale(gg,1.08,5,minSize=(80,80))
            for (x,y,w,h) in r:
                if flip: x=540-x-w
                if best is None or w*h>best[2]*best[3]: best=(x,y,w,h)
    raw.append([v*2 for v in best] if best is not None else None)
# fill gaps by interpolation
idx=[i for i,r in enumerate(raw) if r];arr=np.array([raw[i] for i in idx],float)
full=np.array([np.interp(range(len(raw)),idx,arr[:,k]) for k in range(4)]).T
# smooth
k=5;sm=np.array([np.convolve(np.pad(full[:,j],k,mode='edge'),np.ones(2*k+1)/(2*k+1),'valid') for j in range(4)]).T
faces=[]
for x,y,w,h in sm:
    faces.append([round(y-0.25*h),round(y+h*1.05+0.05*h),round(x),round(x+w)])  # top(incl hair), chin, x0, x1
chin=np.array([f[1] for f in faces]);chin=np.array([chin[max(0,i-3):i+4].max() for i in range(len(chin))])
for i in range(len(faces)): faces[i][1]=int(chin[i])
open('web/faces.js','w').write('window.FACES='+json.dumps(faces)+';\n')
print('detected',len(idx),'/',len(raw),'chin y range',chin.min(),chin.max(),'top',min(f[0] for f in faces))
tiles=[]
for i in range(0,len(fs),43):
    im=cv2.imread(fs[i]);t,c,x0,x1=faces[i];cv2.rectangle(im,(x0,t),(x1,c),(0,255,0),4);cv2.line(im,(0,c),(1080,c),(0,0,255),6)
    im=cv2.resize(im,(216,384));cv2.putText(im,str(i+1),(4,24),0,0.8,(0,255,255),2);tiles.append(im)
while len(tiles)%10: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite('an/faces_qc.jpg',np.vstack([np.hstack(tiles[i:i+10]) for i in range(0,len(tiles),10)]))
