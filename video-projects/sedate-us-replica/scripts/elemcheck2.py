import cv2,numpy as np,sys
S=sys.argv[1]
E={"I":(range(31,36),500,945,535,1025),"think":(range(33,36),540,945,715,1025),"right":(range(34,36),255,985,535,1135),
 "now":(range(34,36),535,1012,800,1108),"pill":(range(35,36),398,1080,684,1160),"is":(range(62,70),352,950,420,1022),
 "in":(range(62,70),418,950,486,1022),"a":(range(66,70),486,965,538,1022),"really":(range(67,70),540,950,724,1036),
 "bar":(range(67,70),222,1020,856,1176),"INTERESTING":(range(68,70),250,1032,830,1166),"tag":(range(45,70,3),105,1192,446,1298)}
def g(im):
    im=cv2.GaussianBlur(im,(0,0),1.0); return np.hypot(cv2.Sobel(im,cv2.CV_32F,1,0),cv2.Sobel(im,cv2.CV_32F,0,1))
for k,(fr,x0,y0,x1,y1) in E.items():
    sh=[]
    for f in fr:
        a=cv2.imread(f"{S}/work/ref/f{f+1:04d}.png",0).astype(np.float32)[y0:y1,x0:x1]
        b=cv2.imread(f"{S}/work/mine/f{f+1:04d}.png",0).astype(np.float32)[y0:y1,x0:x1]
        win=cv2.createHanningWindow((a.shape[1],a.shape[0]),cv2.CV_32F); (dx,dy),r=cv2.phaseCorrelate(g(b),g(a),win); sh.append((dx,dy))
    sh=np.array(sh); print(f"{k:12s} n={len(sh)} dx={np.median(sh[:,0]):+.2f} dy={np.median(sh[:,1]):+.2f}  spread {sh.std(0).round(2)}")
