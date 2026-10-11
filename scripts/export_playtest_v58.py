"""Read-only export of reviewed v57; keep a separate conversion snapshot."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
code = (ROOT/'scripts/export_playtest_v18.py').read_text()
code = code.replace('pharmacie-player-cleanup-v18.blend', 'pharmacie-surveyed-route-v57.blend')
code = code.replace('build/playtest-v18-geometry.json', 'build/playtest-v58-geometry.json')
# Collection archive flags, not just per-object flags, govern the reviewed scene.
code = code.replace("if o.type not in ('MESH','FONT') or o.hide_render: continue", "if o.type not in ('MESH','FONT') or o.hide_render: continue\n    if any(c.hide_render or 'ARCHIVE' in c.name.upper() for c in o.users_collection): continue")
code = code.replace("raise RuntimeError(f'Image surface needs explicit quad conversion: {o.name}')", "warnings.append({'object':o.name,'issue':'Unsupported multi-face photo represented by flat material in this test'}); image=None")
exec(compile(code, str(ROOT/'scripts/export_playtest_v18.py'), 'exec'))
