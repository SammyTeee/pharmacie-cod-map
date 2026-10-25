"""Verify exported photo pixels, triangle totals, paid progression and spawn solids.

Run after generating the core. These are source checks, never gameplay claims.
"""
from pathlib import Path
from collections import Counter
import ast
import hashlib
import json
import re
from PIL import Image, ImageChops
from bo3_map_io import parse_map_entities
from generate_blockout import kv
from bo3_xmodel_format import validate_model_binary

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'build/bo3-core'
report = json.loads((OUT/'model-report.json').read_text())
manifest = json.loads((OUT/'manifest.json').read_text())
materials = {m['asset']:m for m in manifest['materials']}
assert hashlib.sha256((ROOT/report['source']).read_bytes()).hexdigest() == report['source_sha256']
photos = []
for image in report['images']:
    if image['kind'] != 'image':
        continue
    m = materials[image['asset']]
    with Image.open(ROOT/m['source']) as original, Image.open(OUT/'textures'/(m['asset']+'.tif')) as converted:
        w,h = original.size
        a,b = original.convert('RGBA'),converted.convert('RGBA').crop((0,0,w,h))
        assert a.tobytes() == b.tobytes(), 'Photo pixels changed: '+m['name']
    photos.append({'material':m['name'],'native_dimensions':[w,h],'unchanged_source_pixels':True})
model_triangles = 0
for model in report['models']:
    path = OUT/report['model_directory']/(model['asset']+'.xmodel_export')
    text = path.read_text()
    count = int(re.search(r'NUMFACES (\d+)',text)[1])
    assert count == model['triangles']
    assert len(re.findall(r'^TRI ',text,re.M)) == count
    assert len(re.findall(r'^UV 1 ',text,re.M)) == count*3
    assert int(re.search(r'NUMMATERIALS (\d+)',text)[1]) == len(model['materials'])
    assert re.findall(r'^MATERIAL \d+ "([^"]+)"',text,re.M) == model['materials']
    assert all(b-a>.0001 for a,b in zip(*model['bounds_BU'])), 'Planar static-model bounds'
    binary = path.with_suffix('.xmodel_bin')
    validate_model_binary(binary)
    assert hashlib.sha256(binary.read_bytes()).hexdigest() == model['sha256']
    model_triangles += count
assert model_triangles == report['triangles'] == sum(m.get('triangles',0) for m in manifest['materials'])

map_path = ROOT/'map_source/zm/zm_pharmacie_core65.map'
text = map_path.read_text()
entities = parse_map_entities(text)
assert len(entities) == len(re.findall(r'^// entity \d+$',text,re.M)), 'Unnumbered or lost generated entity'
initials = [b for _,_,b in entities if kv(b,'script_noteworthy')=='initial_spawn']
assert len(initials) == 4 and len({kv(b,'origin') for b in initials}) == 4
triggers = [b for _,_,b in entities if kv(b,'classname')=='trigger_use']
assert Counter(kv(b,'zombie_cost') for b in triggers) == Counter({'750':2,'1000':1,'1250':2})
assert sum(kv(b,'classname')=='misc_model' for _,_,b in entities) == len(report['models'])
assert 'v58_route_' not in text and 'Taraj' not in text

# Use the existing independent half-space collision audit on both starts and
# all four actual stock initial_spawn structs, rather than checking one marker.
tree = ast.parse((ROOT/'scripts/check_playtest_v58_spawn.py').read_text())
body = [n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or
        isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('num','triple') for t in n.targets)]
ns = {}
exec(compile(ast.Module(body=body,type_ignores=[]),'existing-half-space-check','exec'),ns)
extra = ''.join('\n// entity '+str(10000+i)+'\n'+b.replace('"classname" "script_struct"','"classname" "info_player_coop"') for i,b in enumerate(initials))
spawns = ns['audit'](text+extra)
assert len(spawns)==5
assert all(not s['body_intersections'] and s['support_brushes'] for s in spawns)
gsc = (ROOT/'usermaps/zm_pharmacie_core65/scripts/zm/zm_pharmacie_core65.gsc').read_text()
assert 'zm_usermap::main();' in gsc and 'round_spawn_func' not in gsc and 'Invulnerability' not in gsc
result = {'source_sha256_unchanged':report['source_sha256'], 'native_photo_pixel_checks':photos,
          'models':len(report['models']), 'triangles':model_triangles, 'unique_initial_spawns':4,
          'spawn_checks':spawns,'paid_trigger_costs':dict(Counter(kv(b,'zombie_cost') for b in triggers)),
          'limits':'Source checks only; official compiler, runtime texture fidelity, purchases, AI and co-op remain separate gates.'}
(OUT/'source-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('CORE_CHECK_PASS',len(photos),'photo materials;',model_triangles,'triangles;',len(spawns),'supported clear starts')
