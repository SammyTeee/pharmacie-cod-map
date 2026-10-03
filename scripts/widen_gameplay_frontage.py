"""Widen gameplay frontage and repair v04 transform update; Blender only."""
from pathlib import Path
import json
import math
import bpy
from mathutils import Matrix, Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-gameplay-space-v05.blend'
assert Path(bpy.data.filepath).name=='pharmacie-gameplay-space-v04.blend'
if OUT.exists():raise RuntimeError('Preserve existing v05 before rerunning')
for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
scale=bpy.data.objects['GAMEPLAY | Pub scale 1.50 - frontage 10.5m']
# Repair local transforms in the initial v04 save, if it predates the fix.
# Mesh edits already exist, so only jamb/hinge/return transforms need repair.
v04_manifest=json.loads((ROOT/'assets/blender/gameplay-space-v04-manifest.json').read_text())
for record in v04_manifest['doorways']:
    base=record['name']
    j0=bpy.data.objects[base+' | jamb 0'];j1=bpy.data.objects[base+' | jamb 1']
    hinge=bpy.data.objects[base+' | hinge']
    direction=j1.location-j0.location;direction.z=0
    width=direction.length;direction.normalize()
    extra=max(0,.95-width)
    j0.location-=direction*extra/2;j1.location+=direction*extra/2
    hinge.location-=direction*extra/2
    hinge.rotation_euler.z=math.atan2(direction.y,direction.x)+(-1 if 'First | toilets front' in base else 1)*math.pi/2
for name in ('Front | entrance leaf 1 hinge','Front | entrance leaf 2 hinge'):
    bpy.data.objects[name].rotation_euler.z=math.pi/2
for name in ('Bar | cabinet run 1','Bar | counter top 1'):
    bpy.data.objects[name].location.x=max(bpy.data.objects[name].location.x,1.501582384109497)
for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
floor=bpy.data.objects['Ground | continuous timber floor']
floor_world=[floor.matrix_world@v.co for v in floor.data.vertices]
left=min(v.x for v in floor_world);right=max(v.x for v in floor_world)
front_width=10.5
factor=(right-left)/front_width
front_collections=[c for c in bpy.data.collections if c.name.startswith(('BLOCKOUT | Frontage','BLOCKOUT | Upper frontage'))]
front_objects=set(o for c in front_collections for o in c.objects)
# A reversible X-only rig preserves the photo frontage, UVs and hinge groups.
rig=bpy.data.objects.new('GAMEPLAY | Front width matches building - 12.66m',None)
scale.users_collection[0].objects.link(rig)
rig.parent=scale;rig.matrix_parent_inverse=Matrix.Identity(4)
rig['width_factor']=factor;rig['matched_width_m']=right-left
rig['reason']='User requested front match widest part instead of narrower plan frontage'
for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
for obj in front_objects:
    if obj.parent!=scale:continue
    matrix=obj.matrix_world.copy()
    obj.parent=rig;obj.matrix_parent_inverse=Matrix.Identity(4)
    obj.matrix_world=matrix
for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
rig.scale=(factor,1,1)
rig.location.x=left/1.5
for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()

def deformed(p):
    # Full frontage widening at Y=0, taper back to source at 9.4m from street.
    weight=max(0,min(1,1-p.y/9.4))
    q=p.copy();q.x+=(p.x-right)*(factor-1)*weight
    return q

modified=[]
for obj in list(bpy.data.objects):
    if obj.type!='MESH' or obj in front_objects:continue
    ancestor=obj.parent
    while ancestor and ancestor!=scale:ancestor=ancestor.parent
    if ancestor!=scale:continue
    if obj.name.startswith(('Model reference','Reference |')) or 'original plan' in obj.name.lower():continue
    world=[obj.matrix_world@v.co for v in obj.data.vertices]
    if not world or min(v.y for v in world)>=9.4:continue
    inv=obj.matrix_world.inverted()
    obj.data=obj.data.copy()
    for vertex,p in zip(obj.data.vertices,world):vertex.co=inv@deformed(p)
    obj['gameplay_frontage_adjustment']='Front width tapers into original layout over first9.4m'
    modified.append(obj.name)

# Move the outside player guide to face the widened entrance centre.
entrance=[bpy.data.objects[n].matrix_world.translation for n in ('Front | entrance leaf 1 hinge','Front | entrance leaf 2 hinge')]
spawn=bpy.data.objects['SPAWN | player outside - facing pub']
old_x=spawn.location.x;spawn.location.x=sum(p.x for p in entrance)/2
guide=bpy.data.objects['CLEARANCE | BO3 player 32x32x72 map units']
guide.location.x+=spawn.location.x-old_x

for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
manifest=json.loads((ROOT/'assets/blender/gameplay-space-v04-manifest.json').read_text())
verified=[]
for d in manifest['doorways']:
    a=bpy.data.objects[d['name']+' | jamb 0'].matrix_world.translation
    b=bpy.data.objects[d['name']+' | jamb 1'].matrix_world.translation
    # Local jamb objects are already shifted to the widened portal; their
    # world matrices require updates in every scene, including upstairs.
    clear=(b-a).length-.12
    assert clear>1.28,(d['name'],clear)
    verified.append({'name':d['name'],'estimated_frame_gap_m':clear})
manifest.update({'file':str(OUT),'frontage_width_m':right-left,'frontage_width_factor':factor,
    'frontage_taper_depth_m':9.4,'doorway_jamb_world_checks':verified,
    'bar_main_counter_width_m':bpy.data.objects['Bar | counter top 0'].dimensions.x,
    'player_spawn_m':list(spawn.location),'radiant_rebuilt':False,'runtime_verified':False,
    'transform_fix':'Update all scene view layers before matrix reads and reparenting'})
(ROOT/'assets/blender/gameplay-space-v05-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for s in bpy.data.scenes:s['gameplay_version']='v05 - wider front, Blender edits only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'saved':str(OUT),'frontage_width_m':right-left,'width_factor':factor,
    'bar_main_counter_width_m':manifest['bar_main_counter_width_m'],
    'min_jamb_gap_m':min(d['estimated_frame_gap_m'] for d in verified),'adjusted_meshes':len(modified),'radiant_rebuilt':False}
