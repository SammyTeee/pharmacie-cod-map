"""1080p/30 distinct-frame tour; streaming encoder and resumable section clips."""
from pathlib import Path
import bpy,json,os,math,subprocess,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v34';build=ROOT/'build'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
fast=os.environ.get('V34_FAST')=='1'
viewport=os.environ.get('V34_VIEWPORT')=='1'
engine='BLENDER_WORKBENCH' if viewport else 'BLENDER_EEVEE' if fast else os.environ.get('V34_RENDER_ENGINE','CYCLES');scene.render.engine=engine
if engine=='CYCLES':
 scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.cycles.denoiser='OPTIX';scene.cycles.max_bounces=6
 pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
 for d in pref.devices:d.use=d.type=='OPTIX'
 scene.cycles.device='GPU';scene.render.use_persistent_data=True
elif engine=='BLENDER_EEVEE':
 scene.eevee.taa_render_samples=4 if fast else 64;scene.eevee.use_raytracing=not fast;scene.eevee.use_fast_gi=not fast
 if fast:scene.eevee.shadow_ray_count=1;scene.eevee.shadow_step_count=2
else:
 shade=scene.display.shading;shade.light='STUDIO';shade.color_type='TEXTURE';shade.show_shadows=True;shade.show_cavity=True;shade.cavity_type='WORLD';shade.show_specular_highlight=True;shade.background_type='WORLD'
 scene.display.render_aa='8';scene.render.film_transparent=False
scene.render.resolution_x=1280 if fast else 1920;scene.render.resolution_y=720 if fast else 1080;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.compression=0;scene.render.image_settings.color_mode='RGB'
w=bpy.data.worlds.new('Temporary v34 tour daylight');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.82,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;scene.world=w
l=bpy.data.lights.new('Temporary v34 tour sun','SUN');l.energy=2.5;o=bpy.data.objects.new(l.name,l);scene.collection.objects.link(o);o.rotation_euler=(.45,-.55,-.45)
for x,y,z in ((4,4,3.8),(4,12,3.8),(5,23,3.8),(4,7,8),(4,18,8),(4,27,8)):
 l=bpy.data.lights.new('Temporary tour room fill','AREA');l.energy=180;l.size=4;o=bpy.data.objects.new(l.name,l);scene.collection.objects.link(o);o.location=(x,y,z)
c=bpy.data.cameras.new('Temporary v34 tour camera');c.lens=24;c.clip_start=.04;c.clip_end=1000
camera=bpy.data.objects.new(c.name,c);scene.collection.objects.link(camera);scene.camera=camera
plan=json.loads((dest/'tour-plan.json').read_text());fps=30
def pose(section,t):
 ps=section['samples'];idx=min(len(ps)-2,max(0,t*(len(ps)-1)));i=int(idx);f=idx-i
 eye=Vector(ps[i]['eye']).lerp(Vector(ps[i+1]['eye']),f)
 target=Vector(ps[i]['target']).lerp(Vector(ps[i+1]['target']),f)
 camera.location=eye;camera.rotation_euler=(target-eye).to_track_quat('-Z','Y').to_euler()
def render_frame(path):
 scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
if os.environ.get('V34_ANIMATION_BENCHMARK'):
 scene.frame_start=1;scene.frame_end=4;camera.rotation_mode='QUATERNION'
 for i,t in enumerate((.15,.16,.17,.18),1):
  pose(plan['sections'][1],t);camera.rotation_quaternion=camera.rotation_euler.to_quaternion();camera.keyframe_insert('location',frame=i);camera.keyframe_insert('rotation_quaternion',frame=i)
 scene.render.filepath=str(build/'v34-animation-benchmark-');start=time.monotonic();bpy.ops.render.render(animation=True)
 print('V34_ANIMATION_BENCHMARK_COMPLETE',time.monotonic()-start,flush=True);raise SystemExit(0)
if os.environ.get('V34_BENCHMARK'):
 times=[]
 for i,(sec,t) in enumerate([(plan['sections'][1],.15),(plan['sections'][1],.16),(plan['sections'][3],.5),(plan['sections'][3],.51)]):
  pose(sec,t);start=time.monotonic();render_frame(dest/('benchmark-'+engine+'-'+str(i)+'.png'));times.append(time.monotonic()-start)
 (dest/('benchmark-'+engine+'.json')).write_text(json.dumps(dict(seconds=times,engine=engine)))
 print('V34_BENCHMARK_COMPLETE',engine,times,flush=True);raise SystemExit(0)
selected=os.environ.get('V34_SECTION');manifest=[]
for sn,section in enumerate(plan['sections']):
 if selected is not None and sn!=int(selected):continue
 output=dest/('tour-section-%02d.webm'%sn);scratch=build/('v34-tour-frame-%02d.png'%sn)
 assert not output.exists() or os.environ.get('V34_VIDEO_REBUILD')=='1',str(output)
 log=open(build/('v34-tour-encode-%02d.log'%sn),'w')
 title=section['name']
 vf="drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+title+"':fontsize=30:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=12:x=30:y=30:enable='lt(t,3)'"
 proc=subprocess.Popen(['C:/ffmpeg/ffmpeg.exe','-hide_banner','-loglevel','error','-y','-f','image2pipe','-vcodec','png','-framerate',str(fps),'-i','pipe:0','-vf',vf,'-c:v','libvpx-vp9','-b:v','10M','-crf','18','-row-mt','1','-deadline','good','-cpu-used','4','-pix_fmt','yuv420p','-an',str(output)],stdin=subprocess.PIPE,stderr=log,creationflags=0x08000000)
 total=section['duration']*fps;start=time.monotonic()
 try:
  for k in range(total):
   pose(section,k/(total-1));render_frame(scratch);assert proc.poll() is None,'Encoder stopped';proc.stdin.write(scratch.read_bytes())
   if k%30==0:
    print('V34_TOUR_PROGRESS',sn,k,total,'elapsed',round(time.monotonic()-start,1),flush=True)
    if k%150==0:bpy.data.images['Render Result'].save_render(str(dest/('tour-contact-%02d-%04d.jpg'%(sn,k))),scene=scene)
 finally:proc.stdin.close();code=proc.wait();log.close()
 assert code==0
 meta=dict(section=sn,name=title,duration=section['duration'],frames=total,fps=fps,resolution=[scene.render.resolution_x,scene.render.resolution_y],engine=engine,samples=16 if engine=='CYCLES' else 8 if viewport else scene.eevee.taa_render_samples,bytes=output.stat().st_size,source=bpy.data.filepath,source_saved=False)
 (dest/('tour-section-%02d.json'%sn)).write_text(json.dumps(meta,indent=2));manifest.append(meta)
 print('V34_TOUR_SECTION_COMPLETE',sn,total,flush=True)
