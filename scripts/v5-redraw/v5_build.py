"""Rebuild the zone-2 (travel cost) outer boundary from the user's new hand-drawn line.
Smooth the line, snap stretches that run close to main roads or the Tehran city edge onto them,
then close it with the untouched north/east part of the old boundary."""
import os
import json, math, pickle, numpy as np, networkx as nx, osmium
from shapely.geometry import LineString, Point, Polygon, MultiLineString
from shapely.ops import transform, unary_union, linemerge, substring, nearest_points
from shapely.strtree import STRtree
from pyproj import Transformer

S = os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
toU = Transformer.from_crs(4326, 32639, always_xy=True).transform
toG = Transformer.from_crs(32639, 4326, always_xy=True).transform
geo = json.load(open(S + 'data/geo.json'))
blue = json.load(open(S + 'v5/blue.json'))

T = 320           # snap threshold (m): how far the drawn line may sit from a road and still mean "this road"
MINRUN = 700      # shortest stretch worth snapping (m)

def chaikin_open(pts, n=3):
    p = np.array(pts)
    for _ in range(n):
        q = 0.75 * p[:-1] + 0.25 * p[1:]; r = 0.25 * p[:-1] + 0.75 * p[1:]
        mid = np.empty((len(q) * 2, 2)); mid[0::2] = q; mid[1::2] = r
        p = np.vstack([p[:1], mid, p[-1:]])
    return p

# 1. drawn line -> metres, de-jittered
raw = LineString([toU(*c) for c in blue['ll']])
sm = LineString(chaikin_open(list(raw.simplify(30).coords), 3))
print('drawn length km', round(raw.length / 1000, 2), 'smoothed', round(sm.length / 1000, 2))

# 2. main-road graph straight from OSM (node ids keep junction topology exact)
MAIN = {'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link'}
env = sm.buffer(T * 3).bounds
gx0, gy0 = toG(env[0], env[1]); gx1, gy1 = toG(env[2], env[3])
Gr = nx.Graph(); NC = {}
class H(osmium.SimpleHandler):
    def way(self, w):
        if w.tags.get('highway') not in MAIN: return
        prev = None
        for n in w.nodes:
            if not n.location.valid(): prev = None; continue
            lon, lat = n.location.lon, n.location.lat
            if not (gx0 < lon < gx1 and gy0 < lat < gy1): prev = None; continue
            NC[n.ref] = toU(lon, lat)
            if prev is not None:
                a, b = NC[prev], NC[n.ref]; Gr.add_edge(prev, n.ref, length=math.dist(a, b))
            prev = n.ref
H().apply_file(S + 'data/osm/region.osm.pbf', locations=True, idx='flex_mem')
print('road graph', Gr.number_of_nodes(), Gr.number_of_edges())
nodes = list(Gr.nodes); npts = np.array([NC[n] for n in nodes])
# per-edge cost: real length, inflated the further the edge strays from the drawn line
for u, v, d in Gr.edges(data=True):
    mpt = Point((NC[u][0] + NC[v][0]) / 2, (NC[u][1] + NC[v][1]) / 2)
    off = sm.distance(mpt)
    d['w'] = d['length'] * (1 + (off / T) ** 2 * 3) if off < T * 1.6 else d['length'] * 1e4
segs = [LineString([NC[u], NC[v]]) for u, v in Gr.edges()]
tree = STRtree(segs)
cityU = transform(toU, Polygon(geo['city']['coordinates'][0]))
cityRing = LineString(cityU.exterior.coords)

# 3. classify sample points along the smoothed line
step = 40
dists = np.arange(0, sm.length, step); samples = [sm.interpolate(d) for d in dists]
def heading(line, d):
    a = line.interpolate(max(0, d - 60)); b = line.interpolate(min(line.length, d + 60))
    return math.atan2(b.y - a.y, b.x - a.x)
def ang(a, b):
    x = abs(a - b) % math.pi; return min(x, math.pi - x)
kind = []
for d, p in zip(dists, samples):
    h = heading(sm, d)
    k = None
    cd = cityRing.distance(p)
    if cd < T:
        q = cityRing.project(p); hc = heading(cityRing, q)
        if ang(h, hc) < math.radians(40): k = 'city'
    if k is None:
        idx = tree.query(p.buffer(T))
        best = None
        for i in idx:
            s = segs[i]; dd = s.distance(p)
            if dd > T: continue
            (x0, y0), (x1, y1) = s.coords
            if ang(h, math.atan2(y1 - y0, x1 - x0)) < math.radians(35) and (best is None or dd < best): best = dd
        if best is not None: k = 'road'
    kind.append(k)
# runs
runs = []; i = 0
while i < len(kind):
    j = i
    while j + 1 < len(kind) and kind[j + 1] == kind[i]: j += 1
    runs.append((kind[i], dists[i], dists[j])); i = j + 1
# absorb tiny gaps (<200 m) inside the same kind
merged = []
for r in runs:
    if merged and r[0] is None and r[2] - r[1] < 200 and len(merged) >= 1:
        merged.append(r); continue
    merged.append(r)
runs2 = []
for r in merged:
    if runs2 and r[0] is not None and len(runs2) >= 2 and runs2[-1][0] is None and runs2[-1][2] - runs2[-1][1] < 200 and runs2[-2][0] == r[0]:
        gap = runs2.pop(); prev = runs2.pop(); runs2.append((r[0], prev[1], r[2]))
    else:
        runs2.append(r)
print('runs:', [(k, round((b - a) / 1000, 2)) for k, a, b in runs2 if k])

# 4. replace snappable runs with the road path / city edge
def nearest_node(pt):
    i = int(np.argmin(((npts - np.array(pt)) ** 2).sum(1))); return nodes[i]
pieces = []; cursor = 0.0; report = []
for k, a, b in runs2:
    if k is None or b - a < MINRUN: continue
    seg_drawn = substring(sm, a, b)
    if k == 'road':
        na, nb = nearest_node(sm.interpolate(a).coords[0]), nearest_node(sm.interpolate(b).coords[0])
        try: path = nx.shortest_path(Gr, na, nb, weight='w')
        except nx.NetworkXNoPath: continue
        rl = LineString([NC[n] for n in path])
        if rl.length < 50 or rl.length > seg_drawn.length * 1.35 or rl.hausdorff_distance(seg_drawn) > T * 1.4: continue
        rep = rl
    else:
        pa, pb = cityRing.project(sm.interpolate(a)), cityRing.project(sm.interpolate(b))
        lo, hi = sorted((pa, pb)); arc = substring(cityRing, lo, hi)
        if arc.length > cityRing.length / 2: continue
        if pa > pb: arc = LineString(list(arc.coords)[::-1])
        if arc.hausdorff_distance(seg_drawn) > T * 1.4: continue
        rep = arc
    if a > cursor: pieces.append(substring(sm, cursor, a))
    pieces.append(rep); cursor = b; report.append((k, round((b - a) / 1000, 2)))
pieces.append(substring(sm, cursor, sm.length))
coords = []
for pc in pieces:
    c = list(pc.coords)
    if coords and math.dist(coords[-1], c[0]) < 1: c = c[1:]
    coords += c
newline = LineString(coords)
# smooth the joins between snapped and free-drawn stretches: drop hairpins, then round gently
def despike(cs, lim=145):
    changed=True
    while changed and len(cs)>3:
        changed=False; out=[cs[0]]
        for i in range(1,len(cs)-1):
            a,b,c=np.array(out[-1]),np.array(cs[i]),np.array(cs[i+1])
            v1,v2=b-a,c-b; n1,n2=np.linalg.norm(v1),np.linalg.norm(v2)
            if n1<1e-6 or n2<1e-6: changed=True; continue
            turn=math.degrees(math.acos(max(-1,min(1,float(v1@v2/(n1*n2))))))
            if turn>lim: changed=True; continue
            out.append(cs[i])
        out.append(cs[-1]); cs=out
    return cs
cs=despike(list(newline.simplify(12).coords))
newline = LineString(chaikin_open(cs, 2))
print('snapped stretches:', report, 'snapped km', round(sum(r[1] for r in report), 2), 'of', round(sm.length / 1000, 2))

# 5. close with the kept (north/east) arc of the old boundary
oldU = transform(toU, Polygon(geo['outer']['coordinates'][0]))
ring = LineString(oldU.exterior.coords)
p0, p1 = Point(newline.coords[0]), Point(newline.coords[-1])
d0, d1 = ring.project(p0), ring.project(p1)
L = ring.length
def arc(dfrom, dto):  # walk the ring forward from dfrom to dto
    if dto >= dfrom: return list(substring(ring, dfrom, dto).coords)
    return list(substring(ring, dfrom, L).coords) + list(substring(ring, 0, dto).coords)[1:]
lav = Point(toU(51.6287, 35.8164))  # Lavasan, far north-east, must stay inside
cands = []
for a_ in (arc(d1, d0), arc(d0, d1)[::-1]):
    poly = Polygon(list(newline.coords) + a_).buffer(0)
    cands.append(poly)
for c in cands: print('cand', c.geom_type, round(c.area/1e6,1), c.contains(lav), round(c.intersection(cityU).area/1e6,1), newline.is_simple)
keep = max(cands, key=lambda p: (p.contains(lav), p.intersection(cityU).area))
outer = unary_union([keep, cityU])
outer = outer.buffer(120, join_style=2).buffer(-120, join_style=2)  # weld slivers along district edges
print('union', outer.geom_type, [round(g.area/1e6,1) for g in getattr(outer,'geoms',[outer])])
if outer.geom_type != 'Polygon': outer = max(outer.geoms, key=lambda g: g.area)
outer = Polygon(outer.exterior).simplify(5)
outer = unary_union([outer, cityU]); outer = Polygon(max(getattr(outer,'geoms',[outer]),key=lambda g:g.area).exterior)
print('city outside by m:', round(cityU.difference(outer).area,1)); assert outer.buffer(12).contains(cityU), 'city must stay inside'
print('old km2', round(oldU.area / 1e6, 1), 'new km2', round(outer.area / 1e6, 1))
pickle.dump(dict(outer=outer, newline=newline, sm=sm, raw=raw), open(S + 'v5/build.pkl', 'wb'))
