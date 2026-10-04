"""Trace connected camera routes with saved-scene ray clearance, not engine nav."""
from pathlib import Path
import bpy,json,os,math,heapq
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v33'
os.environ.update(PHARMACIE_RECON_PHASE='after',PHARMACIE_RECON_OUTPUT=str(dest/'camera-checks'),
                  PHARMACIE_RECON_PROBES_ONLY='1',PHARMACIE_RECON_RADIUS='0.42')
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),'route_bvh','exec'))
except SystemExit:pass
def test_point(p):
    p=Vector(p);support=ray(floorbvh,floornames,(p.x,p.y,p.z+.40),(0,0,-1),1)
    if not support:return {'failure':'floor','point':list(p)}
    z=support['point'][2]
    for height in (.45,1,1.65):
        for k in range(16):
            hit=ray(bvh,names,(p.x,p.y,z+height),(math.cos(k*math.tau/16),math.sin(k*math.tau/16),0),.42)
            if hit:return {'failure':'body','point':list(p),'hit':hit['object']}
    hit=ray(bvh,names,(p.x,p.y,z+.08),(0,0,1),1.95)
    if hit:return {'failure':'head','point':list(p),'hit':hit['object']}
    return None
def line_free(a,b):
    a,b=Vector(a),Vector(b);count=max(1,math.ceil((b-a).length/.10))
    return all(test_point(a.lerp(b,i/count)) is None for i in range(count+1))
start=(5.5,13,0);goal=(-2,14,0);cache={}
def valid(node):
    if node not in cache:
        x,y=node
        cache[node]=(-18<=x<=40 and 0<=y<=104 and test_point((x*.25,y*.25,0)) is None)
    return cache[node]
origin=(22,52);target=(-8,56);queue=[(0,origin)];cost={origin:0};parent={};closed=set()
while queue:
    _,node=heapq.heappop(queue)
    if node in closed:continue
    if node==target:break
    closed.add(node)
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)):
        nxt=(node[0]+dx,node[1]+dy)
        if not valid(nxt):continue
        if dx and dy and (not valid((node[0]+dx,node[1])) or not valid((node[0],node[1]+dy))):continue
        new=cost[node]+math.hypot(dx,dy)
        if new<cost.get(nxt,float('inf')):
            cost[nxt]=new;parent[nxt]=node
            heapq.heappush(queue,(new+math.dist(nxt,target),nxt))
assert target in cost,'Main room has no tested connection to rear corridor'
nodes=[target]
while nodes[-1]!=origin:nodes.append(parent[nodes[-1]])
points=[Vector((x*.25,y*.25,0)) for x,y in reversed(nodes)]
simple=[points[0]];i=0
while i<len(points)-1:
    j=len(points)-1
    while j>i+1 and not line_free(points[i],points[j]):j-=1
    assert line_free(points[i],points[j]),'Invalid path edge'
    simple.append(points[j]);i=j
loop=[(5.5,-1.5,0),(5.5,3,0),(5.5,13,0)]+[tuple(p) for p in simple[1:]]+[
    (-2,15.3,0),(-2.5,23.7,0),(-3,29.75,0),(-3,32.6,0),(-6.5,32.6,0),
    (-7,31.8,0),(-11.4,31.8,0),(-11.4,0,0),(-11.4,-1.5,0),(5.5,-1.5,0)]
stairs=[(-1.35,29.75,0),(5.7,29.75,2.667),(6.6,29.75,2.667),
        (6.6,29.0,2.934),(6.6,25.55,4.8),(6.6,24.85,4.8),
        (6.6,24.35,4.8),(7.7,24.35,4.8),(7.7,20,4.8),(4.5,18,4.8)]
lane=[(46.5,-14,0),(46.5,-28.8,0)]
sections=[dict(name='Pub and rear escape loop',duration=40,feet=loop),
          dict(name='Stairs and upstairs hall',duration=12,feet=stairs),
          dict(name='Enclosed service lane',duration=8,feet=lane)]
samples=[];failures=[]
for section in sections:
    count=0
    for a,b in zip(section['feet'],section['feet'][1:]):
        a,b=Vector(a),Vector(b);steps=max(1,math.ceil((b-a).length/.10))
        for i in range(steps+1):
            point=a.lerp(b,i/steps);fail=test_point(point);count+=1
            if fail:failures.append(dict(section=section['name'],**fail))
    samples.append(dict(section=section['name'],samples=count))
report=dict(sections=sections,connector=[list(p) for p in simple],samples=samples,failures=failures,
            source=bpy.data.filepath,radius_m=.42,spacing_m=.10,
            limitations='Visible mesh radial rays; not continuous capsule sweeps or BO3 nav. Cuts between the three continuous sections.')
(dest/'flythrough-route.json').write_text(json.dumps(report,indent=2))
assert not failures,failures[:10]
print('V33_CAMERA_ROUTES_PASS',samples,flush=True)
