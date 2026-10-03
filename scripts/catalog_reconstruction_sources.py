"""Record reconstruction references without changing any source image."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STREET = [
    'left of pub front.png',
    'right side of pub front.png',
    'opposite front.png',
    'opposite front further right.png',
    'opposite fornt further left.png',
    'opposite front zoomed out better view flat for texture.png',
    'references/what alley should look lkike - building right pushed up to pharmacie, then the alley way.png',
    'references/down from natty wells to pub.png',
    'references/post office head on.png',
    'references/right of post office.png',
    'references/opposite pub.png',
    'references/shut down flotal sohop opposite pub.png',
    'references/fox and hounds opposite poub rightside of red minimart.png',
    'alt/nattywells/front on natty wells.png',
    'alt/nattywells/natty wells right corner.png',
    'alt/nattywells/natty wells front right.png',
]
USES = [
    'Wreake Valley shop joinery, adjoining pub, alley edge',
    'Dry cleaners, nail/spa frontage, pub-side approach to crossing',
    'Mini Market/Aston/Fox elevation and roof transition',
    'Second overlapping Mini Market/Aston/Fox elevation',
    'Floral Fantasy/Lets Move bays, parking and kerb build-out',
    'Near-frontal Mini Market and adjoining units, parking markings',
    'Alley outside Wreake Valley, deep side wall, terrace attachment',
    'Post Office crossing and whole-street sightline towards junction',
    'Natural Wellbeing access lane, Post Office, Papermoon, Pasha',
    'Post Office/Papermoon/Pasha/Floral elevations and street furniture',
    'Floral/Lets Move/Mini Market/Aston/Fox spatial sequence',
    'Papermoon/Pasha/Floral/Lets Move/Mini Market overlapping sequence',
    'Fox front and corner return, junction, island and signs',
    'Natural Wellbeing gable/front windows/sign/door',
    'Natural Wellbeing deep side wall, access lane and roof',
    'Second Natural Wellbeing corner view, lane without truck obstruction',
]

entries = []

def add(source_id, relative, use, review, previous_hash=None):
    path = ROOT / relative
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    with Image.open(path) as im:
        dimensions = list(im.size)
        image_format = im.format
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    assert before == after, f'Source changed while inspecting: {relative}'
    entries.append({
        'id': source_id, 'path': relative, 'dimensions': dimensions,
        'format': image_format, 'sha256': before, 'review': review,
        'use': use, 'source_unchanged_during_catalog': True,
        'matches_existing_catalog': before == previous_hash if previous_hash else None,
    })

for i, (relative, use) in enumerate(zip(STREET, USES), 1):
    add(f'S{i:02}', relative, use, 'Full image visually inspected in this review')

old = json.loads((ROOT / 'assets/blender/photo-review/catalog.json').read_text())
full = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 17, 19, 20, 21, 22, 25, 26, 28}
for item in old:
    source_id = f'P{item["id"]:02}'
    if item['id'] == 12:
        review = 'Existing same-size lossless PNG visually inspected; source catalogued unchanged'
    elif item['id'] in full:
        review = 'Full image and existing numbered contact sheet visually inspected'
    elif item['id'] in {16, 18}:
        review = 'Drawing on existing contact sheet; not photographic building evidence'
    else:
        review = 'Existing numbered contact sheet visually inspected; alternate/duplicate view'
    add(source_id, 'references/pharmacie-syston/' + item['source'],
        'See PUB_PHOTO_RECONSTRUCTION.md source ledger and STREET_PHOTO_RECONSTRUCTION.md',
        review, item['sha256'])

out = ROOT / 'docs/reconstruction-sources.json'
out.write_text(json.dumps({
    'review_date': '2026-10-03',
    'purpose': 'Source identity and visual-review coverage for text reconstruction notes',
    'units': 'Image dimensions in pixels; no world dimensions inferred',
    'sources': entries,
}, indent=2) + '\n', encoding='utf-8')

lines = ['# Reconstruction source index', '',
         'Stable IDs used by STREET_PHOTO_RECONSTRUCTION.md and PUB_PHOTO_RECONSTRUCTION.md.', '',
         'Original filenames and bytes are preserved. Dimensions below are pixels, not survey measurements.', '',
         '| ID | Original image | Dimensions | Review coverage / use |',
         '|---|---|---|---|']
for e in entries:
    link = f'[{Path(e["path"]).name}](<../{e["path"]}>)'
    lines.append(f'| {e["id"]} | {link} | {e["dimensions"][0]}×{e["dimensions"][1]} | {e["review"]}; {e["use"]} |')
lines += ['', 'Full SHA256 values and previous-catalog comparisons: [reconstruction-sources.json](reconstruction-sources.json).', '']
(ROOT / 'docs/RECONSTRUCTION_SOURCE_INDEX.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'sources': len(entries), 'street': len(STREET),
                  'previous_catalog_mismatches': [e['id'] for e in entries if e['matches_existing_catalog'] is False],
                  'catalog': str(out)}))
