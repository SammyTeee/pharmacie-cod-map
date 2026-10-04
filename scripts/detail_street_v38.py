"""An enclosed Town Square recess and individual retail display relief."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,random,os
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath)
assert source.name=='pharmacie-street-scenes-v37.blend'
out=ROOT/'assets/blender/pharmacie-town-square-v38.blend';assert not out.exists() or os.environ.get('V38_REBUILD')=='1'
dest=ROOT/'recon/v38';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene;bpy.context.view_layer.update()
coll=bpy.data.collections.new('STREET v38 | Town Square passage and shop displays');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v38 | Retained superseded B031 and display blocks');archive.use_fake_user=True
basis=Matrix.Identity(4);current='B031';made=[];retired=[];labels=[];routes=[];views=[]
# Reuse the established closed-solid and frontage-frame helpers.
helpers=(ROOT/'scripts/detail_street_v37.py').read_text();helpers=helpers[helpers.index('F=['):helpers.index('# Retain the shelter position')].replace('Street v37 |','Street v38 |');exec(compile(helpers,'v38_geometry_helpers','exec'))
def mat(name,c,rough=.8):
 m=bpy.data.materials.new('Street v38 | '+name);m.use_nodes=True;m.diffuse_color=(*c,1);p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=rough;return m
brick=bpy.data.materials['Syston v27 | weathered brick 2'];paving=bpy.data.materials['Street v37 | block paving'];dark=bpy.data.materials['Street v37 | dark fittings'];steel=bpy.data.materials['Street v37 | galvanised steel'];cream=mat('painted pale joinery',(.69,.67,.58));red=mat('Town Square burgundy',(.29,.035,.028));gold=mat('aged gold trim',(.68,.47,.10));glass=mat('shop display charcoal glazing',(.085,.13,.14),.22);tile=mat('passage plaster ceiling',(.40,.39,.34));wood=bpy.data.materials['Street v36 | weathered bench timber'];paper=mat('display paper',(.78,.75,.65));blue=mat('display blue',(.05,.19,.31));green=mat('display green',(.12,.27,.09));pink=mat('display rose',(.58,.16,.26));yellow=mat('display ochre',(.65,.44,.06));light=mat('warm bulkhead glass',(.80,.63,.36));p=light.node_tree.nodes['Principled BSDF'];p.inputs['Emission Color'].default_value=(1,.72,.37,1);p.inputs['Emission Strength'].default_value=2
w=frontage('B031')
sidebrick=brick.copy();sidebrick.name='Street v38 | passage brick along depth'
for combine in [n for n in sidebrick.node_tree.nodes if n.type=='COMBXYZ']:
 for link in list(combine.inputs['X'].links):
  if link.from_node.type=='SEPXYZ':
   separator=link.from_node;sidebrick.node_tree.links.remove(link);sidebrick.node_tree.links.new(separator.outputs['Y'],combine.inputs['X'])
# Retire the generic entire lower-front shop and solid parcel, preserving all originals.
for o in list(scene.objects):
 if '| B031 |' not in o.name or o.type not in ('MESH','FONT'):continue
 zs=[(o.matrix_world@Vector(v)).z for v in o.bound_box]
 if max(zs)<4.26 or 'rear scenery mass' in o.name:retire(o)
half=1.25
for s in (-1,1):
 a,b=(-w/2,-half) if s<0 else (half,w/2)
 box('retained parcel side mass',a,b,1.25,10,0,8.9,brick)
 outera,outerb=(a,-half-.62) if s<0 else (half+.62,b)
 box('entry outer brick pier',outera,outerb,.12,1.25,0,3.32,brick)
 box('display brick plinth',a,b,.12,1.25,0,.60,brick)
 box('display upper brick band',a,b,.12,1.25,2.88,3.32,brick)
 box('entry brick header',a,b,-.07,.20,2.93,3.35,brick)
 # Angled glass display bay bounded by opaque backing, away from the walking aperture.
 edge=s*(half+.62)
 ps=[(s*half,1.10),(edge,.03),(edge,.08),(s*half,1.15)]
 mesh('angled glazing',[(x,y,z) for z in (.65,2.83) for x,y in ps],F,glass)
 backed=[(x,y+.06) for x,y in ps]
 mesh('opaque angled display backing',[(x,y,z) for z in (.65,2.83) for x,y in backed],F,dark)
 for z in (.60,1.73,2.84):pipe('angled display rail',(s*half,1.10,z),(edge,.03,z),.026,cream)
 for x,y in ((s*half,1.10),(edge,.03)):pipe('display upright',(x,y,.60),(x,y,2.9),.032,cream)
 # A framed information poster on each wing rather than another generic full shop window.
 px=s*(half+1.25);box('wing poster case',px-.25,px+.25,-.10,-.055,.83,2.64,dark);box('wing poster sheet',px-.22,px+.22,-.11,-.10,.88,2.59,paper)
 label('wing directory heading','TOWN\nSQUARE',(px,-.12,2.22),.115,red)
 for j in range(8):box('directory line',px-.18,px+.18,-.118,-.112,1.08+j*.10,1.092+j*.10,dark)
box('passage floor',-half,half,-.10,7,-.22,.025,paving)
for s in (-1,1):
 a,b=(-half-.22,-half+.008) if s<0 else (half-.008,half+.22)
 box('passage side wall',a,b,1.13,7,.01,3.28,sidebrick)
 box('passage skirting',a-.012,b+.012,1.15,6.8,.02,.15,dark)
box('continuous passage ceiling',-half-.22,half+.22,1.10,7,3.06,3.29,tile)
box('entry overhead lintel',-w/2,w/2,-.06,1.20,3.28,4.1,brick)
box('closed rear parcel backing',-w/2,w/2,7,10,0,8.9,brick)
# Rear boundary is a closed shop/service gate, not an invented connection to B028.
box('rear gate panel',-1.15,1.15,6.73,6.83,.04,2.83,dark)
for xx in (-1.19,1.19):box('rear gate jamb',xx-.04,xx+.04,6.70,6.85,.01,2.92,steel)
for i in range(13):box('gate vertical rib',-1.11+i*.18,-1.075+i*.18,6.715,6.73,.08,2.80,steel)
box('gate centre rail',-1.14,1.14,6.695,6.715,1.08,1.16,steel);label('rear boundary notice','SERVICE ACCESS\nKEEP CLEAR',(0,6.68,1.6),.11,paper)
for y in (1.65,3.80,5.75):
 box('ceiling bulkhead housing',-.30,.30,y-.16,y+.16,2.95,3.06,dark);box('bulkhead diffuser',-.26,.26,y-.13,y+.13,2.935,2.951,light)
 data=bpy.data.lights.new('Town Square warm ceiling fill','AREA');data.energy=35;data.color=(1,.74,.45);data.shape='RECTANGLE';data.size=.52;data.size_y=.26;o=bpy.data.objects.new(data.name,data);coll.objects.link(o);o.matrix_world=basis@Matrix.Translation((0,y,2.91))
 # Shallow steel ceiling cable tray follows the side, keeping headroom clear.
 box('ceiling service conduit',1.08,1.105,y-.9,y+.9,2.88,2.91,dark)
# A red and gold sign with a curved crest, following native270 at the retained facade scale.
box('Town Square sign surround',-1.67,1.67,-.23,-.14,3.40,3.97,dark);box('Town Square sign face',-1.61,1.61,-.25,-.23,3.44,3.93,red)
for z in (3.45,3.91):box('sign gold horizontal trim',-1.60,1.60,-.26,-.25,z,z+.018,gold)
for x in (-1.61,1.59):box('sign gold end trim',x,x+.02,-.26,-.25,3.45,3.93,gold)
label('Town Square lettering','TOWN SQUARE',(0,-.27,3.57),.26,gold)
arc=[(-.55,3.97),(.55,3.97)]+[(.55*math.cos(i*math.pi/16),3.97+.55*math.sin(i*math.pi/16)) for i in range(17)]
# Use a simple convex semicircle extrusion, with the straight baseline first.
arc=[(.55*math.cos(i*math.pi/16),3.97+.55*math.sin(i*math.pi/16)) for i in range(17)]
mesh('arched crest',[(x,y,z) for y in (-.23,-.18) for x,z in arc],[tuple(reversed(range(17))),tuple(range(17,34))]+[(i,(i+1)%17,(i+1)%17+17,i+17) for i in range(17)],red)
label('crest initials','TS',(0,-.245,4.10),.23,gold)
pipe('projecting banner bracket',(w/2-.40,-.15,4.65),(w/2-.40,-.85,4.65),.022,dark)
box('hanging banner',w/2-.425,w/2-.375,-.79,-.24,3.77,4.64,red)
route('Town Square entry and return',[(0,-1.3,0),(0,1.4,0),(0,6.10,0)])
route('Town Square pavement',[(-w/2+.3,-1.3,0),(w/2-.3,-1.3,0)])
view('01_town_square',(-4.0,-7.3,1.70),(0,.7,2.0));view('02_passage',(0,.25,1.62),(0,6.5,1.60))
# Two individual display treatments, shaped for their business category.
for cid in ('B041','B039'):
 w=frontage(cid)
 for o in list(scene.objects):
  if o.name.startswith('Melton v35 | '+cid+' |') and any(s in o.name for s in ('window display shelf','display merchandise')):retire(o)
 rest=w-1.65;bayw=max(.8,(rest-.35)/2)
 for bay in range(2):
  x=-w/2+1.6+(bay+.5)*rest/2
  for row in range(3):
   z=.66+row*.69;box('display tier',x-bayw*.40,x+bayw*.40,-.17,-.11,z,z+.045,wood)
   for j in range(6):
    xx=x+(j-2.5)*bayw*.125
    if cid=='B041':
     paint=[red,blue,green,yellow,paper,pink][j];pipe('paint tin',(xx,-.17,z+.045),(xx,-.17,z+.33),.092,paint,20);pipe('paint tin lid',(xx,-.17,z+.33),(xx,-.17,z+.344),.097,steel,20);box('paint tin label',xx-.059,xx+.059,-.268,-.262,z+.10,z+.25,paper);label('paint label','PAINT',(xx,-.274,z+.16),.026,dark)
    else:
     box('greeting card',xx-.090,xx+.090,-.20,-.175,z+.05,z+.43,paper)
     box('card coloured print',xx-.072,xx+.072,-.207,-.20,z+.18,z+.38,[red,blue,green,yellow,pink,paper][j])
     label('card title',['HAPPY','THANKS','HELLO','FOR YOU','LOVE','HAPPY'][j],(xx,-.211,z+.10),.025,dark)
     pipe('card graphic stem',(xx,-.213,z+.22),(xx,-.213,z+.31),.004,gold,6)
 if cid=='B041':
  view('03_diy_display',(-w*.25,-4.3,1.5),(w*.12,-.15,1.5))
 else:view('04_card_display',(-w*.25,-4.3,1.5),(w*.12,-.15,1.5))
 route(cid+' pavement through',[(-w/2+.5,-1.3,0),(w/2-.5,-1.3,0)])
bpy.context.view_layer.update()
(dest/'review-views.json').write_text(json.dumps(views,indent=2));(dest/'local-routes.json').write_text(json.dumps(routes,indent=2))
(dest/'changes.json').write_text(json.dumps(dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),new_solids=[o.name for o in made],archived=retired,labels=labels,engine_implemented=False,scope='B031 native270 informs visible red/gold entrance, brick and angled bays. Enclosed 7m recess/rear service boundary is inferred gameplay adaptation; no connection or functional unlock. DIY/card window contents are category-led approximations.'),indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(out));print('V38_COMPLETE',len(made),len(retired),flush=True)
