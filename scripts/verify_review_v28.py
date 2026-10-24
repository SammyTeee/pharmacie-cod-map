"""Check gallery resources and video metadata, make inspection contact sheets."""
from pathlib import Path
import json,subprocess,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v28-zombies'
stills=sorted(dest.glob('*.png'))+sorted((dest/'pub').glob('*.png'))
sheet=Image.new('RGB',(960,((len(stills)+2)//3)*205),(22,27,33));draw=ImageDraw.Draw(sheet)
for i,p in enumerate(stills):
    im=Image.open(p).convert('RGB');im.thumbnail((312,176));x=(i%3)*320;y=(i//3)*205;sheet.paste(im,(x,y));draw.text((x+3,y+179),p.stem[:40],fill='white')
sheet.save(dest/'stills-contact.jpg',quality=85)
probe=json.loads(subprocess.check_output(['C:/ffmpeg/ffprobe.exe','-v','error','-show_format','-show_streams','-of','json',str(dest/'flythrough.webm')]))
stream=next(s for s in probe['streams'] if s['codec_type']=='video')
assert abs(float(probe['format']['duration'])-26)<.1
assert (stream['width'],stream['height'])==(640,360)
assert stream['codec_name']=='vp9'
assert len(stills)==26
page=(dest/'index.html').read_text()
for rel in re.findall(r'(?:src|poster)="([^"]+)"',page):assert (dest/rel).exists(),rel
routes=json.loads((dest/'pub/route-probes.json').read_text())['samples']
result={'stills':len(stills),'video_duration_seconds':float(probe['format']['duration']),'video_bytes':(dest/'flythrough.webm').stat().st_size,'video_codec':stream['codec_name'],'size':[stream['width'],stream['height']],'route_samples':len(routes),'unsupported_route_samples':sum(s['floor_object'] is None for s in routes),'route_blocker_samples':sum(bool(s['blockers']) for s in routes),'low_overhead_samples':sum(s['overhead'] is not None for s in routes),'no_scene_save':True,'engine_verified':False}
(dest/'review-validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
