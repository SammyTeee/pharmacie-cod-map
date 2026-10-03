"""Source integrity and structural checks; does not claim runtime gameplay passes."""
from pathlib import Path
from PIL import Image
import json,hashlib,re
from generate_blockout import kv
ROOT=Path(__file__).resolve().parents[1]
name='zm_pharmacie_playtest'
original=json.loads((ROOT/'build/playtest-v18-geometry.json').read_text())
converted=json.loads((ROOT/'build/playtest-v18-panels.json').read_text())
converted_by_name={o['name']:o for o in converted['objects']}
bar_records=json.loads((ROOT/'assets/bar-regions/manifest.json').read_text())['regions']
bar_by_name={r['object']:r for r in bar_records}
for o in original['objects']:
    if o['image']:
        if o['name'] in bar_by_name:
            record=bar_by_name[o['name']]
            assert record['original_uvs']==o['face_uvs'][0]
            with Image.open(record['source']) as im:
                expected=im.convert('RGB').crop(record['crop_pixels'])
            with Image.open(ROOT/record['derivative']) as actual:
                assert actual.size==expected.size and actual.tobytes()==expected.tobytes()
        else:
            assert converted_by_name[o['name']]['face_uvs']==o['face_uvs'], f"Changed Blender UVs: {o['name']}"
plaques=[o for o in converted['objects'] if o['name'].endswith('| sharp drinks plaque')]
assert len(plaques)==2
assert all(o['image']['dimensions']==[1024,1024] for o in plaques)
manifest=json.loads((ROOT/'assets/playtest-v18/manifest.json').read_text())
for r in manifest['assets']:
    with Image.open(ROOT/'assets/playtest-v18'/f"{r['asset']}.tif") as image:
        assert image.mode=='RGB' and list(image.size)==r['dimensions']
        assert image.width==image.height, r['asset']
    if r['source']:
        assert hashlib.sha256(Path(r['source']).read_bytes()).hexdigest()==r['source_sha256']
sources=json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']
for r in sources:
    assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
maptext=(ROOT/'map_source/zm'/f'{name}.map').read_text()
# Engine entities are brace-delimited; the legacy helper relies on optional
# editor comments and misses newly authored blocks without those comments.
ents=[];depth=0;start=None
for token in re.finditer(r'"(?:\\.|[^"\\])*"|[{}]',maptext):
    if token.group()=='{':
        if depth==0:start=token.start()
        depth+=1
    elif token.group()=='}':
        depth-=1
        if depth==0:ents.append(maptext[start:token.end()])
assert depth==0
triggers=[b for b in ents if kv(b,'targetname')=='zombie_debris']
clips=[b for b in ents if kv(b,'script_noteworthy')=='clip']
assert len(triggers)==5 and len(clips)==4
def brush_bounds(b):
    pts=[tuple(map(float,m)) for m in re.findall(r'\(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)',b)]
    assert pts
    return tuple((min(p[i] for p in pts),max(p[i] for p in pts)) for i in range(3))
for t in triggers:
    assert kv(t,'cursorhint')=='HINT_ACTIVATE'
    org=tuple(map(float,kv(t,'origin').split()))
    tb=brush_bounds(t)
    # Brush plane writer uses six significant digits; tolerate sub-millimetre
    # rounding between its bounds and the six-decimal entity pivot writer.
    assert all(abs(org[i]-(tb[i][0]+tb[i][1])/2)<.02 for i in range(3))
    linked=[c for c in clips if kv(c,'targetname')==kv(t,'target')]
    assert linked
    for c in linked:
        assert kv(c,'DYNAMICPATH')=='1' and kv(c,'spawnflags')=='1'
        cb=brush_bounds(c)
        assert any(tb[i][1]<cb[i][0] or cb[i][1]<tb[i][0] for i in (0,1)), 'Trigger overlaps blocker'
        assert not all(cb[i][0]<=org[i]<=cb[i][1] for i in range(3)), 'Use centre inside blocker'
assert len({kv(t,'target') for t in triggers})==3
assert 'UV calibration' not in maptext
gsc=(ROOT/'usermaps'/name/'scripts/zm'/f'{name}.gsc').read_text()
assert 'EnableInvulnerability' not in gsc and 'round_spawn_func' not in gsc
assert 'add_adjacent_zone( "street_zone", "crossing_zone", "pt18_crossing_open" )' in gsc
crossing=[t for t in triggers if kv(t,'target')=='pt18_crossing_gate']
assert len(crossing)==2 and all(kv(t,'zombie_cost')=='1250' for t in crossing)
assert len([e for e in ents if kv(e,'targetname')=='crossing_zone_spawners' and kv(e,'script_noteworthy')=='riser_location'])==3
buys=[kv(b,'model') for b in ents if kv(b,'classname')=='misc_prefab' and 'spawnable_weapon' in (kv(b,'model') or '')]
assert len(buys)==4
report={'source_photos_hash_identical':len(sources),'square_assets_verified':len(manifest['assets']),
 'triggers_outside_linked_blockers':len(triggers),'linked_clip_brushmodels':len(clips),'wallbuy_prefabs':buys,
 'diagnostic_panels_removed':True,'runtime_texture_purchase_ai_or_coop_verified':False}
out=ROOT/'docs/build-results/playtest-v18/source-checks.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
