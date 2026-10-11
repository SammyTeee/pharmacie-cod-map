"""Local review for number 29, without redistributing Google source imagery."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v44'
validation=json.loads((dest/'validation.json').read_text());checks=json.loads((dest/'route-checks.json').read_text());views=json.loads((dest/'review-views.json').read_text())['views']
rows=[]
for label in dict.fromkeys(v['view'] for v in views):
 rows.append('<h2>'+html.escape(label)+'</h2><div class="pair">'+''.join('<figure><img src="'+v['image']+'"><figcaption>'+v['stage']+'</figcaption></figure>' for v in views if v['view']==label)+'</div>')
page='''<!doctype html><meta charset="utf-8"><title>29 Holmdale Road — working exterior v44</title><style>body{background:#18212b;color:#edf0f4;font:17px system-ui;margin:30px;max-width:1500px}a{color:#9cd6ff}.pair{display:flex;gap:12px}figure{margin:0;width:50%}img{width:100%}pre{white-space:pre-wrap}</style><h1>29 Holmdale Road — v44 working exterior</h1><p>Photo-led from Sam’s identified Google Street View collage: cream bungalow, paired hipped roofs, bay joinery, porch, ribbed green garage door, driveway, hedge and right brick/timber boundary. Original reference imagery stays local and is not embedded in the model or this gallery.</p><p>Exact dimensions, rear footprint, position and facing remain estimates pending the Google top-down comparison. This is a static closed exterior. Road-end widening and station ramp/car park/rail corridor are unfinished. BO3 unchanged.</p><p>Four matched views use the same cameras before/after. The overhead is a model view, not satellite evidence.</p>'''
page+=''.join(rows)+'<h2>Checks and limitations</h2><pre>'+html.escape(json.dumps({'geometry':validation,'route':{k:checks[k] for k in ('clearance_rays','floor_samples','blocked_count','unsupported_count','limits')}},indent=2))+'</pre>'
(dest/'index.html').write_text(page,encoding='utf-8');print(dest/'index.html')
