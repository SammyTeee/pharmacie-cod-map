"""Fast matched number 29 views, including a model overhead."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v44'
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-house-v44.blend'
original=bpy.context.scene;review=original.copy();review.name='TEMP v44 review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.render_aa='8';review.display.shading.light='STUDIO';review.display.shading.color_type='MATERIAL';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.display.shading.background_type='VIEWPORT';review.display.shading.background_color=(.12,.15,.19)
review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
data=bpy.data.cameras.new('TEMP v44 camera');cam=bpy.data.objects.new(data.name,data);review.collection.objects.link(cam);review.camera=cam;data.clip_end=2000
basis=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world.copy()
views=[('01_front',[7.0,-20,3.3],[7,1,2.0],None),('02_oblique',[17,-15,4.2],[6,1,1.8],None),('03_porch',[1,-6,2.3],[3,0,1.5],None),('04_overhead',[7,1,45],[7,1,0],34)]
stages=globals().get('STAGES',('before','after'))
manifest=[] if len(stages)==2 else [v for v in json.loads((dest/'review-views.json').read_text())['views'] if v['stage'] not in stages]
start=time.monotonic()
try:
 for label,eye,target,ortho in views:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO' if ortho else 'PERSP';data.ortho_scale=ortho or 1;data.lens=35
  for stage in stages:
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='DETAIL v44 | Number 29 photo-led bungalow':child.exclude=(stage=='before')
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True)
   manifest.append({'view':label,'stage':stage,'eye_local':eye,'target_local':target,'orthographic_scale':ortho,'image':f'{label}_{stage}.png'})
finally:
 bpy.context.window.scene=original;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(data)
(dest/'review-views.json').write_text(json.dumps({'style':'Workbench material previews; overhead is model only, not Google verification','seconds':time.monotonic()-start,'views':manifest},indent=2)+'\n')
result={'images':len(manifest),'seconds':time.monotonic()-start}
