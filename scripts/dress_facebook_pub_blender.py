"""Add newer walkthrough details to preserved v09; no engine conversion."""
from pathlib import Path
import ast,json,math,bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-video-details-v10.blend'
assert Path(bpy.data.filepath).name=='pharmacie-video-interior-v09.blend';assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v09-before-facebook-details.blend'),copy=True)
upper=bpy.data.collections['VIDEO | Upstairs furniture and decor - 2019 evidence']
lower=bpy.data.collections.new('VIDEO | Newer Facebook bar and room details')
for name in ('01 Ground floor - mapped rooms','03 Both floors - assembled exterior','05 Interior - photo-led dressing'):bpy.data.scenes[name].collection.children.link(lower)
made=[]
# Share tested modelling helpers without rerunning the earlier scene mutation.
tree=ast.parse((ROOT/'scripts/dress_video_pub_blender.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('mat','record','box','cyl','panel','update','leftx','rightx'):
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<video modelling helper>','exec'))
wood=bpy.data.materials['Video | dark timber'];black=bpy.data.materials['Video | black cabinet'];seat=bpy.data.materials['Video | brown banquette leather'];cream=bpy.data.materials['Video | warm cream trim'];silver=bpy.data.materials['Video | metal tread nosing']
textures={}
for item in json.loads((ROOT/'assets/video-references/facebook-18ZXq1yVKY/textures/manifest.json').read_text())['assets']:
 material=mat('Facebook '+item['name'],(.5,.5,.5));image=bpy.data.images.load(str(ROOT/item['file']),check_existing=True);image.pack();node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=image
 material.node_tree.links.new(node.outputs['Color'],material.node_tree.nodes['Principled BSDF'].inputs['Base Color']);textures[item['name']]=material
# Tall drinks fridge beside left end of bar, leaving passage along wall.
fx,fy=-1.2,15.98
box('tall beer fridge cabinet',(fx,fy,1.04),(.70,.62,2.08),black,lower)
for i,key in enumerate(('fridge-cans','fridge-bottles','fridge-cans','fridge-bottles')):
 z=.32+i*.40
 panel(f'fridge contents shelf {i}',[(fx-.29,fy-.319,z),(fx+.29,fy-.319,z),(fx+.29,fy-.319,z+.36),(fx-.29,fy-.319,z+.36)],textures[key],lower)
for dx in (-.325,.325):box('fridge door side',(fx+dx,fy-.33,1.10),(.055,.035,1.75),silver,lower)
box('fridge door header',(fx,fy-.33,1.98),(.69,.035,.08),black,lower)
box('fridge handle',(fx+.29,fy-.365,1.15),(.03,.055,.40),silver,lower)
box('fridge vent plinth',(fx,fy-.335,.15),(.64,.04,.23),black,lower)
for i in range(6):box('fridge ventilation slit',(fx,fy-.361,.065+i*.03),(.55,.012,.012),silver,lower)
# Tap bank is a separate backing on the left staff return; no invented doorway.
box('staff return tap backing',(.79,19.75,1.80),(1.66,.12,.86),black,lower)
panel('newer backbar tap-bank detail',[(-.01,19.68,1.40),(1.59,19.68,1.40),(1.59,19.68,2.19),(-.01,19.68,2.19)],textures['backbar-tap-bank'],lower)
# Face texture two existing pump badges by adding small editable surfaces.
for i,key in enumerate(('pump-mild','pump-original')):
 x=2.5+i*.7
 panel(key+' badge',[(x-.11,15.62,1.23),(x+.11,15.62,1.23),(x+.11,15.62,1.51),(x-.11,15.62,1.51)],textures[key],lower)
# New native photo detail inserts on downstairs wall, avoiding front windows.
for y,key,h in ((10.8,'dental-board',1.10),(12.3,'band-aid-advert',.95),(16.1,'medical-adverts',.50)):
 x=leftx(y)+.19;w=1.05 if key!='medical-adverts' else 2.25
 panel(key+' downstairs panel',[(x,y-w/2,1.30),(x,y+w/2,1.30),(x,y+w/2,1.30+h),(x,y-w/2,1.30+h)],textures[key],lower)
# Real chairs and tables: several newer views show dining chairs, not only stools.
def table_set(prefix,x,y,floor,col):
 cyl(prefix+' round tabletop',(x,y,floor+.775),.48,.065,wood,col)
 cyl(prefix+' pedestal',(x,y,floor+.40),.07,.70,black,col);cyl(prefix+' base',(x,y,floor+.045),.27,.07,black,col)
 for side in (-1,1):
  cx=x+side*1.05
  box(prefix+f' chair {side} seat',(cx,y,floor+.47),(.43,.43,.07),seat,col)
  box(prefix+f' chair {side} back',(cx+side*.19,y,floor+.77),(.055,.43,.57),wood,col)
  for dx,dy in ((-.16,-.16),(.16,-.16),(.16,.16),(-.16,.16)):box(prefix+' chair leg',(cx+dx,y+dy,floor+.235),(.032,.032,.43),wood,col)
for y in (6.7,10.2):table_set('downstairs dining '+str(y),4.5,y,0,lower)
for y in (11,16.3):table_set('upstairs centre dining '+str(y),4.8,y,4.8,upper)
# Large framed mirror observed upstairs: editable glass, never texture the camera operator.
mirror=mat('upstairs mirror',(.62,.64,.59),.07);bs=mirror.node_tree.nodes['Principled BSDF'];bs.inputs['Metallic'].default_value=.95
mx,my=rightx(10.3),10.3
box('upstairs gilt mirror backing',(mx,my,6.30),(.055,1.65,1.05),cream)
box('upstairs reflective mirror',(mx-.033,my,6.30),(.012,1.49,.89),mirror)
# Modelled back-bar mugs and glassware from newer closeups.
for i in range(8):
 cyl('backbar white mug',(0.2+i*.18,19.73,2.31),.065,.15,cream,lower,20)
 cyl('backbar glass',(0.2+i*.18,19.58,1.25),.045,.14,silver,lower,20)
update()
for o in made:o['evidence']='https://www.facebook.com/share/v/18ZXq1yVKY/'
# Planning labels stay visible in viewport but do not appear on photo-style renders.
for o in bpy.data.objects:
 if o.type=='FONT' and o.name.startswith('Room label |'):o.hide_render=True
for s in bpy.data.scenes:s['gameplay_version']='v10 - both video references, Blender only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'assets/blender/video-details-v10-manifest.json').write_text(json.dumps({'file':str(OUT),'new_objects':len(made),'new_packed_texture_crops':len(textures),'source':'https://www.facebook.com/share/v/18ZXq1yVKY/','placement':'Observed props with inferred world positions; door/stair/room structure retained','validation':'Visual render and static circulation audit; not BO3 tested','radiant_rebuilt':False},indent=2)+'\n')
result={'saved':str(OUT),'new_objects':len(made),'new_textures':len(textures)}
