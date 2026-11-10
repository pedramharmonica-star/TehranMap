#!/usr/bin/env bash
# Builds the "work" folder the scripts expect (TEHRANMAP_WORK), from the files kept in this repo.
# usage: bash tools/setup_work.sh [work-dir]   (default: ./work)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
W="${1:-$REPO/work}"
mkdir -p "$W"/{data/shp,data/osm,data/lf,out2,logo,src,v5,inputs,pub,out}
unzip -oq "$REPO/data/districts/tehran-22-districts-shp.zip" -d "$W/data/shp"
cp "$REPO/data/geo.json" "$W/data/geo.json"
cp "$REPO/data/georef/v1-georef.json" "$W/data/georef.json"
cp "$REPO/data/georef/v1-region-mask.png" "$W/data/region_mask.png"
cp "$REPO/data/osm/tehran-region.osm.pbf" "$W/data/osm/region.osm.pbf"
cp "$REPO/data/basemap/"*.json.gz "$W/out2/"
cp "$REPO/data/logo/payamgostar-logo.svg" "$W/logo/logo.svg"
cp "$REPO/src/template.html" "$W/src/template2.html"
cp "$REPO/src/template-v1.html" "$W/src/template.html"
cp "$REPO/data/georef/v5-georef.json" "$W/v5/georef.json"
cp "$REPO/data/georef/v5-blue-line.json" "$W/v5/blue.json"
cp "$REPO/images/inputs/06-hand-drawn-boundary-v5.png" "$W/v5/draw.png"
cp "$REPO/images/inputs/03-hand-drawn-boundary-v1.png" "$W/inputs/hand-drawn-boundary-v1.png"
cp "$REPO/images/brand/logo-dark-slogan.png" "$W/inputs/logo-dark-slogan.png"
# the React app lives in the repo; the build scripts address it as work/supportmap
ln -sfn "$REPO/app" "$W/supportmap"
# Leaflet stylesheet (inlined into the v1 page)
if [ ! -f "$W/data/lf/package/dist/leaflet.css" ]; then
  (cd "$W/data" && npm pack leaflet@1.9.4 -q >/dev/null && tar -xzf leaflet-1.9.4.tgz -C lf)
fi
echo "work folder ready: $W   (export TEHRANMAP_WORK=$W)"
