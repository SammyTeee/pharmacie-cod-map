"""Recover named thin concave ground surfaces the legacy converter omitted."""
from pathlib import Path
import ast,json,uuid,math
from generate_blockout import parse_entity_blocks
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'scripts/generate_blender_test_map.py').read_text())
ns={'math':math,'uuid':uuid,'NS':uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704'),'UNIT':100/2.54,'SHIFT':(-3.5,-10,0)}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'legacy-convex-helpers','exec'),ns)
report=json.loads((ROOT/'build/playtest-v58-export-report.json').read_text())
skipped={s['name'] for s in report['skipped']}
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text())
materials=json.loads((ROOT/'assets/playtest-v58/manifest.json').read_text())['materials']
path=ROOT/'map_source/zm/zm_pharmacie_v58.map';text=path.read_text()
assert '// v58 recovered ground' not in text
pieces=[];records=[]
for o in data['objects']:
 if o['name'] not in skipped or not any(k in o['name'].lower() for k in ('carriageway','pavement foundation','terrain','turning head','paving','landing')):continue
 vs=o['vertices_m'];lo=min(v[2] for v in vs);hi=max(v[2] for v in vs)
 if hi-lo>.8 or hi-lo<.004:continue
 count=0
 for tri in o['triangles']:
  top=[vs[i] for i in tri]
  if any(abs(v[2]-hi)>.004 for v in top):continue
  if abs(ns['cross'](ns['sub'](top[1],top[0]),ns['sub'](top[2],top[0]))[2])<.0001:continue
  prism=top+[(v[0],v[1],lo) for v in top]
  faces=[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)]
  material=materials[o['material']]['name']
  brush=ns['convex_brush'](o['name']+f' recovered {count}',[ns['world'](v) for v in prism],faces,material,600000+len(pieces))
  if brush:pieces.append(brush);count+=1
 records.append({'object':o['name'],'triangle_prisms':count,'low_BU':lo,'high_BU':hi})
entities=parse_entity_blocks(text);a,b,ws=entities[0]
ws=ws[:ws.rfind('}')]+'// v58 recovered ground\n'+''.join(pieces)+'}\n'
path.write_text(text[:a]+ws+text[b:],newline='\n')
out=ROOT/'docs/build-results/playtest-v58/surface-repairs.json';out.write_text(json.dumps({'recovered':records,'brushes':len(pieces)},indent=2)+'\n')
assert any('continuous carriageway' in r['object'] and r['triangle_prisms']>0 for r in records)
print('Recovered',len(records),'surfaces as',len(pieces),'solid triangle prisms')
