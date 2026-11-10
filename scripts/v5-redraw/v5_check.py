import os
import json, math, pickle, numpy as np, cv2, sys
from pyproj import Transformer
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
G=json.load(open(S+'v5/georef.json')); D=pickle.load(open(S+'v5/build.pkl','rb'))
toG=Transformer.from_crs(32639,4326,always_xy=True).transform
R=math.pi/180
def px(x,y):
    lon,lat=toG(x,y); X=(lon+180)/360*256; Y=(1-math.log(math.tan(lat*R)+1/math.cos(lat*R))/math.pi)/2*256
    return int(G['a']*X+G['bx']), int(G['a']*Y+G['by'])
img=cv2.imread(S+'v5/draw.png')[...,:3].copy()
ov=img.copy()
pts=np.array([px(*c) for c in D['outer'].exterior.coords],np.int32)
cv2.polylines(ov,[pts],True,(30,30,230),5,cv2.LINE_AA)
nl=np.array([px(*c) for c in D['newline'].coords],np.int32)
img=cv2.addWeighted(img,0.55,ov,0.45,0)
cv2.polylines(img,[pts],True,(30,30,230),3,cv2.LINE_AA)
cv2.imwrite(S+'v5/new_check.png',img)
