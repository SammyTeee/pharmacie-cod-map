"""Extract timestamped video frames and authentic reference contact sheets."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import hashlib
import subprocess
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
ID='q0zBpicUXjg'
VIDEO=ROOT/'build/video-reference'/f'{ID}.mp4'
OUT=ROOT/'assets/video-references'/ID
FFMPEG=Path('C:/ffmpeg/ffmpeg.exe')
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'stills').mkdir(exist_ok=True)
info=json.loads((ROOT/'build/pharmacie-video-info.json').read_text(encoding='utf-8-sig'))
times=list(range(0,int(info['duration']),10))

def extract(second):
    path=OUT/'stills'/f'{second//60:02}-{second%60:02}.jpg'
    if not path.exists():
        subprocess.run([str(FFMPEG),'-hide_banner','-loglevel','error','-y','-ss',str(second),'-i',str(VIDEO),
                        '-frames:v','1','-q:v','2',str(path)],check=True,capture_output=True)
    with Image.open(path) as img:dimensions=list(img.size)
    return {'seconds':second,'time':f'{second//60:02}:{second%60:02}',
            'file':str(path.relative_to(ROOT)).replace('\\','/'),'dimensions':dimensions}

with ThreadPoolExecutor(max_workers=4) as pool:frames=list(pool.map(extract,times))
sheets=[]
for start in range(0,len(frames),24):
    entries=frames[start:start+24]
    canvas=Image.new('RGB',(1280,6*205+48),'#181b20');draw=ImageDraw.Draw(canvas)
    draw.text((12,10),f'{info["title"]} | {ID} | 10-second samples | sheet {start//24+1}',fill='white')
    for i,frame in enumerate(entries):
        with Image.open(ROOT/frame['file']) as original:
            thumb=original.copy();thumb.thumbnail((312,176))
            x=(i%4)*320+4;y=(i//4)*205+40;canvas.paste(thumb,(x,y))
            draw.text((x,y+178),frame['time'],fill='white')
    name=f'overview-{start//24+1:02}.jpg';canvas.save(OUT/name,quality=92)
    sheets.append(str((OUT/name).relative_to(ROOT)).replace('\\','/'))
manifest={'source_url':info['webpage_url'],'video_id':ID,'title':info['title'],'uploader':info['uploader'],
          'upload_date':info['upload_date'],'duration_seconds':info['duration'],
          'source_video_local':str(VIDEO.relative_to(ROOT)).replace('\\','/'),
          'source_video_sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
          'download':'yt-dlp best video <=1080 plus best audio, merged mp4; available video720p',
          'extraction':'ffmpeg -ss seconds -frames:v1 -q:v2; full decoded resolution; no crop/repaint',
          'contact_sheets':'Pillow resized previews on separate labelled sheets; source stills unchanged',
          'frames':frames,'contact_sheets':sheets,'status':'Unselected reference samples; compare2019 footage against current photos'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'stills':len(frames),'sheets':sheets,'dimensions':frames[0]['dimensions']},indent=2))
