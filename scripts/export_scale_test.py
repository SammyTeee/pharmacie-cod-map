"""Read-only v15 world geometry and linked image export for safe scale test."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-entrance-fixed-v16.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior']
for s in bpy.data.scenes:
 for layer in s.view_layers:layer.update()
objects=[]
for o in scene.objects:
 if o.type!='MESH' or o.hide_render or o.name.startswith(('Model reference','Reference |','Room label |')):continue
 if any(any(term in c.name.lower() for term in ('reference','guide','planned spawns')) for c in o.users_collection):continue
 mesh=o.data;mesh.calc_loop_triangles();uv=mesh.uv_layers.active
 m=mesh.materials[0] if mesh.materials else None;image=None
 if m and m.use_nodes:
  images=[n.image for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.outputs['Color'].is_linked]
  if images:image={'path':bpy.path.abspath(images[0].filepath),'dimensions':list(images[0].size),'name':images[0].name}
 objects.append({'name':o.name,'vertices_m':[list(o.matrix_world@v.co) for v in mesh.vertices],'faces':[list(p.vertices) for p in mesh.polygons],'triangles':[list(t.vertices) for t in mesh.loop_triangles],'face_uvs':[[list(uv.data[i].uv) for i in p.loop_indices] for p in mesh.polygons] if uv else [],'material':m.name if m else '', 'color':list(m.diffuse_color) if m else [.5,.5,.5,1],'image':image,'slab':o.name in ('Ground | continuous timber floor','First | floor with corrected L stairwell opening','Interior | removable suspended ceiling','Street | left side passage')})
# Close the upper pub for compilation; rectangular roof is test-only.
x0,x1,y0,y1,z0,z1=-5.7,11.15,0,31.25,9.12,9.30
objects.append({'name':'Test | upper roof slab','vertices_m':[[x,y,z] for z in (z0,z1) for x,y in ((x0,y0),(x1,y0),(x1,y1),(x0,y1))],'faces':[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]],'triangles':[[4,5,6],[4,6,7]],'face_uvs':[],'material':'Interior | ceiling tiles','color':[.5,.5,.5,1],'image':None,'slab':True})
out=ROOT/'build/scale-test-geometry.json';out.write_text(json.dumps({'blend':bpy.data.filepath,'scene':scene.name,'unit':'metres','objects':objects},separators=(',',':')))
result={'export':str(out),'objects':len(objects),'photo_objects':sum(bool(o['image']) for o in objects)}
