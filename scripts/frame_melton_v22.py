"""Final overview framing and remove coincident apron/foundation surfaces."""
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-melton-road-v22.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
for v in bpy.data.objects['Street v22 | Roundabout pavement apron'].data.vertices:
    if abs(v.co.z+.12)<.001:v.co.z=-.13
cam=bpy.data.objects['Review v22 | 01_route_overview'];cam.data.ortho_scale=380;scene.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary daylight','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.4,-.5,-.4)
for name in ('01_route_overview','02_roundabout'):
    scene.camera=bpy.data.objects['Review v22 | '+name];scene.render.resolution_x=1200 if 'overview' in name else 1400;scene.render.resolution_y=1600 if 'overview' in name else 1000
    scene.render.filepath=str(ROOT/'recon/v22'/(name+'.png'));bpy.ops.render.render(write_still=True)
