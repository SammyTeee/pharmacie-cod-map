from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
data=[]
for o in scene.objects:
    if o.type!='MESH':continue
    pts=[o.matrix_world@Vector(v) for v in o.bound_box];lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
    if hi[0]<-18 or lo[0]>18 or hi[1]<12 or lo[1]>40:continue
    if not any(t in o.name.lower() for t in ('wall','floor','alley','rear','door','patio','smoking','shell','mass','roof','landing','threshold')):continue
    data.append({'name':o.name,'lo':lo,'hi':hi,'materials':[m.name for m in o.data.materials if m],'collections':[c.name for c in o.users_collection]})
(ROOT/'build/rear-v30-inventory.json').write_text(json.dumps(data,indent=2))
print('INVENTORY',len(data))
