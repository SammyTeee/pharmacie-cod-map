"""Original vehicle props and bounded street combat layout; Blender-only v31."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath);assert source.name=='pharmacie-zombies-alley-v30.blend'
OUT=ROOT/'assets/blender/pharmacie-zombies-street-v31.blend';assert not OUT.exists()
dest=ROOT/'recon/v31';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
coll=bpy.data.collections.new('MAPPING v31 | Street combat vehicles and boundaries');scene.collection.children.link(coll)
made=[];vehicles=[];basis=Matrix.Identity(4);current='street'
def mat(name,color,metal=0,rough=.7):
    m=bpy.data.materials.new('Street v31 | '+name);m.diffuse_color=(*color,1);m.use_nodes=True;bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=m.diffuse_color;bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;return m
teal=mat('aged teal paint',(.075,.21,.21),.55,.34);white=mat('weathered van ivory',(.61,.62,.55),.3,.55);rust=mat('burnt maroon',(.19,.035,.024),.5,.62);tyre=mat('rubber tyres',(.014,.017,.020));silver=mat('wheel and trim metal',(.33,.35,.37),.8,.33);dark=mat('charcoal fittings',(.025,.033,.039),.3);glass=mat('reflective smoke glass',(.025,.055,.075),.4,.18);headlight=mat('headlamp lenses',(.63,.69,.70),.4,.23);tail=mat('red lamp lenses',(.45,.008,.004),.25,.3);yellow=mat('rear registration yellow',(.72,.51,.08));ivory=mat('front registration ivory',(.72,.74,.69));orange=mat('barrier orange',(.66,.16,.025));concrete=mat('aged concrete',(.32,.33,.29));wood=mat('rough timber',(.24,.15,.075));soil=mat('dark planter soil',(.075,.07,.045));earth=mat('terrain backing',(.14,.15,.115));leaf=mat('street shrub leaves',(.065,.13,.047));paving=bpy.data.materials['Street v17 | paving']
def mesh(name,verts,faces,m,role='scenery'):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new('Street v31 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['mapping_role']=role;o['status']='Original Blender geometry; BO3 conversion/collision pending';made.append(o);return o
def box(name,a,b,c,d,e,f,m,role='scenery',bevel=0):
    o=mesh(name,[(a,c,e),(b,c,e),(b,d,e),(a,d,e),(a,c,f),(b,c,f),(b,d,f),(a,d,f)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m,role)
    if bevel:mod=o.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=2
    return o
def cylinder(name,loc,radius,depth,m,axis='Y',vertices=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth);o=bpy.context.object;o.name='Street v31 | '+current+' | '+name
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);rot=Matrix.Rotation(math.pi/2,4,'X') if axis=='Y' else Matrix.Identity(4);o.matrix_world=basis@Matrix.Translation(Vector(loc))@rot;o.data.materials.append(m);o['mapping_role']='vehicle_detail';made.append(o)
    for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
    return o
def panel(name,points,m,thickness=.018):
    # Closed prism around a planar quad; fixes export/collision ambiguity of single-sided panels.
    pts=[Vector(p) for p in points];normal=(pts[1]-pts[0]).cross(pts[2]-pts[0]).normalized();vs=[tuple(p+normal*s*thickness/2) for s in (-1,1) for p in pts]
    return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],m)
def lettering(body,loc,size=.1,rotation=(math.pi/2,0,0),m=ivory):
    cu=bpy.data.curves.new(body,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.001;cu.materials.append(m);o=bpy.data.objects.new('Street v31 | '+current+' | '+body,cu);coll.objects.link(o);o.matrix_world=basis@Matrix.Translation(Vector(loc))@Matrix.Rotation(rotation[2],4,'Z')@Matrix.Rotation(rotation[0],4,'X');return o
def vehicle(ident,loc,yaw,paint,van=False,damage=False):
    global basis,current
    current=ident;basis=Matrix.Translation(Vector(loc))@Matrix.Rotation(math.radians(yaw),4,'Z');start=len(made)
    length=5.2 if van else 4.2;half=length/2;w=1.00 if van else .89
    sections=[(-half,.76,.34,.82),(-half+.30,w,.34,1.02),(-.9,w,.34,1.04),(.85,w,.34,1.02),(half-.28,.83,.34,.89),(half,.73,.36,.78)]
    verts=[]
    for x,width,z0,z1 in sections:verts.extend([(x,-width,z0),(x,width,z0),(x,width,z1),(x,-width,z1)])
    faces=[(3,2,1,0),tuple(range(len(verts)-4,len(verts)))]
    for i in range(len(sections)-1):
        for j in range(4):faces.append((i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j))
    body=mesh('vehicle body with wheel arches',verts,faces,paint,'vehicle_shell')
    # Two axle booleans cut actual wheel arches through the lower silhouette.
    axle=(-1.65,1.60) if van else (-1.30,1.29)
    for x in axle:
        cut=cylinder('temporary wheel arch cutter',(x,0,.32),.365,3,dark)
        mod=body.modifiers.new('Wheel arch','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut
        bpy.context.view_layer.objects.active=body;body.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name);body.select_set(False)
        made.remove(cut);bpy.data.objects.remove(cut,do_unlink=True)
    bevel=body.modifiers.new('Rounded body seams','BEVEL');bevel.width=.035;bevel.segments=2
    box('underbody chassis',-half+.3,half-.3,-.64,.64,.24,.36,dark)
    if van:
        box('van rear cargo shell',-half+.12,.15,-.91,.91,.95,2.03,paint,bevel=.07)
        cabin=[(.05,-.9,.95),(half-.25,-.8,.95),(half-.25,.8,.95),(.05,.9,.95),(.10,-.8,2.03),(1.0,-.73,2.03),(1.0,.73,2.03),(.10,.8,2.03)]
        mesh('van front cabin',cabin,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],paint)
        panel('van windscreen',[(1.06,-.67,1.97),(1.06,.67,1.97),(half-.22,.73,1.12),(half-.22,-.73,1.12)],glass)
        for side in (-1,1):
            panel('van front side window',[(.27,side*.84,1.15),(half-.42,side*.79,1.15),(.92,side*.77,1.89),(.27,side*.84,1.89)],glass)
            box('sliding cargo door relief',-2.17,-.15,side*.927-.008,side*.927+.008,1.02,1.92,paint)
            box('cargo door handle',-.49,-.29,side*.95-.018,side*.95+.018,1.23,1.28,dark)
        for y in (-.46,.46):box('rear split door relief',-half-.015,-half+.005,y-.40,y+.40,.94,1.89,paint)
    else:
        cabin=[(-1.66,-.79,.98),(1.05,-.79,.98),(1.05,.79,.98),(-1.66,.79,.98),(-1.23,-.65,1.49),(.33,-.65,1.49),(.33,.65,1.49),(-1.23,.65,1.49)]
        mesh('hatchback cabin shell',cabin,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],paint)
        panel('windscreen',[(.37,-.61,1.46),(.37,.61,1.46),(1.06,.74,1.01),(1.06,-.74,1.01)],glass)
        panel('rear hatch glazing',[(-1.65,-.73,1.03),(-1.65,.73,1.03),(-1.25,.60,1.45),(-1.25,-.60,1.45)],glass)
        for side in (-1,1):
            panel('front door glass',[(-.36,side*.793,1.04),(.93,side*.793,1.04),(.29,side*.674,1.43),(-.36,side*.674,1.43)],glass)
            panel('rear door glass',[(-1.57,side*.793,1.04),(-.46,side*.793,1.04),(-.46,side*.674,1.43),(-1.20,side*.674,1.43)],glass)
            box('window B pillar',-.46,-.36,side*.79-.018,side*.79+.018,1.01,1.47,dark)
            for x in (-.55,.67):box('door handle',x-.10,x+.10,side*.902-.015,side*.902+.015,.86,.905,dark)
            box('door seam',-.42,-.405,side*.892-.004,side*.892+.004,.43,1.015,dark)
        box('bonnet panel',1.08,half-.15,-.68,.68,.87,.895,paint,bevel=.018)
        if damage:
            # Buckled but closed bonnet, with black soot details; no unsupported loose panel.
            box('buckled bonnet edge',1.30,half-.20,-.65,.65,.895,.965,dark,bevel=.04)
            for x,y in ((1.45,-.42),(1.67,.22),(1.88,-.13)):box('scorched bonnet patch',x-.12,x+.12,y-.14,y+.14,.966,.97,dark)
    for side in (-1,1):
        for x in axle:
            cylinder('tyre',(x,side*(w+.015),.32),.32,.24,tyre)
            cylinder('alloy wheel rim',(x,side*(w+.147),.32),.222,.018,silver)
            cylinder('wheel hub',(x,side*(w+.163),.32),.071,.022,dark)
            for angle in (0,math.pi/2,math.pi,3*math.pi/2):
                cylinder('wheel lug',(x+math.cos(angle)*.095,side*(w+.177),.32+math.sin(angle)*.095),.017,.009,silver,vertices=8)
        box('side mirror support',.56,.73,side*(w+.08)-.035,side*(w+.08)+.035,1.06,1.11,dark)
        box('side mirror housing',.51,.77,side*(w+.18)-.055,side*(w+.18)+.055,1.03,1.18,paint,bevel=.04)
    for x in (-half,half):
        box('bumper',x-.07,x+.07,-.78,.78,.38,.57,dark,bevel=.03)
        box('registration plate',x+(-.079 if x<0 else .079)-.01,x+(-.079 if x<0 else .079)+.01,-.25,.25,.53,.64,yellow if x<0 else ivory)
    for side in (-1,1):
        box('headlamp',half-.01,half+.035,side*.52-.17,side*.52+.17,.68,.81,dark if damage and side<0 else headlight,bevel=.018)
        box('rear lamp',-half-.035,-half+.01,side*.55-.13,side*.55+.13,.68,.84,tail,bevel=.018)
    box('front radiator grille',half+.031,half+.045,-.29,.29,.67,.78,dark)
    for i in range(4):box('radiator grille slat',half+.045,half+.055,-.27,.27,.682+i*.023,.690+i*.023,silver)
    bpy.context.view_layer.update();pts=[o.matrix_world@Vector(v) for o in made[start:] for v in o.bound_box]
    bounds=[[min(p[i] for p in pts),max(p[i] for p in pts)] for i in range(3)]
    vehicles.append({'id':ident,'type':'service van' if van else 'damaged hatchback' if damage else 'hatchback','origin':loc,'yaw_degrees':yaw,'bounds_xyz':bounds,'mesh_names':[o.name for o in made[start:]],'provenance':'Original procedural Blender geometry, not copied CoD assets','engine_candidate':'veh_t7_civ_car_compact' if not van else 'No installed stock van verified'})
vehicle('V01 pub parked hatchback',(1,-4.40,-.08),0,teal)
vehicle('V02 delivery van',(17,-8.45,-.08),180,white,van=True)
vehicle('V03 damaged hatchback',(28,-4.50,-.08),8,rust,damage=True)
vehicle('V04 street-end wreck',(58,-6.70,-.08),90,rust,damage=True)
basis=Matrix.Identity(4);current='street boundaries'
# Back distant pavement pieces with terrain, without covering road tops or brook.
box('Terrain floor backing',-59,68,-42,40,-1.0,-.38,earth,'terrain_backing')
def fence(x,label):
    global current
    current=label
    for y in (-12.9,-10,-6.7,-3.4,-.1):box('fence upright',x-.08,x+.08,y-.07,y+.07,-.15,2.5,dark)
    for z in (.18,1.2,2.35):box('continuous fence rail',x-.035,x+.035,-13,0,z,z+.055,dark)
    # Opaque sheet backing blocks access and views through the boundary.
    box('closed street boundary sheet',x-.025,x+.025,-13,0,.08,2.37,dark,'street_boundary')
    for y in range(-12,0):box('sheet vertical rib',x-.045,x+.045,y-.018,y+.018,.12,2.35,silver)
    box('road-closed sign plate',x-.061,x-.051,-7.7,-5.7,1.45,1.95,orange)
    # Text in YZ plane, normal towards the playable side.
    cu=bpy.data.curves.new('ROAD CLOSED','FONT');cu.body='ROAD CLOSED';cu.align_x='CENTER';cu.align_y='CENTER';cu.size=.19;cu.extrude=.001;cu.materials.append(ivory)
    o=bpy.data.objects.new('Street v31 | '+label+' | ROAD CLOSED',cu);coll.objects.link(o);o.location=(x+(.065 if x<0 else -.065),-6.7,1.7)
    o.rotation_euler=Matrix(((0,0,1 if x<0 else -1),(-1 if x<0 else 1,0,0),(0,1,0))).to_euler()
fence(-18.25,'G31 west future Melton unlock boundary');fence(60.4,'B31 east closed scenery boundary')
current='Natural Wellbeing lane'
for x in (45.08,47.92):box('lane gate post',x-.055,x+.055,-29.85,-29.70,-.05,2.6,dark)
box('closed lane end gate',45.13,47.87,-29.81,-29.75,.07,2.43,dark,'lane_end_boundary')
for x in (45.76,47.14):box('lane gate recessed panel',x-.52,x+.52,-29.72,-29.69,.25,2.22,silver)
box('lane gate latch',46.43,46.57,-29.67,-29.62,1.14,1.35,dark)
current='pavement furnishings'
# Frontage-side details leave pavement centreline free.
for x in (3.65,7.35):
    cylinder('pub entrance bollard',(x,-.40,.44),.095,.88,dark,axis='Z',vertices=16)
    cylinder('bollard reflective collar',(x,-.40,.76),.101,.045,ivory,axis='Z',vertices=16)
for x in (8,32):
    box('low shopfront planter',x-.8,x+.8,-12.63,-12.15,0,.47,concrete,bevel=.045)
    box('planter soil',x-.71,x+.71,-12.57,-12.21,.47,.485,soil)
    for dx in (-.48,0,.48):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.24);o=bpy.context.object;o.name='Street v31 | pavement furnishings | shrub';o.location=(x+dx,-12.39,.69);o.scale=(1,.7,1);o.data.materials.append(leaf)
        for c in list(o.users_collection):c.objects.unlink(o)
        coll.objects.link(o);made.append(o)
for x in (22.3,23.0):
    box('shallow supply crate',x-.27,x+.27,-.72,-.18,0,.46,wood,bevel=.015)
    for z in (.1,.28):box('crate face rail',x-.29,x+.29,-.745,-.73,z,z+.05,dark)
# A short battered road barrier beside the wreck provides a readable end treatment.
for y in (-10.9,-2.25):
    box('concrete roadblock foot',57.0,59.1,y-.25,y+.25,-.08,.44,concrete,bevel=.07)
    box('roadblock orange panel',57.4,58.7,y-.15,y+.15,.44,.80,orange,bevel=.035)
markers=bpy.data.collections.new('GAMEPLAY v31 | Proposed street collision and gate registry');scene.collection.children.link(markers)
for name,loc,role in [('G31_WEST_MELTON',(-18.25,-6.7,0),'Future purchase/zone proposal; not scripted'),('B31_EAST_SCENERY',(60.4,-6.7,0),'Closed outer boundary; not a new purchase'),('P31_LANE_REWARD',(46.5,-27,0),'Possible wall buy/reward on dead-end lane; no prefab'),('P31_STREET_SUPPLIES',(22.65,-1.6,0),'Possible item pickup by shallow crates; no prefab')]:
    o=bpy.data.objects.new(name,None);markers.objects.link(o);o.location=loc;o.empty_display_type='ARROWS';o.empty_display_size=.3;o['proposal']=role;o['engine_implemented']=False
def camera(name,eye,target,ortho=None):
    cd=bpy.data.cameras.new('Review v31 | '+name);o=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(o);o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();cd.lens=26
    if ortho:cd.type='ORTHO';cd.ortho_scale=ortho
    return o
views=[camera('01_pub_vehicle',(-5,-8,1.65),(4,-3.3,1.05)),camera('02_street_combat',(6,-6.7,1.57),(24,-6.7,1.15)),camera('03_van_and_pavement',(12,-11.1,1.65),(19,-7.4,1.0)),camera('04_wreck_crossing',(22,-6.7,1.57),(35,-4.4,1.15)),camera('05_street_end',(51,-6.7,1.57),(59,-6.7,1.2)),camera('06_alley_front',(-14,-7,1.65),(-10.8,2,1.65)),camera('07_lane_gate',(46.5,-19,1.65),(46.5,-29,1.2)),camera('08_street_plan',(20,-6.7,75),(20,-6.7,0),ortho=86)]
bpy.context.view_layer.update()
for o in made:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)*o.matrix_world.determinant()>0,o.name;bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
scene.camera=views[1];scene['gameplay_version']='v31 street combat mapping; Zombies first, future PvP separate'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(dest/'changes.json').write_text(json.dumps({'source':str(source),'source_sha256':source_hash,'output':str(OUT),'new_closed_solids':len(made),'vehicles':vehicles,'changes':['Four original modelled vehicles: parked car, van, damaged car and street-end wreck','Closed west/east street boundaries and Natural Wellbeing lane gate','Entrance bollards, shallow shopfront planters and supply crates','Deep terrain backing beneath High Street surroundings'],'mode_priority':'Zombies first; possible future PvP uses the same architecture, no PvP implementation','stock_asset_candidate':'Installed veh_t7_civ_car_compact model/textures/collision found; not imported or copied into repository','engine_verified':False,'limits':['Vehicles are original preview props, not stock BO3 assets','All gate/weapon/reward markers are proposals, not functioning entities','Original Syston vehicle positions are not claimed','Terrain backing does not calibrate the junction road outline']},indent=2))
print('V31_BUILD_COMPLETE',len(made),flush=True)
