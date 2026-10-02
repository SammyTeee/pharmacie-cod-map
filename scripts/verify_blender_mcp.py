"""Exercise official MCP initialization, listing, Blender inspection and editing."""
import asyncio
import json
import os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]

async def main():
    params = StdioServerParameters(
        command=str(ROOT / 'build/blender-mcp-env/Scripts/blender-mcp.exe'),
        env={**os.environ, 'BLENDER_MCP_HOST': '127.0.0.1', 'BLENDER_MCP_PORT': '9876',
             'BLENDER_PATH': 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            listed = await session.list_tools()
            inspect = await session.call_tool('get_blendfile_summary_datablocks', {})
            edit = await session.call_tool('execute_blender_code', {'code':
                "import bpy\nbpy.context.scene['mcp_verified'] = True\n"
                "bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)\n"
                "result = {'verified': True, 'file': bpy.data.filepath, 'version': bpy.app.version_string}"})
            report = {'server': init.serverInfo.model_dump(), 'tool_count': len(listed.tools),
                      'inspection': inspect.model_dump(mode='json'), 'edit': edit.model_dump(mode='json')}
            (ROOT / 'build/blender-mcp-verification.json').write_text(json.dumps(report, indent=2))
            print(json.dumps(report, indent=2))
            assert not inspect.isError and not edit.isError

asyncio.run(main())
