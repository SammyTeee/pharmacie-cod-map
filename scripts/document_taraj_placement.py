"""Draw a source-oriented plan to make the pub-to-Taraj relationship reviewable."""
from pathlib import Path
import json,math,html
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'recon/v22/validation.json').read_text());s=r['metres_per_pixel_estimate']
latest=ROOT/'recon/v24/validation.json'
destination=ROOT/'recon/v24' if latest.exists() else ROOT/'recon/v23'
length=math.hypot(180,137);ax,ay=180/length,137/length
def pixel(p):
    along=-(p[0]+40)/s;across=(p[1]+6.7)/s
    return (1065+ax*along-ay*across,352+ay*along+ax*across)
def coords(points):return ' '.join(f'{x:.2f},{y:.2f}' for x,y in map(pixel,points))
path=r['melton_centreline'];taraj=json.loads(latest.read_text())['new_front'] if latest.exists() else r['placeholder_buildings'][-1]['front_centre']
parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="250 100 950 1000"><rect x="250" y="100" width="950" height="1000" fill="#18222b"/>',
 '<style>text{font-family:Arial,sans-serif;fill:#eef4f7;font-size:20px}.small{font-size:15px;fill:#a9bccb}</style>',
 '<text x="290" y="140">Pharmacie → roundabout → Melton Road → Taraj</text>',
 '<text class="small" x="290" y="166">Reference-oriented plan · estimated gameplay scale</text>']
for pts,color,width in [([(66,-6.7),(-40,-6.7)],'#5d7180',28),(path,'#5d7180',30)]:parts.append(f'<polyline points="{coords(pts)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>')
parts.append('<circle cx="1065" cy="352" r="27" fill="#5d7180"/><circle cx="1065" cy="352" r="7" fill="#e1e5df"/>')
parts.append('<path d="M770 801 L582 742" stroke="#5d7180" stroke-width="20"/><text x="470" y="745">Brookside</text>')
for name,p,color,dx,dy in [('Pharmacie Arms',(4,0),'#efbc53',-185,0),('Natural Wellbeing',(52.5,-13),'#9acc91',-100,-25),('Taraj Palace',taraj,'#ef785f',20,5)]:
    x,y=pixel(p);parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="9" fill="{color}"/><text x="{x+dx:.2f}" y="{y+dy:.2f}">{html.escape(name)}</text>')
side='opposite road side per Sam correction' if latest.exists() else 'east/right from roundabout'
parts+=['<text x="1000" y="415">Roundabout</text>','<text x="850" y="600" transform="rotate(-55 850 600)">Melton Road</text>',f'<text class="small" x="290" y="1040">Taraj: beyond Brookside; {side}.</text>','<text class="small" x="290" y="1070">Street layout estimated; exact real-world metres remain unconfirmed.</text>','</svg>']
(destination/'pub-to-taraj-plan.svg').write_text('\n'.join(parts)+'\n')
roadlength=sum(math.dist(a,b) for a,b in zip(path,path[1:]))
result={'pub_front_anchor_world':[4,0],'natural_wellbeing_front_world':[52.5,-13],'roundabout_world':[-40,-6.7],'taraj_front_world':taraj,'taraj_side':side,'relation':'Beyond Brookside; pub retained on High Street','full_melton_blockout_centreline_length_m':roadlength,'scale_status':'Estimated against enlarged gameplay scene, not a surveyed real-world distance'}
(destination/'placement.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
