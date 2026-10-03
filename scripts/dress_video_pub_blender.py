"""Video-led editable interior pass; preserve live v08 and leave BO3 alone."""
from pathlib import Path
import bpy, math, json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-video-interior-v09.blend'
assert Path(bpy.data.filepath).name=='pharmacie-backbar-photo-v08.blend'
assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v08-before-video-dressing.blend'),copy=True)
if bpy.context.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
def update():
 for s in bpy.data.scenes:
  for v in s.view_layers:v.update()
update()
upper=bpy.data.collections.new('VIDEO | Upstairs furniture and decor - 2019 evidence')
lower=bpy.data.collections.new('VIDEO | Downstairs display and stair finishes')
for name in ('02 First floor - mapped rooms','03 Both floors - assembled exterior'):bpy.data.scenes[name].collection.children.link(upper)
for name in ('01 Ground floor - mapped rooms','03 Both floors - assembled exterior','05 Interior - photo-led dressing'):bpy.data.scenes[name].collection.children.link(lower)
made=[]
def mat(name,color,rough=.7):
 m=bpy.data.materials.new('Video | '+name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough
 return m
wood=mat('dark timber',(.055,.027,.016));seat=mat('brown banquette leather',(.10,.052,.032),.45)
cream=mat('warm cream trim',(.68,.61,.43));black=mat('black cabinet',(.018,.020,.017));silver=mat('metal tread nosing',(.42,.44,.44),.32)
white=mat('piano ivory keys',(.80,.77,.62));carpet=mat('muted rose carpet',(.18,.07,.105))
bs=carpet.node_tree.nodes.get('Principled BSDF');noise=carpet.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=180
bump=carpet.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.17;bump.inputs['Distance'].default_value=.006
carpet.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);carpet.node_tree.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
textures={}
for item in json.loads((ROOT/'assets/video-references/q0zBpicUXjg/textures/manifest.json').read_text())['assets']:
 m=mat(item['name'],(.5,.5,.5));im=bpy.data.images.load(str(ROOT/item['file']),check_existing=True);im.pack()
 node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=im;m.node_tree.links.new(node.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color']);textures[item['name']]=m
def record(o,col):
 col.objects.link(o);o['evidence']='https://www.youtube.com/watch?v=q0zBpicUXjg';o['placement']='Approximate within current plan; historical 2019 decor';made.append(o);return o
def box(name,loc,size,material,col=upper):
 verts=[(loc[0]+a*size[0]/2,loc[1]+b*size[1]/2,loc[2]+c*size[2]/2) for a,b,c in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);mesh.materials.append(material);mesh.update()
 return record(bpy.data.objects.new('Video | '+name,mesh),col)
def cyl(name,loc,radius,depth,material,col=upper,n=32):
 verts=[(loc[0]+radius*math.cos(i*2*math.pi/n),loc[1]+radius*math.sin(i*2*math.pi/n),loc[2]+z*depth/2) for z in (-1,1) for i in range(n)]
 faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(material);me.update();return record(bpy.data.objects.new('Video | '+name,me),col)
def panel(name,coords,material,col=upper):
 me=bpy.data.meshes.new(name);me.from_pydata(coords,[],[(0,1,2,3)]);me.materials.append(material);me.update();uv=me.uv_layers.new()
 for idx,p in zip(me.polygons[0].loop_indices,((0,0),(1,0),(1,1),(0,1))):uv.data[idx].uv=p
 return record(bpy.data.objects.new('Video | '+name,me),col)
def leftx(y):return -2.01-(y-8)*.145+.34
def rightx(y):return 11.07-(y-6.7)*.059-.30
# Carpet only in open seating footprint: preserve kitchen, offices and stair void.
panel('upstairs seating carpet',[(-1.7,8.35,4.812),(10.25,8.35,4.812),(9.58,20.55,4.812),(-3.15,20.55,4.812)],carpet)
for side in ('left','right'):
 for i,y in enumerate((10.8,14.5,18.2)):
  x=leftx(y)+.34 if side=='left' else rightx(y)-.34
  box(f'{side} banquette {i+1} seat',(x,y,5.28),(.70,2.8,.18),seat)
  box(f'{side} banquette {i+1} base',(x,y,5.01),(.67,2.8,.38),wood)
  backx=x-.29 if side=='left' else x+.29
  box(f'{side} banquette {i+1} back',(backx,y,5.60),(.15,2.8,.60),seat)
  # Separate seat divisions and feet are editable.
  for yy in (y-.9,y,y+.9):box(f'{side} banquette seam {i+1} {yy:.1f}',(x,yy,5.375),(.65,.018,.012),wood)
  tx=x+1.05 if side=='left' else x-1.05
  cyl(f'{side} table {i+1} top',(tx,y,5.56),.50,.075,wood)
  cyl(f'{side} table {i+1} pedestal',(tx,y,5.18),.075,.68,black)
  cyl(f'{side} table {i+1} base',(tx,y,4.85),.30,.065,black)
  sx=tx+.87 if side=='left' else tx-.87
  for j,yy in enumerate((y-.56,y+.56)):
   cyl(f'{side} stool {i+1}.{j} cushion',(sx,yy,5.31),.22,.085,seat)
   for dx,dy in ((-.13,-.13),(.13,-.13),(.13,.13),(-.13,.13)):
    box(f'{side} stool {i+1}.{j} leg {dx} {dy}',(sx+dx,yy+dy,5.05),(.035,.035,.46),black)
# Dado, poster collages and TV along the side walls, away from doors.
for side in ('left','right'):
 for i,y in enumerate((10.7,14.4,18.1)):
  fn=leftx if side=='left' else rightx;x=fn(y)
  panel(f'{side} dark dado {i}',[(fn(y-1.65),y-1.65,4.85),(fn(y+1.65),y+1.65,4.85),(fn(y+1.65),y+1.65,5.85),(fn(y-1.65),y-1.65,5.85)],wood)
  for j,key in enumerate(('music-muddy-waters','music-elvis','music-chuck-berry','music-hit-parade')):
   yy=y-1.15+j*.76
   panel(f'{side} music poster {i}.{j}',[(fn(yy-.34),yy-.34,5.95),(fn(yy+.34),yy+.34,5.95),(fn(yy+.34),yy+.34,6.85),(fn(yy-.34),yy-.34,6.85)],textures[key])
box('upstairs television body',(rightx(14.4)-.06,14.4,6.49),(.14,1.35,.78),black)
box('upstairs television glass',(rightx(14.4)-.145,14.4,6.49),(.015,1.23,.66),mat('television glass',(.008,.014,.02),.12))
# Upright piano in rear-left seating corner, clear of WC doors and circulation.
px,py=-2.05,20.08
box('upright piano cabinet',(px,py,5.43),(1.48,.53,1.23),wood)
box('piano keyboard shelf',(px,py-.36,5.55),(1.44,.26,.10),wood)
for i in range(28):
 x=px-.66+i*.048
 box(f'piano ivory key {i}',(x,py-.39,5.612),(.045,.20,.022),white)
 if i%7 not in (2,6):box(f'piano black key {i}',(x+.023,py-.33,5.632),(.022,.105,.022),black)
box('piano bench',(px,py-.87,5.28),(.8,.32,.10),seat)
for x in (px-.31,px+.31):box('piano bench leg',(x,py-.87,5.04),(.05,.27,.43),wood)
box('vintage radio display shelf',(px,py,6.58),(1.9,.44,.06),black)
for i,key in enumerate(('radio-one','radio-two','radio-three','radio-four')):
 x=px-.70+i*.47;box(f'vintage radio {i+1} case',(x,py-.02,6.82),(.42,.28,.34),wood)
 panel(f'vintage radio {i+1} photo face',[(x-.20,py-.167,6.66),(x+.20,py-.167,6.66),(x+.20,py-.167,6.98),(x-.20,py-.167,6.98)],textures[key])
# Bookcase and stacked board games against left wall; position inferred.
by=17.6;bx=leftx(by)+.25
box('bookcase backing',(bx,by,6.02),(.09,1.40,1.85),black)
for z in (5.12,5.72,6.32,6.92):box(f'bookcase shelf {z}',(bx+.18,by,z),(.44,1.44,.045),black)
for i,z in enumerate((5.16,5.76,6.36)):
 panel(f'bookcase book spines {i}',[(bx+.415,by-.65,z),(bx+.415,by+.65,z),(bx+.415,by+.65,z+.48),(bx+.415,by-.65,z+.48)],textures['book-spines'])
for i in range(5):box(f'stacked board game {i}',(bx+.65,by-.35+i*.18,5.02+i*.07),(.5,.35,.065),cream if i%2 else wood)
# Dartboard generated as real circular sectors, not a perspective-distorted crop.
dy=12.6;dx=leftx(dy)+.04;dz=6.53
panel('dart cork backing',[(dx,dy-.5,dz-.55),(dx,dy+.5,dz-.55),(dx,dy+.5,dz+.55),(dx,dy-.5,dz+.55)],wood)
red=mat('dart red',(.35,.018,.012));green=mat('dart green',(.018,.13,.07))
for ring,(r0,r1) in enumerate(((.025,.14),(.14,.15),(.15,.25),(.25,.268),(.268,.30))):
 for i in range(20):
  a=(i/20)*2*math.pi;b=((i+1)/20)*2*math.pi
  coords=[(dx+.018,dy+rr*math.cos(ang),dz+rr*math.sin(ang)) for rr,ang in ((r0,a),(r1,a),(r1,b),(r0,b))]
  panel(f'dart sector {ring}.{i}',coords,(red if i%2 else green) if ring in (1,3) else (white if i%2 else black))
# Recessed-light appearance on open cutaway: individual trim discs, no ceiling obstruction.
for x in (1.4,5.8,8.4):
 for y in (10,14,18):cyl('upstairs recessed light trim',(x,y,7.72),.095,.025,cream)
# Retain actual stair geometry, add timber surface and thin metal nosings.
for o in list(bpy.data.objects):
 if o.type!='MESH' or not o.name.startswith('Stairs |') or 'tread' not in o.name:continue
 o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(wood)
 points=[o.matrix_world@v.co for v in o.data.vertices];lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
 if 'lower tread' in o.name:loc=(lo[0]+.03,(lo[1]+hi[1])/2,hi[2]+.005);size=(.055,hi[1]-lo[1],.01)
 else:loc=((lo[0]+hi[0])/2,hi[1]-.025,hi[2]+.005);size=(hi[0]-lo[0],.055,.01)
 box(o.name+' metal nosing',loc,size,silver,lower)
# Extra authentic medical board faces along downstairs display wall.
for i,(y,key) in enumerate(((7.3,'medical-board'),(14.6,'medical-detail'))):
 x=leftx(y)+.16
 panel(f'downstairs medical display {i}',[(x,y-.58,1.2),(x,y+.58,1.2),(x,y+.58,2.45),(x,y-.58,2.45)],textures[key],lower)
panel('rear beer poster', [(-4.00,26.45,1.1),(-4.00,27.10,1.1),(-4.00,27.10,2.02),(-4.00,26.45,2.02)],textures['corridor-beer'],lower)
update()
# Assertions establish intended placement rather than claiming engine collision checks.
assert all(not (o.name.startswith('Video |') and o.type=='MESH' and any((o.matrix_world@v.co).z<4.79 for v in o.data.vertices)) for o in upper.objects)
assert len(made)>250
for s in bpy.data.scenes:s['gameplay_version']='v09 - historical video decor, Blender only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'assets/blender/video-interior-v09-manifest.json').write_text(json.dumps({'file':str(OUT),'source_url':'https://www.youtube.com/watch?v=q0zBpicUXjg','user_choice':'Use video upstairs decor','new_objects':len(made),'packed_video_textures':len(textures),'placement':'Inferred positions within existing plan; structure and stair direction retained','radiant_rebuilt':False,'runtime_verified':False},indent=2)+'\n')
result={'saved':str(OUT),'new_objects':len(made),'textures':len(textures),'radiant_rebuilt':False}
