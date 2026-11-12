import cv2,glob,numpy as np,sys,collections
a,b=int(sys.argv[1]),int(sys.argv[2]);out=sys.argv[3]
g=collections.defaultdict(list)
for f in sorted(glob.glob('an/test/T*.jpg')): g[int(f.split('/')[-1][1:3])].append(f)
rows=[]
for t in range(a,b+1):
    ims=[]
    for f in g[t]:
        im=cv2.resize(cv2.imread(f),(270,480));cv2.putText(im,f.split('/')[-1][:-4],(4,20),0,0.6,(0,255,255),2);ims.append(im)
    rows.append(np.hstack(ims))
cv2.imwrite(out,np.vstack([np.hstack(rows[i:i+2]) if i+1<len(rows) else np.hstack([rows[i],np.zeros_like(rows[i])]) for i in range(0,len(rows),2)]),[cv2.IMWRITE_JPEG_QUALITY,85])
