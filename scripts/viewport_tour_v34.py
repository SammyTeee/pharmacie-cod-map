"""Run in the connected Blender GUI: cached GPU viewport capture, no file save."""
from pathlib import Path
import bpy,gpu,json,time,subprocess,math
import numpy as np
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v34';build=ROOT/'build'
source_scene=bpy.data.scenes['03 Both floors - assembled exterior']
capture_window=bpy.context.window_manager.windows[0];capture_window.scene=source_scene;capture_window.view_layer=source_scene.view_layers[0];bpy.context.view_layer.update()
scene=bpy.data.scenes.get('Temporary v34 optimized capture')
assert scene is None or scene.get('codex_capture_only'), 'Preserve an existing user scene'
if scene is None:
 scene=bpy.data.scenes.new('Temporary v34 optimized capture');scene['codex_capture_only']=True;deps=bpy.context.evaluated_depsgraph_get()
 vertices=[];faces=[];uvs=[];face_materials=[];smooth=[];materials=[];mat_indices={}
 for ob in source_scene.objects:
  if ob.type not in ('MESH','FONT','CURVE') or ob.hide_render:continue
  ev=ob.evaluated_get(deps);me=ev.to_mesh()
  if not me or not me.polygons:
   ev.to_mesh_clear();continue
  offset=len(vertices);vertices.extend(tuple(ev.matrix_world@v.co) for v in me.vertices)
  local_mats=[]
  for mat in me.materials:
   if mat is None:local_mats.append(0);continue
   if mat.name not in mat_indices:mat_indices[mat.name]=len(materials);materials.append(mat)
   local_mats.append(mat_indices[mat.name])
  layer=me.uv_layers.active
  for p in me.polygons:
   faces.append(tuple(offset+i for i in p.vertices));face_materials.append(local_mats[p.material_index] if local_mats else 0);smooth.append(p.use_smooth)
   uvs.extend(tuple(layer.data[i].uv) if layer else (0.,0.) for i in p.loop_indices)
  ev.to_mesh_clear()
 me=bpy.data.meshes.new('Temporary v34 merged capture mesh');me.from_pydata(vertices,[],faces);me.update()
 for mat in materials:me.materials.append(mat)
 me.polygons.foreach_set('material_index',face_materials);me.polygons.foreach_set('use_smooth',smooth)
 layer=me.uv_layers.new(name='UVMap');layer.data.foreach_set('uv',np.asarray(uvs,dtype=np.float32).ravel())
 ob=bpy.data.objects.new(me.name,me);scene.collection.objects.link(ob);scene.world=source_scene.world
window=bpy.context.window_manager.windows[0];area=next(a for a in window.screen.areas if a.type=='VIEW_3D');region=next(r for r in area.regions if r.type=='WINDOW');space=area.spaces.active
window.scene=scene;window.view_layer=scene.view_layers[0]
bpy.context.view_layer.update()
scene.view_layers[0].objects.active=next(iter(scene.objects))
plan=json.loads((dest/'tour-plan.json').read_text());W,H=1280,720;FPS=30
space.shading.type='SOLID';space.shading.light='STUDIO';space.shading.color_type='TEXTURE';space.shading.show_shadows=True;space.shading.show_cavity=True;space.shading.cavity_type='WORLD';space.overlay.show_overlays=False
offscreen=gpu.types.GPUOffScreen(W,H)
def view_pose(section,t):
 ps=section['samples'];idx=min(len(ps)-2,max(0,t*(len(ps)-1)));i=int(idx);f=idx-i
 eye=Vector(ps[i]['eye']).lerp(Vector(ps[i+1]['eye']),f);target=Vector(ps[i]['target']).lerp(Vector(ps[i+1]['target']),f)
 matrix=Matrix.Translation(eye)@(target-eye).to_track_quat('-Z','Y').to_matrix().to_4x4()
 return matrix.inverted()
# Perspective matrix for a 24mm lens on a 36mm sensor at 16:9.
near,far=.04,1000.;sx=2*24/36;sy=sx*W/H
projection=Matrix(((sx,0,0,0),(0,sy,0,0),(0,0,-(far+near)/(far-near),-2*far*near/(far-near)),(0,0,-1,0)))
def capture(section,t):
 with bpy.context.temp_override(window=window,area=area,region=region):
  offscreen.draw_view3d(scene,scene.view_layers[0],space,region,view_pose(section,t),projection,do_color_management=True)
 with offscreen.bind():
  buffer=gpu.state.active_framebuffer_get().read_color(0,0,W,H,4,0,'UBYTE')
  return np.array(buffer,dtype=np.uint8).tobytes()
if globals().get('BENCHMARK_ONLY'):
 times=[]
 for t in (.15,.16,.17,.18):
  started=time.monotonic();raw=capture(plan['sections'][1],t);times.append(time.monotonic()-started)
 (build/'v34-viewport-test.rgba').write_bytes(raw);offscreen.free();window.scene=source_scene
 result={'seconds':times,'resolution':[W,H],'estimated_capture_minutes':sum(times[1:])/3*plan['duration']*FPS/60}
else:
 def restore_source():
  window.scene=source_scene
  ob=next(iter(scene.objects),None);me=ob.data if ob else None
  bpy.data.scenes.remove(scene)
  if ob:bpy.data.objects.remove(ob,do_unlink=True)
  if me and me.users==0:bpy.data.meshes.remove(me)
 logfile=open(build/'v34-viewport-encode.log','w')
 vf=['vflip'];elapsed=0
 for sec in plan['sections']:
  vf.append("drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+sec['name']+"':fontsize=25:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=10:x=24:y=24:enable='between(t,"+str(elapsed)+','+str(elapsed+2)+")'");elapsed+=sec['duration']
 output=dest/'preview.webm'
 encoder=subprocess.Popen(['C:/ffmpeg/ffmpeg.exe','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',str(W)+'x'+str(H),'-framerate',str(FPS),'-i','pipe:0','-vf',','.join(vf),'-c:v','libvpx-vp9','-b:v','6M','-crf','18','-row-mt','1','-deadline','realtime','-cpu-used','6','-pix_fmt','yuv420p','-an',str(output)],stdin=subprocess.PIPE,stderr=logfile,creationflags=0x08000000)
 state={'section':0,'frame':0,'total':0,'started':time.monotonic(),'status':'capturing'}
 status_path=dest/'viewport-status.json'
 def step():
  try:
   sn=state['section'];sec=plan['sections'][sn];k=state['frame'];count=sec['duration']*FPS
   raw=capture(sec,k/(count-1));assert encoder.poll() is None,'Encoder stopped';encoder.stdin.write(raw)
   state['frame']+=1;state['total']+=1
   if k%30==0:
    status_path.write_text(json.dumps(dict(state,elapsed_seconds=round(time.monotonic()-state['started'],1),total_frames=plan['duration']*FPS)))
   if state['frame']==count:state['section']+=1;state['frame']=0
   if state['section']==len(plan['sections']):
    encoder.stdin.close();code=encoder.wait();logfile.close();offscreen.free();assert code==0,code
    facts=dict(state,status='complete',duration=plan['duration'],frames=state['total'],fps=FPS,resolution=[W,H],render='Cached GPU textured Workbench viewport; studio shading, shadows/cavity; no ray-traced lighting',elapsed_seconds=round(time.monotonic()-state['started'],1),bytes=output.stat().st_size,source=bpy.data.filepath,source_saved=False)
    status_path.write_text(json.dumps(facts,indent=2));(dest/'viewport-tour.json').write_text(json.dumps(facts,indent=2));restore_source();return None
   return .001
  except Exception as exc:
   state['status']='failed';state['error']=repr(exc);status_path.write_text(json.dumps(state,indent=2))
   try:encoder.stdin.close();encoder.wait();logfile.close();offscreen.free()
   except Exception:pass
   restore_source();return None
 bpy.app.timers.register(step,first_interval=.1)
 result={'started':True,'status_file':str(status_path),'frames':plan['duration']*FPS}
