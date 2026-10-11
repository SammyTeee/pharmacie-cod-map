"""Conservative station platform detail; provisional positions, no road edits."""
from pathlib import Path
import bpy,bmesh,json,math
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-midland-frontage-v42.blend'
OUT=ROOT/'assets/blender/pharmacie-station-detail-v43.blend'
assert not OUT.exists()
dest=ROOT/'recon/v43';dest.mkdir(exist_ok=True)
scene=bpy.context.scene
original={o.name:(o.matrix_basis.copy(),o.data) for o in scene.objects}
ref=json.loads((dest/'station-reference.json').read_text())
platform=next(w for w in ref['mapped_ways'] if w['osm_way']=='309564449')['points']
a=Vector(platform[0]);u=(Vector(platform[2])-a).normalized();n=Vector((-u.y,u.x))
# x along the mapped railward edge, y towards platform rear/car park.
basis=Matrix(((u.x,n.x,0,a.x),(u.y,n.y,0,a.y),(0,0,1,0),(0,0,0,1)))
coll=bpy.data.collections.new('DETAIL v43 | Provisional station platform');scene.collection.children.link(coll)
root=bpy.data.objects.new('Station v43 | Movable reference assembly',None);coll.objects.link(root);root.matrix_world=basis
root['limits']='OSM footprint; dated photographs; schematic not to scale; Google verification pending'
archive=bpy.data.collections.new('ARCHIVE v43 | Misclassified shelter mass');archive.use_fake_user=True
old=bpy.data.objects['Extension v41 | OSM footprint 1428872589'];archive.objects.link(old)
for c in list(old.users_collection):
 if c!=archive:c.objects.unlink(old)
made=[]
def mat(name,c):
 m=bpy.data.materials.new('Station v43 | '+name);m.diffuse_color=(*c,1);return m
blue=mat('blue painted steel',(.055,.12,.25));white=mat('pale sign and edge',(.77,.77,.69));grey=mat('galvanised metal',(.32,.36,.38));yellow=mat('weathered tactile strip',(.54,.44,.19));dark=mat('dark glazing proxy',(.13,.19,.22));wood=mat('bench slats',(.28,.22,.14))
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def box(name,x0,x1,y0,y1,z0,z1,m):
 vs=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],F);me.materials.append(m);me.update()
 ob=bpy.data.objects.new('Station v43 | '+name,me);coll.objects.link(ob);ob.parent=root;made.append(ob);return ob
def text(name,body,x,y,z,size):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.002;cu.materials.append(white)
 ob=bpy.data.objects.new('Station v43 | '+name,cu);coll.objects.link(ob);ob.parent=root;ob.location=(x,y,z);ob.rotation_euler=(math.pi/2,0,0);made.append(ob)
# Thin closed overlays follow the long mapped straight platform edge.
length=(Vector(platform[2])-a).length
for i in range(math.ceil(length/2)):
 x=i*2;end=min(x+1.97,length)
 box('edge coping '+str(i),x,end,.03,.33,.005,.045,white)
 box('tactile paving '+str(i),x,end,.40,.83,.004,.025,yellow)
# Narrow rear-side furniture preserves a broad central walking strip.
# Counts, spacing and exact designs estimated from distant dated photo and OSM tags.
for j,x in enumerate((9.,27.,48.)):
 for leg in (-.68,.68):box('bench leg '+str(j),x+leg-.035,x+leg+.035,2.07,2.48,.02,.46,blue)
 for k in range(4):box('bench seat slat '+str(j)+' '+str(k),x-.95,x+.95,2.04+k*.105,2.12+k*.105,.45,.50,wood)
 for k in range(3):box('bench back slat '+str(j)+' '+str(k),x-.95,x+.95,2.49,2.54,.65+k*.12,.73+k*.12,wood)
for j,x in enumerate((5.,20.,34.,55.)):
 box('light mast '+str(j),x-.045,x+.045,2.49,2.58,.02,4.3,grey)
 box('light head '+str(j),x-.38,x+.38,2.28,2.68,4.25,4.34,grey)
 box('light diffuser '+str(j),x-.30,x+.30,2.30,2.65,4.23,4.25,white)
for j,x in enumerate((14.,43.)):
 for xx in (x-1.05,x+1.05):box('nameboard post '+str(j),xx-.035,xx+.035,2.48,2.55,.02,2.65,blue)
 box('Syston nameboard '+str(j),x-1.2,x+1.2,2.40,2.48,1.90,2.48,blue)
 text('Syston lettering '+str(j),'SYSTON',x,2.385,2.18,.35)
box('platform one sign',30.,30.55,2.35,2.44,2.2,2.85,blue);text('platform one lettering','1',30.275,2.33,2.5,.46)
box('platform one sign post',30.24,30.31,2.40,2.48,.02,2.2,blue)
# Shelter is a schematic placeholder, explicitly not a verified facade recreation.
for x in (33.,36.8):
 for y in (1.52,2.65):box('shelter frame post',x,x+.06,y,y+.06,.02,2.35,blue)
box('shelter rear glazing proxy',33.06,36.8,2.64,2.68,.45,2.25,dark)
box('shelter end glazing proxy',33.01,33.05,1.58,2.64,.45,2.25,dark)
box('shelter roof',32.85,37.01,1.35,2.87,2.35,2.47,blue)
box('shelter rear top rail',33.0,36.86,2.63,2.73,2.25,2.35,blue)
box('shelter rear bottom rail',33.0,36.86,2.63,2.73,.40,.48,blue)
for ob in made:
 if 'shelter' in ob.name.lower():ob.location.x-=4
 if 'platform one' in ob.name.lower():ob.location.x-=5
for ob in made:
 if ob.type=='MESH' and 'shelter' in ob.name.lower():
  for v in ob.data.vertices:
   v.co.x=44.76465+(v.co.x+ob.location.x-29)/3.86*4.96925;v.co.y=3.62328+(v.co.y-1.52)/1.19*1.72201
  ob.location.x=0;ob.data.update()
bpy.context.view_layer.update()
for name,(matrix,data) in original.items():
 ob=bpy.data.objects[name];current=ob.matrix_basis.copy()
 assert ob.data==data and max(abs(current[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5,name
bad=[]
for o in made:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free()
assert not bad,bad
report={'source':'assets/blender/pharmacie-midland-frontage-v42.blend','output':str(OUT.relative_to(ROOT)),'new_meshes':sum(o.type=='MESH' for o in made),'new_text_objects':sum(o.type=='FONT' for o in made),'parent_objects_preserved':len(original),'nonmanifold_or_nonpositive':bad,'mapped_platform_way':'309564449','limits':['Google overhead verification pending.','Furniture positions, counts and sizes estimated.','Shelter is schematic, not visually verified close-up.','Access ramp and station car park remain unfinished.','No rail corridor model yet.','Blender static geometry only; BO3 unchanged.']}
report.update({'archived_unchanged':[old.name],'mapped_shelter_way':'1428872589','corrections':['Replaced six-metre shelter proxy with low shelter on mapped footprint','Moved light mast clear of approach']})
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
