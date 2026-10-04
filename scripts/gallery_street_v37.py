from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v37'
names=[('01_shelter','Green bus shelter','Segmented smoke glazing, lower panels, visible frame joints, bolted feet, sloping roof panels/ribs, gutter, timber seat, divider arms, timetable and block paving.'),('02_cycles','Cycle parking','Two original bicycles with tyres, rims, spokes, frame tubes, saddles, grips, chains and pedals, beside steel stands.'),('03_deliveries','Shop delivery scene','Wheeled roll cage with rails, taped cartons and handling labels, plus a parcel handtruck.'),('04_planting','Fuller planter foliage','Varied leaf clusters and small flowers replace the previous cube foliage. Existing planters retained.')]
cards=[];files=[]
for name,title,desc in names:
 for phase in ('before','after'):
  f=dest/(name+'_'+phase+'.png')
  with Image.open(f) as im:im.load();assert im.size==(1280,720)
  files.append(dict(name=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size))
 cards.append('<section><h2>'+title+'</h2><p>'+desc+'</p><div class="pair"><figure><a href="'+name+'_before.png"><img src="'+name+'_before.png"></a><figcaption>Before · v36</figcaption></figure><figure><a href="'+name+'_after.png"><img src="'+name+'_after.png"></a><figcaption>After · v37</figcaption></figure></div></section>')
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Melton Road street scenes v37</title><style>body{background:#141c22;color:#edf1f3;font:16px/1.5 system-ui;max-width:1440px;margin:25px auto;padding:20px}a{color:#a9d6ff}.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px}section{margin:35px 0}@media(max-width:750px){.pair{grid-template-columns:1fr}}</style><h1>Melton Road — street scenes v37</h1><p>375 new closed meshes. Shelter refinement follows the existing placement and reference photo; cycle/delivery placements are inferred street dressing. Matched Blender previews, not game footage.</p><p>Retained road/pub routes and 224 selected local pavement/shelter samples pass. All 13,377 previous mesh geometries and 44 reference hashes preserved. Full pavement circulation and BO3 gameplay remain unverified.</p>'+''.join(cards)+'<section><h2>New shelter parts highlighted</h2><p>Gold marks the new detail; this temporary colour is not saved into the map.</p><img src="01_shelter_highlight.png"></section></html>'
(dest/'index.html').write_text(page,encoding='utf-8');(dest/'media-validation.json').write_text(json.dumps(files,indent=2));print('V37_GALLERY_COMPLETE',len(files))
