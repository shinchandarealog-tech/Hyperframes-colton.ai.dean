import cv2,numpy as np,json,os
from rembg import new_session,remove
from PIL import Image
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
S='broll/stills/';O='web/img/'
def still(vid,k,t=None):
    p=f'{S}mk_{vid}_{k}.jpg'
    if t is not None:
        p=f'{S}mk_{vid}_t{t}.jpg'
        if not os.path.exists(p): os.system(f'ffmpeg -v error -y -ss {t} -i broll/mk_{vid}.mp4 -frames:v 1 -q:v 2 {p}')
    return cv2.imread(p)
def crop(im,cx,cy,w,h,outw,outh,sharpen=True):
    H,W=im.shape[:2];sc=max(outw/w,outh/h)
    x0=int(np.clip(cx-w/2,0,W-w));y0=int(np.clip(cy-h/2,0,H-h));c=im[y0:y0+h,x0:x0+w]
    c=cv2.resize(c,(outw,outh),interpolation=cv2.INTER_LANCZOS4)
    if sharpen and sc>1.2: b=cv2.GaussianBlur(c,(0,0),1.2);c=cv2.addWeighted(c,1.35,b,-0.35,0)
    return c
hum=new_session('u2net_human_seg');gen=new_session('u2net')
def cut(img,sess,out):
    rgba=remove(Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)),session=sess,post_process_mask=True)
    rgba.save(out);return rgba
# --- full-bleed vertical photo pages (1240x2200 = room for push-in)
v=still('39767',0,t=4.0); v=cv2.resize(v,(1240,2205))[:2200];cv2.imwrite(O+'p_family.jpg',v,[cv2.IMWRITE_JPEG_QUALITY,93]);cut(v,hum,O+'p_family_cut.png')
im=still('49944',0.3);cv2.imwrite(O+'p_momlift.jpg',crop(im,1020,540,608,1080,1240,2200),[cv2.IMWRITE_JPEG_QUALITY,93])
im=still('4397',0.3);cv2.imwrite(O+'p_sunrise.jpg',crop(im,700,540,608,1080,1240,2200),[cv2.IMWRITE_JPEG_QUALITY,93])
# --- cut-outs on flat colour
im=still('4803',0.3);c=crop(im,1500,560,760,1080,760,1080,False);cut(c,hum,O+'c_meditate.png')
im=still('50044',0.3);c=crop(im,1080,560,900,1080,900,1080,False);cut(c,hum,O+'c_mombaby.png')
# --- carousel cards 400x660
cards=[('49974',0.3,1300,540),('4954',0.3,540,960),('4803',0.6,1100,540),('39767',0.3,540,960)]
for i,(vid,k,cx,cy) in enumerate(cards):
    im=still(vid,k);H,W=im.shape[:2]
    if H>W: c=crop(im,cx,cy,W,int(W*660/400),400,660)
    else: c=crop(im,cx,cy,int(H*400/660),H,400,660)
    cv2.imwrite(O+f'card_{i}.jpg',c,[cv2.IMWRITE_JPEG_QUALITY,92])
# --- grid tiles 300x366
tiles=[('49944',0.6,960),('50044',0.6,1000),('49974',0.6,1150),('49952',0.3,1000),('8717',0.3,950),('39767',0.6,None),('31274',0.3,900),('1012',0.3,1080),('4803',0.3,1500)]
for i,(vid,k,cx) in enumerate(tiles):
    im=still(vid,k);H,W=im.shape[:2]
    c=crop(im,W/2 if cx is None else cx,H/2,(W if H>W else int(H*300/366)) if H<W else W,(H if H<W else int(W*366/300)),300,366)
    cv2.imwrite(O+f'tile_{i}.jpg',c,[cv2.IMWRITE_JPEG_QUALITY,92])
print('broll ok')
# --- person mattes for T17 (edit frames 150-230)
E=json.load(open('aroll/edl.json'))['EDL']
def e2o(k):
    for e0,o0,n in E:
        if e0<=k<e0+n: return o0+k-e0
for k in range(150,231):
    o=e2o(k);out=f'web/matte/m_{o+1:04d}.png'
    if os.path.exists(out): continue
    im=cv2.imread(f'aroll/f/a_{o+1:04d}.jpg');small=cv2.resize(im,(540,960))
    m=remove(Image.fromarray(cv2.cvtColor(small,cv2.COLOR_BGR2RGB)),session=hum,only_mask=True,post_process_mask=True)
    m=cv2.resize(np.array(m),(1080,1920),interpolation=cv2.INTER_LINEAR);m=cv2.GaussianBlur(m,(0,0),1.5)
    rgba=np.dstack([im,m]);cv2.imwrite(out,rgba)
print('mattes ok')
