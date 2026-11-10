import os
import numpy as np, math, json
def merc(lat,lon): return lon, math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2)))
cp=[((1022,192),35.8046,51.4336),((205,475),35.7214,51.1090),((70,668),35.6596,51.0592),((503,985),35.5446,51.2353),
((1033,815),35.5880,51.4360),((950,1045),35.5320,51.4040),((833,1105),35.5140,51.3610),((1508,145),35.8236,51.6278),((987,568),35.6800,51.4204)]
# px = a*X + bx ; py = -a*Y + by
A=[];b=[]
for (px,py),lat,lon in cp:
    X,Y=merc(lat,lon); A.append([X,1,0]); b.append(px); A.append([-Y,0,1]); b.append(py)
sol,res,_,_=np.linalg.lstsq(np.array(A),np.array(b),rcond=None)
a,bx,by=sol; print('a',a,'bx',bx,'by',by)
for (px,py),lat,lon in cp:
    X,Y=merc(lat,lon); print((px,py), round(a*X+bx-px,1), round(-a*Y+by-py,1))
json.dump(dict(a=a,bx=bx,by=by),open(''+os.environ.get('TEHRANMAP_WORK','work').rstrip('/')+'/data/georef.json','w'))
