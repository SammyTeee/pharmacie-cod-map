"""New standalone tracing project; run with Blender --background --python."""
from pathlib import Path
import hashlib
import json
import bpy
from mathutils import Quaternion

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Architectural Fire Evacuation Floor Plans.png'
OUT = ROOT / 'assets/blender/pharmacie-evacuation-plan.blend'
if OUT.exists():
    raise RuntimeError('Output already exists; preserve modelling work and choose a new filename')
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = 'Pharmacie - new evacuation plan'
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'
SCALE = 7 / 316
scene['frontage_metres'] = 7.0
scene['metres_per_pixel'] = SCALE
scene['scale_status'] = 'Estimated 7m across ground outer frontage, pixels (82,85) to (82,401); not surveyed'
scene['status'] = 'Aligned tracing references and footprint guides; no playable geometry or export yet'
scene['alignment'] = 'Front upper corners translated to same origin; shared scale; drawing skew retained'
image = bpy.data.images.load(str(SOURCE))
assert tuple(image.size) == (1393,1129)
image.pack()
mat = bpy.data.materials.new('Packed original evacuation drawing')
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()
tex = nodes.new('ShaderNodeTexImage')
tex.image = image
em = nodes.new('ShaderNodeEmission')
out = nodes.new('ShaderNodeOutputMaterial')
mat.node_tree.links.new(tex.outputs['Color'], em.inputs['Color'])
mat.node_tree.links.new(em.outputs[0], out.inputs['Surface'])

def col(name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c

def world(p, anchor, z=0):
    return ((p[1]-anchor[1])*SCALE, (p[0]-anchor[0])*SCALE, z)

def reference(name, bounds, anchor, collection):
    x0,y0,x1,y1 = bounds
    points = [(x0,y0),(x0,y1),(x1,y1),(x1,y0)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([world(p,anchor,-0.02) for p in points], [], [(0,1,2,3)])
    uv = mesh.uv_layers.new()
    for loop in mesh.loops:
        x,y = points[loop.vertex_index]
        uv.data[loop.index].uv = (x/1393,1-y/1129)
    obj = bpy.data.objects.new(name,mesh)
    collection.objects.link(obj)
    mesh.materials.append(mat)
    obj.hide_select = True
    obj['source_region_pixels'] = list(bounds)
    obj['anchor_pixel'] = list(anchor)
    return obj

def line(name, coordinates, collection, closed=False):
    data = bpy.data.curves.new(name,'CURVE')
    data.dimensions = '3D'
    data.bevel_depth = 0.012
    spline = data.splines.new('POLY')
    spline.points.add(len(coordinates)-1)
    for p,co in zip(spline.points,coordinates):
        p.co = (*co,1)
    spline.use_cyclic_u = closed
    obj = bpy.data.objects.new(name,data)
    collection.objects.link(obj)
    obj['status'] = 'Tracing guide only; not collision or wall mesh'
    return obj

ground = col('01 Ground reference')
first = col('02 First reference - hidden, toggle eye')
guides = col('03 Scale guides')
gf = col('04 Ground footprint guide')
ff = col('05 First footprint guide - hidden, toggle eye')
for name in ('06 Ground walls and openings','07 First walls and openings','08 Bar and props','09 Stairs','10 BO3 collision guides'):
    col(name)
reference('Ground floor original plan',(60,0,1340,465),(82,85),ground)
up = reference('First floor original plan',(55,490,1150,965),(76,558),first)
up.hide_set(True)
outline_g = [(82,85),(174,91),(365,91),(1005,20),(1016,327),(778,355),(778,373),(284,401),(82,401),(82,337),(130,290),(158,290),(158,201),(130,198),(82,151)]
outline_f = [(76,558),(172,566),(346,567),(1096,501),(1120,828),(813,856),(813,865),(302,885),(76,885)]
line('Approximate ground outer footprint',[world(p,(82,85),0.015) for p in outline_g],gf,True)
f = line('Approximate first outer footprint',[world(p,(76,558),0.015) for p in outline_f],ff,True)
f.hide_set(True)
guide = line('7 m frontage estimate',[(0,-0.6,0.02),(7,-0.6,0.02)],guides)
for i in range(8):
    line(f'Metre tick {i}',[(i,-0.8,0.02),(i,-0.4,0.02)],guides)
font = bpy.data.curves.new('Scale label','FONT')
font.body = '7 m frontage estimate | 1 m ticks | NOT a measured survey'
font.size = 0.23
label = bpy.data.objects.new('Estimated scale',font)
guides.objects.link(label)
label.location = (0,-1.3,0.02)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.shading.type = 'MATERIAL'
            space.region_3d.view_rotation = Quaternion((1,0,0,0))
            space.region_3d.view_perspective = 'ORTHO'
            space.region_3d.view_location = (3.5,11,0)
            space.region_3d.view_distance = 35
assert abs((guide.data.splines[0].points[1].co-guide.data.splines[0].points[0].co).length-7)<1e-6
OUT.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
manifest = {'file':OUT.name,'source':SOURCE.name,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_dimensions':[1393,1129],'frontage_estimate_m':7,'frontage_pixels':316,'metres_per_pixel':SCALE,'ground_anchor':[82,85],'first_anchor':[76,558],'edits':'None; packed original, UV regions only','status':'Tracing setup; approximate footprint curves, no wall meshes; BO3 conversion unverified'}
(OUT.parent/'evacuation-plan-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest))
