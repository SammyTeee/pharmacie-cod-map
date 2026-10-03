"""Read-only Blender geometry checks for the neighbouring scenery pass."""
from pathlib import Path
import bpy,bmesh,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.data.scenes['03 Both floors - assembled exterior']
new=[o for o in scene.objects if o.name.startswith('Shop v19 |')]
solid_count=0;quads=0
for o in new:
    if o.type!='MESH':continue
    if len(o.data.polygons)==1:
        assert len(o.data.polygons[0].vertices)==4,o.name
        quads+=1;continue
    bm=bmesh.new();bm.from_mesh(o.data)
    assert all(e.is_manifold for e in bm.edges),f'Open solid: {o.name}'
    assert bm.calc_volume(signed=True)>1e-10,f'Inward/zero-volume solid: {o.name}'
    bm.free();solid_count+=1
anchor=bpy.data.objects['Front | sash recessed glass']
def extent(o):
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    return [max(v[i] for v in pts)-min(v[i] for v in pts) for i in range(3)],min(v.z for v in pts),max(v.z for v in pts)
expected=extent(anchor)
windows=[o for o in new if '| Front | sash recessed glass' in o.name]
assert len(windows)==7
for o in windows:
    actual=extent(o)
    assert all(abs(a-b)<1e-5 for a,b in zip(actual[0],expected[0])) and abs(actual[1]-expected[1])<1e-5 and abs(actual[2]-expected[2])<1e-5,o.name
for name in ('Wreake Valley Flooring','Syston Dry Cleaners','Nail and Spa shop'):
    assert 'Street v17 | '+name+' isolated facade' not in scene.objects
for s in json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']:
    assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
report={'closed_outward_solids':solid_count,'deliberately_flat_display_quads':quads,'pub_size_windows':7,'old_full_facade_planes_unlinked':3,'original_reference_hashes_unchanged':44,'radiant_or_game_verified':False}
(ROOT/'recon/v19/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
