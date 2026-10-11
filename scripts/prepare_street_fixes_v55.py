"""Cut evidenced route obstructions without altering archived source objects."""
from pathlib import Path
import json,ast
from shapely.geometry import Polygon,LineString,MultiPoint
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles,set_precision
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v55';dest.mkdir(exist_ok=True)
d=json.loads((ROOT/'recon/v54/prepared-street.json').read_text());v53=json.loads((ROOT/'recon/v53/holmdale-alignment.json').read_text());frame=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
me=d['surfaces']['boundary'];v=me['vertices'];wall=unary_union([Polygon([v[i][:2] for i in f]) for f in me['faces'] if all(abs(v[i][2]-2.8)<1e-5 for i in f)])
paths={'main':(frame['main'],6.5),'holmdale':(v53['holmdale_world'],5.3),'station_access':(frame['station_access'],4.7),'barkby':(d['barkby_world'],5.8)}
clear=unary_union([LineString(p).buffer(w) for p,w in paths.values()]);wall=wall.difference(clear)
obs=json.loads((ROOT/'recon/v54/join-obstructions.json').read_text());rem=[]
for ob in obs:
 poly=MultiPoint([p[:2] for p in ob['vertices']]).convex_hull;rem.append(poly.difference(LineString(d['barkby_world']).buffer(5.8)))
src=ast.parse((ROOT/'scripts/prepare_extension_v45.py').read_text());fn=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=='extrude');exec(compile(ast.Module(body=[fn],type_ignores=[]),'<extrude>','exec'))
surfaces={'clear perimeter':extrude(wall,-1.8,2.8),'old join infill remainder':extrude(unary_union(rem),-.5,3.2)}
report={'surfaces':surfaces,'retire':[o['name'] for o in obs],'limits':['Only static boundary infill is cut for a continuous street opening; original objects archived unchanged.','Barkby join retains its documented geographic deviation.']}
(dest/'prepared-fixes.json').write_text(json.dumps(report));print({'boundary_meshes':len(surfaces),'retire':report['retire']})
