"""Prepare closed station/cul-de-sac surfaces from preserved mapped sources.

Widths/elevations and ramp are estimates; no Google overhead verification.
"""
from pathlib import Path
import json,math
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles,set_precision
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v45';dest.mkdir(exist_ok=True)
old=json.loads((ROOT/'recon/v41/joined-surfaces.json').read_text());route=json.loads((ROOT/'recon/v41/extension-route.json').read_text());ref=json.loads((ROOT/'recon/v43/station-reference.json').read_text())
def top(key,z):
 d=old[key];v=d['vertices'];return unary_union([Polygon([(v[i][0],v[i][1]) for i in f]) for f in d['faces'] if all(abs(v[i][2]-z)<1e-5 for i in f)])
platform=next(w['points'] for w in ref['mapped_ways'] if w['osm_way']=='309564449');a=platform[0];length=math.dist(a,platform[2]);u=[(platform[2][i]-a[i])/length for i in (0,1)];n=[-u[1],u[0]]
def world(x,y):return [a[i]+x*u[i]+y*n[i] for i in (0,1)]
def rect(x0,x1,y0,y1):return Polygon([world(x,y) for x,y in ((x0,y0),(x1,y0),(x1,y1),(x0,y1))])
clip=rect(-25,87,-25,40)
rails=[]
for w in ref['mapped_ways']:
 if w['tags'].get('railway')!='rail':continue
 g=LineString(w['points']).intersection(clip)
 if g.is_empty:continue
 for line in ([g] if g.geom_type=='LineString' else list(g.geoms)):
  if line.geom_type=='LineString' and line.length>1:rails.append({'osm_way':w['osm_way'],'points':list(map(list,line.coords)),'service':w['tags'].get('service')})
railshape=unary_union([LineString(r['points']).buffer(3.3,join_style='mitre') for r in rails])
parking=Polygon(next(w['points'] for w in ref['mapped_ways'] if w['osm_way']=='220522771'))
platformshape=Polygon(platform)
ramp=unary_union([rect(18.2,41.8,2.7,6.3),rect(18.2,21.8,4.5,9),rect(38.2,41.8,.3,6.3)])
railground=railshape.difference(platformshape.buffer(.2)).difference(parking.buffer(.2)).difference(ramp.buffer(.2))
end=route['holmdale'][-1];prev=route['holmdale'][-2];t=[(end[i]-prev[i])/math.dist(end,prev) for i in (0,1)];q=[-t[1],t[0]]
# Modest elliptical turning area: photograph proves widening, exact outline estimated.
head=Polygon([[end[i]+t[i]*(1+3.5*math.cos(j*math.tau/48))+q[i]*4.8*math.sin(j*math.tau/48) for i in (0,1)] for j in range(48)])
road=unary_union([top('road',-.08),head,parking]).difference(platformshape.buffer(.12)).difference(ramp)
kerb=road.buffer(.18,join_style='mitre').difference(road).difference(platformshape.buffer(.25)).difference(ramp.buffer(.4))
footway=unary_union([top('footway',0),head.buffer(2.0),parking.buffer(1.8)]).difference(road.buffer(.18)).difference(platformshape.buffer(.05)).difference(ramp)
ground=unary_union([top('terrain',-.30),parking.buffer(4),railshape.buffer(5),ramp.buffer(3),head.buffer(4)])
highground=ground.difference(railground)
wall=ground.boundary.buffer(.175,join_style='mitre')
# Retain the existing open seam to the approved old map.
b=route['main'][1];seam=route['main'][0];L=math.dist(seam,b);v=[(b[i]-seam[i])/L for i in (0,1)];nn=[-v[1],v[0]]
cut=Polygon([[seam[i]+v[i]*s+nn[i]*off for i in (0,1)] for s,off in ((-.5,-24.5),(.3,-24.5),(.3,24.5),(-.5,24.5))]);wall=wall.difference(cut)
stationzone=unary_union([parking,railshape,ramp,platformshape]).buffer(6)
brickwall=wall.difference(stationzone);stationwall=wall.intersection(stationzone)
def extrude(shape,z0,z1):
 shape=set_precision(shape,.00001);vs=[];fs=[];lookup={}
 def vi(x,y,z):
  k=(round(x,7),round(y,7),z)
  if k not in lookup:lookup[k]=len(vs);vs.append(list(k))
  return lookup[k]
 polys=[shape] if shape.geom_type=='Polygon' else [p for p in shape.geoms if p.geom_type=='Polygon']
 for p in polys:
  for tri in constrained_delaunay_triangles(p).geoms:
   pts=list(tri.exterior.coords)[:-1];fs.append([vi(x,y,z1) for x,y in pts]);fs.append([vi(x,y,z0) for x,y in reversed(pts)])
  for ring in [p.exterior,*p.interiors]:
   coords=list(ring.coords)
   for aa,bb in zip(coords,coords[1:]):fs.append([vi(*aa,z0),vi(*bb,z0),vi(*bb,z1),vi(*aa,z1)])
 return {'vertices':vs,'faces':fs}
surfaces={k:extrude(g,z0,z1) for k,g,z0,z1 in [('road',road,-.3,-.08),('kerb',kerb,-.17,.015),('footway',footway,-.25,0),('terrain',highground,-1.7,-.3),('rail terrain',railground,-1.7,-.97),('boundary',brickwall,-1.8,2.8),('station perimeter plinth',stationwall,-1.8,.40),('ramp',ramp,-.3,.03)]}
# Ramp falls from platform .03 to parking -.08 along the inferred parallel run.
for p in surfaces['ramp']['vertices']:
 if p[2]>.0:
  x=sum((p[i]-a[i])*u[i] for i in (0,1));p[2]=-.08+.11*min(1,max(0,(x-20)/20))
out={'surfaces':surfaces,'rail_paths':rails,'station_frame':{'origin':a,'u':u,'n':n},'parking_way':'220522771','platform_way':'309564449','extra_routes':{'station_parallel_ramp':[world(20,8),world(20,4.5),world(40,4.5),world(40,1.5)]},'head_estimate':{'center':end,'longitudinal_radius':3.5,'lateral_radius':4.8},'limits':['OSM geometry in provisional v41 frame; Google comparison pending.','Cul-de-sac width/outline inferred from September 2023 Street View.','Ramp position, widths, vertical levels and perimeter are gameplay estimates.','Railway switch profiles and operation are not simulated.']}
(dest/'prepared-surfaces.json').write_text(json.dumps(out))
fence=ground.boundary.intersection(stationzone)
out['station_fence_paths']=[list(map(list,g.coords)) for g in ([fence] if fence.geom_type=='LineString' else fence.geoms) if g.geom_type=='LineString']
(dest/'prepared-surfaces.json').write_text(json.dumps(out))
print(json.dumps({'surfaces':{k:[len(v['vertices']),len(v['faces'])] for k,v in surfaces.items()},'rail_paths':len(rails)},indent=2))
