"""Place stock wall guns against inspected exported faces and local road zones."""
from pathlib import Path
import json, math, re, uuid
from generate_blockout import parse_entity_blocks,kv,volume_brush
ROOT=Path(__file__).resolve().parents[1]; NAME='zm_pharmacie_v58'; UNIT=100/2.54
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text())
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):
 l=math.sqrt(dot(a,a));return tuple(x/l for x in a)
def world(p):return ((p[0]-3.5)*UNIT,(p[1]-10)*UNIT,p[2]*UNIT)
def point(p):return ' '.join(f'{v:.5f}' for v in world(p))
def entity(props,brush=''):return '{\n'+''.join(f'"{k}" "{v}"\n' for k,v in props.items())+brush+'}\n'
geometry=[]
for o in data['objects']:
 vs=o['vertices_m'];lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)]
 geometry.append((o,lo,hi))
def ray(p,d,maximum,wall=False):
 best=None
 for o,lo,hi in geometry:
  if wall and not any(k in o['name'].lower() for k in ('shell','wall end','backing','solid mass','boundary','enclosing')):continue
  end=[p[i]+d[i]*maximum for i in range(3)]
  if any(max(p[i],end[i])<lo[i] or min(p[i],end[i])>hi[i] for i in range(3)):continue
  vs=o['vertices_m']
  for tri in o['triangles']:
   a,b,c=[vs[i] for i in tri];e1=sub(b,a);e2=sub(c,a);h=cross(d,e2);det=dot(e1,h)
   if abs(det)<1e-8:continue
   inv=1/det;s=sub(p,a);u=inv*dot(s,h)
   if u<0 or u>1:continue
   q=cross(s,e1);v=inv*dot(d,q)
   if v<0 or u+v>1:continue
   t=inv*dot(e2,q)
   if t<.001 or t>maximum or (best and t>=best[0]):continue
   n=norm(cross(e1,e2))
   if dot(n,d)>0:n=tuple(-x for x in n)
   best=(t,[p[i]+d[i]*t for i in range(3)],n,o['name'])
 return best
weapons=['pistol_burst','pistol_fullauto','smg_standard','smg_fastfire','smg_versatile','ar_standard','ar_cqb','ar_longburst','ar_marksman','shotgun_pump']
# Original four mounts remain; add a varied near-start selection first.
seeds=[((3.4,y,.03),(-1,0,0)) for y in (2,5,9,13,15,18,20,23,25)]
seeds += [((3.4,y,.03),(1,0,0)) for y in (2,5,9,12,15,18,20,23)]
seeds += [((3.4,y,4.83),d) for y in (3.5,9,15,20) for d in ((-1,0,0),(1,0,0))]
routes=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
routes['holmdale']=json.loads((ROOT/'recon/v53/holmdale-alignment.json').read_text())['holmdale_world']
routes['barkby']=json.loads((ROOT/'recon/v54/prepared-street.json').read_text())['barkby_world']
old=json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']
routes['town']=old
for key in ('town','main','holmdale','barkby'):
 pts=routes[key]
 for a,b in list(zip(pts,pts[1:]))[::3]:
  u=norm((b[0]-a[0],b[1]-a[1],0));n=(-u[1],u[0],0);p=((a[0]+b[0])/2,(a[1]+b[1])/2,.03)
  seeds.extend([(p,n),(p,tuple(-x for x in n))])
mounts=[]; additions=[]
for seed,d in seeds:
 hit=ray((seed[0],seed[1],seed[2]+1.4224),d,18,True)
 if not hit:continue
 _,p,n,wall=hit
 if abs(n[2])>.15:continue
 approach=(p[0]+n[0]*.95,p[1]+n[1]*.95,p[2])
 floor=ray((approach[0],approach[1],seed[2]+.65),(0,0,-1),1.1)
 if not floor:continue
 ground=floor[1][2]
 if abs(ground-seed[2])>.3:continue
 if ray(approach,tuple(-x for x in n),.75):continue
 if any(math.dist(p,m['face_hit'])<1.5 for m in mounts):continue
 if any(math.dist((p[0],p[1],ground+.02),v)<1.3 for v in ((-1.84,3.5,.02),(-4.53,26,.02),(-15,-.08,.02),(-2.71,14,4.82))):continue
 weapon=weapons[len(mounts)%len(weapons)]
 origin=(p[0]+n[0]*.055,p[1]+n[1]*.055,ground+.02)
 yaw=math.degrees(math.atan2(n[1],n[0]))+90
 prefab=f'_prefabs/zm/zm_core/spawnable_weapon_{weapon}.map'
 assert (Path('S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130/map_source')/prefab).is_file()
 additions.append(entity({'classname':'misc_prefab','model':prefab,'origin':point(origin),'angles':f'0 {yaw:.5f} 0'}))
 mounts.append({'weapon':weapon,'origin_BU':origin,'face_hit':p,'wall':wall,'normal':n,'approach':approach,'floor_object':floor[3],'cost':0,'ammo_cost':0})
path=ROOT/'map_source/zm'/f'{NAME}.map';text=path.read_text()
assert 'v58_route_' not in text, 'Regenerate clean map before augmentation'
# Small elevated decoration remains visible without creating bottle/leaf snags.
noncolliding=[]
ns=uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704')
decor_guids={}
for o,lo,hi in geometry:
 if max(hi[i]-lo[i] for i in range(3))<.75 and lo[2]>.35 and not o['image']:
  decor_guids[str(uuid.uuid5(ns,o['name']))]=o['name']
def decor_flag(match):
 name=decor_guids.get(match[1])
 if name:noncolliding.append(name);return match[0]+'\n contents nonColliding;'
 return match[0]
text=re.sub(r'guid "\{([a-f0-9-]+)\}"',decor_flag,text)
zones=[];risers=[];links=[]
# Small local volumes keep active spawn selection near the players as they explore.
for key in ('town','main','holmdale','station_access','barkby'):
 pts=routes[key];previous='street_zone' if key!='barkby' else 'crossing_zone'
 for si,(a,b) in enumerate(zip(pts,pts[1:])):
  length=math.dist(a,b);count=max(1,math.ceil(length/40))
  for j in range(count):
   aa=[a[k]+(b[k]-a[k])*j/count for k in range(2)];bb=[a[k]+(b[k]-a[k])*(j+1)/count for k in range(2)]
   zone=f'v58_route_{key}_{si}_{j}';pad=8 if key in ('town','main') else 5
   box=(min(aa[0],bb[0])-pad,max(aa[0],bb[0])+pad,min(aa[1],bb[1])-pad,max(aa[1],bb[1])+pad,-.45,4.3)
   low=world((box[0],box[2],box[4]));hi=world((box[1],box[3],box[5]));bound=(low[0],hi[0],low[1],hi[1],low[2],hi[2])
   additions.append(entity({'classname':'info_volume','targetname':zone,'target':zone+'_spawners','script_noteworthy':'player_volume'},volume_brush(0,bound,'\n')))
   zones.append({'name':zone,'bounds_BU':box});links.append((previous,zone));previous=zone
   for t in (.25,.75):
    p=(aa[0]+(bb[0]-aa[0])*t,aa[1]+(bb[1]-aa[1])*t,.03)
    floor=ray((p[0],p[1],.35),(0,0,-1),.7)
    if not floor:continue
    p=(p[0],p[1],floor[1][2]+.03)
    if any(ray((p[0],p[1],p[2]+z),d,.6) for z in (.5,1.5) for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0))):continue
    additions.append(entity({'classname':'script_struct','origin':point(p),'angles':'0 90 0','targetname':zone+'_spawners','script_noteworthy':'riser_location','script_string':'find_flesh'}))
    risers.append({'zone':zone,'position_BU':p,'floor_object':floor[3]})
path.write_text(text+'\n'.join(additions),newline='\n')
gsc=ROOT/'usermaps'/NAME/'scripts/zm'/f'{NAME}.gsc';script=gsc.read_text()
needle='level flag::set( "always_on" );'
script=script.replace(needle,needle+'\n'+''.join(f'\tzm_zonemgr::add_adjacent_zone( "{a}", "{b}", "always_on" );\n' for a,b in links))
gsc.write_text(script,newline='\n')
out=ROOT/'docs/build-results/playtest-v58';out.mkdir(parents=True,exist_ok=True)
(out/'placements.json').write_text(json.dumps({'wall_mounts':mounts,'route_zones':zones,'road_risers':risers,'noncolliding_small_decor':noncolliding,'limits':'Export-face and point-ray review only; prefab faces, purchases and nav pursuit require runtime checks. Overlapping axis-aligned route volumes are an initial exploration implementation.'},indent=2)+'\n')
assert len(set(m['weapon'] for m in mounts))>=9, 'Insufficient mounted variety'
print('Mounted',len(mounts),'weapons;',len(zones),'local road zones;',len(risers),'supported road risers')
