"""Readable walkthrough-only sheets: remove editorial bars from previews only."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/video-references/facebook-18ZXq1yVKY'
frames=[r for r in json.loads((OUT/'manifest.json').read_text())['frames'] if r['seconds']>=54]
for start in range(0,len(frames),18):
 canvas=Image.new('RGB',(1440,1810),'#181b20');draw=ImageDraw.Draw(canvas)
 draw.text((8,8),'Walkthrough details every 0.5s | editorial bars omitted from previews only',fill='white')
 for i,r in enumerate(frames[start:start+18]):
  with Image.open(ROOT/r['file']) as im:
   thumb=im.crop((0,660,1080,1260));thumb.thumbnail((470,262))
   x=i%3*480+4;y=i//3*295+30;canvas.paste(thumb,(x,y));draw.text((x,y+265),str(r['seconds'])+'s',fill='white')
 canvas.save(OUT/f'detail-{start//18+1:02}.jpg',quality=94)
print('Created 11 readable detail sheets; source frames retained intact')
