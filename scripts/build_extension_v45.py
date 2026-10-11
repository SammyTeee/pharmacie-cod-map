"""Station corridor and bounded Holmdale turning end; all estimates labelled."""
from pathlib import Path
import bpy,bmesh,json,math,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v45'
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-house-v44.blend'
OUT=ROOT/'assets/blender/pharmacie-station-holmdale-v45.blend';assert not OUT.exists()
scene=bpy.context.scene;original=[(o,o.matrix_basis.copy(),o.data) for o in scene.objects];start=time.monotonic()
d=json.loads((dest/'prepared-surfaces.json').read_text());route=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
coll=bpy.data.collections.new('MAPPING v45 | Station corridor and Holmdale turning end');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v45 | Superseded joined extension surfaces');archive.use_fake_user=True
retired=[]
for key in ('road','kerb','footway','terrain','boundary'):
 ob=bpy.data.objects['Extension v41 | Joined '+key];archive.objects.link(ob)
 for c in list(ob.users_collection):
  if c!=archive:c.objects.unlink(ob)
 retired.append(ob.name)
made=[]
def mat(name,c):
 m=bpy.data.materials.new('Extension v45 | '+name);m.diffuse_color=(*c,1);return m
ballast=mat('rail ballast',(.29,.27,.23));steel=mat('rail steel',(.27,.29,.28));sleeper=mat('concrete sleepers',(.36,.35,.31));fence=mat('dark grey perimeter steel',(.10,.13,.13));timber=mat('weathered terminal timber',(.28,.26,.21));yellow=mat('parking markings',(.63,.52,.15))
materials={'road':bpy.data.materials['Street v36 | aged asphalt Street v17 | asphalt'],'kerb':bpy.data.materials['Extension v41 | pale concrete kerbs'],'footway':bpy.data.materials['Syston v27 | concrete paving joints'],'terrain':bpy.data.materials['Extension v41 | earth backing'],'rail terrain':ballast,'boundary':bpy.data.materials['Shop v19 | brick relief'],'station perimeter plinth':bpy.data.materials['Shop v19 | brick relief'],'ramp':bpy.data.materials['Syston v27 | concrete paving joints']}
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 ob=bpy.data.objects.new('Extension v45 | '+name,me);coll.objects.link(ob);ob['engine_implemented']=False;made.append(ob);return ob
for key,data in d['surfaces'].items():mesh('Joined '+key,data['vertices'],data['faces'],materials[key])
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def block(a,b,width,z0,z1):
 a=Vector(a);b=Vector(b);u=(b-a).normalized();n=Vector((-u.y,u.x));pts=[a+n*width/2,b+n*width/2,b-n*width/2,a-n*width/2];return [(p.x,p.y,z) for z in (z0,z1) for p in pts]
def beam(name,a,b,width,z0,z1,m):return mesh(name,block(a,b,width,z0,z1),F,m)
def grouped(name,parts,m):
 vs=[];fs=[]
 for p in parts:
  idx=len(vs);vs.extend(p);fs.extend([tuple(idx+i for i in f) for f in F])
 return mesh(name,vs,fs,m)
def sample(points,dist):
 for aa,bb in zip(points,points[1:]):
  a=Vector(aa);b=Vector(bb);L=(b-a).length
  if dist<=L:return a+(b-a)*(dist/L)
  dist-=L
 return Vector(points[-1])
for j,r in enumerate(d['rail_paths']):
 pts=r['points'];length=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]));gauge=1.435*route['scale']
 for k,(aa,bb) in enumerate(zip(pts,pts[1:])):
  a=Vector(aa);b=Vector(bb)
  if (b-a).length<.05:continue
  u=(b-a).normalized();n=Vector((-u.y,u.x))
  beam('ballast track bed '+str(j)+' '+str(k),a,b,3.05,-.97,-.88,ballast)
  for side in (-1,1):beam('rail '+str(j)+' '+str(k)+' '+str(side),a+n*side*gauge/2,b+n*side*gauge/2,.065,-.77,-.62,steel)
 for k in range(math.floor(length/.67)):
  t=(k+.5)*.67;p=sample(pts,t);u=(sample(pts,min(length,t+.1))-sample(pts,max(0,t-.1))).normalized();n=Vector((-u.y,u.x));beam('sleeper '+str(j)+' '+str(k),p-n*1.35,p+n*1.35,.20,-.89,-.77,sleeper)
# Vertical edge below the retained platform, not an invented full-height wall.
ref=json.loads((ROOT/'recon/v43/station-reference.json').read_text());platform=next(w['points'] for w in ref['mapped_ways'] if w['osm_way']=='309564449')
for j,(a,b) in enumerate(zip(platform[:2],platform[1:3])):beam('platform railward brick retaining face '+str(j),a,b,.15,-.98,.03,materials['boundary'])
frame=d['station_frame'];a=Vector(frame['origin']);u=Vector(frame['u']);n=Vector(frame['n'])
def local(x,y):return a+u*x+n*y
# Parallel ramp handrails leave wide gaps at its entrance and platform turn.
for side in (2.7,6.3):
 endx=35 if side==2.7 else 31
 beam('parallel ramp handrail',local(23,side),local(endx,side),.055,.99,1.05,fence)
 beam('parallel ramp lower rail',local(23,side),local(endx,side),.04,.49,.54,fence)
 for x in range(23,endx+1,2):beam('parallel ramp post',local(x-.03,side),local(x+.03,side),.06,-.08,1.05,fence)
# Perimeter metal panels sit on low plinths well outside the platform/track space.
for j,pts in enumerate(d['station_fence_paths']):
 L=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]));count=math.ceil(L/2.5)
 for k in range(count):
  a0=sample(pts,L*k/count);b0=sample(pts,L*(k+1)/count)
  if (b0-a0).length<.05:continue
  parts=[block(a0,b0,.045,.59,.64),block(a0,b0,.045,1.64,1.69)]
  uu=(b0-a0).normalized()
  for t in range(12):
   p=a0.lerp(b0,t/11);parts.append(block(p-uu*.013,p+uu*.013,.026,.40,1.79))
  grouped('station perimeter steel panel '+str(j)+' '+str(k),parts,fence)
# Photo-observed cul-de-sac end wall and timber fence; position estimated.
end=Vector(route['holmdale'][-1]);t=(end-Vector(route['holmdale'][-2])).normalized();nn=Vector((-t.y,t.x));center=end+t*6.8
beam('Holmdale terminal brick wall',center-nn*6.0,center+nn*6.0,.23,-.3,.65,materials['boundary'])
parts=[]
for k in range(55):
 p=center+nn*(-6+k*12/55);parts.append(block(p,p+nn*.208,.07,.65,2.05))
grouped('Holmdale terminal timber fence',parts,timber)
# Restrained parking-space lines: estimated scene detail on mapped car-park polygon.
for x in range(-52,17,3):beam('station parking bay line',local(x,15),local(x,20),.075,-.079,-.074,white if 'white' in globals() else materials['kerb'])
bpy.context.view_layer.update()
for ob,matrix,data in original:
 current=ob.matrix_basis.copy();assert ob.data==data and max(abs(current[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5,ob.name
bad=[]
for ob in made:
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
report={'source':'assets/blender/pharmacie-holmdale-house-v44.blend','output':str(OUT.relative_to(ROOT)),'new_closed_meshes':len(made),'parent_objects_preserved':len(original),'archived_unchanged':retired,'nonmanifold_or_nonpositive':bad,'rail_paths':len(d['rail_paths']),'limits':d['limits']+['Rail corridor and perimeter are static; no train or BO3 behavior.','Parking markings, ramp and boundary details are estimates.'],'seconds':time.monotonic()-start}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
