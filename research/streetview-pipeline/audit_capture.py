"""Check original hashes, dimensions and route-stop coverage without desktop inputs."""
from pathlib import Path
import json,hashlib
from PIL import Image
BASE=Path(__file__).resolve().parents[2]/'references/streetview-capture/taraj-to-pharmacie'
ROLES={'road-forward','right-forward-angle','right-frontage','right-rear-angle','road-backward','left-rear-angle','left-frontage','left-forward-angle','right-frontage-detail','left-frontage-detail','right-pavement-detail','left-pavement-detail'}
def audit():
    root=BASE.parents[2]
    records=[json.loads(line) for line in (BASE/'manifest.jsonl').read_text(encoding='utf8').splitlines() if line.strip()]
    state=json.loads((BASE/'walk-state.json').read_text())
    errors=[];warnings=[];ids=set();files=set();stops=[]
    for r in records:
        p=root/r['file']
        if r['id'] in ids or r['file'] in files:errors.append('Duplicate record '+r['id'])
        ids.add(r['id']);files.add(r['file'])
        if not p.exists():errors.append('Missing '+r['file']);continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:errors.append('Hash mismatch '+r['id'])
        with Image.open(p) as im:
            if im.width<1000 or im.height<600:errors.append('Small original '+r['id'])
    for stop in state['completed_stops']:
        images=[r for r in records if r['stop']==stop['stop']]
        roles={r['role'] for r in images}
        missing=sorted(ROLES-roles)
        if missing:errors.append(stop['stop']+' missing '+','.join(missing))
        if any(r['metadata'].get('panorama_id')!=stop['panorama_id'] for r in images):errors.append('Panorama mismatch '+stop['stop'])
        offsets={'road-forward':0,'right-forward-angle':45,'right-frontage':90,'right-rear-angle':135,'road-backward':180,'left-rear-angle':225,'left-frontage':270,'left-forward-angle':315,'right-frontage-detail':90,'left-frontage-detail':270,'right-pavement-detail':90,'left-pavement-detail':270}
        sweep_heading=stop['travel_heading']
        for r in images:
            if r['role']=='road-forward':sweep_heading=r['metadata']['heading_degrees']
            expected=(sweep_heading+offsets[r['role']])%360
            actual=r['metadata']['heading_degrees']
            if abs((actual-expected+180)%360-180)>12:warnings.append({'id':r['id'],'issue':'Intended role differs from reported URL heading; photograph needs review','expected_heading':expected,'reported_url_heading':actual})
        stops.append({'stop':stop['stop'],'images':len(images),'missing_roles':missing})
    result={'images':len(records),'completed_route_stops':len(stops),'route_status':state.get('status','in-progress'),'hashes_verified':True,'errors':errors,'warnings':warnings,'stop_coverage':stops}
    (BASE/'integrity-report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='stop_coverage'}))
    if errors:raise SystemExit(1)
if __name__=='__main__':audit()
