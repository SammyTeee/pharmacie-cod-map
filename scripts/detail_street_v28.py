"""Photo-led pavement/crossing details and individual frontage refinements."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath)
assert source.name=='pharmacie-syston-appearance-v27.blend'
OUT=ROOT/'assets/blender/pharmacie-syston-detail-v28.blend';assert not OUT.exists()
dest=ROOT/'recon/v28';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections.new('STREET v28 | Pavements markings and individual shops');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v28 | Superseded generic details');archive.use_fake_user=True
made=[];retired=[];basis=Matrix.Identity(4);current='F012'
protected={o.name:([tuple(o.matrix_world@v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons]) for o in scene.objects if o.type=='MESH'}
hash0=hashlib.sha256(source.read_bytes()).hexdigest()
def mat(name,color):
    m=bpy.data.materials.new('Syston v28 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1);m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*color,1);m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.8;return m
yellow=mat('worn double yellow',(.69,.46,.055));white=bpy.data.materials['Street v17 | road white'];metal=bpy.data.materials['Syston v27 | outdoor metal'];pale=bpy.data.materials['Syston v27 | warm white window paint'];glass=bpy.data.materials['Syston v27 | reflective charcoal glazing'];pink=mat('buff pink tactile paving',(.47,.29,.22));joint=mat('kerb joint',(.16,.15,.13));green=mat('leaf green',(.10,.21,.055));terracotta=mat('planter terracotta',(.25,.13,.075));paint=mat('GLO white masonry',(.70,.69,.64));blue=mat('traffic sign blue',(.018,.065,.35))
def mesh(name,verts,faces,m):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new('Syston v28 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['catalogue_id']=current;o['status']='Photo-led approximate exterior detail, Blender only';made.append(o);return o
def box(name,x0,x1,y0,y1,z0,z1,m):
    return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)
def retire(o):
    archive.objects.link(o)
    for c in list(o.users_collection):
        if c!=archive:c.objects.unlink(o)
    retired.append(o.name)
def beam(name,a,b,width,z0,z1,m):
    a,b=Vector(a),Vector(b);d=(b-a).normalized();n=Vector((-d.y,d.x))*width/2;ps=[a-n,b-n,b+n,a+n]
    return mesh(name,[(p.x,p.y,z) for z in (z0,z1) for p in ps],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)
path=[Vector(p) for p in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']];lengths=[0]
for a,b in zip(path,path[1:]):lengths.append(lengths[-1]+(b-a).length)
def point(s,offset=0):
    s=max(0,min(s,lengths[-1]-.001));i=next(i for i in range(len(path)-1) if lengths[i+1]>=s);u=(path[i+1]-path[i]).normalized();return path[i]+u*(s-lengths[i])+Vector((-u.y,u.x))*offset
def streetframe(s,side=1,offset=0):
    p=point(s,side*offset);u=(point(s+.02)-point(s)).normalized();n=Vector((-u.y,u.x))*side;x=Vector((n.y,-n.x));return Matrix(((x.x,n.x,0,p.x),(x.y,n.y,0,p.y),(0,0,1,0),(0,0,0,1)))
# Continuous yellow edge lining, leaving zebra controlled area and Brookside mouth clear.
current='F016';basis=Matrix.Identity(4)
for side in (-1,1):
    for start in range(42,int(lengths[-1])-1,2):
        if 204<=start<=225:continue
        for offset in (3.62,3.83):beam('double yellow edge line',point(start,side*offset),point(start+2,side*offset),.095,-.074,-.069,yellow)
# Lead-in zigzags and dotted crossing boundaries, matching photo rather than invented road wear.
current='F012'
for side in (-1,1):
    for s in range(18,40,4):
        beam('crossing zigzag',point(s,side*3.35),point(s+2,side*2.85),.10,-.074,-.067,white)
        beam('crossing zigzag',point(s+2,side*2.85),point(s+4,side*3.35),.10,-.074,-.067,white)
for s in (11.9,16.1):
    for offset in [i*.5 for i in range(-7,8)]:
        basis=streetframe(s,1,offset);box('crossing dotted boundary',-.10,.10,-.10,.10,-.073,-.066,white)
# Tactile landings are surface detailing; saved drop/ramp dimensions remain estimates.
for side in (-1,1):
    basis=streetframe(14,side,5.0)
    box('tactile landing',-1.9,1.9,-.80,.80,.002,.016,pink)
    for x in [i*.15 for i in range(-12,13)]:
        for y in [i*.15 for i in range(-5,6)]:box('tactile raised blister',x-.023,x+.023,y-.023,y+.023,.016,.023,pink)
    # A sphere replaces the crude beacon cube; pole retained.
    beacon=next(o for o in scene.objects if o.name.startswith('Syston v25 | F012 | yellow beacon') and (o.matrix_world.translation-Vector((*point(14,side*4.85),0))).length<1)
    bb=beacon.matrix_world.copy();retire(beacon)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.19);o=bpy.context.object;o.name='Syston v28 | F012 | spherical Belisha beacon';o.matrix_world=bb@Matrix.Translation((0,0,3.01));o.data.materials.append(yellow)
    for c in list(o.users_collection):c.objects.unlink(o)
    coll.objects.link(o);made.append(o)
# Kerb segment joints and inset drain grilles, clear of branch gap.
current='F015'
for side in (-1,1):
    for s in range(20,int(lengths[-1])-2):
        if 205<=s<=225:continue
        basis=streetframe(s,side,4.08);box('kerb segment joint',-.007,.007,-.079,.079,.016,.018,joint)
    for s in range(45,int(lengths[-1])-2,25):
        if 204<=s<=225:continue
        basis=streetframe(s,side,3.69);box('gully frame',-.30,.30,-.19,.19,-.074,-.067,metal)
        for i in range(9):box('gully slot',-.26+i*.064,-.23+i*.064,-.15,.15,-.066,-.064,joint)
    for s in (61,123,183,242):
        basis=streetframe(s,side,5.2);box('pavement utility cover frame',-.32,.32,-.23,.23,.002,.009,metal);box('pavement utility cover inset',-.29,.29,-.20,.20,.009,.011,joint)
        for x in (-.21,.21):box('utility cover lifting slot',x-.04,x+.04,-.015,.015,.012,.014,metal)
current='F013';basis=Matrix.Identity(4)
# Three short tangent arrows around painted circle indicate clockwise circulation.
centre=path[0]
for theta in (0,2*math.pi/3,4*math.pi/3):
    p=centre+Vector((math.cos(theta),math.sin(theta)))*2.5;t=Vector((math.sin(theta),-math.cos(theta)))
    beam('roundabout circulating arrow shaft',p-t*.5,p+t*.45,.16,-.072,-.066,white)
    for sign in (-1,1):beam('roundabout arrow head',p+t*.45,p+t*.03+Vector((-t.y,t.x))*sign*.30,.14,-.072,-.066,white)
# Photo-led individual fascia/frame treatments rather than shared stock colours.
groups={ident:[o for o in scene.objects if o.get('catalogue_id')==ident] for ident in ('B015','B032','B033','B045')}
for ident,group in groups.items():
    current=ident;anchor=next(o for o in group if 'upper facade' in o.name);basis=anchor.matrix_world.copy();xs=[v.co.x for v in anchor.data.vertices];x0,x1=min(xs),max(xs);w=x1-x0
    if ident=='B045':
        font=next(o for o in group if o.type=='FONT' and o.data.body=='COSTA COFFEE');font.data.align_y='CENTER';font.data.size=.9;font.scale=Vector((1,1,1));bpy.context.view_layer.update();bb=font.bound_box;fw=max(v[0] for v in bb)-min(v[0] for v in bb);fh=max(v[1] for v in bb)-min(v[1] for v in bb);font.scale*=min(w*.80/fw,.52/fh);continue
    for o in group:
        if o.type=='MESH' and any(s in o.name for s in ('display bay upright','display bay rail','display bay mullion','display bay transom','recessed entrance upright','recessed entrance rail','upper sash upright','upper sash rail','upper sash mullion','upper sash transom')):o.data.materials[0]=pale if ident!='B032' or 'upper sash' not in o.name else metal
        if o.type=='MESH' and ident=='B032' and any(s in o.name for s in ('fascia','front pilaster')):o.data.materials[0]=pale
        if o.type=='FONT' and ident in ('B032','B033'):o.data.materials[0]=metal
    if ident=='B033':
        box('white painted return wall',x0-.015,x0+.025,.02,9.8,0,4.05,paint)
        box('painted blank side of frontage',x0,x0+w*.42,-.23,-.19,.38,3.36,paint)
        for x in (x0+w*.20,x0+w*.48):
            box('small wall vent',x-.12,x+.12,-.26,-.23,.48,.64,metal)
        box('wall utility cable',x0,x1,-.24,-.22,4.40,4.43,metal)
    if ident=='B015':
        # Rectangular windows with blinds and characteristic bright display panels.
        for o in group:
            if o.type=='MESH' and 'upper sash glass' in o.name:
                vx=[v.co.x for v in o.data.vertices];vz=[v.co.z for v in o.data.vertices];a,c=min(vx),max(vx);z0,z1=min(vz),max(vz)
                for j in range(8):box('visible upper blind slat',a+.05,c-.05,-.195,-.177,z1-.12-j*.14,z1-.10-j*.14,pale)
            if o.type=='MESH' and 'display bay glass' in o.name:
                vx=[v.co.x for v in o.data.vertices];a,c=min(vx),max(vx);box('green window advert inset',a+.12,min(c-.12,a+.95),-.21,-.19,.85,2.25,bpy.data.materials['Syston v25 | retail green'])
    if ident=='B032':
        # Correct central entry rhythm from native270. Archive generic ground glazing.
        for o in list(group):
            if o.type=='MESH' and any(s in o.name for s in ('display bay','recessed entrance','door kickplate','door handle','lower plinth')):retire(o)
        brick=bpy.data.materials['Syston v27 | weathered brick 2']
        box('brick shop base',x0,x1,-.10,.7,0,.70,brick)
        for a,c in ((x0+.16,-.72),(.72,x1-.16)):
            if c<=a:continue
            box('broad display glass',a,c,-.13,-.06,.75,3.28,glass)
            for xx in (a,c):box('display white upright',xx-.045,xx+.045,-.19,-.05,.71,3.34,pale)
            for zz in (.75,3.28):box('display white rail',a,c,-.19,-.05,zz-.045,zz+.045,pale)
        box('central light door leaf',-.59,.59,.25,.32,.08,3.27,pale);box('central door glass',-.48,.48,.21,.25,.78,3.14,glass)
        for xx in (-.63,.63):box('central door reveal',xx-.045,xx+.045,-.16,.34,.05,3.34,pale)
        box('central door transom',-.58,.58,.16,.22,2.63,2.70,pale);box('central door handle',.39,.42,.11,.17,1.13,1.53,metal)
        for o in group:
            if o.type=='MESH' and 'upper sash glass' in o.name:
                vx=[v.co.x for v in o.data.vertices];vz=[v.co.z for v in o.data.vertices];a,c=min(vx),max(vx);z0,z1=min(vz),max(vz)
                box('upper pale lintel',a-.1,c+.1,-.19,.03,z1+.03,z1+.17,pale)
                for t in (1/3,2/3):box('upper multi pane rail',a,c,-.19,-.135,z0+(z1-z0)*t-.02,z0+(z1-z0)*t+.02,metal)
        for x in (-.98,.98):
            box('topiary pot',x-.18,x+.18,-.60,-.24,.02,.40,terracotta)
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.30);o=bpy.context.object;o.name='Syston v28 | B032 | rounded topiary';o.matrix_world=basis@Matrix.Translation((x,-.42,.67));o.data.materials.append(green)
            for c in list(o.users_collection):c.objects.unlink(o)
            coll.objects.link(o);made.append(o)
bpy.context.view_layer.update()
for name,(vs,fs) in protected.items():
    o=bpy.data.objects[name];assert vs==[tuple(o.matrix_world@v.co) for v in o.data.vertices],name;assert fs==[tuple(p.vertices) for p in o.data.polygons],name
for o in made:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0,o.name;bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==hash0
# Road overhead checks include additions; no road furniture was added in carriageway.
deps=bpy.context.evaluated_depsgraph_get();checks=0
for s in range(18,min(int(lengths[-1]),278),2):
    for offset in (-2.7,0,2.7):
        p=point(s,offset);hit,loc,n,idx,o,m=scene.ray_cast(deps,Vector((*p,1.7)),Vector((0,0,1)),distance=12);assert not hit,('Road overhead obstruction',s,offset,o.name);checks+=1
def camera(name,eye,target):
    cd=bpy.data.cameras.new('Review v28 | '+name);o=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(o);o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();cd.lens=28;return o
basis=streetframe(24,1,0);eye=basis@Vector((0,0,1.7));target=Vector((*point(9),1.5));crosscam=camera('crossing',eye,target)
g=next(o for o in scene.objects if o.name.startswith('Syston v25 | B032 | upper facade'));bs=g.matrix_world;shopcam=camera('amy_clarke',bs@Vector((2,-9,1.7)),bs@Vector((0,0,3.4)))
scene.camera=crosscam;bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(dest/'validation.json').write_text(json.dumps({'input_sha256':hash0,'checkpoint':str(OUT.relative_to(ROOT)),'new_closed_solids':len(made),'preserved_existing_mesh_geometry':len(protected),'archived_details':retired,'road_overhead_samples':checks,'photo_basis':['F012:00273,00283,00284','F013:00286-00295','B032:00270,00282','B033:00273,00294','B015:00099,00114','B045:00233'],'limits':['Road and parcel dimensions remain estimated','Drains/utility covers indicative placement, not surveyed','Tactile landings added; existing curved kerbs and dropped crossings still need reconstruction','Only Costa/Amy Clarke/Specsavers/GLO individually refined; remaining frontages still need comparable detail','Blender only; no engine export or runtime test']},indent=2)+'\n')
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=1400;scene.render.resolution_y=950;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
ld=bpy.data.lights.new('Temporary v28 daylight','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name,cam in [('01_crossing',crosscam),('02_amy_clarke',shopcam),('03_costa',bpy.data.objects['Review v25 | 02_costa_and_town_square']),('04_street',bpy.data.objects['Review v25 | 06_bridge_player'])]:
    scene.camera=cam;scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print('V28_COMPLETE',OUT)
