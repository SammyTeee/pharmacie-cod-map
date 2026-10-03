"""Simple 3D relief for five opposite facades; extend reviewed v19 safely."""
from pathlib import Path
import bpy,json,math,ast,hashlib,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-opposite-shopfronts-v20.blend'
assert Path(bpy.data.filepath).name=='pharmacie-shopfronts-v19.blend'
assert not OUT.exists(),'Preserve existing reviewed checkpoint'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
old=bpy.data.collections['STREET v17 | Photo-led connected High Street']
coll=bpy.data.collections.new('STREET v20 | Modelled opposite shopfronts')
for s in bpy.data.scenes:
    if old.name in s.collection.children:s.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v19 | Opposite flat fronts and old bays');archive.use_fake_user=True
shops=[('Fox and Hounds',-15,-3,8.9),('Aston and Co',-3,1,9.5),('Syston Mini Market',1,10,9.8),('Lets Move estate agents',10,17,9.2),('Floral Fantasy',17,24,9.2)]
old_bay_prefixes=('Street v17 | Lets Move white upper bay','Street v17 | Lets Move upper bay','Street v17 | Lets Move bay hood','Street v17 | Floral Fantasy white upper bay','Street v17 | Floral Fantasy upper bay','Street v17 | Floral Fantasy bay hood')
def untouched(o):return not any(o.name.startswith('Street v17 | '+s[0]+' ') for s in shops) and not o.name.startswith(old_bay_prefixes)
protected={o.name:([tuple(o.matrix_world@v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons]) for o in scene.objects if o.type=='MESH' and untouched(o)}
made=[];panels=[];photo_mats={}
source_by_name={s['name']:s for s in json.loads((ROOT/'assets/street/v17/manifest.json').read_text())['fronts']}
# Reuse the project-owned geometry helpers, not their scene-changing main code.
helper=(ROOT/'scripts/model_shopfronts_v19.py').read_text().replace('Shop v19 |','Shop v20 |')
tree=ast.parse(helper);functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('material','mesh','box','beam','photo','pane','text')]
exec(compile(ast.Module(body=functions,type_ignores=[]),'v19_geometry_helpers','exec'),globals())
brick=bpy.data.materials['Shop v19 | brick relief'];white=bpy.data.materials['Shop v19 | painted white']
cream=bpy.data.materials['Shop v19 | cream sign'];dark=bpy.data.materials['Shop v19 | dark backing'];glass=bpy.data.materials['Shop v19 | upper glazing']
charcoal=bpy.data.materials['Shop v19 | cleaner grey']
red=material('opposite red sign',(.63,.035,.045));navy=material('estate navy',(.025,.055,.105));sage=material('fox grey sage',(.30,.35,.29))
yellow=material('market sign yellow',(.93,.65,.08));black=material('florist black fascia',(.035,.034,.027))
def archive_object(o):
    archive.objects.link(o)
    for c in list(o.users_collection):
        if c!=archive:c.objects.unlink(o)
for o in list(old.objects):
    if o.name.startswith(old_bay_prefixes):archive_object(o)
def photo_front(name,shop,a,b,z0,z1,crop):
    start=len(made);photo(name,shop,a,b,z0,z1,crop)
    o=made[start];u0=crop[0]/1024;u1=crop[2]/1024
    for d in o.data.uv_layers.active.data:d.uv.x=u0+u1-d.uv.x
    o['orientation']='Opposite front: source left maps to world +X'
def display(name,shop,x0,x1,y,z0,z1,crop,mat):
    photo_front(name+' selected display',shop,(x0,y),(x1,y),z0,z1,crop)
    for x in (x0,x1):box(name+' upright',x-.055,x+.055,y-.04,y+.10,z0-.05,z1+.05,mat)
    for z in (z0,z1):box(name+' rail',x0,x1,y-.04,y+.10,z-.04,z+.04,mat)
def sign(name,wording,x0,x1,z0,z1,mat,letter_mat=white):
    box(name+' projecting sign board',x0,x1,-13.06,-12.77,z0,z1,mat)
    ob=text(name+' sharp lettering',wording,(x0+x1)/2,-12.75,(z0+z1)/2,x1-x0-.25,letter_mat,(z1-z0)*.57)
    ob.rotation_euler.z=math.pi
def closed_door(name,shop,x0,x1,crop,mat):
    box(name+' lower door panel',x0,x1,-13.55,-13.48,.06,.92,mat)
    display(name+' recessed glazing',shop,x0,x1,-13.46,.95,3.20,crop,mat)
    for x in (x0-.08,x1+.08):box(name+' reveal',x-.06,x+.06,-13.56,-12.92,.02,3.35,mat)
    box(name+' threshold',x0-.15,x1+.15,-13.59,-12.98,-.01,.01,cream)
    box(name+' handle',x0+.10,x0+.13,-13.38,-13.33,1.40,1.80,cream)
def upper_window(name,cx,y=-13):
    anchor=bpy.data.objects['Front | sash recessed glass']
    pts=[anchor.matrix_world@v.co for v in anchor.data.vertices];refx=(min(v.x for v in pts)+max(v.x for v in pts))/2
    for o in list(scene.objects):
        if o.type!='MESH' or not o.name.startswith(('Front | sash','Front | stone sash')):continue
        p=[o.matrix_world@v.co for v in o.data.vertices]
        if min(v.x for v in p)<refx-1.25 or max(v.x for v in p)>refx+1.25:continue
        verts=[(v.x+cx-refx,y+.07-v.y,v.z) for v in p]
        m=glass if 'glass' in o.name else cream if 'stone' in o.name else sage if name.startswith('Fox') else white
        mesh(name+' | '+o.name,verts,[tuple(reversed(face.vertices)) for face in o.data.polygons],m)
def bay(name,cx):
    box(name+' projecting bay backing',cx-1.18,cx+1.18,-13.04,-12.49,5.40,8.82,white)
    upper_window(name+' bay window',cx,-12.43)
    box(name+' bay cornice',cx-1.28,cx+1.28,-13.11,-12.12,8.80,8.99,cream)
    box(name+' bay apron',cx-1.22,cx+1.22,-13.08,-12.29,5.35,5.57,white)
    # Simple closed convex hip-shaped hood, with visible geometric roof depth.
    mesh(name+' bay roof',[(cx-1.30,-13.13,8.99),(cx+1.30,-13.13,8.99),(cx+1.30,-12.08,8.99),(cx-1.30,-12.08,8.99),(cx-.60,-12.75,9.47),(cx+.60,-12.75,9.47)],[(0,3,2,1),(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],bpy.data.materials['Street v17 | slate'])
for shop,x0,x1,height in shops:
    flat=bpy.data.objects['Street v17 | '+shop+' isolated facade'];archive_object(flat)
    mass=bpy.data.objects['Street v17 | '+shop+' solid scenery mass'];mass.data=mass.data.copy()
    old_height=max(v.co.z for v in mass.data.vertices)
    for v in mass.data.vertices:
        if abs(v.co.y+13)<.001:v.co.y=-14.05
        if abs(v.co.z-old_height)<.001:v.co.z=height
    for o in list(old.objects):
        if o==mass or o.type!='MESH' or not o.name.startswith('Street v17 | '+shop+' '):continue
        if any(s in o.name for s in ('roof','gutter','chimney')):
            o.data=o.data.copy()
            for v in o.data.vertices:v.co.z+=height-old_height
        elif 'downpipe' in o.name:
            o.data=o.data.copy()
            for v in o.data.vertices:
                if v.co.z>old_height-.2:v.co.z+=height-old_height
    uppermat=cream if shop in ('Fox and Hounds','Aston and Co') else brick
    box(shop+' solid upper facade',x0,x1,-14.05,-13,4.35,height,uppermat)
    box(shop+' opaque display backing',x0,x1,-14.04,-14.00,.0,4.35,dark)
    for x in (x0+.08,x1-.08):box(shop+' outer pier',x-.08,x+.08,-13.10,-12.94,.0,4.36,uppermat)
# Fox: rendered walls, real framed windows and separate projecting pub boards.
shop='Fox and Hounds'
box('Fox ground render left',-15,-11.48,-14,-13,.0,4.35,cream)
box('Fox ground render right',-10.02,-3,-14,-13,.0,4.35,cream)
box('Fox entry lintel render',-11.48,-10.02,-14,-13,3.35,4.35,cream)
for i,(a,b,crop) in enumerate([(-14.1,-12.6,(839,548,935,771)),(-8.4,-7.2,(408,581,474,807)),(-6.9,-4.9,(189,578,352,805))]):
    display('Fox ground sash '+str(i),shop,a,b,-12.97,.85,3.27,crop,sage)
    for fraction in (.25,.5,.75):box('Fox small pane bar',a+(b-a)*fraction-.018,a+(b-a)*fraction+.018,-12.94,-12.86,.85,3.27,sage)
    box('Fox sash meeting rail',a,b,-12.94,-12.86,1.95,2.02,sage)
closed_door('Fox closed entry',shop,-11.4,-10.1,(575,491,647,846),sage)
sign('Fox pub name','THE FOX & HOUNDS',-12.9,-8.9,3.55,4.30,cream,black)
sign('Fox food board','FINE FOOD, REAL ALE & WINES',-7.4,-3.7,3.58,4.24,cream,black)
for x in (-13.0,-9.0,-5.0):upper_window('Fox upper sash',x)
# Aston: red door, listing displays and clean fascia.
shop='Aston and Co';sign('Aston fascia','Aston & Co',-3,1,3.5,4.35,red)
display('Aston right listing window',shop,-.18,.78,-12.96,.35,3.30,(42,660,296,917),red)
display('Aston left listing window',shop,-1.12,-.28,-12.96,.35,3.30,(355,668,583,917),red)
closed_door('Aston red entry',shop,-2.83,-1.36,(780,730,958,916),red)
upper_window('Aston upper sash',-1.0)
# Mini Market: own sharp sign and individually framed printed product panels.
shop='Syston Mini Market';sign('Mini Market fascia','SYSTON MINI MARKET',1,10,3.55,4.38,red)
market_letters=bpy.data.objects['Shop v20 | Mini Market fascia sharp lettering'].data
market_letters.materials.append(yellow)
for i in range(6):market_letters.body_format[i].material_index=1
small=text('Market smaller categories','VAPE  SWEETS  SOFT DRINKS  TOBACCO',5.5,-12.75,3.65,8.2,white,.14);small.rotation_euler.z=math.pi
for i,(a,b,crop) in enumerate([(1.24,3.0,(683,714,842,913)),(4.39,6.23,(407,713,549,912)),(6.39,8.04,(255,710,386,841)),(8.18,9.76,(77,711,216,841))]):
    box('Market low printed-panel backing',a,b,-13.02,-12.95,.12,.70,navy)
    display('Market product panel '+str(i),shop,a,b,-12.92,.70,3.32,crop,white)
closed_door('Market right entry',shop,3.18,4.24,(563,694,650,952),charcoal)
for x in (3.3,7.7):upper_window('Mini Market upper sash',x)
# Estate agent: depth in the entry, display cards and a perpendicular sign.
shop='Lets Move estate agents';sign('Lets Move fascia',"let's move",10,17,3.5,4.35,navy)
closed_door('Lets Move recessed entry',shop,15.50,16.77,(171,566,322,934),navy)
display('Lets Move listing window 1',shop,10.35,12.68,-12.91,.30,3.30,(668,592,833,785),navy)
display('Lets Move listing window 2',shop,12.85,15.25,-12.91,.30,3.30,(449,592,646,785),navy)
box('Lets Move projecting blade sign',16.65,16.77,-12.91,-12.15,3.30,4.17,navy)
bay('Lets Move upper',13.5);upper_window('Lets Move flat upper sash',16.0)
# Florist: modelled white frames and opaque leaf-patterned glazing.
shop='Floral Fantasy';sign('Floral Fantasy fascia','Floral Fantasy',17,24,3.52,4.35,black,cream)
closed_door('Floral Fantasy pale entry',shop,22.00,23.18,(154,642,424,935),white)
display('Floral patterned glass 1',shop,17.30,19.47,-12.95,.20,3.31,(754,519,997,899),white)
display('Floral patterned glass 2',shop,19.63,21.75,-12.95,.20,3.31,(491,519,722,899),white)
bay('Floral Fantasy upper',20.5)
bpy.context.view_layer.update()
for name,(verts,faces) in protected.items():
    o=bpy.data.objects[name];assert verts==[tuple(o.matrix_world@v.co) for v in o.data.vertices] and faces==[tuple(p.vertices) for p in o.data.polygons],name
solid_count=0;quad_count=0
for o in made:
    if o.type!='MESH':continue
    if len(o.data.polygons)==1:quad_count+=1;continue
    bm=bmesh.new();bm.from_mesh(o.data)
    assert all(e.is_manifold for e in bm.edges),o.name
    assert bm.calc_volume(signed=True)>1e-10,o.name
    bm.free();solid_count+=1
for s in json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']:
    assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
views=[('01_fox_and_hounds',(-9,-.7,2.0),(-9,-13,4.7),28),('02_aston_market',(3,-.7,2.0),(3,-13,4.7),24),
 ('03_estate_florist',(17,-.7,2.0),(17,-13,4.7),24),('04_opposite_row',(5,-1,3.1),(5,-13,4.2),10),
 ('05_display_and_bay_depth',(23,-6,1.65),(16,-13,3.2),24),('06_fox_door_depth',(-12,-8,1.65),(-10.4,-13.5,2.2),28)]
cameras=[]
for name,eye,target,lens in views:
    ca=bpy.data.cameras.new('Review v20 | '+name);ca.lens=lens;ob=bpy.data.objects.new(ca.name,ca);coll.objects.link(ob);ob.location=eye
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();cameras.append(ob)
scene.camera=cameras[3]
report={'checkpoint':str(OUT),'shops':[s[0] for s in shops],'new_objects':len(made),'closed_outward_solids':solid_count,'selected_photo_quads':quad_count,
 'preserved_existing_meshes':len(protected),'original_hashes_unchanged':44,'upper_windows':'9 pub-template windows; original size/height, opposite-facing Y reflection and reversed winding',
 'window_regions':panels,'estimated_depths_m':{'closed_door_recess':.48,'bay_projection':.57,'fascia_projection':.23},
 'limits':'Static scenery only, opaque photographic displays; no interiors. Heights approximate gameplay scaling; no Radiant/BO3 conversion. Fonts approximate; some photographic baked reflections remain.'}
renders=ROOT/'recon/v20';renders.mkdir(parents=True,exist_ok=True)
(renders/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'assets/blender/opposite-shopfronts-v20-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.65,.72,.84,1);scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.55
ld=bpy.data.lights.new('v20 temporary daylight','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.5,.5,2.3)
for camera,(name,eye,target,lens) in zip(cameras,views):
    scene.camera=camera;scene.render.filepath=str(renders/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(report))
