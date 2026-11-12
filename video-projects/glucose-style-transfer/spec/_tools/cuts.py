import cv2,numpy as np,glob,json
fs=sorted(glob.glob('ref/c/*.png'))
prev=None;rows=[]
for i,f in enumerate(fs,1):
    im=cv2.imread(f).astype(np.float32)
    if prev is not None:
        d=np.abs(im-prev).mean(); dt=np.abs(im[:240]-prev[:240]).mean(); db=np.abs(im[240:]-prev[240:]).mean()
        h1=cv2.calcHist([im.astype(np.uint8)],[0,1,2],None,[8,8,8],[0,256]*3);h0=cv2.calcHist([prev.astype(np.uint8)],[0,1,2],None,[8,8,8],[0,256]*3)
        hc=cv2.compareHist(h0,h1,cv2.HISTCMP_CORREL)
        rows.append((i,round(float(d),2),round(float(dt),2),round(float(db),2),round(float(hc),3)))
    prev=im
json.dump(rows,open('an/ref_diff.json','w'))
ds=np.array([r[1] for r in rows])
for r in rows:
    if r[1]>12 or r[4]<0.8: print(r)
print('dup frames (d<0.3):',sum(ds<0.3),'median',np.median(ds))
