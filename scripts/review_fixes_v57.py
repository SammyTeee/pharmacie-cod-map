"""Visual-review corrections: residential side and usable dormer silhouettes."""
from pathlib import Path
import bpy,bmesh,json,math,time,ast
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v57';dest.mkdir(exist_ok=True)
assert Path(bpy.data.filepath).name=='pharmacie-surveyed-route-v56.blend'
OUT=ROOT/'assets/blender/pharmacie-surveyed-route-v57.blend';assert not OUT.exists()
schedule=json.loads((ROOT/'recon/v54/prepared-street.json').read_text());sc=schedule['scale_BU_per_m'];scene=bpy.context.scene;start=time.monotonic();original={o.name:(o.matrix_basis.copy(),o.data) for o in scene.objects}
coll=bpy.data.collections.new('STREET v57 | Overhead residential side and dormer corrections');scene.collection.children.link(coll);archive=bpy.data.collections.new('ARCHIVE v57 | Residential side trial and flattened dormers');archive.use_fake_user=True;retired=[];made=[];counter=0;basis=Matrix.Identity(4);item={}
brick=bpy.data.materials['Shop v19 | brick relief'];roofmat=bpy.data.materials['Street v17 | slate'];white=bpy.data.materials['Survey v54 | aged white joinery'];cream=bpy.data.materials['Survey v54 | warm cream render'];glass=bpy.data.materials['Survey v54 | blue grey glazing']
dark=bpy.data.materials['Survey v54 | dark ironwork']
src=ast.parse((ROOT/'scripts/build_street_v54.py').read_text().replace('Survey v54 |','Survey v57 |'));defs=[n for n in src.body if isinstance(n,ast.FunctionDef)];exec(compile(ast.Module(body=defs,type_ignores=[]),'<street helpers>','exec'));F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def archive_ob(ob):
 archive.objects.link(ob)
 for c in list(ob.users_collection):
  if c!=archive:c.objects.unlink(ob)
 retired.append(ob.name)
def matrix(f):
 p=f['origin'];x=f['x'];n=f['y'];return Matrix(((x[0],n[0],0,p[0]),(x[1],n[1],0,p[1]),(0,0,1,0),(0,0,0,1)))
route=json.loads((ROOT/'recon/v53/survey-geometry.json').read_text())['route_world'];segments=[];total=0
for a,b in zip(route,route[1:]):L=math.dist(a,b);segments.append((total,total+L,Vector(a),Vector(b)));total+=L
sidechanges=[]
for item in schedule['frontages'][:9]:
 old=matrix(item['frame']);chain=item['chain_m']*sc
 for aa,bb,a,b in segments:
  if aa<=chain<=bb:p=a+(b-a).normalized()*(chain-aa);break
 new=old.copy();new.translation.x=2*p.x-old.translation.x;new.translation.y=2*p.y-old.translation.y
 for i in (0,1):
  for j in (0,1):new[i][j]=-old[i][j]
 change=new@old.inverted()
 for ob in list(scene.objects):
  if ob.get('frontage_id')!=item['id']:continue
  cp=ob.copy();cp.data=ob.data.copy();cp.name=ob.name.replace('v54','v57',1);cp.matrix_world=change@ob.matrix_world;coll.objects.link(cp);cp['side_revision']='Corrected relative to existing approved opposite placeholders and number29 root';made.append(cp);archive_ob(ob)
 sidechanges.append({'frontage':item['id'],'old_origin':list(old.translation),'new_origin':list(new.translation)})
for item in schedule['frontages']:
 if item['style']!='shopdormer':continue
 h=item['eaves_m']*sc
 for ob in list(scene.objects):
  if ob.get('frontage_id')!=item['id'] or ob.type!='MESH':continue
  zs=[v.co.z for v in ob.data.vertices]
  if 'dormer' in ob.name or ('window' in ob.name and min(zs)>=h-.11):archive_ob(ob)
 basis=matrix(item['frame']);depth=.85*sc
 box('dormer cream face',-.95,.95,depth,depth+1.8,h+.25,h+1.65,cream);window(0,h+.53,1.5,1.0,y=depth)
 # Low pitched dormer roof rests on the face, no gap or hidden window.
 vs=[(-1.05,depth-.12,h+1.65),(1.05,depth-.12,h+1.65),(1.05,depth+1.9,h+1.65),(-1.05,depth+1.9,h+1.65),(0,depth-.12,h+2.17),(0,depth+1.9,h+2.17)]
 mesh('low dormer pitched roof',vs,[(3,2,1,0),(0,1,4),(3,5,2),(0,4,5,3),(1,2,5,4)],roofmat)
bpy.context.view_layer.update();bad=[]
for ob in made:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
for name,(mat,data) in original.items():
 ob=bpy.data.objects[name];assert ob.data==data and max(abs(ob.matrix_basis[r][c]-mat[r][c]) for r in range(4) for c in range(4))<1e-5,name
report={'source':'assets/blender/pharmacie-surveyed-route-v56.blend','output':str(OUT.relative_to(ROOT)),'new_closed_meshes':sum(o.type=='MESH' for o in made),'preserved_source_objects':len(original),'archived_unchanged':retired,'side_changes':sidechanges,'nonmanifold_or_nonpositive':bad,'limits':['Newly inferred residential plots remain approximate; original user-authorized opposite placeholders retained.','Approved number29 assembly unchanged from v53 alignment.','BO3 unchanged.'],'seconds':time.monotonic()-start}
(dest/'build-validation.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result={k:v for k,v in report.items() if k not in ('side_changes','archived_unchanged')}
