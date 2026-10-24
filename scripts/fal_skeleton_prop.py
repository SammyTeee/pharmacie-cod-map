"""One resumable fal image-to-3D attempt; never prints/stores credentials."""
from pathlib import Path
import os,json,hashlib,base64,sys,re,datetime
import requests
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/generated/skeleton-chair';OUT.mkdir(parents=True,exist_ok=True)
IMAGE=ROOT/'assets/photos/skeleton-cutout.png';ENDPOINT='fal-ai/trellis-2';JOB=OUT/'job.json'
def key():
    p=Path('C:/fal.txt');raw=p.read_text().strip() if p.exists() else os.environ.get('FAL_KEY','').strip()
    match=re.search(r'(?m)^\s*(?:export\s+)?FAL_KEY\s*=\s*(.+)$',raw)
    value=(match.group(1) if match else raw).strip().strip('\"\'')
    if not value or any(c.isspace() for c in value):raise RuntimeError('Credential file format unsupported; value not displayed')
    return value
headers={'Authorization':'Key '+key(),'Content-Type':'application/json'}
def call(method,url,**kwargs):
    response=requests.request(method,url,headers=headers,timeout=40,**kwargs)
    if response.status_code>=400:
        # Do not echo request bodies, headers or full server error contents.
        try:
            payload=response.json();detail=str(payload.get('detail',payload.get('error','')))
        except ValueError:detail=''
        detail=detail.replace(headers['Authorization'][4:],'[REDACTED]')
        detail=re.sub(r'fal_sk_[A-Za-z0-9_:]+','[REDACTED]',detail)
        print('FAL_HTTP_ERROR',response.status_code,detail[:180],flush=True);raise SystemExit(2)
    return response.json()
mode=sys.argv[1] if len(sys.argv)>1 else 'status'
if mode=='submit':
    if JOB.exists():print('JOB_ALREADY_EXISTS',json.loads(JOB.read_text())['request_id']);raise SystemExit(0)
    args={'image_url':'data:image/png;base64,'+base64.b64encode(IMAGE.read_bytes()).decode(),'resolution':'1024','texture_size':'2048','decimation_target':30000,'remesh':True,'seed':31004}
    job=call('POST','https://queue.fal.run/'+ENDPOINT,json=args);JOB.write_text(json.dumps(job,indent=2))
    manifest={'endpoint':ENDPOINT,'request_id':job['request_id'],'source':str(IMAGE.relative_to(ROOT)),'source_sha256':hashlib.sha256(IMAGE.read_bytes()).hexdigest(),'parameters':{k:v for k,v in args.items() if k!='image_url'},'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'listed_cost_usd':.30,'intent':'Static bare seated skeleton in black dentist chair; private photo-led Blender asset','references':'docs/PUB_PHOTO_RECONSTRUCTION.md L01; assets/photos/manifest.json','license_note':'Endpoint lists commercial use; original photo rights remain unresolved for distribution'}
    with (OUT/'fal_manifest.jsonl').open('a') as f:f.write(json.dumps(manifest)+'\n')
    print('FAL_SUBMITTED',job['request_id'],flush=True)
else:
    job=json.loads(JOB.read_text());state=call('GET',job['status_url']);(OUT/'status.json').write_text(json.dumps(state,indent=2));print('FAL_STATUS',state.get('status'),flush=True)
    if state.get('status')=='COMPLETED' and not (OUT/'skeleton-chair.glb').exists():
        result=call('GET',job['response_url']);(OUT/'result.json').write_text(json.dumps(result,indent=2))
        url=result['model_glb']['url'];r=requests.get(url,timeout=90);r.raise_for_status();(OUT/'skeleton-chair.glb').write_bytes(r.content)
        print('FAL_GLB_DOWNLOADED',len(r.content),flush=True)
