"""Join and verify finished renders, then make review artifacts. Does not upload."""
from pathlib import Path
import json,subprocess,hashlib,html,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v34';ff='C:/ffmpeg/ffmpeg.exe';probe='C:/ffmpeg/ffprobe.exe'
plan=json.loads((dest/'tour-plan.json').read_text());assert not plan['failures']
output=dest/'preview.webm'
viewport=(dest/'viewport-tour.json').exists()
if viewport:
 meta=json.loads((dest/'viewport-tour.json').read_text());assert meta['status']=='complete';resolution=meta['resolution'];encoding='VP9 CRF18 / 6Mbit target';renderer=meta['render']
else:
 metas=[json.loads((dest/('tour-section-%02d.json'%i)).read_text()) for i in range(5)]
 for i,m in enumerate(metas):assert m['fps']==30 and m['resolution']==[1920,1080] and m['duration']==plan['sections'][i]['duration']
 concat=ROOT/'build/v34-tour-concat.txt';concat.write_text('\n'.join("file '"+(dest/('tour-section-%02d.webm'%i)).as_posix()+"'" for i in range(5)))
 subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(output)],check=True)
 resolution=[1920,1080];encoding='VP9 CRF18 / 10Mbit target';renderer='Cycles16'
subprocess.run([ff,'-hide_banner','-loglevel','error','-i',str(output),'-f','null','-'],check=True)
info=json.loads(subprocess.check_output([probe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(output)]))
stream=info['streams'][0];assert [stream['width'],stream['height']]==resolution and stream['avg_frame_rate']=='30/1'
assert int(stream['nb_read_frames'])==plan['duration']*30
duration=float(info['format']['duration']);assert abs(duration-plan['duration'])<.1
sheet=Image.new('RGB',(1280,4*200),(20,23,26));draw=ImageDraw.Draw(sheet)
for i,t in enumerate([round((plan['duration']-1)*i/15,2) for i in range(16)]):
 p=ROOT/'build'/('v34-video-contact-%02d.jpg'%i)
 subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(output),'-frames:v','1','-vf','scale=320:180',str(p)],check=True)
 with Image.open(p) as im:sheet.paste(im,(i%4*320,i//4*200))
 draw.text((i%4*320+8,i//4*200+183),str(t)+' seconds',fill='white')
sheet.save(dest/'video-contact.jpg',quality=94)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
validation=json.loads((dest/'validation.json').read_text());assert not validation['road_failures'] and not validation['retained_failures']
checkpoint=ROOT/'assets/blender/pharmacie-taraj-road-v34.blend'
stills=[]
for name,eye,target in json.loads((dest/'review-views.json').read_text()):
 for phase in ('before','after'):
  p=dest/(name+'_'+phase+'.png')
  with Image.open(p) as im:im.load();assert im.size==(1280,720)
  stills.append(p.name)
cards=''.join('<section><h2>'+html.escape(name.replace('_',' '))+'</h2><div class="pair"><figure><img src="'+name+'_before.png"><figcaption>Before</figcaption></figure><figure><img src="'+name+'_after.png"><figcaption>After</figcaption></figure></div></section>' for name,_,_ in json.loads((dest/'review-views.json').read_text()))
page='<!doctype html><meta charset="utf-8"><title>Pharmacie to Taraj — v34</title><style>body{background:#111820;color:#edf1f4;font:17px system-ui;max-width:1400px;margin:auto;padding:24px}a{color:#91cfff}video,img{width:100%}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}figcaption{padding:8px}section{margin:32px 0}</style><h1>Pharmacie to Taraj — v34</h1><p>West road closure opened; backed ground, connected frontages and bounded street. Blender preview, not BO3 gameplay.</p><video controls preload="metadata" src="preview.webm" poster="05_taraj_after.png"></video><p>'+str(resolution[1])+'p · 30 distinct rendered fps · '+str(plan['duration'])+' seconds · '+html.escape(encoding)+'. Fast textured viewport capture with studio shadows; simpler shading than Cycles. <a href="https://sammyt.wtf/preview.webm">Hosted video</a> · <a href="../../docs/TARAJ_ROAD_V34.md">Mapping and checks</a> · <a href="validation.json">Geometry evidence</a></p>'+cards
(dest/'index.html').write_text(page,encoding='utf-8')
for link in re.findall(r'(?:href|src|poster)="([^"]+)"',page):
 if not link.startswith('http'):assert (dest/link).exists(),link
facts=dict(video=output.name,sha256=sha(output),bytes=output.stat().st_size,duration_seconds=duration,resolution=resolution,distinct_rendered_frames=int(stream['nb_read_frames']),distinct_fps=30,average_bitrate_bits_per_second=round(output.stat().st_size*8/duration),encoding=encoding,renderer=renderer,full_decode=True,checkpoint_sha256=sha(checkpoint),matched_stills=stills,engine_verified=False,upload_verified=False)
(dest/'delivery-validation.json').write_text(json.dumps(facts,indent=2))
print(json.dumps(facts,indent=2))
