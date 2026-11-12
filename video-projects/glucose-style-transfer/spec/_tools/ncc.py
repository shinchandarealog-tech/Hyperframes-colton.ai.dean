import cv2,numpy as np,glob,json,collections
S=json.load(open('spec/_tools/samples.json'))
res=collections.defaultdict(list)
for f in sorted(glob.glob('an/ft/*.png')):
    n,c=f.split('/')[-1][:-4].split('__')
    a=cv2.imread(f'ref/s_{n}.png',0).astype(np.float32)
    im=cv2.imread(f,0); ys,xs=np.where(im>128); b=im[ys.min():ys.max()+1,xs.min():xs.max()+1].astype(np.float32)
    b=cv2.resize(b,(a.shape[1],a.shape[0]),interpolation=cv2.INTER_AREA)
    a1=cv2.GaussianBlur(a,(5,5),0);b1=cv2.GaussianBlur(b,(5,5),0)
    ncc=((a1-a1.mean())*(b1-b1.mean())).sum()/np.sqrt(((a1-a1.mean())**2).sum()*((b1-b1.mean())**2).sum())
    ar=(im.shape and (xs.max()-xs.min())/(ys.max()-ys.min()))/(a.shape[1]/a.shape[0])
    ink=(b>128).mean()/(a>128).mean()
    res[n].append((round(float(ncc),3),c,round(float(ar),3),round(float(ink),2)))
for n,v in res.items():
    print(n); [print('  ',x) for x in sorted(v,reverse=True)[:5]]
