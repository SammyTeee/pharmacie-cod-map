"""Build recognizable Taraj frontage from supplied day/night photos, v22 route retained."""
from pathlib import Path
import bpy,ast,math,json,hashlib,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-melton-road-v22.blend'
OUT=ROOT/'assets/blender/pharmacie-taraj-front-v23.blend';assert not OUT.exists()
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
report=json.loads((ROOT/'recon/v22/validation.json').read_text());path=[Vector(p) for p in report['melton_centreline']]
front=Vector(report['placeholder_buildings'][-1]['front_centre']);u=(path[-2]-path[-3]).normalized();out=Vector((-u.y,u.x))
archive=bpy.data.collections.new('ARCHIVE v22 | Provisional Taraj front');archive.use_fake_user=True
for o in list(scene.objects):
    if o.name.startswith('Street v22 | Taraj'):
        archive.objects.link(o)
        for c in list(o.users_collection):
            if c!=archive:c.objects.unlink(o)
protected={o.name:[tuple(o.matrix_world@v.co) for v in o.data.vertices] for o in scene.objects if o.type=='MESH'}
coll=bpy.data.collections.new('STREET v23 | Taraj Palace photo-led exterior')
for s in bpy.data.scenes:
    if 'STREET v22 | Melton Road and Taraj blockout' in s.collection.children:s.collection.children.link(coll)
made=[]
helpers=(ROOT/'scripts/model_shopfronts_v19.py').read_text().replace('Shop v19 |','Taraj v23 |')
nodes=[n for n in ast.parse(helpers).body if isinstance(n,ast.FunctionDef) and n.name in ('material','mesh','box')]
exec(compile(ast.Module(body=nodes,type_ignores=[]),'owned_helpers','exec'))
rawbox=box
def box(name,x0,x1,d0,d1,z0,z1,mat):
    o=rawbox(name,x0,x1,d0,d1,z0,z1,mat)
    for v in o.data.vertices:
        p=front-u*v.co.x+out*v.co.y;v.co.x=p.x;v.co.y=p.y
    for poly in o.data.polygons:poly.flip()
    return o
cream=material('aged cream render',(.61,.58,.49));navy=material('dark blue fascia',(.025,.045,.14));gold=material('gold lettering',(.67,.53,.20));black=material('black iron',(.027,.031,.029));white=material('pale window joinery',(.73,.72,.63));glass=material('dark reflective glazing',(.095,.17,.19));brick=bpy.data.materials['Shop v19 | brick relief'];slate=bpy.data.materials['Street v17 | slate'];paving=bpy.data.materials['Street v17 | paving']
def text(name,body,x,d,z,size,mat):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.006;cu.materials.append(mat)
    ob=bpy.data.objects.new('Taraj v23 | '+name,cu);coll.objects.link(ob);p=front-u*x+out*d;ob.location=(p.x,p.y,z);ob.rotation_euler=(math.pi/2,0,math.atan2(out.x,-out.y));made.append(ob)
# Upper terrace wall and two clear ground openings: left passage, right shop recess.
box('upper cream mass',-6,6,-15,0,3.4,9.5,cream)
box('left passage outer wall',-6,-5.82,-15,0,0,3.4,brick)
box('passage dividing pier',-3.3,-3.0,-15,0,0,3.4,brick)
box('right outer pier',5.8,6,-15,0,0,3.4,cream)
box('shop rear closure',-3.0,5.8,-15,-1.15,0,3.4,brick)
box('left passage floor',-5.82,-3.3,-15,.05,-.20,0,paving)
box('left passage rear closure',-5.82,-3.3,-15,-14.85,0,3.4,black)
box('left recessed entrance door',-5.6,-4.2,-4.05,-3.95,.02,2.6,black)
box('left entry glazing',-5.43,-4.37,-3.94,-3.90,.65,2.4,glass)
box('shop recessed platform',-3,5.8,-1.15,.05,-.2,.03,paving)
box('recess cream soffit',-3,5.8,-1.15,.05,3.0,3.4,cream)
# Front windows, brick pier and right-hand brown door within the recessed bay.
for x0,x1 in [(-2.75,-.65),(.05,3.55)]:
    box('brick window plinth',x0,x1,-1.15,-.92,.03,1.0,brick)
    box('window dark glass',x0,x1,-.98,-.92,1.0,2.85,glass)
    for x in (x0,(x0+x1)/2,x1):box('white window upright',x-.045,x+.045,-.90,-.85,1.0,2.88,white)
    for z in (1.0,2.85):box('white window horizontal',x0,x1,-.90,-.85,z-.045,z+.045,white)
box('centre brick pier',-.65,.05,-1.15,-.85,0,3.0,brick)
doorwood=material('warm brown entrance door',(.25,.10,.04))
box('right door',3.85,5.5,-1.14,-1.03,.03,2.85,doorwood)
for z in (.45,1.5,2.4):box('right door raised panel',4.02,5.33,-1.02,-.99,z-.3,z+.3,doorwood)
box('door handle',4.05,4.09,-.97,-.91,1.05,1.35,gold)
# Blue lower fascia and pale main sign with separately editable sharp lettering.
box('blue lower fascia',-6,6,-.10,.12,3.03,4.18,navy)
box('cream main sign',-6,6,-.02,.15,4.30,5.12,white)
text('main sharp lettering','TARAJ PALACE',0,.17,4.48,.62,navy)
text('left restaurant wording','RESTAURANT',-4.6,.14,3.72,.19,gold)
text('left entrance wording','ENTRANCE',-4.6,.14,3.42,.14,gold)
text('eat in takeaway wording','EAT IN - TAKEAWAY',-.65,.14,3.70,.19,gold)
text('opening hours wording','OPEN 7 DAYS - 6PM TIL LATE',3.0,.14,3.70,.18,gold)
box('phone blue plaque',4.55,5.65,.16,.18,4.39,5.02,navy)
text('phone number line 1','0116',5.1,.20,4.76,.15,gold);text('phone number line 2','260 7777',5.1,.20,4.51,.15,gold)
# Three upper sashes retain pub-scale width and height, with cream stone surrounds.
for x in (-3.8,0,3.8):
    box('upper recessed glass',x-.84008,x+.84008,-.005,.035,5.865,8.475,glass)
    for xx in (x-.90,x+.90):box('upper stone jamb',xx-.08,xx+.08,-.06,.08,5.72,8.61,cream)
    for z in (5.78,8.56):box('upper stone sill lintel',x-1.0,x+1.0,-.07,.13,z-.08,z+.08,cream)
    for xx in (x-.82,x,x+.82):box('upper white sash upright',xx-.035,xx+.035,-.01,.07,5.865,8.475,white)
    for z in (5.865,7.17,8.475):box('upper sash rail',x-.84,x+.84,-.01,.07,z-.035,z+.035,white)
box('roof flat placeholder cap',-6.15,6.15,-15.15,.10,9.5,9.8,slate)
box('terrace cornice',-6.1,6.1,-.04,.18,9.18,9.45,white)
for x in [i*.38-5.7 for i in range(31)]:box('cornice dentil',x-.07,x+.07,-.04,.21,9.12,9.25,cream)
# Low black front fence has real bars; two gates remain closed scenery.
for x in (-2.9,-.15,3.7,5.65):box('fence square post',x-.04,x+.04,.12,.20,.03,1.45,black)
for z in (.35,.70,1.17):box('fence horizontal rail',-2.9,5.65,.12,.18,z-.017,z+.017,black)
for i in range(43):
    x=-2.86+i*.20;box('fence vertical bar',x-.012,x+.012,.13,.17,.03,1.31,black)
box('street utility cabinet',6.30,7.05,.04,.34,0,1.0,material('utility muted grey',(.23,.30,.28)))
sources=[]
for name in ['AN OUTISDE VIEW OF TARAJ SLIGHTLY FORM THE RIGHT ANGLE.png','taraj front left side alley way - has the entrance door in.png','right side of taraj.png','non blanked out map for better lables of taraj.png']:
    p=ROOT/'references'/name;sources.append({'file':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for o in made:o['evidence']='User-supplied Taraj day/night frontage references; estimated depths';o['status']='Blender exterior only; no restaurant interior or working door'
bpy.context.view_layer.update()
for name,verts in protected.items():assert verts==[tuple(bpy.data.objects[name].matrix_world@v.co) for v in bpy.data.objects[name].data.vertices]
solids=[o for o in made if o.type=='MESH']
for o in solids:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0,o.name;bm.free()
views=[('01_taraj_front',front+out*10,front),('02_taraj_entry_depth',front+u*8+out*9,front+u*2),('03_taraj_street_context',front-u*20+out*11,front)]
for name,eye,target in views:
    cd=bpy.data.cameras.new('Review v23 | '+name);cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);cam.location=(*tuple(eye),3.8 if 'front' in name else 2.0);cam.rotation_euler=(Vector((*tuple(target),4.7 if 'front' in name else 2.7))-cam.location).to_track_quat('-Z','Y').to_euler();cd.lens=20 if 'front' in name else 26
scene.camera=bpy.data.objects['Review v23 | 01_taraj_front'];bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
dest=ROOT/'recon/v23';dest.mkdir(exist_ok=True)
(dest/'validation.json').write_text(json.dumps({'closed_outward_solids':len(solids),'preserved_meshes':len(protected),'references':sources,'radiant_or_game_verified':False},indent=2)+'\n')
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary Taraj review sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.4,-.5,-.4)
for name,eye,target in views:
    scene.camera=bpy.data.objects['Review v23 | '+name];scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps({'closed_solids':len(solids),'preserved_meshes':len(protected)}))
