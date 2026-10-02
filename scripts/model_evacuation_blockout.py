"""Trace the supplied plan into editable modular geometry, preserving the base file.

Run through the live bridge with scripts/run_blender_script.py. Pixel coordinates
are hand-traced structural centre lines; red evacuation boundaries are ignored.
"""
from pathlib import Path
import math
import json
import hashlib
import bpy
from mathutils import Vector, Quaternion
from mathutils.geometry import tessellate_polygon

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/blender/pharmacie-floorplan-blockout.blend'
SOURCE = ROOT / 'Architectural Fire Evacuation Floor Plans.png'
if OUT.exists():
    raise RuntimeError('Blockout file exists; choose a new version before regenerating')
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
S = 7/316
STOREY = 3.2
HEIGHT = 2.9
EXT = 0.22
INT = 0.14
# Assemble the two drawings into a common estimated building envelope. The raw
# upstairs raster is ~12% longer and 3.5% wider; this is explicit rectification,
# not a claim about measured venue dimensions. Original image remains packed.
FF_X = 316/327
FF_Y = 934/1044
scene = bpy.data.scenes.new('01 Ground floor - mapped rooms')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'
scene['frontage_estimate_m'] = 7.0
scene['storey_height_assumed_m'] = STOREY
scene['wall_height_assumed_m'] = HEIGHT
scene['upstairs_rectification'] = f'Width {FF_X}; depth {FF_Y}; common estimated shell; see manifest'
scene['status'] = 'Blender blockout only. BO3 collision, export and gameplay NOT verified.'

def collection(name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c

ground = collection('BLOCKOUT | Ground floor rooms + shell')
first = bpy.data.collections.new('BLOCKOUT | First floor rooms + shell')
stairs = collection('BLOCKOUT | Continuous L stairs - provisional position')
front = collection('BLOCKOUT | Frontage and forecourt')
references = collection('BLOCKOUT | Original ground plan - toggle eye')
uprefs = bpy.data.collections.new('BLOCKOUT | Original first plan - rectified display')

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color,1)
    return m

wallmat = material('Blockout - warm plaster',(.78,.72,.62))
brick = material('Blockout - frontage brick',(.39,.16,.11))
wood = material('Blockout - timber floor',(.36,.23,.12))
tile = material('Blockout - service tiles',(.48,.57,.59))
bar_mat = material('Blockout - dark bar',(.12,.065,.028))
door_mat = material('Blockout - doors',(.21,.38,.42))
glass_mat = material('Blockout - window proxy blue',(.25,.48,.60))
label_mat = material('Blockout - labels',(.06,.08,.09))
trim_mat = material('Blockout - dark shopfront trim',(.045,.052,.046))
metal = material('Blockout - rails',(.16,.18,.19))
stair_mat = material('Blockout - provisional stairs',(.55,.37,.13))

def pt(pixel, floor=0, z=None):
    ax,ay = (82,85) if floor == 0 else (76,558)
    sx,sy = (1,1) if floor == 0 else (FF_X,FF_Y)
    return Vector(((pixel[1]-ay)*S*sx,(pixel[0]-ax)*S*sy, floor*STOREY if z is None else z))

def mesh_obj(name, verts, faces, c, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    o = bpy.data.objects.new(name,mesh)
    c.objects.link(o)
    mesh.materials.append(mat)
    o.color = mat.diffuse_color
    # Two explicit maps: metre-based tiling and per-face 0..1 photo placement.
    for uvname,normalized in [('UV_Metres',False),('UV_Face_01',True)]:
        uv=mesh.uv_layers.new(name=uvname)
        for poly in mesh.polygons:
            normal=poly.normal
            axis=max(range(3),key=lambda i:abs(normal[i]))
            axes=[i for i in range(3) if i!=axis]
            coords=[(mesh.vertices[mesh.loops[j].vertex_index].co[axes[0]],mesh.vertices[mesh.loops[j].vertex_index].co[axes[1]]) for j in poly.loop_indices]
            lo=[min(v[i] for v in coords) for i in range(2)]
            hi=[max(v[i] for v in coords) for i in range(2)]
            for j,v in zip(poly.loop_indices,coords):
                uv.data[j].uv=tuple((v[i]-lo[i])/max(hi[i]-lo[i],1e-8) if normalized else v[i] for i in range(2))
    mesh.uv_layers.active_index=0
    return o

def box(name,center,dims,c,mat):
    dx,dy,dz = (d/2 for d in dims)
    verts = [(-dx,-dy,-dz),(-dx,-dy,dz),(-dx,dy,-dz),(-dx,dy,dz),
             (dx,-dy,-dz),(dx,-dy,dz),(dx,dy,-dz),(dx,dy,dz)]
    faces = [(0,2,6,4),(1,5,7,3),(0,4,5,1),(2,3,7,6),(0,1,3,2),(4,6,7,5)]
    o = mesh_obj(name,verts,faces,c,mat)
    o.location = center
    return o

def beam(name,a,b,thick,z0,z1,c,mat):
    a,b = Vector(a),Vector(b)
    d = b-a
    if d.xy.length < .001 or z1-z0 < .001:
        return None
    center = ((a.x+b.x)/2,(a.y+b.y)/2,(z0+z1)/2)
    o = box(name,center,(d.xy.length,thick,z1-z0),c,mat)
    o.rotation_euler.z = math.atan2(d.y,d.x)
    return o

doors = []
windows = []

def wall(name,a,b,floor=0,openings=(),external=False,c=None):
    c = c or (ground if floor == 0 else first)
    a,b = pt(a,floor),pt(b,floor)
    length = (b-a).length
    thick = EXT if external else INT
    z = floor*STOREY
    intervals = sorted(openings,key=lambda t:t[0])
    cursor = 0
    for i,(start,end,kind) in enumerate(intervals):
        assert 0 <= start < end <= 1
        assert start >= cursor
        beam(f'{name} | pier {i}',a+(b-a)*cursor,a+(b-a)*start,thick,z,z+HEIGHT,c,wallmat)
        lo,hi = (0,2.1) if kind == 'door' else (.68,2.35)
        p,q = a+(b-a)*start,a+(b-a)*end
        beam(f'{name} | lintel {i}',p,q,thick,z+hi,z+HEIGHT,c,wallmat)
        if lo:
            beam(f'{name} | sill {i}',p,q,thick,z,z+lo,c,wallmat)
        if kind == 'door':
            door(name+f' | door {i}',p,q,z,c)
        else:
            pane = beam(name+f' | glazing {i}',p,q,.035,z+lo,z+hi,c,glass_mat)
            pane['status'] = 'Opaque blue glazing proxy, replace with validated game material'
            windows.append({'name':pane.name,'width_m':round((q-p).length,3),'floor':floor})
            for zz in (lo,hi):
                beam(name+f' | window rail {i}',p,q,.08,z+zz-.035,z+zz+.035,c,trim_mat)
        cursor = end
    beam(name+' | wall end',a+(b-a)*cursor,b,thick,z,z+HEIGHT,c,wallmat)

def door(name,a,b,z,c):
    width = (b-a).length
    theta = math.atan2(b.y-a.y,b.x-a.x)
    for i,p in enumerate((a,b)):
        box(name+f' | jamb {i}',(p.x,p.y,z+1.05),(.08,.08,2.1),c,trim_mat)
    beam(name+' | frame head',a,b,.085,z+2.06,z+2.14,c,trim_mat)
    # Open leaf attached to an independently editable hinge empty.
    hinge = bpy.data.objects.new(name+' | hinge',None)
    c.objects.link(hinge)
    hinge.location = (a.x,a.y,z)
    hinge.rotation_euler.z = theta + math.radians(72)
    leaf = box(name+' | open leaf',(0,0,0),(width-.08,.045,2.02),c,door_mat)
    leaf.parent = hinge
    leaf.location = ((width-.08)/2,0,1.01)
    leaf['status'] = 'Open blockout door; hinge angle editable; no game trigger'
    doors.append({'name':name,'clear_width_m':round(width-.08,3),'base_m':z})

def slab(name,pixels,floor,c,mat=wood):
    polygon = [pt(p,floor) for p in pixels]
    triangles = tessellate_polygon([polygon])
    n = len(polygon)
    vertices = [tuple(p-Vector((0,0,.18))) for p in polygon]+[tuple(p) for p in polygon]
    def index(v):
        if isinstance(v,int):
            return v
        return min(range(n),key=lambda i:(polygon[i]-v).length)
    faces = []
    for tri in triangles:
        ids = [index(v) for v in tri]
        faces.extend([tuple(reversed(ids)),tuple(i+n for i in ids)])
    for i in range(n):
        j = (i+1)%n
        faces.append((i,j,j+n,i+n))
    return mesh_obj(name,vertices,faces,c,mat)

def room_label(name,pixel,floor,c,size=.28):
    font = bpy.data.curves.new(name,'FONT')
    font.body = name
    font.align_x = 'CENTER'
    font.size = size
    font.extrude = 0.002
    o = bpy.data.objects.new('Room label | '+name,font)
    c.objects.link(o)
    o.location = pt(pixel,floor,z=floor*STOREY+.012)
    font.materials.append(label_mat)
    o.color = label_mat.diffuse_color
    return o

OUTLINE_G = [(82,85),(174,91),(365,91),(1005,20),(1016,327),(778,355),(778,373),(284,401),(82,401),(82,337),(130,290),(158,290),(158,201),(130,198),(82,151)]
OUTLINE_F = [(76,558),(172,566),(346,567),(1096,501),(1120,828),(813,856),(813,865),(302,885),(76,885)]
slab('Ground | continuous timber floor',OUTLINE_G,0,ground)
upper_slab = slab('First | floor with L stairwell opening',OUTLINE_F,1,first)

# Ground shell. Front is the left edge of the image and Y=0 in world space.
for i,a in enumerate(OUTLINE_G):
    b = OUTLINE_G[(i+1)%len(OUTLINE_G)]
    gaps = ()
    if i == 3: gaps = ((.12,.25,'door'),)  # rear escape / external pathway
    if i == 6: gaps = ((.37,.45,'door'),)  # lower long-wall door shown by bar
    if i in (8,13): gaps = ((.18,.83,'window'),)
    if i in (9,12): gaps = ((.15,.82,'window'),)
    if i == 11: gaps = ((.30,.76,'door'),)  # central recessed street entrance
    if i == 0: gaps = ((.20,.86,'window'),)
    if i == 7: gaps = ((.59,.92,'window'),)
    wall(f'Ground shell {i:02}',a,b,openings=gaps,external=True)

# Behind the bar: rear lobby, WC/service partitions and upper rear space.
wall('Ground | bar lobby divider',(767,168),(767,358),openings=((.61,.91,'door'),))
wall('Ground | lobby top',(767,168),(838,164),openings=((.20,.69,'door'),))
wall('Ground | WC front',(840,111),(840,260),openings=((.43,.76,'door'),))
wall('Ground | WC top',(840,111),(944,110))
wall('Ground | WC rear',(944,110),(951,259))
wall('Ground | WC bottom',(840,260),(951,259))
wall('Ground | service top',(767,251),(840,247))
wall('Ground | service rear - shortened for L stair adaptation',(891,259),(891,275))
wall('Ground | service bottom',(777,336),(891,326))
wall('Ground | upper rear partition',(840,159),(910,155))
wall('Ground | upper rear short wall',(940,109),(940,155))
wall('Ground | rear passage partition',(847,50),(847,110))

# Bar U footprint is furniture, not the red route boundary.
for i,(a,b) in enumerate([((558,333),(558,143)),((558,143),(641,140)),((641,140),(641,322))]):
    p,q = pt(a),pt(b)
    beam(f'Bar | cabinet run {i}',p,q,.58,0,1.03,ground,bar_mat)
    beam(f'Bar | counter top {i}',p,q,.72,1.03,1.11,ground,wood)
room_label('MAIN PUB',(350,248),0,ground,.50)
room_label('BAR',(605,242),0,ground,.30)
room_label('REAR LOBBY',(800,211),0,ground,.21)
room_label('MENS WC',(890,207),0,ground,.23)
room_label('SERVICE',(827,294),0,ground,.23)
room_label('REAR SPACE\n(use unlabelled)',(887,80),0,ground,.18)

# Upstairs shell / full partitions, with gaps placed from visible door symbols.
for i,a in enumerate(OUTLINE_F):
    gaps = ()
    if i == 0: gaps = ((.21,.87,'window'),)
    if i == 3: gaps = ((.16,.30,'window'),(.69,.84,'window'))
    if i == 7: gaps = ((.05,.50,'window'),)
    if i == 8: gaps = ((.11,.23,'window'),(.43,.55,'window'),(.76,.88,'window'))
    wall(f'First shell {i:02}',a,OUTLINE_F[(i+1)%len(OUTLINE_F)],1,gaps,True)
wall('First | front office bottom',(80,689),(306,689),1)
wall('First | front office rear',(306,574),(306,689),1,((.26,.56,'door'),))
wall('First | kitchen passage rear',(350,693),(350,861),1,((.2169047619,.4382142857,'door'),))
wall('First | kitchen top',(82,693),(350,693),1)
wall('First | store front',(828,540),(828,606),1)
wall('First | store bottom',(828,606),(929,601),1)
wall('First | rear office front',(929,533),(939,630),1,((.14,.44,'door'),))
wall('First | toilets front',(776,613),(784,787),1,((.23,.43,'door'),(.65,.85,'door')))
wall('First | male WC top',(776,613),(932,605),1)
wall('First | toilets middle',(780,698),(933,686),1)
wall('First | toilets rear',(932,605),(938,765),1)
wall('First | female WC bottom',(784,777),(938,765),1)
wall('First | rear office bottom',(934,630),(1016,629),1,((.50,.87,'door'),))
wall('First | office return',(1016,629),(1024,678),1)
wall('First | office bottom rear',(1024,678),(1099,673),1)
wall('First | rear store top',(940,688),(1024,684),1)
wall('First | rear store front',(941,688),(944,762),1,((.11,.61,'door'),))
wall('First | rear store rear',(1024,684),(1029,762),1)
wall('First | rear store bottom',(944,762),(1029,756),1)
wall('First | hall access',(782,787),(782,843),1,((.12,.88,'door'),))
room_label('UPSTAIRS SEATING',(545,703),1,first,.42)
room_label('FRONT OFFICE',(198,627),1,first,.28)
room_label('KITCHEN / PREP',(218,797),1,first,.30)
room_label('STORE',(876,572),1,first,.20)
room_label('REAR OFFICE',(1002,578),1,first,.27)
room_label('MALE WC',(850,652),1,first,.22)
room_label('FEMALE WC',(850,738),1,first,.22)
room_label('STORE',(980,724),1,first,.18)
room_label('HALL',(845,815),1,first,.21)

# Basic kitchen and WC proxies improve readability without implying bespoke art.
def pixelbox(name,a,b,floor,height,c,mat,base=0):
    p,q = pt(a,floor),pt(b,floor)
    return box(name,((p.x+q.x)/2,(p.y+q.y)/2,floor*STOREY+base+height/2),
               (abs(q.x-p.x),abs(q.y-p.y),height),c,mat)
pixelbox('Kitchen | left preparation run',(99,711),(132,859),1,.9,first,tile)
pixelbox('Kitchen | sink and hob run',(134,705),(316,734),1,.9,first,tile)
pixelbox('Kitchen | central prep table',(169,828),(288,858),1,.85,first,wood)
for name,pixel,floor,c in [('Ground WC pan',(925,228),0,ground),('Male WC pan',(907,630),1,first),('Female WC pan',(907,713),1,first)]:
    p=pt(pixel,floor)
    box(name,(p.x,p.y,p.z+.22),(.46,.60,.44),c,tile)
for name,pixel,floor,c in [('Ground basin',(930,183),0,ground),('Male basin',(912,670),1,first),('Female basin',(915,753),1,first)]:
    p=pt(pixel,floor)
    box(name,(p.x,p.y,p.z+.82),(.42,.55,.16),c,tile)

# Continuous L stair adapted from first-floor L footprint, placed within the
# common shell. Ground straight-flight symbol retained as a wire guide below.
# 18 equal risers, 10 + landing + 8; start is in rear ground passage.
stair_shift = Vector((-.45,.27,0))
start = pt((885,800),1,z=0) + stair_shift
corner = pt((1064,800),1,z=0) + stair_shift
end = pt((1064,699),1,z=0) + stair_shift
W = 1.00
N1,N2 = 10,8
RISE = STOREY/(N1+N2)
D1 = (corner-start).normalized()
D2 = (end-corner).normalized()
run1 = (corner-start).length-W/2
run2 = (end-corner).length-W/2
for i in range(N1):
    tread=run1/N1
    pos=start+D1*(i+.5)*tread
    box(f'Stairs | lower tread {i+1:02}',(pos.x,pos.y,(i+1)*RISE/2),
        (W,tread,(i+1)*RISE),stairs,stair_mat)
landing=box('Stairs | turn landing',(corner.x,corner.y,N1*RISE/2),
            (W,W,N1*RISE),stairs,stair_mat)
for i in range(N2):
    tread=run2/N2
    pos=corner+D2*(W/2+(i+.5)*tread)
    height=(N1+i+1)*RISE
    box(f'Stairs | upper tread {i+1:02}',(pos.x,pos.y,height/2),
        (tread,W,height),stairs,stair_mat)
top=box('Stairs | upper arrival landing',(end.x-.30,end.y,STOREY-.09),
        (.60,W,.18),stairs,stair_mat)

# Cut a true L opening in the upper slab. Cutters are used only on newly generated
# geometry and removed after applying; no user data is deleted.
for name,center,dims in [
    ('lower flight void',((start.x+corner.x)/2,(start.y+corner.y)/2,STOREY),(W+.12,(corner-start).length+W+.12,1)),
    ('upper flight void',((corner.x+end.x)/2,(corner.y+end.y)/2,STOREY),((corner-end).length+W/2+.12,W+.12,1))]:
    cutter=box('Temporary '+name,center,dims,first,stair_mat)
    bpy.ops.object.select_all(action='DESELECT')
    # First-floor collection must be linked temporarily for contextual modifier op.
    if first.name not in scene.collection.children:
        scene.collection.children.link(first)
    upper_slab.select_set(True)
    bpy.context.view_layer.objects.active=upper_slab
    mod=upper_slab.modifiers.new(name,'BOOLEAN')
    mod.operation='DIFFERENCE'
    mod.solver='EXACT'
    mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
if first.name in scene.collection.children:
    scene.collection.children.unlink(first)

# Rail outlines along the outside of each flight; vertical dimensions provisional.
# A sloped cylindrical-like rectangular rail model, with actual XYZ slope.
def rail(name,a,b):
    d=b-a
    obj=box(name,(a+b)/2,(.055,.055,d.length),stairs,metal)
    obj.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    return obj
for offset in (-W/2,W/2):
    rail(f'Stairs | lower sloped rail {offset}',start+Vector((offset,0,.95)),corner-D1*(W/2)+Vector((offset,0,N1*RISE+.95)))
    rail(f'Stairs | upper sloped rail {offset}',corner+D2*(W/2)+Vector((0,offset,N1*RISE+.95)),end+Vector((0,offset,STOREY+.95)))
room_label('L STAIRS\nPOSITION PROVISIONAL',(987,803),1,first,.18)

# Facade has real recessed opening and proxy glazing; sign faces the street.
box('Front | forecourt',(3.5,-1.1,-.14),(9,2.2,.20),front,tile)
box('Front | fascia',(3.5,-.17,2.56),(7.05,.18,.46),front,trim_mat)
font=bpy.data.curves.new('Pub fascia lettering','FONT')
font.body='THE PHARMACIE ARMS'
font.align_x='CENTER'
font.size=.33
font.extrude=.003
sign=bpy.data.objects.new('Front | pub name',font)
front.objects.link(sign)
sign.location=(3.5,-.268,2.48)
sign.rotation_euler.x=math.pi/2
font.materials.append(wallmat)
sign.color=wallmat.diffuse_color
box('Front | upstairs brick sill band',(3.5,-.16,3.70),(7.05,.16,.95),front,brick)
box('Front | upstairs brick header band',(3.5,-.16,5.80),(7.05,.16,.66),front,brick)
for lo,hi in ((0,.665),(1.635,3.015),(3.985,5.365),(6.335,7)):
    box('Front | upstairs brick window pier',((lo+hi)/2,-.16,4.63),(hi-lo,.16,1.65),front,brick)
for x in (1.15,3.50,5.85):
    box(f'Front | upper sash window {x}',(x,-.26,4.63),(.9,.07,1.65),front,glass_mat)
    for dx in (-.48,.48):
        box('Front | sash jamb',(x+dx,-.30,4.63),(.07,.10,1.79),front,trim_mat)
    for dz in (-.86,0,.86):
        box('Front | sash horizontal',(x,-.31,4.63+dz),(1.02,.10,.06),front,trim_mat)
    box('Front | sash centre',(x,-.31,4.63),(.045,.10,1.72),front,trim_mat)

# External path + proposed seating plate: not asserted to have been built.
pixelbox('External | pathway estimate',(1020,60),(1062,440),0,.12,ground,tile,base=-.12)
pixelbox('External | proposed seating area',(1062,310),(1162,434),0,.12,ground,tile,base=-.12)
room_label('PROPOSED\nEXTERNAL SEATING',(1111,370),0,ground,.20)

# Duplicate packed-image reference objects, with UVs unchanged. First plane is
# rectified to match the model transformation; original pixel anchors recorded.
def copy_reference(original,c,floor):
    old=bpy.data.objects.get(original)
    assert old is not None
    obj=old.copy()
    obj.data=old.data.copy()
    c.objects.link(obj)
    obj.name='Model reference | '+original
    if floor:
        for vertex in obj.data.vertices:
            vertex.co.x*=FF_X
            vertex.co.y*=FF_Y
            vertex.co.z=STOREY-.025
    obj.hide_select=True
    obj.hide_render=True
    return obj
gr=copy_reference('Ground floor original plan',references,0)
ur=copy_reference('First floor original plan',uprefs,1)
gr.hide_set(True)

# Ground stair symbol is a retained location guide, rather than disguised as
# accurately connected gameplay stairs.
data=bpy.data.curves.new('Ground drawn stair footprint','CURVE')
data.dimensions='3D'
data.bevel_depth=.012
poly=data.splines.new('POLY')
points=[(948,125),(999,125),(999,226),(948,226)]
poly.points.add(3)
for p,pix in zip(poly.points,points): p.co=(*pt(pix,0,z=.02),1)
poly.use_cyclic_u=True
guide=bpy.data.objects.new('Reference | ground drawn stairs - alignment unresolved',data)
references.objects.link(guide)
guide.hide_render=True
guide.hide_set(True)

upscene=bpy.data.scenes.new('02 First floor - mapped rooms')
for c in (first,stairs,uprefs): upscene.collection.children.link(c)
upscene.unit_settings.system='METRIC'
upscene.unit_settings.length_unit='METERS'
assembled=bpy.data.scenes.new('03 Both floors - assembled exterior')
for c in (ground,first,stairs,front): assembled.collection.children.link(c)
assembled.unit_settings.system='METRIC'
assembled.unit_settings.length_unit='METERS'

def configure(s,name,target,position,ortho=27):
    camdata=bpy.data.cameras.new(name)
    cam=bpy.data.objects.new(name,camdata)
    s.collection.objects.link(cam)
    cam.location=position
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    camdata.type='ORTHO'
    camdata.ortho_scale=ortho
    camdata.clip_end=200
    s.camera=cam
    s.render.engine='BLENDER_WORKBENCH'
    s.display.shading.light='STUDIO'
    s.display.shading.color_type='MATERIAL'
    s.display.shading.show_shadows=True
    s.display.shading.show_cavity=True
    s.display.shading.cavity_type='BOTH'
    s.display.shading.background_type='WORLD'
    s.world=bpy.data.worlds.new(name+' World')
    s.world.color=(.82,.84,.87)
    s.render.resolution_x=1400
    s.render.resolution_y=1000
    s.render.resolution_percentage=100
    s.view_settings.view_transform='Standard'
    return cam
configure(scene,'Ground overview camera',(3.2,10,0),(16,-2,35),33)
configure(upscene,'First overview camera',(3.2,10,STOREY),(16,-2,39),33)
configure(assembled,'Assembled exterior camera',(3.5,9,2.7),(27,-22,24),31)
bpy.context.window.scene=scene
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active
            space.shading.type='SOLID'
            space.shading.color_type='MATERIAL'
            space.shading.show_cavity=True
            region=space.region_3d
            region.view_rotation=scene.camera.rotation_euler.to_quaternion()
            region.view_perspective='ORTHO'
            region.view_location=(3.5,10,1)
            region.view_distance=28
ur.hide_set(True,view_layer=upscene.view_layers[0])

manifest={'file':OUT.name,'source':SOURCE.name,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'frontage_estimate_m':7,'metres_per_pixel':S,'storey_height_assumed_m':STOREY,'wall_height_assumed_m':HEIGHT,
          'external_wall_assumed_m':EXT,'internal_wall_assumed_m':INT,'upstairs_display_rectification':{'width':FF_X,'depth':FF_Y},
          'stairs':{'status':'Continuous L adaptation; drawn ground flight does not align with upstairs L; exact venue location unresolved',
                    'risers':18,'riser_m':RISE,'width_m':W,'lower_tread_m':run1/N1,'upper_tread_m':run2/N2,
                    'start':list(start),'turn':list(corner),'arrival':list(end)},
          'doors':doors,'windows':windows,'scenes':[scene.name,upscene.name,assembled.name],
          'limitations':['Hand traced structural centre lines; opening positions approximate','Ground entrance inferred from front recess + photos',
                         'Upstairs affine rectification is a modelling assumption','Heights unmeasured','No ceilings/roof, for cutaway inspection',
                         'Facade three upper sash windows from existing photos; dimensions approximate','No BO3 export, compiler or game test performed']}
# Meaningful structural checks on generated source geometry.
assert abs(18*RISE-STOREY)<1e-8
assert len(doors)>=14 and len(windows)>=10
assert len(upper_slab.data.polygons)>0 and not upper_slab.modifiers
assert all(math.isfinite(v) for d in doors for v in [d['clear_width_m']])
assert min(d['clear_width_m'] for d in doors)>.45
OUT.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(OUT.parent/'floorplan-blockout-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
result={'file':str(OUT),'doors':len(doors),'windows':len(windows),'scenes':manifest['scenes'],
        'stairs_riser_m':RISE,'status':'Saved modular blockout; conversion unverified'}
print(json.dumps(result))
