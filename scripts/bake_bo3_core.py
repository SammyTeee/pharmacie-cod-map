"""Bake procedural core base colour, preserving original object/generated coordinates.

Photo images and their UVs bypass baking. Run on the unchanged v59 file.
This bakes colour only: BO3 lighting/roughness/normals still need their own tuning.
"""
from pathlib import Path
import json
import time
import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/bo3-core'
manifest = json.loads((OUT / 'manifest.json').read_text())
scene = bpy.data.scenes.new('Temporary BO3 colour baking')
bpy.context.window.scene = scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 1
scene.cycles.use_denoising = False
scene.render.threads_mode = 'FIXED'
scene.render.threads = 8
scene.render.bake.margin = 8
scene.render.bake.use_clear = True
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1
started = time.monotonic()
records = []
for info in manifest['materials']:
    if info['kind'] != 'bake' or not info.get('triangles'):
        continue
    data_path = OUT / (info['asset'] + '.json')
    triangles = json.loads(data_path.read_text())
    mat = bpy.data.materials[info['name']].copy()
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    output = next(n for n in nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output)
    original = output.inputs['Surface'].links[0].from_node
    color = original.inputs.get('Base Color')
    if color is None:
        raise RuntimeError('Unsupported bake shader: ' + info['name'])
    emission = nodes.new('ShaderNodeEmission')
    if color.is_linked:
        links.new(color.links[0].from_socket, emission.inputs['Color'])
    else:
        emission.inputs['Color'].default_value = color.default_value
    links.new(emission.outputs[0], output.inputs['Surface'])
    local_attr = nodes.new('ShaderNodeAttribute')
    local_attr.attribute_name = 'pc65_original_object'
    generated_attr = nodes.new('ShaderNodeAttribute')
    generated_attr.attribute_name = 'pc65_original_generated'
    for n in list(nodes):
        if n.type == 'TEX_COORD':
            if n.object:
                raise RuntimeError('Explicit texture object needs separate mapping: ' + info['name'])
            for socket, attr in [('Object', local_attr), ('Generated', generated_attr)]:
                for link in list(n.outputs[socket].links):
                    links.new(attr.outputs['Vector'], link.to_socket)
        # Procedural texture nodes default to generated coordinates.
        if n.type.startswith('TEX_') and n.type != 'TEX_COORD' and n.inputs.get('Vector') and not n.inputs['Vector'].is_linked:
            links.new(generated_attr.outputs['Vector'], n.inputs['Vector'])
    verts, faces, originals, generated, known = [], [], [], [], {}
    for tri_index, tri in enumerate(triangles):
        face = []
        for corner in tri:
            # Keep coincident source faces distinct through Blender's edit BMesh.
            key = (tri_index,) + tuple(round(v, 7) for v in corner[:3] + corner[8:])
            if key not in known:
                known[key] = len(verts)
                verts.append(corner[:3])
                originals.append(corner[8:11])
                generated.append(corner[11:14])
            face.append(known[key])
        faces.append(face)
    mesh = bpy.data.meshes.new(info['asset'])
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for name, values in [('pc65_original_object', originals), ('pc65_original_generated', generated)]:
        attr = mesh.attributes.new(name, 'FLOAT_VECTOR', 'POINT')
        attr.data.foreach_set('vector', [x for v in values for x in v])
    uv = mesh.uv_layers.new(name='pc65_baked_colour')
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(info['asset'], mesh)
    scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=.006)
    bpy.ops.object.mode_set(mode='OBJECT')
    uv = mesh.uv_layers.active
    assert len(mesh.polygons) == len(triangles), 'Bake changed source face count'
    image = bpy.data.images.new(info['asset'] + '_bake', width=2048, height=2048, alpha=False)
    image.colorspace_settings.name = 'sRGB'
    target = nodes.new('ShaderNodeTexImage')
    target.image = image
    nodes.active = target
    print('BAKE_START', info['name'], len(faces), flush=True)
    bpy.ops.object.bake(type='EMIT')
    image.filepath_raw = str(OUT / 'images' / (info['asset'] + '.png'))
    image.file_format = 'PNG'
    image.save()
    for tri, poly in zip(triangles, mesh.polygons):
        for corner, li in zip(tri, poly.loop_indices):
            corner[6:8] = list(uv.data[li].uv)
    data_path.write_text(json.dumps(triangles, separators=(',', ':')))
    info.update(kind='baked_image', source=str(Path(image.filepath_raw).relative_to(ROOT)),
                dimensions=[2048, 2048], extension='EXTEND',
                bake='Emission of original base-colour graph; original object/generated coordinates stored as mesh attributes.')
    records.append({'material': info['name'], 'triangles': len(faces), 'image': info['source']})
    bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.meshes.remove(mesh)
    bpy.data.materials.remove(mat)
    bpy.data.images.remove(image)
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('BAKE_DONE', info['name'], round(time.monotonic()-started, 1), flush=True)
report = {'baked_materials': records, 'seconds': time.monotonic()-started,
          'scope': 'Base colour only. Original Blender source not saved; photo pixels/UVs bypass baking.'}
(OUT / 'bake-report.json').write_text(json.dumps(report, indent=2) + '\n')
