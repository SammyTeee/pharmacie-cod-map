from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/video-references/facebook-18ZXq1yVKY';OUT=BASE/'textures';OUT.mkdir(exist_ok=True)
items=[('fridge-cans','0064.0',(220,800,1000,1190)),('fridge-bottles','0063.0',(200,690,1020,1080)),
 ('backbar-tap-bank','0090.0',(236,860,960,1135)),('dental-board','0124.0',(415,693,710,994)),
 ('medical-adverts','0138.0',(90,987,1060,1160)),('band-aid-advert','0124.0',(512,1004,728,1256)),
 ('pump-original','0071.5',(624,828,860,1109)),('pump-mild','0071.5',(258,817,434,1060))]
records=[];sheet=Image.new('RGB',(1200,630),'#202020');draw=ImageDraw.Draw(sheet)
for i,(name,stamp,crop) in enumerate(items):
 src=BASE/'stills'/f'{stamp}.jpg';dest=OUT/f'{name}.png'
 with Image.open(src) as im:
  texture=im.crop(crop);texture.save(dest);dims=list(texture.size);texture.thumbnail((290,265));x=i%4*300+4;y=i//4*310+4;sheet.paste(texture,(x,y));draw.text((x,y+270),name+' | '+stamp+'s',fill='white')
 records.append({'name':name,'source':str(src.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'file':str(dest.relative_to(ROOT)).replace('\\','/'),'crop_xyxy':crop,'dimensions':dims,'edits':'Native PNG crop; no sharpening/upscale/repaint; perspective and reflections retained','status':'Blender only; BO3 material conversion pending'})
(OUT/'manifest.json').write_text(json.dumps({'source_url':'https://www.facebook.com/share/v/18ZXq1yVKY/','assets':records},indent=2)+'\n');sheet.save(OUT/'texture-review.jpg',quality=94)
print('8 Facebook texture crops created')
