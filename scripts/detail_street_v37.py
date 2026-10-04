"""Reference-led shelter refinement and deliberately clustered street scenes."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,random,os
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath)
assert source.name=='pharmacie-street-life-v36.blend'
out=ROOT/'assets/blender/pharmacie-street-scenes-v37.blend';assert not out.exists() or os.environ.get('V37_REBUILD')=='1'
dest=ROOT/'recon/v37';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
bpy.context.view_layer.update()
coll=bpy.data.collections.new('STREET v37 | Shelter cycles deliveries and planting');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v37 | Retained superseded shelter and block foliage');archive.use_fake_user=True
basis=Matrix.Identity(4);current='shelter';made=[];retired=[];labels=[];routes=[];views=[]
def mat(name,c,rough=.8,metal=0):
 m=bpy.data.materials.new('Street v37 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
green=mat('shelter deep green',(.026,.105,.055),.52,.3);steel=mat('galvanised steel',(.33,.36,.37),.42,.7);rubber=mat('tyre rubber',(.018,.022,.023));black=mat('dark fittings',(.025,.034,.033),.55,.25);red=mat('cycle oxblood paint',(.30,.035,.025),.42,.4);blue=mat('cycle faded teal',(.025,.19,.22),.5,.3)
wood=bpy.data.materials['Street v36 | weathered bench timber'];paper=mat('timetable ivory',(.8,.79,.68));yellow=mat('shelter visibility stripe',(.69,.56,.10));glass=mat('shelter smoke glazing',(.21,.30,.31),.16)
p=glass.node_tree.nodes['Principled BSDF'];p.inputs['Transmission Weight'].default_value=.75;p.inputs['IOR'].default_value=1.45
roof=mat('frosted roof',(.55,.64,.60),.45);roof.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value=.42
leafm=[mat('leaf tone '+str(i),c) for i,c in enumerate(((.045,.14,.035),(.08,.22,.055),(.15,.27,.075),(.21,.26,.075)))]
flower=mat('muted flowers',(.46,.12,.25));card=mat('corrugated carton',(.40,.28,.13));tape=mat('packing tape',(.59,.43,.23));paving=mat('block paving',(.29,.23,.17));joint=mat('paving joint',(.14,.13,.11));soil=bpy.data.materials['Street v36 | planter soil']
# Brick-pattern paving has metric joints and fine grain rather than a photo overlay.
n=paving.node_tree.nodes;l=paving.node_tree.links;tc=n.new('ShaderNodeTexCoord');brick=n.new('ShaderNodeTexBrick');brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=.20;brick.inputs['Row Height'].default_value=.10;brick.inputs['Mortar Size'].default_value=.004;brick.inputs['Color1'].default_value=(.26,.18,.12,1);brick.inputs['Color2'].default_value=(.40,.31,.22,1);brick.inputs['Mortar'].default_value=(.13,.12,.105,1);l.new(tc.outputs['Object'],brick.inputs['Vector']);l.new(brick.outputs['Color'],n['Principled BSDF'].inputs['Base Color']);b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.004;b.inputs['Strength'].default_value=.3;l.new(brick.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],n['Principled BSDF'].inputs['Normal'])
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new('Street v37 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['engine_implemented']=False;made.append(o);return o
def box(name,a,b,c,d,e,f,m):return mesh(name,[(a,c,e),(b,c,e),(b,d,e),(a,d,e),(a,c,f),(b,c,f),(b,d,f),(a,d,f)],F,m)
def pipe(name,a,b,r,m,sides=12):
 a,b=Vector(a),Vector(b);u=(b-a).normalized();v=u.cross(Vector((0,0,1)))
 if v.length<.01:v=u.cross(Vector((0,1,0)))
 v.normalize();w=u.cross(v);vs=[tuple(p+r*(v*math.cos(k*math.tau/sides)+w*math.sin(k*math.tau/sides))) for p in (a,b) for k in range(sides)]
 return mesh(name,vs,[tuple(reversed(range(sides))),tuple(range(sides,2*sides))]+[(k,(k+1)%sides,(k+1)%sides+sides,k+sides) for k in range(sides)],m)
def torus(name,x,y,z,R,r,m):
 ns,nt=32,8;vs=[]
 for i in range(ns):
  a=i*math.tau/ns
  for j in range(nt):
   b=j*math.tau/nt;vs.append((x+(R+r*math.cos(b))*math.cos(a),y+r*math.sin(b),z+(R+r*math.cos(b))*math.sin(a)))
 return mesh(name,vs,[(i*nt+j,((i+1)%ns)*nt+j,((i+1)%ns)*nt+(j+1)%nt,i*nt+(j+1)%nt) for i in range(ns) for j in range(nt)],m)
def blob(name,p,scale,m,rng):
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1)
 for v in bm.verts:
  v.co=Vector(p)+Vector((v.co.x*scale[0],v.co.y*scale[1],v.co.z*scale[2]))*rng.uniform(.87,1.12)
 me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free();me.materials.append(m);o=bpy.data.objects.new('Street v37 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();made.append(o);return o
def label(name,text,p,size,m):
 c=bpy.data.curves.new(name,'FONT');c.body=text;c.size=size;c.align_x='CENTER';c.extrude=.0015;c.materials.append(m);o=bpy.data.objects.new('Street v37 | '+current+' | '+name,c);coll.objects.link(o);o.matrix_world=basis@Matrix.Translation(p)@Matrix.Rotation(math.pi/2,4,'X');labels.append(o.name)
def retire(o):
 archive.objects.link(o)
 for c in list(o.users_collection):
  if c!=archive:c.objects.unlink(o)
 retired.append(o.name)
def world(p):return list(basis@Vector(p))
def route(name,ps):routes.append(dict(name=name,points=[world(p) for p in ps]))
def view(name,eye,target):views.append((name,world(eye),world(target)))
def frontage(cid):
 global basis,current
 current=cid;o=bpy.data.objects['Syston v25 | '+cid+' | upper facade'];old=o.matrix_world;cs=[old.to_3x3().col[i].normalized() for i in range(3)];sx=old.to_3x3().col[0].length;lo=min(v.co.x for v in o.data.vertices);hi=max(v.co.x for v in o.data.vertices)
 basis=Matrix(((cs[0].x,cs[1].x,cs[2].x,old.translation.x),(cs[0].y,cs[1].y,cs[2].y,old.translation.y),(cs[0].z,cs[1].z,cs[2].z,old.translation.z),(0,0,0,1)));basis.translation+=cs[0]*((lo+hi)*.5*sx);return (hi-lo)*sx
# Retain the shelter position and original posts. Replace blockout roof, back and bench.
basis=bpy.data.objects['Syston v25 | F006 | shelter post'].matrix_world.copy()
for o in list(scene.objects):
 if o.name.startswith('Syston v25 | F006 |') and any(s in o.name for s in ('shelter roof','shelter glass back','shelter bench')):retire(o)
box('block paved shelter apron',-2.45,2.45,-.72,.76,-.025,.009,paving)
for x in (-2.1,2.1):
 for y in (-.5,.5):
  box('post bolted foot',x-.09,x+.09,y-.09,y+.09,.01,.045,green)
  for dx in (-.06,.06):
   for dy in (-.06,.06):pipe('foot bolt',(x+dx,y+dy,.046),(x+dx,y+dy,.057),.009,steel,8)
# Split glazing panels with a metal lower kick panel and visible seals.
for j in range(4):
 a=-2.1+j*1.05;b=a+1.05
 box('rear lower kick panel',a+.035,b-.035,.43,.48,.08,.43,green);box('rear glass',a+.035,b-.035,.455,.477,.49,2.19,glass)
 for z in (.44,1.45,2.20):box('rear rail',a,b,.42,.50,z,z+.035,green)
 box('glazing division',a-.018,a+.018,.42,.50,.42,2.23,green)
 for k in range(2):box('visibility decal',a+.22+k*.43,a+.37+k*.43,.449,.455,1.38,1.405,yellow)
for x in (-2.1,2.1):
 box('end glazing',x-.015,x+.015,-.48,.42,.48,2.20,glass)
 box('end kick panel',x-.028,x+.028,-.48,.42,.08,.44,green)
 for z in (.44,1.45,2.20):box('end crossrail',x-.04,x+.04,-.50,.50,z,z+.04,green)
for z in (2.25,):box('front header',-2.2,2.2,-.56,-.48,z,z+.07,green)
# A sloping translucent roof following the photographed segmented canopy.
for j in range(7):
 a=-2.3+j*4.6/7;b=a+4.6/7
 ob=box('sloping frosted roof pane',a+.018,b-.018,-.71,.71,2.32,2.355,roof)
 for v in ob.data.vertices:v.co.z+=(v.co.y+.71)*.27
 pipe('roof rib',(a,-.73,2.32),(a,.73,2.714),.022,green)
for y,z in ((-.74,2.32),(.74,2.72)):pipe('canopy edge',(-2.34,y,z),(2.34,y,z),.035,green)
pipe('back gutter',(-2.32,.76,2.70),(2.32,.76,2.70),.04,green)
pipe('rainwater downpipe',(2.15,.65,.06),(2.15,.65,2.7),.025,green)
for k in range(4):box('bench timber slat',-1.67,1.30,.01+k*.075,.07+k*.075,.46,.51,wood)
for x in (-1.45,.25,1.1):
 pipe('bench foot',(x,.20,.01),(x,.20,.46),.035,green);pipe('seat divider',(x,-.01,.50),(x,-.01,.73),.018,green);pipe('divider arm',(x,-.01,.73),(x,.25,.73),.018,green)
box('timetable case',1.45,1.94,.397,.43,1.0,1.80,green);box('timetable sheet',1.48,1.91,.387,.397,1.035,1.765,paper)
label('timetable heading','BUS TIMES',(1.695,.38,1.63),.065,black)
for k in range(8):box('timetable rows',1.52,1.87,.383,.387,1.12+k*.05,1.125+k*.05,black)
route('shelter open front',[(-2.75,-1.28,0),(2.75,-1.28,0)])
route('shelter entry',[(0,-1.28,0),(0,-.48,0)])
view('01_shelter',(-4.7,-5.5,1.7),(0,.15,1.35))
# Cycle parking at the vape frontage, shallow to preserve the pavement through route.
w=frontage('B030');ox=.25
for xx in (-.6,.6):
 pipe('cycle stand leg',(ox+xx-.25,-.45,.02),(ox+xx-.25,-.45,.75),.025,steel);pipe('cycle stand leg',(ox+xx+.25,-.45,.02),(ox+xx+.25,-.45,.75),.025,steel);pipe('cycle stand top',(ox+xx-.25,-.45,.75),(ox+xx+.25,-.45,.75),.025,steel)
for j,y in enumerate((-.29,-.63)):
 x=ox+(-.12 if j==0 else .14);paint=red if j==0 else blue
 for wx in (-.60,.60):
  torus('cycle tyre',x+wx,y,.355,.315,.026,rubber);torus('cycle wheel rim',x+wx,y,.355,.284,.008,steel)
  for k in range(16):
   a=k*math.tau/16;pipe('wheel spoke',(x+wx,y,.355),(x+wx+.278*math.cos(a),y,.355+.278*math.sin(a)),.0024,steel,6)
  pipe('wheel axle',(x+wx,y-.035,.355),(x+wx,y+.035,.355),.012,steel)
 A=(x-.6,y,.355);B=(x-.17,y,.39);C=(x-.26,y,.87);D=(x+.38,y,.88);E=(x+.60,y,.355)
 for a,b in ((A,B),(A,C),(B,C),(C,D),(B,D),(D,E)):pipe('cycle frame tube',a,b,.016,paint)
 pipe('saddle stem',C,(x-.29,y,1.0),.012,steel);box('saddle',x-.41,x-.17,y-.065,y+.065,.985,1.015,black)
 pipe('handlebar stem',D,(x+.35,y,1.02),.013,steel);pipe('handlebar',(x+.35,y-.16,1.02),(x+.35,y+.16,1.02),.012,steel)
 for s in (-1,1):pipe('handlebar grip',(x+.35,y+s*.10,1.02),(x+.35,y+s*.16,1.02),.017,rubber)
 torus('chainring',x-.17,y-.02,.39,.075,.008,steel);pipe('chain upper',(x-.60,y-.03,.40),(x-.17,y-.03,.46),.004,black);pipe('chain lower',(x-.60,y-.03,.31),(x-.17,y-.03,.32),.004,black)
 pipe('pedal crank',(x-.17,y-.02,.39),(x-.17,y-.08,.29),.008,steel);box('pedal',x-.22,x-.12,y-.14,y-.04,.28,.30,black)
box('cycle parking plaque',-.4,.4,-.22,-.18,1.5,1.76,green);label('cycle plaque','CYCLE PARKING',(0,-.23,1.58),.095,paper)
route('cycle frontage through', [(-w/2+.5,-1.3,0),(w/2-.5,-1.3,0)])
view('02_cycles',(-3.8,-5.4,1.6),(.25,-.25,.8))
# A wheeled delivery cage and handcart at the Food Warehouse display end.
w=frontage('B038');x=-.3
for dx in (-.39,.39):
 for yy in (-.61,-.22):
  torus('delivery caster tyre',x+dx,yy,.12,.074,.018,rubber);pipe('caster bracket',(x+dx,yy,.12),(x+dx,yy,.25),.018,steel)
box('delivery cage platform',x-.45,x+.45,-.67,-.16,.24,.29,steel)
for dx in (-.43,.43):
 for yy in (-.64,-.19):pipe('cage upright',(x+dx,yy,.28),(x+dx,yy,1.55),.015,steel)
for z in (.48,.75,1.02,1.29,1.53):
 pipe('cage back rail',(x-.43,-.19,z),(x+.43,-.19,z),.009,steel)
 for dx in (-.43,.43):pipe('cage side rail',(x+dx,-.64,z),(x+dx,-.19,z),.009,steel)
for dx in (-.25,-.08,.08,.25):pipe('cage back vertical',(x+dx,-.19,.29),(x+dx,-.19,1.53),.006,steel)
for k in range(4):
 z=.30+k*.25;box('delivery carton',x-.34,x+.34,-.58,-.25,z,z+.23,card);box('carton tape',x-.025,x+.025,-.584,-.578,z,z+.23,tape);box('carton tape top',x-.025,x+.025,-.58,-.25,z+.23,z+.233,tape)
 label('carton handling','THIS WAY UP',(x,-.59,z+.10),.044,black)
xx=x+1.05
box('handtruck toe',xx-.22,xx+.22,-.62,-.18,.11,.145,steel)
for dx in (-.20,.20):
 torus('handtruck wheel',xx+dx,-.26,.13,.10,.022,rubber);pipe('handtruck upright',(xx+dx,-.23,.13),(xx+dx,-.23,1.05),.018,steel)
pipe('handtruck handle',(xx-.20,-.23,1.05),(xx+.20,-.23,1.05),.019,black)
box('handtruck parcel',xx-.18,xx+.18,-.56,-.26,.15,.52,card)
route('delivery frontage through',[(-w/2+.5,-1.3,0),(w/2-.5,-1.3,0)])
view('03_deliveries',(-3.5,-5.7,1.65),(.3,-.2,1.0))
# Fuller planting replaces only v36 placeholder leaf boxes, originals archived.
oldleaves=[o for o in list(scene.objects) if o.name.startswith('Street v36 |') and '| leaf cluster' in o.name]
for o in oldleaves:retire(o)
for i,o in enumerate([o for o in scene.objects if o.name.startswith('Street v36 |') and '| planter body' in o.name]):
 current='planting';basis=o.matrix_world.copy();vs=o.data.vertices;cx=(min(v.co.x for v in vs)+max(v.co.x for v in vs))/2;rng=random.Random(3700+i)
 for k in range(28):
  xx=cx+rng.uniform(-.31,.31);yy=rng.uniform(-.57,-.27);zz=rng.uniform(.57,.87);blob('shrub tuft',(xx,yy,zz),(.11,.09,.12),leafm[k%4],rng)
  if k%5==0:blob('flower head',(xx,yy,zz+.10),(.033,.033,.028),flower,rng)
 if i==1:view('04_planting',(cx-2.7,-3.7,1.45),(cx,-.4,.7))
bpy.context.view_layer.update()
(dest/'review-views.json').write_text(json.dumps(views,indent=2));(dest/'local-routes.json').write_text(json.dumps(routes,indent=2))
(dest/'changes.json').write_text(json.dumps(dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),new_solids=[o.name for o in made],archived=retired,labels=labels,engine_implemented=False,scope='F006/native00101 shelter reference; approximate unseen joinery/measurements. Cycles and deliveries are inferred shallow street scenes. All old meshes retained including archived originals.'),indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(out));print('V37_COMPLETE',len(made),len(retired),flush=True)
