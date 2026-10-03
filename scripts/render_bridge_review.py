"""Read-only bridge inspection cameras, renders and visibility measurements."""
from pathlib import Path
import bpy,json,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/bridge-v25';dest.mkdir(exist_ok=True)
source=Path(bpy.data.filepath);before=hashlib.sha256(source.read_bytes()).hexdigest()
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
water=next(o for o in scene.objects if 'F003 | water under bridge' in o.name)
basis=water.matrix_world.copy()
def pos(x,y,z):return basis@Vector((x,y,z))
views=[('01_bridge_overview',(16,-20,16),(0,0,0),None),('02_player_west_brook',(0,-4.6,1.7),(0,-11,-.25),None),('03_player_east_brook',(0,4.6,1.7),(0,11,-.25),None),('04_bridge_side_structure',(7,-15,2),(0,-3,-.3),None),('05_bridge_and_access_plan',(0,0,55),(0,0,0),60)]
deps=bpy.context.evaluated_depsgraph_get();visibility=[]
for y in (-12,-8,8,12):
    hit,loc,n,idx,ob,ma=scene.ray_cast(deps,pos(0,y,10),Vector((0,0,-1)),distance=20)
    visibility.append({'channel_offset':y,'first_surface':ob.name if hit else None,'height':round(loc.z,3) if hit else None,'water_visible':hit and ob==water})
report={'source':str(source.relative_to(ROOT)),'source_sha256':before,'read_only_inspection':True,'water_visibility_samples':visibility,'views':[v[0] for v in views]}
(dest/'inspection.json').write_text(json.dumps(report,indent=2)+'\n')
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100;scene.render.resolution_x=1400;scene.render.resolution_y=1000
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
ld=bpy.data.lights.new('Temporary bridge inspection daylight','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name,eye,target,ortho in views:
    cd=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,cd);scene.collection.objects.link(cam);cam.location=pos(*eye);cam.rotation_euler=(pos(*target)-cam.location).to_track_quat('-Z','Y').to_euler();cd.lens=26
    if ortho:cd.type='ORTHO';cd.ortho_scale=ortho
    scene.camera=cam;scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
print(json.dumps(report))
