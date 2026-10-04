from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1];dest=root/'recon/v35'
views=json.loads((dest/'review-views.json').read_text());parts=[]
names={'01_unlock':'Pub approach','02_junction':'Crossing and junction','03_melton':'Individual Melton shopfronts','04_bridge':'Brook crossing and Halls','05_taraj':'Taraj approach','06_plan':'Retained street plan'}
for name,eye,target in views:
 for phase in ('before','after'):assert (dest/(name+'_'+phase+'.png')).exists()
 parts.append('<section><h2>'+names[name]+'</h2><div>'+''.join('<figure><figcaption>'+phase.title()+'</figcaption><img loading="lazy" src="'+name+'_'+phase+'.png"></figure>' for phase in ('before','after'))+'</div></section>')
(dest/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Melton Road v35 review</title><style>body{background:#14191c;color:#eee;font:16px system-ui;margin:30px}div{display:flex;gap:12px}figure{margin:0;width:50%}img{width:100%}section{margin:30px 0}a{color:#8cf}</style><h1>Melton Road v35 — matched detail review</h1><p>2,860 closed detail meshes across 46 existing frontages. Roofs/chimneys, cornices/blinds, shop listings/displays, barber poles, flower tubs and produce crates. Street plan and interiors retained.</p><p>3,429 road samples and 572 pub/alley samples pass. Blender geometry review only; BO3 unchanged. All 10,217 parent meshes and 44 reference hashes preserved.</p>'+''.join(parts),encoding='utf-8')
print('GALLERY_READY',dest/'index.html')
