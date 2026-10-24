from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'recon/showcase'
def add_aerial(page):
 if 'id="aerials"' in page:return page
 titles=['Whole street','Pub and road junction','Melton Road','Brook crossing and Taraj']
 cards=''.join('<figure><a class="frame" href="media/aerial-%02d.jpg" target="_blank" rel="noopener"><img loading="lazy" decoding="async" src="media/aerial-%02d.jpg" alt="%s from above"><span class="label">V39</span></a><figcaption><h3>%s</h3></figcaption></figure>'%(i,i,title,title) for i,title in enumerate(titles,1))
 section='<section id="aerials"><div class="section-head"><h2>Map overview</h2><p>V39 · Aerial views</p></div><div class="stills">'+cards+'</div></section>'
 return page.replace('<a href="#films">Video previews</a>','<a href="#aerials">Map overview</a><a href="#films">Video previews</a>').replace('<section id="films">',section+'<section id="films">')
if __name__=='__main__':
 for i in range(1,5):
  with Image.open(OUT/'media'/('aerial-%02d.jpg'%i)) as im:im.load();assert im.size==(1600,900)
 p=OUT/'index.html';p.write_text(add_aerial(p.read_text(encoding='utf-8')),encoding='utf-8')
 files=[p,*sorted((OUT/'media').iterdir())];(OUT/'manifest.json').write_text(json.dumps({str(f.relative_to(OUT)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2));print('AERIAL_SHOWCASE_READY')
