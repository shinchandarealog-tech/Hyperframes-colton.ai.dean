import cv2, json, sys
cap = cv2.VideoCapture(sys.argv[1]); det = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
res=[]; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    if i%5==0:
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY); fs=det.detectMultiScale(g,1.1,6,minSize=(80,80))
        if len(fs): x,y,w,h=max(fs,key=lambda r:r[2]*r[3]); res.append((i,int(x*1.5),int(y*1.5),int(w*1.5),int(h*1.5)))
    i+=1
ys=[r[2]+r[4] for r in res]; xs=[r[1] for r in res]; xe=[r[1]+r[3] for r in res]; yt=[r[2] for r in res]
print("frames",i,"detections",len(res)); print("chin y (1080x1920 space) min/max",min(ys),max(ys)); print("top",min(yt),max(yt)); print("x",min(xs),max(xe))
