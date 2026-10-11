"""Local matched review page; states unfinished fidelity requirements."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v43'
validation=json.loads((dest/'validation.json').read_text())
views=json.loads((dest/'review-views.json').read_text())['views']
rows=[]
for label in dict.fromkeys(v['view'] for v in views):
 rows.append('<h2>'+html.escape(label)+'</h2><div class="pair">'+''.join('<figure><img src="'+v['image']+'"><figcaption>'+v['stage']+'</figcaption></figure>' for v in views if v['view']==label)+'</div>')
checks=json.loads((dest/'route-checks.json').read_text())
page='''<!doctype html><meta charset="utf-8"><title>Station v43 — provisional detail</title><style>body{background:#18212b;color:#edf0f4;font:17px system-ui;margin:30px;max-width:1500px}a{color:#9cd6ff}.pair{display:flex;gap:12px}figure{margin:0;width:50%}img{width:100%}pre{white-space:pre-wrap}</style><h1>Syston station — v43 working detail</h1><p>Google overhead comparison remains pending. These are model previews, not evidence of geographic fidelity. Number 29, the station ramp, car park and rail corridor remain unfinished.</p><p>Blue/metal platform furniture uses dated station photos and mapped feature tags. Shelter design, dimensions, count and exact placements are provisional. The mapped platform footprint is retained; existing roads and earlier venue work are unchanged. BO3 unchanged.</p><p><a href="https://www.nationalrail.co.uk/stations/syston/">Official station layout</a> · <a href="https://www.geograph.org.uk/photo/3779706">Nigel Thompson, 22 September 2012, CC BY-SA 2.0</a> · <a href="https://www.geograph.org.uk/photo/8028555">David Howard, 20 April 2025, CC BY-SA 2.0</a> · Map data © OpenStreetMap contributors, ODbL.</p>'''
page+=''.join(rows)+'<h2>Geometry and selected route checks</h2><pre>'+html.escape(json.dumps({'geometry':validation,'route':{k:checks[k] for k in ('clearance_rays','floor_samples','blocked_count','unsupported_count','limits')}},indent=2))+'</pre>'
(dest/'index.html').write_text(page,encoding='utf-8')
print(dest/'index.html')
