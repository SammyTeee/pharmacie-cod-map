"""Matched station corridor and Holmdale end previews."""
from pathlib import Path
import bpy,json,time
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v45'
assert Path(bpy.data.filepath).name=='pharmacie-station-holmdale-v45.blend'
original=bpy.context.scene;review=original.copy();review.name='TEMP v45 review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.render_aa='8';review.display.shading.light='STUDIO';review.display.shading.color_type='MATERIAL';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.display.shading.background_type='VIEWPORT';review.display.shading.background_color=(.12,.15,.19)
review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
data=bpy.data.cameras.new('TEMP v45 camera');cam=bpy.data.objects.new(data.name,data);review.collection.objects.link(cam);review.camera=cam;data.clip_end=2000
f=json.loads((dest/'prepared-surfaces.json').read_text())['station_frame'];a=f['origin'];u=f['u'];n=f['n'];station=Matrix(((u[0],n[0],0,a[0]),(u[1],n[1],0,a[1]),(0,0,1,0),(0,0,0,1)));house=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world.copy()
views=[('01_station_corridor',station,[68,-25,21],[22,6,0],None),('02_station_overhead',station,[12,8,120],[12,8,0],160),('03_station_access',station,[23,23,2.2],[38,3.5,1.0],None),('04_holmdale_end',house,[21,-18,13],[6,-3,1],None)]
manifest=[];start=time.monotonic()
try:
 for label,basis,eye,target,ortho in views:
  cam.location=basis@Vector(eye);cam.rotation_euler=(basis@Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO' if ortho else 'PERSP';data.ortho_scale=ortho or 1;data.lens=34
  for stage in ('before','after'):
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='MAPPING v45 | Station corridor and Holmdale turning end':child.exclude=(stage=='before')
   archive=bpy.data.collections['ARCHIVE v45 | Superseded joined extension surfaces']
   if stage=='before':review.collection.children.link(archive)
   elif archive.name in review.collection.children:review.collection.children.unlink(archive)
   review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True)
   manifest.append({'view':label,'stage':stage,'eye_local':eye,'target_local':target,'orthographic_scale':ortho,'image':f'{label}_{stage}.png'})
finally:
 bpy.context.window.scene=original;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(data)
(dest/'review-views.json').write_text(json.dumps({'style':'Workbench material previews; overhead model only, Google alignment pending','seconds':time.monotonic()-start,'views':manifest},indent=2)+'\n');result={'images':len(manifest),'seconds':time.monotonic()-start}
