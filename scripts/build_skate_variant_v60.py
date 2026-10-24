"""Separate skate dressing; source map and neutral demo remain unchanged."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'recon/skate-v60';DEST.mkdir(parents=True,exist_ok=True)
SOURCE=Path(bpy.data.filepath);assert SOURCE.name=='pharmacie-demo-base-v59.blend'
OUT=ROOT/'assets/blender/pharmacie-skate-street-v60.blend';assert not OUT.exists()
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest();scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections.new('SKATE v60 | Street session additions');scene.collection.children.link(coll)
grinds=bpy.data.collections.new('SKATE v60 | Authored grind paths');scene.collection.children.link(grinds)
archive=bpy.data.collections.new('ARCHIVE SKATE v60 | Parked vehicles retained');archive.use_fake_user=True
made=[];rails=[];retired=[];scale=1.0640686466;floor=-.08
def mat(name,color,metal=0,rough=.75):
 m=bpy.data.materials.new('Skate v60 | '+name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
concrete=mat('weathered cast concrete',(.42,.425,.39));steel=mat('galvanized rubbed steel',(.38,.405,.42),.8,.3);black=mat('dark street ironwork',(.065,.075,.08),.7,.42);wood=mat('loading deck timber',(.32,.235,.15));yellow=mat('muted safety paint',(.68,.48,.13));dark=mat('expansion seams',(.16,.17,.16))
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new('Skate v60 | '+name,me);coll.objects.link(o);o['skate_addition']=True;o['provenance']='Original fictional skate adaptation; no claim of real Syston ramp/rail';made.append(o);return o
def box(name,a,b,c,d,e,f,m):return mesh(name,[(a,c,e),(b,c,e),(b,d,e),(a,d,e),(a,c,f),(b,c,f),(b,d,f),(a,d,f)],F,m)
def cylinder(name,a,b,r,m):
 a,b=Vector(a),Vector(b);length=(b-a).length;n=16
 vs=[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z) for z in (-length/2,length/2) for i in range(n)]
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 o=mesh(name,vs,fs,m);o.location=(a+b)/2;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 return o
def rail(name,points,r=.04):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,q in zip(sp.points,points):p.co=(*q,1)
 o=bpy.data.objects.new('Skate grind | '+name,cu);grinds.objects.link(o);o.hide_render=True;o['skate_grind_path']=True;o['rail_radius_m']=r
 rails.append({'name':o.name,'points_BU':points});return o
def profile(name,origin,width,points,m,yaw=0):
 # A closed prism, with its authored top profile in local x/z.
 n=len(points);vs=[(x,y,z) for y in (-width/2,width/2) for x,z in points]
 fs=[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 o=mesh(name,vs,fs,m);o.matrix_world=Matrix.Translation(Vector(origin))@Matrix.Rotation(yaw,4,'Z');return o
for ob in list(scene.objects):
 if ob.name.startswith('Street v31 | V0'):
  archive.objects.link(ob)
  for c in list(ob.users_collection):
   if c!=archive:c.objects.unlink(ob)
  retired.append(ob.name)
# A small loading-bank kicker with a flush steel toe, generous flat run-outs.
profile('loading-bank kicker',(-6,-7.8,floor),2.1,[(-.3,-.1),(3.0,-.1),(3.0,.62),(2.65,.62),(0,.002)],concrete)
box('kicker steel toe',-6.32,-5.92,-8.88,-6.72,floor-.025,floor+.008,steel)
box('kicker coping lip',-3.38,-3.0,-8.87,-6.73,floor+.61,floor+.64,steel)
# Kerb-height civic ledge, grind path centred on the outer edge.
box('street ledge plinth',-20,-12,-9.65,-8.65,floor-.08,floor+.43,concrete)
box('street ledge rubbed cap',-20.04,-11.96,-9.68,-8.62,floor+.43,floor+.49,stone:=mat('pale ledge cap',(.57,.57,.52)))
rail('civic ledge edge',[(-20,-8.64,floor+.49),(-12,-8.64,floor+.49)],.025)
for x in (-18,-15):box('ledge cap expansion joint',x,x+.014,-9.681,-8.619,floor+.489,floor+.493,dark)
# A low, straight tubular rail with a clear approach on both ends.
for x in (12.2,15.6,19.0):
 box('rail anchor foot',x-.13,x+.13,-7.95,-7.65,floor-.02,floor+.04,steel)
 cylinder('rail upright',(x,-7.8,floor+.04),(x,-7.8,floor+.65),.037,black)
cylinder('flat rail top',(11.4,-7.8,floor+.69),(19.8,-7.8,floor+.69),.045,steel)
rail('pub street flatbar',[(11.4,-7.8,floor+.69),(19.8,-7.8,floor+.69)],.045)
# Manual pad styled as a shallow service island with banks at either end.
profile('manual loading island',(29,-7.6,floor),2.5,[(0,-.10),(8,-.10),(8,.002),(6.65,.34),(1.35,.34),(0,.002)],concrete)
box('manual island coping',30.35,35.65,-6.39,-6.34,floor+.31,floor+.355,steel)
rail('manual island long edge',[(30.4,-6.36,floor+.355),(35.6,-6.36,floor+.355)],.025)
# Curved bank on the closed street end; radius and height in calibrated metres.
R=2.3*scale;H=1.45*scale;angle=math.acos(1-H/R);run=R*math.sin(angle)
arc=[(R*math.sin(angle*i/40),R*(1-math.cos(angle*i/40))) for i in range(41)]
profile('street end curved return',(49,-7.15,floor),4.2,[(0,-.12),(run+1.25,-.12),(run+1.25,H),*reversed(arc)],concrete)
cylinder('quarter return coping',(49+run,-9.25,floor+H),(49+run,-5.05,floor+H),.045,steel)
rail('quarter return coping',[(49+run,-9.25,floor+H),(49+run,-5.05,floor+H)],.045)
for y in (-9.21,-5.1):box('return deck edge paint',49+run+.15,49+run+1.15,y,y+.055,floor+H+.001,floor+H+.008,yellow)
# Low bank near the junction returns the line without filling the whole road.
profile('junction return bank',(-26,-6.8,floor),3.0,[(0,-.12),(3.7,-.12),(3.7,.002),(1.1,.82),(0,.82)],concrete)
for i in range(3):box('bank deck timber strip',-25.9,-25.0,-8.24+i*.96,-7.35+i*.96,floor+.82,floor+.86,wood)
bad=[]
for o in made:
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free()
assert not bad,bad
spawn=bpy.data.objects.new('Skate v60 | Session spawn',None);coll.objects.link(spawn);spawn.location=(4,-7.8,.20);spawn['heading_radians']=math.pi/2;spawn.empty_display_type='ARROWS';spawn.empty_display_size=1
scene['skate_variant_source']='assets/blender/pharmacie-demo-base-v59.blend'
scene['skate_variant_status']='Separate fictional street-session geometry; runtime verification pending'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
(DEST/'build-validation.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT)),'source_sha256':source_hash,'output':str(OUT.relative_to(ROOT)),'new_closed_meshes':len(made),'grind_paths':rails,'archived_vehicle_objects':retired,'nonmanifold_or_nonpositive':bad,'spawn_BU':list(spawn.location),'BU_per_m':scale,'limits':['Original v57 and neutral v59 unchanged.','All skate obstacles are fictional adaptations.','Geometry/manifold checks are not playable skating verification.','Existing source photo and dimensional limitations remain.']},indent=2))
print('SKATE_VARIANT_SAVED',len(made),'closed meshes',len(rails),'grind paths',flush=True)
