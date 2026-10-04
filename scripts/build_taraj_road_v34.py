"""Open the retained Melton branch and finish bounded street geometry, Blender only."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,os
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath)
assert source.name=='pharmacie-enclosure-detail-v33.blend'
OUT=ROOT/'assets/blender/pharmacie-taraj-road-v34.blend';assert not OUT.exists() or os.environ.get('V34_REBUILD')=='1'
dest=ROOT/'recon/v34';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
coll=bpy.data.collections.new('MAPPING v34 | Open Melton branch and bounded Taraj street');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v33 | West road closure opened for Melton');archive.use_fake_user=True
retired=[]
for ob in list(scene.objects):
 if ob.name.startswith(('Street v31 | G31 west','Mapping v33 | West ')) or ob.name=='G31_WEST_MELTON':
  archive.objects.link(ob)
  for c in list(ob.users_collection):
   if c!=archive:c.objects.unlink(ob)
  retired.append(ob.name)
made=[];basis=Matrix.Identity(4)
def material(name,color,metal=0):
 m=bpy.data.materials.new('Mapping v34 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
 p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=.78;p.inputs['Metallic'].default_value=metal;return m
brick=bpy.data.materials['Syston v27 | weathered brick 2'];paving=bpy.data.materials['Street v17 | paving'];asphalt=bpy.data.materials['Street v17 | asphalt'];slate=bpy.data.materials['Street v17 | slate']
stone=material('weathered coping',(.39,.38,.33));earth=material('deep terrain',(.15,.16,.115));metal=material('utility iron',(.04,.055,.055),.5);dark=material('drain recess',(.013,.019,.020));cream=material('pale sign',(.8,.77,.65));orange=material('boundary orange',(.65,.15,.02))
def mesh(name,vs,fs,m,role='scenery'):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();me.materials.append(m)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 ob=bpy.data.objects.new('Mapping v34 | '+name,me);coll.objects.link(ob);ob.matrix_world=basis.copy();ob['mapping_role']=role;ob['engine_implemented']=False;made.append(ob);return ob
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def box(name,x0,x1,y0,y1,z0,z1,m,role='scenery'):
 assert x1>x0 and y1>y0 and z1>z0,name
 return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],F,m,role)
def beam(name,a,b,w,z0,z1,m,role='boundary'):
 a,b=Vector(a),Vector(b);u=(b-a).normalized();n=Vector((-u.y,u.x))*w/2;ps=[a-n,b-n,b+n,a+n]
 return mesh(name,[(p.x,p.y,z) for z in (z0,z1) for p in ps],F,m,role)
path=[Vector(p) for p in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']]
lengths=[0]
for a,b in zip(path,path[1:]):lengths.append(lengths[-1]+(b-a).length)
def frame(s,offset=0):
 s=max(0,min(s,lengths[-1]-.001));i=next(i for i in range(len(path)-1) if lengths[i+1]>=s)
 u=(path[i+1]-path[i]).normalized();n=Vector((-u.y,u.x));return path[i]+u*(s-lengths[i])+n*offset,u,n
def chain(p):
 p=Vector(p);tests=[]
 for i,(a,b) in enumerate(zip(path,path[1:])):
  u=(b-a).normalized();t=max(0,min((p-a).dot(u),(b-a).length));tests.append(((p-a-u*t).length,lengths[i]+t))
 return min(tests)[1]
bridge=bpy.data.objects['Detail v26 | Bridge | bridge soffit deck'];bridge_s=chain(bridge.matrix_world.translation.xy)
def ribbon(name,s0,s1,width,z0,z1,m):
 ss=[s0]+[s for s in lengths if s0<s<s1]+[s1]
 # Each convex segment is a closed solid, overlapping by 10cm at bends.
 for i,(a,b) in enumerate(zip(ss,ss[1:])):
  p,u,n=frame(a);q,_,_=frame(b);beam(name+' %02d'%i,p-u*.10,q+u*.10,width,z0,z1,m,'terrain_backing')
ribbon('Deep road and footway backing',0,lengths[-1],13.1,-1,-.34,earth)
for a,b in ((0,bridge_s-7.2),(bridge_s+7.2,lengths[-1])):ribbon('Parcel terrain backing',a,b,48,-1.2,-.35,earth)
box('Junction terrain backing',-66,-18,-35,20,-1.2,-.35,earth,'terrain_backing')
# Physical outer boundaries sit behind the existing shop masses, never across entrances.
for side in (-1,1):
 for i,(a,b) in enumerate(zip(lengths,lengths[1:])):
  p,u,n=frame(a,side*23.5);q,_,_=frame(b,side*23.5)
  beam('Rear parcel boundary %d %02d'%(side,i),p-u*.15,q+u*.15,.30,-.5,3.2,brick)
  beam('Rear parcel coping %d %02d'%(side,i),p-u*.18,q+u*.18,.38,3.2,3.30,stone)
# The inferred southern arm remains closed scenery; Melton itself is opened.
for name,a,b in [('Junction west return',(-64,-33),(-64,22)),('Junction south closed arm',(-64,-33),(-18,-33)),('Junction east short return',(-18,-33),(-18,-15))]:
 beam(name,a,b,.35,-.5,3.2,brick);beam(name+' coping',a,b,.44,3.2,3.3,stone)
# Close outer road end beyond Taraj, leaving its frontage and passage accessible.
p,u,n=frame(lengths[-1]-1.5)
beam('Beyond Taraj closed road boundary',p-n*23.5,p+n*23.5,.28,-.4,3.2,metal)
beam('Beyond Taraj boundary head',p-n*23.6,p+n*23.6,.36,3.2,3.28,stone)
specs=json.loads((ROOT/'recon/v25/validation.json').read_text())['catalogue_frontages']
intervals={-1:[],1:[]}
for spec in specs:
 side=1 if spec['side']=='east' else -1;w=spec['width_m_estimate']
 ob=bpy.data.objects.get('Syston v25 | '+spec['id']+' | upper facade')
 if not ob:continue
 basis=ob.matrix_world.copy()
 w=max(v.co.x for v in ob.data.vertices)-min(v.co.x for v in ob.data.vertices)
 endpoints=[chain((basis@Vector((x,0,0))).xy) for x in (-w/2,w/2)]
 intervals[side].append((min(endpoints)-.10,max(endpoints)+.10))
 box(spec['id']+' solid frontage apron',-w/2,w/2,-.91,.80,-.27,.001,paving,'pavement')
 box(spec['id']+' buried foundation skirt',-w/2,w/2,.80,10,-.42,.015,brick,'foundation')
 # Restrained wall-side additions keep the main footway clear.
 box(spec['id']+' fascia drip',-w/2,w/2,-.255,-.20,3.34,3.40,metal)
 box(spec['id']+' entrance bulkhead body',-w/2+.34,-w/2+.53,-.245,-.18,2.96,3.17,metal)
 box(spec['id']+' entrance bulkhead lens',-w/2+.365,-w/2+.505,-.26,-.245,2.995,3.135,cream)
 for z in (.6,2.5):box(spec['id']+' rainwater fixing',w/2-.20,w/2-.05,-.24,-.12,z,z+.045,metal)
basis=Matrix.Identity(4)
taraj_s=chain(json.loads((ROOT/'recon/v24/validation.json').read_text())['road_pivot']);intervals[1].append((taraj_s-6.2,taraj_s+6.2))
infill=[]
for side in (-1,1):
 # Retained bridge rails replace front infill across the brook.
 intervals[side].append((bridge_s-7.3,bridge_s+7.3))
 spans=sorted(intervals[side]);cursor=12
 for a,b in spans+[(lengths[-1]-1.5,lengths[-1])]:
  if a>cursor+.02:
   p,u,n=frame(cursor,side*7.12);q,_,_=frame(a,side*7.12);gap=a-cursor
   height=8.8 if gap<.65 else 3.0
   beam('Frontage gap backing %d %.2f'%(side,cursor),p-u*.10,q+u*.10,.32,-.35,height,brick,'frontage_infill')
   beam('Frontage gap coping %d %.2f'%(side,cursor),p-u*.12,q+u*.12,.42,height,height+.10,stone)
   infill.append({'side':side,'start':cursor,'end':a,'height':height})
  cursor=max(cursor,b)
# Brookside is a deliberate short closed branch rather than an unbounded floating road.
branch=bpy.data.objects['Street v22 | Brookside road branch'];ps=[branch.matrix_world@v.co for v in branch.data.vertices];a=(ps[0]+ps[3])/2;b=(ps[1]+ps[2])/2;u=(b-a).xy.normalized();n=Vector((-u.y,u.x));a=a.xy
beam('Brookside supported road backing',a-u*.1,a+u*24,8,-1.1,-.32,earth,'terrain_backing')
for side in (-1,1):
 beam('Brookside side boundary '+str(side),a+u*9+n*side*3.7,a+u*24+n*side*3.7,.25,-.35,3,brick)
beam('Brookside closed service boundary',a+u*24-n*3.8,a+u*24+n*3.8,.25,-.35,3,metal)
# Tie the retained Taraj entry directly into the footway without moving architecture.
floor=bpy.data.objects['Taraj v23 | left passage floor'];pts=[floor.matrix_world@v.co for v in floor.data.vertices];front=Vector(json.loads((ROOT/'recon/v24/validation.json').read_text())['new_front']);p,u,n=frame(taraj_s)
beam('Taraj frontage footway apron',front-u*6.1,front+u*6.1,1.65,-.24,.002,paving,'pavement')
beam('Taraj buried foundation skirt',front-u*6.0+n*7.5,front+u*6.0+n*7.5,15,-.42,-.005,brick,'foundation')
# Shallow grilles and flush maintenance covers along the retained road edges.
for s in range(38,int(lengths[-1])-4,22):
 for side in (-1,1):
  p,u,n=frame(s,side*3.72);basis=Matrix(((u.x,n.x,0,p.x),(u.y,n.y,0,p.y),(0,0,1,0),(0,0,0,1)))
  box('Road drain rim %d %d'%(s,side),-.20,.20,-.115,.115,-.080,-.074,metal)
  for j in range(6):box('Road drain slot %d %d %d'%(s,side,j),-.17+j*.057,-.145+j*.057,-.085,.085,-.074,-.071,dark)
basis=Matrix.Identity(4)
for name,eye,target in json.loads((dest/'review-views.json').read_text()):
 cd=bpy.data.cameras.new('Review v34 | '+name);o=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(o);o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();cd.lens=24;cd.clip_end=1000
 if name=='06_plan':cd.type='ORTHO';cd.ortho_scale=355
scene.camera=bpy.data.objects['Review v34 | 02_junction'];bpy.context.view_layer.update()
for ob in made:
 bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges),ob.name;assert bm.calc_volume(signed=True)>0,ob.name;bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(dest/'changes.json').write_text(json.dumps({'source':str(source),'source_sha256':source_hash,'checkpoint':str(OUT),'new_closed_solids':len(made),'archived_closure':retired,'infill':infill,'bridge_chainage':bridge_s,'taraj_chainage':taraj_s,'new_solids':[o.name for o in made],'engine_verified':False,'provenance':'Original inferred Zombies enclosure/detail, not surveyed hidden architecture'},indent=2))
print('V34_BUILD_COMPLETE',len(made),flush=True)
