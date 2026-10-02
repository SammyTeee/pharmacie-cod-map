"""Install the locally built official Blender Lab extension. Run in background Blender."""
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]
print('Extension repositories:', [(r.name, r.module) for r in bpy.context.preferences.extensions.repos])
bpy.ops.extensions.package_install_files(
    filepath=str(ROOT / 'build/mcp-1.0.0.zip'),
    repo='user_default', enable_on_install=True,
)
key = 'bl_ext.user_default.mcp'
prefs = bpy.context.preferences.addons[key].preferences
prefs.host = '127.0.0.1'
prefs.port = 9876
prefs.use_autostart = True
bpy.ops.wm.save_userpref()
print('Official Blender Lab MCP installed and enabled:', key)
