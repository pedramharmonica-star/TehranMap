import os
import json, math
from shapely.geometry import shape, Point
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
G=json.load(open(S+'data/georef.json')); geo=json.load(open(S+'data/geo.json'))
def px(x,y):
    lon=(x-G['bx'])/G['a']; Y=(G['by']-y)/G['a']
    return round(lon,4), round(math.degrees(2*math.atan(math.exp(math.radians(Y)))-math.pi/2),4)
P=[('قدس','Qods',px(205,475)),('شهریار','Shahriar',px(70,682)),('رضی‌آباد بالا','Raziabad',px(100,580)),('باغستان','Baghestan',px(258,700)),
('سعیدآباد','Saidabad',px(393,636)),('احمدآباد مستوفی','Ahmadabad Mostowfi',px(460,740)),('نصیرآباد','Nasirabad',px(507,843)),('صباشهر','Sabashahr',px(205,902)),
('نسیم‌شهر','Nasimshahr',px(315,958)),('اسلامشهر','Eslamshahr',px(503,1000)),('کهریزک','Kahrizak',px(833,1108)),('باقرشهر','Baqershahr',px(950,1055)),
('شهر ری','Rey',px(1033,828)),('خاورشهر','Khavar Shahr',px(1345,990)),('لواسان','Lavasan',px(1508,158)),('جاجرود','Jajrud',px(1700,392)),
('شهرک امید','Omid Town',px(1270,338)),('اورین','Ovrin',px(245,1015)),
('فردوسیه','Ferdosiyeh',px(82,842)),('آلارد','Alard',px(70,1118)),('صالحیه','Salehiye',px(405,1148)),('شهرک واوان','Vavan',px(493,1158)),
('قلعه‌نو','Qalehno',px(1233,1128)),('عباس‌آباد علاقه‌بند','Abbasabad',px(1393,1075)),('حصارامیر','Hesaramir',px(1693,1120)),('خاتون‌آباد','Khatunabad',px(1610,1170)),
('سولقان','Sulqan',px(590,160)),('افجه','Afjeh',px(1672,32)),('کمرد','Kamard',px(1800,325)),
('کرج','Karaj',(50.9915,35.8355)),('پردیس','Pardis',(51.8098,35.7417)),('بومهن','Bumehen',(51.8650,35.7300)),('ورامین','Varamin',(51.6466,35.3166)),
('شهر جدید اندیشه','Andisheh',(51.0230,35.6890)),('پاکدشت','Pakdasht',(51.6800,35.4670)),('رباط‌کریم','Robat Karim',(51.0830,35.4846))]
outer=shape(geo['outer']); dist=[(d['properties']['id'],shape(d['geometry'])) for d in geo['districts']]
res=[]
for fa,en,(lon,lat) in P:
    p=Point(lon,lat); z=3; did=None
    for i,g in dist:
        if g.contains(p): z=1; did=i
    if z!=1 and outer.contains(p): z=2
    res.append(dict(n=fa,lon=lon,lat=lat,z=z,d=did)); print(fa,en,lon,lat,z,did)
geo['places']=res
json.dump(geo,open(S+'data/geo.json','w'),ensure_ascii=False,separators=(',',':'))
