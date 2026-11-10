import os
import json, math, numpy as np, cv2, networkx as nx
from skimage.morphology import skeletonize
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
img=cv2.imread(S+'v5/draw.png')[...,:3].astype(int); B,G,R=img[...,0],img[...,1],img[...,2]
m=(B>150)&(G<80)&(R<80)&(B-G>100)
m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))>0
n,lab,st,_=cv2.connectedComponentsWithStats(m.astype(np.uint8))
print('components',sorted(st[1:,4])[-5:])
big=1+np.argmax(st[1:,4]); m=lab==big
sk=skeletonize(m)
ys,xs=np.nonzero(sk); idx={(y,x):i for i,(y,x) in enumerate(zip(ys,xs))}
Gr=nx.Graph()
for (y,x),i in idx.items():
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dy or dx) and (y+dy,x+dx) in idx: Gr.add_edge(i,idx[(y+dy,x+dx)],weight=math.hypot(dx,dy))
ends=[v for v in Gr.nodes if Gr.degree(v)==1]
print('endpoints',len(ends),[ (int(xs[e]),int(ys[e])) for e in ends])
# the true ends are the pair with the longest geodesic distance
best=None
for e in ends:
    d=nx.single_source_dijkstra_path_length(Gr,e)
    f=max(ends,key=lambda v:d.get(v,-1))
    if best is None or d[f]>best[0]: best=(d[f],e,f)
L,a,b=best; path=nx.dijkstra_path(Gr,a,b)
pts=[(int(xs[i]),int(ys[i])) for i in path]
# orient: start at the top-left end
if pts[0][1]>pts[-1][1] and pts[0][0]>pts[-1][0]: pts=pts[::-1]
if math.hypot(pts[0][0]-255,pts[0][1]-120)>math.hypot(pts[-1][0]-255,pts[-1][1]-120): pts=pts[::-1]
print('path px',len(pts),'start',pts[0],'end',pts[-1],'len',round(L))
G0=json.load(open(S+'v5/georef.json'))
def ll(x,y):
    X=(x-G0['bx'])/G0['a']; Y=(y-G0['by'])/G0['a']
    lon=X/256*360-180; lat=math.degrees(math.atan(math.sinh(math.pi*(1-2*Y/256)))); return lon,lat
json.dump(dict(px=pts,ll=[ll(*p) for p in pts]),open(S+'v5/blue.json','w'))
vis=cv2.imread(S+'v5/draw.png')[...,:3].copy()
cv2.polylines(vis,[np.array(pts,np.int32)],False,(0,0,255),3)
cv2.circle(vis,pts[0],10,(0,200,0),-1); cv2.circle(vis,pts[-1],10,(0,0,0),-1)
cv2.imwrite(S+'v5/blue_check.png',vis)
