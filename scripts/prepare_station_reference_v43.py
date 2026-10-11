"""Extract station-region mapped footprints/track paths in the provisional frame.

Does not modify a .blend. Reference dataset for the next station modelling pass.
"""
from pathlib import Path
import json,math,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'recon/v41/extension-route.json').read_text())
r=ET.parse(ROOT/'references/streetview-capture/extension-v41/osm-original.xml').getroot()
c=math.cos(math.radians(d['rotation_degrees']));s=math.sin(math.radians(d['rotation_degrees']))
def transform(lon,lat):
    e=(lon+1.0751002)*111320*math.cos(math.radians(52.6974696));n=(lat-52.6974696)*111320
    dx=e-d['geo_seam_local_east_north'][0];dy=n-d['geo_seam_local_east_north'][1]
    return [d['blender_seam'][0]+d['scale']*(c*dx-s*dy),d['blender_seam'][1]+d['scale']*(s*dx+c*dy)]
nodes={x.attrib['id']:transform(float(x.attrib['lon']),float(x.attrib['lat'])) for x in r.findall('node')}
tags=lambda x:{t.attrib['k']:t.attrib['v'] for t in x.findall('tag')}
pin=d['station_pin'];selected=[]
for w in r.findall('way'):
    t=tags(w);ids=[x.attrib['ref'] for x in w.findall('nd')];pts=[nodes[n] for n in ids]
    dist=min(math.dist(pin,p) for p in pts)
    if dist>150:continue
    if t.get('railway') in ('rail','platform') or t.get('highway') in ('footway','service','steps','path') or t.get('amenity')=='parking' or 'building' in t:
        selected.append({'osm_way':w.attrib['id'],'tags':t,'points':pts,'distance_to_station_node':dist,'closed':ids[0]==ids[-1]})
point_features=[]
for n in r.findall('node'):
    t=tags(n)
    if t and math.dist(pin,nodes[n.attrib['id']])<100:point_features.append({'osm_node':n.attrib['id'],'tags':t,'position':nodes[n.attrib['id']]})
out={'mapped_ways':selected,'mapped_nodes':point_features,'source_frame':'recon/v41/extension-route.json','limits':['OSM data only; Google top-down comparison pending.','Station node is not the platform footprint or entrance.','Official station schematic is not to scale.','Dated photographs show different years; do not claim all features are current.'],'visual_references':[{'file':'station-official-layout.jpg','source':'https://www.nationalrail.co.uk/stations/syston/','use':'Ramp parallel to platform, shelter, car park, Melton access; schematic only'},{'file':'station-geograph-8028555.jpg','source':'https://www.geograph.org.uk/photo/8028555','date':'2025-04-20','author':'David Howard','use':'Forecourt yellow grid, fence/gate, low brick planter boundary, plant containers, signs and lighting'},{'file':'station-geograph-3779706-view.jpg','source':'https://www.geograph.org.uk/photo/3779706','date':'2012-09-22','author':'Nigel Thompson','use':'Historical track/one-platform spatial context; current details unverified'}]}
dest=ROOT/'recon/v43';dest.mkdir(exist_ok=True);(dest/'station-reference.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'ways':len(selected),'nodes':len(point_features),'features':[(w['osm_way'],w['tags']) for w in selected if w['tags'].get('amenity')=='parking' or w['tags'].get('railway')=='platform']},indent=2))
