"""Review-led clearance and crossing corrections, retaining superseded originals."""
from pathlib import Path
import bpy,bmesh,json,math,time,ast
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v55'
assert Path(bpy.data.filepath).name=='pharmacie-surveyed-streets-v54.blend'
OUT=ROOT/'assets/blender/pharmacie-route-working-v55.blend';assert not OUT.exists()
d=json.loads((dest/'prepared-fixes.json').read_text());schedule=json.loads((ROOT/'recon/v54/prepared-street.json').read_text());sc=schedule['scale_BU_per_m'];start=time.monotonic();scene=bpy.context.scene
original={o.name:(o.matrix_basis.copy(),o.data) for o in scene.objects};made=[];retired=[];counter=0;item={};basis=Matrix.Identity(4)
coll=bpy.data.collections.new('STREET v55 | Reviewed route clearance and details');scene.collection.children.link(coll);archive=bpy.data.collections.new('ARCHIVE v55 | Superseded join and street details');archive.use_fake_user=True
brick=bpy.data.materials['Shop v19 | brick relief'];roofmat=bpy.data.materials['Street v17 | slate'];white=bpy.data.materials['Survey v54 | aged white joinery'];dark=bpy.data.materials['Survey v54 | dark ironwork'];cream=bpy.data.materials['Survey v54 | warm cream render'];brown=bpy.data.materials['Survey v54 | brown roof tiles'];glass=bpy.data.materials['Survey v54 | blue grey glazing'];paving=bpy.data.materials['Syston v27 | concrete paving joints'];roadmat=bpy.data.materials['Street v36 | aged asphalt Street v17 | asphalt']
src=ast.parse((ROOT/'scripts/build_street_v54.py').read_text());defs=[n for n in src.body if isinstance(n,ast.FunctionDef)];exec(compile(ast.Module(body=defs,type_ignores=[]),'<street helpers>','exec'));F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
route=json.loads((ROOT/'recon/v53/survey-geometry.json').read_text())['route_world'];segments=[];total=0
for a,b in zip(route,route[1:]):
 L=math.dist(a,b);segments.append((total,total+L,Vector(a),Vector(b)));total+=L
def archive_ob(ob):
 if ob.name in retired:return
 archive.objects.link(ob)
 for c in list(ob.users_collection):
  if c!=archive:c.objects.unlink(ob)
 retired.append(ob.name)
for name in d['retire']:archive_ob(bpy.data.objects[name])
archive_ob(bpy.data.objects['Survey v54 | street | boundary 0002'])
for key,data in d['surfaces'].items():mesh(key,data['vertices'],data['faces'],brick)
modified=[]
for ob in list(scene.objects):
 if not ob.name.startswith('Survey v54 |'):continue
 fid=ob.get('frontage_id');delta=None;flatten=False
 if fid=='R054':delta=ob.matrix_world.to_3x3()@Vector((0,5.5,0))
 elif fid=='R047' and 'boundary' in ob.name:delta=ob.matrix_world.to_3x3()@Vector((0,.9,0))
 spec=next((r for r in schedule['frontages'] if r['id']==fid),None)
 if spec and spec['style']=='shopdormer' and ob.type=='MESH':
  zs=[v.co.z for v in ob.data.vertices]
  flatten='dormer' in ob.name or ('window' in ob.name and min(zs)>=spec['eaves_m']*sc-.11)
 if delta is not None or flatten:
  cp=ob.copy();cp.data=ob.data.copy();cp.name=ob.name.replace('v54','v55',1);coll.objects.link(cp);made.append(cp);archive_ob(ob)
  if delta is not None:cp.matrix_world.translation+=delta
  if flatten:
   # Vertices in the dormer-roof object's translated frame start at zero.
   pivot=0 if 'dormer roof' in ob.name else spec['eaves_m']*sc
   for v in cp.data.vertices:v.co.z=pivot+(v.co.z-pivot)*.45
   if 'dormer roof' in ob.name:cp.matrix_world.translation.z=spec['eaves_m']*sc+(ob.matrix_world.translation.z-spec['eaves_m']*sc)*.45
  modified.append(cp.name)
# Retire coarse post-v40 proxies where the new photo-led frontages supersede them.
for osm in ('173168745','429101652','431818792'):
 ob=bpy.data.objects.get('Extension v41 | OSM footprint '+osm)
 if ob and ob.name in scene.objects:archive_ob(ob)
crossings=[o for o in list(scene.objects) if o.type=='MESH' and 'road crossing stripe' in o.name and o.name.startswith('Survey v54')]
for ob in crossings:archive_ob(ob)
for chain in (212,552):
 basis=streetframe(chain,1,0)
 for j in range(7):
  x=-2.2+j*.65;box('corrected crossing stripe',x,x+.33,-3.8,3.8,-.079,-.073,white)
# A closed, labelled static terminal beyond B, not a claim about a real fence.
points=schedule['barkby_world'];end=Vector(points[-1]);u=(end-Vector(points[-2])).normalized();n=Vector((-u.y,u.x));p=end+u*2.2
basis=Matrix(((n.x,u.x,0,p.x),(n.y,u.y,0,p.y),(0,0,1,0),(0,0,0,1)))
box('B route terminal ground support',-7,7,-3,1,-1.7,-.3,bpy.data.materials['Extension v41 | earth backing']);box('B route terminal tarmac backing',-3.5,3.5,-2.21,.2,-.3,-.08,roadmat)
for xx in (-5.3,0,5.3):box('B route static terminal pier',xx-.12,xx+.12,-.05,.17,-.3,2.5,brick)
box('B route static closed terminal',-5.4,5.4,0,.1,.2,2.2,dark);sign('MAP BOUNDARY',4.5,1.3,dark)
basis=Matrix.Identity(4);bpy.context.view_layer.update();bad=[]
for ob in made:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
for name,(matrix,data) in original.items():
 ob=bpy.data.objects[name];assert ob.data==data and max(abs(ob.matrix_basis[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5,name
report={'source':'assets/blender/pharmacie-surveyed-streets-v54.blend','output':str(OUT.relative_to(ROOT)),'new_closed_meshes':sum(o.type=='MESH' for o in made),'new_text_objects':sum(o.type=='FONT' for o in made),'preserved_source_objects':len(original),'archived_unchanged':retired,'modified_copies':modified,'nonmanifold_or_nonpositive':bad,'limits':d['limits']+['The terminal beyond B is an explicit static game boundary, not an observed real fence.','BO3 unchanged.'],'seconds':time.monotonic()-start}
(dest/'build-validation.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result={k:v for k,v in report.items() if k not in ('modified_copies','archived_unchanged')}
