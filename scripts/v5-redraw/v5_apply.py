"""Write the rebuilt yellow boundary (v5/build.pkl) into data geo.json and recompute each town's zone.
Prints every town whose zone changes, for sales to confirm."""
import os, json, pickle
from shapely.geometry import shape, Point
from shapely.ops import transform
from pyproj import Transformer
S = os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
toG = Transformer.from_crs(32639, 4326, always_xy=True).transform
geo = json.load(open(S + 'data/geo.json')); D = pickle.load(open(S + 'v5/build.pkl', 'rb'))
o = transform(toG, D['outer'])
geo['outer'] = {'type': 'Polygon', 'coordinates': [[[round(x, 5), round(y, 5)] for x, y in o.exterior.coords]]}
outer = shape(geo['outer']); dist = [(d['properties']['id'], shape(d['geometry'])) for d in geo['districts']]
for p in geo['places']:
    pt = Point(p['lon'], p['lat']); z = 3; did = None
    for i, g in dist:
        if g.contains(pt): z = 1; did = i
    if z != 1 and outer.contains(pt): z = 2
    if z != p['z']: print('zone change:', p['n'], p['z'], '->', z)
    p['z'] = z; p['d'] = did
json.dump(geo, open(S + 'data/geo.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('outer points', len(o.exterior.coords), '-> copy work/data/geo.json to data/geo.json, then run tools/build.sh')
