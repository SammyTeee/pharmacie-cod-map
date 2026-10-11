"""Matched v47/v48 comparison without changing saved source geometry."""
from pathlib import Path
import bpy,json,math
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v48'
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-garage-v48.blend'
report=json.loads((dest/'validation.json').read_text());house=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'];coll=bpy.data.collections['DETAIL v44 | Number 29 photo-led bungalow']
p=Vector(report['garage_pivot']);turn=Matrix.Translation(p)@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation(-p)
garage=[];boundary=[]
for ob in coll.objects:
 if ob.type!='MESH':continue
 if any(s in ob.name for s in ('boundary','fence')):boundary.append(ob);continue
 if 'garage' in ob.name:garage.append(ob);continue
 # Selected ancillary names now lie near garage; detect using pre-turn bounds.
 old=turn.inverted()@ob.matrix_basis
 if any(s in ob.name for s in ('fascia','gutter','downpipe','lantern')) and abs(ob.matrix_basis[0][1])>.99:garage.append(ob)
saved=[(o,o.matrix_basis.copy()) for o in garage+boundary]
scene=bpy.context.scene;review=scene.copy();review.name='TEMP v48 review';bpy.context.window.scene=review
review.render.engine='BLENDER_WORKBENCH';review.display.shading.color_type='MATERIAL';review.display.shading.light='STUDIO';review.display.shading.show_shadows=True;review.display.shading.show_cavity=True;review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.render.image_settings.file_format='PNG'
cu=bpy.data.cameras.new('TEMP v48 camera');cam=bpy.data.objects.new(cu.name,cu);review.collection.objects.link(cam);review.camera=cam;cu.clip_end=2000;basis=house.matrix_world.copy();images=[]
try:
 for label,eye,target,ortho in [('garage',(-9,-22,8),(7,-2,1.7),None),('house_overhead',(7,-1,45),(7,-1,0),35),('street',(-44,845,135),(-44,845,0),115)]:
  cam.location=Vector(eye) if label=='street' else basis@Vector(eye);aim=Vector(target) if label=='street' else basis@Vector(target);cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler();cu.type='ORTHO' if ortho else 'PERSP';cu.ortho_scale=ortho or 1;cu.lens=38
  for stage in ('before','after'):
   for ob,m in saved:ob.matrix_basis=m
   if stage=='before':
    for ob in garage:ob.matrix_basis=turn.inverted()@ob.matrix_basis
    for ob in boundary:ob.location.x-=2.25
   for child in review.view_layers[0].layer_collection.children:
    if child.name=='CONTEXT v48 | Placeholder opposite Holmdale houses':child.exclude=stage=='before'
   bpy.context.view_layer.update();review.render.filepath=str(dest/f'{label}_{stage}.png');bpy.ops.render.render(write_still=True);images.append(f'{label}_{stage}.png')
finally:
 for ob,m in saved:ob.matrix_basis=m
 bpy.context.window.scene=scene;bpy.data.scenes.remove(review);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.cameras.remove(cu);bpy.context.view_layer.update()
(dest/'review.json').write_text(json.dumps({'images':images,'style':'Matched Workbench v47/v48 reconstruction previews, not source photos'},indent=2)+'\n');result={'images':images,'garage_parts':len(garage)}
