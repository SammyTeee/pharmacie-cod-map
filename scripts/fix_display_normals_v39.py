import bpy,bmesh
from pathlib import Path
assert Path(bpy.data.filepath).name=='pharmacie-retail-detail-v39.blend'
count=0
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith('Street v39 |'):
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();count+=1
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);print('V39_NORMALS_FIXED',count,flush=True)
