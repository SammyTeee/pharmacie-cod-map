from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v32';font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
def sheet(items,path):
 out=Image.new('RGB',(1280,((len(items)+3)//4)*205),(20,24,28));d=ImageDraw.Draw(out)
 for i,(p,label) in enumerate(items):
  im=Image.open(p).convert('RGB');im.thumbnail((320,180));x=i%4*320;y=i//4*205;out.paste(im,(x,y));d.text((x+5,y+181),label,font=font,fill='white')
 out.save(path)
sheet([(p,p.stem[:32]) for p in sorted(dest.glob('*_after.png'))],dest/'still-contact-sheet.jpg')
frames=ROOT/'build/v32-flythrough-frames';items=[(frames/f'{i:05d}.png',f'{i/24:.1f}s') for i in (0,72,144,216,288,360,408,432,456,480,552,648) if (frames/f'{i:05d}.png').exists()];sheet(items,dest/'flythrough-contact-sheet.jpg')
print('MEDIA_CONTACT_SHEETS',len(items))
