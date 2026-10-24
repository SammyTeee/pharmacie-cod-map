"""Bounded 720p material reviews of the saved checkpoints, never saves source."""
import bpy,json,time,math,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];skate='skate-street-v60' in bpy.data.filepath
DEST=ROOT/('recon/skate-v60' if skate else 'recon/v59');DEST.mkdir(exist_ok=True)
s=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=s
s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True;s.cycles.time_limit=15;s.cycles.max_bounces=4
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 s.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
except Exception:s.cycles.device='CPU'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.use_persistent_data=True
s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=94;s.view_settings.view_transform='AgX';s.view_settings.exposure=0
w=bpy.data.worlds.new('TEMP demo sky');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.73,.85,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.65;s.world=w
ld=bpy.data.lights.new('TEMP demo daylight','SUN');ld.energy=2.5;ld.angle=.1;lo=bpy.data.objects.new(ld.name,ld);s.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
cu=bpy.data.cameras.new('TEMP demo camera');cu.lens=32;cu.clip_start=.04;cu.clip_end=2500;cam=bpy.data.objects.new(cu.name,cu);s.collection.objects.link(cam);s.camera=cam
views=[('street_line',(-24,-10.5,3.8),(12,-5,1.8),None),('flatbar',(8,-10.5,1.8),(17,-7.8,.7),None),('return_ramp',(42,-9.6,1.8),(51,-7.15,1.0),None),('pub_player',(-12,-9,1.75),(5,1,2.0),None),('street_plan',(-5,-3,75),(-5,-3,0),110)]
if not skate:
 d=json.loads((ROOT/'recon/v54/prepared-street.json').read_text())['frontages'];it=min(d,key=lambda i:abs(i['chain_m']-378));f=it['frame'];p=f['origin'];x=f['x'];n=f['y'];basis=Matrix(((x[0],n[0],0,p[0]),(x[1],n[1],0,p[1]),(0,0,1,0),(0,0,0,1)))
 views += [('retail_terrace',tuple(basis@Vector((-24,-18,9))),tuple(basis@Vector((0,0,2.5))),None),('retail_player',tuple(basis@Vector((-17,-8,1.75))),tuple(basis@Vector((0,0,2.5))),None)]
 house=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world
 views += [('house_front',tuple(house@Vector((6,-18,7))),tuple(house@Vector((6,0,1.5))),None)]
 for name,camera in [('rear_alley','Review v30 | 02_alley_services'),('taraj','Review v26 | 05_taraj_entry')]:
  o=bpy.data.objects[camera];direction=o.matrix_world.to_quaternion()@Vector((0,0,-1));views.append((name,tuple(o.matrix_world.translation),tuple(o.matrix_world.translation+direction*10),None))
results=[]
selected=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
for name,eye,target,ortho in views:
 if selected and name not in selected:continue
 cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cu.type='ORTHO' if ortho else 'PERSP';cu.ortho_scale=ortho or 1
 s.render.filepath=str(DEST/(name+'.jpg'));started=time.monotonic();bpy.ops.render.render(write_still=True);results.append({'name':name,'file':name+'.jpg','seconds':time.monotonic()-started,'eye':eye,'target':target})
 (DEST/'render-report.json').write_text(json.dumps({'source':bpy.data.filepath,'engine':'Cycles / 12 samples / denoised / 15 second tracing limit / temporary daylight','device':s.cycles.device,'images':results},indent=2))
 print('DEMO_RENDER_COMPLETE',name,round(results[-1]['seconds'],2),flush=True)
