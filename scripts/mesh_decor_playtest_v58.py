"""Use render meshes for already non-colliding decoration, rather than BSP solids."""
from pathlib import Path
import json,re,uuid
from generate_blockout import parse_entity_blocks
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'map_source/zm/zm_pharmacie_v58.map'
s=p.read_text();assert '// v58 mesh decoration conversion' not in s
assert '// v58 engine translation' in s
backup=ROOT/'build/playtest-v58-before-mesh-decor.map'
if not backup.exists():backup.write_text(s,newline='\n')
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text())
placement=json.loads((ROOT/'docs/build-results/playtest-v58/placements.json').read_text())
names=set(placement['noncolliding_small_decor'])
materials=json.loads((ROOT/'assets/playtest-v58/manifest.json').read_text())['materials']
NS=uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704')
objects={str(uuid.uuid5(NS,o['name'])):o for o in data['objects'] if o['name'] in names}
converted=[];patches=0
def coordinate(v):return ((v[0]-3.5)*(100/2.54),(v[1]-10)*(100/2.54)-18000,v[2]*(100/2.54))
def mesh(o,indices,face_number):
 verts=[coordinate(o['vertices_m'][i]) for i in indices]
 if len(verts)==3:verts.append(verts[-1])
 guid=uuid.uuid5(NS,o['name']+f' render patch {face_number}')
 rows=['{',f' guid "{{{guid}}}"',' mesh',' {','  contents nonColliding;','  toolFlags;',f'  {materials[o["material"]]["name"]}','  lightmap_gray','  2 2 0 8']
 for row,order in enumerate(((0,1),(3,2))):
  rows.append('  (')
  for col,i in enumerate(order):
   rows.append('   v '+' '.join(f'{v:.6f}' for v in verts[i])+f' t {col*256} {row*256} {col} {row}')
  rows.append('  )')
 return '\n'.join(rows+[' }','}'])+'\n'
def replace(m):
 global patches
 g=re.search(r'guid "\{([^}]+)',m[0]);o=objects.get(g[1]) if g else None
 if not o:return m[0]
 pieces=[]
 for face in o['faces']:
  faces=[face] if len(face) in (3,4) else [[face[0],face[i],face[i+1]] for i in range(1,len(face)-1)]
  for indices in faces:
   pieces.append(f'// brush {700000+patches}\n'+mesh(o,indices,patches));patches+=1
 converted.append(o['name']);return ''.join(pieces)
a,b,ws=parse_entity_blocks(s)[0]
ws=re.sub(r'(?ms)^// brush \d+\n\{.*?^\}\n?',replace,ws)
s=s[:a]+ws+s[b:];s='// v58 mesh decoration conversion\n'+s
p.write_text(s,newline='\n')
assert len(converted)>5000
(ROOT/'docs/build-results/playtest-v58/mesh-decoration.json').write_text(json.dumps({'converted_noncolliding_objects':len(converted),'render_mesh_patches':patches,'objects':converted,'reason':'Third full brush attempt reproduced cell/portal emission access violation; PRT had 66149 cells. Change representation instead of retrying unchanged. Original Blender meshes remain untouched; converted decoration retains its exported visible shape and existing non-colliding status.'},indent=2)+'\n')
print('Converted',len(converted),'noncolliding objects into',patches,'render patches')
