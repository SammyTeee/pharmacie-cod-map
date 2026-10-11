"""Move the complete Taraj bar across the room, keeping its front bay."""
from pathlib import Path
import bpy, json, math
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name == 'pharmacie-retail-detail-v39.blend'
scene = bpy.context.scene
basis = bpy.data.objects['Detail v26 | Taraj | carpet floor'].matrix_world.copy()
parts = ('bar ', 'backbar', 'fridge', 'optic', 'spirit', 'cash drawer',
         'POS screen', 'shelf tumbler', 'violet shelf', 'beer tap',
         'tap handle', 'mirror backing', 'chilled drink bottle')
objects = [o for o in scene.objects if o.name.startswith('Detail v26 | Taraj | ')
           and any(s in o.name for s in parts)]
assert len(objects) > 90
assert all(o.parent is None for o in objects)
original = {o.name: o.matrix_world.copy() for o in bpy.data.objects}
# Proper 180-degree rotation, not a reflection: labels and normals stay correct.
# The wall faces are x=-3 and x=5.8; bar remains in y=1.3..4.2,
# before the first right booth and clear of the side entrance.
local = Matrix.Translation((2.8, 5.5, 0)) @ Matrix.Rotation(math.pi, 4, 'Z')
transform = basis @ local @ basis.inverted()
preview = ROOT / 'recon/v40'
preview.mkdir(parents=True, exist_ok=True)
bpy.ops.screen.screenshot(filepath=str(preview / 'taraj-before.png'))
for o in objects:
    o.matrix_world = transform @ original[o.name]
bpy.context.view_layer.update()
moved = {o.name for o in objects}
assert all(max(abs(o.matrix_world[r][c] - original[o.name][r][c])
               for r in range(4) for c in range(4)) < 1e-5
           for o in bpy.data.objects if o.name not in moved)
deps = bpy.context.evaluated_depsgraph_get()
checks = []
def ray(a, b, label):
    start, end = basis @ Vector(a), basis @ Vector(b)
    delta = end - start
    hit, pos, normal, index, obj, matrix = scene.ray_cast(
        deps, start, delta.normalized(), distance=delta.length)
    assert not hit, (label, obj.name)
    checks.append(label)
for z in (.35, .85, 1.65):
    for y in (4.25, 4.5, 4.75):
        ray((-4.4, y, z), (-.18, y, z), 'side entry')
    for x in (-.18, 3.12):
        for dx in (-.25, 0, .25):
            ray((x+dx, 4.5, z), (x+dx, 13.85, z), 'dining aisle')
    for x in (2.87, 3.12, 3.37):
        ray((x, 1.3, z), (x, 4.5, z), 'bar approach')
report = {'source': 'assets/blender/pharmacie-retail-detail-v39.blend',
          'checkpoint': 'assets/blender/pharmacie-taraj-bar-v40.blend',
          'reason': 'Sam corrected bar to opposite wall while looking across side entrance',
          'moved_objects': sorted(moved), 'rotation_degrees': 180,
          'local_transform': [list(r) for r in local],
          'unchanged_other_object_transforms': len(original)-len(moved),
          'mesh_data': 'unchanged; object transforms only',
          'clear_route_rays': len(checks),
          'limits': 'Blender sampled rays only; BO3 unchanged'}
(preview / 'validation.json').write_text(json.dumps(report, indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / report['checkpoint']))
print(json.dumps({'moved': len(moved), 'clear_route_rays': len(checks), 'saved': bpy.data.filepath}))
