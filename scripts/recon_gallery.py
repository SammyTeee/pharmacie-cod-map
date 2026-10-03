"""Portable offline recon gallery; no dependencies or external network requests."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1]/'recon/v18'
views=json.loads((R/'after/view-probes.json').read_text())['views'];cards=[]
for v in views:
    name=v['view'];title=html.escape(name.replace('_',' '));rows=[]
    for phase in ('before','after'):
        src=f'{phase}/{name}.png';rows.append(f'<figure><a href="{src}"><img loading="lazy" src="{src}" alt="{phase}: {title}"></a><figcaption>{phase}</figcaption></figure>')
    cards.append(f'<article data-name="{title.lower()}"><h2>{title}</h2><div class="pair">'+''.join(rows)+'</div></article>')
content='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pharmacie player recon v18</title>
<style>body{margin:24px;background:#171b20;color:#eee;font:16px system-ui}header{max-width:1000px}a{color:#8ec8ff}input{padding:12px;background:#272e38;color:white;border:1px solid #677180;border-radius:6px;width:min(90%,500px)}article{margin:28px 0}h2{font-size:19px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}img{width:100%;height:auto;border-radius:5px}figcaption{padding:5px;color:#bac3cc}@media(max-width:700px){.pair{grid-template-columns:1fr}}</style>
<header><h1>Pharmacie player recon — v18</h1><p>36 locations, before and after. Player eye height 1.65m; inspection lighting. Geometry/ray checks are preliminary, not BO3 collision tests.</p><p><a href="README.md">Findings and limits</a> · <a href="validation.json">Validation</a> · <a href="../../docs/ZOMBIES_PROGRESSION_V18.md">Zombies progression proposal</a></p><p>After views 05, 10, 11, 16, 18 and 19 use corrected camera positions/directions. Some original cameras faced a wall or stood inside furniture; those shots are not evidence of a broken doorway.</p><label>Filter locations <input id="search" placeholder="stairs, alley, bar, upstairs…"></label></header>
'''+''.join(cards)+'''<script>document.getElementById('search').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.name.includes(q))})</script></html>'''
(R/'index.html').write_text(content,encoding='utf-8')
index=['# Screenshot index','', '36 before / 36 after. After cameras 05, 10, 11, 16, 18 and 19 are deliberately corrected; compare context, not identical pixels.','', '| Location | Before | After |','|---|---|---|']
for v in views:
    n=v['view'];index.append(f'| {n} | [image](before/{n}.png) | [image](after/{n}.png) |')
(R/'SCREENSHOTS.md').write_text('\n'.join(index)+'\n')
print('Offline gallery and screenshot index generated')
