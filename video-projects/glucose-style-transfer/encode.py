# encode.py sheet | deliver "<name>"  — never overwrites an existing delivery
import glob,os,subprocess,sys,cv2,numpy as np
fr=[f for d in sorted(glob.glob('vid/S*')) for f in sorted(glob.glob(d+'/f_*.jpg'))]
if sys.argv[1]=='sheet':
    t=[]
    for i in range(0,len(fr),12):
        im=cv2.resize(cv2.imread(fr[i]),(135,240));cv2.putText(im,str(i),(3,16),0,.5,(0,255,255),1);t.append(im)
    while len(t)%13: t.append(np.zeros_like(t[0]))
    cv2.imwrite('an/video_sheet.jpg',np.vstack([np.hstack(t[i:i+13]) for i in range(0,len(t),13)]),[cv2.IMWRITE_JPEG_QUALITY,85]);print(len(fr),'frames')
else:
    os.makedirs('Client 1',exist_ok=True);out=f'Client 1/{sys.argv[2]}.mp4'
    if os.path.exists(out): sys.exit('exists, not overwriting: '+out)
    open('an/frames.txt','w').write(''.join(f"file '{os.path.abspath(f)}'\nduration {1001/24000}\n" for f in fr))
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','an/frames.txt','-i','audio/mix.wav','-r','24000/1001','-fps_mode','cfr',
      '-c:v','libx264','-crf','15','-preset','slow','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
      '-c:a','aac','-b:a','320k','-ar','48000','-shortest','-movflags','+faststart',out],check=True);print(out,len(fr),'frames')
