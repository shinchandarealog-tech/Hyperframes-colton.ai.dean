import cv2, glob, json, numpy as np
fs=sorted(glob.glob('aroll/f/a_*.jpg'))
cc=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
R=[]
for f in fs:
    g=cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY)
    d=cc.detectMultiScale(g,1.08,5,minSize=(50,50))
    if len(d): x,y,w,h=max(d,key=lambda r:r[2]*r[3]); R.append([int(y),int(y+h+0.05*h),int(x),int(x+w)])
    else: R.append(R[-1] if R else None)
for i in range(len(R)):
    if R[i] is None: R[i]=next(r for r in R if r)
chin=[max(R[j][1] for j in range(max(0,i-3),min(len(R),i+4))) for i in range(len(R))]
F=[[r[0],c,r[2],r[3]] for r,c in zip(R,chin)]
json.dump(F,open('aroll/faces.json','w'))
a=np.array(F); print('top',a[:,0].min(),a[:,0].max(),'chin',a[:,1].min(),a[:,1].max(),'x',a[:,2].min(),a[:,3].max())
im=cv2.imread(fs[100]); t,c,x0,x1=F[100]; cv2.rectangle(im,(x0,t),(x1,c),(0,255,0),3); cv2.line(im,(0,c),(1080,c),(0,0,255),3)
cv2.imwrite('an/faces_qc.jpg',cv2.resize(im,(540,960)))
