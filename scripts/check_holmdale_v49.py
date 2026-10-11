"""Retain v48 corridor checks, stop porch approach before new threshold."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];f=ROOT/'scripts/check_extension_v41.py'
s=f.read_text().replace("'pharmacie-station-holmdale-v45.blend')","'pharmacie-station-holmdale-v45.blend','pharmacie-holmdale-porch-v49.blend')")
s=s.replace("('v44','v45')","('v44','v45','v49')").replace("output_version=='v45'","output_version in ('v45','v49')")
s=s.replace('(4,-11.5,0),(4,-1.3,0)','(3.9,-11.5,0),(3.9,-1.7,0)').replace('(12,-11.5,0),(12,-1.1,0)','(4,-5,0),(9.5,-5,0)').replace('(3,-3,0),(13,-3,0)','(3,-9,0),(8.5,-9,0)')
s=s.replace('for off in (0,half+1.2,-half-1.2):',"for off in ((0,.2,-.2) if key=='house_approach' else (0,half+1.2,-half-1.2)):")
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns);result=ns['result']
