"""Matched porch and window views before and after photo-led correction."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v49'
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-porch-v49.blend'
scene=bpy.context.scene;review=scene.copy();review.name='TEMP v49 review';bpy.context.window.scene=review
archive=bpy.data.collections['ARCHIVE v49 | Flat porch and incorrect right bay']
review.collection.children.link(archive)
review.render.engine='BLENDER_WORKBENCH';review.display.shading.color_type='MATERIAL';review.display.shading.light='STUDIO';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
cu=bpy.data.cameras.new('TEMP v49 camera');cam=bpy.data.objects.new(cu.name,cu);review.collection.objects.link(cam);review.camera=cam;cu.clip_end=2000;basis=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world.copy();images=[];start=time.monotonic()
views=globals().get('VIEWS',[('porch',(4,-6,2.8),(4,-.2,1.4)),('porch_left',(.3,-5.5,3.0),(3.9,-.2,1.4)),('window',(2,-10,4.8),(7,-1.5,1.6))])
try:
 for label,eye,target in views:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cu.type='PERSP';cu.lens=38
  for stage in ('before','after'):
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='DETAIL v49 | User-photo porch window and paving':child.exclude=stage=='before'
    if child.name==archive.name:child.exclude=stage=='after'
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True);images.append(f'{label}_{stage}.png')
finally:
 bpy.context.window.scene=scene;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(cu)
(dest/'review.json').write_text(json.dumps({'images':images,'seconds':time.monotonic()-start,'style':'Matched Workbench model previews, not photo camera calibration'},indent=2)+'\n');result={'images':images,'seconds':time.monotonic()-start}
