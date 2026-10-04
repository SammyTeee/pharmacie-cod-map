from pathlib import Path
import json,math,os,bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v34'
os.environ.update(PHARMACIE_RECON_PHASE='after',PHARMACIE_RECON_OUTPUT=str(dest/'tour-checks'),PHARMACIE_RECON_PROBES_ONLY='1',PHARMACIE_RECON_RADIUS='.42')
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),'tour_bvh','exec'))
except SystemExit:pass
path=[Vector((*p,6)) for p in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']]
loop=[Vector(p)+Vector((0,0,1.65)) for p in json.loads((ROOT/'recon/v33/flythrough-route.json').read_text())['sections'][0]['feet'][:-1]]
def rounded(points,radius=.12):
 ps=[Vector(p) for p in points];out=[ps[0]]
 for i in range(1,len(ps)-1):
  a,b,c=ps[i-1:i+2];r=min(radius,(b-a).length*.15,(c-b).length*.15)
  entry=b+(a-b).normalized()*r;exit=b+(c-b).normalized()*r;out.append(entry)
  for k in range(1,9):
   t=k/8;out.append(entry*(1-t)**2+b*(2*t*(1-t))+exit*t*t)
 out.append(ps[-1]);return out
def resample(points,spacing=.08):
 lengths=[(b-a).length for a,b in zip(points,points[1:])];total=sum(lengths);out=[]
 for k in range(math.ceil(total/spacing)+1):
  d=total*k/math.ceil(total/spacing)
  for i,l in enumerate(lengths):
   if d<=l:out.append(points[i].lerp(points[i+1],d/l));break
   d-=l
  else:out.append(points[-1])
 return out
sections=[dict(name='High Street and Pharmacie',duration=8,points=[(42,-25,20),(35,-6.7,12),(15,-6.7,7),(5.5,-6.7,3),(5.5,-1.5,1.65)],fixed_target=(5.5,2,2.8)),dict(name='Inside the pub and out through the rear alley',duration=32,points=loop),dict(name='High Street shopfronts - Melton Road now open',duration=16,points=[loop[-1],(-11.4,-6.7,3.5),(25,-6.7,5),(50,-6.7,6),(42,-6.7,7),(-38,-6.7,6)],shops=True),dict(name='Melton Road - shops and brook bridge',duration=38,points=[Vector((-38,-6.7,6))]+path[:7]+[path[6].lerp(path[7],.40)]),dict(name='Taraj Palace - retained opposite-road placement',duration=8,points=[path[6].lerp(path[7],.4),path[6].lerp(path[7],.66)+Vector((0,0,-3)),path[6].lerp(path[7],.83)+Vector((0,0,1))],fixed_target=(-60.5,271.7,4))]
for section,duration in zip(sections,(4,22,8,22,4)):section['duration']=duration
failures=[];samples_total=0
for section in sections:
 points=resample(rounded(section.pop('points')));samples=[]
 for i,eye in enumerate(points):
  if 'fixed_target' in section:target=Vector(section['fixed_target'])
  elif section.get('shops'):
   forward=points[min(len(points)-1,i+18)]-points[max(0,i-5)]
   facing=max(-1,min(1,forward.x/.8));target=eye+Vector((forward.x*.2,-7*facing,-2))
  else:
   target=points[min(len(points)-1,i+12)]
   if i>=len(points)-12:target=eye+(points[-1]-points[-2]).normalized()
  if (target-eye).length<.001:target=eye+Vector((0,1,0))
  # Every camera centre is inspected for a 20cm six-axis sphere approximation.
  for direction in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
   hit=ray(bvh,names,eye,direction,.20)
   if hit:failures.append(dict(section=section['name'],eye=list(eye),hit=hit))
  samples.append(dict(eye=list(eye),target=list(target)))
 section['samples']=samples;samples_total+=len(samples)
report=dict(sections=sections,camera_samples=samples_total,failures=failures,resolution=[1280,720],distinct_fps=30,duration=sum(s['duration'] for s in sections),limits='Camera ray checks; aerial sections are not player routes. Continuous paths within sections, cuts between sections. Not BO3 footage.')
(dest/'tour-plan.json').write_text(json.dumps(report,separators=(',',':')))
assert not failures,failures[:8]
print('V34_TOUR_PLAN_PASS',samples_total,flush=True)
