"""Replace thin preview curtain proxies with photo-like pale side panels."""
from pathlib import Path
import bpy,bmesh,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-house-v44.blend'
coll=bpy.data.collections['DETAIL v44 | Number 29 photo-led bungalow'];root=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'];material=bpy.data.materials['Holmdale v44 | pale curtains']
archive=bpy.data.collections.new('ARCHIVE v44 | Thin curtain proxies');archive.use_fake_user=True;made=[]
for ob in list(coll.objects):
 if 'curtain fold' in ob.name:archive.objects.link(ob);coll.objects.unlink(ob)
 if ob.type!='MESH' or 'glazing' not in ob.name or 'porch' in ob.name:continue
 vs=ob.data.vertices;a=Vector((vs[0].co.x,vs[0].co.y));b=Vector((vs[1].co.x,vs[1].co.y));w=(b-a).length;u=(b-a).normalized();n=Vector((u.y,-u.x));z0=min(v.co.z for v in vs)+.04;z1=max(v.co.z for v in vs)-.06
 for label,s0,s1 in (('left',.025,w*.23),('right',w*.77,w-.025)):
  pts=[a+u*s+n*t for s,t in ((s0,.032),(s1,.032),(s1,.038),(s0,.038))];N=4
  verts=[(p.x,p.y,z) for z in (z0,z1) for p in pts];faces=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
  me=bpy.data.meshes.new('pale side curtain panel');me.from_pydata(verts,[],faces);me.materials.append(material);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges) and bm.calc_volume(signed=True)>0;bm.to_mesh(me);bm.free()
  new=bpy.data.objects.new(ob.name+' '+label+' curtain panel',me);coll.objects.link(new);new.parent=root;made.append(new)
bpy.context.view_layer.update();p=ROOT/'recon/v44/validation.json';d=json.loads(p.read_text());d['active_new_meshes']=sum(o.type=='MESH' for o in coll.objects);d['additional_curtain_panels']=len(made);d['archived_thin_curtains']=len(archive.objects);d['corrections'].append('Pale side curtains replace thin bar-like proxies');p.write_text(json.dumps(d,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);result=d
