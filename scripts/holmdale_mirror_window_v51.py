"""Sam's requested exact right-to-left porch window mirror; retain v50."""
from pathlib import Path
import bpy,bmesh,json,re
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-corner-porch-v50.blend'
out=ROOT/'assets/blender/pharmacie-holmdale-mirrored-window-v51.blend'
assert not out.exists()
dest=ROOT/'recon/v51';dest.mkdir(exist_ok=True)
source=bpy.data.collections['DETAIL v50 | Diagonal central door and porch']
coll=bpy.data.collections.new('DETAIL v51 | Mirrored left porch window');bpy.context.scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v51 | Smaller left porch window');archive.use_fake_user=True
mirror=Matrix(((0,1,0,4.5),(1,0,0,-4.5),(0,0,1,0),(0,0,0,1)))
made=[];retired=[]
def copy(ob,transform=None):
 d=ob.copy();d.data=ob.data.copy();d.name=ob.name.replace('v50','v51');coll.objects.link(d)
 if transform is not None:
  m=transform@ob.matrix_basis
  for v in d.data.vertices:v.co=m@v.co
  d.matrix_basis=Matrix.Identity(4)
 made.append(d);return d
for ob in list(source.objects):
 n=ob.name
 left=any(s in n for s in ('panel 0','pane 0','frame 0','rail 0','corner fascia 0','corner gutter 0'))
 backing=any(s in n for s in ('closed corner porch backing','corner porch low roof cap'))
 if left or backing:
  archive.objects.link(ob);source.objects.unlink(ob);retired.append(n)
  if backing:
   d=copy(ob)
   # Extend rear edge to accommodate the full mirrored 1.07-unit return.
   for v in d.data.vertices:
    if v.co.y>0:v.co.y+=.39
 right=any(s in n for s in ('panel 2','pane 2','frame 2','rail 2','right return transom','right return open vent','corner fascia 2','corner gutter 2'))
 if right:
  d=copy(ob,mirror);d.name=d.name.replace(' 2',' 0').replace('right return','mirrored left return')
bad=[]
for ob in made:
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
# Fit the wider return in front of the existing wall rather than burying its
# rear 0.42 units inside the house. Move the porch and its own landing together;
# keep the separate plant ledge, baskets and pots in place.
for ob in list(source.objects):
 if any(s in ob.name for s in ('porch','central black','black lever','black door','brass peephole','ornament ribbon','wire flower','corner fascia','corner gutter','gutter corner','central door threshold')):
  if any(s in ob.name for s in ('pot','basket','wicker')):continue
  archive.objects.link(ob);source.objects.unlink(ob);retired.append(ob.name);copy(ob)
for ob in made:ob.location.y-=.45
# Carry the adjacent ledge/pots and nearest basket clear of the relocated pane.
for src in (source,bpy.data.collections['DETAIL v49 | User-photo porch window and paving']):
 for ob in list(src.objects):
  near_weave='wicker cone weave' in ob.name and int(ob.name.rsplit('.',1)[1])<176 if '.' in ob.name else 'wicker cone weave' in ob.name
  near_chain='basket suspension chain' in ob.name and ('.' not in ob.name or int(ob.name.rsplit('.',1)[1])<3)
  if (src==source and any(s in ob.name for s in ('basket','wicker','separate raised plant ledge'))) or ob.name in ['Holmdale v49 | observed pot '+str(i) for i in (7,8,9)] or (src!=source and (near_weave or near_chain)):
   archive.objects.link(ob);src.objects.unlink(ob);retired.append(ob.name);d=copy(ob);d.location.y-=.45
bpy.context.view_layer.update()
for ob in made:
 if any(s in ob.name for s in ('basket','wicker')):ob.location.y-=.35
bpy.context.view_layer.update()
report={'new_meshes':len(made),'archived_unchanged':retired,'mirror_house_local':[list(row) for row in mirror],'left_width_before':.68,'left_width_after':1.07,'right_width_retained':1.07,'bad_closed_meshes':bad,'porch_fit_translation_y':-.45,'central_door_landing_right_window':'Shapes retained; porch and landing brought forward together to fit full left return outside house shell','basis':'Sam explicitly requested mirroring approved right window, including upper vent'}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(out));result=report
