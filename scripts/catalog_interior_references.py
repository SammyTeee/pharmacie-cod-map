"""Make numbered review sheets; never modify source photographs."""
from pathlib import Path
import json
import hashlib
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'references/pharmacie-syston'
OUT=ROOT/'assets/blender/photo-review'
OUT.mkdir(parents=True,exist_ok=True)
photos=[p for p in sorted(SOURCE.iterdir()) if p.suffix.lower() in ('.jpg','.jpeg','.png','.avif') and not any(t in p.name.lower() for t in ('plan','preview'))]
entries=[]
for i,path in enumerate(photos,1):
    with Image.open(path) as im:
        entries.append({'id':i,'source':path.name,'dimensions':list(im.size),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
for offset in range(0,len(photos),8):
    sheet=Image.new('RGB',(1200,1400),'#e9e9e9')
    draw=ImageDraw.Draw(sheet)
    for j,path in enumerate(photos[offset:offset+8]):
        x=(j%2)*600
        y=(j//2)*350
        with Image.open(path) as im:
            thumbnail=ImageOps.contain(ImageOps.exif_transpose(im).convert('RGB'),(590,310))
            sheet.paste(thumbnail,(x+(600-thumbnail.width)//2,y+28+(310-thumbnail.height)//2))
        draw.text((x+10,y+8),f'{offset+j+1:02}  {path.name[:65]}',fill='black')
    sheet.save(OUT/f'contact-sheet-{offset//8+1}.jpg',quality=90)
(OUT/'catalog.json').write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
with Image.open(SOURCE/'great for texture.avif') as im:
    im.convert('RGBA').save(OUT/'feature-wall-lossless.png')
print(json.dumps({'photos':len(photos),'sheets':len(range(0,len(photos),8)),'catalog':str(OUT/'catalog.json')}))
