#!/usr/bin/env bash
# Full build of the current map: template -> React app -> single HTML (+ embedded street data) -> WordPress zip.
# Needs: python3 (numpy, shapely, pyproj, osmium for data steps), node 18+, pnpm.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export TEHRANMAP_WORK="${TEHRANMAP_WORK:-$REPO/work}"
[ -d "$TEHRANMAP_WORK" ] || bash "$REPO/tools/setup_work.sh" "$TEHRANMAP_WORK"
cp "$REPO/data/geo.json" "$TEHRANMAP_WORK/data/geo.json"
cp "$REPO/data/geo.json" "$REPO/app/src/geo.json"
# 1. template.html -> app/src (mapEngine.ts, map.css, App.tsx) with the logo inlined
python3 "$REPO/scripts/build/port.py"
# 2. bundle the React app into one HTML file
cd "$REPO/app"
pnpm install --silent
pnpm add -D parcel @parcel/config-default parcel-resolver-tspaths html-inline >/dev/null
rm -rf dist bundle.html
pnpm exec parcel build index.html --dist-dir dist --no-source-maps
pnpm exec html-inline dist/index.html > bundle.html
# 3. add fonts + embed gzip/base64 street data -> pub/payamgostar-support-map.html
python3 "$REPO/scripts/build/finalize.py"
cp "$TEHRANMAP_WORK/pub/payamgostar-support-map.html" "$REPO/dist/payamgostar-support-map.html"
# 4. WordPress plugin: wrap the page as a full document and zip
python3 - "$REPO" <<'PY'
import sys
R=sys.argv[1]
body=open(R+'/dist/payamgostar-support-map.html').read()
doc=('<!doctype html><html lang="fa"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
     '<meta name="robots" content="noindex"><style>html,body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style></head><body>'+body+'</body></html>')
open(R+'/dist/wordpress/payamgostar-support-map/assets/map.html','w').write(doc)
PY
VER=$(grep -m1 "Version:" "$REPO/dist/wordpress/payamgostar-support-map/payamgostar-support-map.php" | awk '{print $NF}')
cd "$REPO/dist/wordpress" && rm -f payamgostar-support-map-*.zip && zip -rq9 "payamgostar-support-map-$VER.zip" payamgostar-support-map
echo "done: dist/payamgostar-support-map.html and dist/wordpress/payamgostar-support-map-$VER.zip"
