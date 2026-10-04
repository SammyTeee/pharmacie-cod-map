from pathlib import Path
import bpy,bmesh,json,math,hashlib,os
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v37'
os.environ.update(PHARMACIE_RECON_PHASE='after',PHARMACIE_RECON_OUTPUT=str(dest/'checks'),PHARMACIE_RECON_PROBES_ONLY='1',PHARMACIE_RECON_RADIUS='.42')
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),'retained_pub_checks','exec'))
except SystemExit:pass
retained=route_samples.copy();path=[Vector((*p,-.08)) for p in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']]
routes=[('pub to junction',[Vector((-16,-6.7,-.08)),path[0]]),('Melton road centre',path[:-1]+[path[-1]-Vector((0,4,0))])]
samples=[]
for label,points in routes:
 for a,b in zip(points,points[1:]):
  steps=math.ceil((b-a).length/.1)
  for i in range(steps+1):
   p=a.lerp(b,i/steps);top=ray(bvh,names,p+Vector((0,0,.4)),(0,0,-1),1)
   z=top['point'][2] if top else p.z;hits=[]
   for h in (.45,1,1.65):
    for j in range(16):
     hit=ray(bvh,names,(p.x,p.y,z+h),(math.cos(j*math.tau/16),math.sin(j*math.tau/16),0),.42)
     if hit:hits.append(hit['object'])
   head=ray(bvh,names,(p.x,p.y,z+.08),(0,0,1),1.95)
   samples.append(dict(route=label,nominal=list(p),floor_z=z,support=top,blockers=sorted(set(hits)),overhead=head))
fails=[s for s in samples if not s['support'] or s['blockers'] or s['overhead']]
retained_fail=[s for s in retained if not s['floor_object'] or s['blockers'] or s['overhead']]
changes=json.loads((dest/'changes.json').read_text());solids=[]
for name in changes['new_solids']:
 ob=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges),name;assert bm.calc_volume(signed=True)>0,name;bm.free();solids.append(name)
def sig(o):
 # Unlinked archived objects have unevaluated matrix_world after reload.
 # Their saved local transform is authoritative; parented objects use world space.
 transform=o.matrix_basis if o.parent is None else o.matrix_world
 return hashlib.sha256(json.dumps({'v':[[round(x,6) for x in transform@v.co] for v in o.data.vertices],'f':[list(p.vertices) for p in o.data.polygons]},separators=(',',':')).encode()).hexdigest()
current={o.name:sig(o) for o in bpy.data.objects if o.type=='MESH'}
refs=json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']
for r in refs:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
parent=Path(changes['source']);assert hashlib.sha256(parent.read_bytes()).hexdigest()==changes['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(parent));count=0
for o in bpy.data.scenes['03 Both floors - assembled exterior'].objects:
 if o.type=='MESH':assert current[o.name]==sig(o),o.name;count+=1
(dest/'road-route-probes.json').write_text(json.dumps(samples,indent=2))
(dest/'validation.json').write_text(json.dumps(dict(new_closed_solids=len(solids),retained_pub_samples=len(retained),retained_failures=retained_fail,road_samples=len(samples),road_failures=fails,parent_mesh_geometry_preserved=count,source_photos_unchanged=len(refs),radius=.42,spacing=.1,bearings=16,engine_verified=False,limits='Visible-mesh sample rays, not a continuous capsule sweep or BO3 navigation test'),indent=2))
assert not fails and not retained_fail,[(p['route'],p['nominal'],p['blockers'],p.get('overhead')) for p in fails+retained_fail][:12]
print('V37_CHECKS_PASS',len(samples),flush=True)
