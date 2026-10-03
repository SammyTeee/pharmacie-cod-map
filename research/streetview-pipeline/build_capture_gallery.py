"""Local searchable screenshot gallery, coordinate CSV, contact sheets and label export."""
from pathlib import Path
import json,csv,html,hashlib,math,argparse
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'references/streetview-capture/taraj-to-pharmacie'
def build(verify=False):
    records=[json.loads(x) for x in (BASE/'manifest.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
    reviews=json.loads((BASE/'review.json').read_text()) if (BASE/'review.json').exists() else {}
    rows=[]
    for r in records:
        p=ROOT/r['file'];assert p.exists(),p
        if verify:assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
        m=r['metadata'];q=reviews.get(r['id'],{});r['review']=q
        r['latitude']=m.get('latitude',m.get('requested_latitude'));r['longitude']=m.get('longitude',m.get('requested_longitude'))
        r['heading']=m.get('heading_degrees',m.get('requested_heading_degrees'));r['pitch']=m.get('pitch_degrees',m.get('requested_pitch_degrees'));r['fov']=m.get('fov_degrees',m.get('requested_fov_degrees'))
        r['local_file']='originals/'+p.name
        rows.append({'id':r['id'],'file':r['local_file'],'stop':r['stop'],'role':r['role'],'latitude':r['latitude'],'longitude':r['longitude'],'heading':r['heading'],'pitch':r['pitch'],'fov':r['fov'],'panorama_id':m.get('panorama_id',m.get('requested_panorama_id')) if ',3a,' in m['url'] or 'map_action=pano' in m['url'] else '', 'window_title':r['window_title'],'capture_utc':r['captured_utc'],'capture_date_observed':q.get('observed_imagery_date',r.get('image_capture_date_observed')),'label':q.get('label',r['label']),'notes':q.get('notes',r['notes']),'url':m['url'],'sha256':r['sha256']})
    with (BASE/'catalogue.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    (BASE/'catalogue.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
    features=[]
    for row in rows:
        if row['latitude'] is not None and row['longitude'] is not None:
            features.append({'type':'Feature','geometry':{'type':'Point','coordinates':[row['longitude'],row['latitude']]},'properties':{k:row[k] for k in ('id','stop','role','heading','pitch','fov','label','file','panorama_id')}})
    state_path=BASE/'walk-state.json'
    state=json.loads(state_path.read_text()) if state_path.exists() else {}
    stops=state.get('completed_stops',[])
    if len(stops)>1:
        features.append({'type':'Feature','geometry':{'type':'LineString','coordinates':[[s['longitude'],s['latitude']] for s in stops]},'properties':{'label':'Observed camera route','position_semantics':'Camera viewpoints; not building survey or exact road centreline'}})
    (BASE/'camera-route.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2)+'\n',encoding='utf8')
    data=json.dumps(records,ensure_ascii=False).replace('<','\\u003c')
    page='''<!doctype html><meta charset="utf-8"><title>Street reference captures</title>
<style>body{margin:0;font:15px system-ui;background:#131c25;color:#e6edf4}header{position:sticky;top:0;background:#172431;padding:16px;z-index:2}h1{margin:0 0 10px;font-size:23px}input,select,button,textarea{background:#243648;color:#fff;border:1px solid #527086;border-radius:5px;padding:9px}input{width:33%}button{cursor:pointer}main{padding:15px;display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:15px}article{background:#20303d;border-radius:8px;overflow:hidden}img{width:100%;display:block}section{padding:12px}a{color:#b1d8ff}textarea{width:94%;margin-top:6px;resize:vertical}.meta{font:12px monospace;color:#becede;margin:8px 0}.tag{font-weight:bold;color:#9bcece}small{color:#bdcbd7}</style>
<header><h1>Taraj → bridge → roundabout → Pharmacie — screenshot catalogue</h1>
<input id="search" placeholder="Search shop, address, stop, label or notes"> <select id="roles"><option value="">All view types</option></select>
<button id="save">Export labels JSON</button> <span id="count"></span><br><small>Original Google Maps viewport screenshots, attribution retained. Coordinates are camera viewpoints, not measured building positions. Local personal collection.</small></header><main id="cards"></main>
<script>const records=DATA;const key='pharmacie-street-capture-labels-v1';let edits=Object.fromEntries(records.filter(r=>Object.keys(r.review||{}).length).map(r=>[r.id,r.review]));try{Object.assign(edits,JSON.parse(localStorage.getItem(key)||'{}'))}catch{}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const roles=document.querySelector('#roles');for(const r of [...new Set(records.map(r=>r.role))].sort()){const o=document.createElement('option');o.value=r;o.textContent=r;roles.append(o)}
function draw(){const q=document.querySelector('#search').value.toLowerCase();const selected=roles.value;const shown=records.filter(r=>(!selected||r.role===selected)&&JSON.stringify({...r,...edits[r.id]}).toLowerCase().includes(q));document.querySelector('#count').textContent=shown.length+' / '+records.length+' images';document.querySelector('#cards').innerHTML=shown.map(r=>{const e=edits[r.id]||r.review||{};return `<article><a href="${esc(r.local_file)}" target="_blank"><img loading="lazy" src="${esc(r.local_file)}" alt="${esc(r.label)}"></a><section><div class="tag">${esc(r.id)} · ${esc(r.stop)} · ${esc(r.role)}</div><div>${esc(r.window_title)}</div><div class="meta">${esc(r.latitude)}, ${esc(r.longitude)} · heading ${esc(r.heading)}° · pitch ${esc(r.pitch)}° · FOV ${esc(r.fov)}°</div><a href="${esc(r.metadata.url)}" target="_blank" rel="noopener">Open original Street View position</a><br><input style="width:94%;margin-top:8px" data-id="${esc(r.id)}" data-field="label" value="${esc(e.label||r.label)}"><textarea data-id="${esc(r.id)}" data-field="notes" placeholder="Building, windows, signs, pavements, bridge, bus stop, obstructions...">${esc(e.notes||'')}</textarea></section></article>`}).join('')}
document.querySelector('#search').oninput=draw;roles.onchange=draw;document.querySelector('#cards').oninput=e=>{const id=e.target.dataset.id,field=e.target.dataset.field;if(!id)return;edits[id]??={};edits[id][field]=e.target.value;try{localStorage.setItem(key,JSON.stringify(edits))}catch{}};
document.querySelector('#save').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(edits,null,2)],{type:'application/json'}));a.download='review.json';a.click();URL.revokeObjectURL(a.href)};draw();</script>'''.replace('DATA',data)
    (BASE/'index.html').write_text(page,encoding='utf8')
    contact=BASE/'contact-sheets';contact.mkdir(exist_ok=True)
    for start in range(0,len(records),24):
        subset=records[start:start+24];sheet=Image.new('RGB',(1440,math.ceil(len(subset)/4)*235),'#15212c');d=ImageDraw.Draw(sheet)
        for j,r in enumerate(subset):
            with Image.open(ROOT/r['file']) as im:
                im.thumbnail((352,180));x=(j%4)*360+4;y=(j//4)*235+4;sheet.paste(im,(x,y))
            d.text((x,y+184),r['id']+' '+r['stop']+' '+r['role'][:25],fill='white')
            d.text((x,y+201),r['window_title'].replace(' — Mozilla Firefox','')[:45],fill='#afc3d0')
            d.text((x,y+217),f"{r['latitude']} {r['longitude']} h={r['heading']}",fill='#afc3d0')
        sheet.save(contact/f'{start+1:05d}-{start+len(subset):05d}.jpg',quality=88)
    total=sum((ROOT/r['file']).stat().st_size for r in records)
    result={'images':len(records),'unique_panorama_ids':len({r['panorama_id'] for r in rows if r['panorama_id']}),'stops':len({r['stop'] for r in rows if r['stop']}),'completed_route_stops':len(stops),'route_status':state.get('status','in-progress'),'original_size_bytes':total,'hashes_verified':verify,'gallery':str(BASE/'index.html')}
    (BASE/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');a=p.parse_args();build(a.verify)
