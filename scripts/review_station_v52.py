"""Matched frontage views for the first resumed route-reference pass."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v52'
assert Path(bpy.data.filepath).name=='pharmacie-station-frontage-v52.blend'
scene=bpy.context.scene;review=scene.copy();review.name='TEMP v52 frontage';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.shading.color_type='MATERIAL';review.display.shading.light='STUDIO';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
cu=bpy.data.cameras.new('TEMP v52 camera');cam=bpy.data.objects.new(cu.name,cu);review.collection.objects.link(cam);review.camera=cam;cu.clip_end=2000;cu.lens=32
basis=bpy.data.objects['Station v52 | Estimated DR boundary assembly'].matrix_world.copy();images=[];start=time.monotonic()
try:
 for name,eye,target in [('frontage',(17,36,5),(17,0,1.2)),('context',(40,40,22),(17,0,1.2))]:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
  for stage in ('before','after'):
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='DETAIL v52 | Station approach blue appliance frontage':child.exclude=stage=='before'
   review.render.filepath=str(dest/f'{name}_{stage}.png');bpy.ops.render.render(write_still=True);images.append(f'{name}_{stage}.png')
finally:
 bpy.context.window.scene=scene;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(cu)
(dest/'review.json').write_text(json.dumps({'images':images,'seconds':time.monotonic()-start,'style':'Material viewport previews; estimated dimensions, not surveyed alignment'},indent=2)+'\n');result={'images':images}
