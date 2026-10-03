"""Create native-resolution PNG crops from visually inspected video stills."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/video-references/q0zBpicUXjg'
OUT=BASE/'textures';OUT.mkdir(exist_ok=True)
items=[('music-muddy-waters','12-31',(438,55,658,293)),
 ('music-elvis','12-31',(669,43,883,293)),('music-chuck-berry','12-31',(455,363,653,594)),
 ('music-hit-parade','12-31',(665,303,879,599)),
 ('corridor-beer','13-53',(580,244,724,450)),
 ('medical-board','06-54',(238,90,633,490)),
 ('medical-detail','14-28',(170,35,1210,680)),
 ('radio-one','13-30',(190,153,342,245)),('radio-two','13-30',(356,151,489,247)),
 ('radio-three','13-30',(504,163,632,250)),('radio-four','13-30',(652,164,763,249)),
 ('book-spines','11-48',(223,83,485,191))]
manifest=[]
sheet=Image.new('RGB',(1200,900),'#222222');draw=ImageDraw.Draw(sheet)
for i,(name,stamp,box) in enumerate(items):
 source=BASE/'dense'/f'{stamp}.jpg';dest=OUT/f'{name}.png'
 with Image.open(source) as im:
  crop=im.crop(box);crop.save(dest);dims=list(crop.size)
  crop.thumbnail((285,260));x=i%4*300+6;y=i//4*300+6;sheet.paste(crop,(x,y));draw.text((x,y+265),name+' | '+stamp.replace('-',':'),fill='white')
 manifest.append({'name':name,'file':str(dest.relative_to(ROOT)).replace('\\','/'),'source':str(source.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop_xyxy':box,'dimensions':dims,'edits':'Native crop only; PNG; no upscale, sharpening, repaint or perspective correction','status':'Blender reference texture; BO3 conversion and runtime verification pending'})
(OUT/'manifest.json').write_text(json.dumps({'source_url':'https://www.youtube.com/watch?v=q0zBpicUXjg','assets':manifest},indent=2)+'\n')
sheet.save(OUT/'texture-review.jpg',quality=95)
print('Created 12 native PNG texture crops')
