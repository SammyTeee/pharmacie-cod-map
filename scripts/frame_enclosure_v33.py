"""Save review cameras/editor view only; geometry and parent remain unchanged."""
from pathlib import Path
import bpy,ast
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-enclosure-detail-v33.blend'
tree=ast.parse((ROOT/'scripts/build_enclosure_v33.py').read_text())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='setup_review_views')
exec(compile(ast.Module(body=[node],type_ignores=[]),'saved_v33_views','exec'))
setup_review_views()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('V33_EDITOR_VIEW_SAVED')
