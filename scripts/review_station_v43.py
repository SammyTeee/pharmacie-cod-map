"""Matched quick station detail review, including overhead footprint."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v43'
assert Path(bpy.data.filepath).name=='pharmacie-station-detail-v43.blend'
original=bpy.context.scene;review=original.copy();review.name='TEMP v43 review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.render_aa='8';review.display.shading.light='STUDIO';review.display.shading.color_type='MATERIAL';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.display.shading.background_type='VIEWPORT';review.display.shading.background_color=(.12,.15,.19)
review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
data=bpy.data.cameras.new('TEMP v43 camera');cam=bpy.data.objects.new(data.name,data);review.collection.objects.link(cam);review.camera=cam;data.clip_end=2000
basis=bpy.data.objects['Station v43 | Movable reference assembly'].matrix_world.copy()
views=[('01_platform',[2,1.25,1.8],[30,1.25,1.35],None),('02_overhead',[30,0,90],[30,0,0],95)]
manifest=[];start=time.monotonic()
try:
 for label,eye,target,ortho in views:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO' if ortho else 'PERSP';data.ortho_scale=ortho or 1;data.lens=32
  for stage in ('before','after'):
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='DETAIL v43 | Provisional station platform':child.exclude=(stage=='before')
   archive=bpy.data.collections['ARCHIVE v43 | Misclassified shelter mass']
   if stage=='before':review.collection.children.link(archive)
   elif archive.name in review.collection.children:review.collection.children.unlink(archive)
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True)
   manifest.append({'view':label,'stage':stage,'eye_local':eye,'target_local':target,'orthographic_scale':ortho,'image':f'{label}_{stage}.png'})
finally:
 bpy.context.window.scene=original;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(data)
(dest/'review-views.json').write_text(json.dumps({'style':'Workbench material previews; overhead is model only, not Google comparison','seconds':time.monotonic()-start,'views':manifest},indent=2)+'\n')
result={'images':len(manifest),'seconds':time.monotonic()-start}
