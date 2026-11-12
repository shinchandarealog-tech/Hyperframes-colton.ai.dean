import cv2,numpy as np,sys
# strip.py out a b step x0 y0 x1 y1 cols scale
out=sys.argv[1];a,b,s,x0,y0,x1,y1,cols=map(int,sys.argv[2:10]);sc=float(sys.argv[10])
ims=[]
for f in range(a,b+1,s):
    im=cv2.imread(f'ref/f/{f:05d}.jpg')[y0:y1,x0:x1];im=cv2.resize(im,None,fx=sc,fy=sc)
    cv2.putText(im,str(f),(4,22),0,0.7,(0,255,255),2);ims.append(im)
while len(ims)%cols: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out,np.vstack([np.hstack(ims[i:i+cols]) for i in range(0,len(ims),cols)]),[cv2.IMWRITE_JPEG_QUALITY,85])
