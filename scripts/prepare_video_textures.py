"""Dense authentic video sampling and sharp-frame selection; originals preserved."""
from pathlib import Path
import cv2, json
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/video-references/q0zBpicUXjg'
DENSE=OUT/'dense';DENSE.mkdir(exist_ok=True)
cap=cv2.VideoCapture(str(ROOT/'build/video-reference/q0zBpicUXjg.mp4'))
records=[]
for start,end in ((350,540),(610,891)):
 for second in range(start,end):
  cap.set(cv2.CAP_PROP_POS_MSEC,second*1000);ok,frame=cap.read()
  if not ok:continue
  gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  sharp=float(cv2.Laplacian(gray,cv2.CV_64F).var())
  path=DENSE/f'{second//60:02}-{second%60:02}.jpg'
  cv2.imwrite(str(path),frame,[cv2.IMWRITE_JPEG_QUALITY,95])
  records.append({'seconds':second,'sharpness':round(sharp,2),'file':str(path.relative_to(ROOT)).replace('\\','/')})
cap.release()
best=[]
for second in range(350,895,5):
 group=[r for r in records if second<=r['seconds']<second+5]
 if group:best.append(max(group,key=lambda r:r['sharpness']))
for start in range(0,len(best),24):
 canvas=Image.new('RGB',(1280,1278),'#181b20');draw=ImageDraw.Draw(canvas)
 draw.text((8,8),'Dense tour review: sharpest frame per 5 seconds (score is only a blur heuristic)',fill='white')
 for i,r in enumerate(best[start:start+24]):
  with Image.open(ROOT/r['file']) as im:
   im.thumbnail((312,176));x=i%4*320+4;y=i//4*205+40;canvas.paste(im,(x,y))
   draw.text((x,y+178),f"{r['seconds']//60:02}:{r['seconds']%60:02} | sharpness {r['sharpness']}",fill='white')
 canvas.save(OUT/f'dense-review-{start//24+1:02}.jpg',quality=93)
(OUT/'dense-manifest.json').write_text(json.dumps({'source_url':'https://www.youtube.com/watch?v=q0zBpicUXjg','sampling':'1 frame/second in tour segments 05:50–09:00 and 10:10–14:51; JPEG95, no crop; Laplacian variance selects candidates, visual inspection required','frames':records,'review_candidates':best},indent=2)+'\n')
print(json.dumps({'dense_frames':len(records),'review_candidates':len(best)}))
