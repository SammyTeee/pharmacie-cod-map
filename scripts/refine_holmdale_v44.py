"""Correct preview curtains, vegetation and road-facing fence setback in v44."""
from pathlib import Path
import bpy,bmesh,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-house-v44.blend'
coll=bpy.data.collections['DETAIL v44 | Number 29 photo-led bungalow']
archive=bpy.data.collections.new('ARCHIVE v44 | Fence pieces beyond pavement setback');archive.use_fake_user=True
for ob in list(coll.objects):
 if ob.type!='MESH':continue
 if any(s in ob.name for s in ('right boundary masonry','right timber fence board','right fence post')):
  if max(v.co.y for v in ob.data.vertices)<=-7.5:
   archive.objects.link(ob);coll.objects.unlink(ob)
  else:
   for v in ob.data.vertices:v.co.y=max(v.co.y,-7.5)
   ob.data.update()
 if 'curtain fold' in ob.name:
  # Every panel's front normal is perpendicular to its long horizontal edge.
  vs=ob.data.vertices;edge=Vector((vs[1].co.x-vs[0].co.x,vs[1].co.y-vs[0].co.y)).normalized();normal=Vector((edge.y,-edge.x))
  for v in vs:v.co.x+=normal.x*.045;v.co.y+=normal.y*.045
  ob.data.update()
 if any(s in ob.name for s in ('foliage','pot plant','round door ornament')):
  material=ob.data.materials[0];bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1);me=bpy.data.meshes.new(ob.data.name+' refined');bm.to_mesh(me);bm.free();me.materials.append(material);ob.data=me
bpy.context.view_layer.update();bad=[]
for ob in coll.objects:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
p=ROOT/'recon/v44/validation.json';d=json.loads(p.read_text());d['active_new_meshes']=sum(o.type=='MESH' for o in coll.objects);d['archived_fence_parts']=len(archive.objects);d['corrections']=['Fence trimmed to leave existing pavement route clear','Curtain folds visible in material previews','Less angular foliage proxies'];p.write_text(json.dumps(d,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);result=d
