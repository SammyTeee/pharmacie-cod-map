from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v28-zombies'
labels={'gap_bar_east':'Priority: unfinished opening beside the bar','gap_bar_outside':'Reverse view of the bar-side opening','gap_junction_ground':'Priority: incomplete junction ground','22_alley_rear':'Rear alley: exposed background around supported route','36_alley_connection':'Rear connector: surrounding terrain needs completion'}
cards=[]
for folder,title in [(dest,'Street, Taraj and targeted gap checks'),(dest/'pub','Pub, stairs, upstairs and rear escape loop')]:
    cards.append(f'<h2>{title}</h2>')
    for p in sorted(folder.glob('*.png')):
        rel=p.relative_to(dest).as_posix();label=labels.get(p.stem,p.stem.replace('_',' '))
        cards.append(f'<figure><figcaption>{html.escape(label)}</figcaption><a href="{html.escape(rel)}"><img loading="lazy" src="{html.escape(rel)}" alt="{html.escape(label)}"></a></figure>')
segments=json.loads((dest/'video-segments.json').read_text())['segments'] if (dest/'video-segments.json').exists() else []
buttons=' '.join(f'<button onclick="document.querySelector(\'video\').currentTime={s["start_seconds"]};document.querySelector(\'video\').play()">{html.escape(s["view"].replace("_"," "))}</button>' for s in segments)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pharmacie Zombies geometry review — v28</title>
<style>body{margin:0;background:#15191e;color:#eceff2;font:17px system-ui;line-height:1.5}main{max-width:1100px;margin:auto;padding:24px}h1{font-size:29px}p,li{max-width:950px}a{color:#a9d4ff}video,img{display:block;width:100%;height:auto;background:#222;border-radius:8px}video{max-height:75vh}figure{margin:28px 0}figcaption{font-size:20px;margin:8px 0}button{padding:8px;margin:4px;background:#293847;border:1px solid #667889;border-radius:5px;color:white}.note{background:#28313b;padding:18px;border-radius:8px}</style><main>
<h1>Pharmacie — Zombies geometry review</h1><p>26 new Blender previews plus a compact inspection fly-through. Saved v28 source; no BO3 deployment or runtime verification.</p>
<div class="note"><strong>Fix first</strong><ol><li>Right-hand doorway beside the bar looks into unfinished space: enclose its room or fit a solid scenery door.</li><li>Complete ground and pavement joins around the junction; one review location has no floor underneath.</li><li>Set a clear playable boundary before opening the long road/bridge extension.</li></ol><p>572 sampled pub route checks pass, but sparse Blender rays cannot certify every wall/floor or BO3 collision. Keep the pub–street–alley–rear-door escape loop and test zombie pursuit, stair bottlenecks and four-player revives.</p></div>
<h2>Compact fly-through</h2><p>26 seconds · 640×360 · solid-material inspection. Textured Cycles stills are below. Short camera moves with cuts; this is not a proved traversable route.</p><video controls preload="metadata" poster="pub/04_main_room_to_bar.png"><source src="flythrough.webm" type="video/webm"></video><p><a href="flythrough.webm" download>Download WebM</a> · <a href="../../docs/ZOMBIES_GEOMETRY_REVIEW_V28.md">Full findings and test limits</a></p>'''+buttons+''.join(cards)+'</main></html>'
(dest/'index.html').write_text(page,encoding='utf-8')
print('GALLERY_COMPLETE',len(list(dest.glob('*.png')))+len(list((dest/'pub').glob('*.png'))))
