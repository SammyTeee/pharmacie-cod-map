from pathlib import Path
import bpy
assert Path(bpy.data.filepath).name=='pharmacie-melton-detail-v35.blend'
for src in list(bpy.data.objects):
 if src.type!='MESH' or not src.name.startswith('Syston v25 | ') or not src.name.endswith('| upper facade'):continue
 ident=src.name.split(' | ')[1];xs=[v.co.x for v in src.data.vertices];delta=src.matrix_world.to_3x3().col[0]*((min(xs)+max(xs))*.5)
 if delta.length<.0001:continue
 for o in bpy.data.objects:
  if o.name.startswith('Melton v35 | '+ident+' | '):o.matrix_world.translation+=delta
 print('FITTED',ident,tuple(delta),flush=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
