"""Dimensioned photo-led frontage schedule, preserving evidence uncertainty."""
from pathlib import Path
import json,math,ast
from shapely.geometry import Polygon,LineString,Point,MultiPoint
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles,set_precision
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v54';dest.mkdir(exist_ok=True)
d=json.loads((ROOT/'recon/v53/survey-geometry.json').read_text());sc=d['frame']['scale'];route=LineString(d['route_world'])
def frame(chain,side,offset):
 p=route.interpolate(chain*sc);a=route.interpolate(max(0,chain*sc-.5));b=route.interpolate(min(route.length,chain*sc+.5));L=a.distance(b);u=((b.x-a.x)/L,(b.y-a.y)/L);n=(-u[1]*side,u[0]*side);x=(n[1],-n[0])
 return {'origin':[p.x+n[0]*offset*sc,p.y+n[1]*offset*sc],'x':x,'y':n}
items=[]
def add(label,chain,side,width,depth,height,style='house',offset=8.7,roof='hip',paint='brick',sign=None,source=None):
 f=frame(chain,side,offset);p=f['origin'];x=f['x'];y=f['y'];w=width*sc;dep=depth*sc
 poly=[[p[j]+x[j]*xx+y[j]*yy for j in (0,1)] for xx,yy in ((-w/2,0),(w/2,0),(w/2,dep),(-w/2,dep))]
 items.append(dict(id=f'R{len(items)+1:03}',label=label,chain_m=chain,side='left' if side==1 else 'right',width_m=width,depth_m=depth,eaves_m=height,style=style,roof=roof,paint=paint,sign=sign,frame=f,polygon=poly,source_stops=source or [max(1,round(chain/12)+1)],dimension_status='Estimated from perspective proportions; location along captured route approx +/- 5–12 m; no laser or cadastral survey'))
# Fill the newly recovered end section; retained opposite placeholders stay intact.
for c in (25,45,65):add('Opposite Holmdale end plot',c,-1,9,8,2.7 if c==25 else 5.6,'house',11,'hip','cream' if c==25 else 'brick')
for i,c in enumerate((32,51,70,91,112,136)):
 add('Holmdale semi / detached frontage',c,1,10.3 if i%2 else 9.2,8,5.6,'bayhouse',10.7,'hip','cream' if i in (2,4) else 'brick')
# Junction shop row and green opposite; no invented terrace across the green.
add('Blue corner shop',185,-1,8.8,8.5,5.8,'shop',7.8,'gable','cream','',source=[16,17])
add('Lucille Hair Studio',196,-1,8,8.5,5.8,'shopbay',7.8,'gable','grey','LUCILLE HAIR STUDIO',[17,18])
for i,c in enumerate((222,239,257,276)):add('Melton hipped semi',c,-1,11.5,9,5.7,'bayhouse',10,'hip','cream' if i%2 else 'brick')
add('Church gable and hall',291,-1,16,22,5.3,'church',27,'gable','brick',None,[24,25,26])
add('Victorian detached bay house',310,1,11,10,6.1,'bayhouse',8.8,'gable','brick')
for c in (317,333):add('Victorian sash and bay terrace',c,-1,12,8.5,6,'bayhouse',8.5,'gable')
add('White corner frontage',335,1,8,9,5.9,'shop',7.4,'gable','cream')
add("Green's Off Licence",350,1,9.2,10,6.4,'shop',7.4,'frontgable','brick',"GREEN'S OFF LICENCE",[30,31,32])
for i,c in enumerate((361,369,378,386,394,402,410)):
 add('Individual retail terrace',c,1,7.8,9,6.1,'shopdormer' if i%3!=1 else 'shopbay',7.4,'gable','brick' if i%3 else 'cream',None,[31+min(i,4),33+min(i,4)])
add('Happy Garden corner',384,-1,8,8.5,5.9,'shopbay',7.5,'frontgable','brick','HAPPY GARDEN',[33,34])
add('Adjacent pale gabled shop',395,-1,8.5,9,5.9,'shop',7.5,'frontgable','cream')
for c in (410,429,448):add('Modern brick flats',c,-1,18,11,6.2,'flats',10,'gable','brick',None,[35,36,37,38])
add('Arched old brick commercial frontage',429,1,11,10,6.1,'hall',7.5,'gable')
add('Tree corner brick house',468,-1,12,10,5.9,'bayhouse',10.5,'hip')
add('L Harris low workshop',486,-1,14,13,3.5,'workshop',8.3,'gable','brick','L. HARRIS',[41,42,43])
add('Peaked dark small shop',501,-1,7.2,10,3.3,'shop',7.5,'frontgable','grey')
add('Dark cafe corner frontage',513,-1,14,11,6,'shop',7.5,'gable','cream',None,[42,43,44])
add('Brick hall with blue doors',500,1,15,15,6,'hall',9,'frontgable','brick',None,[42,43,44])
for i,c in enumerate((520,532,543)):add('Historic brick retail terrace',c,1,10.5,9,6.4,'shopbay' if i==0 else 'shop',7.4,'gable','brick')
add('Bay front corner with rails',540,-1,11.5,10,6.1,'bayhouse',9,'hip')
for i,c in enumerate((573,586,599,612,625)):
 add('Close brick terrace opposite supermarket',c,1,12,9,5.9,'bayhouse' if i%2 else 'house',7.7,'gable','cream' if i==3 else 'brick')
add('Aldi supermarket',593.6,-1,43,44,4.4,'supermarket',18,'shed','grey','ALDI',[48,49,50,51,52])
add('Brick hall and commercial return',649,1,17,12,6.6,'hall',9,'frontgable','brick')
add('Three storey corner retail',670,1,14,10,8.4,'shop',8,'gable','brick')
add('Low commercial strip',654,-1,26,16,3.7,'workshop',11.5,'shed','brick',None,[54,55,56])
# Preserve older approved town buildings. This short joining bend avoids their
# existing, approximate rear massing; the rest follows the geographic line.
barkby=[[-40,0],[-48,10],[-59,13],[-77,13],[-88,27],[-90.0222,42.5851],[-104.5491,48.4344],[-125.0322,55.9348],[-156.0312,64.9539]]
bp=LineString(barkby);actual=LineString(d['route_world'][-8:]);maxdev=max(Point(p).distance(actual)/sc for p in barkby)
# Export one normalized frame per additional Barkby frontage.
savedroute=route;route=bp
for i,c in enumerate((82,98,114,130)):
 for side in (-1,1):add('Barkby service wing' if i==0 and side==1 else 'Barkby brick frontage',c/sc,side,13 if i==0 else 12,8.5,3.2 if i==0 and side==1 else 5.8,'workshop' if i==0 and side==1 else 'house',9.5,'gable','brick',None,[83+i*2,84+i*2])
route=savedroute
old=json.loads((ROOT/'recon/v53/holmdale-alignment.json').read_text())
def top(key,z):
 me=old['surfaces'][key];v=me['vertices'];return unary_union([Polygon([v[i][:2] for i in f]) for f in me['faces'] if all(abs(v[i][2]-z)<1e-5 for i in f)])
oldground=top('terrain',-.3);oldboundary=top('boundary',2.8)
polys=[Polygon(i['polygon']) for i in items];newplots=unary_union([p.buffer(5) for p in polys]);broadground=bp.buffer(22,cap_style='flat').union(newplots)
terrain=oldground.union(broadground)
road=bp.buffer(3.5,cap_style='flat',join_style='round');kerb=road.buffer(.18).difference(road);foot=road.buffer(2.0).difference(road.buffer(.18))
boundary=oldboundary.difference(broadground.buffer(.3)).union(broadground.boundary.buffer(.175).difference(oldground.buffer(.3))).difference(road.buffer(2.3))
# Cut only the obsolete perimeter section crossed by the new road; retain all
# original object datablocks unchanged in an archive, with rebuilt remainder.
obs=json.loads((ROOT/'recon/v53/old-junction-obstacles.json').read_text());retire=[];rem=[]
for ob in obs:
 p=MultiPoint(ob['points']).convex_hull
 if 'Rear parcel boundary' in ob['name'] and p.intersects(road.buffer(2.2)):
  retire.append(ob['name']);rem.append(p.difference(road.buffer(2.2)))
assert retire, 'Expected existing perimeter opening at Barkby join'
remainder=unary_union(rem)
# Shared triangulated closed extrusion helper, taken from retained preparation.
src=ast.parse((ROOT/'scripts/prepare_extension_v45.py').read_text());fn=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=='extrude');exec(compile(ast.Module(body=[fn],type_ignores=[]),'<extrude>','exec'))
surfaces={k:extrude(g,a,b) for k,g,a,b in [('terrain',terrain,-1.7,-.3),('boundary',boundary,-1.8,2.8),('Barkby road',road,-.3,-.08),('Barkby kerb',kerb,-.17,.015),('Barkby footway',foot,-.25,0),('retained perimeter remainder',remainder,-.5,3.2)]}
report={'scale_BU_per_m':sc,'frontages':items,'surfaces':surfaces,'barkby_world':barkby,'barkby_geographic_world':list(actual.coords),'barkby_join_max_deviation_m':maxdev,'retire_boundaries':retire,'limits':['Photo-led scenery; frontage positions, heights and concealed depths estimated.','Barkby join is locally bent around approved v40 rear buildings; maximum offset from geographic centreline recorded, not presented as survey accuracy.','BU/metre compatibility scale retained; no global rescale.','BO3 unchanged.']}
(dest/'prepared-street.json').write_text(json.dumps(report))
print(json.dumps({'frontages':len(items),'retire_boundaries':retire,'barkby_join_max_deviation_m':maxdev,'meshes':{k:len(v['vertices']) for k,v in surfaces.items()}}))
