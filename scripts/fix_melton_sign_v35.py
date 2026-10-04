from pathlib import Path
import bpy
from mathutils import Vector
assert Path(bpy.data.filepath).name=='pharmacie-melton-detail-v35.blend'
o=bpy.data.objects['Melton v35 | B034 | correct black fascia overlay']
for v in o.data.vertices:v.co.y-=.074
o=bpy.data.objects['Melton v35 | B034 | gold barber fascia'];o.matrix_world.translation+=o.matrix_world.to_3x3()@Vector((0,0,.076))
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
