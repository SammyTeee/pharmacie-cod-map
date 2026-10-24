"""Detailed Taraj restaurant and bridge/brook pass; preserve v25 and photo bytes."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-taraj-interior-bridge-v26.blend'
assert Path(bpy.data.filepath).name=='pharmacie-syston-street-v25.blend';assert not OUT.exists()
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
refs=[ROOT/'references'/n for n in ('taraj interiopr.png','taraj bar inside right inside of the left side door -.png','inside taraj THIS MAN MUST FEATUURE SAT IN ONE OF THE BOOTHS.png')]
refhash={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in refs}
archive=bpy.data.collections.new('ARCHIVE v25 | Superseded bridge and Taraj closures');archive.use_fake_user=True;retired=[]
def retire(ob):
    archive.objects.link(ob)
    for c in list(ob.users_collection):
        if c!=archive:c.objects.unlink(ob)
    retired.append(ob.name)
taraj_names=('shop rear closure','passage dividing pier','left recessed entrance door','left entry glazing','right door','right door raised panel','door handle')
waterob=next(o for o in scene.objects if 'F003 | water under bridge' in o.name);bridgebasis=waterob.matrix_world.copy()
for o in list(scene.objects):
    if o.get('catalogue_id')=='F003' or o.name=='Street v22 | Brook approximate course' or (o.name.startswith('Taraj v23 | ') and any(o.name.split(' | ',1)[1].split('.')[0]==n for n in taraj_names)):retire(o)
protected={o.name:([tuple(o.matrix_world@v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons]) for o in scene.objects if o.type=='MESH' and not o.name.startswith('Syston v25 | B014 |') and not o.name.startswith('Street v22 | Melton pavement') and not o.name.startswith('Street v22 | Melton kerb') and o.name!='Street v22 | Brookside road branch'}
coll=bpy.data.collections.new('DETAIL v26 | Bridge brook and Taraj restaurant')
for s in bpy.data.scenes:
    if 'STREET v25 | Catalogue-led Syston scenery' in s.collection.children:s.collection.children.link(coll)
made=[];basis=bridgebasis.copy();area='Bridge'
def material(name,color,rough=.65,metal=0,emission=0):
    m=bpy.data.materials.new('Detail v26 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    if emission:bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=emission
    return m
stone=material('weathered pale concrete',(.49,.49,.43));iron=material('galvanised rail',(.43,.46,.44),.35,.65)
earth=material('bank earth',(.18,.125,.065));grass=material('bank vegetation',(.105,.20,.055));leaf=material('tree foliage',(.08,.17,.035));wood=material('dark polished hardwood',(.12,.038,.013),.26)
gold=material('honey timber',(.43,.21,.047),.24,.12);brass=material('brass details',(.60,.40,.12),.25,.75)
linen=material('ivory linen',(.87,.82,.69));paper=material('folded napkin',(.89,.85,.76));cream=material('damask wallpaper',(.66,.54,.35));cloth=material('floral upholstery',(.24,.15,.075));carpet=material('restaurant carpet',(.10,.075,.043),.95)
dark=material('dark backing',(.016,.021,.018));water=material('brook water',(.10,.22,.18),.12)
glass=material('glass',(.55,.67,.64),.12);bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.65
frost=material('etched pale lines',(.72,.78,.65),.4,emission=.12);warm=material('warm lamp',(.95,.58,.22),.3,emission=3)
purple=material('bar violet LED',(.5,.018,.8),.3,emission=3);bottle_mats=[material('bottle '+str(i),c,.22) for i,c in enumerate([(.06,.17,.065),(.36,.11,.025),(.12,.20,.26),(.40,.27,.08)])]
def pattern(m,colors,scale=7):
    n=m.node_tree.nodes;l=m.node_tree.links;t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=scale;t.inputs['Detail'].default_value=3
    coord=n.new('ShaderNodeTexCoord');l.new(coord.outputs['Object'],t.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*colors[0],1);r.color_ramp.elements[1].color=(*colors[1],1);l.new(t.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
pattern(cream,[(.42,.31,.17),(.74,.66,.47)],9);pattern(cloth,[(.07,.055,.025),(.37,.27,.10)],12);pattern(carpet,[(.055,.045,.025),(.17,.12,.067)],38)
pattern(gold,[(.19,.062,.012),(.60,.35,.095)],4);pattern(earth,[(.085,.060,.029),(.26,.18,.07)],8)
def mesh(name,verts,faces,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();me.materials.append(mat)
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new('Detail v26 | '+area+' | '+name,me);coll.objects.link(ob);ob.matrix_world=basis.copy();made.append(ob);ob['status']='Blender detail; engine conversion pending';return ob
def box(name,x0,x1,y0,y1,z0,z1,m):
    assert x1>x0 and y1>y0 and z1>z0,name
    return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)
def lathe(name,x,y,z,profile,m,segments=16):
    vs=[(x+r*math.cos(i*2*math.pi/segments),y+r*math.sin(i*2*math.pi/segments),z+h) for r,h in profile for i in range(segments)]
    faces=[tuple(reversed(range(segments))),tuple(range((len(profile)-1)*segments,len(profile)*segments))]
    for j in range(len(profile)-1):
        for i in range(segments):a=j*segments+i;b=j*segments+(i+1)%segments;faces.append((a,b,b+segments,a+segments))
    ob=mesh(name,vs,faces,m)
    for p in ob.data.polygons:p.use_smooth=True
    return ob
def tube(name,pts,m,r=.012):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=r;cu.bevel_resolution=2;cu.use_fill_caps=True
    s=cu.splines.new('POLY');s.points.add(len(pts)-1)
    for p,v in zip(s.points,pts):p.co=(*v,1)
    cu.materials.append(m);ob=bpy.data.objects.new('Detail v26 | '+area+' | '+name,cu);coll.objects.link(ob);ob.matrix_world=basis.copy();made.append(ob);return ob
def sphere(name,x,y,z,rx,ry,rz,m):
    prof=[(max(.001,math.sin(t*math.pi/12)), -math.cos(t*math.pi/12)) for t in range(13)]
    ob=lathe(name,0,0,0,prof,m,20);ob.matrix_world=basis@Matrix.Translation((x,y,z))@Matrix.Diagonal((rx,ry,rz,1));return ob
def label(name,body,x,y,z,size,m,rot=math.pi/2):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.001;cu.materials.append(m)
    ob=bpy.data.objects.new('Detail v26 | '+area+' | '+name,cu);coll.objects.link(ob);ob.matrix_world=basis@Matrix.Translation((x,y,z))@Matrix.Rotation(rot,4,'X');made.append(ob);return ob
def light(name,x,y,z,power,color,size=1):
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.color=color;ld.shape='DISK';ld.size=size
    ob=bpy.data.objects.new('Detail v26 | '+area+' | '+name,ld);coll.objects.link(ob);ob.matrix_world=basis@Matrix.Translation((x,y,z));made.append(ob);return ob

# Continuous deeper channel, bridge supports, separate bank terrain.
box('bridge soffit deck',-5.5,5.5,-6.45,6.45,-.48,-.31,stone)
for x in (-3.4,3.4):box('channel abutment',x-.35,x+.35,-6.45,6.45,-1.85,-.40,stone)
box('continuous watercourse',-1.65,1.65,-45,42,-1.68,-1.52,water)
box('river bed',-1.85,1.85,-45,42,-1.95,-1.80,earth)
for sign in (-1,1):
    for y0,y1 in ((-45,-6.5),(6.5,42)):
        xs=[sign*1.65,sign*4.8];zs=[-1.55,-.06]
        mesh('sloping bank',[(xs[0],y0,-1.95),(xs[1],y0,-1.95),(xs[1],y1,-1.95),(xs[0],y1,-1.95),(xs[0],y0,zs[0]),(xs[1],y0,zs[1]),(xs[1],y1,zs[1]),(xs[0],y1,zs[0])],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],grass)
for side in (-1,1):
    y=side*5.5
    box('pale parapet base',-5.4,5.4,y-.18,y+.18,-.20,.14,stone)
    for x in (-5.2,5.2):box('rail end post',x-.045,x+.045,y-.05,y+.05,.12,1.22,iron)
    for i in range(43):
        x=-5.16+i*.246;box('vertical railing',x-.014,x+.014,y-.025,y+.025,.14,1.20,iron)
    for z in (.20,1.18):box('rail horizontal',-5.25,5.25,y-.04,y+.04,z,z+.045,iron)
    label('brook notice','BROOK',2.8,y-side*.065,.60,.10,dark)
for sign in (-1,1):
    for j,y in enumerate((-13,-23,-35,13,23,35)):
        x=sign*(4.6+(j%2)*.8)
        lathe('bank tree trunk',x,y,0,[(.17,0),(.11,2.8),(.045,4.1)],wood)
        for k in range(3):sphere('tree canopy',x+(k-1)*.65,y+(k%2)*.65,3.2+k*.38,1.2,1.1,1.25,leaf)
        for k in range(4):sphere('bank shrub',sign*(2.5+k*.45),y+1.3, -.3+k*.10,.55,.6,.45,grass)
# Photographed parking context, deliberately rough dimensions.
box('parking hardstanding',5.2,25,10,35,-.22,-.05,bpy.data.materials['Street v17 | asphalt'])
for x in range(7,24,3):box('parking bay line',x,x+.08,12,18,-.045,-.035,bpy.data.materials['Street v17 | road white'])
for y in range(12,35):box('parking fence upright',5.1,5.14,y,y+.035,-.05,1.1,iron)
box('parking fence rail',5.07,5.16,11,35,1.06,1.11,iron)
for x,y in ((-5.0,-8),(5.0,8)):
    lathe('green heritage column',x,y,0,[(.12,0),(.12,.22),(.06,.3),(.045,4.8)],material('heritage green '+str(x),(.045,.15,.065)))
    tube('decorative lamp bow',[(x+.85*math.cos(t*math.pi/20),y,4.5+.27*math.sin(t*math.pi/20)) for t in range(21)],iron,.018)
    sphere('lamp globe',x,y,4.85,.14,.14,.17,warm)

# Remove physical B014/side-road intersection with a buffered road cutter.
branch=bpy.data.objects['Street v22 | Brookside road branch'];vs=[branch.matrix_world@v.co for v in branch.data.vertices];a=(vs[0]+vs[3])/2;b=(vs[1]+vs[2])/2
direction=(b-a).normalized();cross=Vector((-direction.y,direction.x,0));cutbasis=Matrix(((cross.x,direction.x,0,a.x),(cross.y,direction.y,0,a.y),(0,0,1,0),(0,0,0,1)))
oldbasis=basis;basis=cutbasis
cutter=box('temporary access clearance cutter',-3.5,3.5,-1,(b-a).length+1,-.45,12,dark)
cut_names=[]
for ob in list(scene.objects):
    if ob.type!='MESH' or not (ob.name.startswith('Syston v25 | B014 |') or ob.name.startswith(('Street v22 | Melton pavement','Street v22 | Melton kerb'))):continue
    # Closed boolean cutter keeps photographed facade, chamfers only intersecting rear.
    ob.data=ob.data.copy();bpy.context.view_layer.objects.active=ob
    mod=ob.modifiers.new('Side access clearance','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name);cut_names.append(ob.name)
made.remove(cutter);retire(cutter);basis=oldbasis
branch.data=branch.data.copy()
for v in branch.data.vertices:
    if v.co.z>-.10:v.co.z+=.006

# Taraj local coordinates: retained opposite-road exterior, x across facade,
# positive y into restaurant. Main floor fits the former 8.8x13.85m closure.
area='Taraj';r22=json.loads((ROOT/'recon/v22/validation.json').read_text());p=[Vector(x) for x in r22['melton_centreline']];u=(p[-2]-p[-3]).normalized();out=Vector((-u.y,u.x));front=Vector(json.loads((ROOT/'recon/v24/validation.json').read_text())['new_front'])
basis=Matrix(((u.x,out.x,0,front.x),(u.y,out.y,0,front.y),(0,0,1,0),(0,0,0,1)));tarajbasis=basis.copy()
box('carpet floor',-3,5.8,1.15,15,-.16,.025,carpet)
box('restaurant rear wall',-3,5.8,14.80,15,0,3.40,cream)
box('left wall before entry',-3.3,-3.0,0,4.1,0,3.4,cream)
box('left wall after entry',-3.3,-3.0,6.1,15,0,3.4,cream)
box('entry header',-3.3,-3.0,4.1,6.1,2.65,3.4,cream)
box('passage open door',-5.65,-5.56,3.9,5.30,.05,2.6,wood)
for y in (4.1,6.1):box('entry frame',-3.36,-2.94,y-.06,y+.06,0,2.70,wood)
box('right wall damask lining',5.72,5.79,1.15,14.80,.20,3.30,cream)
box('left wall damask lining',-2.99,-2.94,6.1,14.80,.20,3.30,cream)
for x in (-2.92,5.70):
    box('skirting',x,x+.045,1.15,14.80,.025,.16,wood)
    box('picture rail',x,x+.035,1.15,14.80,2.45,2.51,gold)
# Closed front right door reinstated in the new shell; passage entry is open.
box('front closed brown door',3.85,5.5,1.03,1.14,.03,2.85,wood)
for z in (.45,1.5,2.4):box('front raised door panel',4.02,5.33,.99,1.02,z-.3,z+.3,wood)
# Close ceiling under retained upper-floor mass, add individual glossy slats.
box('ceiling backing',-3,5.8,1.15,15,3.20,3.36,wood)
for i in range(68):
    y=1.18+i*.202;box('glossy ceiling board',-2.97,5.77,y,y+.184,3.15,3.21,gold)
for y in (6.4,10.8):
    box('ceiling AC cassette',.55,2.55,y-.46,y+.46,3.02,3.16,linen)
    for i in range(12):box('AC louvre',.67,2.43,y-.35+i*.055,y-.325+i*.055,2.99,3.03,cream)
for y in (3.0,5.5,8.0,10.5,13.0):
    for x in (-1.0,4.0):
        lathe('downlight bezel',x,y,3.11,[(.12,0),(.12,.04)],brass)
        lathe('downlight lens',x,y,3.10,[(.08,0),(.08,.012)],warm)
        light('ceiling practical',x,y,3.06,65,(1,.72,.42),.75)
box('central structural column',1.32,1.68,8.80,9.20,.025,3.16,cream)
box('column capital',1.25,1.75,8.73,9.27,2.65,2.83,gold)
label('column table number','02',1.5,8.72,2.48,.085,wood)

def twistpost(x,y):
    n=20;rings=44;vs=[]
    for j in range(rings):
        z=1.10+j*1.45/(rings-1)
        for i in range(n):
            t=i*math.tau/n;rad=.065+.014*math.cos(4*t-z*10);vs.append((x+rad*math.cos(t),y+rad*math.sin(t),z))
    faces=[tuple(reversed(range(n))),tuple(range((rings-1)*n,rings*n))]
    for j in range(rings-1):
        for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    mesh('carved spiral booth column',vs,faces,wood)
    for z in (1.08,2.50):lathe('column collar',x,y,z,[(.10,0),(.10,.08),(.075,.12)],wood)

def setting(x,y):
    lathe('dinner plate',x,y,.797,[(.14,0),(.16,.009),(.16,.022),(.12,.025),(.10,.012)],linen,20)
    lathe('side plate',x+.20,y+.08,.799,[(.075,0),(.085,.01),(.07,.018)],linen)
    mesh('folded napkin',[(x-.065,y-.055,.827),(x+.065,y-.055,.827),(x,y+.075,.827),(x,y,.995)],[(0,2,1),(0,1,3),(1,2,3),(2,0,3)],paper)
    lathe('wine glass',x-.20,y+.08,.800,[(.038,0),(.042,.008),(.010,.025),(.009,.10),(.04,.12),(.056,.18),(.055,.23),(.048,.23),(.043,.18),(.005,.12)],glass)
    box('fork handle',x-.20,x-.186,y-.18,y-.02,.80,.81,iron)
    for j in range(3):box('fork tine',x-.204+j*.008,x-.200+j*.008,y-.03,y+.01,.80,.808,iron)
    box('knife',x+.185,x+.20,y-.18,y+.045,.80,.812,iron)

def table(name,x0,x1,y0,y1):
    box(name+' tabletop',x0,x1,y0,y1,.73,.78,wood);box(name+' linen top',x0-.02,x1+.02,y0-.02,y1+.02,.78,.795,linen)
    for x in (x0+.12,x1-.12):
        for y in (y0+.12,y1-.12):box(name+' leg',x-.035,x+.035,y-.035,y+.035,.025,.73,wood)
    for x in (x0-.02,x1+.015):box(name+' cloth drop',x,x+.008,y0,y1,.46,.785,linen)
    for y in (y0-.02,y1+.012):box(name+' cloth drop',x0,x1,y,y+.008,.46,.785,linen)

def chair(x,y,facing):
    box('chair cushion',x-.22,x+.22,y-.23,y+.23,.43,.51,cloth)
    for xx in (x-.19,x+.19):
        for yy in (y-.19,y+.19):box('chair hardwood leg',xx-.025,xx+.025,yy-.025,yy+.025,.025,.45,wood)
    # Chairs facing across the banquet have their backs away from the tabletop.
    bx=x-facing*.23
    box('upholstered high chair back',bx-.04,bx+.04,y-.21,y+.21,.51,1.22,cloth)
    for yy in (y-.23,y+.23):box('chair carved back upright',bx-.045,bx+.045,yy-.027,yy+.027,.45,1.28,wood)
    box('chair crown',bx-.055,bx+.055,y-.25,y+.25,1.21,1.30,wood)
    for k in range(5):sphere('chair brocade petal',bx-facing*.049,y+.055*math.sin(k*math.tau/5),.91+.055*math.cos(k*math.tau/5),.006,.04,.035,gold)

# Four booth bays per side; all furniture sits outside two continuous aisles.
for side in (-1,1):
    x0,x1=(-2.75,-.75) if side==-1 else (3.65,5.55)
    for j,y in enumerate((5.5,7.75,10.0,12.25)):
        for yy in (y-.96,y+.96):
            box('booth bench base',x0,x1,yy-.22,yy+.22,.05,.43,wood)
            box('booth upholstered seat',x0+.03,x1-.03,yy-.24,yy+.24,.43,.53,cloth)
            box('booth upholstered back',x0,x1,yy-.06,yy+.06,.53,1.04,cloth)
        table('booth table',x0+.12,x1-.12,y-.52,y+.52)
        for xx in (x0+.42,x1-.42):
            setting(xx,y-.28);setting(xx,y+.28)
        # Shared glass divider on outer end of each bay; glass and etched motifs.
        yy=y+1.12;box('booth dark lower divider',x0,x1,yy-.06,yy+.06,.06,1.13,wood)
        box('etched glass partition',x0+.08,x1-.08,yy-.016,yy+.016,1.16,2.49,glass)
        for xx in (x0+.06,x1-.06):twistpost(xx,yy)
        box('booth top beam',x0-.06,x1+.06,yy-.09,yy+.09,2.51,2.66,wood)
        # Stepped/scalloped arched header, following the repeated photo silhouette.
        for k in range(11):
            xx=x0+k*(x1-x0)/11;z=2.70+.30*math.sin((k+.5)*math.pi/11)
            box('scalloped arch header',xx,xx+(x1-x0)/11+.001,yy-.055,yy+.055,z,3.14,cream)
        label('booth number',str(j+1+(0 if side==-1 else 4)),x1-.17,yy-.10,2.62,.08,linen)
        # Fine white linework substitutes for artwork; photo overlays are not baked.
        for k in range(3):
            cx=x0+.4+k*(x1-x0-.8)/2
            tube('etched paisley',[(cx+.12*math.sin(t*math.tau/32),yy-.022,1.77+.40*math.cos(t*math.tau/32)+.12*math.sin(t*math.tau/32)) for t in range(33)],frost,.002)
            for petal in range(5):
                t=petal*math.tau/5;tube('etched flower petal',[(cx+.13*math.cos(t)+.075*math.cos(q*math.tau/20),yy-.023,2.13+.13*math.sin(t)+.08*math.sin(q*math.tau/20)) for q in range(21)],frost,.0018)
table('banquet front',1.05,1.95,4.75,8.75);table('banquet rear',1.05,1.95,9.25,13.45)
for y in (5.25,6.35,7.5,8.25,9.75,10.85,12.0,13.0):
    for x,f in ((.61,1),(2.39,-1)):chair(x,y,f)
    setting(1.28,y);setting(1.73,y)
for x,y in ((1.50,6.90),(1.50,11.40)):
    lathe('table vase',x,y,.795,[(.045,0),(.06,.06),(.023,.16),(.025,.18)],linen)
    tube('flower stem',[(x,y,.95),(x+.02,y,1.10)],grass,.003)
    for j in range(6):sphere('table flower petal',x+.027*math.cos(j*math.tau/6),y+.027*math.sin(j*math.tau/6),1.10,.025,.025,.012,paper)

# Bar just inside entrance: wood cabinet, chilled bottles, optics, mirror and POS.
box('bar cabinet',-2.60,-.90,1.60,3.90,.025,.96,wood)
box('bar marble countertop',-2.68,-.80,1.53,3.97,.96,1.035,material('dark mottled bar top',(.12,.095,.077),.22))
for y0 in (1.70,2.80):
    box('bar fridge inset',-.915,-.902,y0,y0+.90,.13,.85,dark)
    box('bar fridge glazing',-.89,-.875,y0,y0+.90,.15,.83,glass)
    for z in (.25,.53):box('fridge shelf',-1.10,-.895,y0,y0+.9,z,z+.016,iron)
    box('fridge door pull',-.87,-.845,y0+.81,y0+.83,.38,.64,brass)
    for k in range(5):
        for z in (.26,.55):lathe('chilled drink bottle',-1.00,y0+.10+k*.16,z,[(.035,0),(.038,.13),(.020,.17),(.013,.21)],bottle_mats[k%4],12)
box('bar back wallpaper',-2.89,-2.82,1.35,4.20,1.06,2.93,cream)
box('mirror backing',-2.80,-2.78,1.52,2.7,1.12,2.45,iron)
for z in (1.16,1.71):
    box('bar glass shelf',-2.78,-2.27,1.48,3.88,z,z+.028,glass)
    box('violet shelf strip',-2.28,-2.26,1.50,3.88,z+.04,z+.058,purple)
for j in range(8):
    yy=1.60+j*.30
    ob=lathe('inverted optic bottle',0,0,0,[(.045,0),(.065,.08),(.065,.30),(.028,.38),(.019,.46)],bottle_mats[j%4])
    ob.matrix_world=basis@Matrix.Translation((-2.52,yy,2.81))@Matrix.Rotation(math.pi,4,'X')
    box('optic bracket',-2.81,-2.43,yy-.035,yy+.035,2.16,2.22,wood)
    sphere('optic dispenser',-2.48,yy,2.15,.06,.06,.055,dark)
    lathe('backbar bottle',-2.50,yy,1.20,[(.05,0),(.06,.22),(.032,.28),(.025,.39)],bottle_mats[(j+1)%4])
    lathe('shelf tumbler',-2.53,yy,1.75,[(.04,0),(.045,.10),(.04,.105),(.032,.02)],glass)
box('cash drawer',-1.65,-1.06,1.85,2.27,1.04,1.15,iron)
box('POS screen',-1.59,-1.15,1.97,2.04,1.15,1.45,dark)
label('bar food notice','FOOD ALLERGY',-2.77,3.47,1.73,.09,linen)
tube('beer tap', [(-1.12,3.40,1.03),(-1.12,3.40,1.45),(-.95,3.40,1.45),(-.95,3.40,1.35)],brass,.026)
box('tap handle',-1.16,-1.08,3.37,3.43,1.46,1.67,dark)
box('service door',.82,2.18,14.72,14.80,.05,2.45,wood);label('rear exit plaque','SERVICE',1.5,14.69,2.31,.10,linen)
light('bar wash',-1.50,2.6,2.9,40,(.65,.17,1),1)

# Requested booth guest: static seated model with source-photo facial reference.
skin=material('guest skin',(.52,.30,.19));shirt=material('guest pale checked shirt',(.53,.55,.49));pattern(shirt,[(.35,.38,.34),(.76,.76,.68)],30)
guestx,guesty=4.55,8.62
sphere('guest torso',guestx,guesty,.91,.31,.19,.36,shirt);sphere('guest head',guestx,guesty-.035,1.43,.145,.13,.19,skin)
for sign in (-1,1):
    sphere('guest trouser leg',guestx+sign*.16,guesty-.30,.46,.13,.34,.12,dark)
    sphere('guest shoe',guestx+sign*.16,guesty-.58,.14,.11,.18,.085,dark)
    sphere('guest sleeve',guestx+sign*.33,guesty-.05,1.04,.14,.12,.17,shirt)
    sphere('guest forearm',guestx+sign*.32,guesty-.24,.86,.07,.21,.07,skin)
lathe('guest beer glass',guestx-.30,guesty-.43,.80,[(.06,0),(.064,.21),(.055,.215),(.045,.025)],glass)
lathe('guest beer',guestx-.30,guesty-.43,.805,[(.045,0),(.050,.16)],bottle_mats[3])
# UV-only source selection, original unchanged; explicit non-solid photo insert.
im=bpy.data.images.load(str(refs[2]),check_existing=True);im.pack();gm=material('guest photographic face',(.7,.6,.5));tn=gm.node_tree.nodes.new('ShaderNodeTexImage');tn.image=im;gm.node_tree.links.new(tn.outputs['Color'],gm.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
verts=[(guestx,guesty-.168,1.43)]+[(guestx+.137*math.cos(i*math.tau/40),guesty-.168,1.43+.18*math.sin(i*math.tau/40)) for i in range(40)]
me=bpy.data.meshes.new('guest source-face insert');me.from_pydata(verts,[],[(0,i+1,(i+1)%40+1) for i in range(40)]);me.materials.append(gm);uv=me.uv_layers.new(name='UV_reference_face')
for p in me.polygons:
    for li in p.loop_indices:
        v=me.vertices[me.loops[li].vertex_index].co;px=535+(v.x-guestx)/.137*137;py=408-(v.z-1.43)/.18*180;uv.data[li].uv=(px/im.size[0],1-py/im.size[1])
guest=bpy.data.objects.new('Detail v26 | Taraj | requested booth guest source face',me);coll.objects.link(guest);guest.matrix_world=basis;guest['photo_insert']=True;guest['source']=str(refs[2].relative_to(ROOT));guest['crop_method']='UV-only elliptical selection; source PNG unchanged';guest['likeness_status']='Static reference-faced placeholder; no rig/animation';made.append(guest)

# Geometry, retained-model and source checks before the checkpoint save.
bpy.context.view_layer.update()
for name,(vs,fs) in protected.items():
    ob=bpy.data.objects[name];assert vs==[tuple(ob.matrix_world@v.co) for v in ob.data.vertices],name;assert fs==[tuple(p.vertices) for p in ob.data.polygons],name
solids=[o for o in made if o.type=='MESH' and not o.get('photo_insert')]
for ob in solids:
    bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges),ob.name;assert bm.calc_volume(signed=True)>0,ob.name;bm.free();assert ob.matrix_world.determinant()>0,ob.name
deps=bpy.context.evaluated_depsgraph_get();branch_checks=[]
for i in range(1,20):
    pt=a.lerp(b,i/20);pt.z=1.7;hit,loc,n,idx,ob,ma=scene.ray_cast(deps,pt,Vector((0,0,1)),distance=12);assert not hit,('Side access blocked',i,ob.name);branch_checks.append(i/20)
aislechecks=0
for x in (-.18,3.12):
    for yi in range(43,139,3):
        origin=tarajbasis@Vector((x,yi/10,1.0));target=tarajbasis@Vector((x,(yi+2)/10,1.0));d=target-origin
        hit,loc,n,idx,ob,ma=scene.ray_cast(deps,origin,d.normalized(),distance=d.length);assert not hit,('Dining aisle blocked',x,yi,ob.name);aislechecks+=1
for p in refs:assert hashlib.sha256(p.read_bytes()).hexdigest()==refhash[str(p.relative_to(ROOT))]
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
dest=ROOT/'recon/v26';dest.mkdir(exist_ok=True)
views=[]
def camera(name,eye,target,bs,ortho=None):
    cd=bpy.data.cameras.new('Review v26 | '+name);ob=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(ob);ob.location=bs@Vector(eye);ob.rotation_euler=(bs@Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();cd.lens=24
    if ortho:cd.type='ORTHO';cd.ortho_scale=ortho
    views.append((name,ob));return ob
camera('01_taraj_dining',(-.18,4.5,1.65),(1.5,12,1.5),tarajbasis)
camera('02_taraj_booths',(2.9,7,1.65),(4.9,10,1.4),tarajbasis)
camera('03_taraj_bar',(1.4,3.8,1.65),(-1.8,2.8,1.65),tarajbasis)
camera('04_taraj_guest',(3.2,6.2,1.5),(4.55,8.6,1.12),tarajbasis)
camera('05_taraj_entry',(-4.4,2.2,1.65),(-2.0,6.8,1.55),tarajbasis)
camera('06_bridge_overview',(15,-20,13),(0,0,-.2),bridgebasis)
camera('07_bridge_brook',(0,-4.7,1.65),(0,-17,-.65),bridgebasis)
camera('08_bridge_side',(8,-14,1.8),(0,-4,-.6),bridgebasis)
camera('09_bridge_access_plan',(0,0,55),(0,0,0),bridgebasis,65)
scene.camera=views[0][1];bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
report={'checkpoint':str(OUT.relative_to(ROOT)),'source_sha256':source_hash,'references':refhash,'closed_outward_new_solids':len(solids),'retained_meshes_exact':len(protected),'archived_objects':retired,'branch_clearance_samples':len(branch_checks),'dining_aisle_segments':aislechecks,'restaurant_width_m_estimate':8.8,'restaurant_depth_m_estimate':13.85,'booth_bays':8,'chair_count':16,'guest':'Static model with UV-only source-face insert; no rig/animation','channel_water_z_estimate':-1.52,'changed_existing_geometry':cut_names+['Brookside road branch raised6mm'],'limits':['Taraj floor plan/depth/bar placement are photo-led estimates; kitchen/toilets not surveyed','Etched artwork and fabric are procedural interpretations, not exact reproductions','Brook depth/underside are estimated; parking/tree placement approximate','No Radiant/BO3 export, collision or zombie AI verification']}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary v26 exterior review sun','SUN');ld.energy=2.2;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name,cam in views:
    scene.camera=cam;scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps({'checkpoint':str(OUT),'new_solids':len(solids),'retained':len(protected),'aisle_segments':aislechecks,'branch_checks':len(branch_checks)}))
