"""Rectified, isolated facade derivatives; never alter reference originals."""
from pathlib import Path
import json, hashlib, re
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'assets/street/v17'
OUT.mkdir(parents=True, exist_ok=True)
records=[]
def make(name, source, corners, note):
    source=Path(source)
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    with Image.open(source) as im:
        im=im.convert('RGB'); w,h=im.size
        tl,tr,br,bl=corners
        # PIL QUAD resamples the source quadrilateral into a rectangle.
        quad=tuple(v for p in (tl,bl,br,tr) for v in p)
        slug=re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
        dest=OUT/(slug+'.png')
        im.transform((1024,1024),Image.Transform.QUAD,quad,Image.Resampling.BICUBIC).save(dest)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==before
    records.append(dict(name=name,source=str(source.relative_to(ROOT)),source_sha256=before,source_dimensions=[w,h],pixel_quad_TL_TR_BR_BL=corners,derivative=str(dest.relative_to(ROOT)),dimensions=[1024,1024],format='RGB PNG',edits=note,status='Blender preview; BO3 calibration pending'))
for f in json.loads((OUT/'input-facades.json').read_text())['fronts']:
    source=ROOT/f['source']
    with Image.open(source) as im:w,h=im.size
    opposite=f['world'][0][1]<-5
    ids=(2,3,0,1) if opposite else (3,2,1,0)
    corners=[[f['uv'][i][0]*w,(1-f['uv'][i][1])*h] for i in ids]
    make(f['name'].replace('Video | ','').replace(' photographic front',''),source,corners,'Isolated existing approved UV quadrilateral; QUAD rectification; full-panel UVs. Original occlusions retained; no repainting.')
# Explicit facade bounds from S09 / S14. Ground floor only for the gabled shop:
# the distinctive gable and upstairs windows are rebuilt as geometry.
make('Natural Wellbeing',ROOT/'alt/nattywells/front on natty wells.png',[(37,535),(720,535),(714,833),(36,836)],'S14 ground-floor facade only; excludes blank canvas, roof, sky and access lane; pedestrians remain at lower edge.')
with Image.open(ROOT/'references/post office head on.png') as im:
    print('Post Office dimensions',im.size)
    w,h=im.size
# Bounds measured on the displayed 2048px-wide review, scaled to native pixels.
po_corners=[[x*w/2048,y*h/980] for x,y in [(750,292),(1380,322),(1375,649),(750,652)]]
make('Post Office',ROOT/'references/post office head on.png',po_corners,'S09 isolated wall/window/shop facade; poles occlude some signage; roof and sky excluded.')
(OUT/'manifest.json').write_text(json.dumps({'fronts':records,'rights':'Private reference use; publication rights not established'},indent=2)+'\n')
print('Prepared',len(records),'isolated facade PNGs; originals hash-verified')
