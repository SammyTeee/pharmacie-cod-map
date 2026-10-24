"""Targeted renders of open room-envelope rays; no geometry changes."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v28-zombies'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True
scene.render.resolution_x=960;scene.render.resolution_y=540;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.7
ld=bpy.data.lights.new('Temporary gap-review sun','SUN');ld.energy=2;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
cd=bpy.data.cameras.new('Temporary gap-review camera');cd.lens=22;cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);scene.camera=cam
for name,eye,target in [('gap_bar_east',(5,17,1.65),(15,17,1.65)),('gap_bar_outside',(14,17,1.65),(5,17,1.65)),('gap_junction_ground',(-31,-18,1.7),(-31,-13,-.2))]:
    cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    if name=='gap_bar_east':
        ld2=bpy.data.lights.new('Temporary bar-review fill','AREA');ld2.energy=180;ld2.size=4;ob=bpy.data.objects.new(ld2.name,ld2);scene.collection.objects.link(ob);ob.location=(5,16,3.8)
    scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print('GAP_REVIEW_COMPLETE',flush=True)
