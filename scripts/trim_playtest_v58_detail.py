"""Reduce fine non-core engine brushes without reverting concave collision fix."""
from pathlib import Path
import json,re,uuid,collections
from generate_blockout import parse_entity_blocks
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'map_source/zm/zm_pharmacie_v58.map';text=p.read_text()
assert '// v58 reduced engine detail' not in text
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text())
core=set(json.loads((ROOT/'docs/build-results/playtest-v58/core-object-names.json').read_text())['names'])
ns=uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704');remove={}
for o in data['objects']:
 name=o['name'];lower=name.lower()
 if name in core or name.startswith('Holmdale') or any(k in lower for k in ('floor','ceiling','stair','road','carriageway','footway','pavement','foundation','terrain','ramp','perimeter','landing','wall','building','shell','boundary','kerb')):continue
 vs=o['vertices_m'];dims=[max(v[i] for v in vs)-min(v[i] for v in vs) for i in range(3)]
 if dims[0]*dims[1]*dims[2]<3:
  remove[str(uuid.uuid5(ns,name))]=name
removed=[]
def trim(m):
 index=int(re.match(r'// brush (\d+)',m[0])[1])
 if 700000<=index<850000:
  removed.append('tiny non-colliding render patch '+str(index));return ''
 g=re.search(r'guid "\{([^}]+)',m[0]);name=remove.get(g[1]) if g else None
 if name:removed.append(name);return ''
 return m[0]
a,b,ws=parse_entity_blocks(text)[0];ws=re.sub(r'(?ms)^// brush \d+\n\{.*?^\}\n?',trim,ws)
p.write_text('// v58 reduced engine detail\n'+text[:a]+ws+text[b:],newline='\n')
(ROOT/'docs/build-results/playtest-v58/detail-trim.json').write_text(json.dumps({'removed_brushes':len(removed),'objects':removed,'scope':'Fine non-core engine dressing under 3 BU3; pub core, Holmdale, circulation and architecture protected. Blender unchanged.'},indent=2)+'\n')
print('Removed fine engine brushes:',len(removed))
