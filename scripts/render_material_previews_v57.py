"""Textured review of saved v57, without saving scene changes."""
from pathlib import Path
import bpy,json,os,time
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v57/materials';dest.mkdir(parents=True,exist_ok=True)
assert Path(bpy.data.filepath).name=='pharmacie-surveyed-route-v57.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True;scene.cycles.time_limit=20
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='OPTIX';prefs.get_devices()
 for device in prefs.devices:device.use=device.type=='OPTIX'
 scene.cycles.device='GPU' if any(d.use for d in prefs.devices) else 'CPU'
except Exception:scene.cycles.device='CPU'
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.use_persistent_data=True
scene.render.image_settings.file_format='JPEG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.quality=94
scene.render.film_transparent=False;scene.view_settings.view_transform='AgX';scene.view_settings.exposure=0
world=bpy.data.worlds.new('TEMP v57 material review daylight');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.73,.85,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65;scene.world=world
light=bpy.data.lights.new('TEMP review sunlight','SUN');light.energy=2.5;light.angle=.1
sun=bpy.data.objects.new(light.name,light);scene.collection.objects.link(sun);sun.rotation_euler=(.45,-.55,-.45)
cu=bpy.data.cameras.new('TEMP material review camera');cam=bpy.data.objects.new(cu.name,cu);scene.collection.objects.link(cam);scene.camera=cam;cu.clip_end=3000;cu.lens=32
house=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world.copy()
schedule=json.loads((ROOT/'recon/v54/prepared-street.json').read_text())['frontages']
def frame(chain):
 item=min(schedule,key=lambda i:abs(i['chain_m']-chain) if i['chain_m']>166 else 1e6);f=item['frame'];p=f['origin'];x=f['x'];n=f['y']
 return Matrix(((x[0],n[0],0,p[0]),(x[1],n[1],0,p[1]),(0,0,1,0),(0,0,0,1)))
views=[('house_front','Your house',house,(6,-18,7),(6,0,1.5),None),('house_porch','Porch detail',house,(-2,-6.5,3.7),(3.8,-.7,1.2),None),('holmdale','Holmdale Road',house,(-25,-36,28),(12,0,0),None),('junction_shops','Station junction',frame(196),(-21,-18,7),(2,0,2.5),None),('retail_terrace','Melton Road terraces',frame(378),(-24,-18,9),(0,0,2.5),None),('hall_cafe','Hall and cafe vicinity',frame(500),(-24,-20,8),(1,0,2.5),None),('supermarket','Supermarket stretch',frame(594),(-38,-38,20),(0,4,2),None),('barkby','Barkby Road',Matrix.Identity(4),(-95,-25,45),(-98,37,0),None),('route_overview','Whole connected route',Matrix.Identity(4),(-450,470,950),(-35,470,0),1180),('pub','Pub and junction',Matrix.Identity(4),(-38,-35,20),(0,8,2),None)]
selected=os.environ.get('PREVIEW_ONLY');results=[]
report=dest/'render-report.json'
if report.exists():results=json.loads(report.read_text())['images']
for name,title,basis,eye,target,ortho in views:
 if selected and name!=selected:continue
 if not selected and any(r['name']==name and (dest/r['file']).exists() for r in results):continue
 cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cu.type='ORTHO' if ortho else 'PERSP';cu.ortho_scale=ortho or 1
 scene.render.filepath=str(dest/(name+'.jpg'));start=time.monotonic();bpy.ops.render.render(write_still=True)
 results=[r for r in results if r['name']!=name]+[{'name':name,'title':title,'file':name+'.jpg','seconds':time.monotonic()-start,'eye':list(cam.location)}]
 report.write_text(json.dumps({'source':bpy.data.filepath,'engine':'Cycles 8 samples, denoised, temporary daylight','device':scene.cycles.device,'images':results,'missing_images':[i.filepath for i in bpy.data.images if i.source=='FILE' and not i.packed_file and i.filepath and not Path(bpy.path.abspath(i.filepath)).exists()],'limits':'Material renders of existing v57, no model edits or engine deployment. Dimensions and hidden detail retain documented estimates.'},indent=2)+'\n')
 print('PREVIEW_COMPLETE',name,round(time.monotonic()-start,2),flush=True)
