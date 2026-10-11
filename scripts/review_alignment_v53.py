"""Matched fixed cameras for the geographic correction, plus house closeup."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v53'
scene=bpy.context.scene;review=scene.copy();review.name='TEMP v53 review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.render_aa='8';review.display.shading.color_type='MATERIAL';review.display.shading.light='STUDIO';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True
review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
cu=bpy.data.cameras.new('TEMP v53 camera');cam=bpy.data.objects.new(cu.name,cu);review.collection.objects.link(cam);review.camera=cam;cu.clip_end=2500
root=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'];after=root.location.copy();before=Vector(json.loads((dest/'alignment-validation.json').read_text())['house_origin_before']);basis=root.matrix_world.copy()
views=[('holmdale_overhead',Vector((-83,826,190)),Vector((-83,826,0)),245),('holmdale_end',basis@Vector((25,-28,24)),basis@Vector((7,-2,0)),None),('house_front',basis@Vector((6,-18,7)),basis@Vector((6,0,1.5)),None),('town_junction',Vector((-60,80,120)),Vector((-60,45,0)),180)]
archive=bpy.data.collections['ARCHIVE v53 | Estimated Holmdale surfaces and terminal'];images=[]
try:
 for label,eye,target,ortho in views:
  cam.location=eye;cam.rotation_euler=(target-eye).to_track_quat('-Z','Y').to_euler();cu.type='ORTHO' if ortho else 'PERSP';cu.ortho_scale=ortho or 1;cu.lens=36
  for stage in (('before','after') if label=='holmdale_overhead' else ('after',)):
   root.location=before if stage=='before' else after
   if stage=='before':review.collection.children.link(archive)
   elif archive.name in review.collection.children:review.collection.children.unlink(archive)
   review.view_layers[0].layer_collection.children['MAPPING v53 | Surveyed Holmdale end alignment'].exclude=stage=='before'
   bpy.context.view_layer.update();review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True);images.append(review.render.filepath)
finally:
 root.location=after;bpy.context.window.scene=scene;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(cu);bpy.context.view_layer.update()
result={'images':images}
