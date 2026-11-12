import cv2,numpy as np,sys,subprocess
# usage: sheet.py video out.jpg [step]  -- every `step`-th frame, 108x192 tiles, 12 per row
v,out=sys.argv[1],sys.argv[2]; step=int(sys.argv[3]) if len(sys.argv)>3 else 1
cap=cv2.VideoCapture(v); t=[]; f=0
while True:
    ok,fr=cap.read()
    if not ok: break
    if f%step==0:
        im=cv2.resize(fr,(108,192),interpolation=cv2.INTER_AREA); cv2.putText(im,str(f),(3,14),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255),1); t.append(im)
    f+=1
while len(t)%12: t.append(np.zeros_like(t[0]))
cv2.imwrite(out,np.vstack([np.hstack(t[i:i+12]) for i in range(0,len(t),12)]),[cv2.IMWRITE_JPEG_QUALITY,80])
