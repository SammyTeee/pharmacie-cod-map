"""Frame the cleared restaurant landing from the open passage doorway."""
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
basis=next(o for o in scene.objects if '| Taraj | carpet floor' in o.name).matrix_world.copy()
cam=bpy.data.objects['Review v26 | 05_taraj_entry'];cam.location=basis@Vector((-4.4,4.5,1.65));cam.rotation_euler=(basis@Vector((1.5,7,1.45))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.55
scene.camera=cam;scene.render.filepath=str(ROOT/'recon/v26/05_taraj_entry.png');bpy.ops.render.render(write_still=True)
