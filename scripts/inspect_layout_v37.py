from pathlib import Path
import bpy,json
from mathutils import Vector
out=[]
for o in bpy.data.scenes['03 Both floors - assembled exterior'].objects:
 if any(t in o.name.lower() for t in ('shelter','b031','b037')) or ('upper facade' in o.name and o.get('catalogue_id') in ('B030','B038','B042','B043')):
  vs=[o.matrix_world@Vector(v) for v in o.bound_box]
  out.append(dict(name=o.name,loc=list(o.location),bounds=[[min(v[i] for v in vs) for i in range(3)],[max(v[i] for v in vs) for i in range(3)]],matrix=[list(r) for r in o.matrix_world]))
Path('build/v37-layout.json').write_text(json.dumps(out,indent=2));print('LAYOUT_COMPLETE')
