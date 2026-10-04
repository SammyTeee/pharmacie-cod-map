from pathlib import Path
import os,json,bpy,hashlib,math
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v32'
os.environ.update(PHARMACIE_RECON_PHASE='after',PHARMACIE_RECON_OUTPUT=str(dest/'checks'),PHARMACIE_RECON_PROBES_ONLY='1',PHARMACIE_RECON_RADIUS='0.42')
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),str(ROOT/'scripts/recon_blender_players.py'),'exec'))
except SystemExit:pass
retained=json.loads((dest/'checks/route-probes.json').read_text())['samples']
samples=[]
lines=[('road centre',(-16,-6.7,-.08),(55,-6.7,-.08)),('pub pavement',(-16,-1.5,0),(55,-1.5,0)),('opposite pavement west',(-16,-11.5,0),(46,-11.5,0)),('bollard bypass transition',(46,-11.5,0),(47,-11,0)),('opposite pavement east',(47,-11,0),(55,-11,0)),('pub crossing',(5.5,-1.5,0),(5.5,-11.5,0)),('marked crossing',(40,-1.5,0),(40,-11.5,0)),('lane',(46.5,-14,0),(46.5,-28.8,0))]
for label,a,b in lines:
 a=Vector(a);b=Vector(b);count=math.ceil((b-a).length/.2)
 for i in range(count+1):
  p=a.lerp(b,i/count);support=ray(floorbvh,floornames,(p.x,p.y,p.z+.4),(0,0,-1),1)
  # Kerbs are excluded by the legacy floor-name classifier. Probe their top
  # explicitly; a small step is support, not a low ceiling. Engine stepping
  # and dropped-crossing geometry still require separate work.
  top=ray(bvh,names,(p.x,p.y,p.z+.4),(0,0,-1),1)
  if top and ('Long street kerb' in top['object'] or 'road crossing approach ramp' in top['object']) and top['normal'][2]>.5:support=top
  z=support['point'][2] if support else p.z;block=[]
  for height in (.45,1,1.65):
   for angle in range(8):
    hit=ray(bvh,names,(p.x,p.y,z+height),(math.cos(angle*math.pi/4),math.sin(angle*math.pi/4),0),.42)
    if hit:block.append(hit['object'])
  samples.append(dict(route=label,nominal=list(p),floor_object=support['object'] if support else None,blockers=sorted(set(block)),overhead=ray(bvh,names,(p.x,p.y,z+.08),(0,0,1),1.95)))
fail=[p for p in retained+samples if not p['floor_object'] or p['blockers'] or p['overhead']]
boundaries=[ray(bvh,names,(-17,-6.7,1.65),(-1,0,0),2),ray(bvh,names,(59.5,-6.7,1.65),(1,0,0),2),ray(bvh,names,(46.5,-28.8,1.65),(0,-1,0),2)]
assert all(boundaries),boundaries
sources=json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']
for r in sources:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
def signature(o):return hashlib.sha256(json.dumps({'vertices':[[round(x,6) for x in o.matrix_world@v.co] for v in o.data.vertices],'faces':[list(p.vertices) for p in o.data.polygons]},separators=(',',':')).encode()).hexdigest()
current={o.name:signature(o) for o in scene.objects if o.type=='MESH'}
changes=json.loads((dest/'changes.json').read_text());parent=Path(changes['source']);assert hashlib.sha256(parent.read_bytes()).hexdigest()==changes['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(parent));bpy.context.window.scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.view_layer.update();count=0
for o in bpy.context.scene.objects:
 if o.type=='MESH':assert current[o.name]==signature(o),o.name;count+=1
(dest/'validation.json').write_text(json.dumps(dict(retained_samples=len(retained),street_samples=len(samples),radius_m=.42,failures=fail,boundaries=boundaries,parent_scene_meshes_preserved=count,source_photos_unchanged=len(sources),engine_verified=False,limitations='Sparse radial rays, not continuous capsule sweeps or BO3 collision/AI testing'),indent=2))
(dest/'street-route-probes.json').write_text(json.dumps(samples,indent=2))
assert not fail,[(p['route'],p['nominal'],p['blockers']) for p in fail][:20]
print('V32_CHECKS_PASS',len(retained),len(samples),flush=True)
