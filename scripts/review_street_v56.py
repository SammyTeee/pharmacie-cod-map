"""Latest material previews, retaining v54 matched cameras for comparison."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'scripts/review_street_v54.py';s=p.read_text()
s=s.replace("dest=ROOT/'recon/v54'","dest=ROOT/'recon/v56'")
s=s.replace("(dest/'prepared-street.json').read_text()","(ROOT/'recon/v54/prepared-street.json').read_text()")
s=s.replace("for stage in ('before','after'):","for stage in ('after',):")
s=s.replace("archive=bpy.data.collections[", "views += [('house_front',house,(6,-18,7),(6,0,1.5),None),('house_porch',house,(-2,-6.5,3.7),(3.8,-.7,1.2),None),('holmdale_overhead',Matrix.Identity(4),(-83,826,190),(-83,826,0),245)]\narchive=bpy.data.collections[")
ns={'__file__':str(p)};exec(compile(s,str(p),'exec'),ns);result=ns['result']
