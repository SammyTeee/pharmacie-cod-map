"""Create a separate reference-only scene; preserve source images and BO3 map."""
from pathlib import Path
import bpy
from mathutils import Quaternion

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/blender/pharmacie-reference-base.blend'
OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
refs = bpy.data.collections.new('References - original plan, estimated scale')
scene.collection.children.link(refs)
image = bpy.data.images.load(str(ROOT / 'hq floor plan ai.png'))
image.pack()
# Display original full sheet, without cropping/repainting. Frontage spans
# roughly 280 pixels in the ground-floor plan. Seven metres is Sam's estimate.
obj = bpy.data.objects.new('Floor plan - 7m frontage estimate, unmeasured', None)
refs.objects.link(obj)
obj.empty_display_type = 'IMAGE'
obj.data = image
obj.empty_display_size = 7.0 * max(image.size) / 280.0
obj.color[3] = 0.65
obj.empty_image_depth = 'BACK'
obj.location = (0, 0, -0.05)
obj['scale_status'] = 'Provisional: frontage estimated 7m; dimensions unverified'
obj['source'] = 'hq floor plan ai.png; original unchanged; packed for portability'
obj.hide_select = True
for name in ('Ground floor geometry', 'First floor geometry', 'Props', 'BO3 collision guides'):
    scene.collection.children.link(bpy.data.collections.new(name))
scene['workflow'] = 'Blender modelling -> validated BO3 assets/geometry -> Radiant collision, entities, navigation, lighting and compile'
scene['status'] = 'Reference setup only; no building geometry or BO3 conversion yet'
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            region = area.spaces.active.region_3d
            region.view_rotation = Quaternion((1, 0, 0, 0))
            region.view_perspective = 'ORTHO'
            region.view_distance = 45
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
print('Saved reference base:', OUT)
