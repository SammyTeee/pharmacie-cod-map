"""Portable source UV catalogue from v16; no reference image changes."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1]
s=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=s;bpy.context.view_layer.update()
fronts=[]
for o in s.objects:
    if not o.name.endswith('photographic front'):continue
    image=next(n.image for n in o.active_material.node_tree.nodes if n.type=='TEX_IMAGE' and n.image)
    source=Path(bpy.path.abspath(image.filepath))
    fronts.append({'name':o.name,'source':str(source.relative_to(ROOT)),'uv':[list(d.uv) for d in o.data.uv_layers.active.data],'world':[list(o.matrix_world@v.co) for v in o.data.vertices]})
dest=ROOT/'assets/street/v17/input-facades.json';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps({'fronts':fronts},indent=2)+'\n')
print('Extracted',len(fronts),'portable facade records')
