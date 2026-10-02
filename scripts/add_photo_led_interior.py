"""Photo-led object placement and user-corrected staircase, saved as v03."""
from pathlib import Path
import ast
import json
import math
import hashlib
import bpy
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-photo-interior-v03.blend'
assert Path(bpy.data.filepath).name=='pharmacie-floorplan-blockout-v02.blend'
if OUT.exists():raise RuntimeError('Preserve v03 before regeneration')
scene=bpy.data.scenes['01 Ground floor - mapped rooms']
bpy.context.window.scene=scene
first_scene=bpy.data.scenes['02 First floor - mapped rooms']
assembled=bpy.data.scenes['03 Both floors - assembled exterior']
ground=next(c for c in scene.collection.children if c.name.startswith('BLOCKOUT | Ground floor rooms'))
first=next(c for c in first_scene.collection.children if c.name.startswith('BLOCKOUT | First floor rooms'))
stairs=next(c for c in scene.collection.children if c.name.startswith('BLOCKOUT | Continuous L stairs'))
S=7/316
STOREY=3.2
HEIGHT=2.9
EXT=.22
INT=.14
FF_X=316/327
FF_Y=934/1044
for variable,name in [('wallmat','Blockout - warm plaster'),('wood','Blockout - timber floor'),
                      ('door_mat','Blockout - doors'),('trim_mat','Blockout - dark shopfront trim'),
                      ('glass_mat','Blockout - window proxy blue'),('stair_mat','Blockout - provisional stairs'),
                      ('metal','Blockout - rails'),('label_mat','Blockout - labels')]:
    globals()[variable]=bpy.data.materials.get(name) or next(m for m in bpy.data.materials if m.name.startswith(name+'.'))
doors=[]
windows=[]
tree=ast.parse((ROOT/'scripts/model_evacuation_blockout.py').read_text(encoding='utf-8'))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'geometry_helpers','exec'),globals())
catalog=json.loads((ROOT/'assets/blender/photo-review/catalog.json').read_text(encoding='utf-8'))
by_id={p['id']:p for p in catalog}
records=[]

# The user established orientation: front head-on, rear exit is back LEFT.
# Approach that exit past the toilets; staircase starts to the RIGHT of it.
for obj in list(stairs.objects):bpy.data.objects.remove(obj,do_unlink=True)
for obj in list(first.objects):
    if obj.name=='First | floor with L stairwell opening':bpy.data.objects.remove(obj,do_unlink=True)
OUTLINE_F=[(76,558),(172,566),(346,567),(1096,501),(1120,828),(813,856),(813,865),(302,885),(76,885)]
# Contextual boolean operations run in the first-floor scene, with its collection linked.
bpy.context.window.scene=first_scene
upper=slab('First | floor with corrected L stairwell opening',OUTLINE_F,1,first)
START=Vector((.85,19.85,0))
CORNER=Vector((4.78,19.85,0))
END=Vector((4.78,16.95,0))
W=.94
N1,N2=10,8
R=STOREY/18
D1=(CORNER-START).normalized()
D2=(END-CORNER).normalized()
RUN1=(CORNER-START).length-W/2
RUN2=(END-CORNER).length-W/2
for i in range(N1):
    tread=RUN1/N1
    p=START+D1*(i+.5)*tread
    box(f'Stairs | across-back lower tread {i+1:02}',(p.x,p.y,(i+1)*R/2),(tread,W,(i+1)*R),stairs,stair_mat)
box('Stairs | RIGHT turn landing',(CORNER.x,CORNER.y,N1*R/2),(W,W,N1*R),stairs,stair_mat)
for i in range(N2):
    tread=RUN2/N2
    p=CORNER+D2*(W/2+(i+.5)*tread)
    height=(N1+i+1)*R
    box(f'Stairs | right-turn upper tread {i+1:02}',(p.x,p.y,height/2),(W,tread,height),stairs,stair_mat)
box('Stairs | upper arrival landing',(END.x,END.y-.30,STOREY-.09),(W,.60,.18),stairs,stair_mat)
for name,center,dims in [
    ('across-back opening',((START.x+CORNER.x)/2,START.y,STOREY),((CORNER-START).length+W+.08,W+.08,1)),
    ('right-turn opening',(CORNER.x,(CORNER.y+END.y)/2,STOREY),(W+.08,(CORNER-END).length+W/2+.08,1))]:
    cutter=box('Temporary stair void',center,dims,first,stair_mat)
    bpy.ops.object.select_all(action='DESELECT')
    upper.select_set(True)
    bpy.context.view_layer.objects.active=upper
    modifier=upper.modifiers.new(name,'BOOLEAN')
    modifier.operation='DIFFERENCE'
    modifier.solver='EXACT'
    modifier.object=cutter
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
def rail(name,a,b):
    d=b-a
    o=box(name,(a+b)/2,(.05,.05,d.length),stairs,metal)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
for sign in (-1,1):
    rail('Stairs | lower sloped rail',START+Vector((0,sign*W/2,.9)),CORNER-D1*(W/2)+Vector((0,sign*W/2,N1*R+.9)))
    rail('Stairs | upper sloped rail',CORNER+D2*(W/2)+Vector((sign*W/2,0,N1*R+.9)),END+Vector((sign*W/2,0,STOREY+.9)))

# Store wall adjustment is small and explicit: the stair opening approaches its
# outer edge; shorten the rear store by 12 cm to preserve a clear upper corridor.
for o in list(first.objects):
    if o.name.startswith('First | rear store bottom'):
        o.location.x-=.12
    if o.name.startswith('First | rear store rear | wall end'):
        o.location.x-=.06
        for v in o.data.vertices:
            if v.co.x>0:v.co.x-=.12
bpy.context.window.scene=scene
props=bpy.data.collections.new('INTERIOR | Photo-led editable objects')
scene.collection.children.link(props)
assembled.collection.children.link(props)
decor=bpy.data.collections.new('INTERIOR | Photo wall surfaces + display cases')
scene.collection.children.link(decor)
assembled.collection.children.link(decor)
ceiling=bpy.data.collections.new('INTERIOR | Ceiling + pendants - hide for top view')
scene.collection.children.link(ceiling)
assembled.collection.children.link(ceiling)

brown=material('Interior | brown upholstery',(.13,.066,.035))
brass=material('Interior | brass',(.55,.36,.10))
cream=material('Interior | cream chairs',(.78,.73,.61))
bone=material('Interior | skeleton placeholder bone',(.78,.72,.52))
black=material('Interior | dark cabinet',(.035,.029,.024))
greyglass=material('Interior | glass tabletop proxy',(.41,.56,.57))
tile=material('Interior | ceiling tiles',(.73,.72,.66))
red=material('Interior | red stool frames',(.39,.06,.045))
amber=material('Interior | amber bottles',(.37,.19,.038))
blue=material('Interior | blue bottles',(.05,.19,.36))

def group(name,xy,sources,observed,confidence='medium',c=props):
    root=bpy.data.objects.new(name,None)
    c.objects.link(root)
    root.location=(*xy,0)
    root.empty_display_type='PLAIN_AXES'
    root.empty_display_size=.15
    root['sources']='; '.join(by_id[i]['source'] for i in sources)
    root['observation']=observed
    root['placement_confidence']=confidence
    root['status']='Editable photo-inspired prototype; dimensions estimated'
    records.append({'object':name,'xy_m':list(xy),'source_ids':sources,'observation':observed,'placement_confidence':confidence})
    return root

def part(parent,name,location,dims,mat,c=props):
    o=box(parent.name+' | '+name,location,dims,c,mat)
    o.parent=parent
    # Coordinates are deliberately local to the group, making placement editable.
    return o

def cylinder(parent,name,loc,radius,depth,mat,c=props):
    bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=radius,depth=depth,location=(0,0,0))
    o=bpy.context.object
    o.name=parent.name+' | '+name
    for owner in list(o.users_collection):owner.objects.unlink(o)
    c.objects.link(o)
    o.parent=parent
    o.location=loc
    o.data.materials.append(mat)
    o.color=mat.diffuse_color
    return o

def sphere(parent,name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(0,0,0))
    o=bpy.context.object
    o.name=parent.name+' | '+name
    for owner in list(o.users_collection):owner.objects.unlink(o)
    props.objects.link(o)
    o.parent=parent
    o.location=loc
    # Mesh dimensions, not an unapplied object scale.
    for v in o.data.vertices:
        v.co.x*=scale[0];v.co.y*=scale[1];v.co.z*=scale[2]
    o.data.materials.append(mat)
    o.color=mat.diffuse_color
    return o

def leftwall(y):return .133 if y<=6.27 else .133-(y-6.27)*1.573/14.20

def table(name,xy,medical=True,base=0):
    g=group(name,xy,[2,19,21,22],'Glass-topped medical cabinet/trolley used as pub table' if medical else 'Small square pub table')
    topmat=greyglass if medical else wood
    part(g,'tabletop',(0,0,base+.77),(.68,1.08,.045),topmat)
    if medical:
        part(g,'lower shelf',(0,0,base+.25),(.61,1.00,.045),cream)
        part(g,'drawer body',(0,0,base+.64),(.57,.48,.16),cream)
    for x in (-.27,.27):
        for y in (-.46,.46):
            part(g,'leg',(x,y,base+.38),(.034,.034,.72),metal)
            if medical:cylinder(g,'small caster',(x,y,base+.075),.045,.045,black)
    return g

def stool(name,xy,base=0,high=False):
    g=group(name,xy,[2,3,19,20,21,22],'Round dark stools / red metal-framed high stools')
    h=.72 if high else .47
    cylinder(g,'round seat',(0,0,base+h),.20,.065,brown)
    for x in (-.13,.13):
        for y in (-.13,.13):part(g,'leg',(x,y,base+h/2),(.035,.035,h),red if high else black)
    return g

platform=group('Raised right-hand seating platform',(5.53,5.4),[3,19,20],'Raised carpeted area on right when facing bar',confidence='high')
part(platform,'platform slab',(0,0,.09),(2.03,6.4,.18),brown)
for y in (2.65,5.1,7.7):
    table(f'Platform | medical table {y}',(5.53,y),base=.18)
    stool(f'Platform | high stool {y} A',(4.94,y-.62),base=.18,high=True)
    stool(f'Platform | high stool {y} B',(6.05,y+.61),base=.18,high=True)
for y in (2.6,9.0):
    table(f'Left-side | medical table {y}',(1.35,y))
    stool(f'Left-side | stool {y} A',(1.35,y-.72))
    stool(f'Left-side | stool {y} B',(1.35,y+.72))

for index,y in enumerate((4.5,6.0),1):
    sofa=group(f'Left wall | sofa section {index}',(leftwall(y)+.65,y),[9,10,22],'Brown sofa seating along pharmacy display wall',confidence='high')
    part(sofa,'seat base',(0,0,.30),(.87,1.35,.34),brown)
    part(sofa,'seat cushion',(.08,0,.52),(.78,1.21,.18),brown)
    part(sofa,'back',(-.35,0,.82),(.20,1.34,.75),brown)
    for side in (-1,1):part(sofa,'arm',(.03,side*.64,.68),(.87,.15,.43),brown)
    for side in (-1,1):part(sofa,'feet',(0,side*.5,.09),(.65,.08,.18),black)

dentist=group('Left wall | dentist chair + skeleton placeholder',(leftwall(7.7)+.69,7.7),[4,9,10,22],'Skeleton seated in black dentist chair beside sofa',confidence='high')
part(dentist,'chair base',(0,0,.08),(.82,.65,.12),metal)
cylinder(dentist,'pedestal',(0,0,.32),.12,.48,metal)
part(dentist,'seat',(.02,0,.58),(.56,.60,.14),black)
part(dentist,'back',(-.24,0,.97),(.15,.61,.85),black)
part(dentist,'headrest',(-.22,0,1.43),(.16,.36,.22),black)
part(dentist,'footrest',(.43,0,.27),(.46,.50,.10),metal)
for side in (-1,1):part(dentist,'armrest',(.03,side*.35,.85),(.45,.09,.10),black)
def bone_link(name,a,b,r=.018):
    a,b=Vector(a),Vector(b)
    o=cylinder(dentist,name,(a+b)/2,r,(b-a).length,bone)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    return o
sphere(dentist,'skull',(-.02,0,1.46),(.12,.105,.15),bone)
for side in (-1,1):sphere(dentist,'eye socket',(.08,side*.043,1.48),(.018,.027,.032),black)
part(dentist,'jaw',(.028,0,1.355),(.12,.15,.065),bone)
bone_link('spine',(-.10,0,.69),(-.08,0,1.31),.027)
bone_link('shoulders',(-.04,-.23,1.23),(-.04,.23,1.23),.019)
for level in range(6):
    z=.93+level*.049
    # Deliberately simple rib proxy, tagged as a placeholder rather than finished art.
    bone_link(f'rib left {level}',(-.07,0,z),(.02,-(.14-level*.008),z+.026),.009)
    bone_link(f'rib right {level}',(-.07,0,z),(.02,(.14-level*.008),z+.026),.009)
for side in (-1,1):
    bone_link('upper arm',(-.04,side*.23,1.23),(.02,side*.30,.95))
    bone_link('forearm',(.02,side*.30,.95),(.29,side*.28,.83))
    sphere(dentist,'hand',(.29,side*.28,.83),(.07,.035,.02),bone)
    bone_link('thigh',(.02,side*.10,.66),(.39,side*.12,.58),.026)
    bone_link('shin',(.39,side*.12,.58),(.43,side*.12,.30),.023)
    bone_link('foot',(.43,side*.12,.30),(.58,side*.12,.27),.023)
    sphere(dentist,'knee',(.39,side*.12,.58),(.035,.035,.035),bone)

for index,(x,y) in enumerate(((1.72,7.55),(1.72,8.45)),1):
    g=group(f'Dentist seating | cream bucket chair {index}',(x,y),[10,22],'Cream curved bucket chairs next to dentist chair')
    cylinder(g,'round seat',(0,0,.48),.25,.08,cream)
    part(g,'back',(.20,0,.72),(.10,.46,.43),cream)
    for side in (-1,1):part(g,'arm',(0,side*.22,.63),(.38,.075,.23),cream)
    for xoff in (-.16,.16):
        for yoff in (-.16,.16):part(g,'leg',(xoff,yoff,.22),(.025,.025,.44),metal)
table('Dentist seating | low coffee table',(1.37,5.30),medical=False)

# Photo surfaces sample originals through UV coordinates. No image files changed.
photo_materials={}
def photo_panel(name,verts,source,crop=None,c=decor):
    if source not in photo_materials:
        imagepath=ROOT/'references/pharmacie-syston'/source
        if source=='great for texture.avif':
            imagepath=ROOT/'assets/blender/photo-review/feature-wall-lossless.png'
        image=bpy.data.images.load(str(imagepath),check_existing=True)
        image.pack()
        m=bpy.data.materials.new('Interior photo | '+source[:50])
        m.use_nodes=True
        texture=m.node_tree.nodes.new('ShaderNodeTexImage')
        texture.image=image
        m.node_tree.nodes.active=texture
        m.node_tree.links.new(texture.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
        m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.7
        photo_materials[source]=(m,image)
    mat,image=photo_materials[source]
    o=mesh_obj(name,verts,[(0,1,2,3)],c,mat)
    uv=o.data.uv_layers.new(name='UV_Original_Photo')
    width,height=image.size
    a,b,d,e=crop or (0,0,width,height)
    coords=[(a/width,1-b/height),(d/width,1-b/height),(d/width,1-e/height),(a/width,1-e/height)]
    for loop,value in zip(o.data.loops,coords):uv.data[loop.index].uv=value
    o.data.uv_layers.active_index=len(o.data.uv_layers)-1
    uv.active_render=True
    o['source']=source
    o['source_pixel_crop']=list(crop or (0,0,width,height))
    return o

start_y,end_y=3.05,8.55
split_y=6.27
split_pixel=round((split_y-start_y)/(end_y-start_y)*1973)
for i,(a,b,lo,hi) in enumerate([(start_y,split_y,0,split_pixel),(split_y,end_y,split_pixel,1973)],1):
    photo_panel(f'Left wall | pharmacy display backing segment {i}',[
        (leftwall(a)+.13,a,2.73),(leftwall(b)+.13,b,2.73),
        (leftwall(b)+.13,b,.98),(leftwall(a)+.13,a,.98)],'great for texture.avif',(lo,0,hi,1227))
for index,(y,length) in enumerate(((5.82,1.35),(7.23,1.35)),1):
    g=group(f'Left wall | framed medicine cabinet {index}',(leftwall(y)+.17,y),[2,12,20,21,22],'Paired lit wall cases contain bottles',confidence='high',c=decor)
    for offset in (-length/2,length/2):part(g,'cabinet side',(.10,offset,1.93),(.24,.055,.88),black,c=decor)
    for z in (1.49,1.93,2.37):part(g,'shelf / frame',(.10,0,z),(.24,length,.04),black,c=decor)
    part(g,'warm strip light',(.105,0,2.33),(.15,length-.1,.024),brass,c=decor)

for index,y in enumerate((2.9,9.0),1):
    g=group(f'Left wall | pharmacy shelf {index}',(leftwall(y)+.27,y),[1,5,17,22],'Black shelves with medicine bottles, jars and medical objects')
    part(g,'shelf',(.05,0,1.95),(.32,1.2,.065),black)
    for j in range(6):
        cylinder(g,'medicine bottle',(.06,-.48+j*.18,2.09),.044,.23,amber if j%2 else blue)
        cylinder(g,'bottle neck',(.06,-.48+j*.18,2.24),.020,.07,black)

# Right wall advert/instrument board: actual photo surface + projecting board.
g=group('Right platform | optical instrument display',(6.55,5.5),[17,20,21],'Cream instrument boards above perimeter seating',c=decor)
part(g,'cream display board',(-.02,0,1.97),(.12,1.15,.95),cream,c=decor)
photo_panel('Right platform | instrument photo face',[(6.47,6.08,2.43),(6.47,4.92,2.43),(6.47,4.92,1.52),(6.47,6.08,1.52)],'textures wall.jpg',(42,180,420,520))

# Preserve the U bar from the floor plan, adding the observed drawer frontage,
# central screen, tap pumps and bottle shelves without inventing new rooms.
photo_panel('Bar | drawer-front photo face',[(1.28,10.235,1.01),(5.49,10.235,1.01),(5.49,10.235,.035),(1.28,10.235,.035)],'bar front.jpg',(50,745,1900,1230))
g=group('Bar | taps and counter dressing',(3.34,10.54),[6,23],'Brass beer pump row and black counter',confidence='high')
for i in range(5):
    x=-1.25+i*.56
    cylinder(g,'pump brass base',(x,0,1.15),.075,.08,brass)
    cylinder(g,'pump stem',(x,0,1.34),.023,.35,brass)
    part(g,'dark pump handle',(x,.02,1.48),(.05,.07,.20),black)
    cylinder(g,'pump badge',(x,-.05,1.42),.065,.026,cream)

g=group('Bar | backbar shelves and screen',(3.3,13.62),[6,23],'Central screen flanked by bottles and ornaments',confidence='high')
part(g,'screen body',(0,-.08,2.05),(1.45,.13,.86),black)
part(g,'screen glass',(0,-.155,2.05),(1.31,.022,.71),glass_mat)
for z in (1.29,1.73,2.56):
    part(g,'long shelf',(0,0,z),(4.1,.36,.06),black)
    if z!=1.73:
        for i in range(16):
            x=-1.84+i*.24
            cylinder(g,'bottle body',(x,-.04,z+.15),.043,.24,amber if i%3 else blue)
            cylinder(g,'bottle neck',(x,-.04,z+.30),.020,.07,black)

# Removable ceiling and practical lamps, useful for photo comparison. Ceiling
# is hidden for cutaway; pendant geometry stays visible.
roof_mesh=slab('Interior | removable suspended ceiling',[(82,85),(365,91),(760,151),(760,372),(284,401),(82,401)],0,ceiling,tile)
roof_mesh.location.z=2.92
roof_mesh.hide_set(True)
roof_mesh.hide_render=True
for i,(x,y) in enumerate([(3.35,2.8),(3.35,5.4),(3.35,8.1),(2.1,10.5),(4.5,10.5)],1):
    g=group(f'Lighting | pendant {i}',(x,y),[3,5,6,19,22,23],'Brass conical pendants under suspended tile ceiling',c=ceiling)
    cylinder(g,'cord',(0,0,2.73),.010,.34,black,c=ceiling)
    bpy.ops.mesh.primitive_cone_add(vertices=20,radius1=.23,radius2=.07,depth=.22,location=(0,0,0))
    lamp=bpy.context.object
    lamp.name=g.name+' | brass shade'
    for owner in list(lamp.users_collection):owner.objects.unlink(lamp)
    ceiling.objects.link(lamp)
    lamp.parent=g
    lamp.location=(0,0,2.44)
    lamp.data.materials.append(brass)
    lamp.color=brass.diffuse_color

# Direction markings are reference overlays, excluded from render.
for text,pixel in [('REAR LEFT EXIT',(1000,60)),('STAIRS START / UP',(985,145))]:
    o=room_label(text,pixel,0,ground,.18)
    o.hide_render=True
for o in first.objects:
    if o.type=='FONT' and 'POSITION PROVISIONAL' in o.data.body:
        o.data.body='L STAIRS\nRIGHT TURN'

interior_scene=bpy.data.scenes.new('05 Interior - photo-led dressing')
for c in (ground,props,decor,ceiling,stairs):interior_scene.collection.children.link(c)
for prefix in ('BLOCKOUT | Frontage','BLOCKOUT | Upper frontage'):
    c=next(c for c in assembled.collection.children if c.name.startswith(prefix))
    interior_scene.collection.children.link(c)
    if prefix=='BLOCKOUT | Upper frontage' and c.name not in first_scene.collection.children:
        first_scene.collection.children.link(c)
interior_scene.unit_settings.system='METRIC'
configure(interior_scene,'Interior overview camera',(3.3,10,1.1),(17,-8,30),33)
interior_scene.display.shading.color_type='TEXTURE'
configure(scene,'Updated ground overview',(3.0,10,0),(16,-2,35),33)
scene.display.shading.color_type='TEXTURE'
for s in (assembled,first_scene):s.display.shading.color_type='TEXTURE'
first_scene.camera.location=(16,-2,39)
first_scene.camera.rotation_euler=(Vector((3.2,10,STOREY))-first_scene.camera.location).to_track_quat('-Z','Y').to_euler()
first_scene.camera.data.ortho_scale=33
bpy.context.window.scene=interior_scene
for s in (scene,assembled,interior_scene):
    roof_mesh.hide_set(True,view_layer=s.view_layers[0])
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active
            space.shading.type='SOLID'
            space.shading.color_type='TEXTURE'
            space.region_3d.view_rotation=interior_scene.camera.rotation_euler.to_quaternion()
            space.region_3d.view_perspective='ORTHO'
            space.region_3d.view_location=(3.3,10,1.1)
            space.region_3d.view_distance=32

manifest=json.loads((OUT.parent/'floorplan-blockout-v02-manifest.json').read_text(encoding='utf-8'))
manifest['file']=OUT.name
manifest['stairs']={'user_confirmed':'Rear-left outside exit when facing building head-on; past toilets, stairs start on your right; up then right',
    'start':list(START),'turn':list(CORNER),'arrival':list(END),'direction':'Lower +X across back; clockwise right turn to -Y towards street',
    'risers':18,'riser_m':R,'width_assumed_m':W,'lower_tread_m':RUN1/N1,'upper_tread_m':RUN2/N2,
    'assumptions':'Storey height 3.2m; approximate endpoints; upper rear store shortened 0.12m'}
manifest['interior_objects']=records
manifest['photo_review']='28 reference images reviewed, including 2 layout drawings; WhatsApp sources are partly duplicates/alternate encodings'
manifest['scenes'].append(interior_scene.name)
manifest['limitations'].extend(['Interior placements inferred from photo sightlines, not measured','Skeleton is a simple 3D placeholder, not finished character art','No interior photo evidence for upstairs, service rooms or stairs themselves'])
(OUT.parent/'photo-interior-v03-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
assert all(hashlib.sha256((ROOT/'references/pharmacie-syston'/p['source']).read_bytes()).hexdigest()==p['sha256'] for p in catalog)
assert abs(N1*R+N2*R-STOREY)<1e-8
assert D1.cross(D2).z<0  # verified clockwise right turn in world XY
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
for s,filename in [(interior_scene,'photo-interior-v03.png'),(scene,'ground-floor-v03.png'),(first_scene,'first-floor-v03.png')]:
    s.render.filepath=str(OUT.parent/filename)
    bpy.ops.render.render(write_still=True,scene=s.name)
result={'file':str(OUT),'photo_led_groups':len(records),'source_hashes_unchanged':len(catalog),
        'stairs':'Rear left door; lower across back then clockwise right towards front','preview':str(OUT.parent/'photo-interior-v03.png')}
