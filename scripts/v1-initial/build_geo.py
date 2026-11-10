import cv2, json, math, pickle, numpy as np
from shapely.geometry import Polygon, mapping, LineString, MultiLineString, box
from shapely.ops import transform, unary_union
from pyproj import Transformer
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
G=json.load(open(S+'data/georef.json')); P=pickle.load(open(S+'data/prep.pkl','rb'))
toU=Transformer.from_crs(4326,32639,always_xy=True).transform
toG=Transformer.from_crs(32639,4326,always_xy=True).transform
def px2ll(x,y):
    lon=(x-G['bx'])/G['a']; Y=(G['by']-y)/G['a']
    lat=math.degrees(2*math.atan(math.exp(math.radians(Y)))-math.pi/2); return lon,lat
reg=cv2.imread(S+'data/region_mask.png',0)
cs,_=cv2.findContours(reg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
c=max(cs,key=cv2.contourArea)[:,0,:]
outer=Polygon([px2ll(x,y) for x,y in c])
# region mask included the dilated stroke (~10px outward); shrink back to the drawn line centre
outerU=transform(toU,outer).buffer(-350)
cityU=transform(toU,P['city'])
def chaikin(coords,n=4):
    pts=np.array(coords[:-1])
    for _ in range(n):
        q=0.75*pts+0.25*np.roll(pts,-1,0); r=0.25*pts+0.75*np.roll(pts,-1,0)
        pts=np.empty((len(q)*2,2)); pts[0::2]=q; pts[1::2]=r
    return np.vstack([pts,pts[:1]])
def smooth(polyU, simp=250, it=4):
    p=polyU.buffer(400).buffer(-800).buffer(400)   # open+close: drop wiggles, keep corridors
    p=p.simplify(simp)
    if p.geom_type!='Polygon': p=max(p.geoms,key=lambda g:g.area)
    return Polygon(chaikin(list(p.exterior.coords),it))
outerS=smooth(unary_union([outerU, cityU.buffer(700)]))
assert outerS.contains(cityU), 'outer must contain city'
print('outer km2', outerS.area/1e6, 'city km2', cityU.area/1e6, 'pts', len(outerS.exterior.coords))
# a gently smoothed city outline for the glow edge
cityS=cityU.simplify(30)
def r5(g):
    gj=mapping(transform(toG,g))
    def rnd(o):
        if isinstance(o,(list,tuple)):
            if len(o)==2 and all(isinstance(v,float) for v in o): return [round(o[0],5),round(o[1],5)]
            return [rnd(v) for v in o]
        return o
    gj['coordinates']=rnd(gj['coordinates']); return gj
names={1:'منطقه ۱',}
dists=[]
for f in P['feats']:
    gU=transform(toU,f['geom']).simplify(25)
    cen=transform(toG,gU.representative_point())
    dists.append(dict(type='Feature',properties=dict(id=f['id'],pop=f['pop'],area=f['area'],lx=round(cen.x,5),ly=round(cen.y,5)),geometry=r5(gU)))
dists.sort(key=lambda d:d['properties']['id'])
roads=[]
for t,n,s,g in P['roads']:
    if g.is_empty: continue
    gU=transform(toU,g).simplify(60)
    roads.append(dict(type='Feature',properties=dict(t=t,s=s),geometry=r5(gU)))
out=dict(districts=dists, city=r5(cityS), outer=r5(outerS), roads=roads)
json.dump(out,open(S+'data/geo.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print('bytes',os.path.getsize(S+'data/geo.json'))
# validation overlay
img=cv2.imread(S+'inputs/hand-drawn-boundary-v1.png')
def topx(lon,lat):
    Y=math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2))); return int(G['a']*lon+G['bx']), int(-G['a']*Y+G['by'])
for g,col in [(outerS,(0,140,255)),(cityS,(0,0,255))]:
    pts=np.array([topx(*toG(*xy)) for xy in g.exterior.coords],np.int32); cv2.polylines(img,[pts],True,col,3)
cv2.imwrite(S+'outer_check.png',img)
