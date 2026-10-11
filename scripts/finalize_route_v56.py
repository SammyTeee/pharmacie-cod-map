"""Final surveyed route surface corrections; all replaced geometry retained."""
from pathlib import Path
import bpy,bmesh,json,time
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v56'
assert Path(bpy.data.filepath).name=='pharmacie-route-working-v55.blend'
OUT=ROOT/'assets/blender/pharmacie-surveyed-route-v56.blend';assert not OUT.exists()
d=json.loads((dest/'prepared-final.json').read_text());scene=bpy.context.scene;start=time.monotonic();original={o.name:(o.matrix_basis.copy(),o.data) for o in scene.objects}
coll=bpy.data.collections.new('MAPPING v56 | Overhead traced end and clear seam');scene.collection.children.link(coll);archive=bpy.data.collections.new('ARCHIVE v56 | Symmetric head and seam perimeter');archive.use_fake_user=True;retired=[];made=[]
for key,data in d['surfaces'].items():
 name='Survey v54 | street | clear perimeter 0001' if key=='perimeter' else 'Survey v53 | Joined '+key
 ob=bpy.data.objects[name];archive.objects.link(ob)
 for c in list(ob.users_collection):
  if c!=archive:c.objects.unlink(ob)
 retired.append(name);me=bpy.data.meshes.new('Survey v56 | '+key);me.from_pydata(data['vertices'],[],data['faces']);me.materials.append(ob.data.materials[0]);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 new=bpy.data.objects.new('Survey v56 | '+key,me);coll.objects.link(new);new['engine_implemented']=False;made.append(new)
bpy.context.view_layer.update();bad=[]
for ob in made:
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
for name,(matrix,data) in original.items():
 ob=bpy.data.objects[name];assert ob.data==data and max(abs(ob.matrix_basis[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5,name
report={'source':'assets/blender/pharmacie-route-working-v55.blend','output':str(OUT.relative_to(ROOT)),'new_closed_meshes':len(made),'preserved_source_objects':len(original),'archived_unchanged':retired,'nonmanifold_or_nonpositive':bad,'limits':d['limits'],'seconds':time.monotonic()-start}
(dest/'build-validation.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
