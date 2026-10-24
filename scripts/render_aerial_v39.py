from pathlib import Path
import bpy,json,os
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/showcase/media'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU';scene.render.resolution_x=1600;scene.render.resolution_y=900;scene.render.resolution_percentage=100
w=bpy.data.worlds.new('Temporary aerial review');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.82,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.65;scene.world=w
l=bpy.data.lights.new('Temporary aerial sunlight','SUN');l.energy=2.5;o=bpy.data.objects.new(l.name,l);scene.collection.objects.link(o);o.rotation_euler=(.45,-.55,-.45)
c=bpy.data.cameras.new('Temporary aerial camera');c.lens=35;c.clip_end=1500;o=bpy.data.objects.new(c.name,c);scene.collection.objects.link(o);scene.camera=o
views=[('aerial-01','Whole street',(-220,35,300),(-30,145,0)),('aerial-02','Pub and road junction',(-72,-68,72),(-20,15,0)),('aerial-03','Melton Road',(-130,120,95),(-57,147,0)),('aerial-04','Brook crossing and Taraj',(8,235,70),(-60,260,0))]
for name,title,eye,target in views:
 if os.environ.get('AERIAL_ONLY') and name!=os.environ['AERIAL_ONLY']:continue
 c.lens=28 if name=='aerial-01' else 35
 o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();scene.render.image_settings.file_format='JPEG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.quality=94;scene.render.filepath=str(dest/(name+'.jpg'));bpy.ops.render.render(write_still=True)
(ROOT/'recon/showcase/aerial-views.json').write_text(json.dumps(views,indent=2));print('AERIAL_V39_COMPLETE',flush=True)
