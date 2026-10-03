"""Correct approach pavement mouth and review framing without altering v21."""
from pathlib import Path
import bpy,json,ast
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-melton-road-v22.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
report=json.loads((ROOT/'recon/v22/validation.json').read_text());path=[Vector(p) for p in report['melton_centreline']]
direction=(path[1]-path[0]).normalized()
for side in (-1,1):
    ob=bpy.data.objects['Street v22 | Roundabout approach pavement '+str(side)]
    for v in ob.data.vertices:
        p=Vector((v.co.x,v.co.y))
        if abs((p-path[0]).dot(direction))<3:
            v.co.x+=direction.x*14;v.co.y+=direction.y*14
c=Vector(report['placeholder_buildings'][-1]['front_centre']);u=(path[-2]-path[-3]).normalized();n=Vector((-u.y,u.x));eye=c+n*7.2
views=[('01_route_overview',(-15,150,350),(-15,150,0),265),('02_roundabout',(-66,-26,24),(-33,1,0),None),('03_melton_player',(*tuple(path[2]),1.7),(*tuple(path[3]),2.8),None),('04_taraj_placeholder',(*tuple(eye),1.7),(*tuple(c),2.8),None)]
for name,eye,target,ortho in views:
    cam=bpy.data.objects['Review v22 | '+name];cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    if ortho:cam.data.ortho_scale=ortho
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True
bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary road review sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.4,-.5,-.4)
for name,eye,target,ortho in views:
    scene.render.resolution_x=1200 if ortho else 1400;scene.render.resolution_y=1600 if ortho else 1000
    scene.camera=bpy.data.objects['Review v22 | '+name];scene.render.filepath=str(ROOT/'recon/v22'/(name+'.png'));bpy.ops.render.render(write_still=True)
