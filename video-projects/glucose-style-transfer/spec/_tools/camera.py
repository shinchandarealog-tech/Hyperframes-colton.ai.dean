import cv2,numpy as np,json
segs=[(1,62),(63,104),(160,310),(354,422),(550,714),(715,788)]
def g(f):
    im=cv2.imread(f'ref/c/{f:05d}.png',0).astype(np.float32);return im
out={}
for a,b in segs:
    ref=g(a);rows=[];W=np.eye(2,3,dtype=np.float32)
    for f in range(a,b+1):
        try: _,W=cv2.findTransformECC(ref,g(f),W.copy(),cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,80,1e-5),None,5)
        except cv2.error: pass
        s=float(np.sqrt(abs(np.linalg.det(W[:, :2]))));rows.append((f,round(1/s,4),round(float(W[0,2])*4,1),round(float(W[1,2])*4,1)))
    out[f'{a}-{b}']=rows
    sc=[r[1] for r in rows];print(a,b,'scale(rel first)',' '.join(f'{x:.3f}' for x in sc[::4]))
json.dump(out,open('spec/_tools/camera.json','w'))
