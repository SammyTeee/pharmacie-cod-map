"""Blender-only swept route samples and ground support, not BO3 tests."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
name=Path(bpy.data.filepath).name
assert name in ('pharmacie-extension-route-v41.blend','pharmacie-midland-frontage-v42.blend','pharmacie-station-detail-v43.blend','pharmacie-holmdale-house-v44.blend','pharmacie-station-holmdale-v45.blend')
output_version=name.removesuffix('.blend').split('-')[-1]
scene=bpy.context.scene
route=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
verts=[];faces=[];labels=[]
for ob in scene.objects:
 if ob.type!='MESH' or ob.hide_render:continue
 me=ob.data;idx=len(verts)
 verts.extend(ob.matrix_world@v.co for v in me.vertices)
 faces.extend(tuple(idx+i for i in p.vertices) for p in me.polygons)
 labels.extend([ob.name]*len(me.polygons))
tree=BVHTree.FromPolygons(verts,faces,all_triangles=False)
checks=0;blocked=[];floor_checks=0;unsupported=[];floor_heights=[]
def cast(a,b,label):
 global checks
 a=Vector(a);b=Vector(b);delta=b-a
 hit,normal,index,d=tree.ray_cast(a,delta.normalized(),delta.length)
 checks+=1
 if index is not None:blocked.append({'sample':label,'object':labels[index],'position':list(hit)})
def floor(p,label):
 global floor_checks
 hit,normal,index,d=tree.ray_cast(Vector((p.x,p.y,.35)),Vector((0,0,-1)),.65)
 floor_checks+=1
 if index is None:unsupported.append({'sample':label,'position':list(p)})
 else:floor_heights.append(hit.z)
route['station_link']=json.loads((ROOT/'recon/v41/joined-surfaces.json').read_text())['station_final_link']
keys=['main','holmdale','station_access','station_link']
if output_version in ('v44','v45'):
 basis=bpy.data.objects['Holmdale v44 | Movable number 29 assembly'].matrix_world
 for key,points in {'house_approach':[(4,-11.5,0),(4,-1.3,0)],'garage_approach':[(12,-11.5,0),(12,-1.1,0)],'drive_crossing':[(3,-3,0),(13,-3,0)]}.items():
  route[key]=[list((basis@Vector(p))[:2]) for p in points];keys.append(key)
if output_version=='v45':
 prepared=json.loads((ROOT/'recon/v45/prepared-surfaces.json').read_text())
 for key,points in prepared['extra_routes'].items():route[key]=points;keys.append(key)
 frame=prepared['station_frame'];a=Vector(frame['origin']);u=Vector(frame['u']);n=Vector(frame['n'])
 route['station_parking']=[list(a+u*x+n*y) for x,y in ((-50,24),(20,24),(20,8))];keys.append('station_parking')
 end=Vector(route['holmdale'][-1]);t=(end-Vector(route['holmdale'][-2])).normalized()
 route['holmdale_turning_end']=[list(end-t*.5),list(end+t*3)];keys.append('holmdale_turning_end')
for key in keys:
 pts=[Vector(p) for p in route[key]]
 if key=='main':
  old=json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']
  pts.insert(0,Vector(old[-2]))
  # Stop the walk half a metre before its intentional terminal perimeter wall.
  pts[-1]-=(pts[-1]-pts[-2]).normalized()*.5
 half={'main':4.,'holmdale':2.8,'station_access':2.0,'station_link':1.4}.get(key,0.)
 for i,(a,b) in enumerate(zip(pts,pts[1:])):
  u=(b-a).normalized();n=Vector((-u.y,u.x));length=(b-a).length
  count=math.ceil(length/.85)
  for j in range(count):
   p=a+u*(length*j/count);q=a+u*(length*(j+1)/count)
   for off in (0,half+1.2,-half-1.2):
    pp=p+n*off;qq=q+n*off;label=f'{key}/{i}/{j}/{off}'
    floor(pp,label)
    for z in (.35,1.0,1.7):
     for side in (-.42,0,.42):
      aa=pp+n*side;bb=qq+n*side
      cast((aa.x,aa.y,z),(bb.x,bb.y,z),label)
report={'clearance_rays':checks,'floor_samples':floor_checks,'blocked_count':len(blocked),'unsupported_count':len(unsupported),'blocked':blocked[:60],'unsupported':unsupported[:60],'radius':.42,'heights':[.35,1.,1.7],'method':'Longitudinal short rays with three lateral offsets; downward support samples; selected main/footway centrelines and inferred station link only','limits':['Not full continuous capsule collision.','Not all junction transitions sampled.','Not BO3 collision, navigation, co-op or gameplay tests.']}
enclosure=[]
for key in ('main','holmdale'):
 pts=[Vector(p) for p in route[key]]
 for i,(a,b) in enumerate(zip(pts,pts[1:])):
  p=(a+b)/2;u=(b-a).normalized();n=Vector((-u.y,u.x))
  for side in (-1,1):
   hit,normal,index,d=tree.ray_cast(Vector((p.x,p.y,1.5)),Vector((n.x*side,n.y*side,0)),250)
   enclosure.append({'sample':f'{key}/{i}/{side}','hit':labels[index] if index is not None else None})
report['enclosure_side_rays']=len(enclosure);report['enclosure_misses']=[e for e in enclosure if e['hit'] is None]
report['endpoint_note']='Main walk stops .5m before intentional terminal wall; old-map seam traversal included.'
report['sampled_routes']=keys
report['floor_height_range']=[min(floor_heights),max(floor_heights)]
if output_version in ('v44','v45'):report['method']+='; additional estimated house/garage driveway approaches and driveway crossing sampled'
if output_version=='v45':report['method']+='; parallel station ramp, parking aisle and Holmdale turning end sampled'
(ROOT/f'recon/{output_version}/route-checks.json').write_text(json.dumps(report,indent=2)+'\n')
result={k:v for k,v in report.items() if k not in ('blocked','unsupported')}
