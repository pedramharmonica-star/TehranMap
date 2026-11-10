import os
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
t=open(S+'src/template.html').read()
css=open(S+'data/lf/package/dist/leaflet.css').read()
geo=open(S+'data/geo.json').read()
out=t.replace('/*__LFCSS__*/',css).replace('/*__GEO__*/null',geo)
open(S+'payamgostar-support-map.html','w').write(out)
cdn='<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>'
test=out.replace(cdn,'<script>'+open(S+'data/lf/package/dist/leaflet.js').read()+'</script>')
open(S+'test.html','w').write('<!doctype html><html dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+test.split('<div class="app">')[0]+'</head><body><div class="app">'+test.split('<div class="app">')[1]+'</body></html>')
print(len(out))
