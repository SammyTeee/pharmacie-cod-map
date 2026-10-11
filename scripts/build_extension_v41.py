"""Connected map-data route blockout, additive to v40. Run in live Blender.

Widths/heights/boundaries are gameplay estimates. House architecture is pending
visual identification. Keep the mapped road and provisional features separate.
"""
from pathlib import Path
import bpy, bmesh, json, math, hashlib
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-extension-route-v41.blend'
assert Path(bpy.data.filepath).name=='pharmacie-taraj-bar-v40.blend'
assert not OUT.exists(), 'Never overwrite a milestone'
scene=bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene=scene
route=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
dest=ROOT/'recon/v41';dest.mkdir(exist_ok=True)
def fingerprint(o):
 h=hashlib.sha256()
 h.update(repr([list(row) for row in o.matrix_basis]).encode())
 if o.type=='MESH':
  h.update(repr([tuple(v.co) for v in o.data.vertices]).encode())
  h.update(repr([tuple(p.vertices) for p in o.data.polygons]).encode())
 h.update(repr([m.name if m else None for m in o.data.materials] if hasattr(o.data,'materials') else []).encode())
 return h.hexdigest()
original={o.name:fingerprint(o) for o in scene.objects}
coll=bpy.data.collections.new('MAPPING v41 | OSM Melton station Holmdale route blockout')
scene.collection.children.link(coll)
markers=bpy.data.collections.new('REFERENCE v41 | Locations awaiting visual confirmation')
scene.collection.children.link(markers)
archive=bpy.data.collections.new('ARCHIVE v41 | Retained v34 beyond-Taraj closure')
archive.use_fake_user=True
retired=[]
for name in ('Mapping v34 | Beyond Taraj closed road boundary','Mapping v34 | Beyond Taraj boundary head'):
 o=bpy.data.objects[name];archive.objects.link(o)
 for c in list(o.users_collection):
  if c!=archive:c.objects.unlink(o)
 retired.append(name)
made=[]
def mat(name,c):
 m=bpy.data.materials.new('Extension v41 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.85
 return m
asphalt=bpy.data.materials['Street v36 | aged asphalt Street v17 | asphalt']
paving=bpy.data.materials['Syston v27 | concrete paving joints']
brick=bpy.data.materials['Shop v19 | brick relief']
kerb=mat('pale concrete kerbs',(.43,.42,.38));terrain=mat('earth backing',(.13,.15,.10))
shell=mat('provisional building masses',(.48,.45,.39));cream=mat('Midland mapped footprint provisional render',(.73,.71,.65))
dark=mat('station safety boundary',(.045,.065,.06));white=bpy.data.materials['Street v17 | road white']
def solid(name,poly,z0,z1,m,meta='Estimated gameplay geometry'):
 pts=[tuple(p) for p in poly]
 if pts[0]==pts[-1]:pts=pts[:-1]
 n=len(pts);assert n>=3
 vs=[(x,y,z) for z in (z0,z1) for x,y in pts]
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new('Extension v41 | '+name,me);coll.objects.link(o)
 o['evidence']=meta;o['engine_implemented']=False;made.append(o);return o
def ribbon(name,pts,lo,hi,z0,z1,m):
 pts=[Vector(p) for p in pts];left=[];right=[]
 for i,p in enumerate(pts):
  ua=(pts[i]-pts[i-1]).normalized() if i else (pts[1]-p).normalized()
  ub=(pts[i+1]-p).normalized() if i<len(pts)-1 else ua
  na=Vector((-ua.y,ua.x));nb=Vector((-ub.y,ub.x));n=(na+nb).normalized();div=max(.3,n.dot(nb))
  left.append(p+n*(lo/div));right.append(p+n*(hi/div))
 return solid(name,left+list(reversed(right)),z0,z1,m)
def distance(p,pts):
 p=Vector(p);best=1e9
 for a,b in zip(pts,pts[1:]):
  a=Vector(a);b=Vector(b);v=b-a;t=max(0,min(1,(p-a).dot(v)/v.length_squared));best=min(best,(p-a-v*t).length)
 return best
paths={k:route[k] for k in ('main','holmdale','station_access')}
# Drop the initial station-access points already part of the Melton centreline.
paths['station_access']=paths['station_access'][1:]
widths={'main':4.,'holmdale':2.8,'station_access':2.0}
for key,pts in paths.items():
 half=widths[key]
 ribbon(key+' continuous terrain backing',pts,-24,24,-1.2,-.30,terrain)
 ribbon(key+' continuous carriageway',pts,-half,half,-.30,-.08,asphalt)
 # Footway/kerb fragments deliberately stop at crossing-road mouths.
 for i,(a,b) in enumerate(zip(pts,pts[1:])):
  a=Vector(a);b=Vector(b);u=(b-a).normalized();n=Vector((-u.y,u.x));length=(b-a).length
  count=math.ceil(length/2.0)
  for j in range(count):
   pa=a+u*(length*j/count);pb=a+u*(length*(j+1)/count);mid=(pa+pb)/2
   for side in (-1,1):
    q=mid+n*side*(half+1.1)
    crossing=any(distance(q,other)<widths[k]+.7 for k,other in paths.items() if k!=key)
    if not crossing:
     offsets=sorted([side*(half+.02),side*(half+2.4)])
     ribbon(f'{key} footway {i:02d} {j:02d} {side}',[pa,pb],*offsets,-.25,0,paving)
     offsets=sorted([side*half,side*(half+.18)])
     ribbon(f'{key} kerb {i:02d} {j:02d} {side}',[pa+u*.008,pb-u*.008],*offsets,-.17,.015,kerb)
   # Wide outer containment is a game boundary, not a mapped garden fence.
   for side in (-1,1):
    q=mid+n*side*23.5
    if any(distance(q,other)<24.5 for k,other in paths.items() if k!=key):continue
    offsets=sorted([side*23.3,side*23.65])
    ribbon(f'{key} outer boundary {i:02d} {j:02d} {side}',[pa,pb],*offsets,-.4,2.8,brick)
 # Inferred dashed centre line for main road only; avoids junctions.
 if key=='main':
  for i,(a,b) in enumerate(zip(pts,pts[1:])):
   a=Vector(a);b=Vector(b);u=(b-a).normalized();length=(b-a).length
   for j in range(int(length//7)):
    p=a+u*(j*7+2);q=p+u*2.4
    if any(distance(p,other)<9 for k,other in paths.items() if k!=key):continue
    ribbon(f'main inferred centre dash {i:02d} {j:02d}',[p,q],-.055,.055,-.079,-.074,white)
# Footprint solids, without inventing facade fenestration. Only new route vicinity.
footprints=[]
for w in route['ways']:
 if 'building' not in w['tags']:continue
 pts=w['points'];centre=[sum(p[i] for p in pts[:-1])/(len(pts)-1) for i in range(2)]
 if centre[1]<350:continue
 if min(distance(centre,p) for p in paths.values())>48:continue
 # Avoid mapped footprints overlapping gameplay-expanded circulation.
 if any(min(distance(p,line) for p in pts)<widths[k]+2.9 for k,line in paths.items()):continue
 levels=float(w['tags'].get('building:levels',2));height=levels*3.0
 material=cream if w['id']=='173168754' else shell
 o=solid('OSM footprint '+w['id'],pts,-.30,height,material,'OSM way '+w['id']+' footprint; height estimated; facade pending reference')
 o['osm_way']=w['id'];footprints.append(w['id'])
for w in route['ways']:
 if w['tags'].get('railway')=='platform':
  o=solid('mapped station platform '+w['id'],w['points'],-.35,.03,paving,'OSM platform footprint; elevation provisional')
  o['osm_way']=w['id']
# Editor-only markers. No fabricated house standing in for number 29.
for label,key in [('29 Holmdale USER PIN - visual identity pending','house_pin'),('Syston station mapped location','station_pin'),('Midland Railway mapped location','midland_pin')]:
 o=bpy.data.objects.new('Reference v41 | '+label,None);markers.objects.link(o);o.location=(*route[key],1);o.empty_display_type='CIRCLE';o.empty_display_size=2;o.show_name=True
 o['status']='Location reference only; no house geometry verified';o['engine_implemented']=False
bpy.context.view_layer.update()
assert all(fingerprint(bpy.data.objects[n])==h for n,h in original.items()),'Parent geometry changed'
nonmanifold=[];volumes=[]
for o in made:
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges):nonmanifold.append(o.name)
 if bm.calc_volume(signed=True)<=0:volumes.append(o.name)
 bm.free()
assert not nonmanifold and not volumes,(nonmanifold,volumes)
report={'source':'assets/blender/pharmacie-taraj-bar-v40.blend','output':str(OUT.relative_to(ROOT)),'preserved_parent_objects':len(original),'new_closed_meshes':len(made),'archived_unchanged':retired,'osm_building_footprints':footprints,'nonmanifold':nonmanifold,'nonpositive_volume':volumes,'route_checks_pending':True,'house_modelled':False,'engine_implemented':False,'limits':route['limits']}
(dest/'build-validation.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result=report
