"""Retain corridor checks; update driveway routes for forward right arm."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
f=ROOT/'scripts/check_extension_v41.py'
s=f.read_text().replace("'pharmacie-station-holmdale-v45.blend')","'pharmacie-station-holmdale-v45.blend','pharmacie-holmdale-depth-v47.blend')")
s=s.replace("('v44','v45')","('v44','v45','v47')").replace("output_version=='v45'","output_version in ('v45','v47')")
s=s.replace('(12,-1.1,0)','(12,-3.35,0)').replace('(3,-3,0)','(3,-5.2,0)').replace('(13,-3,0)','(13,-5.2,0)')
# A recessed porch approach is a narrow pedestrian passage, not a road lane:
# retain .42 radius rays, sample centre and +/-.2 instead of +/−1.2 centres.
s=s.replace('for off in (0,half+1.2,-half-1.2):',"for off in ((0,.2,-.2) if key=='house_approach' else (0,half+1.2,-half-1.2)):")
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns);result=ns['result']
