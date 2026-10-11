"""Check authored spawn headroom against actual exported convex solid planes."""
from pathlib import Path
import json,re,math,subprocess
from generate_blockout import parse_entity_blocks,kv
ROOT=Path(__file__).resolve().parents[1]
num=r'[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'
triple=r'\(\s*('+num+r')\s+('+num+r')\s+('+num+r')\s*\)'
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def dot(a,b):return sum(a[i]*b[i] for i in range(3))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def audit(text):
 entities=parse_entity_blocks(text);solids=[]
 collision_text=entities[0][2]+'\n'+''.join(b for _,_,b in entities[1:] if kv(b,'classname')=='script_brushmodel')
 for match in re.finditer(r'(?ms)^// brush (\d+)\n\{.*?^\}\n?',collision_text):
  b=match[0]
  if '\n mesh\n' in b or 'nonColliding' in b or re.search(r'\)\s+sky\s',b):continue
  planes=[]
  for line in b.splitlines():
   points=re.findall(triple,line)
   if len(points)!=3:continue
   a,bb,c=[tuple(map(float,p)) for p in points];n=cross(sub(bb,a),sub(c,a));length=math.sqrt(dot(n,n))
   if length:planes.append((tuple(v/length for v in n),a))
  if len(planes)>=4:solids.append((int(match[1]),planes))
 def inside(p):return [index for index,planes in solids if all(dot(n,sub(p,a))>=-.01 for n,a in planes)]
 results=[]
 for _,_,b in entities:
  if kv(b,'classname') not in ('info_player_start','info_player_coop','info_player_deathmatch'):continue
  origin=tuple(map(float,kv(b,'origin').split()));body=[]
  for height in (2,32,64):
   for dx,dy in ((0,0),(-14,-14),(-14,14),(14,-14),(14,14)):
    p=(origin[0]+dx,origin[1]+dy,origin[2]+height);hits=inside(p)
    if hits:body.append({'offset':[dx,dy,height],'solid_brushes':hits})
  # Origin is just above the floor. Sample 8 engine units below it.
  support=inside((origin[0],origin[1],origin[2]-8))
  results.append({'classname':kv(b,'classname'),'origin':origin,'body_intersections':body,'support_brushes':support})
 return results
current=audit((ROOT/'map_source/zm/zm_pharmacie_v58.map').read_text())
old=audit(subprocess.check_output(['git','show','f4000d2:map_source/zm/zm_pharmacie_v58.map'],cwd=ROOT).decode())
assert current,'No player spawns checked'
result={'before':old,'after':current,'method':'Five lateral body positions at three heights against inward convex brush half-spaces; downward floor sample. Source geometry check, runtime retest required.'}
(ROOT/'docs/build-results/playtest-v58/spawn-solid-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'before_blocked':sum(bool(r['body_intersections']) for r in old),'after_blocked':sum(bool(r['body_intersections']) for r in current),'after_unsupported':sum(not r['support_brushes'] for r in current),'spawns':len(current)},indent=2))
assert all(not r['body_intersections'] and r['support_brushes'] for r in current)
