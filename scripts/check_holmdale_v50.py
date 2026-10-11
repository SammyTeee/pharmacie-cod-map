"""v49 corridor samples plus diagonal approach across v50 porch landing."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];f=ROOT/'scripts/check_holmdale_v49.py'
s=f.read_text().replace("'pharmacie-holmdale-porch-v49.blend'","'pharmacie-holmdale-corner-porch-v50.blend'").replace("'v49'","'v50'")
# This wrapper has no nested string injections; modify only its replacement target.
s=s.replace('(3.9,-11.5,0),(3.9,-1.7,0)','(3.9,-11.5,0),(1.5,-3,0),(3.26,-1.24,0)')
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns);result=ns['result']
