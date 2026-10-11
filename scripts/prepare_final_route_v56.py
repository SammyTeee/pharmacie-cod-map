"""Trace the asymmetric turning apron from saved north-up overhead evidence."""
from pathlib import Path
import json,math,ast
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles,set_precision
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v56';dest.mkdir(exist_ok=True)
d=json.loads((ROOT/'recon/v53/holmdale-alignment.json').read_text());fix=json.loads((ROOT/'recon/v55/prepared-fixes.json').read_text());frame=json.loads((ROOT/'recon/v41/extension-route.json').read_text());a=math.radians(frame['rotation_degrees']);c=math.cos(a);s=math.sin(a);sc=frame['scale']
def top(me,z):
 v=me['vertices'];return unary_union([Polygon([v[i][:2] for i in f]) for f in me['faces'] if all(abs(v[i][2]-z)<1e-5 for i in f)])
def pixel(px,py):
 # Mercator north-up zoom20, central map viewport after left-side chrome.
 mpp=156543.03392*math.cos(math.radians(52.6934))/2**20
 lon=-1.07874+(px-696)*mpp/(111320*math.cos(math.radians(52.6934)));lat=52.6934+(438-py)*mpp/111320
 x=(lon+1.0751002)*111320*math.cos(math.radians(52.6974696))-frame['geo_seam_local_east_north'][0];y=(lat-52.6974696)*111320-frame['geo_seam_local_east_north'][1]
 return [frame['blender_seam'][0]+sc*(c*x-s*y),frame['blender_seam'][1]+sc*(s*x+c*y)]
trace=[[435,488],[460,492],[483,481],[540,502],[561,517],[510,603],[488,626],[452,608],[438,579],[434,545],[415,519]]
head=Polygon([pixel(*p) for p in trace]);end=Point(d['holmdale_world'][-1]);zone=end.buffer(12)
road=top(d['surfaces']['road'],-.08).difference(zone).union(head).union(LineString(d['holmdale_world']).buffer(2.8,cap_style='flat').difference(end.buffer(2.5)))
kerb=top(d['surfaces']['kerb'],.015).difference(zone.buffer(2)).union(road.intersection(zone).buffer(.18).difference(road))
foot=top(d['surfaces']['footway'],0).difference(zone.buffer(2)).union(road.intersection(zone).buffer(1.95).difference(road.buffer(.18)))
wall=top(fix['surfaces']['clear perimeter'],2.8)
oldcentre=json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline'];seamline=LineString([oldcentre[-2],*frame['main']]);wall=wall.difference(seamline.buffer(6.5))
src=ast.parse((ROOT/'scripts/prepare_extension_v45.py').read_text());fn=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=='extrude');exec(compile(ast.Module(body=[fn],type_ignores=[]),'<extrude>','exec'))
surfaces={k:extrude(g,z0,z1) for k,g,z0,z1 in [('road',road,-.3,-.08),('kerb',kerb,-.17,.015),('footway',foot,-.25,0),('perimeter',wall,-1.8,2.8)]}
report={'surfaces':surfaces,'overhead_source':'references/streetview-capture/authored-route-2026-10-11/overhead-number29-end-plot.jpg','trace_pixels':trace,'trace_world':list(head.exterior.coords),'method':'Approximate north-up pixel tracing; zoom20 Mercator conversion using central viewport (696,438), map centre52.6934,-1.07874. Width tolerance about 0.6–1m; roof relief does not affect road trace.','limits':['Turning apron follows visible asymmetric outline; driveway/pavement seams and exact curb corners remain estimated.','No source pixels embedded in model.','Not a measured land survey; BO3 unchanged.']}
(dest/'prepared-final.json').write_text(json.dumps(report));print({'head_area_m2':head.area/sc**2,'head_bounds_BU':head.bounds})
