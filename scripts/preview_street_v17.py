"""Render the saved v17 review cameras, without changing its saved lighting."""
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=True
scene.render.resolution_x=1400;scene.render.resolution_y=850;scene.render.resolution_percentage=100
world=bpy.data.worlds.new('Review daylight');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.60,.70,.85,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.7;scene.world=world
data=bpy.data.lights.new('Review sun','SUN');data.energy=2.5;data.angle=.12
sun=bpy.data.objects.new('Review sun',data);scene.collection.objects.link(sun);sun.rotation_euler=(.5,-.4,-.5)
for o in scene.objects:
    if o.type=='FONT' and not o.name.startswith('Street v17 |'):o.hide_render=True
for name,slug in [('Pub frontage','frontage'),('Whole street','street'),('Alley and rear route','alley'),('Crossing row','crossing')]:
    scene.camera=bpy.data.objects['Review v17 | '+name]
    scene.render.filepath=str(ROOT/'assets/blender'/('street-v17-'+slug+'.png'))
    bpy.ops.render.render(write_still=True)
print('Rendered four v17 previews; blend file unchanged')
