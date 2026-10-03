"""Apply all seven selected v06 review fixes; save v07, no BO3 rebuild."""
from pathlib import Path
import json
import math
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-layout-fixed-v07.blend'
BACKUP=ROOT/'assets/blender/pharmacie-v06-before-layout-fixes.blend'
assert Path(bpy.data.filepath).name=='pharmacie-gameplay-space-v06.blend'
if OUT.exists() or BACKUP.exists():raise RuntimeError('Preserve existing review-fix versions')
if bpy.context.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.wm.save_as_mainfile(filepath=str(BACKUP),copy=True)
active_scene=bpy.context.window.scene

def update():
    for s in bpy.data.scenes:
        for vl in s.view_layers:vl.update()

def descendants(root):
    return [root]+list(root.children_recursive)

def bounds(objects):
    points=[o.matrix_world@v.co for o in objects if o.type=='MESH' for v in o.data.vertices]
    return [(min(p[i] for p in points),max(p[i] for p in points)) for i in range(3)]

def level(o):
    n=0;p=o.parent
    while p:n+=1;p=p.parent
    return n

def transform(objects,fn):
    objects=list(objects);update()
    matrices={o:o.matrix_world.copy() for o in objects}
    vertices={o:[o.matrix_world@v.co for v in o.data.vertices] for o in objects if o.type=='MESH'}
    for depth in sorted(set(level(o) for o in objects)):
        for o in objects:
            if level(o)!=depth:continue
            m=matrices[o].copy();m.translation=fn(m.translation.copy());o.matrix_world=m
        update()
    for o,points in vertices.items():
        inv=o.matrix_world.inverted();o.data=o.data.copy()
        for v,p in zip(o.data.vertices,points):v.co=inv@fn(p.copy())
    update()

def group(name,dx=0,dy=0,height=None,base=0,xy_size=None,target_xy=None):
    root=bpy.data.objects[name];objects=descendants(root);update()
    b=bounds(objects);cx=sum(b[0])/2;cy=sum(b[1])/2
    sx=xy_size[0]/(b[0][1]-b[0][0]) if xy_size else 1
    sy=xy_size[1]/(b[1][1]-b[1][0]) if xy_size else 1
    zfactor=(height-base)/(b[2][1]-base) if height is not None else 1
    tx,ty=target_xy if target_xy else (cx+dx,cy+dy)
    def fn(p):return Vector((tx+(p.x-cx)*sx,ty+(p.y-cy)*sy,base+(p.z-base)*zfactor))
    transform(objects,fn)
    root['layout_review_fix']='v07: seating clearance and furniture height review'
    return {'name':name,'before':b,'after':bounds(objects)}

records=[]
# Bar approach and dentist cluster: move the nearby medical table/stools as a
# set, opening the route ahead of the bar rather than shuffling one loose stool.
for name in ('Left-side | medical table 9.0','Left-side | stool 9.0 A','Left-side | stool 9.0 B'):
    records.append(group(name,dx=2.8,dy=-1.2,height=.78 if 'table' in name else .50))
records.append(group('Dentist seating | cream bucket chair 1',dy=-.4,height=.90))
records.append(group('Dentist seating | cream bucket chair 2',dy=.8,height=.90))
records.append(group('Dentist seating | low coffee table',height=.45,xy_size=(1,.65),target_xy=(.5,12.2)))

# Move the complete front set onto its platform before normalising its heights.
for name in ('Platform | medical table 2.65','Platform | high stool 2.65 A','Platform | high stool 2.65 B'):
    records.append(group(name,dy=.9,height=1.05 if 'table' in name else 1.02,base=.27))
for name in ('Platform | medical table 5.1','Platform | medical table 7.7'):
    records.append(group(name,height=1.05,base=.27))
for name in ('Platform | high stool 5.1 A','Platform | high stool 5.1 B','Platform | high stool 7.7 A','Platform | high stool 7.7 B'):
    records.append(group(name,height=1.02,base=.27))
records.append(group('Left-side | medical table 2.6',height=.78))
for name in ('Left-side | stool 2.6 A','Left-side | stool 2.6 B'):
    records.append(group(name,height=.50))
for name in ('Left wall | sofa section 1','Left wall | sofa section 2'):
    # Restore a ~0.5m seat cushion height, while preserving sofa footprint.
    o=bpy.data.objects[name+' | seat cushion'];update();z=bounds([o])[2][1]
    objects=descendants(bpy.data.objects[name])
    transform(objects,lambda p:Vector((p.x,p.y,p.z*.5/z)))
records.append(group('Left wall | dentist chair + skeleton placeholder',height=1.80))

# Counter, drawer photo, pumps and backbar fittings stay aligned vertically.
update();bar_top=bounds([bpy.data.objects['Bar | counter top 0']])[2][1]
bar_objects=[o for o in bpy.data.objects if o.name.startswith('Bar |') and o.type in ('MESH','EMPTY')]
transform(bar_objects,lambda p:Vector((p.x,p.y,p.z*1.10/bar_top)))
for o in bar_objects:o['layout_review_fix']='v07: counter height1.10m; wide footprint retained'
for name in ('Kitchen | left preparation run','Kitchen | sink and hob run','Kitchen | central prep table'):
    if name in bpy.data.objects:
        o=bpy.data.objects[name];update();top=bounds([o])[2][1]
        transform([o],lambda p:Vector((p.x,p.y,4.8+(p.z-4.8)*.9/(top-4.8))))

# Replace only the derivative passage meshes, retaining names/collections.
def prism_mesh(obj,polygon,low=-.25,high=0):
    n=len(polygon);mesh=bpy.data.meshes.new(obj.name+' | corrected geometry')
    verts=[(x,y,z) for z in (low,high) for x,y in polygon]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh.from_pydata(verts,[],faces);mesh.update()
    for mat in obj.data.materials:mesh.materials.append(mat)
    obj.data=mesh

inner=[(-2.46,0),(-2.64,3),(-2.72,9.38),(-5.80,30.65),(-5.85,33)]
outer=[(x-1.8,y) for x,y in reversed(inner)]
prism_mesh(bpy.data.objects['Street | left side passage'],inner+outer)
prism_mesh(bpy.data.objects['Street | rear exit landing'],[(-7.65,30.5),(2,30.5),(2,34),(-7.65,34)])
bpy.data.objects['Street | left side passage']['layout_review_fix']='1.8m wide, follows skewed west wall to rear landing'

# Guard internal stair-void edges, leaving the arrival edge open.
update();floor=bpy.data.objects['First | floor with corrected L stairwell opening']
vs=[floor.matrix_world@v.co for v in floor.data.vertices];counts={}
for p in floor.data.polygons:
    if not all(abs(vs[i].z-4.8)<.01 for i in p.vertices):continue
    ids=list(p.vertices)
    for a,b in zip(ids,ids[1:]+ids[:1]):
        key=tuple(sorted((a,b)));counts[key]=counts.get(key,0)+1
floor_bvh=BVHTree.FromPolygons(vs,[list(p.vertices) for p in floor.data.polygons])
guards=bpy.data.collections.new('GAMEPLAY | Upstairs stairwell edge guards')
for scene in bpy.data.scenes:
    if scene.name.startswith(('02','03')):scene.collection.children.link(guards)
metal=next(m for m in bpy.data.materials if m.name.startswith('Blockout - rails'))
scale=bpy.data.objects['GAMEPLAY | Pub scale 1.50 - frontage 10.5m']

def beam(name,a,b,width=.055):
    d=(b-a).normalized()
    u=d.cross(Vector((0,0,1)))
    if u.length<.01:u=d.cross(Vector((1,0,0)))
    u.normalize();u*=width/2;v=d.cross(u).normalized()*width/2
    verts=[p+su*u+sv*v for p in (a,b) for su,sv in ((-1,-1),(1,-1),(1,1),(-1,1))]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
    mesh.materials.append(metal);mesh.update()
    o=bpy.data.objects.new(name,mesh);guards.objects.link(o)
    o.parent=scale;o.matrix_parent_inverse=scale.matrix_world.inverted()
    o['bo3_role']='solid stairwell guard geometry'
    return o

guard_edges=[]
for (ia,ib),count in counts.items():
    if count!=1:continue
    a,b=vs[ia].copy(),vs[ib].copy()
    if min(a.y,b.y)<24.9:continue
    if abs(a.x-b.x)>.015 and abs(a.y-b.y)>.015:continue # outer skewed shell
    if abs(a.y-25.013)<.05 and abs(b.y-25.013)<.05:continue # open stair arrival
    d=b-a
    if d.length<.12:continue
    normal=Vector((-d.y,d.x,0)).normalized()
    center=(a+b)/2
    hit=floor_bvh.ray_cast(center+normal*.12+Vector((0,0,.2)),Vector((0,0,-1)),.5)
    if hit[0] is None:normal=-normal
    a+=normal*.085;b+=normal*.085
    n=len(guard_edges)+1
    for height in (.55,1.05):beam(f'Stair guard {n:02} | rail {height}',a+Vector((0,0,height)),b+Vector((0,0,height)))
    for j in range(max(1,math.ceil(d.length/.9))+1):
        p=a+(b-a)*(j/max(1,math.ceil(d.length/.9)))
        beam(f'Stair guard {n:02} | post {j:02}',p,p+Vector((0,0,1.05)))
    guard_edges.append({'start':list(a),'end':list(b)})

update()
table=bounds(descendants(bpy.data.objects['Left-side | medical table 9.0']))
stool=bounds(descendants(bpy.data.objects['Left-side | stool 9.0 B']))
bar=bounds([bpy.data.objects['Bar | counter top 0']])
gap=bar[1][0]-stool[1][1]
assert gap>1.5,gap
platform=bounds(descendants(bpy.data.objects['Raised right-hand seating platform']))
frontset=[bounds(descendants(bpy.data.objects[name])) for name in ('Platform | medical table 2.65','Platform | high stool 2.65 A','Platform | high stool 2.65 B')]
assert all(b[1][0]>platform[1][0] and b[1][1]<platform[1][1] for b in frontset)
assert abs(bar[2][1]-1.10)<.001
assert len(guard_edges)>=5
manifest={'file':str(OUT),'safety_copy':str(BACKUP),'review':'docs/LAYOUT_REVIEW_V06.md',
    'all_seven_fixes_applied':True,'furniture_changes':records,'counter_height_m':bar[2][1],
    'bar_approach_gap_m':gap,'outside_path_inner_edge_xy':inner,'outside_path_width_m':1.8,
    'stair_guard_edges':guard_edges,'arrival_left_open':True,
    'radiant_rebuilt':False,'runtime_verified':False,'validation':'Mesh bounds/geometry assertions and visual previews; in-game traversal pending'}
(ROOT/'assets/blender/layout-fixed-v07-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for s in bpy.data.scenes:s['gameplay_version']='v07 - all seven layout review fixes, Blender only'
bpy.context.window.scene=active_scene
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'saved':str(OUT),'backup':str(BACKUP),'bar_height_m':bar[2][1],'bar_approach_gap_m':gap,
    'guarded_edges':len(guard_edges),'guard_objects':len(guards.objects),'radiant_rebuilt':False}
