import bpy,json
from pathlib import Path
rows=[]
for o in bpy.data.objects:
 if o.type=='MESH' and any(s in o.name for s in ('closed pitched','upper facade')):
  rows.append(dict(name=o.name,matrix=[list(r) for r in o.matrix_world],bounds=[[min(v.co[i] for v in o.data.vertices),max(v.co[i] for v in o.data.vertices)] for i in range(3)]))
Path('build/roof-v35.json').write_text(json.dumps(rows,indent=2))
