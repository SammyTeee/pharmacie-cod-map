"""Photo-led 3D shopfront revision; keep the original blockout file intact."""
from pathlib import Path
import ast
import math
import json
import hashlib
import bpy
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-floorplan-blockout-v02.blend'
if OUT.exists():
    raise RuntimeError('v02 already exists; preserve it before regeneration')
scene=bpy.data.scenes['01 Ground floor - mapped rooms']
bpy.context.window.scene=scene
ground=next(c for c in scene.collection.children if c.name.startswith('BLOCKOUT | Ground floor rooms'))
first_scene=bpy.data.scenes['02 First floor - mapped rooms']
first=next(c for c in first_scene.collection.children if c.name.startswith('BLOCKOUT | First floor rooms'))
assembled=bpy.data.scenes['03 Both floors - assembled exterior']
front=next(c for c in scene.collection.children if c.name.startswith('BLOCKOUT | Frontage'))
upper=next(c for c in assembled.collection.children if c.name.startswith('BLOCKOUT | Upper frontage'))
S=7/316
STOREY=3.2
HEIGHT=2.9
EXT=.22
INT=.14
FF_X=316/327
FF_Y=934/1044
for variable,name in [('wallmat','Blockout - warm plaster'),('wood','Blockout - timber floor'),
                      ('brick','Blockout - frontage brick'),('trim_mat','Blockout - dark shopfront trim'),
                      ('glass_mat','Blockout - window proxy blue'),('door_mat','Blockout - doors')]:
    globals()[variable]=bpy.data.materials[name]
doors=[]
windows=[]
# Reuse project-owned geometry/UV helpers without rerunning the scene generator.
tree=ast.parse((ROOT/'scripts/model_evacuation_blockout.py').read_text(encoding='utf-8'))
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
exec(compile(ast.Module(body=functions,type_ignores=[]),'geometry_helpers','exec'),globals())

def delete_generated(collection,predicate):
    for o in list(collection.objects):
        if predicate(o.name):
            bpy.data.objects.remove(o,do_unlink=True)

delete_generated(front,lambda n:n.startswith('Front |') and n!='Front | forecourt')
delete_generated(upper,lambda n:n.startswith('Front |'))
delete_generated(ground,lambda n:any(n.startswith(f'Ground shell {i:02}') for i in range(8,15)))
delete_generated(first,lambda n:n.startswith('First shell 08'))

# Strengthen the full shared divider; no toilet-to-toilet door is present.
delete_generated(first,lambda n:n.startswith('First | toilets middle'))
wall('First | MEN / WOMEN solid divider - NO connecting door',(774,698),(945,686),1)
for hinge in first.objects:
    if hinge.name.startswith('First | toilets front | door') and hinge.name.endswith('hinge'):
        # Open towards the common seating side, making the separate entries clear.
        hinge.rotation_euler.z=-math.radians(72)

photo=ROOT/'references/pharmacie-syston/pharmacie-arms-syston-2.jpg'
image=bpy.data.images.load(str(photo),check_existing=True)
image.pack()
assert tuple(image.size)==(1024,751)
photo_mat=bpy.data.materials.new('Frontage photo | original packed source, UV crops')
photo_mat.use_nodes=True
photo_mat.diffuse_color=(.065,.075,.075,1)
nodes=photo_mat.node_tree.nodes
tex=nodes.new('ShaderNodeTexImage')
tex.image=image
tex.interpolation='Linear'
nodes.active=tex
shader=nodes.get('Principled BSDF')
photo_mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
shader.inputs['Roughness'].default_value=.62

def panel(name,a,b,bottom,top,crop,c=front,parent=None):
    x0,y0,x1,y1=crop
    # Top-left/right followed by bottom-right/left; image coordinates untouched.
    verts=[(a[0],a[1],top),(b[0],b[1],top),(b[0],b[1],bottom),(a[0],a[1],bottom)]
    o=mesh_obj(name,verts,[(0,1,2,3)],c,photo_mat)
    uv=o.data.uv_layers.new(name='UV_Source_Photo')
    coords=[(x0/1024,1-y0/751),(x1/1024,1-y0/751),(x1/1024,1-y1/751),(x0/1024,1-y1/751)]
    for loop,coord in zip(o.data.loops,coords):uv.data[loop.index].uv=coord
    o.data.uv_layers.active_index=len(o.data.uv_layers)-1
    uv.active_render=True
    o['source_pixel_crop']=list(crop)
    o['source']=photo.name
    o['status']='UV region from unchanged packed photo; photographic lighting/reflections remain baked'
    if parent:o.parent=parent
    return o

def fx(pixel):return (pixel-28)/972*7
left=fx(90)
left_front=fx(222)
recess_left=fx(330)
door_left=fx(535)
door_right=fx(700)
right_front=fx(812)
right=fx(947)
DEPTH=.95
TOP=2.62

# Replace only the front section of the ground slab, matching the photographic
# asymmetric recess while preserving the plan-traced building behind it.
delete_generated(ground,lambda n:n=='Ground | continuous timber floor')
pixels=[(82,85),(174,91),(365,91),(1005,20),(1016,327),(778,355),(778,373),(284,401),(82,401)]
for x,y in [(right,0),(right_front,0),(door_right,DEPTH),(recess_left,DEPTH),(left_front,0),(left,0)]:
    pixels.append((82+y/S,85+x/S))
slab('Ground | continuous timber floor',pixels,0,ground)

# Pilasters and joinery sit over actual angled glass rather than a flat photo.
for x,width in ((left/2,left),(7-(7-right)/2,7-right)):
    box('Front | full-height dark pilaster',(x,-.07,1.32),(width,.20,2.64),front,trim_mat)
    box('Front | pilaster base',(x,-.12,.22),(width+.06,.30,.44),front,trim_mat)
    box('Front | pilaster cap',(x,-.15,2.52),(width+.08,.30,.20),front,trim_mat)

facets=[('left display', (left,0),(left_front,0),(90,370,222,687)),
        ('left angled display',(left_front,0),(recess_left,DEPTH),(222,370,330,687)),
        ('recess fixed glazing',(recess_left,DEPTH),(door_left,DEPTH),(330,437,535,674)),
        ('right angled display',(door_right,DEPTH),(right_front,0),(700,370,812,687)),
        ('right display',(right_front,0),(right,0),(812,370,947,687))]
for name,a,b,crop in facets:
    beam('Front | '+name+' plinth',a,b,.15,0,.22,front,trim_mat)
    beam('Front | '+name+' head',a,b,.10,2.53,TOP,front,trim_mat)
    panel('Front | '+name+' photo glass',a,b,.23,2.53,crop)
    for p in (a,b):box('Front | display mullion',(p[0],p[1]-.02,1.40),(.06,.10,2.40),front,trim_mat)
    # Separate lower blue panels can be replaced/textured without changing glass.
    beam('Front | '+name+' blue-panel rail',a,b,.065,.90,.95,front,trim_mat)

# Central glazing/transom is at the back of the recess. The active entrance is
# to the right of the fixed central pane, as in the photograph.
panel('Front | entrance transom',(recess_left,DEPTH-.01),(door_right,DEPTH-.01),2.24,2.53,(330,375,700,435))
beam('Front | transom horizontal',(recess_left,DEPTH),(door_right,DEPTH),.10,2.20,2.26,front,trim_mat)
for x in (door_left,door_right):box('Front | entrance jamb',(x,DEPTH,1.12),(.085,.13,2.24),front,trim_mat)
door_width=(door_right-door_left)/2
for i,(hinge_x,angle,crop) in enumerate([(door_left,72,(535,435,618,674)),(door_right,108,(618,435,700,674))]):
    hinge=bpy.data.objects.new(f'Front | entrance leaf {i+1} hinge',None)
    front.objects.link(hinge)
    hinge.location=(hinge_x,DEPTH,0)
    hinge.rotation_euler.z=math.radians(angle)
    leaf=box(f'Front | entrance leaf {i+1} joinery',(0,0,0),(door_width-.04,.06,2.19),front,trim_mat)
    leaf.parent=hinge
    leaf.location=((door_width-.04)/2,0,1.095)
    panel(f'Front | entrance leaf {i+1} photo',(0,-.035),(door_width-.04,-.035),.03,2.18,crop,parent=hinge)
    leaf['status']='Photo-based double door; open hinges editable; no BO3 trigger'

# Full black fascia, layered cornice, photographed lettering and FREEHOUSE.
box('Front | fascia body',(3.5,-.06,3.08),(7.05,.25,.91),front,trim_mat)
panel('Front | photographed fascia',(fx(62),-.197),(fx(967),-.197),2.76,3.40,(62,235,967,326))
for z,thick,depth in [(2.64,.09,.31),(2.72,.06,.27),(3.47,.09,.34),(3.55,.065,.39)]:
    box('Front | fascia moulding',(3.5,-.09,z),(7.13,depth,thick),front,trim_mat)
for x in (.22,6.80):
    box('Front | fascia end corbel',(x,-.16,3.12),(.26,.28,.68),front,trim_mat)

# Upper storey: three sash windows and pale stone sills from the photographs.
stone=material('Front | pale stone lintels',(.70,.67,.54))
centers=[fx(209.5),fx(521.5),fx(831)]
widths=[fx(274)-fx(145),fx(591)-fx(452),fx(902)-fx(760)]
bottom,top=3.91,5.65
box('Front | upper brick sill band',(3.5,-.035,3.71),(7.05,.18,.34),upper,brick)
box('Front | upper brick head band',(3.5,-.035,5.99),(7.05,.18,.68),upper,brick)
cursor=0
for i,(x,w) in enumerate(zip(centers,widths)):
    lo,hi=x-w/2-.07,x+w/2+.07
    box('Front | upper brick pier',((cursor+lo)/2,-.035,(bottom+top)/2),(lo-cursor,.18,top-bottom),upper,brick)
    box('Front | sash recessed glass',(x,.035,(bottom+top)/2),(w,.045,top-bottom),upper,glass_mat)
    for side in (-1,1):box('Front | sash jamb',(x+side*w/2,-.105,(bottom+top)/2),(.07,.12,top-bottom+.12),upper,trim_mat)
    for z in (bottom,(bottom+top)/2,top):box('Front | sash meeting rail',(x,-.11,z),(w+.10,.12,.06),upper,trim_mat)
    for z in (bottom+(top-bottom)*.25,bottom+(top-bottom)*.75):box('Front | sash glazing bar',(x,-.12,z),(w,.055,.027),upper,trim_mat)
    for delta in (-w/6,w/6):box('Front | sash glazing upright',(x+delta,-.12,(bottom+top)/2),(.025,.055,top-bottom),upper,trim_mat)
    box('Front | stone sash sill',(x,-.17,bottom-.12),(w+.28,.32,.18),upper,stone)
    box('Front | stone sash lintel',(x,-.14,top+.12),(w+.25,.25,.19),upper,stone)
    cursor=hi
box('Front | upper brick final pier',((cursor+7)/2,-.035,(bottom+top)/2),(7-cursor,.18,top-bottom),upper,brick)

# Front-only inspection scene: real photographic UVs visible via Workbench.
front_scene=bpy.data.scenes.new('04 Photo frontage - inspection')
for c in (front,upper):front_scene.collection.children.link(c)
front_scene.unit_settings.system='METRIC'
configure(front_scene,'Photo frontage camera',(3.5,.3,3.0),(10,-14,7.1),10)
front_scene.display.shading.color_type='TEXTURE'
for s in (scene,assembled):s.display.shading.color_type='TEXTURE'
bpy.context.window.scene=front_scene
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active
            space.shading.type='SOLID'
            space.shading.color_type='TEXTURE'
            space.region_3d.view_rotation=front_scene.camera.rotation_euler.to_quaternion()
            space.region_3d.view_perspective='ORTHO'
            space.region_3d.view_location=(3.5,.3,3)
            space.region_3d.view_distance=12

manifest=json.loads((ROOT/'assets/blender/floorplan-blockout-manifest.json').read_text(encoding='utf-8'))
manifest['file']=OUT.name
manifest['frontage']={'source':photo.name,'source_sha256':hashlib.sha256(photo.read_bytes()).hexdigest(),
    'width_estimate_m':7,'recess_depth_assumed_m':DEPTH,'door_x_m':[door_left,door_right],
    'observed':'Asymmetric recessed entrance, fixed pane left of double doors; angled display bays, dark pilasters/fascia, blue lower glazing panels, three upstairs sash windows',
    'edits':'Original photo packed; UV sampling only; no source edits',
    'status':'Photo-led editable 3D joinery plus selected photographic surfaces; texture bake reflections retained'}
manifest['toilets']='Separate men/women entrances to common seating; continuous solid shared divider, no connecting door'
manifest['scenes'].append(front_scene.name)
(OUT.parent/'floorplan-blockout-v02-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
front_scene.render.filepath=str(OUT.parent/'photo-frontage-v02.png')
bpy.ops.render.render(write_still=True,scene=front_scene.name)
result={'file':str(OUT),'frontage_preview':front_scene.render.filepath,'photo_source_unchanged':True,'toilets':'Solid divider; independent doors','stairs':'Awaiting outside-door clarification'}
