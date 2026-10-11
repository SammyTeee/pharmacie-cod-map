"""Observed DR Electrical blue fence / brick boundary, estimated scene fit."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v52';dest.mkdir(exist_ok=True)
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-mirrored-window-v51.blend'
OUT=ROOT/'assets/blender/pharmacie-station-frontage-v52.blend';assert not OUT.exists()
scene=bpy.context.scene
def fingerprint(o):
 h=hashlib.sha256();h.update(repr((o.type,[list(r) for r in o.matrix_world],o.parent.name if o.parent else None)).encode())
 if o.type=='MESH':h.update(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode())
 if o.type=='FONT':h.update(repr((o.data.body,o.data.size,o.data.extrude)).encode())
 if hasattr(o.data,'materials'):h.update(repr([m.name if m else None for m in o.data.materials]).encode())
 return h.hexdigest()
before={o.name:fingerprint(o) for o in scene.objects}
coll=bpy.data.collections.new('DETAIL v52 | Station approach blue appliance frontage');scene.collection.children.link(coll)
a=Vector((19,863));b=Vector((52,872));u=(b-a).normalized();n=Vector((-u.y,u.x));length=(b-a).length
root=bpy.data.objects.new('Station v52 | Estimated DR boundary assembly',None);coll.objects.link(root);root.matrix_world=Matrix(((u.x,n.x,0,a.x),(u.y,n.y,0,a.y),(0,0,1,0),(0,0,0,1)))
root['evidence']='Visible Google Street View panorama dVYPkj-O2QW9N0UbzcxnJQ, Sept 2023; camera 52.6940665,-1.0815764 heading40. DR Electrical wall/blue palisade observed; dimensions/scene fit estimated.'
# Keep frontage outside the retained coarse warehouse footprint.
root.location.x+=n.x*2.5;root.location.y+=n.y*2.5
def mat(name,c):
 m=bpy.data.materials.new('Station v52 | '+name);m.diffuse_color=(*c,1);return m
brick=mat('red brown boundary brick',(.42,.16,.085));mortar=mat('weathered mortar',(.31,.25,.20));blue=mat('cobalt blue painted steel',(.035,.10,.65));navy=mat('blue sign board',(.015,.055,.23));white=mat('white lettering',(.90,.92,.89));stone=mat('moss stained coping',(.28,.29,.22))
made=[]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update();o=bpy.data.objects.new('Station v52 | '+name,me);coll.objects.link(o);o.parent=root;made.append(o);return o
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def box(name,x,y,z,w,d,h,m):return mesh(name,[(x+dx*w/2,y+dy*d/2,z+dz*h/2) for dx,dy,dz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]],F,m)
box('continuous low brick boundary backing',length/2,0,.62,length,.32,1.38,mortar)
for row in range(15):
 for j in range(int(length/.34)):
  x=(j+.5+(row%2)*.5)*.34
  if x>length-.12:continue
  box('individual face brick',x,.175,.055+row*.083,.315,.025,.068,brick)
for j in range(7):
 x=j*length/6;box('brick pier',x,0,1.23,.58,.53,2.60,brick);box('pier coping',x,0,2.57,.64,.59,.10,stone)
for j in range(int(length/.23)):
 x=.12+j*.23
 # Closed spear-topped steel pales; geometry rather than transparent image.
 w=.055;z0=1.35;z1=2.55
 vs=[(x+dx*w/2,dy*.045,z) for z in (z0,z1-.10) for dx,dy in [(-1,-1),(1,-1),(1,1),(-1,1)]]+[(x,-.045,z1),(x,.045,z1)]
 mesh('blue pointed palisade pale',vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,8),(5,6,9,8),(6,7,9),(7,4,8,9)],blue)
for z in (1.65,2.22):box('blue horizontal fence rail',length/2,-.03,z,length,.075,.07,blue)
for j in range(int(length/.28)):box('wall coping brick',j*.28+.14,0,1.36,.255,.40,.13,stone)
def text(body,x,z,size):
 cu=bpy.data.curves.new('Station v52 | lettering','FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.001;cu.materials.append(white);o=bpy.data.objects.new('Station v52 | '+body,cu);coll.objects.link(o);o.parent=root;o.location=(x,.245,z);o.rotation_euler=(math.pi/2,0,math.pi);made.append(o)
for i,label in enumerate(('Cookers & Ovens','Dishwashers','Refrigeration','Washing Machines')):
 x=(i+.5)*length/4;box('blue appliance category sign',x,.202,.78,length/4-.9,.035,.55,navy);text(label,x,.78,.29)
box('DR Electrical small upper sign',length*.30,.20,2.92,4.4,.035,.42,blue);text('DR Electrical',length*.30,2.92,.27)
bad=[]
for o in made:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free()
assert not bad,bad
bpy.context.view_layer.update();changed=[name for name,h in before.items() if fingerprint(bpy.data.objects[name])!=h];assert not changed,changed
report={'new_meshes':sum(o.type=='MESH' for o in made),'text_objects':sum(o.type=='FONT' for o in made),'unchanged_v51_scene_objects':len(before),'changed_parent_objects':changed,'bad_closed_meshes':bad,'assembly_origin':list(a),'u':list(u),'n':list(n),'length':length,'observed':['low red brick boundary and taller piers','bright blue pointed palisade and horizontal rails','blue appliance category signs','small DR Electrical sign'],'estimated':['boundary dimensions and fit to station approach','exact pier and pale count','lettering spacing','coping and brick dimensions'],'limits':['Source panorama observed, not measured survey','No source-image pixels copied into geometry','OSM building tag Buildbase nearby may be stale; no unverified building renamed','BO3 unchanged; final overhead alignment still pending']}
report['frontage_fit_outward_offset']=2.5;report['assembly_origin_final']=list(root.location)
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
