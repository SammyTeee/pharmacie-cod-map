"""Carry frontage width through the skewed plan; Blender only, saved v06."""
from pathlib import Path
import json
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-gameplay-space-v06.blend'
assert Path(bpy.data.filepath).name=='pharmacie-gameplay-space-v05.blend'
if OUT.exists():raise RuntimeError('Preserve existing v06 before rerunning')
for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
scale=bpy.data.objects['GAMEPLAY | Pub scale 1.50 - frontage 10.5m']
front_rig=bpy.data.objects['GAMEPLAY | Front width matches building - 12.66m']
factor=front_rig['width_factor']
right=10.5
left=right-right*factor
center=(left+right)/2
EXTRA=.08

def descends(obj,parent):
    p=obj.parent
    while p:
        if p==parent:return True
        p=p.parent
    return False

body=[o for o in bpy.data.objects if descends(o,scale) and not descends(o,front_rig) and o!=front_rig
      and not o.name.startswith(('Model reference','Reference |')) and 'original plan' not in o.name.lower()]
matrices={o:o.matrix_world.copy() for o in body}
world_vertices={o:[o.matrix_world@v.co for v in o.data.vertices] for o in body if o.type=='MESH'}

def source_point(p,undo_front=False):
    q=p.copy()
    if undo_front:
        w=max(0,min(1,1-p.y/9.4))
        q.x=(p.x+right*(factor-1)*w)/(1+(factor-1)*w)
    return q

def widen(p):
    q=p.copy()
    q.x=left+factor*p.x
    w=max(0,min(1,p.y/9.4))
    q.x=center+(q.x-center)*(1+EXTRA*w)
    return q

def depth(obj):
    n=0;p=obj.parent
    while p:n+=1;p=p.parent
    return n

# Move origins as well as geometry so hinges and grouped furnishings remain
# useful. Update between hierarchy levels before assigning child world matrices.
levels=sorted(set(depth(o) for o in body))
for level in levels:
    for o in body:
        if depth(o)!=level:continue
        m=matrices[o].copy();m.translation=widen(m.translation)
        o.matrix_world=m
    for s in bpy.data.scenes:
        for vl in s.view_layers:vl.update()

for o,vertices in world_vertices.items():
    undo='gameplay_frontage_adjustment' in o
    inv=o.matrix_world.inverted();o.data=o.data.copy()
    for vertex,p in zip(o.data.vertices,vertices):
        vertex.co=inv@widen(source_point(p,undo))
    o['gameplay_body_adjustment']='Plan angles/steps retained, front-width scale carried through plus8% behind entrance'

for s in bpy.data.scenes:
    for vl in s.view_layers:vl.update()
floor=bpy.data.objects['Ground | continuous timber floor']
points=[floor.matrix_world@v.co for v in floor.data.vertices if (floor.matrix_world@v.co).z>-.01]

def section_width(y):
    # Boundary edges of the top surface, excluding triangulation diagonals.
    mesh=floor.data;edge_count={}
    for p in mesh.polygons:
        if not all((floor.matrix_world@mesh.vertices[i].co).z>-.01 for i in p.vertices):continue
        ids=list(p.vertices)
        for a,b in zip(ids,ids[1:]+ids[:1]):
            key=tuple(sorted((a,b)));edge_count[key]=edge_count.get(key,0)+1
    crossings=[]
    for (a,b),count in edge_count.items():
        if count!=1:continue
        p=floor.matrix_world@mesh.vertices[a].co;q=floor.matrix_world@mesh.vertices[b].co
        if min(p.y,q.y)<=y<max(p.y,q.y):
            crossings.append(p.x+(q.x-p.x)*(y-p.y)/(q.y-p.y))
    return max(crossings)-min(crossings) if len(crossings)>=2 else None

bar=bpy.data.objects['Bar | counter top 0']
bar_points=[bar.matrix_world@v.co for v in bar.data.vertices]
bar_width=max(p.x for p in bar_points)-min(p.x for p in bar_points)
manifest=json.loads((ROOT/'assets/blender/gameplay-space-v05-manifest.json').read_text())
manifest.update({'file':str(OUT),'body_width_relative_factor':factor,'extra_body_width_factor':1+EXTRA,
    'bar_main_counter_width_m':bar_width,
    'body_sections_m':{str(y):section_width(y) for y in (3,8,15,22,29)},
    'floor_envelope_width_m':max(p.x for p in points)-min(p.x for p in points),
    'shape':'Original plan side angles/steps retained; not a rectangular or exact rhombus footprint',
    'radiant_rebuilt':False,'runtime_verified':False})
# Planning risers follow their corresponding body area; street markers stay put.
for name in ('ZOMBIES | planned 3 rear outside','ZOMBIES | planned 4 upstairs'):
    marker=bpy.data.objects[name];marker.location=widen(marker.location)
manifest['zombie_markers']=[{'name':o.name,'position_m':list(o.location),'route_goal':o.get('route_goal','')}
                          for o in bpy.data.objects if o.name.startswith('ZOMBIES | planned')]
for s in bpy.data.scenes:s['gameplay_version']='v06 - skewed wider body, Blender only'
(ROOT/'assets/blender/gameplay-space-v06-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'saved':str(OUT),'frontage_width_unchanged_m':manifest['frontage_width_m'],
    'bar_counter_width_m':bar_width,'body_sections_m':manifest['body_sections_m'],
    'body_objects_adjusted':len(body),'radiant_rebuilt':False}
