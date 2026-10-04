"""Park rear leaf against wall so narrow corridor has no swinging-leaf pinch."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
assert not bpy.data.objects.get('Mapping v30 | Rear exit door leaf parked against wall')
old=bpy.data.objects['Ground shell 03 | door 0 | open leaf'];coll=bpy.data.collections['MAPPING v30 | Enclosed rear alley and sealed service door'];archive=bpy.data.collections['ARCHIVE v30 | Open rear floor slabs']
new=old.copy();new.data=old.data.copy();new.name='Mapping v30 | Rear exit door leaf parked against wall';coll.objects.link(new)
hinge=bpy.data.objects['Ground shell 03 | door 0 | jamb 0'];pivot=sum((hinge.matrix_world@Vector(v) for v in hinge.bound_box),Vector())/8;pivot.z=0
new.matrix_world=Matrix.Translation(Vector((0,.22,0)))@Matrix.Translation(pivot)@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-pivot)@old.matrix_world
new['mapping_role']='scenery_open_door';new['status']='Leaf parked against wall for rear-alley clearance; original archived'
archive.objects.link(old)
for c in list(old.users_collection):
    if c!=archive:c.objects.unlink(old)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
p=ROOT/'recon/v30/changes.json';r=json.loads(p.read_text());r['new_closed_solids']+=1;r['archived_original_door']=old.name;r['changes'].append('Rear open leaf parked against wall to clear narrow turn');p.write_text(json.dumps(r,indent=2))
print('V30_REAR_DOOR_PARKED')
