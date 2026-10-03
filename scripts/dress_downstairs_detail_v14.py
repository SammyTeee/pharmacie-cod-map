"""Second downstairs pass from inspected 06:35/07:29 video frames."""
from pathlib import Path
import bpy,ast,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-downstairs-details-v14.blend'
assert Path(bpy.data.filepath).name=='pharmacie-street-details-v13.blend';assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v13-before-downstairs-detail.blend'),copy=True)
lower=bpy.data.collections.new('VIDEO | Downstairs dense displays - second pass');upper=lower;made=[]
for name in ('01 Ground floor - mapped rooms','03 Both floors - assembled exterior','05 Interior - photo-led dressing'):bpy.data.scenes[name].collection.children.link(lower)
tree=ast.parse((ROOT/'scripts/dress_video_pub_blender.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('mat','record','box','cyl','panel','update'):exec(compile(ast.Module(body=[node],type_ignores=[]),'<detail helpers>','exec'))
update()
fixed=[]
for m in bpy.data.materials:
 if m.name.startswith(('Interior |','Blockout -')) and m.use_nodes:
  bs=m.node_tree.nodes.get('Principled BSDF')
  if bs and not bs.inputs['Base Color'].is_linked:
   bs.inputs['Base Color'].default_value=m.diffuse_color;fixed.append(m.name)
   if 'brass' in m.name:bs.inputs['Metallic'].default_value=.75
wood=bpy.data.materials['Video | dark timber'];black=bpy.data.materials['Video | black cabinet'];cream=bpy.data.materials['Video | warm cream trim'];metal=bpy.data.materials['Video | metal tread nosing']
glow=mat('display warm lamp',(.85,.65,.30));bs=glow.node_tree.nodes['Principled BSDF'];bs.inputs['Emission Color'].default_value=(1,.65,.24,1);bs.inputs['Emission Strength'].default_value=2.0
textures={}
for name in ('camera-cabinet','camera-adverts','medicine-adverts','medical-shelf'):
 m=mat('downstairs '+name,(.5,.5,.5));im=bpy.data.images.load(str(ROOT/'assets/video-references/q0zBpicUXjg/textures-downstairs'/f'{name}.png'),check_existing=True);im.pack();n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=im;m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color']);textures[name]=m
# Right wall line interpolated from current optical-display bounds. Keep all
# new display depth above seating and out of the centre/rear passage.
def rx(y):return 10.07-.032*(y-8)
for a,b in ((3.6,6.8),(9.2,13.0)):
 panel('right medical advert collage',[(rx(a)-.04,a,1.35),(rx(b)-.04,b,1.35),(rx(b)-.04,b,2.28),(rx(a)-.04,a,2.28)],textures['camera-adverts'])
 panel('right dark timber dado',[(rx(a)-.025,a,.35),(rx(b)-.025,b,.35),(rx(b)-.025,b,1.27),(rx(a)-.025,a,1.27)],wood)
 box('right dado top trim',(rx((a+b)/2)-.075,(a+b)/2,1.30),(.11,b-a,.06),wood)
for y in (5.15,11.1):
 x=rx(y)-.12
 box('camera display cabinet backing',(x,y,2.94),(.16,2.35,1.18),black)
 panel('vintage camera display contents',[(x-.09,y-1.11,2.40),(x-.09,y+1.11,2.40),(x-.09,y+1.11,3.48),(x-.09,y-1.11,3.48)],textures['camera-cabinet'])
 for z in (2.37,2.94,3.51):box('camera cabinet shelf',(x-.16,y,z),(.30,2.4,.055),wood)
 for yy in (y-1.18,y+1.18):box('camera cabinet side',(x-.16,yy,2.94),(.30,.055,1.18),wood)
 box('camera cabinet warm strip',(x-.20,y,3.44),(.04,2.17,.025),glow)
# Another layered medicine shelf and jars beside existing front-left shelf.
sx,sy=-1.53,4.38
box('lower pharmacy display shelf',(sx,sy,2.36),(.36,1.65,.055),wood)
for i in range(7):
 y=sy-.68+i*.22;h=.16+(i%3)*.055
 cyl('ceramic medicine jar',(sx+.04,y,2.40+h/2),.065,h,cream,n=16)
 cyl('medicine jar lid',(sx+.04,y,2.40+h+.015),.072,.025,black,n=16)
box('upper medicine display shelf',(-2.27,13.5,3.47),(.32,1.72,.055),wood)
for i in range(5):
 y=12.87+i*.30
 cyl('upper amber jar',(-2.23,y,3.62),.075,.24,bpy.data.materials['Interior | amber bottles'],n=16)
 cyl('upper jar cap',(-2.23,y,3.75),.08,.035,black,n=16)
# Small vintage instrument silhouette displayed above seating, not a floor prop.
box('medical instrument display plinth',(-2.18,13.1,2.66),(.31,.42,.06),wood)
cyl('instrument upright',(-2.13,13.1,2.89),.035,.43,metal,n=16)
box('instrument head',(-2.10,13.1,3.09),(.17,.22,.12),black)
# Visible ceiling-grid seams, timber flooring and warm bulbs seen throughout tour.
grid=mat('suspended ceiling grid',(.42,.40,.33))
for x in (-1, .2,1.4,2.6,3.8,5,6.2,7.4,8.6,9.8):box('ceiling longitudinal grid',(x,10.5,4.102),(.018,20.5,.018),grid)
for i in range(17):box('ceiling cross grid',(4.35,.65+i*1.2,4.10),(10.2,.018,.018),grid)
for o in list(bpy.data.collections['INTERIOR | Ceiling + pendants - hide for top view'].objects):
 if o.type=='MESH' and 'brass shade' in o.name:
  pts=[o.matrix_world@v.co for v in o.data.vertices];x=sum(p.x for p in pts)/len(pts);y=sum(p.y for p in pts)/len(pts)
  cyl('pendant warm diffuser',(x,y,3.505),.22,.015,glow,n=24)
floor=next(o for o in bpy.data.objects if o.name=='Ground | continuous timber floor')
m=mat('downstairs timber planks',(.27,.13,.05));nodes=m.node_tree.nodes;links=m.node_tree.links;bs=nodes['Principled BSDF'];coord=nodes.new('ShaderNodeTexCoord');brick=nodes.new('ShaderNodeTexBrick')
brick.inputs['Scale'].default_value=1;brick.inputs['Brick Width'].default_value=.18;brick.inputs['Row Height'].default_value=1.8;brick.inputs['Mortar Size'].default_value=.003;brick.inputs['Color1'].default_value=(.32,.16,.065,1);brick.inputs['Color2'].default_value=(.19,.075,.025,1);brick.inputs['Mortar'].default_value=(.065,.035,.02,1)
links.new(coord.outputs['Object'],brick.inputs['Vector']);links.new(brick.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.6
floor.data.materials.clear();floor.data.materials.append(m)
update();root=bpy.data.objects.get('GAMEPLAY | Pub scale 1.50 - frontage 10.5m')
if root is None:root=next(o for o in bpy.data.objects if o.type=='EMPTY' and o.name.startswith('GAMEPLAY |'))
for o in made:o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();o['evidence']='YouTube q0zBpicUXjg 06:35/07:29; Facebook 135–143s';o['placement']='Adapted to widened footprint; decorative wall/ceiling props, approximate'
update()
# New low objects are only wall dado; no added central floor furniture.
assert all(not (min((o.matrix_world@v.co).z for v in o.data.vertices)<2 and 1.5<sum((o.matrix_world@v.co).x for v in o.data.vertices)/len(o.data.vertices)<6) for o in made)
for w in bpy.context.window_manager.windows:
 w.scene=bpy.data.scenes['05 Interior - photo-led dressing']
 for a in w.screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.shading.type='SOLID';a.spaces.active.shading.color_type='TEXTURE';r=a.spaces.active.region_3d;eye=Vector((5.2,3.4,2.4));target=Vector((3,15.8,1.8));r.view_rotation=(target-eye).to_track_quat('-Z','Y');r.view_distance=8;r.view_location=eye+r.view_rotation@Vector((0,0,-8));r.view_perspective='PERSP'
for s in bpy.data.scenes:s['gameplay_version']='v14 - dense downstairs display pass; Blender only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'assets/blender/downstairs-v14-manifest.json').write_text(json.dumps({'file':str(OUT),'new_meshes':len(made),'corrected_materials':fixed,'new_texture_crops':4,'placement':'Reference-led approximate scenery, static centre-clear assertion passed; no engine validation','radiant_rebuilt':False},indent=2)+'\n')
result={'saved':str(OUT),'new_meshes':len(made),'corrected_materials':len(fixed)}
