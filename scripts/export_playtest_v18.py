"""Read evaluated v18 geometry without saving or changing the Blender source."""
from pathlib import Path
import bpy, json
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name == 'pharmacie-player-cleanup-v18.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene=scene
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
objects=[]; warnings=[]
for o in scene.objects:
    if o.type not in ('MESH','FONT') or o.hide_render: continue
    if o.name.startswith(('Model reference','Reference |','Room label |')): continue
    if any(any(t in c.name.lower() for t in ('reference','guide','planned spawns','planning only')) for c in o.users_collection): continue
    evaluated=o.evaluated_get(deps)
    mesh=evaluated.to_mesh(); mesh.calc_loop_triangles()
    # Unlinked image vectors use the render UV map, which can differ from the
    # map selected for editing. Resolve explicit UV nodes per material below.
    default_uv=next((layer for layer in mesh.uv_layers if layer.active_render),mesh.uv_layers.active)
    verts=[list(o.matrix_world@v.co) for v in mesh.vertices]
    materials=list(mesh.materials)
    groups={}
    for p in mesh.polygons: groups.setdefault(p.material_index,[]).append(p)
    for mi,polys in groups.items():
        uv=default_uv
        m=materials[mi] if mi<len(materials) else None
        image=None; procedural=False
        if m and m.use_nodes:
            outputs=[n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output]
            shader=outputs[0].inputs['Surface'].links[0].from_node if outputs and outputs[0].inputs['Surface'].is_linked else None
            socket=shader.inputs.get('Base Color') if shader else None
            if socket and socket.is_linked:
                node=socket.links[0].from_node
                if node.type=='TEX_IMAGE' and node.image:
                    if node.inputs['Vector'].is_linked:
                        mapping=node.inputs['Vector'].links[0].from_node
                        if mapping.type not in ('UVMAP','TEX_COORD'): raise RuntimeError(f'Unsupported image mapping: {o.name}')
                        if mapping.type=='UVMAP' and mapping.uv_map:
                            uv=mesh.uv_layers.get(mapping.uv_map)
                            if uv is None: raise RuntimeError(f'Missing shader UV map: {o.name}: {mapping.uv_map}')
                        elif mapping.type=='TEX_COORD' and node.inputs['Vector'].links[0].from_socket.name!='UV':
                            raise RuntimeError(f'Non-UV texture coordinates: {o.name}')
                    image={'path':bpy.path.abspath(node.image.filepath),'dimensions':list(node.image.size),'name':node.image.name}
                    if not Path(image['path']).is_file(): raise RuntimeError(f'Missing image: {image}')
                else: procedural=True
        if image and (len(polys)!=1 or len(polys[0].vertices)!=4):
            raise RuntimeError(f'Image surface needs explicit quad conversion: {o.name}')
        if len(groups)>1 and not image:
            warnings.append({'object':o.name,'issue':'Multiple solid materials; dominant material used for collision brush'})
            if mi!=max(groups,key=lambda k:len(groups[k])): continue
            polys=list(mesh.polygons)
        faces=[list(p.vertices) for p in polys]
        # Concave horizontal floors/ceilings are triangulated into solid prisms.
        slab=('floor' in o.name.lower() or 'ceiling' in o.name.lower() or 'connector' in o.name.lower())
        objects.append({'name':o.name,'vertices_m':verts,'faces':faces,
          'triangles':[list(t.vertices) for t in mesh.loop_triangles],
          'face_uvs':[[list(uv.data[i].uv) for i in p.loop_indices] for p in polys] if uv else [],
          'material':m.name if m else '', 'color':list(m.diffuse_color) if m else [.5,.5,.5,1],
          'image':image,'procedural':procedural,'slab':slab and not image})
    evaluated.to_mesh_clear()
out=ROOT/'build/playtest-v18-geometry.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({'blend':bpy.data.filepath,'scene':scene.name,'objects':objects,'warnings':warnings},separators=(',',':')))
result={'export':str(out),'objects':len(objects),'images':sum(bool(o['image']) for o in objects),'warnings':warnings}
print(json.dumps(result))
