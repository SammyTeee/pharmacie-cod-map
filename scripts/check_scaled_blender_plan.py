"""Read back scale/alignment and capture Blender viewport evidence."""
from pathlib import Path
import bpy
ROOT = Path(__file__).resolve().parents[1]
scene = bpy.context.scene
assert scene['frontage_metres'] == 7.0
assert scene.unit_settings.scale_length == 1.0
planes = [o for o in scene.objects if o.type == 'MESH']
assert len(planes) == 2
assert all(o.data.materials[0].node_tree.nodes.get('Image Texture').image.packed_file for o in planes)
assert all(o['metres_per_pixel'] == scene['metres_per_pixel'] for o in planes)
guide = scene.objects['Frontage width - assumed 7 metres']
points = guide.data.splines[0].points
assert abs((points[1].co.xyz-points[0].co.xyz).length - 7.0) < 0.00001
bpy.ops.screen.screenshot(filepath=str(ROOT / 'build/blender-scaled-plan.png'))
result = {'frontage_guide_m':7.0, 'planes':len(planes), 'packed_original':True,
          'shared_uniform_scale':True, 'screenshot':'build/blender-scaled-plan.png'}
