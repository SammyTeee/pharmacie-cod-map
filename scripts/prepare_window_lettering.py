"""Draw new crisp signage assets from observed wording; never edit photos."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/signage'; OUT.mkdir(exist_ok=True)
lines=['Cask Ales · Lagers','Craft Beers · Ciders','Wines · Spirits','Cocktails']
font=ImageFont.truetype('C:/Windows/Fonts/times.ttf',94)
image=Image.new('RGB',(1024,1024),(224,230,222))
draw=ImageDraw.Draw(image)
draw.rounded_rectangle((22,22,1002,1002),radius=100,outline=(93,105,99),width=5)
draw.rounded_rectangle((38,38,986,986),radius=88,outline=(143,152,144),width=3)
for line,y in zip(lines,(235,410,585,760)):
    assert draw.textlength(line,font=font)<900
    draw.text((512,y),line,font=font,anchor='mm',fill=(28,34,30))
image.save(OUT/'drinks-plaque.png')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">',
     '<rect width="1024" height="1024" fill="#e0e6de"/>',
     '<rect x="22" y="22" width="980" height="980" rx="100" fill="none" stroke="#5d6963" stroke-width="5"/>',
     '<rect x="38" y="38" width="948" height="948" rx="88" fill="none" stroke="#8f9890" stroke-width="3"/>']
for line,y in zip(lines,(235,410,585,760)):
    svg.append(f'<text x="512" y="{y}" text-anchor="middle" dominant-baseline="central" font-family="Times New Roman,serif" font-size="94" fill="#1c221e">{line}</text>')
(OUT/'drinks-plaque.svg').write_text('\n'.join(svg+['</svg>'])+'\n',encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps({'asset':'drinks-plaque.png','dimensions':[1024,1024],
 'reference':'references/pharmacie-syston/pharmacie-arms-syston-2.jpg',
 'wording':lines,'method':'New typeset artwork, not a photo edit or upscaled crop; wording observed in reference; ornamental shape/font/colour approximate',
 'font':'Windows Times New Roman, rasterized locally; font file not distributed',
 'target':'BO3 square RGB TIFF via playtest generator; two outer display panes'},indent=2)+'\n')
print('Prepared high-resolution drinks plaque and editable SVG; originals untouched')
