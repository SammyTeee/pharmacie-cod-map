from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil, subprocess, html, json, hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'recon/showcase'
OUT.mkdir(exist_ok=True)
(OUT/'media').mkdir(exist_ok=True)
shots=[('v39','01_B035_after.png','Designer Daisies','Individual flower displays'),('v39','02_B036_after.png','Syston Jewellers','Jewellery trays and necklaces'),('v39','03_B015_after.png','Specsavers','Spectacle frames and stands'),('v39','04_B024_after.png','Greggs','Bread trays and bakery detail'),('v39','05_B017_after.png','Age UK','Clothing displays and tags'),('v39','06_B002_after.png','Carpets & Beds','Carpet rolls and sample swatches'),('v38','01_town_square_after.png','Town Square','Red and gold recessed entrance'),('v38','02_passage_after.png','Town Square recess','Enclosed passage and warm lighting'),('v38','03_diy_display_after.png','Syston DIY','Individual paint tins'),('v38','04_card_display_after.png','Greeting cards','Layered card displays'),('v37','01_shelter_after.png','Melton Road shelter','Glazing, seating and timetable'),('v37','02_cycles_after.png','Cycle parking','Bicycles and steel stands'),('v37','03_deliveries_after.png','Delivery scene','Roll cage, cartons and handtruck'),('v37','04_planting_after.png','Street planting','Fuller foliage and flowers')]
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',24)
for i,(version,name,title,desc) in enumerate(shots):
    im=Image.open(ROOT/'recon'/version/name).convert('RGB')
    im.save(OUT/'media'/f'still-{i:02}.jpg',quality=92)
    im=im.resize((1280,720))
    d=ImageDraw.Draw(im);label=f'{title.upper()}  /  {version.upper()}'
    box=d.textbbox((0,0),label,font=font);w=box[2]+32
    d.rectangle((1280-w-24,24,1256,76),fill='#121a20')
    d.text((1280-w-8,37),label,font=font,fill='#ffffff')
    im.save(OUT/f'reel-{i:02}.jpg',quality=94)
concat=OUT/'reel.txt'
concat.write_text(''.join(f"file 'reel-{i:02}.jpg'\nduration 3\n" for i in range(len(shots)))+f"file 'reel-{len(shots)-1:02}.jpg'\n")
subprocess.run(['C:/ffmpeg/ffmpeg.exe','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30','-t','42','-c:v','libvpx-vp9','-crf','28','-b:v','0','-pix_fmt','yuv420p',str(OUT/'media/latest-details.webm')],check=True)
videos=[('Latest detail reel','V39 / V38 / V37','media/latest-details.webm','media/still-00.jpg','42 sec · labelled still reel','The newest retail displays, Town Square recess and Melton Road scenes.'),('Pharmacie to Taraj','V34 / FULL TOUR','/preview.webm','media/tour.jpg','60 sec · 720p / 30 fps','High Street, the pub interior, rear alley, Melton Road and Taraj.'),('Pub & rear service lane','V33 / PLAYER HEIGHT','media/pub-alley.webm','media/pub.jpg','Player-height fly-through','Pub interior and rear service lane.'),('Rear alley changes','V30 / BEFORE & AFTER','media/alley-changes.webm','media/alley.jpg','Before / after / highlights','Rear alley before and after.')]
for source,target in [('v34/05_taraj_after.png','tour.jpg'),('v33/after-flight-08.png','pub.jpg'),('v30/01_alley_after.png','alley.jpg')]:
    p=ROOT/'recon'/source
    if not p.exists():
        p=next((ROOT/'recon'/source.split('/')[0]).glob('*after*.png'))
    Image.open(p).convert('RGB').save(OUT/'media'/target,quality=90)
shutil.copy2(ROOT/'recon/v33/player-route-flythrough.webm',OUT/'media/pub-alley.webm')
shutil.copy2(ROOT/'recon/v30/mapping-changes.webm',OUT/'media/alley-changes.webm')
vc=''.join(f'<article class="video-card"><div class="frame"><video controls playsinline preload="none" poster="{poster}" src="{src}"></video><span class="label">{label}</span></div><div class="caption"><span class="meta">{meta}</span><h3>{title}</h3><p>{desc}</p></div></article>' for title,label,src,poster,meta,desc in videos)
sc=''.join(f'<figure><a class="frame" href="media/still-{i:02}.jpg" target="_blank" rel="noopener"><img loading="lazy" decoding="async" src="media/still-{i:02}.jpg" alt="{html.escape(desc)} at {html.escape(title)}"><span class="label">{html.escape(title)} / {version.upper()}</span></a><figcaption><h3>{html.escape(title)}</h3><p>{desc}</p></figcaption></figure>' for i,(version,name,title,desc) in enumerate(shots))
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="The Pharmacie Arms Zombies map: latest street and shop detail, video tours and labelled stills."><title>Pharmacie map previews</title><style>
:root{color-scheme:dark;--paper:#e9e8e2;--muted:#aeb6b3;--accent:#d5b97c}*{box-sizing:border-box}body{margin:0;background:#101716;color:var(--paper);font:16px/1.55 system-ui,sans-serif}header,main,footer{max-width:1500px;margin:auto;padding:28px 5vw}header{border-bottom:1px solid #34423d;display:flex;justify-content:space-between;align-items:center;gap:18px}.brand{font-weight:750;letter-spacing:.18em;font-size:13px}nav{display:flex;gap:24px}a{color:inherit;text-decoration:none}a:hover{color:var(--accent)}a:focus-visible,video:focus-visible{outline:3px solid var(--accent);outline-offset:4px}.intro{padding:26px 0 28px;max-width:850px}.eyebrow,.meta{color:var(--accent);font-size:12px;letter-spacing:.12em;text-transform:uppercase}h1{font:normal clamp(38px,5vw,68px)/1.08 Georgia,serif;margin:14px 0 18px}h2{font:normal 32px Georgia,serif;margin:0}h3{font-size:19px;line-height:1.3;margin:8px 0}p{color:var(--muted);margin:8px 0}.section-head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin:16px 0 22px}.videos,.stills{display:grid;grid-template-columns:1fr 1fr;gap:24px}.frame{position:relative;display:block;background:#080c0b;overflow:hidden}.frame video,.frame img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}.label{position:absolute;right:14px;top:14px;max-width:calc(100% - 28px);padding:7px 11px;background:#111a20e8;color:#fff;font-size:11px;font-weight:650;letter-spacing:.08em;text-transform:uppercase;pointer-events:none;border:1px solid #ffffff25}.caption,figcaption{padding:17px 0 10px}figure{margin:0}.stills{grid-template-columns:repeat(3,1fr)}section{scroll-margin-top:24px;margin-bottom:60px}.notice{font-size:13px;border-left:2px solid var(--accent);padding:10px 18px;margin:18px 0 0}footer{border-top:1px solid #34423d;font-size:13px;color:var(--muted);padding-bottom:36px}@media(max-width:900px){.stills{grid-template-columns:1fr 1fr}}@media(max-width:600px){header,main,footer{padding-left:20px;padding-right:20px}header{align-items:flex-start;flex-direction:column}.videos,.stills{grid-template-columns:1fr}.section-head{display:block}.label{font-size:10px;right:10px;top:10px}h1{font-size:44px}}
</style></head><body><header><a class="brand" href="#">THE PHARMACIE / SYSTON</a><nav aria-label="Page sections"><a href="#films">Video previews</a><a href="#stills">Latest stills</a></nav></header><main><div class="intro"><div class="eyebrow">04 October 2026 · v39</div><h1>Pharmacie map previews</h1><p class="notice">Work in progress · Blender previews. The latest v39 detail appears in the still reel and gallery; the full moving tour shows v34. These previews do not show verified BO3 gameplay.</p></div><section id="films"><div class="section-head"><h2>Video previews</h2><p></p></div>'''+vc+'''</section><section id="stills"><div class="section-head"><h2>Latest screenshots</h2><p>V39–V37 · Select a still to view it full size.</p></div><div class="stills">'''+sc+'''</div></section></main><footer>The Pharmacie Arms · Syston, Leicestershire · Custom Zombies map project<br>Modelled details and unseen spaces include creative gameplay adaptations. More architecture, interiors and engine testing remain.</footer><script>const films=[...document.querySelectorAll('video')];films.forEach(v=>v.addEventListener('play',()=>films.forEach(other=>{if(other!==v)other.pause()})));</script></body></html>'''
# Wrap video cards in their responsive grid.
page=page.replace(vc,'<div class="videos">'+vc+'</div>')
from add_aerial_showcase import add_aerial
page=add_aerial(page)
(OUT/'index.html').write_text(page,encoding='utf-8')
manifest={str(p.relative_to(OUT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'index.html',*(OUT/'media').iterdir()]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('SHOWCASE_READY',len(manifest),'files')
