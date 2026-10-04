"""Apply validation-discovered frontage return correction once to v30."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1];scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
assert Path(bpy.data.filepath).name=='pharmacie-zombies-alley-v30.blend'
wall=bpy.data.objects['Mapping v30 | Outer alley east brick boundary']
assert min(v.co.y for v in wall.data.vertices)>14
for o in [wall]+[o for o in scene.objects if o.name.startswith('Mapping v30 | Boundary stone coping') and abs(min(v.co.x for v in o.data.vertices)+10.41)<.02]:
    for v in o.data.vertices:
        if v.co.y<15:v.co.y=.15
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
p=ROOT/'recon/v30/changes.json';r=json.loads(p.read_text());r['review_correction']='East alley wall extended to street mouth after side-enclosure ray found frontage gap';p.write_text(json.dumps(r,indent=2))
print('V30_FRONTAGE_RETURN_FIXED')
