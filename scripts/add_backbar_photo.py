"""Pack original bar reference and map its backbar region in Blender v08."""
from pathlib import Path
import json
import hashlib
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-backbar-photo-v08.blend'
assert Path(bpy.data.filepath).name=='pharmacie-layout-fixed-v07.blend'
if OUT.exists():raise RuntimeError('Preserve existing v08 before rerunning')
source=ROOT/'references/pharmacie-syston/bar front.jpg'
alternate=ROOT/'references/pharmacie-syston/WhatsApp Image 2026-10-02 at 10.19.05 PM (5).jpeg'
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,alternate)}
for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
image=bpy.data.images.load(str(source),check_existing=True)
image.pack()
crop=(.205,.215,.985,.585) # normalised left, top, right, bottom; UV-only
x0,x1=-.225,7.784
z0,z1=1.08,3.61
y=20.72

material=bpy.data.materials.new('Interior photo | bar front BACKBAR region')
material.use_nodes=True
bs=material.node_tree.nodes.get('Principled BSDF')
bs.inputs['Roughness'].default_value=.85
texture=material.node_tree.nodes.new('ShaderNodeTexImage');texture.image=image
material.node_tree.links.new(texture.outputs['Color'],bs.inputs['Base Color'])

def photo_plane(name,coords,region,collection):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(coords,[],[(0,1,2,3)]);mesh.update()
    mesh.materials.append(material)
    uv=mesh.uv_layers.new(name='UV_Photo_Backbar')
    left,top,right,bottom=region
    for loop,point in zip(mesh.polygons[0].loop_indices,[(left,1-bottom),(right,1-bottom),(right,1-top),(left,1-top)]):
        uv.data[loop].uv=point
    uv.active_render=True
    obj=bpy.data.objects.new(name,mesh);collection.objects.link(obj)
    obj['source']='references/pharmacie-syston/bar front.jpg'
    obj['uv_crop_normalised']=list(region)
    obj['note']='Photo backing; recorded doors/objects are visual detail, not gameplay entities'
    scale=bpy.data.objects['GAMEPLAY | Pub scale 1.50 - frontage 10.5m']
    obj.parent=scale;obj.matrix_parent_inverse=scale.matrix_world.inverted()
    return obj

collection=bpy.data.collections.new('INTERIOR | Photo-backed bar display')
for name in ('03 Both floors - assembled exterior','05 Interior - photo-led dressing'):
    bpy.data.scenes[name].collection.children.link(collection)
panel=photo_plane('Bar | photo-backed bottles, shelves and staff-door detail',[(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],crop,collection)

# Match the existing 3D screen to its photographed position rather than show
# two mismatched televisions. Keep its body and frame as editable geometry.
tv=(.435,.262,.575,.402)
tx0=x0+(tv[0]-crop[0])/(crop[2]-crop[0])*(x1-x0)
tx1=x0+(tv[2]-crop[0])/(crop[2]-crop[0])*(x1-x0)
tz0=z1-(tv[3]-crop[1])/(crop[3]-crop[1])*(z1-z0)
tz1=z1-(tv[1]-crop[1])/(crop[3]-crop[1])*(z1-z0)
for name in ('Bar | backbar shelves and screen | screen body','Bar | backbar shelves and screen | screen glass'):
    obj=bpy.data.objects[name]
    points=[obj.matrix_world@v.co for v in obj.data.vertices]
    oldx=(min(p.x for p in points),max(p.x for p in points))
    oldz=(min(p.z for p in points),max(p.z for p in points))
    border=.055 if name.endswith('glass') else 0
    obj.data=obj.data.copy();inv=obj.matrix_world.inverted()
    for vertex,p in zip(obj.data.vertices,points):
        p.x=tx0+border+(p.x-oldx[0])/(oldx[1]-oldx[0])*(tx1-tx0-2*border)
        p.z=tz0+border+(p.z-oldz[0])/(oldz[1]-oldz[0])*(tz1-tz0-2*border)
        vertex.co=inv@p
photo_plane('Bar | photo menu on 3D screen',[(tx0+.055,20.175,tz0+.055),(tx1-.055,20.175,tz0+.055),
    (tx1-.055,20.175,tz1-.055),(tx0+.055,20.175,tz1-.055)],tv,collection)

for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
for p in (source,alternate):assert hashes[str(p.relative_to(ROOT))]==hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'file':str(OUT),'source':'references/pharmacie-syston/bar front.jpg',
    'alternate_reference':str(alternate.relative_to(ROOT)),'source_hashes':hashes,
    'source_dimensions':list(image.size),'derivative':'No raster edit; packed original with UV crops',
    'backbar_uv_crop_normalised':crop,'screen_uv_crop_normalised':tv,
    'panel_bounds_m':{'x':[x0,x1],'y':y,'z':[z0,z1]},
    'source_photos_unchanged':True,'radiant_rebuilt':False,'bo3_material_conversion':'Pending next authorized export; existing BO3 generator does not yet distinguish this backbar crop material'}
(ROOT/'assets/blender/backbar-photo-v08-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for s in bpy.data.scenes:s['gameplay_version']='v08 - photo-backed bar, Blender edits only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'saved':str(OUT),'packed_photo':image.name,'crop':crop,'source_unchanged':True,'radiant_rebuilt':False}
