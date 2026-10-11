"""Local matched review and provenance for the Midland/station reference pass."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v42'
r=json.loads((dest/'validation.json').read_text());q=json.loads((dest/'route-checks.json').read_text())
body='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Midland exterior v42</title><style>body{font:16px system-ui;background:#14212d;color:#e9eef2;max-width:1500px;margin:auto;padding:28px}p{line-height:1.6;max-width:1050px}.status{border-left:4px solid #e8b453;background:#253541;padding:14px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}img{width:100%}figcaption{padding:8px}section{margin:30px 0}a{color:#a9dbff}@media(max-width:800px){.pair{grid-template-columns:1fr}}</style><h1>Midland Railway exterior — v42</h1><p class="status">Extension in progress. Google satellite verification and number 29 remain pending. This pub assembly can move independently of the provisional roads.</p>'''
body+=f'<p>{r["new_meshes"]} new closed meshes and {r["new_text_objects"]} text objects, following the reviewed official exterior photo. Blue/white walls, sash windows, entrances, fascia, roof/chimneys, deck, picnic furniture and umbrella. Geometry dimensions and unseen rear wing remain estimates. Closed static exterior only.</p>'
body+=f'<p>{q["clearance_rays"]:,} selected Blender clearance rays and {q["floor_samples"]:,} ground-support samples still pass. Prior pub/Taraj and road placement retained. BO3 unchanged. Workbench material-colour previews show geometry, not final textured lighting.</p>'
for slug,title in [('01_front','Frontage'),('02_oblique','Oblique view'),('03_roof','Roof and side wing')]:
 body+=f'<section><h2>{title}</h2><div class="pair">'+''.join(f'<figure><img src="{slug}_{stage}.png"><figcaption>{stage.title()}</figcaption></figure>' for stage in ('before','after'))+'</div></section>'
body+='<p><a href="../../docs/MIDLAND_FRONTAGE_V42.md">Evidence and implementation limits</a> · <a href="../v41/index.html">Route blockout review</a> · <a href="validation.json">Mesh checks</a> · <a href="route-checks.json">Blender route samples</a></p></html>'
(dest/'index.html').write_text(body,encoding='utf-8')
refs=ROOT/'references/streetview-capture/extension-v41';p=refs/'manifest.json';manifest=json.loads(p.read_text())
new=[('station-official-layout.jpg','https://images.nationalrail.co.uk/e8xgegruud3g/7Lr38CYAchk5qmoxB9oKmG/f7544cede309d784e2e3f059ebfd4ec4/Syston_station_map.jpg','National Rail; copyrighted schematic, private reference only',None),('station-geograph-8028555.jpg','https://www.geograph.org.uk/photo/8028555','Syston Station © David Howard, CC BY-SA 2.0 https://creativecommons.org/licenses/by-sa/2.0/','2025-04-20'),('station-geograph-3779706-view.jpg','https://www.geograph.org.uk/photo/3779706','Syston railway station, Leicestershire © Nigel Thompson, CC BY-SA 2.0 https://creativecommons.org/licenses/by-sa/2.0/','2012-09-22')]
existing={x['file'] for x in manifest['references']}
for name,url,credit,date in new:
 if name in existing:continue
 f=refs/name;manifest['references'].append({'file':name,'source_url':url,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size,'credit':credit,'capture_date':date,'edits':'None','retrieval_date':'2026-10-10','visually_reviewed':True})
manifest['failed_retrievals']=[{'file':'station-geograph-3779706.jpg','status':'Forbidden: Missing signature; this is an error response, not a reference photograph','replacement':'station-geograph-3779706-view.jpg'}]
p.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'gallery':str(dest/'index.html'),'reference_files':len(manifest['references'])}))
