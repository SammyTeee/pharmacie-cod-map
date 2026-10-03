"""Read-only export of assembled Blender geometry for the Radiant test generator."""
from pathlib import Path
import json
import bpy
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-photo-interior-v03.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.view_layer.update()
objects=[]
for o in scene.objects:
    if o.type!='MESH' or o.name.startswith(('Model reference','Reference |')):continue
    mesh=o.data
    mesh.calc_loop_triangles()
    verts=[list(o.matrix_world@v.co) for v in mesh.vertices]
    uv=next((u for u in mesh.uv_layers if u.active_render),mesh.uv_layers.active)
    objects.append({'name':o.name,'vertices_m':verts,'faces':[[v for v in p.vertices] for p in mesh.polygons],
        'triangles':[[v for v in tri.vertices] for tri in mesh.loop_triangles],
        'face_uvs':[[list(uv.data[i].uv) for i in p.loop_indices] for p in mesh.polygons] if uv else [],
        'material':mesh.materials[0].name if mesh.materials else '',
        'slab':o.name in ('Ground | continuous timber floor','First | floor with corrected L stairwell opening','Interior | removable suspended ceiling')})
# An upper roof for the in-game test; not an edit to the saved Blender source.
pixels=[(76,558),(172,566),(346,567),(1096,501),(1120,828),(813,856),(813,865),(302,885),(76,885)]
poly=[Vector(((y-558)*(7/316)*(316/327),(x-76)*(7/316)*(934/1044),6.20)) for x,y in pixels]
triangles=tessellate_polygon([poly])
ids=lambda tri:[v if isinstance(v,int) else min(range(len(poly)),key=lambda i:(poly[i]-v).length) for v in tri]
objects.append({'name':'Test | upper roof slab','vertices_m':[list(p) for p in poly]+[list(p-Vector((0,0,.15))) for p in poly],
    'faces':[],'triangles':[ids(t) for t in triangles],'face_uvs':[],'material':'Interior | ceiling tiles','slab':True})
out=ROOT/'build/blender-test-geometry.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'blend':bpy.data.filepath,'scene':scene.name,'unit':'metres','objects':objects},separators=(',',':')),encoding='utf-8')
result={'export':str(out),'mesh_objects':len(objects),'source_scene_unmodified':True}
