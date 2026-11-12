import cv2,numpy as np,json,sys
sys.path.insert(0,'spec/_tools');from eases import fit
R=json.load(open('spec/_tools/rest.json'));only=sys.argv[1:] 
out={}
def g(f): return cv2.imread(f'ref/f/{f:05d}.jpg')
for n,e in R.items():
    if only and n not in only: continue
    x0,y0,x1,y1=e['bbox'];r=e['rest'];a=e['a'];P=40
    T=cv2.cvtColor(g(r)[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY)
    ser=[]
    for f in range(a,r+1):
        im=g(f);gr=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        sx0,sy0=max(0,x0-120),max(0,y0-120);S=gr[sy0:min(1920,y1+120),sx0:min(1080,x1+120)]
        best=(-2,0,0,1)
        for s in np.arange(0.7,1.31,0.02):
            t=cv2.resize(T,None,fx=s,fy=s)
            if t.shape[0]>=S.shape[0] or t.shape[1]>=S.shape[1] or min(t.shape)<8: continue
            m=cv2.matchTemplate(S,t,cv2.TM_CCOEFF_NORMED);_,mv,_,ml=cv2.minMaxLoc(m)
            if mv>best[0]:
                cx=sx0+ml[0]+t.shape[1]/2;cy=sy0+ml[1]+t.shape[0]/2;best=(mv,cx-(x0+x1)/2,cy-(y0+y1)/2,s)
        row=dict(f=f,score=round(float(best[0]),3),dx=round(float(best[1]),1),dy=round(float(best[2]),1),s=round(float(best[3]),3))
        if e['ink']:
            reg=im[y0-P:y1+P,x0-P:x1+P].astype(np.float32) if y0>=P and x0>=P else im[y0:y1,x0:x1].astype(np.float32)
            d=np.sqrt(((reg-np.array(e['ink'][::-1],np.float32))**2).sum(2));m=d<e['tol']
            ys,xs=np.where(m);row['ink']=int(m.sum())
            row['ix0'],row['ix1']=(int(xs.min()),int(xs.max())) if len(xs) else (0,0)
        sh=cv2.Laplacian(gr[y0:y1,x0:x1],cv2.CV_32F).var();row['sharp']=round(float(sh),1)
        ser.append(row)
    if e['ink']:
        mx=ser[-1]['ink'] or 1
        for rw in ser: rw['vis']=round(rw['ink']/mx,3)
    fits={}
    fs=[r_['f'] for r_ in ser]
    for k in ['dx','dy','s','vis','sharp']:
        v=np.array([r_.get(k,np.nan) for r_ in ser],float)
        if np.isnan(v).any(): continue
        v0,v1=v[0],v[-1]
        if abs(v1-v0)<{'dx':6,'dy':6,'s':0.03,'vis':0.25,'sharp':v1*0.4+1}[k]: continue
        fits[k]=dict(fit(fs,(v-v0)/(v1-v0)),frm=round(float(v0),3),to=round(float(v1),3))
    out[n]=dict(bbox=e['bbox'],series=ser,fits=fits)
    print(n,e['bbox'],json.dumps(fits))
json.dump(out,open('spec/_tools/track_'+('_'.join(only) if only else 'all')+'.json','w'))
