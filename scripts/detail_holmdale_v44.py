"""User-identified number 29 photo-led static exterior; no source photo pixels."""
from pathlib import Path
import bpy,bmesh,json,math,random,hashlib,time
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-station-detail-v43.blend'
OUT=ROOT/'assets/blender/pharmacie-holmdale-house-v44.blend';assert not OUT.exists()
dest=ROOT/'recon/v44';dest.mkdir(exist_ok=True)
scene=bpy.context.scene;start=time.monotonic()
# Keep references to objects, avoiding repeated name lookup in the large scene.
original=[(o,o.matrix_basis.copy(),o.data) for o in scene.objects]
d=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
pin=Vector(d['house_pin']);end=Vector(d['holmdale'][-1]);n=(pin-end).normalized();u=Vector((n.y,-n.x));origin=pin-u*5-n*3.5
basis=Matrix(((u.x,n.x,0,origin.x),(u.y,n.y,0,origin.y),(0,0,1,0),(0,0,0,1)))
coll=bpy.data.collections.new('DETAIL v44 | Number 29 photo-led bungalow');scene.collection.children.link(coll)
root=bpy.data.objects.new('Holmdale v44 | Movable number 29 assembly',None);coll.objects.link(root);root.matrix_world=basis
root['evidence']='Sam identified references/29 holmdale.png; facade observed, dimensions/rear footprint estimated'
root['alignment']='House place pin and facing inferred from end of Holmdale; Google overhead check pending'
made=[];rng=random.Random(29)
def mat(name,c,noise=False):
 m=bpy.data.materials.new('Holmdale v44 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.82
 if noise:
  ns=m.node_tree.nodes;ls=m.node_tree.links;tex=ns.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=24;coord=ns.new('ShaderNodeTexCoord');ls.new(coord.outputs['Object'],tex.inputs['Vector']);b=ns.new('ShaderNodeBump');b.inputs['Strength'].default_value=.25;b.inputs['Distance'].default_value=.015;ls.new(tex.outputs['Fac'],b.inputs['Height']);ls.new(b.outputs['Normal'],p.inputs['Normal'])
 return m
cream=mat('cream rough render',(.78,.75,.64),True);white=mat('white uPVC',(.86,.85,.79));glass=mat('grey blue opaque glazing',(.18,.24,.25));curtain=mat('pale curtains',(.62,.64,.55));brick=mat('brown brick',(.31,.20,.13),True);mortar=mat('weathered mortar',(.46,.43,.35));green=mat('dark green garage',(.055,.115,.075));dark=mat('dark lamp and handles',(.035,.04,.035));concrete=mat('concrete steps',(.40,.39,.34),True);drive=mat('brown grey driveway',(.28,.25,.20),True);fence=mat('grey brown timber fence',(.29,.26,.20),True);leaf=mat('hedge green',(.16,.24,.055));leaf2=mat('hedge gold green',(.30,.34,.075));pot=mat('blue glazed pot',(.055,.10,.20));terra=mat('terracotta pot',(.39,.22,.10));tiles=[mat('weathered roof tile '+str(i),(.28+i*.017,.265+i*.014,.20+i*.013),True) for i in range(5)]
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 ob=bpy.data.objects.new('Holmdale v44 | '+name,me);coll.objects.link(ob);ob.parent=root;made.append(ob);return ob
def box(name,x0,x1,y0,y1,z0,z1,m):return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],F,m)
def prism(name,pts,z0,z1,m):
 N=len(pts);return mesh(name,[(x,y,z) for z in (z0,z1) for x,y in pts],[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m)
def tube(name,x,y,z0,z1,r,m):return prism(name,[(x+r*math.cos(j*math.tau/12),y+r*math.sin(j*math.tau/12)) for j in range(12)],z0,z1,m)
def sphere(name,x,y,z,scale,m):
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1);me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free();me.materials.append(m)
 ob=bpy.data.objects.new('Holmdale v44 | '+name,me);coll.objects.link(ob);ob.parent=root;ob.location=(x,y,z);ob.scale=scale;made.append(ob);return ob
def text(name,body,x,y,z,size,m):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.001;cu.materials.append(m);ob=bpy.data.objects.new('Holmdale v44 | '+name,cu);coll.objects.link(ob);ob.parent=root;ob.location=(x,y,z);ob.rotation_euler=(math.pi/2,0,0);made.append(ob)
box('main left closed bungalow shell',0,5.1,0,7.5,-.25,2.8,cream)
box('lower right closed front wing',4.9,10.2,-.12,5.0,-.25,2.58,cream)
box('garage closed shell',10.2,15.2,.05,5.,-.25,2.43,cream)
box('driveway apron',-.7,15.5,-11.9,-.15,-.28,-.045,drive)
for x0,x1,y in ((0,5.1,-.02),(4.9,10.2,-.14)):
 box('brick plinth backing',x0,x1,y-.04,y,.02,.55,mortar)
 for row in range(6):
  x=x0+(0.12 if row%2 else 0)
  while x+.09<x1:
   box('individual plinth brick',x,min(x+.225,x1),y-.065,y-.035,.035+row*.083,.108+row*.083,brick);x+=.24
def framed_panel(name,a,b,z0,z1,cols,lower_white=False):
 # Oriented rectangular panel supports angled bay side glazing.
 a=Vector(a);b=Vector(b);v=(b-a).normalized();normal=Vector((v.y,-v.x));w=(b-a).length
 def strip(label,s0,s1,t0,t1,h0,h1,m):
  pts=[a+v*s+normal*t for s,t in ((s0,t0),(s1,t0),(s1,t1),(s0,t1))];return prism(name+' '+label,[tuple(p) for p in pts],h0,h1,m)
 strip('glazing',0,w,-.015,.015,z0,z1,glass)
 if lower_white:strip('opaque lower skirt',0,w,.016,.04,.15,z0,white)
 for k in range(cols+1):
  s=w*k/cols;strip('vertical frame',max(0,s-.027),min(w,s+.027),.025,.09,z0-.05,z1+.05,white)
 for z in (z0,z1-.45,z1):strip('horizontal frame',0,w,.025,.09,z-.025,z+.025,white)
 strip('projecting sill',-.07,w+.07,.015,.17,z0-.11,z0-.035,white)
 if 'porch' not in name:
  strip('left curtain panel',.025,w*.23,.017,.023,z0+.04,z1-.06,curtain)
  strip('right curtain panel',w*.77,w-.025,.017,.023,z0+.04,z1-.06,curtain)
def bay(name,x0,x1,yback,yfront,z0,z1,whitebase):
 pts=[(x0,yback),(x0+.27,yfront),(x1-.27,yfront),(x1,yback)]
 prism(name+' closed base',pts,.02,z0-.035,white if whitebase else brick)
 framed_panel(name+' left angled pane',pts[0],pts[1],z0,z1,1,whitebase)
 framed_panel(name+' broad front panes',pts[1],pts[2],z0,z1,2 if not whitebase else 3,whitebase)
 framed_panel(name+' right angled pane',pts[2],pts[3],z0,z1,1,whitebase)
 prism(name+' white head',pts,z1,z1+.12,white)
bay('left projecting bay',.7,3.0,-.04,-.47,.64,2.56,False)
bay('right broad bay',5.1,8.8,-.16,-.57,.68,2.38,True)
# White porch: sidelight, obscured-glass door and upper transom.
box('porch white enclosed relief',3.25,4.93,-.30,.03,.02,2.69,white)
framed_panel('porch narrow sidelight',(3.34,-.34),(3.75,-.34),.38,2.22,1)
box('porch door opaque panel',3.85,4.77,-.36,-.31,.18,2.25,white)
box('porch grey upper door glass',3.91,4.71,-.385,-.36,.91,2.17,glass)
box('porch lower door raised panel',3.92,4.70,-.39,-.365,.26,.83,white)
box('porch upper transom glass',3.84,4.79,-.365,-.33,2.33,2.55,glass)
box('porch door handle',3.92,3.95,-.43,-.39,1.00,1.22,dark)
sphere('round door ornament',4.32,-.40,1.60,(.11,.012,.11),white)
# Shallow curved concrete step follows visible porch threshold.
pts=[(3.0,-.27),(5.02,-.27)]+[(4.01+1.05*math.cos(t),-.28-.69*math.sin(t)) for t in [math.pi*j/12 for j in range(13)]]
# Use an unambiguous convex front-facing half ellipse with straight back edge.
pts=[(3.,-.27),(5.06,-.27)]+[(4.03+1.03*math.cos(math.pi*j/12),-.27-.70*math.sin(math.pi*j/12)) for j in range(1,12)]
prism('curved porch step',pts,-.04,.10,concrete)
box('right narrow white door',9.12,9.96,-.20,-.145,.06,2.38,white)
box('right door glazed upper panel',9.24,9.84,-.225,-.20,.65,2.17,glass)
box('right door handle',9.20,9.23,-.26,-.225,1.0,1.20,dark)
box('garage green door',10.42,14.98,-.01,.045,.04,2.25,green)
for k in range(39):box('garage horizontal rib '+str(k),10.42,14.98,-.028,-.01,.07+k*.054,.083+k*.054,green)
for x in (10.32,15.0):box('garage white upright',x,x+.10,-.06,.08,.01,2.42,white)
box('garage white lintel',10.28,15.14,-.06,.08,2.28,2.43,white)
def hip(name,x0,x1,y0,y1,eave,peak):
 xm=(x0+x1)/2;ym=(y0+y1)/2;ridgehalf=max(.1,((x1-x0)-(y1-y0))*.35)
 # Ridge runs along depth for the narrow main wing.
 if y1-y0>x1-x0:
  r0=(xm,y0+(x1-x0)*.43,peak);r1=(xm,y1-(x1-x0)*.43,peak)
  faces=[[(x0,y0,eave),(x1,y0,eave),r0,r0],[(x1,y0,eave),(x1,y1,eave),r1,r0],[(x1,y1,eave),(x0,y1,eave),r1,r1],[(x0,y1,eave),(x0,y0,eave),r0,r1]]
 else:
  r0=(x0+(y1-y0)*.40,ym,peak);r1=(x1-(y1-y0)*.40,ym,peak)
  faces=[[(x0,y0,eave),(x1,y0,eave),r1,r0],[(x1,y0,eave),(x1,y1,eave),r1,r1],[(x1,y1,eave),(x0,y1,eave),r0,r1],[(x0,y1,eave),(x0,y0,eave),r0,r0]]
 vs=[(x0,y0,eave),(x1,y0,eave),(x1,y1,eave),(x0,y1,eave),r0,r1]
 fs=[(3,2,1,0)]
 # Build a closed roof volume with unique coordinate-index lookup.
 lookup={tuple(p):i for i,p in enumerate(vs)}
 for f in faces:
  idx=list(dict.fromkeys(lookup[tuple(p)] for p in f));fs.append(tuple(idx))
 mesh(name+' closed roof',vs,fs,tiles[1])
 for fi,f in enumerate(faces):
  a,b,c,d=map(Vector,f);rows=max(8,math.ceil((eave-peak).__abs__()/.16))
  for row in range(rows):
   t0=row/rows;t1=min((row+.96)/rows,.997);lo=a.lerp(d,t0);ro=b.lerp(c,t0);hi=a.lerp(d,t1);ri=b.lerp(c,t1);count=max(1,math.ceil((ro-lo).length/.34))
   for col in range(count):
    s0=col/count;s1=(col+.97)/count;quad=[lo.lerp(ro,s0),lo.lerp(ro,s1),hi.lerp(ri,s1),hi.lerp(ri,s0)]
    # Tiny apex tiles are omitted; the closed base roof remains beneath them.
    if (quad[1]-quad[0]).cross(quad[3]-quad[0]).length<1e-6:continue
    verts=[tuple(v+Vector((0,0,z))) for z in (.012,.035) for v in quad]
    mesh(name+' individual tile',verts,F,rng.choice(tiles))
hip('main high hipped roof',-.24,5.3,-.25,7.75,2.81,4.54)
hip('lower right hipped roof',4.72,10.43,-.38,5.24,2.60,3.98)
# Garage lean roof, tiled shallow slope.
for row in range(13):
 y0=-.15+row*.40;y1=y0+.39;z0=2.47+(y0+.15)*.055;z1=2.47+(y1+.15)*.055
 for col in range(16):
  x0=10.21+col*.325;x1=x0+.315
  mesh('garage shallow roof tile',[(x0,y0,z0),(x1,y0,z0),(x1,y1,z1),(x0,y1,z1),(x0,y0,z0+.035),(x1,y0,z0+.035),(x1,y1,z1+.035),(x0,y1,z1+.035)],F,rng.choice(tiles))
box('garage closed roof backing',10.18,15.45,-.15,5.1,2.43,2.47,tiles[1])
for x0,x1,y,z in ((-.26,5.3,-.26,2.78),(4.72,10.43,-.39,2.57),(10.18,15.45,-.16,2.43)):
 box('white fascia',x0,x1,y-.045,y+.045,z-.10,z+.045,white)
 box('white front gutter',x0,x1,y-.10,y-.045,z-.02,z+.04,white)
for x,y,z in ((.10,-.08,2.8),(5.0,-.24,2.58),(10.1,-.19,2.58),(15.25,-.03,2.43)):
 box('downpipe',x-.025,x+.025,y-.035,y+.035,.10,z,white)
 for h in (.7,1.7):box('downpipe collar',x-.04,x+.04,y-.05,y+.05,h,h+.06,white)
for x in (4.94,10.03,15.18):
 box('facade lantern bracket',x-.035,x+.035,-.25,-.05,2.17,2.30,dark)
 box('facade lantern case',x-.07,x+.07,-.32,-.20,2.00,2.26,dark)
 box('facade lantern pale lens',x-.047,x+.047,-.325,-.318,2.04,2.21,white)
box('small number plaque',.27,.47,-.08,-.04,1.95,2.10,dark);text('number 29','29',.37,-.085,2.025,.105,white)
# Three diamond decorations beside the left bay.
for x,z in ((.20,1.62),(.43,1.40),(.62,1.64)):
 ob=box('diamond wall decoration',-.075,.075,-.025,.025,-.075,.075,grey if 'grey' in globals() else concrete);ob.location=(x,-.08,z);ob.rotation_euler.y=math.pi/4
for j,(x,y) in enumerate(((3.12,-.68),(4.82,-.67),(3.0,-.81))):
 tube('porch plant pot '+str(j),x,y,.02,.26,.14,pot if j%2 else terra)
 sphere('pot plant '+str(j),x,y,.30,(.13,.13,.14),leaf)
# Photo-observed left hedge/tree and right brick/timber boundary.
box('left hedge earth bed',-1.1,-.72,-10.9,5.2,-.2,.03,brick)
for j in range(24):
 y=-10.6+j*.65;sphere('left hedge foliage',-.99+rng.uniform(-.12,.12),y,.55+rng.uniform(-.06,.10),(.42,.5,.62),leaf2 if j<10 else leaf)
tube('left front tree trunk',-.83,.0,.02,3.8,.11,brick)
for j in range(16):sphere('left tree foliage',-.9+rng.uniform(-.7,.7),rng.uniform(-.8,.8),2.8+rng.uniform(-.35,.7),(.66,.63,.75),leaf)
box('right boundary masonry',15.5,15.72,-10.7,4.9,-.3,.66,brick)
for j in range(46):
 y=-10.7+j*.34;box('right timber fence board',15.53,15.62,y,y+.323,.66,2.05,fence)
for y in (-10.7,-8.1,-5.5,-2.9,-.3,2.3,4.8):box('right fence post',15.49,15.72,y-.06,y+.06,.60,2.13,concrete)
archive=bpy.data.collections.new('ARCHIVE v44 | Fence pieces beyond pavement setback');archive.use_fake_user=True
for ob in made:
 if ob.type!='MESH' or not any(s in ob.name for s in ('right boundary masonry','right timber fence board','right fence post')):continue
 if max(v.co.y for v in ob.data.vertices)<=-7.5:
  archive.objects.link(ob);coll.objects.unlink(ob)
 else:
  for v in ob.data.vertices:v.co.y=max(v.co.y,-7.5)
  ob.data.update()
bpy.context.view_layer.update()
for ob,matrix,data in original:
 current=ob.matrix_basis.copy();assert ob.data==data and max(abs(current[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5,ob.name
bad=[]
for ob in made:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
report={'source':'assets/blender/pharmacie-station-detail-v43.blend','output':str(OUT.relative_to(ROOT)),'new_meshes':sum(o.type=='MESH' for o in made),'new_text_objects':sum(o.type=='FONT' for o in made),'parent_objects_preserved':len(original),'nonmanifold_or_nonpositive':bad,'assembly_root':root.name,'source_photo':'references/29 holmdale.png','source_sha256':hashlib.sha256((ROOT/'references/29 holmdale.png').read_bytes()).hexdigest(),'seconds':time.monotonic()-start,'limits':['Facade based on user-identified collage; Google source photo pixels not embedded.','Dimensions, rear footprint and placement are estimated; overhead comparison pending.','Static closed exterior; no accessible interior or BO3 behavior.','Road-end widening and house approach verification still pending.']}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
