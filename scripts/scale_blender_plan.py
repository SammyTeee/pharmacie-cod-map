"""Prepare aligned floor-plan tracing planes in a new scene, preserving existing work."""
from pathlib import Path
import math
import bpy
from mathutils import Quaternion

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/pharmacie-syston/floor plan of downstairs and upstairs council to scale.png'
OUT = ROOT / 'assets/blender/pharmacie-scaled-plan.blend'
WIDTH_M = 7.0
# Manually inspected outside frontage endpoints on the original raster.
# This calibrates an estimate, not a dimension recovered from the drawing.
GROUND_ANCHOR = (205, 119)
FIRST_ANCHOR = (208, 516)
FRONTAGE_PIXELS = 222.0
METRES_PER_PIXEL = WIDTH_M / FRONTAGE_PIXELS

scene = bpy.data.scenes.new('Pharmacie - scaled tracing base')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'
scene.unit_settings.scale_length = 1.0
scene['frontage_metres'] = WIDTH_M
scene['scale_status'] = 'User estimate, NOT surveyed; shared uniform scale for both floors'
scene['metres_per_pixel'] = METRES_PER_PIXEL
scene['floor_height_status'] = 'No floor elevation chosen: both tracing planes at Z=0; toggle visibility'
scene['alignment_status'] = 'Front upper corner aligned by translation; no perspective/skew correction'

image = bpy.data.images.load(str(SOURCE), check_existing=True)
image.pack()
width, height = image.size
assert (width, height) == (1264, 874), (width, height)
material = bpy.data.materials.new('Original council plan - packed image')
material.use_nodes = True
nodes = material.node_tree.nodes
nodes.clear()
tex = nodes.new('ShaderNodeTexImage')
tex.image = image
emission = nodes.new('ShaderNodeEmission')
output = nodes.new('ShaderNodeOutputMaterial')
material.node_tree.links.new(tex.outputs['Color'], emission.inputs['Color'])
material.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])

def collection(name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c

ground = collection('01 Ground floor reference - visible')
first = collection('02 First floor reference - toggle to trace')
guides = collection('03 Scale guides - frontage estimate')
for name in ('04 Ground floor traced geometry', '05 First floor traced geometry', '06 Props', '07 Collision guides'):
    collection(name)

def world(pixel, anchor):
    px, py = pixel
    ax, ay = anchor
    return ((py-ay)*METRES_PER_PIXEL, (px-ax)*METRES_PER_PIXEL, -0.02)

def plane(name, bounds, anchor, c):
    x0, y0, x1, y1 = bounds
    corners = [(x0,y0), (x0,y1), (x1,y1), (x1,y0)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([world(p,anchor) for p in corners], [], [(0,1,2,3)])
    mesh.uv_layers.new(name='Original image crop - source untouched')
    for loop in mesh.loops:
        px, py = corners[loop.vertex_index]
        mesh.uv_layers.active.data[loop.index].uv = (px/width, 1-py/height)
    obj = bpy.data.objects.new(name, mesh)
    c.objects.link(obj)
    obj.data.materials.append(material)
    obj.hide_select = True
    obj['source'] = SOURCE.name
    obj['reference_region_pixels'] = list(bounds)
    obj['front_corner_pixel'] = list(anchor)
    obj['metres_per_pixel'] = METRES_PER_PIXEL
    obj['status'] = 'Reference plane only; not map geometry'
    return obj

plane('Ground floor - 7m estimated frontage', (190,60,1028,393), GROUND_ANCHOR, ground)
upstairs = plane('First floor - same scale, aligned front corner', (190,460,900,748), FIRST_ANCHOR, first)
upstairs.hide_set(True)

def line(name, points):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = 0.018
    poly = curve.splines.new('POLY')
    poly.points.add(len(points)-1)
    for p, co in zip(poly.points, points):
        p.co = (*co,1)
    obj = bpy.data.objects.new(name, curve)
    guides.objects.link(obj)
    return obj

line('Frontage width - assumed 7 metres', [(0,-0.6,0.01),(7,-0.6,0.01)])
for i in range(8):
    line(f'Metre tick {i}', [(i,-0.8,0.01),(i,-0.4,0.01)])
font = bpy.data.curves.new('Estimate label', 'FONT')
font.body = '7 m frontage ESTIMATE | each tick = 1 m'
font.size = 0.28
label = bpy.data.objects.new('Scale assumption - not measured',font)
guides.objects.link(label)
label.location = (0,-1.25,0.01)

for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.shading.type = 'MATERIAL'
            space.region_3d.view_rotation = Quaternion((1,0,0,0))
            space.region_3d.view_perspective = 'ORTHO'
            space.region_3d.view_location = (3.5,12,0)
            space.region_3d.view_distance = 44

assert math.isclose(FRONTAGE_PIXELS*METRES_PER_PIXEL, 7.0)
assert math.isclose((world((205,341),GROUND_ANCHOR)[0]),7.0)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result = {'file':str(OUT), 'frontage_m':7.0, 'metres_per_pixel':METRES_PER_PIXEL,
          'source_pixels':[width,height], 'reference_planes':2, 'status':'estimated scale; no building geometry'}
print(result)
