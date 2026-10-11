"""Geographic Holmdale endpoint and satellite-calibrated plot fit; no image edits."""
from pathlib import Path
import json,math
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles,set_precision
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v53'
survey=json.loads((dest/'survey-geometry.json').read_text());frame=survey['frame'];sc=frame['scale']
a=math.radians(frame['rotation_degrees']);c=math.cos(a);s=math.sin(a)
def geo(lon,lat):
 x=(lon+1.0751002)*111320*math.cos(math.radians(52.6974696))-frame['geo_seam_local_east_north'][0]
 y=(lat-52.6974696)*111320-frame['geo_seam_local_east_north'][1]
 return [frame['blender_seam'][0]+sc*(c*x-s*y),frame['blender_seam'][1]+sc*(s*x+c*y)]
old=json.loads((ROOT/'recon/v45/prepared-surfaces.json').read_text())
def top(key,z):
 d=old['surfaces'][key];vs=d['vertices'];polys=[]
 for f in d['faces']:
  if len(f)>=3 and all(abs(vs[i][2]-z)<1e-5 for i in f):polys.append(Polygon([vs[i][:2] for i in f]))
 return unary_union(polys)
route=survey['route_world'];holmdale=list(reversed(route[1:7]))
# Authored A is an observation point on the drive edge; node 1 is carriageway end.
line=LineString(holmdale);oldend=Point(frame['holmdale'][-1])
rebuild=oldend.buffer(8).union(LineString([frame['holmdale'][-1],route[1]]).buffer(9))
end=Point(route[1]);head=end.buffer(4.9*sc,quad_segs=2)
newroad=line.buffer(2.8,cap_style='flat',join_style='round').union(head)
road=top('road',-.08).difference(rebuild).union(newroad)
kerb=top('kerb',.015).difference(rebuild.buffer(2)).union(newroad.buffer(.18).difference(road))
foot=top('footway',0).difference(rebuild.buffer(2)).union(newroad.buffer(1.95).difference(road.buffer(.18)))
root_geo=[-1.078935,52.693454];house=geo(*root_geo)
# Preserve approved house dimensions; this is a rigid placement correction.
u=(-.9601240158,-.279573977);n=(.279573977,-.9601240158)
def hp(x,y):return [house[0]+x*u[0]+y*n[0],house[1]+x*u[1]+y*n[1]]
plot=Polygon([hp(x,y) for x,y in [(-2,-13.5),(26,-13.5),(26,24),(-2,24)]])
ground0=top('terrain',-.3);newground=line.buffer(23,cap_style='flat').union(plot.buffer(2)).union(newroad.buffer(5))
ground=ground0.union(newground)
boundary=top('boundary',2.8).difference(newground.buffer(.3))
boundary=boundary.union(newground.boundary.buffer(.175).difference(ground0.buffer(.3)))
# Avoid perimeter crossing the retained road at the new section seam.
boundary=boundary.difference(road.buffer(2.4)).difference(foot.buffer(.05))
def extrude(g,z0,z1):
 g=set_precision(g,.00001);vs=[];fs=[];lookup={}
 def vi(x,y,z):
  k=(round(x,7),round(y,7),z)
  if k not in lookup:lookup[k]=len(vs);vs.append(k)
  return lookup[k]
 for p in ([g] if g.geom_type=='Polygon' else g.geoms):
  if p.geom_type!='Polygon' or p.area<1e-6:continue
  for tri in constrained_delaunay_triangles(p).geoms:
   ps=list(tri.exterior.coords)[:-1];fs.append([vi(x,y,z1) for x,y in ps]);fs.append([vi(x,y,z0) for x,y in reversed(ps)])
  for ring in [p.exterior,*p.interiors]:
   for aa,bb in zip(list(ring.coords),list(ring.coords)[1:]):fs.append([vi(*aa,z0),vi(*bb,z0),vi(*bb,z1),vi(*aa,z1)])
 return {'vertices':vs,'faces':fs}
surfaces={key:extrude(g,z0,z1) for key,g,z0,z1 in [('road',road,-.3,-.08),('kerb',kerb,-.17,.015),('footway',foot,-.25,0),('terrain',ground,-1.7,-.3),('boundary',boundary,-1.8,2.8)]}
# Two consistency baselines in the same geographic frame, not independent surveys.
baselines=[]
for label,p,q in [('Holmdale last long straight',holmdale[-2],holmdale[-1]),('Melton Holmdale junction to Goodes Lane',route[6],route[12])]:
 bu=math.dist(p,q);baselines.append({'label':label,'blender_length_BU':bu,'geographic_length_m':bu/sc,'scale_BU_per_m':sc})
report={'surfaces':surfaces,'house_origin_world':house,'house_origin_lonlat':root_geo,
 'house_fit':'Approximate main left front corner traced at pixel (550,374) in overhead-number29-end-plot.jpg; viewport1320x876, centre52.6934,-1.07874, zoom20. Position tolerance about 1.5–2m; roof relief/perspective and pixel identification limit accuracy.',
 'holmdale_world':holmdale,'drive_observation_A':route[0], 'new_ground_polygon':list(newground.exterior.coords),
 'retire_zone':list(rebuild.buffer(2).exterior.coords),'baselines':baselines,
 'width_checks':[{'feature':'Holmdale straight carriageway','satellite_estimate_m':5.3,'tolerance_m':.6,'model_m':5.6/sc}, {'feature':'house left roof frontage','satellite_estimate_m':5.8,'tolerance_m':1.,'model_m':5.54/sc}],
 'limits':['1.064 BU/metre is retained compatibility scale; Blender METRIC unit display alone is not physical calibration.','Road centreline comes from OSM; overhead visually corroborates bends and end plot, not cadastral measurement.','Head outline, paving widths, building heights and concealed footprint remain estimates.','No source-image pixels embedded; BO3 unchanged.']}
(dest/'holmdale-alignment.json').write_text(json.dumps(report))
print(json.dumps({k:v for k,v in report.items() if k not in ('surfaces','new_ground_polygon','retire_zone')},indent=2))
