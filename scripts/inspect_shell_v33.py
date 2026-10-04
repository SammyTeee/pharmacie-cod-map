from pathlib import Path
import bpy,json
from mathutils import Vector
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
out={}
for obj in scene.objects:
    if obj.type=='MESH' and (obj.name in ('Ground | continuous timber floor','First | floor with corrected L stairwell opening','Recon v18 | Upper removable ceiling') or obj.name.startswith('Ground shell')):
        out[obj.name]={'vertices':[list(obj.matrix_world@v.co) for v in obj.data.vertices],
                       'faces':[list(p.vertices) for p in obj.data.polygons]}
(Path(__file__).resolve().parents[1]/'build/v33-shell-meshes.json').write_text(json.dumps(out))
print('SHELL_INVENTORY_COMPLETE',len(out))
