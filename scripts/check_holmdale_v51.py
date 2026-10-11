"""Retain v50 route samples for the mirrored left window."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
f=ROOT/'scripts/check_holmdale_v50.py'
s=f.read_text().replace('pharmacie-holmdale-corner-porch-v50.blend','pharmacie-holmdale-mirrored-window-v51.blend').replace('"\'v50\'"','"\'v51\'"')
s=s.replace('(3.26,-1.24,0)','(3.26,-1.69,0)')
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns);result=ns['result']
