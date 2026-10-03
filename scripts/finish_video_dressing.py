"""Final circulation correction and scene integration for v10."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-video-details-v10.blend'
for s in bpy.data.scenes:
 for vl in s.view_layers:vl.update()
# Bookcase initially intersected the rear banquette; move into the clear rear corner.
moved=[]
for o in bpy.data.objects:
 if o.name.startswith(('Video | bookcase','Video | stacked board game')):
  for v in o.data.vertices:v.co+=Vector((-.435,3,0))
  moved.append(o.name)
root=bpy.data.objects['GAMEPLAY | Pub scale 1.50 - frontage 10.5m']
for o in bpy.data.objects:
 if o.name.startswith('Video |') and o.type=='MESH' and o.parent is None:
  o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted()
for s in bpy.data.scenes:
 for vl in s.view_layers:vl.update()
# Furniture was kept to the sides or spaced centre groups; doorway approach row
# at Y19.6–20.9 remains clear of new centre dining furniture.
upper=bpy.data.collections['VIDEO | Upstairs furniture and decor - 2019 evidence']
center=[o for o in upper.objects if o.name.startswith('Video | upstairs centre dining')]
assert max((o.matrix_world@v.co).y for o in center for v in o.data.vertices)<17
book=[o for o in upper.objects if o.name.startswith('Video | bookcase')]
assert min((o.matrix_world@v.co).y for o in book for v in o.data.vertices)>19.7
fridge=[o for o in bpy.data.objects if o.name=='Video | tall beer fridge cabinet'][0]
assert max((fridge.matrix_world@v.co).x for v in fridge.data.vertices)<-.8
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
manifest=ROOT/'assets/blender/video-details-v10-manifest.json';d=json.loads(manifest.read_text())
d['final_review']={'bookcase_moved_clear_of_banquette':moved,'new_meshes_parented_to_gameplay_scale':True,'static_checks':'Upstairs centre furniture ends before Y17; rear doorway approach row clear; bookcase beyond banquette; fridge stays left of counter. In-game verification pending.'};manifest.write_text(json.dumps(d,indent=2)+'\n')
result={'saved':bpy.data.filepath,'bookcase_objects_repositioned':len(moved),'checks_passed':True}
