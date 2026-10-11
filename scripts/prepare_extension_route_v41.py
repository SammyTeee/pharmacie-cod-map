"""Read OSM road topology; tie new route to v25 chainage and v40 seam.

OSM data: (c) OpenStreetMap contributors, ODbL; no imagery copied into model.
The rigid extension frame is an explicit gameplay adaptation, not a survey.
"""
from pathlib import Path
import json, math, heapq, hashlib
import xml.etree.ElementTree as ET
from audit_extension_frame_v41 import audit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'references/streetview-capture/extension-v41/osm-original.xml'
r = ET.parse(SOURCE).getroot()
nodes = {n.attrib['id']: (float(n.attrib['lon']), float(n.attrib['lat'])) for n in r.findall('node')}
tags = lambda x: {t.attrib['k']: t.attrib['v'] for t in x.findall('tag')}
ways = {w.attrib['id']: {'id':w.attrib['id'], 'nodes':[n.attrib['ref'] for n in w.findall('nd')], 'tags':tags(w)} for w in r.findall('way')}
origin = (-1.0751002,52.6974696)
def local(p): return ((p[0]-origin[0])*111320*math.cos(math.radians(origin[1])), (p[1]-origin[1])*111320)
xy = {n:local(p) for n,p in nodes.items()}
def closest(p, ids): return min(ids,key=lambda n:math.dist(xy[n],p))
graph={}
for w in ways.values():
    if 'highway' not in w['tags']:continue
    for a,b in zip(w['nodes'],w['nodes'][1:]):
        d=math.dist(xy[a],xy[b]); graph.setdefault(a,[]).append((b,d));graph.setdefault(b,[]).append((a,d))
def shortest(start,end):
    queue=[(0,start)];dist={start:0};prev={}
    while queue:
        d,n=heapq.heappop(queue)
        if d!=dist[n]:continue
        if n==end:break
        for k,length in graph[n]:
            nd=d+length
            if nd<dist.get(k,float('inf')):dist[k]=nd;prev[k]=n;heapq.heappush(queue,(nd,k))
    assert end in dist
    route=[end]
    while route[-1]!=start:route.append(prev[route[-1]])
    return list(reversed(route))
melton={n for w in ways.values() if w['tags'].get('name')=='Melton Road' and w['tags'].get('highway')=='tertiary' for n in w['nodes']}
holmdale={n for w in ways.values() if w['tags'].get('name')=='Holmdale Road' for n in w['nodes']}
start=closest((0,0),melton)
# Main road ends just south-west of Holmdale junction, before railway bridge.
end=closest(local((-1.0823,52.69355)),melton)
main=shortest(start,end)
house=local((-1.0800171,52.693457))
hend=closest(house,holmdale)
hroute=shortest(start,hend)
fork=next(i for i,n in enumerate(hroute) if n not in set(main))-1
branch=hroute[fork:]
reachable={start};todo=[start]
while todo:
    for n,_ in graph[todo.pop()]:
        if n not in reachable:reachable.add(n);todo.append(n)
station_access=shortest(main[-5],closest(xy['6415345154'],reachable))
audit_data=audit(); scale=audit_data['blender_units_per_capture_metre_estimate']
seam_distance=(audit_data['blender_centreline_length']-audit_data['taraj_chainage'])/scale
# Project capture anchor to the first Melton segment, rather than its nearest vertex.
raw=[xy[n] for n in main]
u0=tuple((raw[1][j]-raw[0][j])/math.dist(raw[0],raw[1]) for j in range(2))
t=max(0,min(math.dist(raw[0],raw[1]),sum(-raw[0][j]*u0[j] for j in range(2))))
raw[0]=tuple(raw[0][j]+t*u0[j] for j in range(2))
remaining=seam_distance
for i,(a,b) in enumerate(zip(raw,raw[1:])):
    length=math.dist(a,b)
    if remaining<=length:
        ug=tuple((b[j]-a[j])/length for j in range(2)); geo_seam=tuple(a[j]+remaining*ug[j] for j in range(2)); raw=[geo_seam]+raw[i+1:];break
    remaining-=length
else:raise ValueError('Seam beyond available road')
ub=audit_data['extension_seam']['tangent']; bs=audit_data['extension_seam']['position']
c=ug[0]*ub[0]+ug[1]*ub[1]; s=ug[0]*ub[1]-ug[1]*ub[0]
def transform(p):
    dx=p[0]-geo_seam[0];dy=p[1]-geo_seam[1]
    return [bs[0]+scale*(c*dx-s*dy),bs[1]+scale*(s*dx+c*dy)]
def pos(n):return transform(xy[n])
out={
 'source_url':'https://api.openstreetmap.org/api/0.6/map?bbox=-1.083,52.691,-1.071,52.700',
 'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'attribution':'© OpenStreetMap contributors; ODbL https://www.openstreetmap.org/copyright',
 'frame_method':'Start at nearest Melton node to route-001, project first capture onto first segment; advance (v22 length - v24 Taraj chainage) / v25 scale; rigidly rotate local OSM tangent onto retained Blender seam tangent. New geometry only.',
 'scale':scale,'rotation_degrees':math.degrees(math.atan2(s,c)),
 'geo_seam_local_east_north':geo_seam,'blender_seam':bs,
 'main': [transform(p) for p in raw], 'main_osm_node_ids':main,
 'holmdale':[pos(n) for n in branch], 'holmdale_osm_node_ids':branch,
 'station_access':[pos(n) for n in station_access], 'station_access_osm_node_ids':station_access,
 'house_pin':transform(house), 'house_pin_status':'User supplied location only; identity/footprint not visually verified',
 'station_pin':pos('6415345154'),'midland_pin':pos('30147285'),
 'ways':[{**w,'points':[pos(n) for n in w['nodes']]} for w in ways.values() if ('building' in w['tags'] or w['tags'].get('railway')=='platform' or w['tags'].get('amenity')=='parking' and w['tags'].get('name')=='Midland Railway')],
 'limits':['Local street positions are mapped data, not survey verification.','Width, height, enclosure and frame rotation are gameplay estimates.','House architecture requires visual reference; do not substitute another Holmdale listing.','No BO3 behavior implemented.']
}
dest=ROOT/'recon/v41/extension-route.json';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('rotation_degrees','main','holmdale','house_pin','station_pin','midland_pin')},indent=2))
