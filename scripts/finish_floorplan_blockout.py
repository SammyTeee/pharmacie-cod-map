"""Finish UV maps, correct the generated office corridor and save previews."""
from pathlib import Path
import json
import bpy
import bmesh
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-floorplan-blockout.blend'
assert Path(bpy.data.filepath).resolve()==OUT.resolve()
ground=bpy.data.scenes['01 Ground floor - mapped rooms']
first=bpy.data.scenes['02 First floor - mapped rooms']
assembled=bpy.data.scenes['03 Both floors - assembled exterior']

# Fix only the generated partition: the red route at y575..693 is not a wall.
old_prefix='First | front-room passage rear'
pier=bpy.data.objects.get(old_prefix+' | pier 0')
if pier:
    delta=(693-575)*(7/316)*(316/327)
    old_length=max(v.co.x for v in pier.data.vertices)-min(v.co.x for v in pier.data.vertices)
    new_length=old_length-delta
    assert new_length>.5
    for v in pier.data.vertices:
        v.co.x=(1 if v.co.x>0 else -1)*new_length/2
    pier.location.x+=delta/2
    for o in list(first.objects):
        if o.name.startswith(old_prefix):
            o.name=o.name.replace(old_prefix,'First | kitchen passage rear',1)

objects={o for s in (ground,first,assembled) for o in s.objects if o.type=='MESH' and not o.name.startswith('Model reference')}
for o in objects:
    mesh=o.data
    bm=bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    for uvname,normalized in [('UV_Metres',False),('UV_Face_01',True)]:
        uv=mesh.uv_layers.get(uvname) or mesh.uv_layers.new(name=uvname)
        for poly in mesh.polygons:
            axis=max(range(3),key=lambda i:abs(poly.normal[i]))
            axes=[i for i in range(3) if i!=axis]
            values=[tuple(mesh.vertices[mesh.loops[j].vertex_index].co[i] for i in axes) for j in poly.loop_indices]
            low=[min(v[i] for v in values) for i in range(2)]
            high=[max(v[i] for v in values) for i in range(2)]
            for j,v in zip(poly.loop_indices,values):
                uv.data[j].uv=tuple((v[i]-low[i])/max(high[i]-low[i],1e-8) if normalized else v[i] for i in range(2))
    mesh.uv_layers.active_index=0
    o['texture_status']='Placeholder material; UV_Metres for tiling, UV_Face_01 for individual photo faces'

ground.camera.data.ortho_scale=33
first.camera.data.ortho_scale=33
# Keep the shop's upper facade in the assembled view; ground cutaway shows the
# street entrance without an upper-storey facade hiding it.
front=next(c for c in ground.collection.children if c.name.startswith('BLOCKOUT | Frontage'))
upper=bpy.data.collections.new('BLOCKOUT | Upper frontage - assembled view')
assembled.collection.children.link(upper)
for o in list(front.objects):
    if o.name.startswith(('Front | upstairs','Front | upper sash','Front | sash')):
        upper.objects.link(o)
        front.objects.unlink(o)

preview_paths=[]
for s,filename in [(ground,'ground-floor-blockout.png'),(first,'first-floor-blockout.png'),(assembled,'assembled-blockout.png')]:
    s.render.filepath=str(OUT.parent/filename)
    bpy.ops.render.render(write_still=True,scene=s.name)
    preview_paths.append(s.render.filepath)

for s,filename in [(ground,'ground-floor-top-plan.png'),(first,'first-floor-top-plan.png')]:
    camera=s.camera
    original_matrix=camera.matrix_world.copy()
    original_ortho=camera.data.ortho_scale
    camera.location=(3.5,10,45)
    camera.rotation_euler=(Vector((3.5,10,0))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=35
    s.render.filepath=str(OUT.parent/filename)
    bpy.ops.render.render(write_still=True,scene=s.name)
    preview_paths.append(s.render.filepath)
    camera.matrix_world=original_matrix
    camera.data.ortho_scale=original_ortho

bpy.context.window.scene=ground
bpy.ops.object.select_all(action='DESELECT')
assert all('UV_Metres' in o.data.uv_layers and 'UV_Face_01' in o.data.uv_layers for o in objects)
manifest_path=OUT.parent/'floorplan-blockout-manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['texture_uvs']={'UV_Metres':'Planar face projection, 1 UV unit per metre','UV_Face_01':'Each face normalized 0..1 for photographic panels; final photo alignment remains to do'}
manifest['stairs']['status']='User approved continuous L staircase; position adapted from upstairs plan; original ground stair symbol preserved as hidden guide'
manifest['stairs']['ground_service_adaptation']='Service rear partition shortened to leave L stair approach clear'
manifest['verification']={'mesh_uv_count':len(objects),'normals':'Recalculated outward','previews':preview_paths,'game':'Not compiled or tested; Blender modelling task only'}
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'file':str(OUT),'uv_mapped_meshes':len(objects),'previews':preview_paths,'corridor':'Office hall open to seating; kitchen has its own door'}
