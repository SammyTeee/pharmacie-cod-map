"""Close measured shell seams and finish service boundaries; preserve v32."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math,os
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
source=Path(bpy.data.filepath)
assert source.name=='pharmacie-street-frontages-v32.blend'
OUT=ROOT/'assets/blender/pharmacie-enclosure-detail-v33.blend'
assert not OUT.exists() or os.environ.get('V33_REBUILD')=='1', 'Preserve the existing checkpoint'
dest=ROOT/'recon/v33';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
coll=bpy.data.collections.new('MAPPING v33 | Shell seam closure and service detail');scene.collection.children.link(coll)
made=[]
def material(name,color,metal=0,rough=.8):
    m=bpy.data.materials.new('Mapping v33 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
    bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=m.diffuse_color
    bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    return m
brick=bpy.data.materials['Syston v27 | weathered brick 2']
plaster=material('service plaster',(.53,.49,.39));stone=material('weathered masonry coping',(.38,.37,.33))
metal=material('painted utility iron',(.055,.075,.078),.5);wood=material('rear door timber',(.18,.12,.075))
cream=material('lettering ivory',(.84,.80,.66));orange=material('road closure orange',(.64,.16,.025))
dark=material('vent recess',(.018,.025,.027));glass=material('bulkhead diffuser',(.66,.59,.39))
slate=bpy.data.materials['Street v17 | slate'];paving=bpy.data.materials['Street v17 | paving']
def mesh(name,verts,faces,mat,role='scenery'):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();me.materials.append(mat)
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new('Mapping v33 | '+name,me);coll.objects.link(ob)
    ob['mapping_role']=role;ob['engine_implemented']=False;made.append(ob);return ob
def box(name,x0,x1,y0,y1,z0,z1,mat,role='scenery'):
    assert x1>x0 and y1>y0 and z1>z0,name
    return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
                      (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],
                [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat,role)
def strip(name,a,b,width,z0,z1,mat,role='shell_seal'):
    a,b=Vector(a),Vector(b);d=b-a;d.z=0;d.normalize();n=Vector((-d.y,d.x,0))*width/2
    pts=[a-n,b-n,b+n,a+n]
    return mesh(name,[(p.x,p.y,z) for z in (z0,z1) for p in pts],
                [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat,role)
def text(name,body,loc,right,normal,size,mat):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER'
    cu.size=size;cu.extrude=.001;cu.materials.append(mat)
    ob=bpy.data.objects.new('Mapping v33 | '+name,cu);coll.objects.link(ob);ob.location=loc
    r=Vector(right);n=Vector(normal);u=Vector((0,0,1))
    ob.rotation_euler=Matrix(((r.x,u.x,n.x),(r.y,u.y,n.y),(r.z,u.z,n.z))).to_euler()
    return ob
# Original ground walls stop at 4.35m; upper walls start at 4.8m. Keep both,
# add full-thickness closure bands instead of moving the approved architecture.
for old in list(scene.objects):
    if old.type!='MESH' or not old.name.startswith('Ground shell'):
        continue
    if not any(term in old.name for term in ('wall end','| pier','| lintel')):
        continue
    vs=[old.matrix_world@v.co for v in old.data.vertices]
    low=min(v.z for v in vs);high=max(v.z for v in vs)
    mesh('Interstorey band | '+old.name,[(v.x,v.y,4.30+(v.z-low)/(high-low)*.53) for v in vs],
         [list(p.vertices) for p in old.data.polygons],plaster,'shell_seal')
first=bpy.data.objects['First | floor with corrected L stairwell opening']
outline=[first.matrix_world@first.data.vertices[i].co for i in range(9)]
for i,(a,b) in enumerate(zip(outline,outline[1:]+outline[:1])):
    strip('Upper footprint seam %02d'%i,a,b,.36,4.30,4.83,plaster)
# The ground and first floor have slightly different skewed footprints. A
# solid ground-footprint ceiling bridges the exposed edge; stair holes stay open.
floor=bpy.data.objects['Ground | continuous timber floor'];vs=[floor.matrix_world@v.co for v in floor.data.vertices]
def clip(poly,axis,bound,sign):
    result=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        da=sign*(a[axis]-bound);db=sign*(b[axis]-bound)
        if da>=0:result.append(a)
        if (da<0)!=(db<0):
            result.append(a.lerp(b,da/(da-db)))
    clean=[]
    for p in result:
        if not clean or (p-clean[-1]).length>1e-6:clean.append(p)
    if len(clean)>1 and (clean[0]-clean[-1]).length<1e-6:clean.pop()
    return clean
def subtract_rect(poly,bounds):
    x0,x1,y0,y1=bounds;inside=poly;outside=[]
    for axis,bound,sign in ((0,x0,1),(0,x1,-1),(1,y0,1),(1,y1,-1)):
        if len(inside)<3:break
        piece=clip(inside,axis,bound,-sign)
        if len(piece)>=3:outside.append(piece)
        inside=clip(inside,axis,bound,sign)
    return outside
ceiling_pieces=[]
for face in floor.data.polygons:
    if not all(abs(vs[i].z)<1e-5 for i in face.vertices):continue
    pieces=[[vs[i].copy() for i in face.vertices]]
    for bounds in ((-2.10,7.79,28.88,30.67),(5.52,7.79,24.88,29.04)):
        pieces=[part for poly in pieces for part in subtract_rect(poly,bounds)]
    for poly in pieces:
        area=abs(sum(a.x*b.y-b.x*a.y for a,b in zip(poly,poly[1:]+poly[:1])))/2
        if area<1e-5:continue
        n=len(poly)
        ob=mesh('Ground ceiling backing section %02d'%len(ceiling_pieces),
            [(p.x,p.y,z) for z in (4.30,4.54) for p in poly],
            [tuple(reversed(range(n))),tuple(range(n,n*2))]+
            [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],plaster,'ceiling_backing')
        ceiling_pieces.append(ob)
# The rear upper shell is discontinuous behind the store/stair hall. Back it
# with a solid outside wall above the door head; no new accessible room.
strip('Upper rear continuous wall',outline[3],outline[4],.26,4.78,9.20,plaster,'boundary_wall')
strip('Rear interstorey weather band',(-5.49,30.68,0),(7.81,31.04,0),.40,4.30,4.84,brick)
# Rear doorway finish and a shallow wall-side practical; no leaf across route.
for x0,x1 in ((-4.13,-4.04),(-1.97,-1.88)):
    box('Rear exit external reveal',x0,x1,30.94,31.055,.008,3.20,stone)
box('Rear exit head drip',-4.18,-1.82,30.90,31.08,3.21,3.29,stone)
box('Rear exit lamp mounting',-4.46,-4.19,30.87,30.95,2.53,2.88,metal)
box('Rear exit lamp diffuser',-4.43,-4.22,30.958,30.97,2.57,2.84,glass)
box('Rear drain channel frame',-4.03,-2.05,31.03,31.08,.010,.017,metal)
for i in range(18):
    box('Rear threshold drain slot',-3.96+i*.105,-3.915+i*.105,31.038,31.075,.017,.020,dark)
# A closed maintenance building backs the lane gate and defines its distant
# view. These service-yard forms are inferred gameplay scenery, not a survey.
box('Lane service building closed mass',44.35,49.10,-37.8,-30.03,-.38,4.10,brick,'closed_scenery_mass')
box('Lane service building roof',44.23,49.22,-37.92,-29.96,4.10,4.23,slate)
for x0,x1 in ((44.88,45.13),(47.87,48.12)):
    box('Lane continuous side boundary',x0,x1,-30.05,-13.13,-.24,3.05,brick,'boundary_wall')
    box('Lane side wall coping',x0-.025,x1+.025,-30.08,-13.13,3.05,3.13,stone)
box('Lane gate header',45.02,47.98,-29.87,-29.63,2.56,2.76,metal,'boundary_wall')
box('Lane gate bottom closure',45.13,47.87,-29.84,-29.71,-.20,.08,metal,'boundary_wall')
for x in (45.18,47.72):
    box('Gate masonry end pier',x-.13,x+.13,-30.00,-29.88,-.10,3.15,brick)
    box('Gate end pier coping',x-.16,x+.16,-30.03,-29.85,3.15,3.23,stone)
for x in (45.10,47.05):
    box('Service building high window dark backing',x,x+.90,-30.01,-29.995,2.90,3.69,dark)
    for j in range(5):
        box('Service window protective grille',x+.08+j*.18,x+.095+j*.18,-29.987,-29.97,2.91,3.68,metal)
box('Service wall conduit',45.14,45.17,-29.59,-14.6,2.22,2.26,metal)
box('Lane wall utility cabinet',45.055,45.24,-23.10,-22.50,.84,1.57,metal)
for z in (1.0,1.16,1.32):
    box('Cabinet recessed louvre',45.245,45.252,-23.02,-22.58,z,z+.035,dark)
box('Lane gate lamp plate',47.80,47.97,-29.60,-29.55,2.16,2.49,metal)
box('Lane gate lamp lens',47.83,47.94,-29.545,-29.53,2.20,2.44,glass)
for y in (-17,-24,-28):
    box('Lane flush drainage rim',45.30,45.70,y-.11,y+.11,.001,.008,metal)
    for j in range(5):
        box('Lane drainage slot',45.34+j*.066,45.37+j*.066,y-.07,y+.07,.008,.012,dark)
text('Lane maintenance notice','SERVICE ACCESS', (46.5,-29.61,2.66),(-1,0,0),(0,1,0),.12,cream)
# Add correctly oriented inside-facing plates over the reversed v31 lettering,
# and close the small gap below the boundary sheets at road level.
for name,x,side in [('West',-18.25,1),('East',60.4,-1)]:
    box(name+' boundary kick plate',x-.06,x+.06,-13.02,.10,-.22,.10,metal,'boundary_wall')
    face=x+side*.08
    box(name+' inside-facing closure sign',face-.018,face+.018,-7.85,-5.55,1.42,2.0,orange)
    text(name+' readable closure text','ROAD CLOSED',(face+side*.022,-6.7,1.73),(0,side,0),(side,0,0),.245,cream)
    for y in (-12.9,-.10):
        box(name+' boundary return footing',x-.22,x+.22,y-.15,y+.15,-.18,.16,stone)
    for y in (-7.72,-5.68):
        box(name+' sign fixing',face+side*.025-.004,face+side*.025+.004,y-.025,y+.025,1.69,1.74,metal)
bpy.context.view_layer.update()
solids=[]
for ob in made:
    bm=bmesh.new();bm.from_mesh(ob.data)
    assert all(e.is_manifold for e in bm.edges),ob.name
    assert bm.calc_volume(signed=True)>0,ob.name
    solids.append(ob.name);bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
scene['gameplay_version']='v33 enclosure seam closure and service detail; engine conversion pending'
def setup_review_views():
    scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
    scene.render.engine='CYCLES'
    for name,eye,target in [('10_lane_end',(46.5,-24,1.65),(46.5,-29.8,2)),
                            ('17_stair_seam',(6.6,29,4.49444475),(9.5,31,4.65))]:
        obj=bpy.data.objects.get('Review v33 | '+name)
        if obj is None:
            data=bpy.data.cameras.new('Review v33 | '+name)
            obj=bpy.data.objects.new(data.name,data);scene.collection.objects.link(obj)
        obj.location=eye;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler();obj.data.lens=24
        if name=='10_lane_end':scene.camera=obj
    for obj in scene.objects:obj.select_set(False)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                space=area.spaces.active;space.region_3d.view_perspective='CAMERA'
                try:space.shading.type='MATERIAL'
                except TypeError:
                    space.shading.type='SOLID';space.shading.color_type='MATERIAL'
                space.shading.use_scene_world=False;space.shading.use_scene_lights=False
setup_review_views()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(dest/'changes.json').write_text(json.dumps(dict(source=source.relative_to(ROOT).as_posix(),source_sha256=source_hash,
    output=OUT.relative_to(ROOT).as_posix(),new_closed_solids=len(solids),solids=solids,
    changes=['Ground/upstairs seam bands','Ground footprint ceiling with L stair void retained',
             'Continuous upper rear wall','Rear threshold reveals and drainage','Backed service lane and utility detail',
             'Readable inward road-closure signs and bottom kick plates'],
    provenance='Original geometry; seam fixes measured from the existing model, service scenery inferred for gameplay',
    engine_verified=False),indent=2))
print('V33_BUILD_COMPLETE',len(solids),flush=True)
