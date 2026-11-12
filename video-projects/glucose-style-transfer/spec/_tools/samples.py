import cv2,numpy as np,json
# (name, frame, crop x0,y0,x1,y1 (generous), ink rgb, tol, text)
S=[('sans_basically',390,(150,395,930,480),(255,255,255),70,'basically contain glucose'),
   ('sans_andyouhave',415,(300,280,780,380),(255,255,255),70,'and you have'),
   ('serif_blood',700,(30,150,1060,365),(160,45,30),80,'BLOOD'),
   ('serif_give',300,(100,352,1000,440),(150,40,30),80,'GIVE YOUR BODY'),
   ('serif_sweet',545,(240,225,820,380),(55,55,55),70,'sweet'),
   ('serif_sugars',520,(200,500,900,660),(55,55,55),70,'sugars.'),
]
res={}
for n,f,(x0,y0,x1,y1),rgb,tol,t in S:
    im=cv2.imread(f'ref/f/{f:05d}.jpg')[y0:y1,x0:x1].astype(np.float32)
    bgr=np.array(rgb[::-1],np.float32)
    d=np.sqrt(((im-bgr)**2).sum(2))
    m=(d<tol).astype(np.uint8)*255
    n_,lab,st,_=cv2.connectedComponentsWithStats(m)
    keep=np.zeros_like(m)
    for i in range(1,n_):
        if st[i,4]>25: keep[lab==i]=255
    ys,xs=np.where(keep>0)
    bb=(int(xs.min()+x0),int(ys.min()+y0),int(xs.max()+x0),int(ys.max()+y0))
    cv2.imwrite(f'ref/s_{n}.png',keep[ys.min():ys.max()+1,xs.min():xs.max()+1])
    # median colour of ink
    col=np.median(im[keep>0],axis=0)[::-1]
    res[n]=dict(frame=f,bbox=bb,text=t,ink='#%02x%02x%02x'%tuple(int(c) for c in col))
    print(n,res[n])
json.dump(res,open('spec/_tools/samples.json','w'),indent=1)
