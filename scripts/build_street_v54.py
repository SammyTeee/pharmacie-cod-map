"""Photo-led Holmdale/Melton/Barkby street scenery; editable closed geometry."""
from pathlib import Path
import bpy,bmesh,json,math,time,random
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v54'
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-alignment-v53.blend'
OUT=ROOT/'assets/blender/pharmacie-surveyed-streets-v54.blend';assert not OUT.exists()
d=json.loads((dest/'prepared-street.json').read_text());sc=d['scale_BU_per_m'];scene=bpy.context.scene;start=time.monotonic();original={o.name:(o.matrix_basis.copy(),o.data) for o in scene.objects}
coll=bpy.data.collections.new('STREET v54 | Authored route photo-led frontages');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v54 | Replaced terrain perimeter and provisional masses');archive.use_fake_user=True;retired=[];made=[];basis=Matrix.Identity(4);item={};counter=0
def retire(ob):
 archive.objects.link(ob)
 for c in list(ob.users_collection):
  if c!=archive:c.objects.unlink(ob)
 retired.append(ob.name)
def material(name,c):
 m=bpy.data.materials.new('Survey v54 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.78;return m
brick=bpy.data.materials['Shop v19 | brick relief'];roofmat=bpy.data.materials['Street v17 | slate'];paving=bpy.data.materials['Syston v27 | concrete paving joints'];roadmat=bpy.data.materials['Street v36 | aged asphalt Street v17 | asphalt']
white=material('aged white joinery',(.78,.79,.74));cream=material('warm cream render',(.72,.69,.59));grey=material('painted grey',(.31,.34,.33));dark=material('dark ironwork',(.055,.068,.065));glass=material('blue grey glazing',(.12,.20,.23));green=material('deep green fascias',(.045,.22,.12));blue=material('deep retail blue',(.035,.13,.39));yellow=material('warm sign yellow',(.78,.58,.12));red=material('post box red',(.48,.025,.02));grass=material('short green planting',(.24,.31,.13));leaves=material('tree leaf green',(.19,.29,.10));wood=material('timber',(.27,.22,.15));brown=material('brown roof tiles',(.28,.25,.19));curtain=material('pale curtains',(.58,.56,.40))
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(label,vs,fs,m):
 global counter
 counter+=1;name=f'Survey v54 | {item.get("id","street")} | {label} {counter:04}'
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 ob=bpy.data.objects.new(name,me);coll.objects.link(ob);ob.matrix_world=basis.copy();ob['engine_implemented']=False;ob['evidence']='docs/AUTHORED_ROUTE_SURVEY_2026-10-11.md';ob['frontage_id']=item.get('id','street');ob['dimension_status']='Estimated dimensions; retained BU/m compatibility frame';made.append(ob);return ob
def box(label,x0,x1,y0,y1,z0,z1,m):
 assert x1>x0 and y1>y0 and z1>z0,label
 return mesh(label,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],F,m)
def roof(label,w,dep,h,kind):
 x=w/2+.25;y0=-.25;y1=dep+.25;rise=1.9*sc
 if kind=='shed':return mesh(label,[(-x,y0,h),(x,y0,h),(x,y1,h),(-x,y1,h),(-x,y0,h+1.1),(x,y0,h+1.1)],[(0,3,2,1),(0,1,5,4),(4,5,2,3),(0,4,3),(1,2,5)],roofmat)
 if kind=='hip':
  r=min(w*.28,dep*.28);vs=[(-x,y0,h),(x,y0,h),(x,y1,h),(-x,y1,h),(-x+r,dep/2,h+rise),(x-r,dep/2,h+rise)];fs=[(3,2,1,0),(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)]
 elif kind=='frontgable':
  vs=[(-x,y0,h),(x,y0,h),(x,y1,h),(-x,y1,h),(0,y0,h+rise),(0,y1,h+rise)];fs=[(3,2,1,0),(0,1,4),(3,5,2),(0,4,5,3),(1,2,5,4)]
 else:
  vs=[(-x,y0,h),(x,y0,h),(x,y1,h),(-x,y1,h),(-x,dep/2,h+rise),(x,dep/2,h+rise)];fs=[(3,2,1,0),(0,1,5,4),(4,5,2,3),(0,4,3),(1,2,5)]
 return mesh(label,vs,fs,brown if kind=='hip' else roofmat)
def window(x,z,w=1.25,h=1.5,y=0,mullion=True):
 box('window outer frame',x-w/2,x+w/2,y-.12,y+.01,z,z+h,white)
 box('window glass',x-w/2+.075,x+w/2-.075,y-.15,y-.12,z+.08,z+h-.08,glass)
 if mullion:box('window centre mullion',x-.025,x+.025,y-.18,y-.15,z+.08,z+h-.08,white)
 box('window upper transom',x-w/2+.07,x+w/2-.07,y-.18,y-.15,z+h*.71,z+h*.71+.045,white)
 box('projecting sill',x-w/2-.06,x+w/2+.06,y-.25,y+.02,z-.06,z,cream)
def door(x,w=1,h=2.2,m=dark):
 box('door surround',x-w/2-.09,x+w/2+.09,-.1,.02,0,h+.1,white);box('door leaf',x-w/2,x+w/2,-.14,-.1,.04,h,m);box('door upper glass',x-w*.36,x+w*.36,-.17,-.14,h*.45,h-.12,glass);box('door handle',x+w*.3,x+w*.34,-.23,-.17,.93,1.04,white)
def sign(body,w,z,m):
 box('fascia panel',-w/2,w/2,-.28,-.12,z-.26,z+.26,m)
 if body:
  cu=bpy.data.curves.new('Survey sign '+body,'FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=min(.46,w/max(4,len(body))*.95);cu.extrude=.006;cu.materials.append(white)
  ob=bpy.data.objects.new('Survey v54 | '+item.get('id','street')+' | '+body,cu);coll.objects.link(ob);ob.matrix_world=basis@Matrix.Translation((0,-.30,z))@Matrix.Rotation(math.pi/2,4,'X');ob['engine_implemented']=False;made.append(ob)
def archwindow(x,z,w,h,m=white,y=0):
 # Solid arched insert with a lower rectangle and semicircular crown.
 r=w/2;ps=[(x-r,z),(x+r,z),(x+r,z+h-r)]+[(x+r*math.cos(t*math.pi/12),z+h-r+r*math.sin(t*math.pi/12)) for t in range(1,13)]
 vs=[(xx,yy,zz) for yy in (y-.12,y-.03) for xx,zz in ps];n=len(ps);fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];mesh('arched surround',vs,fs,m)
 window(x,z+.12,w-.22,h-.4,y-.14)
def ball(label,p,r,m):
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=1,radius=r)
 for v in bm.verts:v.co+=Vector(p)
 bm.verts.ensure_lookup_table();vs=[tuple(v.co) for v in bm.verts];fs=[[v.index for v in f.verts] for f in bm.faces];bm.free();return mesh(label,vs,fs,m)
def fence(w,y,z=.9):
 box('boundary plinth',-w/2,w/2,y,y+.16,-.25,.28,brick)
 for x in range(math.ceil(w/.8)):
  xx=-w/2+x*.8;box('boundary rail upright',xx,xx+.045,y+.04,y+.09,.28,z,dark)
 box('boundary top rail',-w/2,w/2,y+.04,y+.09,z-.04,z,dark)
# Replace only current estimate surfaces; immutable originals stay archived.
for key in ('terrain','boundary'):retire(bpy.data.objects['Survey v53 | Joined '+key])
for name in d['retire_boundaries']:retire(bpy.data.objects[name])
materials={'terrain':bpy.data.materials['Extension v41 | earth backing'],'boundary':brick,'Barkby road':roadmat,'Barkby kerb':bpy.data.materials['Extension v41 | pale concrete kerbs'],'Barkby footway':paving,'retained perimeter remainder':brick}
for key,me in d['surfaces'].items():mesh(key,me['vertices'],me['faces'],materials[key])
# Superseded provisional church mass is archived; the station warehouse remains.
for osm in ('1155793607',):retire(bpy.data.objects['Extension v41 | OSM footprint '+osm])
for item in d['frontages']:
 f=item['frame'];p=f['origin'];x=f['x'];n=f['y'];basis=Matrix(((x[0],n[0],0,p[0]),(x[1],n[1],0,p[1]),(0,0,1,0),(0,0,0,1)))
 w=item['width_m']*sc;dep=item['depth_m']*sc;h=item['eaves_m']*sc;style=item['style'];paint={'brick':brick,'cream':cream,'grey':grey}[item['paint']]
 body=box(item['label']+' enclosed shell',-w/2,w/2,0,dep,-.3,h,paint);body['source_stops']=json.dumps(item['source_stops']);body['schedule']=json.dumps({k:v for k,v in item.items() if k not in ('frame','polygon')})
 box('foundation brick course',-w/2,w/2,-.02,.04,-.3,.5,brick);roof('closed roof',w,dep,h,item['roof']);box('white eaves fascia',-w/2-.26,w/2+.26,-.28,-.22,h-.14,h+.02,white)
 for xx in (-w/2+.12,w/2-.16):box('rainwater downpipe',xx,xx+.06,-.09,-.02,.1,h,grey)
 if style in ('house','bayhouse'):
  floors=2 if h>4 else 1
  for iz in range(floors):
   z=.8+iz*2.9*sc
   for xx in (-w*.29,w*.27):
    if style=='bayhouse':
     box('projecting bay brick support',xx-1.02,xx+1.02,-.60,.01,z-.65,z-.04,paint);window(xx,z,1.95,1.55,y=-.60)
     for side in (-1,1):box('bay outer cheek',xx+side*1.02-.04,xx+side*1.02+.04,-.60,.04,z-.04,z+1.63,white)
    else:window(xx,z,1.5,1.55)
  door(-.15);box('entrance canopy',-.95,.65,-.75,.05,2.3,2.4,roofmat)
  box('garden grass',-w/2,w/2,-2.1,-.55,-.22,-.04,grass);box('drive apron',w*.25,w*.48,-4.3,.0,-.26,-.025,paving)
  if item['chain_m']>166:fence(w,-2.45)
 elif style.startswith('shop'):
  for xx in (-w*.29,w*.28):window(xx,.42,w*.32,2.15,mullion=False)
  door(0,w=.95);col=yellow if item.get('sign')=='HAPPY GARDEN' else green if item.get('sign') and 'GREEN' in item['sign'] else dark if item.get('sign')=='LUCILLE HAIR STUDIO' else blue if item['id']=='R010' else grey
  sign(item.get('sign'),w-.12,2.95,col)
  for zz in ([3.7,6.3] if h>8 else [3.7] if h>4 else []):
   for xx in (-w*.28,w*.28):
    if style=='shopbay':box('upper projecting bay apron',xx-.88,xx+.88,-.48,.01,zz-.30,zz-.04,cream);window(xx,zz,1.6,1.7,y=-.45)
    else:window(xx,zz,1.5,1.6)
  if style=='shopdormer':
   box('dormer face',-.85,.85,dep*.23,dep*.42,h-.1,h+1.25,cream);window(0,h+.1,1.25,1.,y=dep*.23);oldbasis=basis.copy();basis=basis@Matrix.Translation((0,dep*.23,h+1.25));roof('dormer roof',1.8,dep*.18,0,'frontgable');basis=oldbasis
 elif style=='flats':
  for z in (1.0,3.85):
   for xx in [(-w/2+1.5)+j*3.3 for j in range(int(w/3.3))]:window(xx,z,1.5,1.45)
  box('grey floor band',-w/2,w/2,-.09,.0,3.1,3.4,grey);door(0);fence(w,-2.4,1.15)
 elif style in ('church','hall'):
  for xx in (-w*.32,0,w*.32):archwindow(xx,1.1,2.0,3.5)
  door(0,1.5,2.5,blue)
  if style=='church':archwindow(0,h-.4,2.8,2.4,cream);box('church modest cross vertical',-.07,.07,-.16,-.10,h+1.1,h+2.5,white);box('church cross horizontal',-.43,.43,-.16,-.10,h+1.9,h+2.04,white)
 elif style=='supermarket':
  for j in range(12):window(-w/2+2+j*(w-4)/11,.55,2.8,2.6,mullion=False)
  box('entrance canopy',-5,5,-2.8,1,3.15,3.35,grey)
  for xx in (-4.5,4.5):box('entrance canopy post',xx,xx+.12,-2.45,-2.30,-.1,3.2,grey)
  sign('ALDI',4,3.85,blue);box('setback car park paving',-w/2,w/2,-10,-3,-.30,-.08,roadmat)
  for j in range(9):box('parking bay line',-w/2+j*4.5,-w/2+j*4.5+.08,-9,-4,-.079,-.073,white)
 elif style=='workshop':
  for xx in (-w*.27,w*.27):
   box('closed shutter',xx-w*.15,xx+w*.15,-.10,-.02,.1,2.6,grey)
   for k in range(12):box('shutter horizontal slat',xx-w*.15,xx+w*.15,-.13,-.10,.15+k*.19,.18+k*.19,dark)
  sign(item.get('sign'),w-.1,min(h-.25,3),blue)
 if h>4 and style not in ('supermarket','flats'):
  box('brick chimney',w*.22,w*.22+.7,dep*.45,dep*.45+.9,h+1,h+2.6,brick)
  box('chimney cap',w*.22-.08,w*.22+.78,dep*.45-.08,dep*.45+.98,h+2.6,h+2.73,cream)
  for xx in (w*.22+.1,w*.22+.43):box('chimney pot',xx,xx+.18,dep*.45+.25,dep*.45+.45,h+2.73,h+3.10,brown)
 if style not in ('supermarket','workshop'):box('front entrance slab',-.8,.8,-.8,-.02,-.24,-.03,paving)
# Street furniture and open greens are positioned outside route walking lines.
item={};basis=Matrix.Identity(4)
route=json.loads((ROOT/'recon/v53/survey-geometry.json').read_text())['route_world'];segments=[];total=0
for a,b in zip(route,route[1:]):L=math.dist(a,b);segments.append((total,total+L,Vector(a),Vector(b)));total+=L
def streetframe(chain,side,off):
 for aa,bb,a,b in segments:
  if aa<=chain*sc<=bb:u=(b-a).normalized();p=a+u*(chain*sc-aa);break
 n=Vector((-u.y,u.x))*side;x=Vector((n.y,-n.x));p+=n*off
 return Matrix(((x.x,n.x,0,p.x),(x.y,n.y,0,p.y),(0,0,1,0),(0,0,0,1)))
for chain in (204,252,300,348,396,444,492,540,588,636):
 basis=streetframe(chain,-1,7.0);box('lamp pole',-.045,.045,-.045,.045,-.1,5.5,dark);box('lamp outreach',-.05,.05,-1.2,.05,5.45,5.55,dark);box('lamp head',-.24,.24,-1.35,-.8,5.40,5.5,grey)
for chain in (210,235,260,280,460,559,580,610):
 basis=streetframe(chain,1 if chain<300 else -1,14);box('tree trunk',-.16,.16,-.16,.16,-.3,3.0,wood);ball('tree canopy',(0,0,3.6),2.1,leaves);box('planted bed',-2,2,-1.6,1.6,-.29,-.06,grass)
# Visible red post box by station junction, wall-side not in pavement centre.
basis=streetframe(196,-1,7.1);box('red post box pillar',-.25,.25,-.25,.25,-.1,1.32,red);box('post box cap',-.31,.31,-.31,.31,1.32,1.46,red);box('post box letter slot',-.17,.17,-.28,-.25,1.03,1.09,dark)
# Static zebra at the monument/Aldi approach, signal crossing near station.
for chain,mode in ((212,'signal'),(552,'zebra')):
 basis=streetframe(chain,1,0)
 for j in range(7):box(mode+' road crossing stripe',-2.2,2.2,-3.8+j*1.1,-3.25+j*1.1,-.079,-.073,white)
 for side in (-1,1):
  yy=side*6.9;box('crossing pole',-.045,.045,yy-.045,yy+.045,-.1,2.9,dark)
  if mode=='zebra':
   for z in (.35,1.05,1.75,2.45):box('Belisha white band',-.052,.052,yy-.052,yy+.052,z,z+.3,white)
   ball('Belisha globe',(0,yy,3.0),.22,yellow)
  else:
   box('signal head',-.18,.18,yy-.16,yy+.16,2.2,2.95,dark)
   for z,m in ((2.32,green),(2.56,yellow),(2.8,red)):ball('static signal lens',(-.19,yy,z),.075,m)
  box('tactile crossing landing',-1.1,1.1,yy-.55,yy+.55,-.015,.008,yellow)
basis=Matrix.Identity(4);bpy.context.view_layer.update()
bad=[]
for ob in made:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(ob.name)
 bm.free()
assert not bad,bad
for name,(matrix,data) in original.items():
 ob=bpy.data.objects[name];assert ob.data==data,name
 assert max(abs(ob.matrix_basis[r][c]-matrix[r][c]) for r in range(4) for c in range(4))<1e-5,name
report={'source':'assets/blender/pharmacie-holmdale-alignment-v53.blend','output':str(OUT.relative_to(ROOT)),'frontages':len(d['frontages']),'new_closed_meshes':sum(o.type=='MESH' for o in made),'new_text_objects':sum(o.type=='FONT' for o in made),'preserved_source_objects':len(original),'archived_unchanged':retired,'nonmanifold_or_nonpositive':bad,'limits':d['limits'],'seconds':time.monotonic()-start}
(dest/'build-validation.json').write_text(json.dumps(report,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=report
