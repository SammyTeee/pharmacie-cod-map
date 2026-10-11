"""Replace large concave bounding-box substitutes with top-surface prisms."""
from pathlib import Path
import ast,json,math,re,uuid
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles
from generate_blockout import parse_entity_blocks
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'scripts/generate_blender_test_map.py').read_text())
ns={'math':math,'uuid':uuid,'NS':uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704'),'UNIT':100/2.54,'SHIFT':(-3.5,-10,0)}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'helpers','exec'),ns)
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text())
materials=json.loads((ROOT/'assets/playtest-v58/manifest.json').read_text())['materials']
path=ROOT/'map_source/zm/zm_pharmacie_v58.map';text=path.read_text()
assert '// v58 repaired concave bounds' not in text
number=r'[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'
pattern=re.compile(r'(?ms)^// brush \d+\n\{.*?^\}\n?')
def world(v):
 p=ns['world'](v);return (p[0],p[1]-18000,p[2])
targets=[]
for o in data['objects']:
 vs=o['vertices_m'];lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)]
 if o['slab'] or len(o['faces'])<=32 or min(hi[i]-lo[i] for i in range(2))<=5:continue
 targets.append((o,world(lo),world(hi)))
records=[];pieces=[]
for o,lo,hi in targets:
 matches=[]
 for m in pattern.finditer(text):
  if '\n mesh\n' in m[0]:continue
  pts=[tuple(map(float,v)) for v in re.findall(r'\(\s*('+number+r')\s+('+number+r')\s+('+number+r')\s*\)',m[0])]
  # Legacy box writer used six significant digits before recentering.
  if pts and all(abs(min(v[i] for v in pts)-lo[i])<.2 and abs(max(v[i] for v in pts)-hi[i])<.2 for i in range(3)):matches.append(m)
 if not matches:
  records.append({'name':o['name'],'replaced_box':False,'reason':'No bounding substitute in final map'})
  continue
 assert len(matches)==1,(o['name'],len(matches))
 m=matches[0];text=text[:m.start()]+text[m.end():]
 count=0;vs=o['vertices_m'];bottom=min(v[2] for v in vs);top_height=max(v[2] for v in vs)
 caps=[]
 for tri in o['triangles']:
  top=[vs[i] for i in tri];normal=ns['cross'](ns['sub'](top[1],top[0]),ns['sub'](top[2],top[0]))
  length=ns['length'](normal)
  if length<.00001 or normal[2]/length<.5 or min(v[2] for v in top)-bottom<.004:continue
  caps.append(Polygon([(v[0],v[1]) for v in top]))
 # Dissolve redundant triangulation and approximate densely sampled curves
 # within 0.08 BU, retaining holes and connectivity. Never fill the bounds.
 footprint=unary_union(caps).simplify(.08,preserve_topology=True)
 assert footprint.is_valid
 polygons=list(constrained_delaunay_triangles(footprint).geoms)
 # Merge adjacent triangles when their union is convex. This avoids hundreds
 # of redundant internal collision planes in long road/boundary ribbons.
 for iteration in range(30):
  edges={};used=set();merged=[]
  for i,poly in enumerate(polygons):
   coords=list(poly.exterior.coords)
   for a,b in zip(coords,coords[1:]):
    edge=tuple(sorted((tuple(round(v,6) for v in a),tuple(round(v,6) for v in b))))
    edges.setdefault(edge,[]).append(i)
  for pair in edges.values():
   if len(pair)!=2 or any(i in used for i in pair):continue
   a,b=[polygons[i] for i in pair];hull=a.union(b).convex_hull
   if len(hull.exterior.coords)<=17 and abs(hull.area-a.area-b.area)<1e-5:
    used.update(pair);merged.append(hull)
  if not used:break
  polygons=[poly for i,poly in enumerate(polygons) if i not in used]+merged
 for polygon in polygons:
  top=[(x,y,top_height) for x,y in list(polygon.exterior.coords)[:-1]]
  prism=top+[(v[0],v[1],bottom) for v in top]
  n=len(top);faces=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
  brush=ns['convex_brush'](o['name']+f' true footprint {count}',[world(v) for v in prism],faces,materials[o['material']]['name'],850000+len(pieces))
  if brush:
   brush=re.sub(r'( guid "[^\n]+\n)',r'\1 contents detail;\n',brush,count=1)
   pieces.append(brush);count+=1
 assert count,(o['name'],'no upward surfaces')
 records.append({'name':o['name'],'replaced_box':True,'prisms':count,'curve_tolerance_BU':.08,'footprint_area_BU2':footprint.area})
a,b,ws=parse_entity_blocks(text)[0];ws=ws[:ws.rfind('}')]+'// v58 repaired concave bounds\n'+''.join(pieces)+'}\n';text=text[:a]+ws+text[b:]
path.write_text(text,newline='\n')
(ROOT/'docs/build-results/playtest-v58/concave-bounds-repair.json').write_text(json.dumps({'objects':records,'prisms':len(pieces),'runtime':'Retest required; no game input sent'},indent=2)+'\n')
print(json.dumps(records,indent=2))
