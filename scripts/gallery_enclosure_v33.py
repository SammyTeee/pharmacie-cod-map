"""Make local review gallery, finished-video contact sheet and delivery evidence."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,subprocess,html
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v33';ffmpeg='C:/ffmpeg/ffmpeg.exe';ffprobe='C:/ffmpeg/ffprobe.exe'
before=json.loads((dest/'before-enclosure-survey.json').read_text());after=json.loads((dest/'after-enclosure-survey.json').read_text())
assert after['unexplained_open_rays']==0,after['unexplained_open_rays']
validation=json.loads((dest/'validation.json').read_text());assert not validation['failures']
route=json.loads((dest/'flythrough-route.json').read_text());assert not route['failures']
changes=json.loads((dest/'changes.json').read_text());parent=ROOT/changes['source'];checkpoint=ROOT/changes['output']
assert hashlib.sha256(parent.read_bytes()).hexdigest()==changes['source_sha256']
sources=json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']
for source in sources:assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
videos={}
for filename,expected in [('player-route-flythrough.webm',60),('before-inspection.webm',12)]:
    path=dest/filename
    probe=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_format','-show_streams','-of','json',str(path)]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert (video['width'],video['height'],video['r_frame_rate'])==(1280,720,'24/1')
    duration=float(probe['format']['duration']);assert abs(duration-expected)<.1,(filename,duration)
    # Decode every frame, so a valid header alone cannot hide a truncated clip.
    subprocess.run([ffmpeg,'-v','error','-i',str(path),'-f','null','-'],check=True)
    videos[filename]=dict(bytes=path.stat().st_size,duration_seconds=duration,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
views=json.loads((dest/'review-views.json').read_text());sections=[]
key=('03_back_stairs','10_lane_end','11_west_boundary','17_stair_seam','18_diagonal_ceiling','19_rear_ceiling')
for name,eye,target in views:
    columns=[]
    for phase,label in [('before','Before v32'),('after','After v33'),('highlight','New geometry highlighted')]:
        filename=name+'_'+phase+'.png'
        if phase=='highlight' and not (dest/filename).exists():continue
        with Image.open(dest/filename) as image:image.load();assert image.size==(1280,720)
        columns.append('<figure><figcaption>'+label+'</figcaption><a href="'+filename+'"><img loading="lazy" src="'+filename+'"></a></figure>')
    title=name.split('_',1)[1].replace('_',' ').title()
    sections.append((name not in key,'<section><h2>'+title+'</h2><div class="pair">'+''.join(columns)+'</div></section>'))
sections.sort(key=lambda x:x[0])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pharmacie v33 enclosure review</title><style>body{margin:0;background:#14191e;color:#edf0ed;font:16px system-ui}main{max-width:1450px;margin:auto;padding:26px}a{color:#dfb967}h1{margin-bottom:8px}p{max-width:1000px;line-height:1.6}.pair{display:flex;gap:12px;flex-wrap:wrap}figure{margin:0;flex:1;min-width:300px}img,video{width:100%;border-radius:5px}figcaption{padding:8px 0;color:#c7cec7}section{margin:30px 0}aside{background:#253128;padding:14px;border-left:4px solid #9dbb87}</style><main><h1>Pharmacie v33 — enclosure and service detail</h1><p>The pub and rear loop retain their layout. This pass closes the wall/floor seams around the stairs and rear ceiling, encloses the service lane sides, and finishes gates, signs and threshold details.</p>'''
page+='<aside>'+str(before['unexplained_open_rays'])+' unexplained open rays before → '+str(after['unexplained_open_rays'])+' after, across '+str(after['interior_ray_count'])+' sampled interior rays. The '+str(after['intentional_rear_exit_sky_rays'])+' remaining open rays pass through the intended rear doorway into the outdoor sky. These are Blender geometry checks; BO3 collision, pursuit and co-op remain untested.</aside>'
page+='''<h2>Player-height fly-through</h2><p>0–40s: street → pub → rear corridor → alley → street. 40–52s: stairs and upstairs hall. 52–60s: service lane. Three continuous sections with cuts between them. 720p, 12 distinct rendered frames per second, 24fps playback.</p><video controls preload="metadata" poster="01_pub_entrance_after.png"><source src="player-route-flythrough.webm" type="video/webm"></video><p><a href="player-route-flythrough.webm" download>Download fly-through</a> · <a href="video-contact.jpg">Video contact sheet</a></p><details><summary>12-second inspection of the earlier gaps</summary><video controls preload="none"><source src="before-inspection.webm" type="video/webm"></video></details>'''
page+=''.join(section for _,section in sections)
page+='''<h2>Review findings</h2><p>The main pub aisle, upstairs envelope and narrow rear alley still read coherently. The previous interstorey sky strip and diagonal ceiling escapes are covered by closed solids. The lane now ends in a walled maintenance pocket rather than isolated gate scenery. Outdoor sky above streets and open alleys remains intentional.</p><p>The wider junction and long Melton/bridge scenery still need further accurate road/terrain detail before expanding combat there. Taraj is retained as a separate future branch. Door purchases, barricades, spawning, zombie pursuit and four-player traversal require Radiant conversion and runtime tests.</p><p><a href="../../docs/ENCLOSURE_DETAIL_V33.md">Mapping notes and reproduction</a> · <a href="changes.json">Changes</a> · <a href="validation.json">Retained route checks</a> · <a href="flythrough-route.json">Connected camera route checks</a> · <a href="delivery-validation.json">Delivery verification</a></p></main></html>'''
(dest/'index.html').write_text(page,encoding='utf-8')
out=ROOT/'build/v33-video-contact';out.mkdir(exist_ok=True)
subprocess.run([ffmpeg,'-v','error','-y','-i',str(dest/'player-route-flythrough.webm'),'-vf','fps=1/4,scale=320:180','-frames:v','15',str(out/'%02d.png')],check=True)
sheet=Image.new('RGB',(1280,4*205),(20,24,28));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for i,path in enumerate(sorted(out.glob('*.png'))):
    x=i%4*320;y=i//4*205;sheet.paste(Image.open(path).convert('RGB'),(x,y));draw.text((x+5,y+181),str(i*4+2)+'s',font=font,fill='white')
sheet.save(dest/'video-contact.jpg')
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):self.links.extend(v for k,v in attrs if k in ('src','href','poster') and v)
parser=Links();parser.feed(page)
local=[link for link in parser.links if not link.startswith(('http:', 'https:', '#'))]
missing=[link for link in local if link!='delivery-validation.json' and not (dest/link).is_file()];assert not missing,missing
report=dict(checkpoint_sha256=hashlib.sha256(checkpoint.read_bytes()).hexdigest(),parent_checkpoint_hash_unchanged=True,
    original_reference_hashes_unchanged=len(sources),unexplained_open_rays_before=before['unexplained_open_rays'],
    unexplained_open_rays_after=after['unexplained_open_rays'],sampled_interior_rays=after['interior_ray_count'],
    retained_route_samples=validation['retained_samples'],street_route_samples=validation['street_samples'],
    connected_camera_route_samples=sum(section['samples'] for section in route['samples']),
    local_gallery_links=len(local),missing_links=missing,videos=videos,engine_verified=False,
    limits='Sparse visible-mesh rays and presentation media; not engine collision, AI pursuit, co-op or a watertightness certificate.')
(dest/'delivery-validation.json').write_text(json.dumps(report,indent=2))
print('V33_DELIVERY_CHECKS_PASS',len(local),videos)
