"""Remove render-discovered isolated rear sliver, support bank trees, frame bridge."""
from pathlib import Path
import bpy,json,bmesh,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v26'
assert Path(bpy.data.filepath).name=='pharmacie-taraj-interior-bridge-v26.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections['DETAIL v26 | Bridge brook and Taraj restaurant'];archive=bpy.data.collections.new('ARCHIVE v26 | First road-clearance rear mass');archive.use_fake_user=True
made=[]
def retire(ob):
    archive.objects.link(ob)
    for c in list(ob.users_collection):
        if c!=archive:c.objects.unlink(ob)
mass=bpy.data.objects['Syston v25 | B014 | rear scenery mass'];mb=mass.matrix_world.copy()
for i in range(3):
    axis=mb.col[i].xyz.normalized();mb.col[i]=Vector((*axis,mb.col[i].w))
for ob in (mass,bpy.data.objects['Syston v25 | B014 | roof cap']):retire(ob)
def box(name,coords,mat,basis):
    x0,x1,y0,y1,z0,z1=coords;me=bpy.data.meshes.new(name);me.from_pydata([(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]);me.materials.append(mat);me.update()
    ob=bpy.data.objects.new('Detail v26 | Bridge | '+name,me);coll.objects.link(ob);ob.matrix_world=basis;made.append(ob);return ob
newbody=box('compact Banking Hub rear',(-5.5,5.5,.9,3.0,0,8.9),bpy.data.materials['Shop v19 | brick relief'],mb)
newroof=box('compact Banking Hub roof',(-5.62,5.62,-.05,3.15,8.9,9.15),bpy.data.materials['Street v17 | slate'],mb)
branch=bpy.data.objects['Street v22 | Brookside road branch'];v=[branch.matrix_world@x.co for x in branch.data.vertices];a=(v[0]+v[3])/2;b=(v[1]+v[2])/2;u=(b-a).normalized();n=Vector((-u.y,u.x,0));cb=Matrix(((n.x,u.x,0,a.x),(n.y,u.y,0,a.y),(0,0,1,0),(0,0,0,1)))
cutter=box('temporary clearance cutter',(-3.5,3.5,-1,(b-a).length+1,-.45,12),bpy.data.materials['Detail v26 | dark backing'],cb)
for ob in (newbody,newroof):
    bpy.context.view_layer.objects.active=ob;mod=ob.modifiers.new('Access corner clearance','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name)
made.remove(cutter);retire(cutter)
rail=next(o for o in coll.objects if '| Bridge | continuous watercourse' in o.name);bb=rail.matrix_world.copy()
grass=bpy.data.materials['Detail v26 | bank vegetation']
for sign in (-1,1):
    x0,x1=(4.8,9.0) if sign==1 else (-9.0,-4.8)
    for y0,y1 in ((-45,-6.5),(6.5,42)):box('outer bank ground',(x0,x1,y0,y1,-1.95,.01),grass,bb)
tb=next(o for o in coll.objects if '| Taraj | carpet floor' in o.name).matrix_world.copy()
for y in (2.1,3.2):
    box('fridge interior light strip',(-1.22,-.94,y-.35,y+.35,.83,.842),bpy.data.materials['Detail v26 | warm lamp'],tb)
    ld=bpy.data.lights.new('Fridge interior practical','AREA');ld.energy=4;ld.color=(1,.83,.60);ld.shape='RECTANGLE';ld.size=.65;ld.size_y=.18
    ob=bpy.data.objects.new('Detail v26 | Taraj | fridge interior practical',ld);coll.objects.link(ob);ob.matrix_world=tb@Matrix.Translation((-1.06,y,.81))
# Top-down first frame cropped sides; choose a view with less foreground roof.
cam=bpy.data.objects['Review v26 | 06_bridge_overview'];cam.location=bb@Vector((17,-14,24));cam.rotation_euler=(bb@Vector((0,0,-.25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=24
bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
for i in range(1,20):
    p=a.lerp(b,i/20);p.z=1.7;hit,loc,n,idx,ob,ma=scene.ray_cast(dep,p,Vector((0,0,1)),distance=12);assert not hit,('Access obstructed',i,ob.name)
for ob in made:
    bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges),ob.name;assert bm.calc_volume(signed=True)>0,ob.name;bm.free();assert ob.matrix_world.determinant()>0,ob.name
r=json.loads((dest/'validation.json').read_text());r['bridge_final_review']={'compact_rear_depth_m_estimate':3,'eliminated_disconnected_rear_sliver':True,'bank_tree_ground_support':True,'rechecked_branch_samples':19,'new_closed_solids':len(made)};(dest/'validation.json').write_text(json.dumps(r,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100;scene.render.resolution_x=1400;scene.render.resolution_y=1000
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary final bridge sun','SUN');ld.energy=2.2;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name in ('03_taraj_bar','06_bridge_overview','07_bridge_brook','08_bridge_side','09_bridge_access_plan'):
    scene.camera=bpy.data.objects['Review v26 | '+name];scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(r['bridge_final_review']))
