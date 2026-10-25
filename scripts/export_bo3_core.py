"""Export evaluated v59 core triangles and material inputs without saving Blender.

Run Blender --background <v59.blend> --python scripts/export_bo3_core.py.
Triangle clipping interpolates every corner attribute; no bounding-box geometry.
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/bo3-core'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'images').mkdir(exist_ok=True)
BOUNDS = ((-55, 68), (-30, 38), (-4, 24))
scene = bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene = scene
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
materials = {}
groups = defaultdict(list)
objects = []


def describe(mat):
    name = mat.name if mat else '<none>'
    if name in materials:
        return materials[name]
    info = {'name': name, 'asset': 'pc65_' + hashlib.sha256(name.encode()).hexdigest()[:12], 'kind': 'constant',
            'color_linear': list(mat.diffuse_color) if mat else [.5, .5, .5, 1]}
    if mat and mat.use_nodes:
        output = next((n for n in mat.node_tree.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output), None)
        shader = output.inputs['Surface'].links[0].from_node if output and output.inputs['Surface'].is_linked else None
        color = shader.inputs.get('Base Color') if shader else None
        if not color and shader and shader.type == 'EMISSION':
            color = shader.inputs['Color']
            info['emissive'] = True
        info['kind'] = 'bake' if not color or color.is_linked else 'constant'
        if color and not color.is_linked:
            info['color_linear'] = list(color.default_value)
        if color and color.is_linked:
            tex = color.links[0].from_node
            if tex.type == 'TEX_IMAGE' and tex.image:
                info['kind'] = 'image'
                info['uv_map'] = None
                if tex.inputs['Vector'].is_linked:
                    link = tex.inputs['Vector'].links[0]
                    if link.from_node.type == 'UVMAP':
                        info['uv_map'] = link.from_node.uv_map
                    elif not (link.from_node.type == 'TEX_COORD' and link.from_socket.name == 'UV'):
                        info['kind'] = 'bake'
                image = tex.image
                raw = bytes(image.packed_file.data) if image.packed_file else Path(bpy.path.abspath(image.filepath)).read_bytes()
                digest = hashlib.sha256(raw).hexdigest()
                path = OUT / 'images' / (digest + '.source')
                if not path.exists():
                    path.write_bytes(raw)
                info.update(source=str(path.relative_to(ROOT)), source_sha256=digest,
                            source_name=image.name, dimensions=list(image.size), extension=tex.extension)
        if shader:
            for key, socket in [('roughness', 'Roughness'), ('metallic', 'Metallic')]:
                s = shader.inputs.get(socket)
                info[key] = float(s.default_value) if s and not s.is_linked else None
            info['other_linked_channels'] = [s.name for s in shader.inputs if s.is_linked and s.name != 'Base Color']
    materials[name] = info
    return info


def clip(poly, axis, boundary, sign):
    result = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        da = (a[axis] - boundary) * sign
        db = (b[axis] - boundary) * sign
        if da <= 0:
            result.append(a)
        if (da < 0 < db) or (db < 0 < da):
            t = da / (da - db)
            result.append([x + t * (y-x) for x, y in zip(a, b)])
    return result


for obj in sorted(scene.objects, key=lambda o: o.name):
    if obj.type not in {'MESH', 'FONT', 'CURVE'} or obj.hide_render:
        continue
    if any(c.hide_render or any(s in c.name.lower() for s in ('archive', 'reference', 'guide', 'planning only', 'planned spawn')) for c in obj.users_collection):
        continue
    bb = [obj.matrix_world @ Vector(p) for p in obj.bound_box]
    if any(max(p[i] for p in bb) < lo or min(p[i] for p in bb) > hi for i, (lo, hi) in enumerate(BOUNDS)):
        continue
    evaluated = obj.evaluated_get(deps)
    mesh = evaluated.to_mesh()
    if not mesh or not mesh.polygons:
        if mesh:
            evaluated.to_mesh_clear()
        continue
    mesh.calc_loop_triangles()
    normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
    default_uv = next((u for u in mesh.uv_layers if u.active_render), mesh.uv_layers.active)
    source_coords = [v.co.copy() for v in mesh.vertices]
    lo = Vector(tuple(min(v[i] for v in source_coords) for i in range(3)))
    size = Vector(tuple(max(v[i] for v in source_coords)-lo[i] for i in range(3)))
    negative = obj.matrix_world.determinant() < 0
    count = 0
    used = set()
    for tri in mesh.loop_triangles:
        mat = mesh.materials[tri.material_index] if tri.material_index < len(mesh.materials) else None
        info = describe(mat)
        uv = mesh.uv_layers.get(info.get('uv_map')) if info.get('uv_map') else default_uv
        if info['kind'] == 'image' and uv is None:
            raise RuntimeError('Image without required UV layer: ' + obj.name)
        corners = []
        indices = list(tri.loops)
        if negative:
            indices.reverse()
        for li in indices:
            local = source_coords[mesh.loops[li].vertex_index]
            pos = obj.matrix_world @ local
            normal = (normal_matrix @ mesh.corner_normals[li].vector).normalized()
            tex = list(uv.data[li].uv) if uv else [0, 0]
            generated = [(local[i]-lo[i])/size[i] if size[i] else 0 for i in range(3)]
            corners.append(list(pos) + list(normal) + tex + list(local) + generated)
        poly = corners
        for axis, (low, high) in enumerate(BOUNDS):
            poly = clip(poly, axis, low, -1) if poly else []
            poly = clip(poly, axis, high, 1) if poly else []
        for i in range(1, len(poly)-1):
            points = [poly[0], poly[i], poly[i+1]]
            if (Vector(points[1][:3])-Vector(points[0][:3])).cross(Vector(points[2][:3])-Vector(points[0][:3])).length < 1e-9:
                continue
            groups[info['name']].append(points)
            count += 1
        if poly:
            used.add(info['name'])
    objects.append({'name': obj.name, 'source_triangles': len(mesh.loop_triangles), 'exported_triangles': count, 'materials': sorted(used)})
    evaluated.to_mesh_clear()
    if len(objects) % 500 == 0:
        print('CORE_EXPORT_OBJECTS', len(objects), flush=True)

for name, triangles in groups.items():
    info = materials[name]
    (OUT / (info['asset'] + '.json')).write_text(json.dumps(triangles, separators=(',', ':')))
    info['triangles'] = len(triangles)
manifest = {'source': str(Path(bpy.data.filepath).relative_to(ROOT)),
            'source_sha256': hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
            'bounds_BU': BOUNDS, 'objects': objects, 'materials': list(materials.values()),
            'corner_layout': 'world xyz, world normal xyz, Blender uv, original object xyz, original generated xyz',
            'geometry': 'Evaluated triangles, clipped at core boundary; no visual simplification or box substitutes.'}
(OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('CORE_EXPORT_DONE', len(objects), sum(len(v) for v in groups.values()), len(materials), flush=True)
