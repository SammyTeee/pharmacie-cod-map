"""Review every half second of the new walkthrough, preserving decoded frames."""
from pathlib import Path
import cv2,json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/video-references/facebook-18ZXq1yVKY';OUT.mkdir(exist_ok=True);(OUT/'stills').mkdir(exist_ok=True)
VIDEO=ROOT/'build/video-reference/facebook-18ZXq1yVKY.mp4';cap=cv2.VideoCapture(str(VIDEO));fps=cap.get(cv2.CAP_PROP_FPS)
records=[];index=0;next_time=0
while True:
 ok,frame=cap.read()
 if not ok:break
 t=index/fps;index+=1
 if t<next_time:continue
 sec=round(next_time,1);next_time+=.5
 path=OUT/'stills'/f'{sec:06.1f}.jpg';cv2.imwrite(str(path),frame,[cv2.IMWRITE_JPEG_QUALITY,95])
 records.append({'seconds':sec,'file':str(path.relative_to(ROOT)).replace('\\','/'),'sharpness':round(float(cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),cv2.CV_64F).var()),2),'dimensions':[frame.shape[1],frame.shape[0]]})
cap.release()
# Small sheets with only 12 portrait frames keep details readable.
for start in range(0,len(records),12):
 canvas=Image.new('RGB',(1440,3*650+40),'#181b20');draw=ImageDraw.Draw(canvas)
 draw.text((8,8),f'Facebook walkthrough | half-second frames | sheet {start//12+1}',fill='white')
 for i,r in enumerate(records[start:start+12]):
  with Image.open(ROOT/r['file']) as im:
   im.thumbnail((350,620));x=i%4*360+4;y=i//4*650+35;canvas.paste(im,(x,y));draw.text((x,y+620),f"{r['seconds']:.1f}s | sharpness {r['sharpness']}",fill='white')
 canvas.save(OUT/f'review-{start//12+1:02}.jpg',quality=93)
info=json.loads((ROOT/'build/facebook-video-info.json').read_text(encoding='utf-8-sig'))
(OUT/'manifest.json').write_text(json.dumps({'source_url':'https://www.facebook.com/share/v/18ZXq1yVKY/','video_id':info['id'],'uploader':info['uploader'],'upload_date':info['upload_date'],'duration_seconds':info['duration'],'source_video':str(VIDEO.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'extraction':'OpenCV sequential decode every 0.5 seconds, JPEG95, full native size; separate resized review sheets; originals unchanged','frames':records},indent=2)+'\n')
print(json.dumps({'frames':len(records),'sheets':(len(records)+11)//12,'dimensions':records[0]['dimensions']}))
