"""Rebuild observed porch and flat wing window from Sam's 19 close photos."""
from pathlib import Path
import bpy,bmesh,json,math,random
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-garage-v48.blend'
OUT=ROOT/'assets/blender/pharmacie-holmdale-porch-v49.blend';assert not OUT.exists()
dest=ROOT/'recon/v49';dest.mkdir(exist_ok=True)
scene=bpy.context.scene;root=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'];old=bpy.data.collections['DETAIL v44 | Number 29 photo-led bungalow']
archive=bpy.data.collections.new('ARCHIVE v49 | Flat porch and incorrect right bay');archive.use_fake_user=True;retired=[]
for ob in list(old.objects):
 if any(s in ob.name for s in ('porch','round door ornament','right broad bay','diamond wall decoration')):
  archive.objects.link(ob);old.objects.unlink(ob);retired.append(ob.name)
coll=bpy.data.collections.new('DETAIL v49 | User-photo porch window and paving');scene.collection.children.link(coll);made=[]
def mat(name,c):
 m=bpy.data.materials.new('Holmdale v49 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.75;return m
white=bpy.data.materials['Holmdale v44 | white uPVC'];brick=bpy.data.materials['Holmdale v44 | brown brick'];dark=bpy.data.materials['Holmdale v44 | dark lamp and handles'];cream=bpy.data.materials['Holmdale v44 | cream rough render'];terra=bpy.data.materials['Holmdale v44 | terracotta pot'];blue=bpy.data.materials['Holmdale v44 | blue glazed pot'];green=bpy.data.materials['Holmdale v44 | hedge green']
glass=mat('obscure glass',(.17,.23,.23));clear=mat('dark window glass',(.12,.17,.18));curtain=mat('cream yellow curtains',(.65,.59,.39));stone=mat('weathered paving mortar',(.34,.31,.23));wicker=mat('dark woven wicker',(.19,.12,.075));metal=mat('galvanized grey',(.38,.42,.41));black=mat('black handle and slot',(.025,.027,.025));gold=mat('peephole brass',(.47,.35,.12));colours=[mat('flower '+str(i),c) for i,c in enumerate(((.8,.18,.3),(.9,.65,.07),(.08,.39,.15),(.2,.35,.65)))];stones=[mat('paving stone '+str(i),(.39+i*.018,.34+i*.015,.24+i*.012)) for i in range(5)]
# Vertical texture in obscure glass; geometry stays closed behind it.
ns=glass.node_tree.nodes;ls=glass.node_tree.links;t=ns.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=45;c=ns.new('ShaderNodeTexCoord');mapping=ns.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(7,7,.35);ls.new(c.outputs['Generated'],mapping.inputs[0]);ls.new(mapping.outputs[0],t.inputs['Vector']);b=ns.new('ShaderNodeBump');b.inputs['Strength'].default_value=.3;b.inputs['Distance'].default_value=.012;ls.new(t.outputs['Fac'],b.inputs['Height']);ls.new(b.outputs[0],ns['Principled BSDF'].inputs['Normal'])
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('Holmdale v49 | '+name,me);coll.objects.link(ob);ob.parent=root;made.append(ob);return ob
def box(name,x0,x1,y0,y1,z0,z1,m):return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],F,m)
def prism(name,pts,z0,z1,m):
 N=len(pts);return mesh(name,[(x,y,z) for z in (z0,z1) for x,y in pts],[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m)
def rod(name,a,b,r,m,sides=8):
 a=Vector(a);b=Vector(b);u=(b-a).normalized();v=u.cross(Vector((0,0,1)))
 if v.length<.01:v=u.cross(Vector((1,0,0)))
 v.normalize();w=u.cross(v);vs=[tuple(p+r*(v*math.cos(i*math.tau/sides)+w*math.sin(i*math.tau/sides))) for p in (a,b) for i in range(sides)];return mesh(name,vs,[tuple(reversed(range(sides))),tuple(range(sides,2*sides))]+[(i,(i+1)%sides,(i+1)%sides+sides,i+sides) for i in range(sides)],m)
def panel(name,a,b,z0,z1,m,t=.045):
 a=Vector(a);b=Vector(b);n=Vector(((b-a).y,-(b-a).x)).normalized();return prism(name,[tuple(p) for p in (a-n*t/2,b-n*t/2,b+n*t/2,a+n*t/2)],z0,z1,m)
def frame(name,a,b,z0,z1,m):
 a=Vector(a);b=Vector(b);u=(b-a).normalized();panel(name+' bottom',a,b,z0,z0+.055,m);panel(name+' head',a,b,z1-.055,z1,m);panel(name+' left',a,a+u*.055,z0,z1,m);panel(name+' right',b-u*.055,b,z0,z1,m)
# Three exposed porch faces: left return, central door, right return.
outline=[(3.08,.03),(3.08,-.40),(3.58,-.90),(4.42,-.90),(4.92,-.40),(4.92,.03)]
prism('closed porch backing',outline,.03,2.58,white)
faces=[((3.08,-.40),(3.58,-.90)),((3.58,-.90),(4.42,-.90)),((4.42,-.90),(4.92,-.40))]
for i,(a,b) in enumerate(faces):
 a=Vector(a);b=Vector(b);n=Vector(((b-a).y,-(b-a).x)).normalized();aa=a+n*.035;bb=b+n*.035
 panel('porch lower recessed panel '+str(i),aa,bb,.12,.92,white)
 panel('porch obscure pane '+str(i),aa+n*.016,bb+n*.016,.99,2.46,glass)
 frame('porch mitred frame '+str(i),aa+n*.045,bb+n*.045,.08,2.52,white)
 panel('porch mid rail '+str(i),aa+n*.045,bb+n*.045,.91,1.00,white)
 if i==2:
  panel('right return transom',aa+n*.05,bb+n*.05,2.08,2.14,white)
  vent=panel('right return open vent',aa+n*.07,bb+n*.07,2.15,2.46,glass)
  # A subtle tilted glazing face, retaining a solid closed pane beneath.
  for v in vent.data.vertices:v.co+=Vector((n.x,n.y,0))*.09*(2.46-v.co.z)/.31
box('central black letter slot',3.70,4.28,-.999,-.967,.91,1.005,black)
box('black lever backplate',3.66,3.70,-1.015,-.975,1.07,1.35,black)
rod('black door lever',(3.68,-1.04,1.20),(3.84,-1.04,1.20),.018,black)
rod('brass peephole',(4,-.978,2.13),(4,-1.004,2.13),.025,gold,12)
# Flower hanging ornament, recognizable colour layout, not a copied photo texture.
rod('ornament ribbon',(4,-1.01,2.03),(4,-1.01,1.85),.007,colours[0])
for j in range(6):
 angle=j*math.tau/6;cx=4+.09*math.cos(angle);cz=1.70+.09*math.sin(angle)
 for k in range(10):
  t=k*math.tau/10;s=(k+1)*math.tau/10;rod('wire flower petal',(cx+.07*math.cos(t),-1.014,cz+.07*math.sin(t)),(cx+.07*math.cos(s),-1.014,cz+.07*math.sin(s)),.004,colours[j%4])
prism('porch shallow polygon cap',[(x+(-.07 if x<4 else .07),y-.07) for x,y in outline],2.59,2.70,white)
for i,(a,b) in enumerate(faces):
 a=Vector(a);b=Vector(b);n=Vector(((b-a).y,-(b-a).x)).normalized();panel('porch fascia '+str(i),a+n*.08,b+n*.08,2.53,2.69,white);panel('porch gutter '+str(i),a+n*.14,b+n*.14,2.65,2.73,white)
rod('left porch downpipe',(3.08,-.45,.12),(3.08,-.45,2.56),.032,white)
# Flat right window. Its outer wall is Y=-2.37; no angled bay returns.
y=-2.415
box('flat wing white lower skirt',5.10,8.8,y-.035,y,.10,.73,white)
for i in range(29):box('lower cladding groove',5.11+i*.128,5.116+i*.128,y-.041,y-.036,.12,.72,stone)
for j,(a,b) in enumerate(((5.1,6.5),(6.5,7.4),(7.4,8.8))):
 panel('flat lower glazing '+str(j),(a,y-.02),(b,y-.02),.75,1.96,clear)
 panel('flat upper glazing '+str(j),(a,y-.02),(b,y-.02),2.01,2.40,clear)
 frame('flat lower frame '+str(j),(a,y-.06),(b,y-.06),.73,1.99,white);frame('flat upper frame '+str(j),(a,y-.06),(b,y-.06),1.96,2.44,white)
 for k in range(8):
  xx=a+.06+(b-a-.12)*k/8;box('curtain folded panel',xx,xx+(b-a-.12)/8*.92,y-.045,y-.035,.80,2.35,curtain)
vent=panel('central top-hung vent',(6.57,y-.10),(7.33,y-.10),2.05,2.37,clear)
for v in vent.data.vertices:v.co.y-=.13*(2.37-v.co.z)/.32
frame('central vent sash',(6.53,y-.10),(7.37,y-.10),2.01,2.41,white)
box('projecting flat window sill',5.02,8.88,y-.14,y+.04,.69,.75,white)
# Paving aprons: individually closed base and inset irregular stone fan pieces.
def paving(name,pts,z):
 prism(name+' mortar backing',pts,-.045,z,stone);centre=Vector((sum(x for x,y in pts)/len(pts),sum(y for x,y in pts)/len(pts)))
 for i,(a,b) in enumerate(zip(pts,pts[1:]+pts[:1])):
  a=Vector(a);b=Vector(b);mid=(a+b+centre)/3
  tri=[tuple(mid+(v-mid)*.96) for v in (centre,a,b)];prism(name+' irregular slab',tri,z,z+.012,stones[i%5])
paving('left bay raised apron',[(-.12,0),(3.13,0),(3.13,-.72),(2.70,-.88),(.40,-.88),(-.05,-.62)],.13)
paving('rounded porch landing',[(3.12,-.58),(4.92,-.58),(4.90,-1.18),(4.65,-1.42),(4.0,-1.56),(3.38,-1.42),(3.12,-1.18)],.055)
paving('wing return pot strip',[(4.30,-.43),(4.91,-.43),(4.91,-2.40),(4.30,-2.40)],.13)
paving('rounded flat wing front apron',[(4.93,-2.36),(9.98,-2.36),(9.98,-2.83),(9.62,-3.13),(5.35,-3.13),(4.93,-2.83)],.10)
def pot(name,x,y,z,r,h,m):
 sides=12;vs=[]
 for rr,zz in ((r*.72,z),(r,z+h),(r*.85,z+h),(r*.61,z+.045)):
  vs.extend((x+rr*math.cos(i*math.tau/sides),y+rr*math.sin(i*math.tau/sides),zz) for i in range(sides))
 fs=[]
 for row,nxt in ((0,1),(1,2),(2,3),(3,0)):
  fs.extend((row*sides+i,row*sides+(i+1)%sides,nxt*sides+(i+1)%sides,nxt*sides+i) for i in range(sides))
 mesh(name,vs,fs,m)
for i,(x,y,r,h,m) in enumerate(((.25,-.65,.18,.25,terra),(.65,-.65,.09,.15,white),(.91,-.65,.09,.15,white),(1.16,-.65,.08,.14,white),(2.80,-.62,.15,.21,terra),(3.02,-.57,.16,.34,metal),(3.35,-.65,.20,.28,terra),(4.48,-1.38,.19,.23,terra),(4.54,-1.72,.21,.30,blue),(4.55,-2.10,.23,.27,terra))):pot('observed pot '+str(i),x,y,.15,r,h,m)
rod('bare potted tree trunk',(3.02,-.57,.43),(3.02,-.57,1.82),.012,metal)
for i in range(9):
 z=.65+i*.13;side=(-1)**i;rod('bare tree branch',(3.02,-.57,z),(3.02+side*(.32-i*.02),-.57,z+.15),.006,metal)
# Wicker cones: separate circular strands and sloping ribs, three chains each.
for j,yy in enumerate((-.72,-1.80)):
 cx=4.36;cz=1.69
 rod('basket wall plate',(4.86,yy,2.10),(4.86,yy,2.48),.016,black)
 rod('basket bracket horizontal',(4.86,yy,2.43),(4.31,yy,2.43),.012,black)
 rod('basket bracket diagonal',(4.86,yy,2.12),(4.31,yy,2.43),.010,black)
 for row in range(11):
  z=cz-.36+row*.034;r=.025+row*.020
  for k in range(16):
   a=k*math.tau/16;b=(k+1)*math.tau/16;rod('wicker cone weave',(cx+r*math.cos(a),yy+r*math.sin(a),z),(cx+r*math.cos(b),yy+r*math.sin(b),z),.009,wicker)
 for k in range(3):
  a=k*math.tau/3;rod('basket suspension chain',(cx+.225*math.cos(a),yy+.225*math.sin(a),cz),(4.31,yy,2.43),.006,metal)
# Three dimensional galvanized wall pockets replace the old flat diamonds.
for j,(x,z) in enumerate(((.20,1.62),(.43,1.40),(.67,1.64))):
 mesh('tapered wall planter',[(x-.095,-.075,z+.10),(x+.095,-.075,z+.10),(x,-.075,z-.15),(x-.09,-.17,z+.08),(x+.09,-.17,z+.08),(x,-.10,z-.13)],[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],metal)
# Rectangular service cover lies on the drive outside perpendicular garage.
box('rusty service cover',8.85,9.42,-3.40,-2.86,-.052,-.035,brick)
for ob in made:
 if 'flat wing white lower skirt' in ob.name or 'lower cladding groove' in ob.name:ob.location.y-=.075
 if 'central black letter slot' in ob.name:ob.location.y-=.055
 if ob.name in ['Holmdale v49 | observed pot '+str(i) for i in (7,8,9)]:
  xs=[v.co.x for v in ob.data.vertices];ys=[v.co.y for v in ob.data.vertices];cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2
  for v in ob.data.vertices:v.co.x=cx+(v.co.x-cx)*.70;v.co.y=cy+(v.co.y-cy)*.70
  ob.location.x+=.20
 if ob.name=='Holmdale v49 | observed pot 6':ob.location.x-=.30;ob.location.y-=.20
bpy.context.view_layer.update();bad=[]
for ob in made:
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
report={'source':'pharmacie-holmdale-garage-v48.blend','new_closed_meshes':len(made),'archived_unchanged':retired,'nonmanifold_or_nonpositive':bad,'observed_corrections':['Three-face porch with central door and angled side glazing','Flat right-wing window and grooved lower skirt','Separate rounded paving aprons','Pots bare tree wicker baskets and galvanized wall pockets'],'limits':['Dimensions and return angles estimated from photos','Static closed exterior only; no interior or working door','Remaining roof boundaries landscaping and placement require refinement','No BO3 changes']}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result={k:v for k,v in report.items() if k!='archived_unchanged'}
