"""Read-only Blender material/geometry audit; run with Blender --background --python.

No save, shader substitution, image mutation, or engine installation writes.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/build-results/bo3-transfer'
OUT.mkdir(parents=True, exist_ok=True)
scene = bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene = scene
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()


def material_info(mat):
    result = {'name': mat.name if mat else '<none>', 'kind': 'constant', 'images': []}
    if not mat or not mat.use_nodes:
        return result
    nodes = mat.node_tree.nodes
    output = next((n for n in nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output), None)
    shader = output.inputs['Surface'].links[0].from_node if output and output.inputs['Surface'].is_linked else None
    base = shader.inputs.get('Base Color') if shader else None
    result['shader'] = shader.type if shader else None
    if not base:
        result['kind'] = 'bake_or_manual'
    elif base.is_linked:
        tex = base.links[0].from_node
        result['kind'] = 'direct_image' if tex.type == 'TEX_IMAGE' and tex.image else 'bake_or_manual'
        if result['kind'] == 'direct_image':
            result['base_image'] = tex.image.name
            vector = tex.inputs['Vector']
            result['uv_map'] = None
            result['mapping'] = 'render_uv'
            if vector.is_linked:
                link = vector.links[0]
                result['mapping'] = link.from_node.type + ':' + link.from_socket.name
                if link.from_node.type == 'UVMAP':
                    result['uv_map'] = link.from_node.uv_map
                elif not (link.from_node.type == 'TEX_COORD' and link.from_socket.name == 'UV'):
                    result['kind'] = 'bake_or_manual'
    result['extra_linked_channels'] = [s.name for s in shader.inputs if s.is_linked and s.name != 'Base Color'] if shader else []
    for n in nodes:
        if n.type == 'TEX_IMAGE' and n.image:
            im = n.image
            path = Path(bpy.path.abspath(im.filepath))
            result['images'].append({'name': im.name, 'size': list(im.size), 'packed': bool(im.packed_file),
                                     'source_path': str(path), 'external_exists': path.is_file()})
    return result


materials = {}
objects = []
for obj in sorted(scene.objects, key=lambda o: o.name):
    if obj.type not in {'MESH', 'FONT', 'CURVE'} or obj.hide_render:
        continue
    if any(any(t in c.name.lower() for t in ('archive', 'reference', 'guide', 'planned spawn', 'planning only')) for c in obj.users_collection):
        continue
    evaluated = obj.evaluated_get(deps)
    mesh = evaluated.to_mesh()
    if not mesh:
        continue
    mesh.calc_loop_triangles()
    used = []
    for mi in sorted({p.material_index for p in mesh.polygons}):
        mat = mesh.materials[mi] if mi < len(mesh.materials) else None
        key = mat.name if mat else '<none>'
        if key not in materials:
            materials[key] = material_info(mat)
        used.append(key)
    objects.append({'name': obj.name, 'vertices': len(mesh.vertices), 'triangles': len(mesh.loop_triangles),
                    'materials': used, 'uv_maps': [uv.name for uv in mesh.uv_layers],
                    'negative_determinant': obj.matrix_world.determinant() < 0})
    evaluated.to_mesh_clear()

report = {'source': str(Path(bpy.data.filepath).relative_to(ROOT)),
          'source_sha256': hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
          'blender_version': bpy.app.version_string, 'scene': scene.name,
          'scene_scale_length': scene.unit_settings.scale_length,
          'object_count': len(objects), 'triangles': sum(o['triangles'] for o in objects),
          'material_kinds': dict(Counter(m['kind'] for m in materials.values())),
          'materials': list(materials.values()), 'objects': objects,
          'limits': ['Inventory only; direct_image class covers base colour, not complete PBR equivalence.',
                     'Packed images are available even when their historical external path is absent.',
                     'No model compilation, lighting or runtime result is inferred.']}
(OUT / 'blender-audit.json').write_text(json.dumps(report, indent=2) + '\n')
print('BO3_TRANSFER_AUDIT', json.dumps({k: report[k] for k in ('object_count', 'triangles', 'material_kinds')}), flush=True)
