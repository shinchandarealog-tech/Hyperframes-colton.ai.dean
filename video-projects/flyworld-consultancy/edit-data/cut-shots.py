import subprocess, json, glob, os
U='/root/.claude/uploads/0076372e-2d12-5fc9-9c6c-efb9ad4a2a95/'
P='/workspace/Hyperframes-colton.ai.dean/video-projects/flyworld-consultancy/assets/'
def f(h): return glob.glob(U+h+'-*.mp4')[0]
REAL=f('252708fa'); C={i+1:f(h) for i,h in enumerate('f0841691 d9e09d24 916bb633 8196cf44 7422266e 0bf32b71 79cf036c 57fe450d ccc4c520 936885c8 4f013b87 361f7191 2165b8f4 f254f4c6 99d3abf5'.split())}
PAD=0.25; END=74.4
# shot: name, [ (src, src_in, src_out, vo_a, vo_b), ... ]
shots=[
 ('s01-office-sign',[(REAL,21.0,23.9,0.0,2.9)]),
 ('s02-office-desks',[(REAL,24.2,26.1,2.9,4.8)]),
 ('s03-office-logo',[(REAL,45.3,47.2,4.8,6.7)]),
 ('s04-dream',[(C[2],1.3,5.5,6.7,10.9)]),
 ('s05-dubai',[(C[3],1.4,5.6,10.9,15.1)]),
 ('s06-urgent',[(C[4],1.6,5.9,15.1,18.8)]),
 ('s07-trades1',[(C[5],0.2,1.7,18.8,20.36),(C[5],2.3,3.6,20.36,21.2),(C[5],4.3,5.9,21.2,21.96)]),
 ('s08-trades2',[(C[6],0.1,1.6,21.96,22.88),(C[6],2.3,3.6,22.88,24.06),(C[6],4.3,5.9,24.06,25.04)]),
 ('s09-trades3',[(C[8],0.0,1.1,25.04,26.0),(C[8],1.3,2.6,26.0,26.86),(C[8],3.0,4.1,26.86,28.0),(C[8],4.5,6.0,28.0,29.0)]),
 ('s10-civil',[(C[9],0.6,6.0,29.0,34.4)]),
 ('s11-visa',[(C[10],0.0,6.0,34.4,42.6)]),
 ('s12-benefits',[(C[11],0.0,1.4,42.6,43.8),(C[11],1.5,2.9,43.8,45.0),(C[11],3.5,5.9,45.0,46.4)]),
 ('s13-medical',[(C[12],0.2,1.6,46.4,47.35),(C[12],2.0,5.9,47.35,49.2)]),
 ('s14-interview',[(C[13],1.5,5.9,49.2,52.9)]),
 ('s15-contact-cta',[(C[14],0.0,6.0,52.9,59.0)]),
 ('s16-contact-card',[(C[15],1.3,6.0,59.0,64.4)]),
 ('s17-office-entry',[(REAL,11.0,13.9,64.4,67.3)]),
 ('s18-future',[(C[1],0.3,3.6,67.3,70.4)]),
 ('s19-outro',[(C[15],3.4,6.0,70.4,END)]),
]
VF='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30'
plan=[]
for i,(name,subs) in enumerate(shots):
    parts=[]
    for j,(src,si,so,a,b) in enumerate(subs):
        k=(so-si)/(b-a)
        pre = PAD if (j==0 and i>0) else 0
        post= PAD if (j==len(subs)-1 and i<len(shots)-1) else 0
        s0=max(0,si-pre*k); s1=so+post*k
        dur=(b-a)+pre+post
        tmp=f'/tmp/part_{i}_{j}.mp4'
        srcdur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
        s1=min(s1,srcdur-0.05)
        stretch=dur/(s1-s0)
        subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{s0:.3f}','-to',f'{s1:.3f}','-i',src,'-an','-vf',
          f'setpts=(PTS-STARTPTS)*{stretch:.5f},{VF},tpad=stop_mode=clone:stop_duration=1,trim=duration={dur:.3f}',
          '-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',tmp],check=True)
        parts.append(tmp)
    out=P+name+'.mp4'
    with open('/tmp/list.txt','w') as fl: fl.write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','/tmp/list.txt','-c','copy','-movflags','+faststart',out],check=True)
    a=subs[0][3]; b=subs[-1][4]
    start=a-(PAD if i>0 else 0); end=b+(PAD if i<len(shots)-1 else 0)
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out]))
    plan.append(dict(name=name,start=round(start,3),dur=round(end-start,3),file_dur=round(d,3)))
    print(plan[-1])
json.dump(plan,open(P+'../edit-data/edl.json','w'),indent=1)
