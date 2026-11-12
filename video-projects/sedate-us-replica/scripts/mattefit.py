import cv2,numpy as np,sys
S=sys.argv[1]
def blob(f):
    fg=cv2.imread(f"{S}/work/myfg_{f}.png",0)
    b=(fg>128).astype(np.uint8)
    b=cv2.morphologyEx(b,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,61)))
    # fill holes (mic etc) via flood fill from top corners
    h,w=b.shape; ff=b.copy()*255; m=np.zeros((h+2,w+2),np.uint8)
    cv2.floodFill(ff,m,(0,0),128); cv2.floodFill(ff,m,(w-1,0),128)
    out=(ff!=128).astype(np.float32); return out
for f in [1,3,5]:
    ref=cv2.imread(f"{S}/work/refalpha_{f}.png",0).astype(np.float32)/255
    B=blob(f); best=None
    for sig in [15,20,25,30,35,40,50,60]:
        bl=cv2.GaussianBlur(B,(0,0),sig)
        for g in [1.0,1.3,1.6,2.0,2.5,3.0,4.0]:
            a=np.clip(bl*g,0,1); e=np.abs(a[:900]-ref[:900]).mean()
            if best is None or e<best[0]: best=(e,sig,g)
    e,sig,g=best; a=np.clip(cv2.GaussianBlur(B,(0,0),sig)*g,0,1)
    print(f,"best sigma",sig,"gain",g,"mae %.3f"%e, "row600",[int(a[600,x]*255) for x in range(0,200,20)])
    cv2.imwrite(f"{S}/work/fit_{f}.png",(a*255).astype(np.uint8)); np.save(f"{S}/work/blob_{f}.npy",B)
