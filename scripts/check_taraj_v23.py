"""Check corrected Taraj solids, visible glazing, passage and road retention."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-taraj-front-v23.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
road=json.loads((ROOT/'recon/v22/validation.json').read_text());path=[Vector(p) for p in road['melton_centreline']];front=Vector(road['placeholder_buildings'][-1]['front_centre']);u=(path[-2]-path[-3]).normalized();out=Vector((-u.y,u.x));dg=bpy.context.evaluated_depsgraph_get()
hits=[]
for x in (-3.5,.3,4.1):
    p=front-u*x+out*3
    hit,loc,n,idx,obj,m=scene.ray_cast(dg,Vector((*tuple(p),6.5)),Vector((-out.x,-out.y,0)),distance=4)
    assert hit and 'upper recessed glass' in obj.name,(x,obj.name if obj else None)
    hits.append(obj.name)
p=front+u*4.8+out*1
hit,loc,n,idx,obj,m=scene.ray_cast(dg,Vector((*tuple(p),1.6)),Vector((-out.x,-out.y,0)),distance=6)
assert hit and 'left entry glazing' in obj.name,obj.name if obj else None
solids=[o for o in scene.objects if o.type=='MESH' and o.name.startswith(('Taraj v23 |','Street v22 |'))]
for o in solids:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0,o.name;bm.free()
refs=json.loads((ROOT/'recon/v23/validation.json').read_text())['references']
for r in refs:assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256']
result={'closed_outward_route_and_taraj_solids':len(solids),'upper_glazing_ray_hits':hits,'passage_ray_hits':'Taraj v23 | left entry glazing','new_reference_hashes_unchanged':len(refs),'radiant_or_game_verified':False}
(ROOT/'recon/v23/source-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
