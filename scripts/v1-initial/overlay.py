import os
import pickle, json, math, cv2, numpy as np
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
P=pickle.load(open(S+'data/prep.pkl','rb')); G=json.load(open(S+'data/georef.json'))
def topx(lon,lat):
    Y=math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2)))
    return int(G['a']*lon+G['bx']), int(-G['a']*Y+G['by'])
img=cv2.imread(S+'inputs/hand-drawn-boundary-v1.png')
for f in P['feats']:
    pts=np.array([topx(*c) for c in f['geom'].exterior.coords],np.int32)
    cv2.polylines(img,[pts],True,(0,0,255),2)
cv2.imwrite(S+'overlay.png',img)
