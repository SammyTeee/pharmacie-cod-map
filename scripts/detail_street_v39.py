"""Category-led retail display construction, keeping the approved street footprint."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,random,os
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath)
assert source.name=='pharmacie-town-square-v38.blend'
out=ROOT/'assets/blender/pharmacie-retail-detail-v39.blend';assert not out.exists() or os.environ.get('V39_REBUILD')=='1'
dest=ROOT/'recon/v39';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene;bpy.context.view_layer.update()
coll=bpy.data.collections.new('STREET v39 | Florist jeweller optician bakery and charity displays');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v39 | Retained generic merchandise');archive.use_fake_user=True
basis=Matrix.Identity(4);current='retail';made=[];retired=[];labels=[];routes=[];views=[]
helpers=(ROOT/'scripts/detail_street_v37.py').read_text();helpers=helpers[helpers.index('F=['):helpers.index('# Retain the shelter position')].replace('Street v37 |','Street v39 |');exec(compile(helpers,'v39_geometry_helpers','exec'))
def mat(name,c,rough=.7,metal=0):
 m=bpy.data.materials.new('Street v39 | '+name);m.use_nodes=True;m.diffuse_color=(*c,1);p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
paper=mat('warm wrapping paper',(.74,.68,.53));cream=mat('linen',(.75,.75,.68));dark=bpy.data.materials['Street v37 | dark fittings'];steel=bpy.data.materials['Street v37 | galvanised steel'];wood=bpy.data.materials['Street v36 | weathered bench timber'];gold=mat('jewellery brass',(.67,.43,.085),.27,.85);velvet=mat('display velvet',(.055,.075,.095));pink=mat('rose petals',(.54,.095,.22));yellow=mat('cream petals',(.83,.62,.24));green=mat('flower stems',(.055,.19,.07));blue=mat('navy fabric',(.035,.105,.19));red=mat('rust fabric',(.36,.085,.045));bread=mat('baked crust',(.57,.30,.095));crumb=mat('bread scoring',(.83,.62,.32));glass=mat('display lens',(.15,.24,.25),.16);rng=random.Random(39)
# Procedural cloth grain and fibres, not copied photographs.
for m in (cream,blue,red,paper):
 n=m.node_tree.nodes;l=m.node_tree.links;tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=145;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],noise.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.0018;b.inputs['Strength'].default_value=.25;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],n['Principled BSDF'].inputs['Normal'])
def horizontal_ring(name,x,y,z,R,r,m):
 o=torus(name,0,0,0,R,r,m)
 for v in o.data.vertices:
  p=v.co.copy();v.co=Vector((x+p.x,y+p.z,z+p.y))
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 return o
def shirt(name,x,y,z,s,m):
 # Closed shirt silhouette, including sleeves rather than a rectangular display block.
 ps=[(-.23,.0),(.23,.0),(.23,.40),(.40,.28),(.50,.45),(.25,.64),(.11,.67),(.07,.58),(-.07,.58),(-.11,.67),(-.25,.64),(-.50,.45),(-.40,.28),(-.23,.40)]
 N=len(ps);mesh(name,[(x+a*s,yy,z+b*s) for yy in (y,y+.045) for a,b in ps],[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m)
for idx,cid in enumerate(('B035','B036','B015','B024','B017','B002')):
 w=frontage(cid)
 for o in list(scene.objects):
  if o.name.startswith('Melton v35 | '+cid+' |') and any(s in o.name for s in ('window display shelf','display merchandise','opening hours')):retire(o)
 rest=w-1.65;bayw=max(.8,(rest-.35)/2)
 for bay in range(2):
  x=-w/2+1.6+(bay+.5)*rest/2
  if cid=='B035':
   for row in range(2):
    z=.65+row*.85;box('florist display shelf',x-bayw*.41,x+bayw*.41,-.235,-.13,z,z+.045,wood)
    for j in range(4):
     xx=x+(j-1.5)*bayw*.19
     pipe('flower pot',(xx,-.235,z+.045),(xx,-.235,z+.24),.09,red,14);horizontal_ring('pot lip',xx,-.235,z+.24,.095,.012,paper)
     for k in range(5):
      a=k*math.tau/5;px=xx+math.cos(a)*.08;py=-.235+math.sin(a)*.035;pz=z+.43+(k%2)*.08
      pipe('bouquet stem',(xx,-.235,z+.22),(px,py,pz),.008,green,6)
      blob('flower centre',(px,py,pz),(.023,.018,.023),yellow,rng)
      for q in range(4):
       b=q*math.tau/4;blob('flower petal',(px+math.cos(b)*.034,py-.010,pz+math.sin(b)*.034),(.035,.019,.022),pink if j%2 else cream,rng)
     box('florist stock ticket',xx-.055,xx+.055,-.347,-.337,z+.08,z+.15,paper)
  elif cid=='B036':
   for row in range(2):
    z=.68+row*.85;box('jewellery velvet tray',x-bayw*.4,x+bayw*.4,-.25,-.12,z,z+.07,velvet);box('tray brass lip',x-bayw*.4,x+bayw*.4,-.26,-.245,z+.03,z+.085,gold)
    for j in range(5):
     xx=x+(j-2)*bayw*.15
     box('ring presentation block',xx-.07,xx+.07,-.23,-.15,z+.07,z+.19,cream);pipe('ring support pin',(xx,-.235,z+.19),(xx,-.235,z+.24),.005,gold,6);torus('display ring',xx,-.244,z+.24,.035,.008,gold);blob('ring stone',(xx,-.249,z+.279),(.015,.009,.013),glass,rng)
    for j in range(2):
     xx=x+(j-.5)*bayw*.48;box('necklace display stand',xx-.10,xx+.10,-.185,-.145,z+.28,z+.61,velvet)
     torus('necklace chain',xx,-.201,z+.48,.092,.005,gold);blob('necklace pendant',(xx,-.205,z+.38),(.016,.009,.027),gold,rng)
   label('repair wording','JEWELLERY & REPAIRS',(x,-.268,2.62),min(.12,bayw/20),paper)
  elif cid=='B015':
   for row in range(3):
    z=.70+row*.57;box('optical display ledge',x-bayw*.40,x+bayw*.40,-.23,-.13,z,z+.035,cream)
    for j in range(5):
     xx=x+(j-2)*bayw*.15
     for side in (-1,1):torus('spectacle rim',xx+side*.043,-.248,z+.13,.032,.005,dark if row%2 else gold)
     pipe('spectacle bridge',(xx-.012,-.248,z+.132),(xx+.012,-.248,z+.132),.004,steel,6)
     box('spectacle stand foot',xx-.025,xx+.025,-.26,-.18,z+.035,z+.043,steel);pipe('spectacle stand',(xx,-.242,z+.043),(xx,-.242,z+.132),.005,steel,6)
     for side in (-1,1):pipe('spectacle arm',(xx+side*.073,-.248,z+.135),(xx+side*.073,-.14,z+.135),.004,dark,6)
   label('optical display heading','FRAMES',(x,-.25,2.58),.14,cream)
  elif cid=='B024':
   for row in range(3):
    z=.65+row*.58;box('bakery display tray',x-bayw*.40,x+bayw*.40,-.26,-.13,z,z+.045,steel)
    for j in range(5):
     xx=x+(j-2)*bayw*.15;blob('bread roll',(xx,-.23,z+.11),(.12,.065,.07),bread,rng)
     for q in range(3):pipe('bread score',(xx-.08+q*.055,-.283,z+.12),(xx-.05+q*.055,-.285,z+.15),.007,crumb,6)
    box('tray label',x-.10,x+.10,-.275,-.265,z-.035,z+.015,paper)
   label('bakery heading','FRESHLY BAKED',(x,-.28,2.58),min(.12,bayw/23),cream)
  elif cid=='B017':
   box('clothes rail base',x-bayw*.4,x+bayw*.4,-.23,-.13,.60,.67,wood)
   pipe('clothes hanging rail',(x-bayw*.38,-.15,2.42),(x+bayw*.38,-.15,2.42),.014,steel)
   for j in range(4):
    xx=x+(j-1.5)*bayw*.20;shirt('charity clothing',xx,-.24,1.49,.8,[blue,red,cream,pink][j]);pipe('hanger hook',(xx,-.19,2.04),(xx,-.19,2.41),.006,steel,6)
    box('clothing tag',xx-.026,xx+.026,-.252,-.246,1.82,1.90,paper)
   for j in range(5):
    xx=x+(j-2)*bayw*.15
    for k in range(3):box('folded clothes',xx-.10,xx+.10,-.23,-.13,.68+k*.055,.725+k*.055,[cream,blue,red][k])
  else:
   box('carpet sample plinth',x-bayw*.40,x+bayw*.40,-.245,-.13,.61,.71,wood)
   for j in range(6):
    xx=x+(j-2.5)*bayw*.12;pipe('upright carpet roll',(xx,-.21,.71),(xx,-.21,1.42+(j%3)*.13),.065,[cream,blue,paper][j%3],18);horizontal_ring('carpet roll fibre edge',xx,-.21,1.42+(j%3)*.13,.042,.010,paper)
   box('carpet swatch ledge',x-bayw*.40,x+bayw*.40,-.26,-.13,1.855,1.90,wood)
   for j in range(5):
    xx=x+(j-2)*bayw*.14
    for k in range(4):box('layered sample swatch',xx-.12,xx+.12,-.24,-.14,1.90+k*.018,1.916+k*.018,[paper,blue,cream,red][k])
   label('sample heading','CARPET SAMPLES',(x,-.25,2.58),min(.11,bayw/23),paper)
 route(cid+' retained pavement',[(-w/2+.45,-1.30,0),(w/2-.45,-1.30,0)])
 view('%02d_%s'%(idx+1,cid),(-w*.18,-4.1,1.6),(w*.08,-.15,1.55))
bpy.context.view_layer.update()
(dest/'review-views.json').write_text(json.dumps(views,indent=2));(dest/'local-routes.json').write_text(json.dumps(routes,indent=2))
(dest/'changes.json').write_text(json.dumps(dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),new_solids=[o.name for o in made],archived=retired,labels=labels,engine_implemented=False,scope='Catalogue-led business categories; original modelled display inventory, not observed product stock. Original opaque glazing/closed backing and entrance geometry retained.'),indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(out));print('V39_COMPLETE',len(made),len(retired),flush=True)
