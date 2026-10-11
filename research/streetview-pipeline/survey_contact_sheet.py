"""Local review derivatives only; preserve captured originals and ledger."""
from pathlib import Path
import argparse,json
from PIL import Image,ImageDraw

p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--start',type=int,default=0);p.add_argument('--end',type=int,default=100)
a=p.parse_args();ledger=json.loads((a.folder/'ledger.json').read_text())
for batch in range(a.start,a.end):
    rows=[e for e in ledger if e['file'].endswith('r2.jpg') and batch*5<=e['stop_index']<(batch+1)*5]
    if not rows:continue
    out=Image.new('RGB',(1280,5*205),(25,30,35));d=ImageDraw.Draw(out)
    for e in rows:
        x=e['view_index']*320;y=(e['stop_index']%5)*205
        im=Image.open(a.folder/e['file']);im.thumbnail((320,180));out.paste(im,(x,y));d.text((x+3,y+182),e['file'],fill='white')
    out.save(a.folder/f'contact-{batch:02}.jpg')
