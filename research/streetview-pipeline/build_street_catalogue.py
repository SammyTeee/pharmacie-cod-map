"""Build small individual dossiers, photo labels and a numbered local route map.

Reviewed facts live in docs/street-catalogue/entries/<ID>.json. This script does
not recognise images or measure buildings; camera-offset markers are estimates.
"""
from pathlib import Path
import json,csv,math,html
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'references/streetview-capture/taraj-to-pharmacie'
OUT=ROOT/'docs/street-catalogue'
H=html.escape
SIDES={
1:('B001','B006 B007 B008'),2:('B001 B002','B008 B009 B010 B011'),3:('B002','B010 B011 B012 B013'),4:('B002 B003','B012 B013 B014'),5:('B003 B004','B013 B014'),6:('F003 F004 B034','F003 F005 B015'),7:('B034 B035 B036 B037 F006','B015 F003'),8:('B034 B035 B036 B037 F006','B015 B016'),9:('B034 B035 B036 B037 F006','B015 B016 B017'),10:('B034 B035 B036','B015 B016 B017 B018 B019'),11:('B038 B040','B018 B019 B020 B021 F016'),12:('B038 B039 B040 B051','B019 B020 B021'),13:('B041 B051 B039','B022 B023 B024'),14:('B041 B042 B051','B023 B024 B025 B026'),15:('B042 F009','B024 B025 B026 B027'),16:('B042 B043 F009','B026 B027'),17:('B043 B044','B027 F010'),18:('B044 B045','B027 B028 F010'),19:('B045 B046 F011','B028 B029'),20:('B046 B047','B029 B030 B031 F017'),21:('B047','B029 B030 B031 B032'),22:('B048 B049 F012 F013','B032 B033'),23:('B048 B049 F013','B033 B032 F012')}
SECTIONS=[(1,5,'S01','Taraj and southern terrace'),(6,10,'S02','Brook, bridge and corner shops'),(11,15,'S03','Main retail and crossing'),(16,21,'S04','Shopping centre to Bistro'),(22,23,'S05','Mini-roundabout and junction')]
DATES={'00001':'Aug 2024','00030':'Aug 2024','00075':'Apr 2019','00113':'Apr 2023','00126':'Apr 2016','00154':'Aug 2024','00157':'Apr 2026','00177':'Apr 2026','00222':'Apr 2026','00258':'Apr 2026','00270':'Apr 2026','00273':'Apr 2026','00285':'Apr 2026'}
NATIVE=set(DATES)|{'00008'}
def section(n):return next((code,name) for low,high,code,name in SECTIONS if low<=n<=high)
def write_csv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
def build():
    records=[json.loads(line) for line in (BASE/'manifest.jsonl').read_text(encoding='utf8').splitlines()]
    by_id={r['id']:r for r in records}
    state=json.loads((BASE/'walk-state.json').read_text())
    state['status']='stopped-by-user-coverage-sufficient'
    state['stop_reason']='Sam requested no further captures; 23 completed stops reach the mini-roundabout. New close High Street/pub views were not captured.'
    state['route']=json.loads((ROOT/'research/streetview-pipeline/routes/taraj-pharmacie.json').read_text())
    (BASE/'walk-state.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf8')
    entries=[json.loads(p.read_text(encoding='utf8')) for p in sorted((OUT/'entries').glob('*.json'))]
    names={e['id']:e['name'] for e in entries}
    observed={id:[] for id in by_id}
    for e in entries:
        for id in e['primary_photos']:
            assert id in by_id,(e['id'],id)
            observed[id].append(e['id'])
    reviews=json.loads((BASE/'review.json').read_text(encoding='utf8'))
    dates_by_pano={by_id[id]['metadata'].get('panorama_id'): (date,id) for id,date in DATES.items()}
    photo_rows=[];stop_records={}
    for r in records:
        n=int(r['stop'][-3:]) if r['stop'].startswith('route-') and r['stop']!='route-endpoint' else None
        code,area=section(n) if n else ('S00','Pilot and endpoint map')
        nearby=[]
        if n:
            right,left=SIDES[n]
            if r['role'].startswith('right-'):nearby=right.split()
            elif r['role'].startswith('left-'):nearby=left.split()
            else:nearby=list(dict.fromkeys((right+' '+left+' F001 F002').split()))
        else:nearby=['B050'] if r['id']=='00008' else ['B001','B002','B005','B006','B007','B008']
        known=observed[r['id']]
        label=f"{r['id']} | {area} | {r['role']}"
        if known:label+=' | '+', '.join(names[id] for id in known)
        note='Observed subjects: '+(', '.join(known) if known else 'route context; no individual identity asserted from this view')+'. Nearby candidates: '+', '.join(nearby)+'.'
        if r['role']=='road-forward' or r['role']=='road-backward':note+=' Wide road context: compare building order, roof silhouettes, kerb bends and traffic furniture across adjacent cameras.'
        elif 'detail' in r['role']:note+=' Detail candidate: use for frame/sign/plinth/threshold appearance; vehicles, reflections, people and UI are not architecture.'
        else:note+=' Oblique/context candidate: useful for returns, recess depth and adjacency; not an orthographic facade.'
        q=reviews.setdefault(r['id'],{})
        if 'catalogue_note' not in q:q['manual_notes']=q.get('notes','')
        q.update(label=label,catalogue_note=note,notes=(q.get('manual_notes','')+'\n'+note).strip(),observed_ids=known,nearby_candidate_ids=nearby,section=code,review_status='native-original-and-contact-sheet-reviewed' if r['id'] in NATIVE else 'contact-sheet-reviewed')
        pano=r['metadata'].get('panorama_id')
        if pano in dates_by_pano:
            date,source=dates_by_pano[pano];q['observed_imagery_date']=date;q['date_evidence_photo']=source
        else:q['observed_imagery_date']=None;q['date_evidence_photo']=None
        if r['id'] in ('00126','00128'):q['metadata_issue']='Reported URL heading conflicts with the photographed west/left row; heading excluded from building placement.'
        row={'photo_id':r['id'],'stop':r['stop'],'section':code,'role':r['role'],'observed_ids':' '.join(known),'nearby_candidate_ids':' '.join(nearby),'imagery_date':q['observed_imagery_date'] or 'unverified','review':q['review_status'],'label':label}
        photo_rows.append(row);stop_records.setdefault(r['stop'],[]).append(row)
    (BASE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    (OUT/'stops').mkdir(exist_ok=True)
    for stop,rows in stop_records.items():(OUT/'stops'/f'{stop}.json').write_text(json.dumps({'stop':stop,'photos':rows},indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    write_csv(OUT/'PHOTO_INDEX.csv',photo_rows)
    stops=state['completed_stops'];lat0=stops[0]['latitude'];lon0=stops[0]['longitude'];scale=111195.08
    def local(lat,lon):return ((lon-lon0)*scale*math.cos(math.radians(lat0)),(lat-lat0)*scale)
    route=[local(s['latitude'],s['longitude']) for s in stops]
    summaries=[];geo=[]
    for e in entries:
        i=int(e['anchor_stop'][-3:])-1;x,y=route[i]
        a=route[max(0,i-1)];b=route[min(len(route)-1,i+1)];dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);ux,uy=dx/length,dy/length
        along=e['along_offset_m_estimate'];x+=ux*along;y+=uy*along
        side=e['side']
        if side in ('east','west'):
            sign=1 if side=='east' else -1;x+=uy*12*sign;y-=ux*12*sign
        elif side=='north':y+=18
        if e['id']=='B050':x,y=local(52.6994153,-1.0733271)
        latitude=lat0+y/scale;longitude=lon0+x/(scale*math.cos(math.radians(lat0)))
        code,area=section(i+1)
        e.update(map_position={'latitude':round(latitude,7),'longitude':round(longitude,7),'east_m':round(x,2),'north_m':round(y,2),'method':'Estimated offset from photographed camera route; B050 uses Google place pin. Not measured building geometry.'},section=code)
        photos=[by_id[id] for id in e['primary_photos']]
        md=f"# {e['id']} — {e['name']}\n\n{e['kind']} · {side} side/context · {code}: {area}\n\n"
        md+='[Numbered map](../index.html) · [Small index](../INDEX.csv)\n\n'
        md+='## Observed appearance\n\n'+'\n'.join('- '+o for o in e['observations'])+'\n\n'
        md+='## Evidence and photo selection\n\n'+e['review_basis']+' Camera address labels are not shop addresses.\n\n'
        for r in photos:
            p=Path('../../../')/r['file'];q=reviews[r['id']]
            md+=f"- [{r['id']}]({p.as_posix()}) — {r['role']}; imagery {q['observed_imagery_date'] or 'date unverified'}; {q['review_status']}.\n"
        md+='\n## Reconstruction guidance\n\n'
        md+=('Build upper mass/roof, lower facade piers, sign, openings and recessed returns as separate parts. Use sharp independent lettering and display inserts rather than one full-room/photo texture. No interiors are established by this entry. ' if e['kind']=='building-frontage' else 'Build this as independent road/prop geometry alongside the relevant storefronts; photographed occluders and image overlays are not structure. ')
        md+=f"Terrace/context group: {e['terrace_group']}; adjacency does not establish ownership or shared interiors. Preserve existing pub scale until calibrated.\n\n"
        md+='## Position and unknowns\n\n'+e['placement_confidence']+f" Anchor {e['anchor_stop']}; approximate marker {latitude:.7f}, {longitude:.7f}. Never use the marker as a footprint/width.\n\n"+'\n'.join('- '+u for u in e['unknowns'])+'\n'
        (OUT/'entries'/f"{e['id']}.md").write_text(md,encoding='utf8')
        image_html=''.join(f'<figure><a href="../../../{H(r["file"])}"><img loading="lazy" src="../../../{H(r["file"])}" alt="Photo {r["id"]}"></a><figcaption>{r["id"]} · {H(r["role"])} · imagery {H(reviews[r["id"]]["observed_imagery_date"] or "unverified")}</figcaption></figure>' for r in photos)
        page=f'<!doctype html><meta charset="utf-8"><title>{H(e["id"]+" "+e["name"])}</title><style>body{{max-width:1100px;margin:30px auto;padding:15px;font:16px/1.55 system-ui;background:#15212b;color:#e5edf3}}a{{color:#a5d5ff}}li{{margin-bottom:8px}}figure{{margin:20px 0}}img{{width:100%;height:auto}}small,figcaption{{color:#b8cad5}}</style><a href="../index.html">← Numbered route map</a><h1>{H(e["id"])} · {H(e["name"])}</h1><small>{H(code+" · "+side+" · "+e["kind"])}</small><h2>Observed appearance</h2><ul>'+''.join('<li>'+H(o)+'</li>' for o in e['observations'])+'</ul><h2>Unknowns / position confidence</h2><p>'+H(e['placement_confidence'])+'</p><ul>'+''.join('<li>'+H(u)+'</li>' for u in e['unknowns'])+'</ul><p>Markers are approximate references, not measured footprints. Images may be from different years. No Blender changes applied.</p><p><a href="'+e['id']+'.md">Markdown notes for rebuilding</a></p><h2>Selected evidence</h2><p>'+H(e['review_basis'])+'</p>'+image_html
        (OUT/'entries'/f"{e['id']}.html").write_text(page,encoding='utf8')
        (OUT/'entries'/f"{e['id']}.json").write_text(json.dumps(e,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
        summary={'id':e['id'],'name':e['name'],'kind':e['kind'],'side':side,'section':code,'anchor_stop':e['anchor_stop'],'notes':f"entries/{e['id']}.md",'page':f"entries/{e['id']}.html",'map_position':e['map_position']}
        summaries.append(summary);geo.append({'type':'Feature','geometry':{'type':'Point','coordinates':[longitude,latitude]},'properties':{'id':e['id'],'name':e['name'],'confidence':'estimated reference marker','notes':summary['notes']}})
    (OUT/'index.json').write_text(json.dumps(summaries,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    write_csv(OUT/'INDEX.csv',[{k:s[k] for k in ('id','name','kind','side','section','anchor_stop','notes')} for s in summaries])
    (OUT/'reference-markers.geojson').write_text(json.dumps({'type':'FeatureCollection','features':geo},indent=2)+'\n',encoding='utf8')
    vx=min(x for x,y in route)-65;vy=-max(y for x,y in route)-55;vw=max(x for x,y in route)-vx+65;vh=-vy+60
    paths=' '.join(f'{x:.2f},{-y:.2f}' for x,y in route)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx} {vy} {vw} {vh}" role="img" aria-label="Numbered route reference map"><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="#14222d"/><polyline points="{paths}" fill="none" stroke="#405a6b" stroke-width="8"/><polyline points="{paths}" fill="none" stroke="#e3e9a3" stroke-width=".6" stroke-dasharray="2 2"/>'
    for j,(x,y) in enumerate(route):svg+=f'<circle cx="{x:.2f}" cy="{-y:.2f}" r="1" fill="#d7e8ef"><title>Camera stop {j+1:03d}</title></circle>'
    label_boxes=[]
    for s in summaries:
        p=s['map_position'];x=p['east_m'];y=-p['north_m'];colour='#ffca84' if s['id'].startswith('B') else '#9cdbca';side=s['side'];sign=-1 if side=='west' else 1;offset=9*sign
        anchor='end' if sign<0 else 'start';lx=x+offset;ly=y+1
        chosen=False
        for extra in (0,15,30):
            for dy in (0,-6,6,-12,12,-18,18,-24,24):
                tx=x+offset+extra*sign;ty=y+1+dy
                box=(tx-13 if sign<0 else tx,ty-4.5,tx if sign<0 else tx+13,ty+1.5)
                if not any(box[0]<b[2]+1 and box[2]>b[0]-1 and box[1]<b[3]+.5 and box[3]>b[1]-.5 for b in label_boxes):
                    lx,ly=tx,ty;label_boxes.append(box);chosen=True;break
            if chosen:break
        svg+=f'<a href="{s["page"]}" target="_blank" data-id="{s["id"]}"><line x1="{x}" y1="{y}" x2="{lx}" y2="{ly-1}" stroke="{colour}" stroke-width=".25" opacity=".65"/><circle cx="{x}" cy="{y}" r="1.6" fill="{colour}"/><text x="{lx}" y="{ly}" font-size="4.2" text-anchor="{anchor}" fill="{colour}">{s["id"]}</text><title>{H(s["id"]+" "+s["name"])} — estimated location</title></a>'
    svg+=f'<text x="{vx+8}" y="{vy+12}" fill="#fff" font-size="5">N ↑</text><text x="{vx+8}" y="{vy+20}" fill="#c5d3db" font-size="3.5">Numbered reference markers; positions estimated</text></svg>'
    (OUT/'numbered-map.svg').write_text(svg,encoding='utf8')
    payload=json.dumps(summaries,ensure_ascii=False).replace('<','\\u003c')
    page='''<!doctype html><meta charset="utf-8"><title>Numbered street reference map</title><style>body{margin:0;background:#14222d;color:#e4eef5;font:15px system-ui}header{padding:18px;background:#1b2e3b}h1{margin:0 0 12px;font-size:24px}a{color:#b4d8ff}input,select,button{padding:9px;background:#263e50;color:white;border:1px solid #567286;border-radius:5px}input{width:40%}.layout{display:grid;grid-template-columns:1fr 420px;gap:12px;padding:15px}#map{height:78vh;overflow:hidden;border:1px solid #456171}svg{width:100%;height:100%;touch-action:none}#list{max-height:78vh;overflow:auto}.card{display:block;padding:12px;border-bottom:1px solid #435361;text-decoration:none}.card small{display:block;color:#b6c8d4;margin-top:5px}.hidden{display:none}p{max-width:1000px} @media(max-width:850px){.layout{grid-template-columns:1fr}#list{max-height:40vh}}</style><header><h1>Taraj → brook → retail street → mini-roundabout</h1><input id="search" placeholder="Search ID, shop or section"><select id="kind"><option value="">Buildings + street features</option><option value="building-frontage">Buildings/shopfronts</option><option value="street-feature">Street features</option></select><button id="reset">Reset map</button><p><span id="count"></span> · Wheel to zoom, drag empty map to pan, click an ID to open its own photo/notes page. <a href="INDEX.csv">Small index CSV</a> · <a href="README.md">How to use</a> · <a href="../../references/streetview-capture/taraj-to-pharmacie/index.html">All captured photos</a></p><small>Camera route is observed. Building markers are approximate offsets, not surveyed footprints. Numbered units can share a terrace mass. Captures stop at the roundabout; existing pub notes are linked by B050.</small></header><div class="layout"><div id="map">SVG</div><aside id="list"></aside></div><script>const items=DATA;const svg=document.querySelector('svg');const initial=svg.getAttribute('viewBox').split(' ').map(Number);let vb=[...initial];function set(){svg.setAttribute('viewBox',vb.join(' '))}document.querySelector('#reset').onclick=()=>{vb=[...initial];set()};const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function draw(){const q=document.querySelector('#search').value.toLowerCase(),kind=document.querySelector('#kind').value;const shown=items.filter(i=>(!kind||i.kind===kind)&&JSON.stringify(i).toLowerCase().includes(q));const ids=new Set(shown.map(i=>i.id));document.querySelector('#count').textContent=shown.length+' / '+items.length+' entries';for(const a of svg.querySelectorAll('[data-id]'))a.classList.toggle('hidden',!ids.has(a.dataset.id));document.querySelector('#list').innerHTML=shown.map(i=>`<a class="card" href="${esc(i.page)}" target="_blank"><b>${esc(i.id)} · ${esc(i.name)}</b><small>${esc(i.section)} · ${esc(i.side)} · ${esc(i.kind)}</small></a>`).join('')}document.querySelector('#search').oninput=draw;document.querySelector('#kind').onchange=draw;svg.onwheel=e=>{e.preventDefault();const factor=e.deltaY>0?1.15:1/1.15;const nw=vb[2]*factor;if(nw<initial[2]*.12||nw>initial[2]*3)return;const r=svg.getBoundingClientRect(),u=(e.clientX-r.left)/r.width,v=(e.clientY-r.top)/r.height;vb=[vb[0]+vb[2]*u*(1-factor),vb[1]+vb[3]*v*(1-factor),nw,vb[3]*factor];set()};let drag=null;svg.onpointerdown=e=>{if(e.target.closest('a'))return;drag={x:e.clientX,y:e.clientY,v:[...vb]};svg.setPointerCapture(e.pointerId)};svg.onpointermove=e=>{if(!drag)return;const r=svg.getBoundingClientRect();vb=[drag.v[0]-(e.clientX-drag.x)*drag.v[2]/r.width,drag.v[1]-(e.clientY-drag.y)*drag.v[3]/r.height,drag.v[2],drag.v[3]];set()};svg.onpointerup=()=>drag=null;draw();</script>'''.replace('SVG',svg).replace('DATA',payload)
    (OUT/'index.html').write_text(page,encoding='utf8')
    report={'entries':len(entries),'building_frontage_entries':sum(e['kind']=='building-frontage' for e in entries),'street_features':sum(e['kind']=='street-feature' for e in entries),'photos_labelled':len(records),'completed_camera_stops':len(stops),'reviewed_all_contact_sheets':True,'native_originals_reviewed':sorted(NATIVE),'unresolved_heading_metadata':['00126','00128'],'coverage':'Taraj to mini-roundabout; close High Street/pub capture not completed and not claimed','positions':'Estimated offsets, not surveyed building footprints','originals_modified':False}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps(report))
if __name__=='__main__':build()
