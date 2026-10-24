from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1];out=[]
for name in ['pharmacie-zombies-alley-v30.blend','pharmacie-syston-detail-v29.blend']:
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/blender'/name));o=bpy.data.objects['Ground shell 03 | door 0 | open leaf']
    out.append({'file':name,'matrix':list(map(list,o.matrix_world)),'local':list(map(list,o.matrix_local)),'location':list(o.location),'rotation':list(o.rotation_euler),'parent':o.parent.name if o.parent else None,'vertices':[list(v.co) for v in o.data.vertices],'world':[list(o.matrix_world@v.co) for v in o.data.vertices]})
(ROOT/'build/door-archive-v30.json').write_text(json.dumps(out,indent=2))
