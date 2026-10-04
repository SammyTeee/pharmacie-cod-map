"""Enclose rear circulation and unfinished bar door; checkpoint v29 untouched."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath)
assert source.name=='pharmacie-syston-detail-v29.blend'
OUT=ROOT/'assets/blender/pharmacie-zombies-alley-v30.blend';assert not OUT.exists()
dest=ROOT/'recon/v30';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
protected={o.name:([tuple(o.matrix_world@v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons]) for o in scene.objects if o.type=='MESH'}
coll=bpy.data.collections.new('MAPPING v30 | Enclosed rear alley and sealed service door');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v30 | Open rear floor slabs');archive.use_fake_user=True
made=[];archived=[];basis=Matrix.Identity(4)
def mat(name,color,metal=0,rough=.8):
    m=bpy.data.materials.new('Mapping v30 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1);bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;return m
brick=bpy.data.materials['Syston v27 | weathered brick 2'];paving=bpy.data.materials['Street v17 | paving'];slate=bpy.data.materials['Street v17 | slate']
stone=mat('weathered coping',(.36,.35,.31));dark=mat('painted service metal',(.065,.095,.095),.35);wood=mat('old barricade boards',(.24,.14,.07));cream=mat('lettering ivory',(.8,.77,.65));ground=mat('surrounding earth base',(.12,.12,.105));red=mat('safety red',(.45,.055,.025));glass=mat('bulkhead frosted glass',(.68,.61,.39))
def box(name,x0,x1,y0,y1,z0,z1,m,role='scenery'):
    verts=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]);me.materials.append(m);me.update()
    o=bpy.data.objects.new('Mapping v30 | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['mapping_role']=role;o['status']='Blender geometry; engine entities/collision not yet converted';made.append(o);return o
def text(name,body,position,rotation,size=.16):
    data=bpy.data.curves.new(name,'FONT');data.body=body;data.align_x='CENTER';data.align_y='CENTER';data.size=size;data.extrude=.001;data.materials.append(cream)
    o=bpy.data.objects.new('Mapping v30 | '+name,data);coll.objects.link(o);o.location=position;o.rotation_euler=rotation;return o
def retire(name):
    o=bpy.data.objects[name];archive.objects.link(o)
    for c in list(o.users_collection):
        if c!=archive:c.objects.unlink(o)
    archived.append(name)
for name in ['Street | rear exit landing','Street v17 | Outer-left alley walkable floor','Street v17 | Alley rear route connector']:retire(name)
# Narrow L shaped route, maintained to existing rear-door approach.
box('Outer alley walkable floor',-12.41,-10.39,0,31.12,-.25,0,paving,'walkable_floor')
box('Rear turn walkable floor',-12.41,-1.53,31.12,33.13,-.25,.008,paving,'walkable_floor')
box('Rear door threshold landing',-4.10,-1.95,30.52,31.12,-.25,.008,paving,'walkable_floor')
# Deep low slab backs the terrain without coincident floor faces. Walls define access.
box('Surrounding rear ground backing',-19,17,-.1,40,-.65,-.29,ground,'terrain_backing')
box('Outer alley west brick boundary',-12.66,-12.41,.15,33.40,-.28,3.05,brick,'boundary_wall')
box('Outer alley east brick boundary',-10.39,-10.14,.15,30.86,-.28,3.05,brick,'boundary_wall')
box('Neighbour rear service infill mass',-10.14,-5.70,15.1,30.85,-.28,3.45,brick,'closed_scenery_mass')
box('Neighbour rear infill roof',-10.19,-5.65,15.05,30.9,3.45,3.57,slate)
box('Rear turn south brick boundary',-10.39,-5.66,30.86,31.12,-.28,3.05,brick,'boundary_wall')
box('Rear turn east boundary',-1.78,-1.53,31.08,33.4,-.28,3.05,brick,'boundary_wall')
# North wall has a real framed opening backed by an enclosed spawn pocket.
for name,x0,x1,z0,z1 in [('north west',-12.66,-8.5,-.28,3.05),('north east',-6.8,-1.53,-.28,3.05),('window sill',-8.5,-6.8,-.28,.72),('window lintel',-8.5,-6.8,2.42,3.05)]:
    box('Rear '+name+' brick boundary',x0,x1,33.13,33.40,z0,z1,brick,'boundary_wall')
for a,b,c,d in [(-12.68,-12.39,.15,33.42),(-10.41,-10.12,.15,30.85),(-10.40,-5.64,30.84,31.14),(-12.68,-1.51,33.11,33.42),(-1.80,-1.51,31.08,33.42)]:
    box('Boundary stone coping',a,b,c,d,3.05,3.13,stone)
box('Barricade pocket floor',-8.76,-6.54,33.40,35.48,-.28,0,paving)
box('Barricade pocket back wall',-8.76,-6.54,35.23,35.48,-.28,3.05,brick)
for x0,x1 in [(-8.76,-8.5),(-6.8,-6.54)]:box('Barricade pocket side wall',x0,x1,33.4,35.48,-.28,3.05,brick)
box('Barricade pocket ceiling',-8.76,-6.54,33.4,35.48,3.05,3.18,slate)
for x in (-8.49,-6.84):box('Barricade vertical frame',x,x+.045,33.065,33.17,.68,2.46,dark)
for z in (.70,2.42):box('Barricade horizontal frame',-8.5,-6.8,33.065,33.17,z,z+.045,dark)
for i,z in enumerate((.95,1.28,1.61,1.94,2.27)):
    o=box('Repairable window board %02d'%i,-8.53,-6.77,33.005,33.065,z,z+.13,wood,'future_zombie_barricade_visual')
    for v in o.data.vertices:v.co.z+=(v.co.x+7.65)*(.035 if i%2 else -.035)
# Utility details hug walls; retain 1.55m minimum clear width beside the bins.
for y in (7.5,20,28):
    box('Alley bulkhead backing',-12.405,-12.35,y-.16,y+.16,2.35,2.65,dark)
    box('Alley bulkhead glass',-12.35,-12.30,y-.12,y+.12,2.39,2.61,glass)
    ld=bpy.data.lights.new('Mapping v30 | alley bulkhead','AREA');ld.energy=35;ld.color=(1,.73,.43);ld.shape='DISK';ld.size=.28
    o=bpy.data.objects.new(ld.name,ld);coll.objects.link(o);o.location=(-12.28,y,2.5);o.rotation_euler=Vector((1,0,-.2)).to_track_quat('-Z','Y').to_euler()
box('Alley utility cabinet',-12.40,-12.22,25.2,26.0,.85,1.7,dark)
for y in (22.5,23.15):
    box('Shallow refuse bin body',-12.39,-12.02,y,y+.48,.02,.9,dark)
    box('Shallow refuse bin lid',-12.40,-12.00,y-.015,y+.495,.90,.96,dark)
    box('Bin handle',-12.005,-11.985,y+.14,y+.32,.73,.78,stone)
for y0,y1 in [(1,14.8),(15.2,30.5)]:box('Wall surface conduit',-10.445,-10.415,y0,y1,2.2,2.24,dark)
for y in range(2,31,4):
    box('Alley drain frame',-12.28,-12.02,y-.12,y+.12,.001,.013,dark)
    for x in (-12.23,-12.16,-12.09):box('Drain inset slots',x,x+.025,y-.09,y+.09,.013,.015,stone)
# Close the exposed right-hand bar opening with an explicit opaque service door.
j0=bpy.data.objects['Ground shell 06 | door 0 | jamb 0'];j1=bpy.data.objects['Ground shell 06 | door 0 | jamb 1']
def centre(o):return sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
a,b=centre(j0),centre(j1);c=(a+b)/2;c.z=0;t=(b-a);t.z=0;width=t.length;t.normalize();out=Vector((-t.y,t.x,0))
basis=Matrix(((t.x,out.x,0,c.x),(t.y,out.y,0,c.y),(0,0,1,0),(0,0,0,1)))
box('Closed bar service door leaf',-width/2-.025,width/2+.025,-.065,.055,0,3.10,dark,'closed_scenery_door')
for z0,z1 in ((.20,1.30),(1.48,2.86)):box('Service door recessed panel',-width/2+.13,width/2-.13,-.075,-.065,z0,z1,stone)
box('Service door handle',width/2-.22,width/2-.17,-.13,-.075,1.28,1.50,dark)
box('Service door sign plate',-.43,.43,-.085,-.076,1.91,2.20,dark)
normal=-out;rot=Matrix(((t.x,0,normal.x),(t.y,0,normal.y),(0,1,0))).to_euler()
text('Service door lettering','STAFF ONLY',basis@Vector((0,-.088,2.05)),rot,.16)
basis=Matrix.Identity(4)
# Doorway at end of turn remains open; its existing leaf/threshold are retained.
box('Rear door emergency sign plate',-3.58,-2.45,30.96,31.01,3.32,3.58,dark)
text('Rear door emergency lettering','EXIT',(-3.015,31.02,3.45),(math.pi/2,0,math.pi),.20)
# Named future-engine anchors are deliberately separate from solid geometry.
markers=bpy.data.collections.new('GAMEPLAY v30 | Rear alley proposed engine anchors');scene.collection.children.link(markers)
for name,loc,role in [('R30_Z01_rear_barricade',(-7.65,34.2,0),'Zombie spawn pocket; zone and stock barricade still need engine setup'),('R30_D01_existing_rear_exit',(-3,30.7,0),'Retained rear door; preserve engine front/rear linked-purchase behavior'),('R30_W01_alley_wall_buy',(-10.39,26.5,1.3),'Possible wall buy on supported route; no weapon prefab placed')]:
    o=bpy.data.objects.new(name,None);markers.objects.link(o);o.location=loc;o.empty_display_type='ARROWS';o.empty_display_size=.25;o['proposal']=role;o['engine_implemented']=False
def camera(name,eye,target,lens=24,ortho=None):
    cd=bpy.data.cameras.new('Review v30 | '+name);o=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(o);o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();cd.lens=lens
    if ortho:cd.type='ORTHO';cd.ortho_scale=ortho
    return o
views=[camera('01_alley_from_street',(-11.4,1,1.65),(-11.4,18,1.65)),camera('02_alley_services',(-11.4,19,1.65),(-11.4,29,1.65)),camera('03_rear_turn',(-11.4,31.9,1.65),(-3,32.1,1.65)),camera('04_rear_door',(-6.4,32.4,1.65),(-3,30.7,1.65)),camera('05_rear_barricade',(-7.65,31.7,1.65),(-7.65,34,1.65)),camera('06_closed_bar_door',(5,17,1.65),(15,17,1.65)),camera('07_rear_plan',(-7,21,45),(-7,21,0),ortho=40)]
bpy.context.view_layer.update()
for name,(vs,fs) in protected.items():
    o=bpy.data.objects[name];assert vs==[tuple(o.matrix_world@v.co) for v in o.data.vertices],name;assert fs==[tuple(p.vertices) for p in o.data.polygons],name
for o in made:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)*o.matrix_world.determinant()>0,o.name;bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
scene.camera=views[2];scene['gameplay_version']='v30 enclosed rear alley; engine conversion pending'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(dest/'changes.json').write_text(json.dumps({'source':str(source),'source_sha256':source_hash,'output':str(OUT),'new_closed_solids':len(made),'preserved_preexisting_mesh_geometry':len(protected),'archived_open_floor_slabs':archived,'clear_alley_width_m':2.02,'rear_turn_clear_width_m':2.01,'width_beside_bins_m':1.595,'changes':['Continuous narrow two-wall alley and tight rear turn','Neighbour infill shell and ground backing','Retained rear-door escape loop','Enclosed future zombie barricade pocket','Opaque bar-side service door','Wall-hugging utility cabinet, bins, drains and practical lamps'],'assumptions':['Rear surroundings and props are gameplay adaptations, not surveyed architecture','Door/barricade/spawn/wall-buy markers are proposals; no engine entities or behavior'],'radiant_rebuilt':False,'runtime_verified':False},indent=2))
print('V30_BUILD_COMPLETE',len(made),OUT,flush=True)
