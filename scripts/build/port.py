import os
import re
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
t=open(S+'src/template2.html').read()
css=re.findall(r'<style>(.*?)</style>',t,re.S)[1]
markup=t.split('</style>\n',2)[2].split('<script src=')[0]
script=t.split('const GEO = /*__GEO__*/null;\n(function(){')[1].rsplit('})();',1)[0]
rep=[("?` · منطقه ${fa(c.d)}`:''","?`، منطقه ${fa(c.d)}`:''"),
("OpenStreetMap</a> · مرز مناطق","OpenStreetMap</a>؛ مرز مناطق")]
for a,b in rep:
    assert a in script, a; script=script.replace(a,b)
script=script.replace('__LOGO_SVG__',open(S+'logo/logo.svg').read().replace("'","\\'").strip())
open(S+'supportmap/src/mapEngine.ts','w').write("// @ts-nocheck\nimport L from 'leaflet';\nexport function initMap(GEO){\n"+script+"\n}\n")
open(S+'supportmap/src/map.css','w').write(css)
jsx=markup.replace('class=','className=')
jsx=re.sub(r'style="--rc:var\(--z(\d)\)"',lambda m:'style={{"--rc":"var(--z%s)"} as React.CSSProperties}'%m.group(1),jsx)
jsx=re.sub(r'(<input[^>]*?)>',r'\1 />',jsx); jsx=jsx.replace(' hidden>',' hidden>').replace('autocomplete=','autoComplete=')
jsx=jsx.replace('<span>بیرون از خط زرد · ایاب و ذهاب و حق مأموریت</span>','<span>بیرون از خط زرد، با هزینه‌ی ایاب و ذهاب و حق مأموریت</span>')
app="""import { useEffect, useRef } from 'react'
import type React from 'react'
import 'leaflet/dist/leaflet.css'
import './map.css'
import GEO from './geo.json'
import { initMap } from './mapEngine'

export default function App() {
  const done = useRef(false)
  useEffect(() => { if (done.current) return; done.current = true; initMap(GEO) }, [])
  return (<>
"""+jsx+"""  </>)
}
"""
open(S+'supportmap/src/App.tsx','w').write(app)
