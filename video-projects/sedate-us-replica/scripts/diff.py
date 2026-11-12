import cv2,numpy as np,sys
S=sys.argv[1]; n=int(sys.argv[2])
rows=[]
for f in range(n):
    a=cv2.imread(f"{S}/work/ref/f{f+1:04d}.png").astype(np.float32); b=cv2.imread(f"{S}/work/mine/f{f+1:04d}.png").astype(np.float32)
    d=np.abs(a-b).mean(2)
    rows.append((f,d.mean(),d[900:1320].mean(),d[:900].mean(), (d>40).sum()))
for r in rows: print("f%02d all %.2f text-band %.2f top %.2f px>40: %d"%r)
