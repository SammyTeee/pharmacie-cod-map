from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for name,link in [('README.md','docs/ENCLOSURE_DETAIL_V33.md'),
                  ('AGENTS.md','docs/ENCLOSURE_DETAIL_V33.md'),
                  ('assets/blender/README.md','../../docs/ENCLOSURE_DETAIL_V33.md'),
                  ('MODDING_PLAN.md','docs/ENCLOSURE_DETAIL_V33.md')]:
    path=ROOT/name;content=path.read_text(encoding='utf-8')
    prefix=f'''[Latest enclosure fixes, service-lane detail and player-height fly-through]({link}).

Latest Blender checkpoint: `assets/blender/pharmacie-enclosure-detail-v33.blend`.
Closes ground/upstairs seams and diagonal ceiling escapes; enclosed service lane,
rear threshold details and readable closure signs. V32 street, v30 rear loop and
approved pub/Taraj placement retained. Blender-only; engine package unchanged.
Saved route and visibility rays are not BO3 collision, navigation or co-op tests.
Older latest/checkpoint statements below are historical.

'''
    if not content.startswith(prefix):path.write_text(prefix+content,encoding='utf-8')
path=ROOT/'scripts/open-blender.ps1'
path.write_text(path.read_text().replace('pharmacie-street-frontages-v32.blend','pharmacie-enclosure-detail-v33.blend'))
print('V33_NOTES_UPDATED')
