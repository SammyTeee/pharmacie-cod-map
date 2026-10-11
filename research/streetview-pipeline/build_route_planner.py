"""Offline A/B road planner using the project's preserved OSM snapshot."""
from pathlib import Path
import json,xml.etree.ElementTree as ET,hashlib
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'references/streetview-capture/extension-v41/osm-original.xml'
def dataset(path):
 tree=ET.parse(path).getroot()
 nodes={n.attrib['id']:[float(n.attrib['lon']),float(n.attrib['lat'])] for n in tree.findall('node')}
 roads=[];buildings=[]
 for w in tree.findall('way'):
  tags={t.attrib['k']:t.attrib['v'] for t in w.findall('tag')};ids=[n.attrib['ref'] for n in w.findall('nd')]
  if not all(i in nodes for i in ids):continue
  if tags.get('highway') in ('tertiary','secondary','primary','residential','unclassified','living_street','service','tertiary_link','secondary_link'):
   roads.append({'ids':ids,'name':tags.get('name',tags.get('highway'))})
  elif 'building' in tags:buildings.append([nodes[i] for i in ids])
 used={i for road in roads for i in road['ids']}
 return {'nodes':{i:nodes[i] for i in used},'roads':roads,'buildings':buildings,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
if __name__=='__main__':
 data=dataset(SOURCE);template=Path(__file__).with_name('route-planner.html').read_text(encoding='utf8')
 out=ROOT/'recon/route-planner/index.html';out.parent.mkdir(exist_ok=True)
 out.write_text(template.replace('/*DATA*/{}',json.dumps(data)),encoding='utf8')
 print(json.dumps({'output':str(out),'nodes':len(data['nodes']),'roads':len(data['roads'])}))
