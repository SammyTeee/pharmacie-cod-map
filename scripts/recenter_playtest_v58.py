"""Apply one documented engine-space translation to the entire generated map."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'map_source/zm/zm_pharmacie_v58.map'
s=p.read_text();assert '// v58 engine translation' not in s
before=hashlib.sha256(p.read_bytes()).hexdigest()
backup=ROOT/'build/playtest-v58-before-recenter.map'
if not backup.exists():backup.write_text(s,newline='\n')
offset=(0,-18000,0);counts={'planes':0,'mesh_vertices':0,'origins':0}
num=r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
def xyz(vals):return ' '.join(f'{float(v)+offset[i]:.6f}'.rstrip('0').rstrip('.') or '0' for i,v in enumerate(vals))
def plane(m):counts['planes']+=1;return '( '+xyz(m.groups())+' )'
s=re.sub(r'\(\s*('+num+r')\s+('+num+r')\s+('+num+r')\s*\)',plane,s)
def vertex(m):counts['mesh_vertices']+=1;return m[1]+xyz(m.groups()[1:])
s=re.sub(r'(?m)^(\s*v\s+)('+num+r')\s+('+num+r')\s+('+num+r')',vertex,s)
def origin(m):counts['origins']+=1;return m[1]+xyz(m[2].split())+'"'
s=re.sub(r'(?m)^(\s*"origin"\s+")([^"]+)"',origin,s)
s='// v58 engine translation 0 -18000 0; dimensions unchanged\n'+s
p.write_text(s,newline='\n')
out=ROOT/'docs/build-results/playtest-v58/engine-recenter.json'
out.write_text(json.dumps({'offset_engine_units':offset,'counts':counts,'before_sha256':before,'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'contract':'engine = (BU + (-3.5,-10,0))*39.37007874015748 + (0,-18000,0)','reason':'Retry after repeated cell/portal emission access violations; full old-axis bounds exceeded 32768. Causality pending successful compiler result.'},indent=2)+'\n')
print(counts)
