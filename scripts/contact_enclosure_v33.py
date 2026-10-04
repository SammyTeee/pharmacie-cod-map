from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'recon/v33'
phase=sys.argv[1] if len(sys.argv)>1 else 'before'
items=sorted(dest.glob('after-flight-*.png' if phase=='flight' else '*_'+phase+'.png'))
sheet=Image.new('RGB',(1600,((len(items)+3)//4)*250),(20,24,28))
draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for i,path in enumerate(items):
    im=Image.open(path).convert('RGB');im.thumbnail((400,225))
    x=i%4*400;y=i//4*250;sheet.paste(im,(x,y));draw.text((x+5,y+227),path.stem,font=font,fill='white')
sheet.save(dest/(phase+'-contact.jpg'))
print('CONTACT_COMPLETE',phase,len(items))
