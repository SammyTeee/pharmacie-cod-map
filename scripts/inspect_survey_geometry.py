from pathlib import Path
import json,math,xml.etree.ElementTree as ET
from shapely.geometry import Point,Polygon,LineString
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'references/streetview-capture/authored-route-2026-10-11/route.json').read_text())
frame=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
ang=math.radians(frame['rotation_degrees']);c=math.cos(ang);s=math.sin(ang)
def local(lon,lat):return ((lon+1.0751002)*111320*math.cos(math.radians(52.6974696)),(lat-52.6974696)*111320)
def world(p):
 x=p[0]-frame['geo_seam_local_east_north'][0];y=p[1]-frame['geo_seam_local_east_north'][1]
 return [frame['blender_seam'][0]+frame['scale']*(c*x-s*y),frame['blender_seam'][1]+frame['scale']*(s*x+c*y)]
points=[local(w['position'][1],w['position'][0]) for w in r['waypoints']]
path=LineString(points)
tree=ET.parse(ROOT/'references/streetview-capture/extension-v41/osm-original.xml').getroot()
nodes={n.attrib['id']:local(float(n.attrib['lon']),float(n.attrib['lat'])) for n in tree.findall('node')}
items=[]
for w in tree.findall('way'):
 tags={t.attrib['k']:t.attrib['v'] for t in w.findall('tag')}
 if 'building' not in tags:continue
 poly=Polygon([nodes[n.attrib['ref']] for n in w.findall('nd')])
 if not poly.is_valid or poly.area<8 or poly.distance(path)>40:continue
 p=poly.centroid;chain=path.project(p);road=path.interpolate(chain);t=path.interpolate(min(chain+1,path.length));u=(t.x-road.x,t.y-road.y)
 side='left' if u[0]*(p.y-road.y)-u[1]*(p.x-road.x)>0 else 'right'
 items.append({'id':w.attrib['id'],'tags':tags,'chain_m':round(chain,1),'side':side,'setback_m':round(poly.distance(path),1),'area_m2':round(poly.area,1),'points':[world(p) for p in poly.exterior.coords]})
out={'origin_lonlat':[-1.0751002,52.6974696],'frame':frame,'route_world':[world(p) for p in points],'route_local':points,'route_length_m':path.length,'buildings':sorted(items,key=lambda x:x['chain_m'])}
dest=ROOT/'recon/v53';dest.mkdir(exist_ok=True)
(dest/'survey-geometry.json').write_text(json.dumps(out,indent=2))
print(json.dumps([{k:v for k,v in x.items() if k!='points'} for x in out['buildings']],indent=2))
