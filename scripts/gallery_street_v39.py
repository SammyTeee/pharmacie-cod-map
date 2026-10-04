from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v39'
views=json.loads((dest/'review-views.json').read_text());titles=['Designer Daisies flowers','Syston Jewellers trays and jewellery','Specsavers frames','Greggs bakery trays','Age UK clothing','Carpets and sample swatches'];cards=[];files=[]
sheet=Image.new('RGB',(1280,6*200),(20,25,29));draw=ImageDraw.Draw(sheet)
for row,((name,eye,target),title) in enumerate(zip(views,titles)):
 cards.append('<section><h2>'+title+'</h2><div>'+''.join('<figure><a href="'+name+'_'+phase+'.png"><img loading="lazy" src="'+name+'_'+phase+'.png"></a><figcaption>'+('Before — v38' if phase=='before' else 'After — v39')+'</figcaption></figure>' for phase in ('before','after'))+'</div></section>')
 for col,phase in enumerate(('before','after')):
  f=dest/(name+'_'+phase+'.png')
  with Image.open(f) as im:im.load();assert im.size==(1280,720);sheet.paste(im.resize((640,180)),(col*640,row*200+20))
  files.append(dict(name=f.name,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 draw.text((8,row*200+3),title+' — before / after',fill=(235,235,235))
sheet.save(dest/'contact-sheet.jpg',quality=90)
(dest/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Melton retail detail v39</title><style>body{background:#141c22;color:#edf1f3;font:16px/1.5 system-ui;max-width:1440px;margin:25px auto;padding:20px}a{color:#a9d6ff}section>div{display:grid;grid-template-columns:1fr 1fr;gap:14px}figure{margin:0}img{width:100%}section{margin:35px 0}@media(max-width:750px){section>div{grid-template-columns:1fr}}</style><h1>Melton Road — individual retail detail v39</h1><p>1,118 closed detail meshes across six businesses. Approved street footprint, entrances and earlier pub/Taraj/Town Square interiors retained. Generic display blocks are archived unchanged. Category-led original modelled stock; no source photo edits or established new shop interiors.</p><p>Road, pub/alley and 1,054 selected pavement/shelter/entry samples pass. Blender geometry checks only, not continuous collision or BO3 runtime tests.</p>'+''.join(cards)+'</html>',encoding='utf-8')
(dest/'media-validation.json').write_text(json.dumps(files,indent=2));print('V39_GALLERY_COMPLETE',len(files),flush=True)
