"""Geometry and uninterrupted road-surface checks for the saved blockout."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-melton-road-v22.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
report=json.loads((ROOT/'recon/v22/validation.json').read_text());path=[Vector(p) for p in report['melton_centreline']]
dg=bpy.context.evaluated_depsgraph_get();checks=0
for a,b in zip(path,path[1:]):
    d=b-a;u=d.normalized();n=Vector((-u.y,u.x))
    for j in range(7 if a==path[0] else 1,int(d.length),2):
        for side in (-2,0,2):
            p=a+u*j+n*side
            hit,loc,normal,index,obj,matrix=scene.ray_cast(dg,Vector((p.x,p.y,3)),Vector((0,0,-1)),distance=4)
            assert hit and -.09<=loc.z<=-.06,(list(p),obj.name if obj else None,list(loc))
            checks+=1
solids=[o for o in scene.objects if o.type=='MESH' and o.name.startswith('Street v22 |')]
for o in solids:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0,o.name;bm.free()
assert hashlib.sha256((ROOT/report['source']).read_bytes()).hexdigest()==report['source_sha256']
result={'closed_outward_solids':len(solids),'clear_road_samples_three_lanes':checks,'labelled_map_original_unchanged':True,'radiant_or_game_verified':False}
(ROOT/'recon/v22/source-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
