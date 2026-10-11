"""Correct corner porch: diagonal middle door, two perpendicular sidelights."""
from pathlib import Path
import bpy,bmesh,json,math,re
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-porch-v49.blend'
OUT=ROOT/'assets/blender/pharmacie-holmdale-corner-porch-v50.blend';assert not OUT.exists()
dest=ROOT/'recon/v50';dest.mkdir(exist_ok=True)
root=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'];source=bpy.data.collections['DETAIL v49 | User-photo porch window and paving']
coll=bpy.data.collections.new('DETAIL v50 | Diagonal central door and porch');bpy.context.scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v50 | Straight-facing porch revision');archive.use_fake_user=True
made=[];retired=[];F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
white=bpy.data.materials['Holmdale v44 | white uPVC'];stone=bpy.data.materials['Holmdale v49 | weathered paving mortar'];cream=bpy.data.materials['Holmdale v44 | cream rough render'];stones=[bpy.data.materials['Holmdale v49 | paving stone '+str(i)] for i in range(5)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('Holmdale v50 | '+name,me);coll.objects.link(ob);ob.parent=root;made.append(ob);return ob
def prism(name,pts,z0,z1,m):
 N=len(pts);return mesh(name,[(x,y,z) for z in (z0,z1) for x,y in pts],[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m)
def panel(name,a,b,z0,z1,m,t=.055):
 a=Vector(a);b=Vector(b);n=Vector(((b-a).y,-(b-a).x)).normalized();return prism(name,[tuple(p) for p in (a-n*t/2,b-n*t/2,b+n*t/2,a+n*t/2)],z0,z1,m)
oldfaces=[((3.08,-.40),(3.58,-.90)),((3.58,-.90),(4.42,-.90)),((4.42,-.90),(4.92,-.40))]
newfaces=[((3.10,.03),(3.10,-.65)),((3.10,-.65),(3.85,-1.40)),((3.85,-1.40),(4.92,-1.40))]
def face_matrix(i):
 a,b=map(Vector,oldfaces[i]);aa,bb=map(Vector,newfaces[i]);u=(b-a).normalized();n=Vector((u.y,-u.x));v=(bb-aa).normalized();nn=Vector((v.y,-v.x));scale=(bb-aa).length/(b-a).length
 old=Matrix(((u.x,n.x,0,a.x),(u.y,n.y,0,a.y),(0,0,1,0),(0,0,0,1)))
 new=Matrix(((v.x*scale,nn.x,0,aa.x),(v.y*scale,nn.y,0,aa.y),(0,0,1,0),(0,0,0,1)))
 return new@old.inverted()
transforms=[face_matrix(i) for i in range(3)]
def clone(ob,matrix=None):
 dup=ob.copy();dup.data=ob.data.copy();dup.name=ob.name.replace('v49','v50');coll.objects.link(dup)
 if matrix is not None:
  # Bake the planar affine map into copied vertices: assigning an object TRS
  # would discard shear when a 45-degree pane also changes width.
  transform=matrix@ob.matrix_basis
  for v in dup.data.vertices:v.co=transform@v.co
  dup.matrix_basis=Matrix.Identity(4);dup.data.update()
 made.append(dup);return dup
for ob in list(source.objects):
 name=ob.name;i=None
 if any(s in name for s in ('porch lower recessed panel','porch obscure pane','porch mitred frame','porch mid rail')):
  match=re.search(r'(?:panel|pane|frame|rail) ([012])',name);i=int(match.group(1))
 elif 'right return transom' in name or 'right return open vent' in name:i=2
 elif any(s in name for s in ('central black letter slot','black lever backplate','black door lever','brass peephole','ornament ribbon','wire flower petal')):i=1
 replace=i is not None or any(s in name for s in ('closed porch backing','porch shallow polygon cap','porch fascia','porch gutter','left porch downpipe','rounded porch landing','wing return pot strip'))
 if replace:
  archive.objects.link(ob);source.objects.unlink(ob);retired.append(ob.name)
  if i is not None:clone(ob,transforms[i])
 elif name=='Holmdale v49 | observed pot 6':
  archive.objects.link(ob);source.objects.unlink(ob);retired.append(ob.name);dup=clone(ob);dup.location.x-=.65;dup.location.y+=.35
 # Basket nearest entrance moves along the blank return, away from central door.
 elif any(s in name for s in ('basket','wicker')) and ob.type=='MESH':
  points=[ob.matrix_basis@v.co for v in ob.data.vertices]
  if sum(p.y for p in points)/len(points)>-1.2:
   archive.objects.link(ob);source.objects.unlink(ob);retired.append(ob.name);dup=clone(ob);dup.location.y-=.52
outline=[(3.10,.03),(3.10,-.65),(3.85,-1.40),(4.92,-1.40),(4.92,.03)]
prism('closed corner porch backing',outline,.035,2.58,white)
prism('corner porch low roof cap',[(x,y-.025) for x,y in outline],2.59,2.69,white)
for i,(a,b) in enumerate(newfaces):
 a=Vector(a);b=Vector(b);n=Vector(((b-a).y,-(b-a).x)).normalized()
 panel('corner fascia '+str(i),a+n*.08,b+n*.08,2.53,2.69,white)
 panel('corner gutter '+str(i),a+n*.14,b+n*.14,2.65,2.73,white)
 # Small corner caps join adjacent gutter segments.
 if i<2:
  p=b+n*.13;prism('gutter corner cap '+str(i),[(p.x-.07,p.y-.07),(p.x+.07,p.y-.07),(p.x+.07,p.y+.07),(p.x-.07,p.y+.07)],2.64,2.74,white)
# Landing is centred on the diagonal door and opens into driveway to southwest.
centre=Vector((3.475,-1.025));u=Vector((math.sqrt(.5),-math.sqrt(.5)));n=Vector((-math.sqrt(.5),-math.sqrt(.5)))
pts=[tuple(centre-u*.66),tuple(centre+u*.66)]+[tuple(centre+u*(.66*math.cos(math.pi*j/16))+n*(.72*math.sin(math.pi*j/16))) for j in range(1,16)]
def paving(name,pts,z):
 prism(name+' backing',pts,-.045,z,stone);c=Vector((sum(x for x,y in pts)/len(pts),sum(y for x,y in pts)/len(pts)))
 for i,(a,b) in enumerate(zip(pts,pts[1:]+pts[:1])):
  a=Vector(a);b=Vector(b);m=(a+b+c)/3;prism(name+' stone', [tuple(m+(v-m)*.96) for v in (c,a,b)],z,z+.012,stones[i%5])
paving('central door rounded walkable landing',pts,.070)
paving('separate raised plant ledge',[(4.08,-1.40),(4.91,-1.40),(4.91,-2.40),(4.08,-2.40)],.13)
# Low threshold strip follows the central diagonal door, not the plant ledge.
panel('central door threshold',newfaces[1][0],newfaces[1][1],.070,.095,white,.12)
bpy.context.view_layer.update();bad=[]
for ob in made:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
root['porch_correction']='v50: diagonal central door connecting perpendicular left/right glazing; door threshold over rounded walkable landing; separate higher plant ledge. Photo 2/8 and Sam correction; dimensions estimated.'
report={'new_meshes':len(made),'archived_unchanged':retired,'old_faces':oldfaces,'corrected_faces':newfaces,'door_midpoint':list(centre),'door_direction_outward':list(n),'landing_height':.082,'plant_ledge_height':.142,'bad_closed_meshes':bad,'limits':['Photo-led topology; exact dimensions not measured','Static closed exterior, not functioning door or interior','Focus restricted to porch; wider extension completion still pending']}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result={k:v for k,v in report.items() if k!='archived_unchanged'}
