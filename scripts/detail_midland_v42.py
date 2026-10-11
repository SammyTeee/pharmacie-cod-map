"""Photo-led Midland frontage assembly, movable independently of provisional roads.

Observed: blue/white facade, four upper sash windows, two broad lower windows,
two entry bays, hipped slate roof/chimneys, deck/rail/picnic tables/umbrella.
Dimensions and rear shape/height are estimated. No photo textures or interiors.
"""
from pathlib import Path
import bpy,bmesh,json,math,random,hashlib
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-extension-route-v41.blend'
OUT=ROOT/'assets/blender/pharmacie-midland-frontage-v42.blend';assert not OUT.exists()
dest=ROOT/'recon/v42';dest.mkdir(exist_ok=True)
scene=bpy.context.scene
original={o.name:(o.matrix_basis.copy(),o.data) for o in scene.objects}
coll=bpy.data.collections.new('DETAIL v42 | Midland photo-led exterior');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v42 | Provisional Midland footprint mass');archive.use_fake_user=True
old=bpy.data.objects['Extension v41 | OSM footprint 173168754'];archive.objects.link(old)
for c in list(old.users_collection):
 if c!=archive:c.objects.unlink(old)
route=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
poly=next(w['points'][:-1] for w in route['ways'] if w['id']=='173168754');a=Vector(poly[0]);u=(Vector(poly[1])-a).normalized();n=Vector((-u.y,u.x));W=(Vector(poly[1])-a).length
basis=Matrix(((u.x,n.x,0,a.x),(u.y,n.y,0,a.y),(0,0,1,0),(0,0,0,1)))
root=bpy.data.objects.new('Midland v42 | Movable reference assembly',None);coll.objects.link(root);root.matrix_world=basis
root['evidence']='Official exterior image linked in reference manifest; OSM footprint association provisional';root['status']='Blender static exterior; road alignment awaits Google satellite comparison'
made=[]
def material(name,c,noise=False):
 m=bpy.data.materials.new('Midland v42 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.8
 if noise:
  ns=m.node_tree.nodes;ls=m.node_tree.links;t=ns.new('ShaderNodeTexCoord');tex=ns.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=18;tex.inputs['Detail'].default_value=3;ls.new(t.outputs['Object'],tex.inputs['Vector']);b=ns.new('ShaderNodeBump');b.inputs['Strength'].default_value=.35;b.inputs['Distance'].default_value=.018;ls.new(tex.outputs['Fac'],b.inputs['Height']);ls.new(b.outputs['Normal'],p.inputs['Normal'])
 return m
blue=material('rough blue painted masonry',(.065,.13,.18),True);white=material('white render',(.77,.76,.69),True);joinery=material('off-white sash joinery',(.80,.80,.73));glass=material('opaque grey-blue window proxy',(.14,.20,.23));dark=material('black painted iron',(.025,.033,.035));wood=material('weathered deck timber',(.21,.16,.085),True);pale=material('picnic timber',(.46,.33,.15));cloth=material('navy umbrella fabric',(.045,.075,.21));pot=material('terracotta pots',(.36,.17,.065));leaf=material('basket greenery',(.08,.19,.045));yellow=material('small yellow flowers',(.68,.48,.075));slate=bpy.data.materials['Street v17 | slate'];brick=bpy.data.materials['Shop v19 | brick relief']
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new('Midland v42 | '+name,me);coll.objects.link(o);o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4);o['engine_implemented']=False;made.append(o);return o
def box(name,x0,x1,y0,y1,z0,z1,m):return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],F,m)
def prism(name,pts,z0,z1,m):
 N=len(pts);return mesh(name,[(x,y,z) for z in (z0,z1) for x,y in pts],[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m)
def tube(name,x,y,z0,z1,r,m,count=12):
 pts=[(x+r*math.cos(j*2*math.pi/count),y+r*math.sin(j*2*math.pi/count)) for j in range(count)];return prism(name,pts,z0,z1,m)
def text(name,body,x,y,z,size,m,width):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.003;cu.materials.append(m);o=bpy.data.objects.new('Midland v42 | '+name,cu);coll.objects.link(o);o.parent=root;o.location=(x,y,z);o.rotation_euler=(math.pi/2,0,0);made.append(o);bpy.context.view_layer.update();bounds=[v[0] for v in o.bound_box];actual=max(bounds)-min(bounds)
 if actual>width:o.scale*=width/actual
 return o
local=[((Vector(p)-a).dot(u),(Vector(p)-a).dot(n)) for p in poly]
prism('mapped lower footprint blue render',local,-.3,3.35,blue)
prism('estimated two-storey front wing',[(0,0),(W,0),(17.59,10.27),(-.84,9.84)],3.35,6.6,white)
prism('photo blue upper side flank',[(-.08,-.01),(-.03,-.01),(-.87,9.85),(-.92,9.85)],3.35,6.6,blue)
box('front fascia',-.10,W+.15,-.18,-.025,3.13,3.68,blue)
box('fascia top moulding',-.15,W+.2,-.23,-.03,3.65,3.73,blue)
box('fascia lower moulding',-.10,W+.15,-.22,-.035,3.10,3.17,blue)
text('main fascia lettering','THE MIDLAND RAILWAY',9.4,-.242,3.42,.42,joinery,7.3)
text('small offerings fascia','FOOD · SPORT · FUNCTIONS · ENTERTAINMENT',14.7,-.245,3.42,.15,joinery,3.6)
text('upper M emblem','M',5.7,-.055,4.65,.9,blue,1.1)
for i in range(18):
 angle=math.radians(30+i*17.65);x=5.7+.72*math.sin(angle);z=4.65+.77*math.cos(angle)
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=1,radius=1);me=bpy.data.meshes.new('emblem wreath leaf');bm.to_mesh(me);bm.free();me.materials.append(blue)
 ob=bpy.data.objects.new('Midland v42 | Emblem wreath leaf '+str(i),me);coll.objects.link(ob);ob.parent=root;ob.location=(x,-.065,z);ob.scale=(.07,.018,.15);ob.rotation_euler.y=angle;made.append(ob)
side=text('side painted pub title','THE\nMIDLAND\nRAILWAY',0,0,0,.42,joinery,4.5);side.location=(-.49,5,4.55);side.rotation_euler=(math.pi/2,0,math.radians(-85.12))
def window(name,x,z,w,h,cols=3):
 box(name+' glazing',x-w/2,x+w/2,-.12,-.015,z,z+h,glass)
 # Curtains are shallow proxies behind joinery, not photographic image panels.
 for j in range(8):
  xx=x-w/2+.08+j*(w-.16)/8
  box(name+' curtain fold '+str(j),xx,xx+.025,-.126,-.12,z+.06,z+h-.06,white)
 for xx in (x-w/2,x+w/2):box(name+' jamb',xx-.045,xx+.045,-.18,-.05,z-.05,z+h+.05,joinery)
 for zz in (z,z+h*.48,z+h):box(name+' rail',x-w/2,x+w/2,-.185,-.055,zz-.035,zz+.035,joinery)
 for j in range(1,cols):
  xx=x-w/2+w*j/cols;box(name+' mullion '+str(j),xx-.025,xx+.025,-.18,-.06,z,z+h,joinery)
 box(name+' projecting sill',x-w/2-.12,x+w/2+.12,-.25,.025,z-.13,z-.045,joinery)
for i,x in enumerate((3.15,8.65,11.8,14.85)):window('upper sash '+str(i),x,4.0,1.35,1.9,3)
for i,x in enumerate((1.05,4.75)):window('lower narrow sash '+str(i),x,.91,1.05,1.65,3)
for i,x in enumerate((8.45,14.55)):window('lower broad sash '+str(i),x,.72,2.8,2.1,6)
for i,x in enumerate((2.8,11.7)):
 box('static entry door '+str(i),x-.52,x+.52,-.12,-.02,.20,2.85,dark)
 box('entry glazed upper panel '+str(i),x-.43,x+.43,-.14,-.12,1.0,2.64,glass)
 for xx in (x-.58,x+.58):box('entry white surround '+str(i),xx-.06,xx+.06,-.23,-.04,.12,2.92,joinery)
 box('entry lintel '+str(i),x-.64,x+.64,-.23,-.04,2.86,2.98,joinery)
 box('entry threshold '+str(i),x-.67,x+.67,-.39,-.04,.05,.20,wood)
 box('door handle '+str(i),x+.33,x+.36,-.21,-.17,.95,1.28,joinery)
 box('small framed door notice '+str(i),x-.34,x+.24,-.17,-.145,1.12,1.69,blue)
text('entry glass welcome','WELCOME',11.7,-.18,2.35,.18,joinery,.9)
for i,x in enumerate((6.1,16.35)):
 box('beer garden plaque '+str(i),x-.42,x+.42,-.18,-.05,.96,2.0,blue)
 for j,line in enumerate(('LARGE','BEER','GARDEN','TO REAR')):text('garden plaque text '+str(i)+' '+str(j),line,x,-.20,1.83-j*.22,.13,joinery,.72)
# Closed roof volume follows the photographed hipped front wing.
roof=[(-.4,-.4,6.55),(W+.4,-.4,6.55),(18.0,10.6,6.55),(-1.2,10.2,6.55),(1.45,4.9,8.12),(15.1,4.9,8.12)]
mesh('hipped slate front roof',roof,[(3,2,1,0),(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],slate)
box('front dark gutter',-.43,W+.43,-.45,-.28,6.48,6.62,dark)
for x in (.13,W-.15):
 box('front downpipe',x-.035,x+.035,-.19,-.115,.2,6.48,dark)
 for z in (1.1,2.5,4.0,5.7):box('pipe collar',x-.05,x+.05,-.21,-.11,z,z+.06,dark)
for idx,(x,y) in enumerate(((3.3,4.9),(14.9,5.4))):
 box('brick chimney '+str(idx),x-.55,x+.55,y-.35,y+.35,7.6,9.1 if idx==0 else 8.65,brick)
 top=9.1 if idx==0 else 8.65
 box('chimney stone cap '+str(idx),x-.61,x+.61,y-.41,y+.41,top,top+.13,white)
 for j in range(3 if idx==0 else 2):tube('terracotta chimney pot '+str(idx)+' '+str(j),x-.34+j*.34,y,top+.13,top+.65,.115,pot)
# Deck furniture stays in the frontage setback, clear of the road/footway.
box('raised frontage deck',-.05,W+.15,-2.2,-.18,-.1,.18,wood)
for j in range(22):box('deck plank seam '+str(j),-.02,W+.12,-2.17+j*.09,-2.16+j*.09,.18,.185,dark)
for left,right in ((.1,2.05),(3.55,10.85),(12.5,W)):
 box('front deck handrail',left,right,-2.2,-2.11,1.05,1.12,dark)
 box('front deck bottom rail',left,right,-2.19,-2.12,.3,.36,dark)
 for j in range(math.ceil((right-left)/.25)+1):
  x=left+(right-left)*j/math.ceil((right-left)/.25);box('front rail spindle',x-.018,x+.018,-2.18,-2.14,.36,1.05,dark)
 for x in (left,right):box('front deck rail post',x-.045,x+.045,-2.22,-2.09,.15,1.18,dark)
for idx,x in enumerate((.9,5.9,9.0,14.3)):
 box('picnic table top '+str(idx),x-.75,x+.75,-1.60,-.92,.83,.90,pale)
 for yy in (-1.88,-.65):box('picnic bench '+str(idx),x-.85,x+.85,yy-.12,yy+.12,.51,.57,pale)
 for xx in (x-.54,x+.54):
  for yy in (-1.62,-.92):box('picnic table leg '+str(idx),xx-.045,xx+.045,yy-.04,yy+.04,.18,.83,pale)
  box('picnic bench bearer '+str(idx),xx-.05,xx+.05,-2.0,-.5,.38,.45,pale)
# Umbrella with a thick closed faceted fabric canopy and radial timber struts.
tube('umbrella pole',2.8,-1.22,.18,3.55,.045,pale)
N=8;vs=[(2.8+2.6*math.cos(i*2*math.pi/N),-1.22+1.28*math.sin(i*2*math.pi/N),2.7) for i in range(N)]+[(2.8,-1.22,3.5)]
vs += [(x,y,z-.04) for x,y,z in vs]
fs=[]
for i in range(N):
 j=(i+1)%N;fs.extend([(i,j,N),(i+N+1,2*N+1,j+N+1),(i,i+N+1,j+N+1,j)])
mesh('octagonal navy umbrella canopy',vs,fs,cloth)
# Hanging baskets and small practical facade lamps.
rng=random.Random(42)
for idx,x in enumerate((.55,5.75,10.8,13.0,16.5)):
 tube('hanging basket '+str(idx),x,-.36,2.6,2.9,.22,pot)
 box('basket mounting bracket '+str(idx),x-.018,x+.018,-.45,-.04,2.92,3.24,dark)
 for j in range(10):
  bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=1,radius=rng.uniform(.08,.16));me=bpy.data.meshes.new('basket foliage');bm.to_mesh(me);bm.free();me.materials.append(leaf if j<8 else yellow)
  o=bpy.data.objects.new('Midland v42 | Basket foliage '+str(idx)+' '+str(j),me);coll.objects.link(o);o.parent=root;o.location=(x+rng.uniform(-.21,.21),-.36+rng.uniform(-.17,.17),rng.uniform(2.85,3.12));made.append(o)
for idx,x in enumerate((1.,6.9,10.4,15.7)):
 box('small fascia lamp bracket '+str(idx),x-.08,x+.08,-.28,-.06,6.1,6.18,dark)
 box('small fascia lamp '+str(idx),x-.13,x+.13,-.36,-.20,6.02,6.10,dark)
# Keep lower/rear roof surfaces closed without asserting unseen details.
prism('provisional flat rear service roof',local,3.35,3.48,slate)
bpy.context.view_layer.update()
assert all(bpy.data.objects[name].data==data and max(abs(bpy.data.objects[name].matrix_basis[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5 for name,(matrix,data) in original.items())
bad=[]
for o in made:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free()
assert not bad,bad
photo=ROOT/'references/streetview-capture/extension-v41/midland-official-exterior.jpg'
report={'source':'assets/blender/pharmacie-extension-route-v41.blend','output':str(OUT.relative_to(ROOT)),'assembly_root':root.name,'front_width_estimate':W,'new_meshes':sum(o.type=='MESH' for o in made),'new_text_objects':sum(o.type=='FONT' for o in made),'parent_objects_preserved':len(original),'archived_unchanged':[old.name],'source_photo_sha256':hashlib.sha256(photo.read_bytes()).hexdigest(),'nonmanifold_or_nonpositive':bad,'limits':['Google satellite/frame verification pending.','OSM footprint association provisional.','Facade is surface relief on closed static shell, not accessible interior.','Heights/depths/setbacks/rear service wing are estimates.','Photo capture date and current appearance unverified.','No photo pixels baked into geometry.','No BO3 implementation.']}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
