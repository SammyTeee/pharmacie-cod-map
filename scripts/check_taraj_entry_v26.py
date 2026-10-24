"""Arrival-space QOL pass, practical passage lighting and multi-height paths."""
from pathlib import Path
import bpy,bmesh,json,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v26'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections['DETAIL v26 | Bridge brook and Taraj restaurant'];basis=next(o for o in coll.objects if '| Taraj | carpet floor' in o.name).matrix_world.copy()
archive=bpy.data.collections.new('ARCHIVE v26 | Entry booth arrival clearance');archive.use_fake_user=True;cleared=[]
for ob in list(coll.objects):
    if ob.type!='MESH' or not any(s in ob.name for s in ('booth bench base','booth upholstered seat','booth upholstered back')):continue
    vs=[v.co for v in ob.data.vertices]
    if max(v.x for v in vs)<0 and sum(v.y for v in vs)/len(vs)<5:
        archive.objects.link(ob)
        for c in list(ob.users_collection):
            if c!=archive:c.objects.unlink(ob)
        cleared.append(ob.name)
assert len(cleared)==3,cleared
for y in (2.7,5.0):
    ld=bpy.data.lights.new('Taraj entry passage practical','AREA');ld.energy=24;ld.color=(1,.78,.48);ld.shape='DISK';ld.size=.7
    ob=bpy.data.objects.new('Detail v26 | Taraj | entry passage practical',ld);coll.objects.link(ob);ob.matrix_world=basis@Matrix.Translation((-4.4,y,3.10))
bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();tests=0
def ray(a,b,description):
    a=basis@Vector(a);b=basis@Vector(b);d=b-a
    hit,loc,n,i,ob,m=scene.ray_cast(dep,a,d.normalized(),distance=d.length)
    assert not hit,(description,ob.name);return 1
for z in (.35,.85,1.65):
    for y in (4.25,4.50,4.75):tests+=ray((-4.4,y,z),(-.18,y,z),'Entry blocked')
    for x in (-.18,3.12):
        for dx in (-.25,0,.25):tests+=ray((x+dx,4.50,z),(x+dx,13.85,z),'Aisle blocked')
r=json.loads((dest/'validation.json').read_text());r['entry_qol']={'archived_front_bench_objects':cleared,'reason':'Clear landing from passage into main dining aisles; gameplay adaptation','multi_height_body_width_rays':tests,'body_width_estimate_m':.5,'passage_practical_lights':2};(dest/'validation.json').write_text(json.dumps(r,indent=2)+'\n')
cam=bpy.data.objects['Review v26 | 05_taraj_entry'];cam.location=basis@Vector((-4.4,4.5,1.65));cam.rotation_euler=(basis@Vector((1.5,7,1.45))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100;scene.render.resolution_x=1400;scene.render.resolution_y=1000
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary entry review sun','SUN');ld.energy=2.2;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name in ('05_taraj_entry','10_taraj_cutaway'):
    hidden=[]
    if name.endswith('cutaway'):
        for o in scene.objects:
            if o.name.startswith(('Taraj v23 | upper cream mass','Taraj v23 | roof flat placeholder cap')) or ('| Taraj |' in o.name and any(t in o.name for t in ('ceiling backing','ceiling board','ceiling AC','AC louvre','downlight','smooth scalloped arch header','booth top beam'))):hidden.append((o,o.hide_render));o.hide_render=True
    scene.camera=bpy.data.objects['Review v26 | '+name];scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
    for o,state in hidden:o.hide_render=state
print(json.dumps(r['entry_qol']))
