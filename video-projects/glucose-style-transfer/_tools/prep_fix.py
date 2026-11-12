import cv2,numpy as np,json,os
from rembg import new_session,remove
from PIL import Image
hum=new_session('u2net_human_seg');gen=new_session('u2net')
def mask(img,s): return np.array(remove(Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)),session=s,only_mask=True,post_process_mask=True))
im=cv2.imread('broll/stills/mk_4954_0.3.jpg')  # vertical 1080x1920
m=np.maximum(mask(im,hum),mask(im,gen));m=cv2.GaussianBlur(m,(0,0),1.2)
ys,xs=np.where(m>20);x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
rgba=np.dstack([im,m])[y0:y1+1,x0:x1+1];cv2.imwrite('web/img/c_laptop.png',rgba);print('laptop',rgba.shape)
os.remove('web/img/c_meditate.png')
E=json.load(open('aroll/edl.json'))['EDL']
def e2o(k):
    for e0,o0,n in E:
        if e0<=k<e0+n: return o0+k-e0
for k in range(150,231):
    o=e2o(k);im=cv2.imread(f'aroll/f/a_{o+1:04d}.jpg');small=cv2.resize(im,(540,960))
    m=np.maximum(mask(small,hum),mask(small,gen))
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    m=cv2.resize(m,(1080,1920),interpolation=cv2.INTER_LINEAR);m=cv2.GaussianBlur(m,(0,0),1.5)
    cv2.imwrite(f'web/matte/m_{o+1:04d}.png',np.dstack([im,m]))
print('mattes ok')
