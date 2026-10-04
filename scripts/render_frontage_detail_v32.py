"""Matching before/after views plus temporary new-geometry highlight."""
from pathlib import Path
import bpy,json,os,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v32'
source=ROOT/'assets/blender/pharmacie-zombies-street-v31.blend';after=ROOT/'assets/blender/pharmacie-street-frontages-v32.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
views=[(o.name.split('|')[-1].strip(),list(o.location),list(o.rotation_euler),o.data.lens,o.data.type,o.data.ortho_scale) for o in scene.objects if o.type=='CAMERA' and o.name.startswith(('Review v31 |','Review v32 |'))]

if os.environ.get('V31_PLAN_ONLY'):views=[v for v in views if v[0]=='08_street_plan']
def setup():
    s=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=s
    s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
    w=bpy.data.worlds.new('Temporary v31 review daylight');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.82,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;s.world=w
    ld=bpy.data.lights.new('Temporary v31 review sun','SUN');ld.energy=2.5;lo=bpy.data.objects.new(ld.name,ld);s.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
    ld=bpy.data.lights.new('Temporary v31 bar fill','AREA');ld.energy=160;ld.size=4;lo=bpy.data.objects.new(ld.name,ld);s.collection.objects.link(lo);lo.location=(5,16,3.8)
    return s
def render(s,v,path):
    name,pos,rot,lens,typ,scale=v;cd=bpy.data.cameras.new('Temporary review camera');cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);cam.location=pos;cam.rotation_euler=rot;cd.lens=lens;cd.type=typ;cd.ortho_scale=scale;s.camera=cam;s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
scene=setup()
for v in views:render(scene,v,dest/(v[0]+'_after.png'))
# Gold new walls/props and green floors are temporary review overrides only.
gold=bpy.data.materials.new('Temporary NEW geometry gold');gold.diffuse_color=(.95,.43,.035,1);gold.use_nodes=True;gold.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=gold.diffuse_color
green=bpy.data.materials.new('Temporary NEW walkable floors green');green.diffuse_color=(.12,.55,.23,1);green.use_nodes=True;green.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=green.diffuse_color
for o in scene.objects:
    if o.type=='MESH' and o.name.startswith('Street v32 |') and o.get('mapping_role')!='terrain_backing':
        o.data.materials.clear();o.data.materials.append(green if o.get('mapping_role')=='walkable_floor' else gold)
for v in views:
    if v[0] in ('02_street_combat','09_opposite_shop_detail','08_street_plan'):render(scene,v,dest/(v[0]+'_highlight.png'))
if not os.environ.get('V31_AFTER_ONLY'):
    bpy.ops.wm.open_mainfile(filepath=str(source));scene=setup()
    for v in views:
        if v[0] in ('02_street_combat','09_opposite_shop_detail','10_fox_street_furniture','11_crossing_approach'):render(scene,v,dest/(v[0]+'_before.png'))
(dest/'views.json').write_text(json.dumps(views,indent=2))
print('V32_RENDER_COMPLETE',flush=True)
