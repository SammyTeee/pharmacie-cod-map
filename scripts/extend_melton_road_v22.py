"""Labelled user map -> estimated street blockout, preserving reviewed v21."""
from pathlib import Path
import bpy,ast,math,json,hashlib,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-shopfronts-fridge-v21.blend'
OUT=ROOT/'assets/blender/pharmacie-melton-road-v22.blend';assert not OUT.exists()
source=ROOT/'references/the top view map to build down to taraj - top right is natural wellbeing and opposite down the road is pharmacie -.png'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections.new('STREET v22 | Melton Road and Taraj blockout')
for s in bpy.data.scenes:
    if 'STREET v17 | Photo-led connected High Street' in s.collection.children:s.collection.children.link(coll)
made=[]
helpers=(ROOT/'scripts/model_shopfronts_v19.py').read_text().replace('Shop v19 |','Street v22 |')
nodes=[n for n in ast.parse(helpers).body if isinstance(n,ast.FunctionDef) and n.name in ('material','mesh','box','beam')]
exec(compile(ast.Module(body=nodes,type_ignores=[]),'owned_helpers','exec'))
road=bpy.data.materials['Street v17 | asphalt'];paving=bpy.data.materials['Street v17 | paving'];white=bpy.data.materials['Street v17 | road white'];slate=bpy.data.materials['Street v17 | slate'];brick=bpy.data.materials['Shop v19 | brick relief'];glass=bpy.data.materials['Shop v19 | upper glazing'];cream=bpy.data.materials['Shop v19 | cream sign']
green=material('park grass',(.10,.24,.075));water=material('brook water',(.055,.22,.28));red=material('Taraj provisional fascia',(.38,.035,.055))
archive=bpy.data.collections.new('ARCHIVE v21 | Superseded junction stub');archive.use_fake_user=True
retired=[]
for o in list(scene.objects):
    if o.name.startswith(('Street v17 | Fox junction','Street v17 | Junction keep-left')):
        archive.objects.link(o)
        for c in list(o.users_collection):
            if c!=archive:c.objects.unlink(o)
        retired.append(o.name)
protected={o.name:([tuple(o.matrix_world@v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons]) for o in scene.objects if o.type=='MESH'}
# Similarity transform aligns the existing High Street with the drawn road.
# Natural Wellbeing road projection (885,215) -> (52.5,-6.7), junction
# centre (1065,352) -> (-40,-6.7). Scale is gameplay calibration, not survey.
axis=Vector((180,137)).normalized();cross=Vector((-axis.y,axis.x));scale=92.5/Vector((180,137)).length
def mapxy(px,py):
    d=Vector((px-1065,py-352));return Vector((-40-d.dot(axis)*scale,-6.7+d.dot(cross)*scale))
pixels=[(1065,352),(1020,455),(970,555),(910,645),(835,730),(765,815),(703,885),(642,956),(615,990)]
path=[mapxy(*p) for p in pixels]
def disk(name,c,r,z0,z1,mat,n=48):
    pts=[(c.x+r*math.cos(i*2*math.pi/n),c.y+r*math.sin(i*2*math.pi/n)) for i in range(n)]
    return mesh(name,[(x,y,z) for z in (z0,z1) for x,y in pts],[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)
def strip(name,points,width,z0,z1,mat):
    # Mitred joins make one watertight ribbon instead of overlapping quads.
    norms=[Vector((-(b-a).y,(b-a).x)).normalized() for a,b in zip(points,points[1:])]
    offsets=[]
    for i in range(len(points)):
        if i==0:n=norms[0]*width/2
        elif i==len(points)-1:n=norms[-1]*width/2
        else:
            bis=(norms[i-1]+norms[i]).normalized();n=bis*(width/2/bis.dot(norms[i]))
        offsets.append(n)
    outline=[p-n for p,n in zip(points,offsets)]+list(reversed([p+n for p,n in zip(points,offsets)]))
    area=sum(a.x*b.y-b.x*a.y for a,b in zip(outline,outline[1:]+outline[:1]))
    if area<0:outline.reverse()
    count=len(outline)
    return mesh(name,[(p.x,p.y,z) for z in (z0,z1) for p in outline],[tuple(reversed(range(count))),tuple(range(count,2*count))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)],mat)
centre=path[0]
disk('Roundabout pavement apron',centre,13,-.30,-.13,paving)
disk('Roundabout carriageway',centre,10,-.23,-.078,road)
disk('Roundabout central low island',centre,2.3,-.078,.08,paving)
disk('Roundabout white island marking',centre,1.9,.08,.085,white)
strip('Melton Road pavement foundation',path,13,-.31,-.12,paving)
strip('Melton Road continuous carriageway',path,8,-.23,-.08,road)
# Side pavements and kerbs. Begin clear of the roundabout mouth.
for side in (-1,1):
    normals=[]
    for i,p in enumerate(path):
        d=path[min(i+1,len(path)-1)]-path[max(i-1,0)];normals.append(Vector((-d.y,d.x)).normalized())
    walk=[p+n*side*5.25 for p,n in zip(path,normals)]
    kerb=[p+n*side*4.08 for p,n in zip(path,normals)]
    strip('Melton pavement '+str(side),walk[1:],2.45,-.25,0,paving)
    strip('Melton kerb '+str(side),kerb[1:],.16,-.17,.015,cream)
    start=walk[0]+(path[1]-path[0]).normalized()*14
    strip('Roundabout approach pavement '+str(side),[start,walk[1]],2.45,-.25,0,paving)
# Connect retained High Street to new junction; speculative clipped arm remains short.
beam('High Street roundabout connection',(-40,-6.7),(-29,-6.7),-.24,-.076,7.4,road)
beam('Unsurveyed far junction arm',(-40,-6.7),(-55,-28),-.24,-.08,8,road)
for a,b in zip(path[1:],path[2:]):
    d=b-a;length=d.length;u=d.normalized()
    for t in range(6,int(length)-4,10):beam('Melton centre dash',a+u*t,a+u*(t+3),-.075,-.065,.09,white)
def label(name,body,pos,size,rotation=0):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.008;cu.materials.append(cream)
    ob=bpy.data.objects.new('Street v22 | '+name,cu);coll.objects.link(ob);ob.location=pos;ob.rotation_euler=(math.pi/2,0,rotation);made.append(ob);return ob
def building(name,c,u,side,width,depth,height,taraj=False):
    n=Vector((-u.y,u.x));front=c+n*side*7.2;back=front+n*side*depth
    vs=[front-u*width/2,front+u*width/2,back+u*width/2,back-u*width/2]
    if sum(a.x*b.y-b.x*a.y for a,b in zip(vs,vs[1:]+vs[:1]))<0:vs.reverse()
    mass=mesh(name+' solid mass',[(p.x,p.y,z) for z in (0,height) for p in vs],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],brick)
    mass['enterable']=False
    beam(name+' roof cap',front+n*side*depth/2-u*(width+.25)/2,front+n*side*depth/2+u*(width+.25)/2,height,height+.38,depth+.25,slate)
    face=front-n*side*.06
    beam(name+' fascia',face-u*width*.49,face+u*width*.49,2.8,3.45,.14,red if taraj else cream)
    for j in range(max(1,int(width/3))):
        x=(-width/2)+(j+.5)*width/max(1,int(width/3));p=face+u*x
        beam(name+' ground display',p-u*.85,p+u*.85,.5,2.75,.12,glass)
        beam(name+' upper window',p-u*.65,p+u*.65,4.8,6.7,.12,glass)
    if taraj:
        facing=-n*side;rot=math.atan2(facing.x,-facing.y)
        label('Taraj provisional sign','TARAJ',(*tuple(face+facing*.1),2.97),.38,rot)
    return {'name':name,'front_centre':list(front),'width_m':width,'depth_m':depth,'height_m':height,'status':'Taraj facade awaiting photo' if taraj else 'Anonymous estimated placeholder'}
buildings=[]
# Labels identify only robust locations in the supplied map. All other frontage
# forms are generic and their individual parcel lengths are deliberately estimated.
for i,(a,b) in enumerate(zip(path[1:],path[2:])):
    u=(b-a).normalized();length=(b-a).length
    for side in (-1,1):
        for k in range(int(length/11)):
            c=a+u*(6+k*11)
            if side==-1 and i>=5:continue # reserve circled Taraj parcel
            name=('Costa vicinity' if i==0 and side==1 and k==0 else 'Melton placeholder')+f' {i}-{side}-{k}'
            buildings.append(building(name,c,u,side,9.8,10+(k%3)*2,7.5+(k%2)))
taraj_front_pixel=(683,916);t=mapxy(*taraj_front_pixel)
# Project onto road segment beside the circled building, then offset right.
a,b=path[-3],path[-2];u=(b-a).normalized();c=a+u*max(0,min((t-a).dot(u),(b-a).length))
buildings.append(building('Taraj',c,u,-1,12,15,8.5,True))
# Brookside, adjacent brook and park are broad landscape anchors only.
brookside=[mapxy(770,801),mapxy(582,742)]
strip('Brookside road branch',brookside,5.5,-.24,-.08,road)
brook=[mapxy(*p) for p in [(490,697),(642,754),(752,824),(770,883),(746,944),(766,990)]]
strip('Brook approximate course',brook,3.5,-.34,-.18,water)
park=[mapxy(*p) for p in [(335,726),(490,715),(633,775),(495,958),(340,972)]]
count=len(park)
if sum(a.x*b.y-b.x*a.y for a,b in zip(park,park[1:]+park[:1]))<0:park.reverse()
mesh('Kids park broad ground',[(p.x,p.y,z) for z in (-.5,-.3) for p in park],[tuple(reversed(range(count))),tuple(range(count,count*2))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)],green)
for o in made:o['evidence']='User-labelled top map; approximate gameplay scale';o['status']='Blender blockout only, collision/navmesh not exported'
bpy.context.view_layer.update()
for name,(verts,faces) in protected.items():
    o=bpy.data.objects[name];assert verts==[tuple(o.matrix_world@v.co) for v in o.data.vertices] and faces==[tuple(p.vertices) for p in o.data.polygons]
solids=[o for o in made if o.type=='MESH']
for o in solids:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0,o.name;bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
views=[('01_route_overview',(-15,150,350),(-15,150,0),380),('02_roundabout',(-66,-26,24),(-33,1,0),None),('03_melton_player',(*tuple(path[2]),1.7),(*tuple(path[3]),2.8),None),('04_taraj_placeholder',(*tuple(c),1.7),(*tuple(Vector(buildings[-1]['front_centre'])),2.8),None)]
for name,eye,target,ortho in views:
    cd=bpy.data.cameras.new('Review v22 | '+name);cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cd.lens=24
    if ortho:cd.type='ORTHO';cd.ortho_scale=ortho
scene.camera=bpy.data.objects['Review v22 | 01_route_overview']
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
dest=ROOT/'recon/v22';dest.mkdir(exist_ok=True)
report={'source':str(source.relative_to(ROOT)),'source_sha256':source_hash,'metres_per_pixel_estimate':scale,'roundabout_centre':list(centre),'melton_centreline': [list(p) for p in path],'carriageway_width_m':8,'placeholder_buildings':buildings,'closed_outward_solids':len(solids),'preserved_meshes':len(protected),'archived_old_junction':retired,'radiant_or_game_verified':False}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.55
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary street review sun','SUN');ld.energy=2;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.4,-.5,-.4)
for name,eye,target,ortho in views:
    scene.render.resolution_x=1200 if ortho else 1400;scene.render.resolution_y=1600 if ortho else 1000
    scene.camera=bpy.data.objects['Review v22 | '+name];scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps({'closed_solids':len(solids),'preserved_meshes':len(protected),'buildings':len(buildings),'checkpoint':str(OUT)}))
