"""Publish verified local Blender material renders into the existing review."""
from pathlib import Path
import json,html,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v57/materials'
report=json.loads((dest/'render-report.json').read_text());cards=[];files=[]
for item in report['images']:
 path=dest/item['file']
 with Image.open(path) as image:image.load();assert image.size==(1280,720)
 files.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 title=html.escape(item['title']);name=html.escape(item['file'])
 cards.append(f'<figure><a href="{name}"><img loading="lazy" src="{name}" alt="{title}, detailed Blender v57 material render"></a><figcaption>{title}</figcaption></figure>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Detailed Blender previews · v57</title><style>body{background:#151b1f;color:#eee;font:17px/1.6 system-ui;max-width:1440px;margin:32px auto;padding:20px}a{color:#a9d9ef}h1{font-size:36px}p{max-width:1000px}.gallery{display:grid;grid-template-columns:1fr 1fr;gap:26px}figure{margin:0}img{width:100%;border-radius:8px}figcaption{padding:8px 0}.notice{border-left:3px solid #d6bb83;padding-left:16px}@media(max-width:850px){.gallery{grid-template-columns:1fr}}</style><h1>Detailed Blender previews · v57</h1><p>11 October 2026 · Textured daylight views of the saved Blender model: your house, Holmdale Road and the connected street extension.</p><p class="notice">These show the detailed Blender source. The Radiant conversion has lost visual fidelity and is set aside. Architecture and dimensions retain the documented survey estimates; concealed building depths and the Barkby joining bend remain approximate. No model geometry was changed for these renders.</p><p><a href="../">Route notes and earlier matched views</a> · <a href="../../../assets/blender/pharmacie-surveyed-route-v57.blend">Editable Blender file</a></p><div class="gallery">'''+''.join(cards)+'</div></html>'
(dest/'index.html').write_text(page,encoding='utf-8');(dest/'media-validation.json').write_text(json.dumps(files,indent=2)+'\n')
p=ROOT/'recon/v57/index.html';text=p.read_text()
banner='<p id="textured-review"><a href="materials/">Latest textured daylight Blender previews →</a></p>'
if 'id="textured-review"' not in text:text=text.replace('<section>',banner+'<section>',1)
p.write_text(text,encoding='utf-8')
showcase=ROOT/'recon/showcase/index.html'
if showcase.exists():
 text=showcase.read_text(encoding='utf-8')
 section='<section id="latest-v57"><h2>Latest detailed Blender model · v57</h2><p>Your house and the surveyed street extension, with materials and daylight. Radiant testing is set aside.</p><p><a href="../v57/materials/">Open all latest Blender previews →</a></p><a href="../v57/materials/"><img style="width:100%;max-width:1280px" src="../v57/materials/house_front.jpg" alt="Latest detailed Blender house preview"></a></section>'
 if 'id="latest-v57"' not in text:text=text.replace('<section id="',section+'<section id="',1)
 showcase.write_text(text,encoding='utf-8')
print('MATERIAL_GALLERY_READY',len(files))
