import os
import cv2, numpy as np
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
img=cv2.imread(S+'inputs/hand-drawn-boundary-v1.png')
b,g,r=[img[:,:,i].astype(int) for i in range(3)]
m=((b>140)&(g<70)&(r<70)&(b-g>100)).astype(np.uint8)*255
print('blue px',(m>0).sum())
k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
md=cv2.dilate(m,k,iterations=2)
h,w=md.shape
ff=md.copy(); mask=np.zeros((h+2,w+2),np.uint8)
for sd in [(w-5,h-5),(5,5),(60,1150),(20,900),(5,800),(1800,600),(900,30),(1000,1175),(300,1170)]:
    if ff[sd[1],sd[0]]==0: cv2.floodFill(ff,mask,sd,128)
inside=(ff==0).astype(np.uint8)*255
inside=cv2.bitwise_or(inside, md)  # include the line itself
# remove the stroke-only bits (tail) via opening
inside=cv2.morphologyEx(inside,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)))
n,lab,st,_=cv2.connectedComponentsWithStats(inside)
print('components',[(i,st[i,4]) for i in range(n)])
big=1+np.argmax(st[1:,4]); reg=(lab==big).astype(np.uint8)*255
cv2.imwrite(S+'data/region_mask.png',reg)
vis=img.copy(); vis[m>0]=(0,0,255); ov=vis.copy(); ov[reg>0]=(0,200,0)
cv2.imwrite(S+'region_vis.png',cv2.addWeighted(vis,0.6,ov,0.4,0))
