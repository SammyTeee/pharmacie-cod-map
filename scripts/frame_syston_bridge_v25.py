"""Correct the saved first review camera after the bridge moved into its gap."""
from pathlib import Path
import bpy,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-syston-street-v25.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
cam=bpy.data.objects['Review v25 | 06_bridge_player']
# Original camera was left behind the moved bridge. Shift along the same segment.
if not cam.get('final_bridge_framed'):
    cam.location+=Vector((.52083,13.56310,0));cam['final_bridge_framed']=True
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_x=1400;scene.render.resolution_y=950;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
ld=bpy.data.lights.new('Temporary camera review sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
scene.render.filepath=str(ROOT/'recon/v25/06_bridge_player.png');bpy.ops.render.render(write_still=True)
