"""Fixed before/after street views and overview for visual checking."""
from pathlib import Path
import bpy,json
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v54'
scene=bpy.context.scene;review=scene.copy();review.name='TEMP v54 street review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.render_aa='8';review.display.shading.color_type='MATERIAL';review.display.shading.light='STUDIO';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
cu=bpy.data.cameras.new('TEMP v54 camera');cam=bpy.data.objects.new(cu.name,cu);review.collection.objects.link(cam);review.camera=cam;cu.clip_end=2500;cu.lens=32
d=json.loads((dest/'prepared-street.json').read_text());schedule=d['frontages'];house=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world.copy()
def viewframe(chain):
 item=min(schedule,key=lambda i:abs(i['chain_m']-chain) if i['chain_m']>166 else 1e6);f=item['frame'];p=f['origin'];x=f['x'];n=f['y'];return Matrix(((x[0],n[0],0,p[0]),(x[1],n[1],0,p[1]),(0,0,1,0),(0,0,0,1)))
views=[('holmdale',house,(-25,-36,28),(12,0,0),None),('junction_shops',viewframe(196),(-21,-18,7),(2,0,2.5),None),('retail_terrace',viewframe(378),(-24,-18,9),(0,0,2.5),None),('hall_cafe',viewframe(500),(-24,-20,8),(1,0,2.5),None),('supermarket',viewframe(594),(-38,-38,20),(0,4,2),None),('barkby',Matrix.Identity(4),(-95,-25,45),(-98,37,0),None)]
archive=bpy.data.collections['ARCHIVE v54 | Replaced terrain perimeter and provisional masses'];images=[]
try:
 for label,basis,eye,target,ortho in views:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cu.type='ORTHO' if ortho else 'PERSP';cu.ortho_scale=ortho or 1
  for stage in ('before','after'):
   if stage=='before':review.collection.children.link(archive)
   elif archive.name in review.collection.children:review.collection.children.unlink(archive)
   review.view_layers[0].layer_collection.children['STREET v54 | Authored route photo-led frontages'].exclude=stage=='before'
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True);images.append({'label':label,'stage':stage,'file':review.render.filepath,'eye_world':list(cam.location)})
finally:
 bpy.context.window.scene=scene;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(cu)
(dest/'review-views.json').write_text(json.dumps({'style':'Workbench previews, not photographs; local fit and estimated proportions','images':images},indent=2));result={'images':len(images)}
