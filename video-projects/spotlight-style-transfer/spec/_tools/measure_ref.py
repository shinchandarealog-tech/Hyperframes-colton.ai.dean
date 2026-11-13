import cv2, numpy as np, json
im=cv2.imread('ref/ref_frame.jpg'); im=cv2.resize(im,(1080,1920),interpolation=cv2.INTER_CUBIC)
cv2.imwrite('ref/ref_1080.png',im)
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
# yellow
Y=((hsv[...,0]>20)&(hsv[...,0]<40)&(hsv[...,1]>120)&(hsv[...,2]>150)).astype(np.uint8)
n,lab,st,cen=cv2.connectedComponentsWithStats(Y)
ys=[]
for i in range(1,n):
    x,y,w,h,a=st[i]
    if a>40:
        col=im[lab==i].mean(0)[::-1]; ys.append(dict(box=[int(x),int(y),int(x+w),int(y+h)],area=int(a),rgb='#%02x%02x%02x'%tuple(int(c) for c in col)))
print('YELLOW',json.dumps(ys))
# bright white text pixels
g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
W=((g>200)&(hsv[...,1]<40)).astype(np.uint8)
rows=W[:, :].sum(1)
band=[]; on=False
for y,v in enumerate(rows):
    if v>3 and not on: on=True; y0=y
    if v<=3 and on:
        on=False
        if y-y0>4:
            xs=np.where(W[y0:y].sum(0)>0)[0]; band.append([y0,y,int(xs.min()),int(xs.max())])
print('WHITE_BANDS',band)
# card: column profile of brightness in y 300-1100 band
for y in [300,600,900,1100,1160]:
    r=g[y].astype(int); print('row',y,[ (x,r[x]) for x in range(150,960,30)])
