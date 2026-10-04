"""Continuous textured exterior fly-through; source scene never saved."""
from pathlib import Path
import bpy,json,os
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v32';frames=ROOT/'build/v32-flythrough-frames';frames.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True;scene.cycles.denoiser='OPTIX';scene.render.use_persistent_data=True
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU'
# Genuine unique 24fps frames, denoised GPU Cycles with cached static geometry.
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
w=bpy.data.worlds.new('Temporary flythrough daylight');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.82,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;scene.world=w
ld=bpy.data.lights.new('Temporary flythrough sun','SUN');ld.energy=2.5;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
cd=bpy.data.cameras.new('Temporary continuous flythrough');cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);scene.camera=cam;cd.lens=22
# Eye path stays outside the buildings; turns/rear-alley descend are continuous.
nodes=[(0,(-16,-6.7,3.2),(1,-6.7,2)),(6,(32,-6.7,3.2),(48,-6.7,2)),(9,(51,-6.7,5),(46,-13,3)),(12,(28,-9,11),(12,-4,2)),(15,(-19,-8,15),(1,8,2)),(18,(-19,30,12),(-9,25,1)),(20,(-11.4,29,2.2),(-11.4,16,2)),(26,(-11.4,2,2.2),(-11.4,-6,2)),(28,(-11.4,-5,3.2),(5,-3,2))]
fps=24;total=28*fps;start=int(os.environ.get('FLY_START','0'));end=min(total,int(os.environ.get('FLY_END',str(total))))
for frame in range(start,end):
 t=frame/fps;i=next(i for i in range(len(nodes)-1) if nodes[i][0]<=t<nodes[i+1][0]);a,b=nodes[i],nodes[i+1];u=(t-a[0])/(b[0]-a[0]);u=u*u*(3-2*u)
 eye=Vector(a[1]).lerp(Vector(b[1]),u);target=Vector(a[2]).lerp(Vector(b[2]),u);cam.location=eye;cam.rotation_euler=(target-eye).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(frames/f'{frame:05d}.png')
 if os.environ.get('FLY_OVERWRITE') or not Path(scene.render.filepath).exists():bpy.ops.render.render(write_still=True)
 if frame%24==0:print('FLY_PROGRESS',frame,total,flush=True)
(dest/'flythrough.json').write_text(json.dumps(dict(fps=fps,frames=total,duration_seconds=28,resolution=[1280,720],style='Continuous textured exterior camera flight; not proof of player traversal',path=nodes,render='GPU OptiX Cycles8 denoised'),indent=2));print('FLY_RENDER_COMPLETE',start,end,flush=True)
