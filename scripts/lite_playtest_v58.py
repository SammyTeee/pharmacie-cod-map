"""Bound first engine exploration geometry while keeping all route architecture."""
from pathlib import Path
import json,re,uuid
from generate_blockout import parse_entity_blocks
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'map_source/zm/zm_pharmacie_v58.map';s=p.read_text()
assert '// v58 lean exploration export' not in s
backup=ROOT/'build/playtest-v58-before-lite.map'
if not backup.exists():backup.write_text(s,newline='\n')
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text())
core=ROOT/'docs/build-results/playtest-v58/core-object-names.json'
if core.exists():oldnames=set(json.loads(core.read_text())['names'])
else:
 old=json.loads((ROOT/'build/playtest-v18-geometry.json').read_text())
 oldnames={o['name'] for o in old['objects']}
 core.write_text(json.dumps({'source':'Prior v18 evaluated export; names only, no game assets','names':sorted(oldnames)},indent=2)+'\n')
byname={o['name']:o for o in data['objects']}
NS=uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704');protected=set()
for o in data['objects']:
 name=o['name']
 if name in oldnames or name.startswith(('Holmdale v49','Holmdale v50','Holmdale v51')) or any(k in name.lower() for k in ('floor','ceiling','stair','connector','carriageway','pavement','foundation','terrain','ramp','turning head')):
  protected.add(str(uuid.uuid5(NS,name)))
  if o['slab']:
   protected.update(str(uuid.uuid5(NS,name+f' triangle {j}')) for j in range(len(o['triangles'])))
decor=json.loads((ROOT/'docs/build-results/playtest-v58/mesh-decoration.json').read_text())
mesh_keep=set();counter=700000
for name in decor['objects']:
 o=byname[name];count=sum(1 if len(face) in (3,4) else len(face)-2 for face in o['faces'])
 if name in oldnames or name.startswith(('Holmdale v44','Holmdale v49','Holmdale v50','Holmdale v51')):mesh_keep.update(range(counter,counter+count))
 counter+=count
removed=[];kept=0
number=r'[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'
def cull(m):
 global kept
 brush=m[0];index=int(re.match(r'// brush (\d+)',brush)[1])
 if index>=700000 and index not in mesh_keep:
  removed.append({'brush':index,'reason':'fine street render dressing deferred'});return ''
 g=re.search(r'guid "\{([^}]+)',brush)
 if ' mesh\n' not in brush and not re.search(r'\)\s+sky\s',brush) and index<600000 and (not g or g[1] not in protected):
  coords=[tuple(map(float,v)) for v in re.findall(r'\(\s*('+number+r')\s+('+number+r')\s+('+number+r')\s*\)',brush)]
  dims=[(max(v[i] for v in coords)-min(v[i] for v in coords))/(100/2.54) for i in range(3)]
  volume=dims[0]*dims[1]*dims[2]
  if volume<.15:
   removed.append({'brush':index,'reason':'fine street brush dressing deferred','bounding_volume_BU3':volume});return ''
 kept+=1;return brush
a,b,ws=parse_entity_blocks(s)[0];ws=re.sub(r'(?ms)^// brush \d+\n\{.*?^\}\n?',cull,ws)
s='// v58 lean exploration export\n'+s[:a]+ws+s[b:];p.write_text(s,newline='\n')
(ROOT/'docs/build-results/playtest-v58/lean-export.json').write_text(json.dumps({'retained_world_brushes_or_patches':kept,'deferred_count':len(removed),'deferred':removed,'preservation':'Full geographic route and large architecture retained; original v18 pub objects and corrected Holmdale porch protected; Blender source unchanged. Fine street decoration deferred to a future optimized model export.'},indent=2)+'\n')
print('Retained',kept,'world brushes/patches; deferred',len(removed),'fine dressing elements')
