"""Bound tiny non-colliding render props, never large concave architecture."""
from pathlib import Path
import json,re
from generate_blockout import parse_entity_blocks,box_brush
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'map_source/zm/zm_pharmacie_v58.map';text=path.read_text()
assert '// v58 tiny decor proxies' not in text
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text());byname={o['name']:o for o in data['objects']}
names=json.loads((ROOT/'docs/build-results/playtest-v58/mesh-decoration.json').read_text())['objects']
materials=json.loads((ROOT/'assets/playtest-v58/manifest.json').read_text())['materials']
lookup={};counter=700000
for name in names:
 o=byname[name];count=sum(1 if len(f) in (3,4) else len(f)-2 for f in o['faces'])
 for i in range(counter,counter+count):lookup[i]=name
 counter+=count
seen=set();removed=0;proxies=[]
def replace(m):
 global removed
 index=int(m[1]);name=lookup.get(index)
 if not name:return m[0]
 removed+=1
 if name in seen:return ''
 seen.add(name);o=byname[name];vs=o['vertices_m'];lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)]
 assert max(hi[i]-lo[i] for i in range(3))<.751 and lo[2]>.35 and not o['image'],name
 bounds=[]
 for i in range(3):
  shift=(-3.5,-10,0)[i];offset=(0,-18000,0)[i]
  bounds.extend(((lo[i]+shift)*(100/2.54)+offset,(max(hi[i],lo[i]+.006)+shift)*(100/2.54)+offset))
 b=box_brush(900000+len(proxies),tuple(bounds),materials[o['material']]['name'],'\n')
 proxies.append(name)
 return re.sub(r'( guid "[^\n]+\n)',r'\1 contents nonColliding detail;\n',b,count=1)
a,b,ws=parse_entity_blocks(text)[0];ws=re.sub(r'(?ms)^// brush (\d+)\n\{.*?^\}\n?',replace,ws)
path.write_text('// v58 tiny decor proxies\n'+text[:a]+ws+text[b:],newline='\n')
(ROOT/'docs/build-results/playtest-v58/decor-proxies.json').write_text(json.dumps({'removed_face_patches':removed,'small_noncolliding_proxies':len(proxies),'objects':proxies,'limits':'Tiny curved props appear boxy in the engine test; Blender unchanged. Every replaced source is under .751 BU in all dimensions, above .35 BU, non-photographic and non-colliding.'},indent=2)+'\n')
print(removed,'face patches replaced with',len(proxies),'tiny noncolliding proxies')
