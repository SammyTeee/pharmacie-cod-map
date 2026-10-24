"""Fast low-resolution solid inspection video; never saves the source scene."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v28-zombies';out=dest/'video-frames';out.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='BLENDER_WORKBENCH';scene.display.render_aa='OFF'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL'
scene.display.shading.show_shadows=False;scene.display.shading.show_cavity=False
scene.display.shading.background_type='WORLD';scene.world=scene.world.copy();scene.world.color=(.10,.13,.18)
scene.render.resolution_x=640;scene.render.resolution_y=360;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
data=bpy.data.cameras.new('Temporary fast review camera');cam=bpy.data.objects.new(data.name,data);scene.collection.objects.link(cam);scene.camera=cam
shots=[]
for term in ['crossing','amy_clarke','02_costa_and_town_square','06_bridge_player','01_taraj_dining','05_taraj_entry','03_taraj_bar']:
    c=next(o for o in scene.objects if o.type=='CAMERA' and o.name.startswith('Review') and o.name.endswith(term))
    shots.append((term,c.location.copy(),c.rotation_euler.copy(),c.data.lens))
for v in json.loads((dest/'pub/view-probes.json').read_text())['views']:
    if v['view'] in ['04_main_room_to_bar','08_bar_front','12_stairs_start','16_upper_arrival','17_upstairs_seating','22_alley_rear']:
        eye=Vector(v['eye']);shots.append((v['view'],eye,(Vector(v['look_at'])-eye).to_track_quat('-Z','Y').to_euler(),22))
frame=0;manifest=[]
for name,eye,rot,lens in shots:
    cam.rotation_euler=rot;data.lens=lens;forward=rot.to_quaternion()@Vector((0,0,-1))
    for k in range(16):
        cam.location=eye+forward*(k/15*.45);scene.render.filepath=str(out/f'{frame:05d}.png');bpy.ops.render.render(write_still=True);frame+=1
    manifest.append({'view':name,'start_seconds':(frame-16)/8,'duration_seconds':2})
(dest/'video-segments.json').write_text(json.dumps({'fps':8,'frames':frame,'style':'Solid material inspection; short dolly shots and cuts, not continuous proved traversal','segments':manifest},indent=2))
print('FAST_VIDEO_COMPLETE',frame,flush=True)
