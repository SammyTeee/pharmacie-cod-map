"""Reuse established pub route probes on latest checkpoint; no scene saves."""
from pathlib import Path
import os,json,bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'recon/v28-zombies/pub';dest.mkdir(exist_ok=True)
os.environ['PHARMACIE_RECON_PHASE']='after'
os.environ['PHARMACIE_RECON_OUTPUT']=str(dest)
os.environ['PHARMACIE_RECON_VIEWS']='02_threshold_inward,04_main_room_to_bar,08_bar_front,12_stairs_start,14_stairs_turn,16_upper_arrival,17_upstairs_seating,20_alley_entrance,22_alley_rear,32_rear_exit_clear,34_left_bar_route,36_alley_connection'
code=(ROOT/'scripts/recon_blender_players.py').read_text()
code=code.replace('scene.cycles.samples=12','scene.cycles.samples=8').replace('resolution_x=1100','resolution_x=960').replace('resolution_y=700','resolution_y=540')
# Keep all signs visible for this review.
code=code.replace("if o.type=='FONT' and not o.name.startswith('Street v17 |'):o.hide_render=True","if False:o.hide_render=True")
exec(compile(code,str(ROOT/'scripts/recon_blender_players.py'),'exec'))
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.render.resolution_x=640;scene.render.resolution_y=360
out=dest/'frames';out.mkdir(exist_ok=True)
data=json.loads((dest/'view-probes.json').read_text());frame=0;segments=[]
for v in data['views']:
    if v['view'] not in ['04_main_room_to_bar','08_bar_front','12_stairs_start','16_upper_arrival','17_upstairs_seating','22_alley_rear']:continue
    cam=scene.camera;eye=Vector(v['eye']);cam.rotation_euler=(Vector(v['look_at'])-eye).to_track_quat('-Z','Y').to_euler()
    f=cam.rotation_euler.to_quaternion()@Vector((0,0,-1))
    for k in range(36):
        cam.location=eye+f*(k/35*.45);scene.render.filepath=str(out/f'{frame:05d}.png');bpy.ops.render.render(write_still=True);frame+=1
    segments.append({'view':v['view'],'start_seconds':(frame-36)/12,'duration_seconds':3})
(dest/'video-segments.json').write_text(json.dumps(segments,indent=2))
print('PUB_REVIEW_COMPLETE',frame,flush=True)
