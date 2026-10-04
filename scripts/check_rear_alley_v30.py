"""Saved-file route checks, widened sensitivity, and new enclosure assertions."""
from pathlib import Path
import os,json,bpy,bmesh,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v30';dest.mkdir(exist_ok=True)
os.environ['PHARMACIE_RECON_PHASE']='after';os.environ['PHARMACIE_RECON_OUTPUT']=str(dest/'checks');os.environ['PHARMACIE_RECON_PROBES_ONLY']='1';os.environ['PHARMACIE_RECON_RADIUS']='0.42'
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),str(ROOT/'scripts/recon_blender_players.py'),'exec'))
except SystemExit:pass
routes=json.loads((dest/'checks/route-probes.json').read_text())['samples']
fail=[p for p in routes if not p['floor_object'] or p['blockers'] or p['overhead']]
enclosure=[]
for y in (1,8,16,20,24,28,30):
    for direction in ((-1,0,0),(1,0,0)):
        hit=ray(bvh,names,(-11.4,y,1.65),direction,1.2)
        assert hit,('Alley side open',y,direction)
        enclosure.append({'origin':[-11.4,y,1.65],'direction':direction,'hit':hit})
for x in (-10.8,-9.5,-8,-6.5,-5,-3):
    hit=ray(bvh,names,(x,32.2,1.65),(0,1,0),4)
    assert hit,('Rear north enclosure open',x);enclosure.append({'origin':[x,32.2,1.65],'direction':[0,1,0],'hit':hit})
bar=ray(bvh,names,(5,17,1.65),(1,0,0),8);assert bar and 'Closed bar service door leaf' in bar['object'],bar
# Window pocket has backing floor/ceiling and rear wall, not a sky-facing void.
for d in [(0,1,0),(0,0,-1),(0,0,1)]:assert ray(bvh,names,(-7.65,34.2,1.65),d,3),d
new=[o for o in scene.objects if o.type=='MESH' and o.name.startswith('Mapping v30 |')]
for o in new:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)*o.matrix_world.determinant()>0,o.name;bm.free()
sources=json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']
for r in sources:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
r={'saved_checkpoint':bpy.data.filepath,'route_radius_m':.42,'route_samples':len(routes),'route_failures':fail,'alley_and_rear_enclosure_samples':enclosure,'bar_door_ray':bar,'window_pocket_floor_ceiling_backing':True,'closed_positive_volume_new_meshes':len(new),'original_reference_hashes_unchanged':len(sources),'runtime_verified':False,'limitations':['Sparse radial rays, not a player capsule sweep','Outdoor sky above alley is intentional','No purchase behavior, spawn logic, zombie pursuit or coop test']}
def signature(o):
    return hashlib.sha256(json.dumps({'vertices':[[round(x,6) for x in o.matrix_world@v.co] for v in o.data.vertices],'faces':[list(p.vertices) for p in o.data.polygons]},separators=(',',':')).encode()).hexdigest()
# Unlinked archives have unevaluated world matrices after reopening. Link only
# for preservation comparison, after all route rays; never save or render this.
scene.collection.children.link(bpy.data.collections['ARCHIVE v30 | Open rear floor slabs']);bpy.context.view_layer.update()
current={o.name:signature(o) for o in bpy.data.objects if o.type=='MESH'}
changes=json.loads((dest/'changes.json').read_text());parent=Path(changes['source']);assert hashlib.sha256(parent.read_bytes()).hexdigest()==changes['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(parent));base=bpy.data.scenes['03 Both floors - assembled exterior'];count=0
for o in base.objects:
    if o.type=='MESH':assert current[o.name]==signature(o),o.name;count+=1
r['parent_checkpoint_hash_unchanged']=True;r['parent_scene_mesh_geometry_preserved_including_archives']=count
(dest/'validation.json').write_text(json.dumps(r,indent=2))
assert not fail,[(p['route'],p['nominal'],p['blockers']) for p in fail]
print('V30_SAVED_CHECKS_PASS',len(routes),len(new),flush=True)
