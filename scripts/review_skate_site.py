import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v59'
s=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=s
c=bpy.data.cameras.new('TEMP skate site');o=bpy.data.objects.new(c.name,c);s.collection.objects.link(o);s.camera=o
o.location=(-5,-3,65);o.rotation_euler=(Vector((-5,-3,0))-o.location).to_track_quat('-Z','Y').to_euler();c.type='ORTHO';c.ortho_scale=115
s.render.engine='BLENDER_WORKBENCH';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True
s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.filepath=str(dest/'skate-site-before.png');bpy.ops.render.render(write_still=True)
print('SITE_RENDER_COMPLETE',flush=True)
