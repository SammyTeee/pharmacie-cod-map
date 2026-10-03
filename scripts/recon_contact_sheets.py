from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]/'recon/v18'
for phase in ('before','after'):
    paths=sorted((ROOT/phase).glob('[0-9][0-9]_*.png'))
    for start in range(0,len(paths),12):
        sheet=Image.new('RGB',(1200,660),(25,25,25));draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(paths[start:start+12]):
            im=Image.open(p).convert('RGB');im.thumbnail((300,192))
            x=(i%4)*300;y=(i//4)*220;sheet.paste(im,(x,y));draw.text((x+5,y+195),p.stem,fill='white')
        sheet.save(ROOT/phase/f'contact-{start//12+1:02d}.jpg',quality=94)
    print(phase,len(paths),'frames')
