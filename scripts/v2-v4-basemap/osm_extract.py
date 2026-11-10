"""Extract a compact basemap (roads, water, green, places) from an OSM .pbf for the support map.
usage: python3 -I osm_extract.py <file.osm.pbf> <outdir>"""
import sys, json, math, osmium
from shapely.geometry import LineString, Polygon, box, MultiPolygon
from shapely import wkb as swkb

PBF, OUT = sys.argv[1], sys.argv[2]
W, S, E, N = 50.95, 35.42, 51.85, 35.90
Q = 100000  # 1e-5 deg ~ 1 m
BB = box(W, S, E, N)
KX = 111320 * math.cos(math.radians(35.7)); KY = 110540  # m per deg

ROAD = {'motorway': 'motorway', 'motorway_link': 'mlink', 'trunk': 'trunk', 'trunk_link': 'mlink',
        'primary': 'primary', 'primary_link': 'link', 'secondary': 'secondary', 'secondary_link': 'link',
        'tertiary': 'tertiary', 'tertiary_link': 'link', 'residential': 'minor', 'unclassified': 'minor',
        'living_street': 'minor', 'pedestrian': 'minor'}
SIMP = {'motorway': 6, 'trunk': 6, 'mlink': 4, 'primary': 5, 'secondary': 5, 'tertiary': 4, 'link': 4, 'minor': 3,
        'rail': 6, 'river': 6}
GREEN = {('leisure', 'park'), ('landuse', 'forest'), ('natural', 'wood'), ('landuse', 'grass'), ('leisure', 'garden'),
         ('landuse', 'recreation_ground'), ('landuse', 'orchard'), ('landuse', 'cemetery')}
fab = osmium.geom.WKBFactory()

def to_m(g):  # shapely in local metres for simplify
    from shapely.affinity import scale, translate
    return scale(translate(g, -W, -S), KX, KY, origin=(0, 0))
def from_m(g):
    from shapely.affinity import scale, translate
    return translate(scale(g, 1 / KX, 1 / KY, origin=(0, 0)), W, S)
def enc(coords):
    out = []; px = py = 0
    for x, y in coords:
        ix, iy = round((x - W) * Q), round((y - S) * Q)
        out += [ix - px, iy - py]; px, py = ix, iy
    return out
def lines_of(g):
    if g.is_empty: return []
    if g.geom_type == 'LineString': return [g]
    if hasattr(g, 'geoms'): return [x for x in g.geoms if x.geom_type == 'LineString']
    return []
def polys_of(g):
    if g.is_empty: return []
    if g.geom_type == 'Polygon': return [g]
    if hasattr(g, 'geoms'): return [x for x in g.geoms if x.geom_type == 'Polygon']
    return []

layers = {k: [] for k in ['motorway', 'trunk', 'mlink', 'primary', 'secondary', 'tertiary', 'link', 'minor', 'rail', 'river',
                          'water', 'green', 'airport']}
names = {k: [] for k in layers}
places = []

class H(osmium.SimpleHandler):
    def node(self, n):
        p = n.tags.get('place')
        if p in ('city', 'town', 'suburb', 'neighbourhood', 'quarter', 'village') and (W < n.location.lon < E and S < n.location.lat < N):
            nm = n.tags.get('name:fa') or n.tags.get('name')
            if nm: places.append(dict(t=nm, k=p, x=round(n.location.lon, 5), y=round(n.location.lat, 5)))
    def way(self, w):
        t = w.tags; hw = t.get('highway'); cls = None
        if hw in ROAD: cls = ROAD[hw]
        elif t.get('railway') == 'rail' and t.get('tunnel') != 'yes': cls = 'rail'
        elif t.get('waterway') in ('river', 'canal'): cls = 'river'
        if not cls: return
        if t.get('tunnel') == 'yes' and cls in ('minor',): return
        try: g = swkb.loads(fab.create_linestring(w), hex=True)
        except Exception: return
        if not g.intersects(BB): return
        g = g.intersection(BB)
        nm = t.get('name:fa') or t.get('name') or ''
        for l in lines_of(from_m(to_m(g).simplify(SIMP[cls]))):
            if len(l.coords) < 2: continue
            layers[cls].append(enc(l.coords)); names[cls].append(nm)
    def area(self, a):
        t = a.tags; kind = None
        if t.get('natural') == 'water' or t.get('landuse') == 'reservoir' or t.get('water'): kind = 'water'
        elif t.get('aeroway') == 'aerodrome': kind = 'airport'
        else:
            for k, v in GREEN:
                if t.get(k) == v: kind = 'green'; break
        if not kind: return
        try: g = swkb.loads(fab.create_multipolygon(a), hex=True)
        except Exception: return
        if not g.intersects(BB): return
        g = from_m(to_m(g.intersection(BB)).simplify(5).buffer(0))
        for p in polys_of(g):
            if to_m(p).area < (2500 if kind == 'green' else 1500): continue
            layers[kind].append([enc(p.exterior.coords)] + [enc(r.coords) for r in p.interiors])
            names[kind].append(t.get('name:fa') or t.get('name') or '')

H().apply_file(PBF, locations=True, idx='flex_mem')
base = {k: v for k, v in layers.items() if k != 'minor'}
meta = dict(bbox=[W, S, E, N], q=Q)
json.dump(dict(meta, layers=base, names={k: names[k] for k in base}, places=places),
          open(OUT + '/base.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(dict(meta, layers={'minor': layers['minor']}, names={'minor': names['minor']}),
          open(OUT + '/minor.json', 'w'), ensure_ascii=False, separators=(',', ':'))
for k, v in layers.items(): print(k, len(v))
print('places', len(places))
