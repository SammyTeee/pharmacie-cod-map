"""Partition repaired concave surfaces into stationary brush models."""
from pathlib import Path
import json,re
from generate_blockout import parse_entity_blocks
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'map_source/zm/zm_pharmacie_v58.map';s=p.read_text()
assert '// v58 static surface groups' not in s
parts=[]
def take(m):
 if 850000<=int(m[1])<900000:
  parts.append(m[0]);return ''
 return m[0]
a,b,ws=parse_entity_blocks(s)[0];ws=re.sub(r'(?ms)^// brush (\d+)\n\{.*?^\}\n?',take,ws)
assert parts
entities=[]
for start in range(0,len(parts),16):
 group=parts[start:start+16]
 entities.append('{\n"classname" "script_brushmodel"\n"targetname" "v58_static_surface_'+str(start//16)+'"\n'+''.join(group)+'}\n')
p.write_text(s[:a]+ws+s[b:]+'\n// v58 static surface groups\n'+''.join(entities),newline='\n')
(ROOT/'docs/build-results/playtest-v58/static-surface-groups.json').write_text(json.dumps({'stationary_brushmodels':len(entities),'brushes':len(parts),'group_size':16,'limits':'No movement script; colliding default brush models. Street navmesh and actual collision require runtime checks. Pub floor remains world geometry.'},indent=2)+'\n')
print(len(parts),'surface prisms in',len(entities),'stationary brushmodels')
