"""Run a project-owned script through the installed official Blender bridge."""
from pathlib import Path
import json
import sys
from blmcp.tools_helpers.connection import send_code

path = Path(sys.argv[1]).resolve()
root = Path(__file__).resolve().parents[1]
if not path.is_relative_to(root / 'scripts'):
    raise ValueError('Only project scripts are accepted')
code = f'__file__ = {str(path)!r}\n' + path.read_text(encoding='utf-8')
response = send_code(code, strict_json=False)
print(json.dumps(response, indent=2))
if response.get('status') != 'ok':
    raise SystemExit(1)
