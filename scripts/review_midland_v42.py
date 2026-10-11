"""Fast matched material previews of source-led pub exterior."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v42'
assert Path(bpy.data.filepath).name=='pharmacie-midland-frontage-v42.blend'
original=bpy.context.scene;review=original.copy();review.name='TEMP v42 review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.render_aa='8';review.display.shading.light='STUDIO';review.display.shading.color_type='MATERIAL';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.display.shading.background_type='VIEWPORT';review.display.shading.background_color=(.12,.15,.19)
review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
data=bpy.data.cameras.new('TEMP v42 review camera');cam=bpy.data.objects.new(data.name,data);review.collection.objects.link(cam);review.camera=cam;data.clip_end=2000
basis=bpy.data.objects['Midland v42 | Movable reference assembly'].matrix_world.copy()
views=[('01_front',[8.35,-22,3.5],[8.35,1,3.8],None),('02_oblique',[-8,-17,5.5],[7,2,3.5],None),('03_roof',[-16,-21,22],[5,5,2.5],50)]
manifest=[];start=time.monotonic()
try:
 for label,eye,target,ortho in views:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO' if ortho else 'PERSP';data.ortho_scale=ortho or 1;data.lens=30
  for stage in ('before','after'):
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='DETAIL v42 | Midland photo-led exterior':child.exclude=(stage=='before')
   closure=bpy.data.collections['ARCHIVE v42 | Provisional Midland footprint mass']
   if stage=='before':review.collection.children.link(closure)
   elif closure.name in review.collection.children:review.collection.children.unlink(closure)
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True)
   manifest.append({'view':label,'stage':stage,'eye_local':eye,'target_local':target,'orthographic_scale':ortho,'image':f'{label}_{stage}.png'})
finally:
 bpy.context.window.scene=original;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(data)
(dest/'review-views.json').write_text(json.dumps({'style':'Workbench material-colour previews, not final textured lighting','seconds':time.monotonic()-start,'views':manifest},indent=2)+'\n');result={'images':len(manifest),'seconds':time.monotonic()-start}
