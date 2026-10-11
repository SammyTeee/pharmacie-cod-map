"""Show central diagonal door and its landing in matched porch-only views."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v50'
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-corner-porch-v50.blend'
scene=bpy.context.scene;review=scene.copy();review.name='TEMP v50 porch review';bpy.context.window.scene=review
archive=bpy.data.collections['ARCHIVE v50 | Straight-facing porch revision'];review.collection.children.link(archive)
review.render.engine='BLENDER_WORKBENCH';review.display.shading.color_type='MATERIAL';review.display.shading.light='STUDIO';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.render.resolution_x=1280;review.render.resolution_y=900;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
cu=bpy.data.cameras.new('TEMP v50 camera');cam=bpy.data.objects.new(cu.name,cu);review.collection.objects.link(cam);review.camera=cam;cu.clip_end=2000;basis=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world.copy();images=[];start=time.monotonic()
views=[('porch_front',(-.45,-4.95,2.85),(3.475,-1.025,1.20),None),('porch_context',(-2,-6.5,3.7),(3.8,-.7,1.20),None),('porch_plan',(3.5,-.7,12),(3.5,-.7,0),5.0)]
try:
 for label,eye,target,ortho in views:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cu.type='ORTHO' if ortho else 'PERSP';cu.ortho_scale=ortho or 1;cu.lens=42
  for stage in ('before','after'):
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='DETAIL v50 | Diagonal central door and porch':child.exclude=stage=='before'
    if child.name==archive.name:child.exclude=stage=='after'
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True);images.append(f'{label}_{stage}.png')
finally:
 bpy.context.window.scene=scene;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(cu)
(dest/'review.json').write_text(json.dumps({'images':images,'seconds':time.monotonic()-start,'style':'Matched Workbench porch revision views, not photo calibration'},indent=2)+'\n');result={'images':images,'seconds':time.monotonic()-start}
