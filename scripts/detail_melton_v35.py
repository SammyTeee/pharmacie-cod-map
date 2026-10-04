"""Additive, catalogue-led Melton detailing. No engine changes or source edits."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
source=Path(bpy.data.filepath);assert source.name=='pharmacie-taraj-road-v34.blend'
out=ROOT/'assets/blender/pharmacie-melton-detail-v35.blend';assert not out.exists()
dest=ROOT/'recon/v35';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections.new('MAPPING v35 | Melton individual shop and terrace detail');scene.collection.children.link(coll)
basis=Matrix.Identity(4);made=[];current='street'
def mat(name,c):
 m=bpy.data.materials.new('Melton v35 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=.72;return m
cream=mat('warm stone',(.72,.69,.58));white=mat('paper and joinery',(.85,.85,.78));dark=mat('iron',(.035,.045,.04));red=mat('terracotta',(.48,.09,.045));green=mat('foliage',(.075,.22,.065));yellow=mat('gold lettering',(.95,.65,.08));blue=mat('poster blue',(.045,.14,.38));pink=mat('flowers',(.66,.18,.35));wood=mat('display timber',(.25,.16,.08));slate=bpy.data.materials['Street v17 | slate'];brick=bpy.data.materials['Syston v27 | weathered brick 2']
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new('Melton v35 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['catalogue_id']=current;o['engine_implemented']=False;made.append(o);return o
def box(name,x0,x1,y0,y1,z0,z1,m):return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],F,m)
def label(name,text,x,y,z,size,m):
 c=bpy.data.curves.new(name,'FONT');c.body=text;c.size=size;c.align_x='CENTER';c.extrude=.003;c.materials.append(m);o=bpy.data.objects.new('Melton v35 | '+current+' | '+name,c);coll.objects.link(o);o.matrix_world=basis@Matrix.Translation((x,y,z))@Matrix.Rotation(math.pi/2,4,'X');return o
specs=json.loads((ROOT/'recon/v25/validation.json').read_text())['catalogue_frontages'];records=[]
for spec in specs:
 current=spec['id'];src=bpy.data.objects.get('Syston v25 | '+current+' | upper facade')
 if not src:continue
 old=src.matrix_world;cols=[old.to_3x3().col[i].normalized() for i in range(3)];basis=Matrix(((cols[0].x,cols[1].x,cols[2].x,old.translation.x),(cols[0].y,cols[1].y,cols[2].y,old.translation.y),(cols[0].z,cols[1].z,cols[2].z,old.translation.z),(0,0,0,1)))
 sx=old.to_3x3().col[0].length;lo=min(v.co.x for v in src.data.vertices);hi=max(v.co.x for v in src.data.vertices)
 w=(hi-lo)*sx;basis.translation+=cols[0]*((lo+hi)*.5*sx);h=max(v.co.z for v in src.data.vertices)
 # Metric frontage dimensions derive from actual meshes, not historical estimates.
 if current not in {'B027','B028','B045','B032','B033','B015'}:
  a,b=-w/2-.09,w/2+.09;y0,y1=-.12,10.12;ridge=h+1.45
  mesh('closed pitched terrace roof',[(a,y0,h+.20),(b,y0,h+.20),(a,y1,h+.20),(b,y1,h+.20),(a,5,ridge),(b,5,ridge)],[(0,2,3,1),(0,1,5,4),(4,5,3,2),(0,4,2),(1,3,5)],slate)
  box('ridge cap',a,b,4.89,5.11,ridge-.04,ridge+.09,dark)
  for j in range(1,9):
   yy=y0+(5-y0)*j/9;zz=h+.20+(ridge-h-.20)*j/9
   box('slate course %02d'%j,a,b,yy-.016,yy+.016,zz,zz+.018,dark)
  if current not in {'B038','B039','B040','B051','B042','B043'}:
   x=w*.30;box('brick chimney stack',x-.30,x+.30,5.9,6.55,h+.65,h+2.0,brick);box('chimney stone crown',x-.36,x+.36,5.84,6.61,h+1.98,h+2.10,cream)
   for xx in (x-.17,x+.17):box('chimney pot',xx-.085,xx+.085,6.10,6.30,h+2.10,h+2.43,red)
  if current=='B014':
   # The brook-side bank has a clipped rear parcel, not a full-depth terrace.
   for ob in made:
    if ob.get('catalogue_id')=='B014':
     for v in ob.data.vertices:
      v.co.y*=.1;v.co.z=9.1+(v.co.z-9.1)*.15
 # Fine cornice/dentils, lintel relief and alternate blinds give terrace rhythm.
 box('eaves weathered cornice',-w/2,w/2,-.27,-.15,h-.25,h-.15,cream)
 for j in range(max(2,int(w/.42))):
  x=-w/2+.20+j*.42
  if x+.09<w/2:box('cornice tooth %02d'%j,x,x+.09,-.29,-.15,h-.39,h-.25,cream)
 count=max(1,int(w/2.9))
 for j in range(count):
  x=-w/2+(j+.5)*w/count;ww=min(1.68016,w/count-.55)
  box('upper lintel %02d'%j,x-ww/2-.08,x+ww/2+.08,-.25,-.18,8.48,8.59,cream)
  if j%2==0:
   for k in range(7):box('blind slat %d %d'%(j,k),x-ww*.42,x+ww*.42,-.132,-.115,7.55+k*.095,7.58+k*.095,cream)
 box('utility junction box',w/2-.52,w/2-.30,-.29,-.18,4.35,4.65,dark)
 box('horizontal service cable',-w/2+.15,w/2-.25,-.24,-.22,4.48,4.505,dark)
 # Small display graphics sit within glazing outlines; do not invent accessible interiors.
 rest=w-1.65;displayw=max(.8,(rest-.35)/2)
 if current in {'B010','B042','B025','B012'}:
  for bay in range(2):
   x=-w/2+1.6+(bay+.5)*rest/2
   for row in range(3):
    for col in range(3):
     xx=x+(col-1)*displayw*.25;z=.80+row*.58
     box('listing card %d %d %d'%(bay,row,col),xx-.17,xx+.17,-.143,-.130,z,z+.43,white);box('listing photograph %d %d %d'%(bay,row,col),xx-.145,xx+.145,-.150,-.143,z+.17,z+.39,blue)
 elif current in {'B035','B004','B041','B023','B039','B051','B017','B018','B019'}:
  for bay in range(2):
   x=-w/2+1.6+(bay+.5)*rest/2
   for row in range(2):
    box('window display shelf %d %d'%(bay,row),x-displayw*.42,x+displayw*.42,-.155,-.130,.8+row*.8,.85+row*.8,wood)
    for j in range(5):
     xx=x+(j-2)*displayw*.14;z=.86+row*.8
     box('display merchandise %d %d %d'%(bay,row,j),xx-.09,xx+.09,-.19,-.155,z,z+.23+(j%3)*.09,[red,green,cream,blue,pink][j])
 else:
  x=w*.15;box('opening hours backing',x-.16,x+.16,-.146,-.13,1.45,1.88,white)
  for j in range(5):box('opening hours line '+str(j),x-.12,x+.12,-.151,-.146,1.50+j*.065,1.515+j*.065,dark)
 if current in {'B003','B009','B034'}:
  x=w/2-.42;box('barber pole bracket',x-.06,x+.06,-.46,-.18,2.10,2.17,dark);box('barber pole housing',x-.10,x+.10,-.51,-.31,1.65,2.75,white)
  for j in range(8):box('barber pole stripe '+str(j),x-.105,x+.105,-.516,-.51,1.7+j*.12,1.755+j*.12,red if j%2 else blue)
 if current in {'B030','B003','B026'}:
  x=w/2-.4;box('projecting sign bracket',x-.04,x+.04,-.70,-.15,3.0,3.10,dark);box('projecting sign blade',x-.055,x+.055,-.75,-.28,2.45,2.98,blue if current=='B026' else dark)
 if current=='B034':
  box('correct black fascia overlay',-w/2+.02,w/2-.02,-.245,-.225,3.42,4.02,dark);label('gold barber fascia','GOLDEN BARBER',0,-.255,3.61,min(.48,w/17),yellow)
 if current=='B035':
  for x in (-w*.30,w*.25):
   box('flower tub',x-.17,x+.17,-.54,-.20,.02,.38,red)
   for j in range(4):box('flower cluster '+str(x)+' '+str(j),x-.16+j*.08,x-.10+j*.08,-.45,-.25,.40,.62+(j%2)*.10,pink if j%2 else green)
 if current=='B004':
  for j in range(3):
   x=-w*.15+j*.7;box('produce crate '+str(j),x-.28,x+.28,-.66,-.20,.05,.55,wood)
   for k in range(4):box('crate produce %d %d'%(j,k),x-.22+k*.12,x-.12+k*.12,-.60,-.28,.55,.68,green if j%2 else yellow)
 if current=='B031':
  box('passage crest panel',-.35,.35,-.20,-.17,3.49,4.02,red);label('passage crest','TS',0,-.215,3.60,.22,yellow)
 records.append({'id':current,'physical_width':w,'evidence':'docs/street-catalogue/entries/'+current+'.md'})
bpy.context.view_layer.update()
changes={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'new_solids':[o.name for o in made],'frontages':records,'engine_implemented':False,'scope':'Photo-led upper detailing and window display relief; hidden roof slopes, service fixings and display contents are modelling approximations. Original meshes remain unchanged.'}
(dest/'changes.json').write_text(json.dumps(changes,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(out));print('V35_COMPLETE',len(made),len(records),flush=True)
