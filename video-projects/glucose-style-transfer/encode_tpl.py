import json,subprocess,os,re,glob,cv2,numpy as np
FPS='24000/1001';OUT='Templates';os.makedirs(OUT,exist_ok=True);os.makedirs('an/enc',exist_ok=True)
def run(c): subprocess.run(c,check=True,capture_output=True)
clips=[]
for i in range(1,21):
    d=f'tpl/T{i:02d}';m=json.load(open(f'{d}/meta.json'))
    name=re.sub(r'[\\/:*?"<>|]','',m['name']).strip()
    out=f'{OUT}/T{i:02d} - {name}.mp4'
    dur=m['N']*1001/24000
    run(['ffmpeg','-y','-v','error','-framerate',FPS,'-i',f'{d}/f_%04d.jpg','-ss',f"{m['s0']:.4f}",'-t',f'{dur:.4f}','-i','audio/voice_tpl.wav',
         '-af',f'afade=t=in:d=0.01,afade=t=out:st={max(0,dur-0.04):.3f}:d=0.04',
         '-c:v','libx264','-crf','15','-preset','slow','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
         '-c:a','aac','-b:a','320k','-ar','48000','-ac','2','-shortest','-movflags','+faststart',out])
    clips.append((i,name,out,m['N']));print('enc',out)
# number cards + pack
parts=[]
for i,name,out,N in clips:
    card=np.zeros((1920,1080,3),np.uint8)
    cv2.putText(card,f'T{i:02d}',(330,960),cv2.FONT_HERSHEY_DUPLEX,5,(240,240,240),8,cv2.LINE_AA)
    cv2.imwrite('an/enc/card.png',card);cp=f'an/enc/card_{i:02d}.mp4'
    run(['ffmpeg','-y','-v','error','-loop','1','-framerate',FPS,'-i','an/enc/card.png','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','0.8',
         '-c:v','libx264','-crf','15','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-ar','48000','-shortest',cp])
    parts+= [cp,out]
open('an/enc/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','an/enc/list.txt','-c:v','libx264','-crf','15','-preset','slow','-pix_fmt','yuv420p',
     '-r',FPS,'-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',f'{OUT}/00 ALL TEMPLATES.mp4'])
# overview: one hero frame per template (85 % in, everything on screen)
tiles=[]
for i,name,out,N in clips:
    im=cv2.imread(f'tpl/T{i:02d}/f_{int(N*0.85):04d}.jpg');im=cv2.resize(im,(360,640),interpolation=cv2.INTER_AREA)
    bar=np.zeros((70,360,3),np.uint8);cv2.putText(bar,f'T{i:02d}',(8,30),cv2.FONT_HERSHEY_DUPLEX,0.85,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(bar,name[:44],(8,58),cv2.FONT_HERSHEY_SIMPLEX,0.42,(200,200,200),1,cv2.LINE_AA);tiles.append(np.vstack([im,bar]))
cv2.imwrite(f'{OUT}/00 OVERVIEW.jpg',np.vstack([np.hstack(tiles[r*5:r*5+5]) for r in range(4)]),[cv2.IMWRITE_JPEG_QUALITY,90])
print('done')
