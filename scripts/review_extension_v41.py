"""Minutes-scale matched Workbench reviews; restore source render settings."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v41'
original=bpy.context.scene
assert Path(bpy.data.filepath).name=='pharmacie-extension-route-v41.blend'
review=original.copy();review.name='TEMP v41 review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.render_aa='8';review.display.shading.light='STUDIO';review.display.shading.color_type='MATERIAL';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.display.shading.background_type='VIEWPORT';review.display.shading.background_color=(.12,.15,.19)
review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
data=bpy.data.cameras.new('TEMP v41 review camera');cam=bpy.data.objects.new(data.name,data);review.collection.objects.link(cam);review.camera=cam;data.clip_end=3000
views=[('01_route_overview',[-20,480,1000],[-20,480,0],1120),('02_station_holmdale',[150,750,170],[0,868,0],240),('03_taraj_seam',[-50,296,1.65],[-51,345,1.65],None),('04_holmdale',[-2,840,1.65],[-80,845,1.65],None)]
manifest=[];start=time.monotonic()
try:
 for label,eye,target,ortho in views:
  cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO' if ortho else 'PERSP';data.ortho_scale=ortho or 1;data.lens=25
  if label=='01_route_overview':cam.rotation_euler.z+=1.5707963267948966
  for stage in ('before','after'):
   for child in review.view_layers[0].layer_collection.children:
    if child.name.startswith(('MAPPING v41','REFERENCE v41')):child.exclude=(stage=='before')
   closure=bpy.data.collections['ARCHIVE v41 | Retained v34 beyond-Taraj closure']
   if stage=='before':review.collection.children.link(closure)
   elif closure.name in review.collection.children:review.collection.children.unlink(closure)
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True)
   manifest.append({'view':label,'stage':stage,'eye':eye,'target':target,'orthographic_scale':ortho,'image':f'{label}_{stage}.png'})
finally:
 bpy.context.window.scene=original;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(data)
(dest/'review-views.json').write_text(json.dumps({'style':'Workbench material-colour previews, not final textured lighting','seconds':time.monotonic()-start,'views':manifest},indent=2)+'\n')
result={'images':len(manifest),'seconds':time.monotonic()-start}
