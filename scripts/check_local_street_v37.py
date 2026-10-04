from pathlib import Path
import bpy,json,os,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v37'
os.environ.update(PHARMACIE_RECON_PHASE='after',PHARMACIE_RECON_OUTPUT=str(dest/'local-checks'),PHARMACIE_RECON_PROBES_ONLY='1',PHARMACIE_RECON_RADIUS='.42')
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),'retained_probes','exec'))
except SystemExit:pass
samples=[]
for route in json.loads((dest/'local-routes.json').read_text()):
 for a,b in zip(route['points'],route['points'][1:]):
  a,b=Vector(a),Vector(b);count=math.ceil((b-a).length/.10)
  for i in range(count+1):
   p=a.lerp(b,i/count);floor=ray(bvh,names,p+Vector((0,0,.4)),(0,0,-1),1);z=floor['point'][2] if floor else p.z;block=[]
   for h in (.45,1,1.65):
    for j in range(16):
     hit=ray(bvh,names,(p.x,p.y,z+h),(math.cos(j*math.tau/16),math.sin(j*math.tau/16),0),.42)
     if hit:block.append(hit['object'])
   head=ray(bvh,names,(p.x,p.y,z+.08),(0,0,1),1.95)
   samples.append(dict(route=route['name'],nominal=list(p),floor=floor,blockers=sorted(set(block)),overhead=head))
fails=[s for s in samples if not s['floor'] or s['blockers'] or s['overhead']]
(dest/'local-route-validation.json').write_text(json.dumps(dict(samples=len(samples),failures=fails,radius=.42,spacing=.1,limits='Selected frontage/shelter paths only; not all pavements or continuous sweeps or engine navigation.'),indent=2))
assert not fails,[(p['route'],p['nominal'],p['blockers'],p['overhead']) for p in fails][:12]
print('V37_LOCAL_ROUTES_PASS',len(samples),flush=True)
