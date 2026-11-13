import cv2, numpy as np, glob, sys
n = sys.argv[1]
f = sorted(glob.glob(f'an/s_{n}_*.png'))
ims = [cv2.resize(cv2.imread(x), (200, 356))[0:210] for x in f]
while len(ims) % 6:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite(f'an/strip_{n}.jpg', np.vstack([np.hstack(ims[i:i + 6]) for i in range(0, len(ims), 6)]))
