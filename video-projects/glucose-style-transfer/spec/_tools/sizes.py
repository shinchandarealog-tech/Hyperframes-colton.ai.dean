import cv2,numpy as np,json
M={'sans':dict(cap=.69,xh=.47,asc=.71,desc=.2),'serif':dict(cap=.66,xh=.485,asc=.705,desc=.23),'serifi':dict(cap=.66,xh=.5,asc=.7,desc=.23)}
# name, frame, region, ink, tol, font, metric (top,bottom), text
T=[('hook "the word"',30,(380,1240,700,1330),(250,250,250),60,'sans','asc',''),
('hook GLUCOSE',30,(330,1335,760,1420),(250,250,250),60,'serifi','cap',''),
('hook "to me is"',55,(330,1240,760,1320),(250,250,250),60,'sans','asc',''),
('hook OVERWHELMING',55,(150,1300,1000,1390),(240,140,40),90,'serif','cap',''),
('S02 "so glucose is"',95,(60,690,520,760),(250,250,250),50,'sans','asc',''),
('S03 "all of our"',125,(250,330,850,418),(250,250,250),60,'sans','asc',''),
('S03 BRAINS',125,(240,430,900,590),(100,70,60),70,'serifi','cap',''),
('S06 "so it\'s"',225,(300,950,700,1022),(250,250,250),60,'sans','asc',''),
('S06 "the energy"',225,(120,1030,1000,1200),(240,150,40),90,'serifi','asc+desc',''),
('S07 "to do everything"',260,(200,950,1000,1080),(250,240,215),45,'serif','asc+desc',''),
('S08 "and how do you"',300,(250,280,900,350),(150,40,30),70,'sans','asc',''),
('S08 GIVE YOUR BODY',300,(100,352,1000,440),(150,40,30),70,'serif','cap',''),
('S08 "this energy" pill',300,(560,420,980,540),(150,40,30),70,'sans','box',''),
('S10 carbs',390,(250,220,950,400),(250,240,230),40,'serifi','asc','carbs (x-height+asc)'),
('S10 bar',390,(250,300,950,400),(150,40,30),70,'-','box',''),
('S10 basically',390,(150,395,930,480),(250,250,250),70,'sans','asc+desc',''),
('S11 pill',415,(370,380,920,500),(245,232,215),30,'-','box',''),
('S16 starches pill',590,(120,1060,1040,1240),(70,30,25),45,'-','box',''),
('S16 "starches or sugars"',590,(150,1080,1000,1220),(250,250,250),60,'serifi','asc','x'),
('S17 GLUCOSE MOLECULES',650,(100,200,1000,295),(150,40,30),70,'serifi','cap',''),
('S17 GO FROM THE FOOD',650,(250,280,850,330),(150,40,30),70,'sans','cap',''),
('S17 stomach box',650,(10,490,460,700),(150,45,30),60,'-','box',''),
('S18 BLOOD',705,(30,150,1060,365),(160,45,30),80,'serif','cap',''),
('S19 "gets brought"',785,(130,620,800,700),(250,250,250),60,'sans','asc+desc',''),
('S19 cells',785,(150,760,700,930),(245,215,150),70,'serifi','asc',''),
]
rows=[]
for n,f,(x0,y0,x1,y1),ink,tol,font,met,_ in T:
    im=cv2.imread(f'ref/f/{f:05d}.jpg');reg=im[y0:y1,x0:x1].astype(np.float32)
    d=np.sqrt(((reg-np.array(ink[::-1],np.float32))**2).sum(2));m=(d<tol).astype(np.uint8)
    nn,lab,st,_=cv2.connectedComponentsWithStats(m);keep=np.isin(lab,[i for i in range(1,nn) if st[i,4]>40])
    ys,xs=np.where(keep);bb=[int(x0+xs.min()),int(y0+ys.min()),int(x0+xs.max()+1),int(y0+ys.max()+1)];h=bb[3]-bb[1]
    col=np.median(reg[keep],axis=0)[::-1];hexc='#%02x%02x%02x'%tuple(int(c) for c in col)
    if font=='-': size=None
    else:
        k=M[font];den={'cap':k['cap'],'asc':k['asc'],'asc+desc':k['asc']+k['desc'],'x':k['xh']}.get(met)
        size=round(h/den,1) if den else None
    rows.append(dict(el=n,frame=f,bbox=bb,w=bb[2]-bb[0],h=h,cx=(bb[0]+bb[2])/2,font=font,size_px=size,size_pctW=round(size/10.8,2) if size else None,ink=hexc))
    print(f"{n:28s} bbox={bb} h={h:4d} cx={(bb[0]+bb[2])/2:6.1f} size={size} ink={hexc}")
json.dump(rows,open('spec/_tools/sizes.json','w'),indent=1)
