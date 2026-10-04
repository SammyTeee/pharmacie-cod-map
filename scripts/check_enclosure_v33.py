"""Saved-file route regression plus v33 solid and parent preservation checks."""
from pathlib import Path
import bpy,bmesh,json
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'recon/v33'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
solids=[]
for obj in scene.objects:
    if obj.type=='MESH' and obj.name.startswith('Mapping v33 |'):
        bm=bmesh.new();bm.from_mesh(obj.data)
        assert all(e.is_manifold for e in bm.edges),obj.name
        assert bm.calc_volume(signed=True)>0,obj.name
        solids.append(obj.name);bm.free()
manifest=json.loads((dest/'changes.json').read_text())
assert sorted(solids)==sorted(manifest['solids'])
script=(ROOT/'scripts/check_frontage_detail_v32.py').read_text()
script=script.replace("dest=ROOT/'recon/v32'", "dest=ROOT/'recon/v33'")
script=script.replace("parent=Path(changes['source'])", "parent=ROOT/changes['source']")
script=script.replace('V32_CHECKS_PASS','V33_CHECKS_PASS')
exec(compile(script,'retained_street_and_pub_checks','exec'))
