"""Preserve v20 shopfronts and move the complete fridge against the bar end."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-opposite-shopfronts-v20.blend'
out=ROOT/'assets/blender/pharmacie-shopfronts-fridge-v21.blend'
assert not out.exists()
def bounds(o):
    p=[o.matrix_world@Vector(c) for c in o.bound_box]
    return [[min(v[i] for v in p),max(v[i] for v in p)] for i in range(3)]
group=[o for o in bpy.data.objects if o.type=='MESH' and 'fridge' in o.name.lower()]
assert len(group)==16
before={o.name:bounds(o) for o in group}
# The return counter has a wider left edge than the front run. Keep 5 mm
# clear of its outermost timber so neither cabinet nor door trim intersects it.
edge=min(bounds(bpy.data.objects[n])[0][0] for n in ('Bar | counter top 0','Bar | counter top 1','Bar | cabinet run 0','Bar | cabinet run 1'))
dx=edge-.005-max(bounds(o)[0][1] for o in group)
delta=Vector((dx,-.28,0))
for o in group:
    m=o.matrix_world.copy();m.translation+=delta;o.matrix_world=m
    o['placement_note']='v21: beside left bar end; user-directed flush placement; Facebook 61s reference'
bpy.context.view_layer.update()
for o in group:
    b=bounds(o)
    for i in range(3):
        for j in range(2):assert abs(b[i][j]-before[o.name][i][j]-delta[i])<1e-5
report={'moved_meshes':16,'world_translation_m':list(delta),'minimum_bar_end_clearance_m':.005,'reference':'assets/video-references/facebook-18ZXq1yVKY/stills/0061.0.jpg','placement':'Beside left bar return; front brought forward 0.28 m. Exact appliance position is estimated, not surveyed.','radiant_or_game_verified':False}
scene=bpy.data.scenes['01 Ground floor - mapped rooms'];bpy.context.window.scene=scene
cd=bpy.data.cameras.new('Review v21 | fridge against bar');cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam)
cam.location=(-2.0,12.3,1.8);cam.rotation_euler=(Vector((.4,16.1,1.1))-cam.location).to_track_quat('-Z','Y').to_euler();cd.lens=28;scene.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=str(out))
dest=ROOT/'recon/v21';dest.mkdir(exist_ok=True)
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
# Temporary render lighting is deliberately not saved into the map.
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=800;scene.render.resolution_percentage=100
for name,loc,energy,size in [('bar review fill',(2,13,3),600,4),('fridge review fill',(-1,14,2.6),250,2)]:
    ld=bpy.data.lights.new(name,'AREA');ld.energy=energy;ld.shape='DISK';ld.size=size
    ob=bpy.data.objects.new(name,ld);scene.collection.objects.link(ob);ob.location=loc
    ob.rotation_euler=(Vector((1,16,1))-ob.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath=str(dest/'01_fridge_against_bar.png');bpy.ops.render.render(write_still=True)
print(json.dumps(report))
