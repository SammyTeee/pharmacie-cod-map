"""Union road junctions and footways before extruding watertight surfaces."""
from pathlib import Path
import json
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely import constrained_delaunay_triangles, set_precision
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
paths=[(d['main'],4),(d['holmdale'],2.8),(d['station_access'][1:],2)]
# Unseen final link is explicitly a gameplay adaptation, separately recorded.
link=[d['station_access'][-1],[84.57706432073542,912.2934363105933]]
paths.append((link,1.4))
def buffers(extra):return unary_union([LineString(p).buffer(w+extra,cap_style='flat',join_style='mitre') for p,w in paths]+[Point(link[0]).buffer(2+extra,quad_segs=8)])
road=buffers(0);curb=buffers(.18).difference(road);pave=buffers(2.4).difference(buffers(.18))
footprints=set(json.loads((ROOT/'recon/v41/build-validation.json').read_text())['osm_building_footprints'])
grounds=[LineString(p).buffer(24,cap_style='flat',join_style='mitre') for p,w in paths[:-1]]
grounds += [LineString(link).buffer(6),Point(d['holmdale'][-1]).buffer(24)]
grounds += [Polygon(w['points']).buffer(2) for w in d['ways'] if w['id'] in footprints or w['tags'].get('railway')=='platform']
ground=unary_union(grounds)
wall=ground.boundary.buffer(.175,join_style='mitre')
# Leave the old-map seam open across its full terrain width.
a=d['main'][0];b=d['main'][1];length=((b[0]-a[0])**2+(b[1]-a[1])**2)**.5
u=((b[0]-a[0])/length,(b[1]-a[1])/length);n=(-u[1],u[0])
seamcut=Polygon([(a[0]+u[0]*t+n[0]*off,a[1]+u[1]*t+n[1]*off) for t,off in [(-.5,-24.5),(.3,-24.5),(.3,24.5),(-.5,24.5)]])
wall=wall.difference(seamcut)
def extrude(shape,z0,z1):
    shape=set_precision(shape,.00001)
    vs=[];fs=[];lookup={}
    def vi(x,y,z):
        k=(round(x,7),round(y,7),z)
        if k not in lookup:lookup[k]=len(vs);vs.append(k)
        return lookup[k]
    polys=list(shape.geoms) if shape.geom_type=='MultiPolygon' else [shape]
    for poly in polys:
        for triangle in constrained_delaunay_triangles(poly).geoms:
            pts=list(triangle.exterior.coords)[:-1]
            fs.append([vi(x,y,z1) for x,y in pts]);fs.append([vi(x,y,z0) for x,y in reversed(pts)])
        for ring in [poly.exterior,*poly.interiors]:
            coords=list(ring.coords)
            for a,b in zip(coords,coords[1:]):fs.append([vi(*a,z0),vi(*b,z0),vi(*b,z1),vi(*a,z1)])
    return {'vertices':vs,'faces':fs}
out={'road':extrude(road,-.30,-.08),'kerb':extrude(curb,-.17,.015),'footway':extrude(pave,-.25,0),'terrain':extrude(ground,-1.2,-.30),'boundary':extrude(wall,-.4,2.8),'station_final_link':link,'method':'Planar polygon unions/differences with constrained Delaunay triangulation; explicit estimated final station link and perimeter'}
(ROOT/'recon/v41/joined-surfaces.json').write_text(json.dumps(out))
print({k:(len(out[k]['vertices']),len(out[k]['faces'])) for k in ('road','kerb','footway')})
