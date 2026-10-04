from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1]
m=bpy.data.materials.new('Temporary v38 detail highlight');m.use_nodes=True;m.diffuse_color=(.95,.50,.04,1);p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=.65
for o in bpy.data.collections['STREET v38 | Town Square passage and shop displays'].objects:
 if o.type in ('MESH','FONT'):
  for slot in o.material_slots:slot.material=m
code=(ROOT/'scripts/inspect_street_v38.py').read_text().replace("phase='after' if 'v38' in bpy.data.filepath else 'before'","phase='highlight'")
exec(compile(code,'v38_highlight_render','exec'))
