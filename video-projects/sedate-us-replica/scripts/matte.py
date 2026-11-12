import cv2,numpy as np,sys,math,mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision
S=sys.argv[1]
seg=vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=f"{S}/models/selfie_multiclass.tflite"),output_confidence_masks=True))
def circ(x): x=min(max(x,0),1); return math.sqrt(1-(x-1)**2)
def M_for(f):
    s=1+0.15*(1-circ(f/31)); M=np.float64([[1.8*s,0,0],[0,1.8*s,0]]); M[0,2]=540-s*(540+940); M[1,2]=960-s*(960+11); return M
for f,k in [(1,2),(3,4),(5,5)]:
    raw=cv2.imread(f"{S}/work/raw/f{k+1:04d}.png")
    img=mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(raw,cv2.COLOR_BGR2RGB))
    r=seg.segment(img); bg=r.confidence_masks[0].numpy_view().copy()
    fg=1-bg  # all non-background classes (hair, body, face, clothes, others)
    fgw=cv2.warpAffine(fg.astype(np.float32),M_for(f),(1080,1920))
    # measured ref alpha: compare strobe frame to the adjacent normal frame warped content
    ref=cv2.imread(f"{S}/work/ref/f{f+1:04d}.png").astype(np.float32)
    nrm=cv2.warpAffine(raw,M_for(f),(1080,1920)).astype(np.float32)
    a=((ref-nrm)/np.maximum(255-nrm,8)).mean(2).clip(0,1)
    cv2.imwrite(f"{S}/work/refalpha_{f}.png",(a*255).astype(np.uint8))
    cv2.imwrite(f"{S}/work/myfg_{f}.png",(fgw*255).astype(np.uint8))
    # row profile y=600 first 300 px
    print(f,"ref row600",[int(a[600,x]*255) for x in range(0,300,20)])
    print(f," my row600",[int(fgw[600,x]*255) for x in range(0,300,20)])
