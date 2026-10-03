"""Physical checks on saved v20; no Blender writes except validation report."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene;bpy.context.view_layer.update()
new=[o for o in scene.objects if o.name.startswith('Shop v20 |') and o.type=='MESH']
solids=0;quads=0
for o in new:
    if len(o.data.polygons)==1:quads+=1;continue
    bm=bmesh.new();bm.from_mesh(o.data)
    assert all(e.is_manifold for e in bm.edges),o.name
    assert bm.calc_volume(signed=True)>1e-10,o.name
    bm.free();solids+=1
def extent(o):
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    return tuple((min(v[i] for v in pts),max(v[i] for v in pts)) for i in range(3))
anchor=extent(bpy.data.objects['Front | sash recessed glass'])
windows=[o for o in new if '| Front | sash recessed glass' in o.name]
assert len(windows)==9
for o in windows:
    bounds=extent(o)
    assert abs((bounds[0][1]-bounds[0][0])-(anchor[0][1]-anchor[0][0]))<1e-5 and all(abs(bounds[2][i]-anchor[2][i])<1e-5 for i in range(2)),o.name
hit,pos,n,index,obj,matrix=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((-10.75,-12,1.8)),Vector((0,-1,0)),distance=3)
assert hit and 'Fox closed entry recessed glazing' in obj.name, f'Fox doorway obstructed: {obj.name if hit else None}'
for name in ('Fox and Hounds','Aston and Co','Syston Mini Market','Lets Move estate agents','Floral Fantasy'):
    assert 'Street v17 | '+name+' isolated facade' not in scene.objects
for s in json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']:
    assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
report={'closed_outward_solids':solids,'selected_photo_quads':quads,'pub_size_windows':9,'fox_entry_ray_hits_recessed_door':obj.name,'old_full_facade_planes_unlinked':5,'original_reference_hashes_unchanged':44,'radiant_or_game_verified':False}
(ROOT/'recon/v20/source-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
