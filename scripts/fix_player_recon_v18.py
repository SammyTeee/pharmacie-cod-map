"""Confirmed player recon fixes; preserve the live v17 input and save v18."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector,Matrix,geometry
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-player-cleanup-v18.blend'
assert not OUT.exists(),'Refuse to overwrite a reviewed file'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene;bpy.context.view_layer.update()
changes=[];made=[]
coll=bpy.data.collections.new('RECON v18 | Player clearance and finishing')
ceiling_coll=bpy.data.collections.new('RECON v18 | Upper ceiling and roof - toggle for cutaway')
for s in bpy.data.scenes:
    if s.name.startswith(('01 ','02 ','03 ','05 ')):s.collection.children.link(coll)
    if s.name.startswith(('02 ','03 ')):s.collection.children.link(ceiling_coll)
archive=bpy.data.collections.new('ARCHIVE v17 | Recon replaced stair treads and nosings');archive.use_fake_user=True
def bounds(o):
    pts=[o.matrix_world@Vector(v) for v in o.bound_box]
    return [min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]
def mesh(name,verts,faces,mat,collection=coll):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();me.materials.append(mat)
    o=bpy.data.objects.new('Recon v18 | '+name,me);collection.objects.link(o);made.append(o)
    o['evidence']='recon/v18/README.md';o['status']='Blender recon fix; game traversal unverified';return o
def box(name,x0,x1,y0,y1,z0,z1,mat,collection=coll):
    return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat,collection)
# Rotate the aisle-side dining chairs to each table's rear, retaining all pieces.
for y in (6.7,10.2):
    prefix='Video | downstairs dining '+str(y)+' chair'
    selected=[o for o in scene.objects if o.type=='MESH' and o.name.startswith(prefix) and bounds(o)[0][0]>5.2]
    pivot=Vector((4.5,y,0));transform=Matrix.Translation(pivot)@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-pivot)
    for o in selected:o.matrix_world=transform@o.matrix_world;o['recon_fix']='Aisle-side chair rotated to table end; main route clear'
    changes.append({'id':'R01','action':'Rotate aisle-side chair to table end','table_y':y,'objects':[o.name for o in selected]})
bpy.context.view_layer.update()
# Right-wall photo quads must read left-to-right from INSIDE the room. Preserve
# already-correct historic instrument face; swap whole UV pairs within each row.
fixed=[]
for o in list(scene.objects):
    if o.type!='MESH' or len(o.data.vertices)!=4 or len(o.data.polygons)!=1 or not o.data.uv_layers.active:continue
    if not any(m and m.use_nodes and any(n.type=='TEX_IMAGE' and n.image for n in m.node_tree.nodes) for m in o.data.materials):continue
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    if min(p.x for p in pts)<7 or max(p.x for p in pts)-min(p.x for p in pts)>.4 or max(p.y for p in pts)-min(p.y for p in pts)<.3:continue
    loops=list(o.data.polygons[0].loop_indices);uv=o.data.uv_layers.active
    ys=[pts[o.data.loops[i].vertex_index].y for i in loops];us=[uv.data[i].uv.x for i in loops]
    cov=sum((y-sum(ys)/4)*(u-sum(us)/4) for y,u in zip(ys,us))
    if cov<=0:continue
    o['recon_previous_uv']=json.dumps([list(uv.data[i].uv) for i in loops])
    ordered=sorted(loops,key=lambda i:pts[o.data.loops[i].vertex_index].z)
    for a,b in (ordered[:2],ordered[2:]):
        va,vb=uv.data[a].uv.copy(),uv.data[b].uv.copy();uv.data[a].uv=vb;uv.data[b].uv=va
    o['recon_fix']='Corrected mirrored right-wall image UV from player perspective';fixed.append(o.name)
changes.append({'id':'R02','action':'Correct mirrored right-wall photo UVs','objects':fixed})
# Separate coincident alley/landing tops by a tiny height, removing z-fighting.
connector=bpy.data.objects['Street v17 | Alley rear route connector']
for v in connector.data.vertices:
    if v.co.z>-.01:v.co.z=.008
changes.append({'id':'R03','action':'Rear connector top raised 8mm to remove coplanar overlap; no source floor removed'})
# Smooth the gameplay-enlarged risers while retaining footprint/turn/landings.
old=[o for o in scene.objects if o.type=='MESH' and o.name.startswith('Stairs |') and 'tread' in o.name]
lower=sorted([o for o in old if 'lower tread' in o.name],key=lambda o:bounds(o)[0][0])
upper=sorted([o for o in old if 'upper tread' in o.name],key=lambda o:-bounds(o)[1][1])
lx0=bounds(lower[0])[0][0];lx1=bounds(lower[-1])[1][0];ly0=bounds(lower[0])[0][1];ly1=bounds(lower[0])[1][1]
ux0=bounds(upper[0])[0][0];ux1=bounds(upper[0])[1][0];uy1=bounds(upper[0])[1][1];uy0=bounds(upper[-1])[0][1]
turn=bounds(bpy.data.objects['Stairs | RIGHT turn landing'])[1][2]
arrival=bounds(bpy.data.objects['Stairs | upper arrival landing'])[1][2]
wood=lower[0].active_material;metal=bpy.data.materials['Video | metal tread nosing']
nosings=[o for o in scene.objects if o.type=='MESH' and o.name.startswith('Video | Stairs |') and 'metal nosing' in o.name]
for o in old+nosings:
    archive.objects.link(o)
    for c in list(o.users_collection):
        if c!=archive:c.objects.unlink(o)
    o.name='ARCHIVE v17 | '+o.name
for i in range(14):
    a=lx0+(lx1-lx0)*i/14;b=lx0+(lx1-lx0)*(i+1)/14;z=turn*(i+1)/14
    box('Stairs lower tread %02d'%(i+1),a,b,ly0,ly1,0,z,wood)
    box('Stairs lower nosing %02d'%(i+1),a,a+.035,ly0,ly1,z,z+.005,metal)
for i in range(12):
    b=uy1-(uy1-uy0)*i/12;a=uy1-(uy1-uy0)*(i+1)/12;z=turn+(arrival-turn)*(i+1)/12
    box('Stairs upper tread %02d'%(i+1),ux0,ux1,a,b,0,z,wood)
    box('Stairs upper nosing %02d'%(i+1),ux0,ux1,b-.035,b,z,z+.005,metal)
changes.append({'id':'R04','action':'18 treads replaced by 26 in same footprint; rails/landings retained','lower_rise_m':turn/14,'upper_rise_m':(arrival-turn)/12,'previous_rise_m':turn/10,'venue_fact':False})
# A smaller front step onto the 270mm raised seating platform, outside main aisle.
platform=bpy.data.objects['Raised right-hand seating platform | platform slab'];lo,hi=bounds(platform)
box('Raised seating front intermediate step',lo[0]+.20,hi[0]-.20,lo[1]-.36,lo[1],0,hi[2]/2,platform.active_material)
box('Raised seating front step nosing',lo[0]+.20,hi[0]-.20,lo[1]-.365,lo[1]-.34,hi[2]/2,hi[2]/2+.005,metal)
changes.append({'id':'R05','action':'135mm intermediate front platform step; keeps main aisle clear','venue_fact':False})
# Close the open upstairs sky with a removable ceiling and temporary roof cap.
# Angled perimeter is retained; this is a finish proxy, not a surveyed roof design.
floor=bpy.data.objects['First | floor with corrected L stairwell opening']
xy=sorted(set((round((floor.matrix_world@v.co).x,5),round((floor.matrix_world@v.co).y,5)) for v in floor.data.vertices))
indices=geometry.convex_hull_2d([Vector(p) for p in xy]);outline=[xy[i] for i in indices]
def slab(name,z0,z1,m):
    n=len(outline);verts=[(x,y,z) for z in (z0,z1) for x,y in outline]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name,verts,faces,m,ceiling_coll)
cream=bpy.data.materials['Street v17 | painted white joinery'];slate=bpy.data.materials['Street v17 | slate']
slab('Upper removable ceiling',9.15,9.25,cream)
slab('Upper provisional roof cap',9.25,9.40,slate)
changes.append({'id':'R06','action':'Close missing upper ceiling and roof; angled outer perimeter, removable collection','limitations':'Flat rear cap and ceiling perimeter inferred; detailed roof pitch remains a future reference task'})
# Keep the inspection view separate from geometry; cameras never become collision.
camdata=bpy.data.cameras.new('Recon v18 | Player entrance camera');camdata.lens=22
cam=bpy.data.objects.new(camdata.name,camdata);scene.collection.objects.link(cam);cam.location=(5.5,.5,1.65);cam.rotation_euler=(Vector((5.5,8,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
for a in bpy.context.screen.areas:
    if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='SOLID';a.spaces.active.shading.color_type='TEXTURE'
bpy.context.view_layer.update()
assert len(lower)==10 and len(upper)==8 and len(fixed)==15
assert turn/14<.20 and (arrival-turn)/12<.20
scene['gameplay_version']='v18 player recon and cleanup; Blender only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
manifest={'input_snapshot':'recon/v18/input-live-v17.blend','output':str(OUT.relative_to(ROOT)),'changes':changes,'new_meshes':len(made),'radiant_rebuilt':False,'runtime_verified':False}
(ROOT/'recon/v18/changes.json').write_text(json.dumps(manifest,indent=2)+'\n')
result={'saved':str(OUT),'fixes':len(changes),'uv_panels_fixed':len(fixed),'new_meshes':len(made)}
