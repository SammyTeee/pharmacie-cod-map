"""Render video-dressed upstairs with temporary cameras/lights; restore settings."""
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.data.scenes['02 First floor - mapped rooms'];previous=bpy.context.window.scene;bpy.context.window.scene=scene
old=(scene.camera,scene.render.engine,scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage,scene.render.filepath)
objects=[]
camdata=bpy.data.cameras.new('Temporary video review');cam=bpy.data.objects.new('Temporary video review',camdata);scene.collection.objects.link(cam);objects.append(cam)
cam.location=(8.0,9.5,6.7);cam.rotation_euler=(Vector((-.5,17.2,5.8))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.lens=24;scene.camera=cam
for x,y in ((2,11),(7,15),(1,19)):
 data=bpy.data.lights.new('Temporary video review light','AREA');data.energy=150;data.shape='DISK';data.size=5
 obj=bpy.data.objects.new(data.name,data);scene.collection.objects.link(obj);obj.location=(x,y,8.1);objects.append(obj)
scene.render.engine='CYCLES';samples=scene.cycles.samples;scene.cycles.samples=12;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.render.filepath=str(ROOT/'assets/blender/video-upstairs-v09.png')
labels=[(o,o.hide_render) for o in scene.objects if o.type=='FONT']
for o,_ in labels:o.hide_render=True
old_world=scene.world
world=bpy.data.worlds.new('Temporary video review world');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.2,.18,.14,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;scene.world=world
try:bpy.ops.render.render(write_still=True)
finally:
 scene.camera,scene.render.engine,scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage,scene.render.filepath=old;scene.cycles.samples=samples
 scene.world=old_world;bpy.data.worlds.remove(world)
 for o,hidden in labels:o.hide_render=hidden
 for o in objects:
  data=o.data;bpy.data.objects.remove(o,do_unlink=True)
  if isinstance(data,bpy.types.Camera):bpy.data.cameras.remove(data)
  else:bpy.data.lights.remove(data)
 bpy.context.window.scene=previous
result={'preview':'assets/blender/video-upstairs-v09.png','temporary_objects_removed':True}
