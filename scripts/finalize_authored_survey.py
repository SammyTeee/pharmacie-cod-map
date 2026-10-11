"""Summarise immutable browser captures; build a local evidence browser."""
from pathlib import Path
import json,re,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'references/streetview-capture/authored-route-2026-10-11'
ledger=json.loads((folder/'ledger.json').read_text())
repair={e['stop_index']:e for e in json.loads((folder/'metadata-repair.json').read_text())}
accepted={}
for e in ledger:
 if 'pass' in e.get('visual_review','') and not e['visual_review'].startswith('rejected'):
  accepted[e['stop_index'],e['view_index']]=e
assert len(accepted)==368,len(accepted)
records=[]
for (i,v),e in sorted(accepted.items()):
 assert hashlib.sha256((folder/e['file']).read_bytes()).hexdigest()==e['sha256'],e['file']
 url=e['actual_url'];verified=False
 if '@52.' not in url and i in repair:
  url=repair[i]['actual_url'];verified=True
 if url.startswith('google.com/'):url='https://www.'+url
 pos=re.search(r'@([\d.]+),(-?[\d.]+)',url)
 pano=re.search(r'!1s([^!/?]+)',url) or re.search(r'!2s([^&!]+)',e['dom'])
 date=re.search(r'Image capture: ([A-Za-z]+ \d{4})',e['dom'])
 records.append({'stop':e['stop_id'],'view':['ahead','right','back','left'][v],
 'requested_position':e['requested_position'],'chainage_m':e['chainage_m'],
 'resolved_url':url,'resolved_position':[float(x) for x in pos.groups()] if pos else None,
 'position_from_later_ahead_verification':verified,'panorama_id':pano[1] if pano else None,
 'imagery_date_visible':date[1] if date else 'see original screenshot','title':e['title'],
 'file':e['file'],'sha256':e['sha256'],'captured_utc':e['captured_utc'],
 'limitation':'Early directional UI metadata may precede final image; repaired ahead position is an independent check, not proof that all four views used the same panorama.' if verified else ''})
dest=ROOT/'recon/v53';dest.mkdir(exist_ok=True)
summary={'route_length_m':1090.768583563,'planned_stops':92,'accepted_views':len(records),
 'attempts_retained':len(ledger),'unique_observed_pano_ids':len({e['panorama_id'] for e in records if e['panorama_id']}),
 'resolved_positions':sum(e['resolved_position'] is not None for e in records),
 'attribution':'Google Street View; dates per image. Satellite Airbus/Maxar/Google; copyright date is not capture date.',
 'local_originals':str(folder.relative_to(ROOT)),'records':records}
(dest/'capture-manifest.json').write_text(json.dumps(summary,indent=2))
rows=[]
for i in range(92):
 views=[e for e in records if e['stop']==f'survey-{i+1:03}']
 pictures=''.join(f'<figure><a href="{html.escape(e["file"])}"><img loading="lazy" src="{html.escape(e["file"])}"></a><figcaption>{e["view"]} · {html.escape(e["imagery_date_visible"])}</figcaption></figure>' for e in views)
 rows.append(f'<section id="stop-{i+1}"><h2>{i+1:03} · {views[0]["chainage_m"]:.0f} m · {html.escape(views[0]["title"])}</h2><div>{pictures}</div></section>')
page='<!doctype html><meta charset="utf-8"><title>Authored route evidence</title><style>body{background:#15202a;color:#ecf1f5;font:16px system-ui;margin:2rem}a{color:#8cd5ff}section{border-top:1px solid #456;padding:1rem 0}section div{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem}figure{margin:0}img{width:100%}figcaption{padding:.5rem}</style><h1>Holmdale → Melton → Barkby Road</h1><p>92 stops · 368 reviewed views · 1.091 km. Google Street View; dates differ. Local reference evidence, not distributed image assets.</p><p><a href="../../../docs/AUTHORED_ROUTE_SURVEY_2026-10-11.md">Detailed observations</a></p>'+''.join(rows)
(folder/'index.html').write_text(page)
print(json.dumps({k:v for k,v in summary.items() if k!='records'},indent=2))
