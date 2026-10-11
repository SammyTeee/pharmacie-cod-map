"""v48 route adaptation for perpendicular garage; inherited road checks."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];f=ROOT/'scripts/check_holmdale_v47.py'
s=f.read_text().replace("'pharmacie-holmdale-depth-v47.blend'","'pharmacie-holmdale-garage-v48.blend'").replace("'v47'","'v48'")
s=s.replace("ns={'__file__':str(f)};exec", "s=s.replace('(12,-11.5,0),(12,-3.35,0)','(4,-5,0),(9.5,-5,0)').replace('(3,-5.2,0),(13,-5.2,0)','(3,-9,0),(8.5,-9,0)')\nns={'__file__':str(f)};exec")
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns);result=ns['result']
