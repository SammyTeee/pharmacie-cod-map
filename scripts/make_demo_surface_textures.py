"""Original, seamless surface textures; no photo or game assets used."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/materials/demo-v59';OUT.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(59014);size=1024
y,x=np.mgrid[:size,:size]/size
grain=rng.normal(0,1,(size,size))
entries=[]
def save(name,rgb,metres):
 p=OUT/(name+'.png');Image.fromarray(np.uint8(np.clip(rgb,0,1)*255)).save(p)
 entries.append({'file':p.name,'repeat_metres':metres,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
def masonry(name,cols,rows,base,mortar,metres,joint):
 row=np.floor(y*rows).astype(int);u=(x*cols+(row%2)*.5)%cols;col=np.floor(u).astype(int)
 fx=u%1;fy=(y*rows)%1
 tint=rng.uniform(.82,1.15,(rows,cols))[row,col]
 broad=.018*np.sin(x*55+y*37)+.012*np.sin(x*137-y*89)
 rgb=np.array(base)[None,None,:]*tint[:,:,None]+(grain*.012+broad)[:,:,None]
 mask=(fx<joint)|(fy<joint*.65)
 rgb[mask]=np.array(mortar)+grain[mask,None]*.008
 # Small dark lower-edge shadow gives a restrained relief cue in viewport mode.
 rgb[(fy>1-joint*.9)&~mask]*=.72
 save(name,rgb,metres)
masonry('slate',16,24,(.24,.275,.30),(.105,.12,.13),(4.8,4.8),.025)
masonry('clay-tile',16,24,(.34,.275,.20),(.14,.13,.115),(4.8,4.8),.028)
for i,base in enumerate(((.45,.235,.15),(.37,.18,.115),(.48,.29,.20))):
 masonry('brick-'+str(i),18,32,base,(.40,.375,.32),(4.23,2.56),.026)
masonry('paving',8,8,(.47,.455,.415),(.285,.28,.26),(4.8,3.6),.018)
rgb=np.ones((size,size,3))*np.array((.19,.205,.21))+(grain*.024)[:,:,None]
rgb+=(.009*np.sin(x*21+y*16))[:,:,None]
save('asphalt',rgb,(3.0,3.0))
(OUT/'manifest.json').write_text(json.dumps({'origin':'Original procedural textures, scripts/make_demo_surface_textures.py; seed 59014','textures':entries},indent=2))
print('AUTHORED_TEXTURES',len(entries))
