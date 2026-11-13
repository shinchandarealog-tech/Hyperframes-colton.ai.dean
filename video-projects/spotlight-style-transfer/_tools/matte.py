import glob, os, numpy as np, cv2
from rembg import new_session, remove
from PIL import Image
s=new_session('u2net_human_seg')
fs=sorted(glob.glob('aroll/f/a_*.jpg'))
for i,f in enumerate(fs):
    o='aroll/m/'+os.path.basename(f).replace('a_','m_').replace('.jpg','.png')
    if os.path.exists(o): continue
    im=Image.open(f).convert('RGB').resize((540,960))
    m=remove(im,session=s,only_mask=True,post_process_mask=True)
    m=np.array(m.resize((1080,1920),Image.BILINEAR)); m=cv2.GaussianBlur(m,(5,5),0)
    cv2.imwrite(o,m)
    if i%20==0: print(i,flush=True)
print('done')
