"""Final saved-file verification, no Blender scene modifications."""
from pathlib import Path
import bpy,bmesh,json,hashlib
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v26'
assert Path(bpy.data.filepath).name=='pharmacie-taraj-interior-bridge-v26.blend'
r=json.loads((dest/'validation.json').read_text());coll=bpy.data.collections['DETAIL v26 | Bridge brook and Taraj restaurant']
solids=[o for o in coll.objects if o.type=='MESH' and not o.get('photo_insert')]
for ob in solids:
    bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges),ob.name;assert bm.calc_volume(signed=True)>0 and ob.matrix_world.determinant()>0,ob.name;bm.free()
for file,sha in r['references'].items():assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==sha,file
assert hashlib.sha256((ROOT/'assets/blender/pharmacie-syston-street-v25.blend').read_bytes()).hexdigest()==r['source_sha256']
paths=[dest/(n+'.png') for n in ('01_taraj_dining','02_taraj_booths','03_taraj_bar','04_taraj_guest','05_taraj_entry','06_bridge_overview','07_bridge_brook','08_bridge_side','09_bridge_access_plan','10_taraj_cutaway')]
for p in paths:assert p.exists() and p.stat().st_size>10000,p
result={'final_checkpoint_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'closed_outward_new_solids':len(solids),'curve_details':len([o for o in coll.objects if o.type=='CURVE']),'practical_lights':len([o for o in coll.objects if o.type=='LIGHT']),'photographic_guest_inserts':len([o for o in coll.objects if o.get('photo_insert')]),'source_checkpoint_unchanged':True,'three_source_images_unchanged':True,'render_count':len(paths),'radiant_or_game_verified':False}
r['closed_outward_new_solids']=len(solids);r['final_checkpoint_sha256']=result['final_checkpoint_sha256'];(dest/'validation.json').write_text(json.dumps(r,indent=2)+'\n')
(dest/'final-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
