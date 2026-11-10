import os
import json, shapefile, sys
from shapely.geometry import shape, box, mapping, Polygon
from shapely.ops import transform, unary_union
from pyproj import Transformer
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
D=S+'data/'
tr=Transformer.from_crs(32639,4326,always_xy=True).transform
r=shapefile.Reader(D+'shp/shp/tehran')
feats=[]
for sr in r.shapeRecords():
    g=transform(tr, shape(sr.shape.__geo_interface__)).buffer(0)
    rec=sr.record.as_dict()
    feats.append(dict(id=int(rec['Region_ID']), pop=rec['pop'], area=round(rec['Area']/100,2), geom=g))
city=unary_union([f['geom'] for f in feats]).buffer(0.0003).buffer(-0.0003)
print('city', city.geom_type, city.bounds, city.area)
BB=box(50.75,35.30,51.95,36.0)
roads=[]
for f in json.load(open(D+'ne_10m_roads.geojson'))['features']:
    g=shape(f['geometry'])
    if not g.intersects(BB): continue
    p=f['properties']; roads.append((p.get('type'),p.get('name'),p.get('scalerank'), g.intersection(BB)))
print('roads',len(roads)); 
for t,n,s,_ in roads: print(' ',t,n,s)
pl=[]
for f in json.load(open(D+'ne_10m_populated_places_simple.geojson'))['features']:
    g=shape(f['geometry'])
    if BB.contains(g): pl.append((f['properties']['name'],f['properties'].get('scalerank'),g.x,g.y))
print('places',pl)
ua=[shape(f['geometry']).intersection(BB) for f in json.load(open(D+'ne_10m_urban_areas.geojson'))['features'] if shape(f['geometry']).intersects(BB)]
print('urban',len(ua))
import pickle; pickle.dump(dict(feats=feats,city=city,roads=roads,ua=ua),open(D+'prep.pkl','wb'))
