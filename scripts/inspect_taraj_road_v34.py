from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v34';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU';scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
w=bpy.data.worlds.new('Temporary v34 review');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.82,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;scene.world=w
l=bpy.data.lights.new('Temporary v34 daylight','SUN');l.energy=2.5;o=bpy.data.objects.new(l.name,l);scene.collection.objects.link(o);o.rotation_euler=(.45,-.55,-.45)
c=bpy.data.cameras.new('Temporary v34 camera');c.lens=24;c.clip_end=1000;o=bpy.data.objects.new(c.name,c);scene.collection.objects.link(o);scene.camera=o
views=[('01_unlock',(-15,-6.7,1.57),(-40,-6.7,1.8)),('02_junction',(-31,-6.7,1.57),(-45,9,1.8)),('03_melton',(-56,95,1.57),(-61,130,1.8)),('04_bridge',(-58,197,1.57),(-57,220,1.8)),('05_taraj',(-54,260,1.57),(-64,272,2.5)),('06_plan',(-20,155,350),(-40,155,0))]
(dest/'review-views.json').write_text(json.dumps(views,indent=2))
phase='after' if 'v34' in bpy.data.filepath else 'before'
for name,eye,target in views:
 c.type='ORTHO' if name=='06_plan' else 'PERSP';c.ortho_scale=355
 o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(dest/(name+'_'+phase+'.png'));bpy.ops.render.render(write_still=True)
print('V34_INSPECTION_COMPLETE',phase,flush=True)
