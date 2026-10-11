"""Private reference ledger and local checkpoint review page."""
from pathlib import Path
from datetime import datetime, timezone
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
refs=ROOT/'references/streetview-capture/extension-v41'
sources=[('osm-original.xml','https://api.openstreetmap.org/api/0.6/map?bbox=-1.083,52.691,-1.071,52.700','© OpenStreetMap contributors; ODbL; mapped geometry, not imagery'),('national-rail-original.pdf','https://assets.nationalrail.co.uk/e8xgegruud3g/sysOnwardTravelMap/4d251dc06b0548629e38ae47099f338d/Syston__SYS_.pdf','National Rail/EMR; April 2024 map; OS and OSM attribution retained; private reference'),('midland-official-exterior.jpg','https://images.cdn.inapub.co.uk/photos/79a507042a64404ba121dd2f62fa8105.jpg','Linked from Midland Railway official website; photo date and redistribution rights unverified; private visual reference only')]
ledger=[]
for name,url,credit in sources:
 p=refs/name;ledger.append({'file':name,'source_url':url,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'credit':credit,'edits':'None','retrieval_date':'2026-10-10'})
(refs/'manifest.json').write_text(json.dumps({'references':ledger,'derivatives':[{'file':'build/syston-local-map-detail.png','source':'national-rail-original.pdf','method':'PyMuPDF crop Rect(935,420,1730,1210), matrix 3x, source unchanged'}],'google_satellite_verified':False,'house_visually_identified':False},indent=2)+'\n')
dest=ROOT/'recon/v41'
check=json.loads((dest/'route-checks.json').read_text());surfaces=json.loads((dest/'surface-fix.json').read_text())
rows=[]
for slug,title in [('01_route_overview','Whole route'),('02_station_holmdale','Station and Holmdale junction'),('03_taraj_seam','Connection beyond Taraj'),('04_holmdale','Along Holmdale')]:
 rows.append(f'<section><h2>{title}</h2><div class="pair">'+''.join(f'<figure><img src="{slug}_{stage}.png"><figcaption>{stage.title()}</figcaption></figure>' for stage in ('before','after'))+'</div></section>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Extension v41 — provisional route review</title><style>body{font:16px system-ui;background:#15202b;color:#e7edf2;margin:0 auto;padding:28px;max-width:1500px}p{max-width:1000px;line-height:1.6}.status{border-left:4px solid #efb657;padding:14px;background:#273544}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}img{width:100%;background:#34414e}figcaption{padding:8px}section{margin:32px 0}a{color:#a9d9ff}@media(max-width:800px){.pair{grid-template-columns:1fr}}</style><h1>Melton / station / Holmdale — v41</h1><p class="status">Provisional road blockout. Google satellite comparison and number 29 visual identification remain pending. This is not the completed extension.</p>'''
page+=f'<p>Saved editable checkpoint: pharmacie-extension-route-v41.blend. Prior v40 retained. {surfaces["active_extension_meshes"]} active new meshes after joining the surfaces. {check["clearance_rays"]:,} selected Blender clearance rays and {check["floor_samples"]:,} ground-support samples pass. BO3 unchanged.</p>'
page+='<p>Alignment follows OpenStreetMap road geometry, rigidly tied to the existing gameplay frame. Widths, heights, terrain, perimeter walls, centre markings and final station walkway are estimates. Building masses follow mapped footprints; detailed architecture is pending. Material-colour Workbench previews show shape, not final texture or lighting.</p>'
page+=''.join(rows)+'<p><a href="../../docs/EXTENSION_ROUTE_V41.md">Implementation, evidence and limits</a> · <a href="extension-route.json">Mapped route and frame</a> · <a href="route-checks.json">Blender checks</a></p></html>'
(dest/'index.html').write_text(page,encoding='utf-8')
print(json.dumps({'reference_files':len(ledger),'review':str(dest/'index.html'),'active_new_meshes':surfaces['active_extension_meshes']}))
