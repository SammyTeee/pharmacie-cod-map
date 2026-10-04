from pathlib import Path
import bpy
assert Path(bpy.data.filepath).name=='pharmacie-melton-detail-v35.blend'
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith('Melton v35 | B014 | ') and any(s in o.name for s in ('roof','ridge','slate course','chimney')):
  for v in o.data.vertices:v.co.y*=.1
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
