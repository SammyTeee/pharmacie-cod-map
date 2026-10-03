"""Refine v19 review cameras and replace obstructed/cropped previews."""
from pathlib import Path
import bpy,ast
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-shopfronts-v19.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
tree=ast.parse((ROOT/'scripts/model_shopfronts_v19.py').read_text())
views=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='views' for t in n.targets))
for name,eye,target in views:
    co=bpy.data.objects['Review v19 | '+name];co.location=eye;co.rotation_euler=(Vector(target)-co.location).to_track_quat('-Z','Y').to_euler();co.data.lens=12 if name=='05_neighbour_row' else 28
scene.camera=bpy.data.objects['Review v19 | 01_wreake_front']
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.65,.72,.84,1)
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.55
ld=bpy.data.lights.new('v19 temporary review sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.5,-.5,-.4)
for name,eye,target in views:
    if name in ('02_wreake_recess','06_right_shop_depth'):continue
    scene.camera=bpy.data.objects['Review v19 | '+name];scene.render.filepath=str(ROOT/'recon/v19'/(name+'.png'));bpy.ops.render.render(write_still=True)
