"""Layered small props from video displays; preserve all circulation."""
from pathlib import Path
import bpy,ast,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-detailed-pub-v15.blend'
assert Path(bpy.data.filepath).name=='pharmacie-downstairs-details-v14.blend';assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v14-before-small-props.blend'),copy=True)
lower=bpy.data.collections['VIDEO | Downstairs dense displays - second pass'];upper=lower;made=[]
tree=ast.parse((ROOT/'scripts/dress_video_pub_blender.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('mat','record','box','cyl','panel','update'):exec(compile(ast.Module(body=[node],type_ignores=[]),'<props helpers>','exec'))
wood=bpy.data.materials['Video | dark timber'];black=bpy.data.materials['Video | black cabinet'];cream=bpy.data.materials['Video | warm cream trim'];metal=bpy.data.materials['Video | metal tread nosing'];brass=bpy.data.materials['Interior | brass'];glass=mat('smoky glassware',(.27,.32,.28),.15)
adverts=bpy.data.materials['Video | downstairs medicine-adverts']
for a,b in ((3.4,5.55),(12.85,14.5)):
 def lx(y):return -1.89-(y-3.4)*.10
 panel('additional left medicine collage',[(lx(a)+.04,a,1.20),(lx(b)+.04,b,1.20),(lx(b)+.04,b,2.20),(lx(a)+.04,a,2.20)],adverts)
# Camera silhouettes in foreground of photograph: cases, silver lenses and knobs.
for y in (4.35,5.03,5.72,10.3,11,11.7):
 x=9.79-.032*(y-8)
 box('vintage camera body',(x,y,2.60),(.13,.29,.19),black)
 lens=cyl('camera silver lens',(0,0,0),.062,.075,metal,n=20)
 # Cylinders point along X toward room. Their mesh was built at origin.
 lens.rotation_euler[1]=math.pi/2;lens.location=(x-.105,y,2.60)
 box('camera viewfinder',(x,y-.07,2.72),(.08,.075,.035),metal)
# Ceramic display pots and small specimen boxes on upper right shelf.
for i in range(6):
 y=9.55+i*.52;x=9.82-.032*(y-8)
 box('ceramic display shelf',(x,y,3.71),(.30,.49,.035),wood)
 cyl('white ceramic display vessel',(x-.02,y,3.82),.09,.18,cream,n=20)
 cyl('ceramic vessel rim',(x-.02,y,3.915),.102,.024,cream,n=20)
 box('vintage medicine carton',(x,y+.17,3.80),(.12,.09,.14),cream)
# Small stands/coasters are on existing tables, not in walking routes.
for x,y,z in ((4.5,6.7,.81),(4.5,10.2,.81),(7.97,4.88,1.055),(8.08,7.65,1.055),(8.13,11.55,1.055)):
 cyl('table drinks coaster',(x+.18,y,z+.008),.065,.006,cream,n=16)
 cyl('table tumbler',(x+.18,y,z+.065),.047,.11,glass,n=16)
 box('table menu stand foot',(x-.17,y,z+.02),(.18,.09,.025),black)
 box('table menu stand',(x-.17,y,z+.15),(.15,.025,.24),cream)
# Counter service details visible around hand pumps in both videos.
for x in (.50,6.5,7.15):
 box('counter drip tray',(x,15.80,1.115),(.42,.24,.025),black)
 for i in range(6):box('drip tray silver slot',(x-.16+i*.064,15.80,1.131),(.015,.19,.008),metal)
box('counter menu holder',(6.35,15.70,1.29),(.24,.05,.36),black)
panel('counter beer menu insert',[(6.245,15.669,1.13),(6.455,15.669,1.13),(6.455,15.669,1.45),(6.245,15.669,1.45)],bpy.data.materials['Video | corridor-beer'])
# Three framed entrance notices, as seen in YouTube 07:09–07:12.
for i in range(3):
 y=3.45+i*.42;x=10.06
 box('entrance notice black frame',(x,y,2.53),(.045,.30,.38),black)
 box('entrance notice cream insert',(x-.025,y,2.53),(.012,.26,.33),cream)
# Clock with individually modelled hands above left-side shelves.
cx,cy,cz=-1.63,4.34,3.72
o=cyl('display wall clock',(0,0,0),.19,.04,black,n=32);o.rotation_euler[1]=math.pi/2;o.location=(cx,cy,cz)
o=cyl('clock cream face',(0,0,0),.17,.012,cream,n=32);o.rotation_euler[1]=math.pi/2;o.location=(cx+.025,cy,cz)
box('clock minute hand',(cx+.04,cy,cz+.065),(.008,.012,.135),black)
box('clock hour hand',(cx+.045,cy-.04,cz+.015),(.008,.09,.012),black)
update();root=bpy.data.objects['GAMEPLAY | Pub scale 1.50 - frontage 10.5m']
for o in made:
 world=o.matrix_world.copy();o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();o.matrix_world=world
 o['evidence']='YouTube 06:14–07:32, Facebook 61–143s';o['placement']='Approximate small decorative props; no new floor furniture'
update()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'assets/blender/downstairs-v15-manifest.json').write_text(json.dumps({'file':str(OUT),'additional_meshes':len(made),'details':'Camera cases/lenses, ceramics/cartons, glasses/coasters/menu holders, counter drip trays, entrance notices, clock, extra collage','radiant_rebuilt':False},indent=2)+'\n')
result={'saved':str(OUT),'additional_meshes':len(made)}
