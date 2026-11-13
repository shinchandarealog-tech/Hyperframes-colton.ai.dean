import cv2,numpy as np,glob,os
r=cv2.imread('ref/ref_1080.png'); hsv=cv2.cvtColor(r,cv2.COLOR_BGR2HSV); g=cv2.cvtColor(r,cv2.COLOR_BGR2GRAY)
def bbox(m):
    ys,xs=np.where(m>0); return xs.min(),ys.min(),xs.max()+1,ys.max()+1
def refmask(kind):
    if kind=='script':
        m=((hsv[...,0]>20)&(hsv[...,0]<40)&(hsv[...,1]>80)&(hsv[...,2]>90)).astype(np.float32); m[:495]=0;m[605:]=0;m[:,:335]=0;m[:,668:]=0
    elif kind=='sans':
        m=(g>110).astype(np.float32)*(hsv[...,1]<60); m[:420]=0;m[495:]=0;m[:,:390]=0;m[:,:][:,660:]=0
    else:
        m=(g>90).astype(np.float32)*(hsv[...,1]<60); m[:600]=0;m[722:]=0;m[:,:320]=0;m[:,735:]=0
    x0,y0,x1,y1=bbox(m); return m[y0:y1,x0:x1],(x0,y0,x1,y1)
out={}
for kind in ['script','sans','bold']:
    R,bb=refmask(kind); print(kind,'ref ink bbox',bb, 'size',R.shape[::-1])
    res=[]
    for f in glob.glob(f'an/font/{kind}_*.png'):
        im=cv2.imread(f,0).astype(np.float32)/255
        if kind=='bold':  # crop to x-height band like ref (top of i-dot to baseline): drop descender
            pass
        m=(im>0.4).astype(np.float32)
        if m.sum()==0: continue
        x0,y0,x1,y1=bbox(m); c=m[y0:y1,x0:x1]
        if kind=='bold':  # ref is cut at baseline (p descender excluded): cut candidate at baseline = bottom of 'e'
            col=m[:,x1-40:x1]; yb=np.where(col.sum(1)>0)[0].max()+1; c=m[y0:yb,x0:x1]
        aspect=c.shape[1]/c.shape[0]; ra=R.shape[1]/R.shape[0]
        c=cv2.resize(c,(R.shape[1],R.shape[0]),interpolation=cv2.INTER_AREA)
        a=R-R.mean(); b=c-c.mean(); ncc=(a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum())
        res.append((round(float(ncc),3),round(aspect/ra,3),os.path.basename(f)))
    res.sort(reverse=True); print(*res[:8],sep='\n')
