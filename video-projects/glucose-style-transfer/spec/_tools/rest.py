import cv2,numpy as np,json,sys
sys.path.insert(0,'spec/_tools');from elements import E
out={};tiles=[]
for n,a,r,(x0,y0,x1,y1),ink,tol in E:
    im=cv2.imread(f'ref/f/{r:05d}.jpg');reg=im[y0:y1,x0:x1]
    if ink is None: bb=(x0,y0,x1,y1)
    else:
        d=np.sqrt(((reg.astype(np.float32)-np.array(ink[::-1],np.float32))**2).sum(2));m=(d<tol).astype(np.uint8)
        nn,lab,st,_=cv2.connectedComponentsWithStats(m);keep=np.isin(lab,[i for i in range(1,nn) if st[i,4]>30])
        ys,xs=np.where(keep)
        if len(xs)==0: print('FAIL',n); continue
        bb=(int(x0+xs.min()),int(y0+ys.min()),int(x0+xs.max()+1),int(y0+ys.max()+1))
    out[n]=dict(a=a,rest=r,bbox=bb,ink=ink,tol=tol)
    c=im[bb[1]:bb[3],bb[0]:bb[2]].copy();h=80;c=cv2.resize(c,(max(1,int(c.shape[1]*h/c.shape[0])),h))
    c=cv2.copyMakeBorder(c,24,4,4,4,cv2.BORDER_CONSTANT,0);cv2.putText(c,f'{n} {bb}',(2,18),0,0.5,(0,255,255),1);tiles.append(c)
json.dump(out,open('spec/_tools/rest.json','w'),indent=1)
W=max(t.shape[1] for t in tiles);W=min(W,1400)
rows=[];row=[];w=0
for t in tiles:
    t=t[:, :1400]
    if w+t.shape[1]>1400: rows.append(row);row=[];w=0
    row.append(t);w+=t.shape[1]
rows.append(row)
cv2.imwrite('an/rest.jpg',np.vstack([np.pad(np.hstack(r),((0,0),(0,1400-sum(x.shape[1] for x in r)),(0,0))) for r in rows]))
