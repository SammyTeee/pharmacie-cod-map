"""Rigidly fit approved number 29 to the surveyed end plot; retain old sources."""
from pathlib import Path
import bpy,bmesh,json,time
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v53'
assert Path(bpy.data.filepath).name=='pharmacie-station-frontage-v52.blend'
OUT=ROOT/'assets/blender/pharmacie-holmdale-alignment-v53.blend';assert not OUT.exists()
scene=bpy.context.scene;start=time.monotonic()
d=json.loads((dest/'holmdale-alignment.json').read_text())
root=bpy.data.objects['Holmdale v44 | Movable number 29 assembly']
before=list(root.location)
original={o.name:(o.matrix_basis.copy(),o.data) for o in scene.objects}
coll=bpy.data.collections.new('MAPPING v53 | Surveyed Holmdale end alignment');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v53 | Estimated Holmdale surfaces and terminal');archive.use_fake_user=True
retired=[];made=[]
for key in ('road','kerb','footway','terrain','boundary'):
 ob=bpy.data.objects['Extension v45 | Joined '+key];archive.objects.link(ob)
 for c in list(ob.users_collection):
  if c!=archive:c.objects.unlink(ob)
 retired.append(ob.name)
 me=bpy.data.meshes.new('Survey v53 | '+key);data=d['surfaces'][key];me.from_pydata(data['vertices'],[],data['faces']);me.materials.append(ob.data.materials[0]);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 new=bpy.data.objects.new('Survey v53 | Joined '+key,me);coll.objects.link(new);new['engine_implemented']=False;made.append(new)
for name in ('Holmdale terminal brick wall','Holmdale terminal timber fence'):
 ob=bpy.data.objects['Extension v45 | '+name];archive.objects.link(ob)
 for c in list(ob.users_collection):
  if c!=archive:c.objects.unlink(ob)
 retired.append(ob.name)
root.location.x,root.location.y=d['house_origin_world']
root['placement_source']='overhead-number29-end-plot.jpg; approximate left front corner; rigid translation v53'
bpy.context.view_layer.update()
for name,(matrix,data) in original.items():
 ob=bpy.data.objects[name]
 assert ob.data==data,name
 if ob!=root:assert max(abs(ob.matrix_basis[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5,name
bad=[]
for ob in made:
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
report={'source':'assets/blender/pharmacie-station-frontage-v52.blend','output':str(OUT.relative_to(ROOT)),'new_closed_meshes':len(made),'archived_unchanged':retired,'house_origin_before':before,'house_origin_after':list(root.location),'preserved_local_geometry_objects':len(original)-1,'nonmanifold_or_nonpositive':bad,'limits':d['limits'],'seconds':time.monotonic()-start}
(dest/'alignment-validation.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
