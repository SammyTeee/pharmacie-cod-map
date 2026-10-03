from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/video-references/q0zBpicUXjg';OUT=BASE/'textures-downstairs';OUT.mkdir(exist_ok=True)
items=[('camera-cabinet','07-29',(6,45,762,426)),('camera-adverts','07-29',(9,440,1130,710)),('medicine-adverts','06-35',(2,489,1130,713)),('medical-shelf','06-35',(1007,179,1270,438))]
records=[]
for name,stamp,rect in items:
 source=BASE/'dense'/f'{stamp}.jpg';dest=OUT/f'{name}.png'
 with Image.open(source) as im:crop=im.crop(rect);crop.save(dest);dims=list(crop.size)
 records.append({'name':name,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'file':str(dest.relative_to(ROOT)),'crop_xyxy':rect,'dimensions':dims,'edits':'Native crop only, no repaint or upscale'})
(OUT/'manifest.json').write_text(json.dumps({'assets':records},indent=2)+'\n')
print('Created four native downstairs crops')
