"""User-corrected perpendicular garage and explicitly fictional opposite houses."""
from pathlib import Path
import bpy,bmesh,json,math
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-depth-v47.blend'
OUT=ROOT/'assets/blender/pharmacie-holmdale-garage-v48.blend';assert not OUT.exists()
dest=ROOT/'recon/v48';dest.mkdir(exist_ok=True)
house=bpy.data.objects['Holmdale v44 | Movable number 29 assembly']
coll=bpy.data.collections['DETAIL v44 | Number 29 photo-led bungalow']
pivot=Vector((10.2,-2.25,0));turn=Matrix.Translation(pivot)@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation(-pivot)
garage=[];boundary=[]
for ob in list(coll.objects):
 if ob.type!='MESH':continue
 if 'garage' in ob.name:garage.append(ob);continue
 points=[ob.matrix_basis@v.co for v in ob.data.vertices]
 if any(s in ob.name for s in ('boundary','fence')):boundary.append(ob);continue
 if min(v.x for v in points)>=10.16 and any(s in ob.name for s in ('fascia','gutter','downpipe','lantern')):garage.append(ob)
for ob in garage:ob.matrix_basis=turn@ob.matrix_basis
# Keep the right plot boundary behind the rotated garage, outside its shell.
for ob in boundary:ob.location.x+=2.25
house['garage_orientation']='Sam explicitly corrected garage to 90 degrees from windows, facing inward across drive; v48 -90 local Z, pivot (10.2,-2.25); dimensions estimated'
context=bpy.data.collections.new('CONTEXT v48 | Placeholder opposite Holmdale houses');bpy.context.scene.collection.children.link(context)
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
made=[]
def material(name,c):
 m=bpy.data.materials.new('Context v48 | '+name);m.diffuse_color=(*c,1);return m
brick=material('muted red brick',(.39,.23,.17));cream=material('cream render',(.66,.63,.52));roofmat=material('grey brown tiles',(.21,.20,.17));white=material('white frames',(.77,.78,.72));glass=material('dark window glass',(.13,.19,.21));drive=material('drive concrete',(.32,.31,.28));grass=material('small front lawn',(.22,.28,.12))
def mesh(name,vs,fs,mat,parent):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();ob=bpy.data.objects.new('Context v48 | '+name,me);context.objects.link(ob);ob.parent=parent;made.append(ob);return ob
def box(name,x0,x1,y0,y1,z0,z1,mat,parent):return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],F,mat,parent)
route=json.loads((ROOT/'recon/v41/extension-route.json').read_text());pts=[Vector(p) for p in route['holmdale']];segments=[];total=0
for a,b in zip(pts,pts[1:]):
 length=(b-a).length;segments.append((total,total+length,a,b));total+=length
placements=[]
for i,chain in enumerate(range(10,int(total)-3,11)):
 for start,end,a,b in segments:
  if start<=chain<=end:
   u=(b-a).normalized();p=a+u*(chain-start);break
 n=Vector((-u.y,u.x))
 if n.dot(Vector((house.matrix_world[0][1],house.matrix_world[1][1])))>0:n=-n
 origin=p+n*10
 root=bpy.data.objects.new('Context v48 | Opposite house '+str(i+1),None);context.objects.link(root)
 root.matrix_world=Matrix(((u.x,n.x,0,origin.x),(u.y,n.y,0,origin.y),(0,0,1,0),(0,0,0,1)))
 root['evidence']='User-authorized placeholder house; invented footprint/detail, not surveyed address'
 h=2.85 if i%3==0 else 5.35
 box('house body '+str(i),-3.8,3.8,0,8,-.3,h,cream if i%3==0 else brick,root)
 mesh('closed pitched roof '+str(i),[(-4,-.2,h),(4,-.2,h),(4,8.2,h),(-4,8.2,h),(-4,4,h+2),(4,4,h+2)],[(3,2,1,0),(0,1,5,4),(4,5,2,3),(0,4,3),(1,2,5)],roofmat,root)
 box('drive apron '+str(i),-4,0,-4.7,0,-.22,-.025,drive,root)
 box('front lawn '+str(i),.3,4,-3.5,-.3,-.22,-.02,grass,root)
 box('door surround '+str(i),-.55,.55,-.10,.01,.03,2.22,white,root)
 box('door panel '+str(i),-.46,.46,-.13,-.10,.06,2.13,glass,root)
 for z in ([.8,3.35] if h>3 else [.8]):
  for x in (-2.35,2.35):
   box('window frame '+str(i),x-.8,x+.8,-.09,.02,z,z+1.45,white,root)
   box('window glazing '+str(i),x-.73,x+.73,-.12,-.09,z+.07,z+1.38,glass,root)
   box('window mullion '+str(i),x-.025,x+.025,-.15,-.12,z+.06,z+1.4,white,root)
 box('chimney '+str(i),2.4,2.95,3.5,4.2,h+1.35,h+2.7,brick,root)
 placements.append({'chainage':chain,'origin':list(origin),'height':h})
# First trial plot encroaches on the Melton junction; preserve but retire it.
first=bpy.data.objects['Context v48 | Opposite house 1']
archive=bpy.data.collections.new('ARCHIVE v48 | Junction placeholder conflict');archive.use_fake_user=True
for ob in [first]+list(first.children):archive.objects.link(ob);context.objects.unlink(ob)
bpy.context.view_layer.update();bad=[]
for ob in made:
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
report={'garage_rotated_parts':len(garage),'garage_rotation_local_degrees':-90,'garage_pivot':list(pivot),'right_boundary_shift':2.25,'placeholder_houses':len(placements),'new_closed_meshes':len(made),'placements':placements,'limits':['Placeholder houses invented at user request, not geographically verified','Garage angle user-corrected; dimensions and exact plot placement estimated','BO3 unchanged']}
report['placeholder_houses']=7
report['archived_junction_placeholder']='First trial house intersected Melton road clearance rays; retained unchanged in unlinked archive'
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
