import cv2,numpy as np,sys,glob
src,out,step,start,end,cols=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])
fs=sorted(glob.glob(src+'/*'))
tiles=[]
for i in range(start,min(end,len(fs)+1),step):
    im=cv2.imread(fs[i-1]); im=cv2.resize(im,(216,384))
    cv2.putText(im,str(i),(5,25),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)
    tiles.append(im)
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[r:r+cols]) for r in range(0,len(tiles),cols)]
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,80])
