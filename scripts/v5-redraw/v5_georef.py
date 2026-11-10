import os
import json, math, numpy as np, cv2
from scipy import ndimage, optimize
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
img=cv2.imread(S+'v5/draw.png'); H,W=img.shape[:2]
geo=json.load(open(S+'data/geo.json'))
R=math.pi/180
mx=lambda lon:(lon+180)/360*256
my=lambda lat:(1-math.log(math.tan(lat*R)+1/math.cos(lat*R))/math.pi)/2*256
P={p['n']:(p['lon'],p['lat']) for p in geo['places']}
cp=[('قدس',288,338),('رضی‌آباد بالا',136,489),('شهریار',94,637),('باغستان',363,661),('سعیدآباد',557,570),('احمدآباد مستوفی',653,718),
('نصیرآباد',720,866),('صباشهر',287,951),('نسیم‌شهر',446,1031),('اسلامشهر',715,1091),('کهریزک',1188,1246),('باقرشهر',1356,1170),
('قلعه‌نو',1762,1275),('فردوسیه',110,864),('اورین',345,1113)]
A=[];b=[]
for n,px,py in cp:
    lon,lat=P[n]; A.append([mx(lon),1,0]); b.append(px); A.append([my(lat),0,1]); b.append(py)
sol=np.linalg.lstsq(np.array(A),np.array(b),rcond=None)[0]; print('init',sol)
res=[(n,round(sol[0]*mx(P[n][0])+sol[1]-px,1),round(sol[0]*my(P[n][1])+sol[2]-py,1)) for n,px,py in cp]; print(res)
# refine: chamfer against yellow edge + green city edge
bgr=img[...,:3].astype(int); B,G,Rr=bgr[...,0],bgr[...,1],bgr[...,2]
yellow=(Rr>220)&(G>160)&(G<200)&(B<60)
green=(G>120)&(Rr<60)&(B>80)&(B<130)&(G-Rr>80)
print('mask px',yellow.sum(),green.sum())
dty=ndimage.distance_transform_edt(~yellow); dtg=ndimage.distance_transform_edt(~green)
def ring_px(coords,s): return np.array([[s[0]*mx(x)+s[1], s[0]*my(y)+s[2]] for x,y in coords])
outer=geo['outer']['coordinates'][0]; city=geo['city']['coordinates'][0]
def cost(s):
    c=0;n=0
    for ring,dt in [(outer,dty),(city,dtg)]:
        p=ring_px(ring,s); m=(p[:,0]>2)&(p[:,0]<W-3)&(p[:,1]>2)&(p[:,1]<H-3)
        # ignore the area under the cards/tooltip/popup (right side & popup box)
        m&=~((p[:,0]>1850))&~((p[:,0]>1210)&(p[:,0]<1670)&(p[:,1]>380)&(p[:,1]<600))
        v=dt[p[m,1].astype(int),p[m,0].astype(int)]; v=np.minimum(v,15); c+=v.sum(); n+=m.sum()
    return c/max(n,1)
print('cost init',cost(sol))
s=sol  # label fit is sub-pixel; skip refinement
_r=None and optimize.minimize(cost,sol,method='Nelder-Mead',options={'xatol':1e-3,'fatol':1e-4,'maxiter':4000,'initial_simplex':[sol,sol*[1.003,1,1]+[0,0,0],sol+[0,8,0],sol+[0,0,8]]})
print('cost',cost(s))
json.dump(dict(a=s[0],bx=s[1],by=s[2]),open(S+'v5/georef.json','w'))
vis=img[...,:3].copy()
for ring,col in [(outer,(0,0,255)),(city,(255,0,255))]:
    cv2.polylines(vis,[ring_px(ring,s).astype(np.int32)],True,col,2)
cv2.imwrite(S+'v5/georef_check.png',vis)
