"""Check retained pub geometry, adjacency, alley and all reference hashes."""
from pathlib import Path
import bpy,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def snapshot(scene):
    bpy.context.window.scene=scene;bpy.context.view_layer.update()
    return {o.name:{'vertices':[[round(v,6) for v in o.matrix_world@p.co] for p in o.data.vertices],'faces':[list(p.vertices) for p in o.data.polygons]} for o in scene.objects if o.type=='MESH'}
current=snapshot(bpy.data.scenes['03 Both floors - assembled exterior'])
assert 'Street | left side passage' not in current
threshold='Front | continuous entrance threshold - no floor gap'
assert threshold in current
manifest=json.loads((ROOT/'assets/blender/street-rebuilt-v17-manifest.json').read_text())
buildings={b['name']:b for b in manifest['buildings']}
assert buildings['Wreake Valley Flooring']['x'][1]==-2.16
assert buildings['Syston Dry Cleaners']['x'][0]==10.50
assert abs(manifest['alley']['x'][1]-manifest['alley']['x'][0]-2.58)<1e-6
assert manifest['alley']['x'][1]==buildings['Wreake Valley Flooring']['x'][0]
assert buildings['Wreake Valley Flooring']['y'][1]<manifest['alley']['rear_connector_y'][0]
assert buildings['Post Office']['x'][1]==45 and buildings['Natural Wellbeing']['x'][0]==48
source_records=json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']
for r in source_records:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-entrance-fixed-v16.blend'))
scene=bpy.data.scenes['03 Both floors - assembled exterior'];before=snapshot(scene)
street_names={o.name for c in bpy.data.collections if c.name.startswith('STREET |') for o in c.all_objects}
protected={n:data for n,data in before.items() if n not in street_names and n!='Street | left side passage'}
protected[threshold]=before[threshold]
for name,data in protected.items():assert current.get(name)==data,'Pub geometry altered or missing: '+name
report={'pub_meshes_identical':len(protected),'reference_hashes_identical':len(source_records),'threshold_identical':True,'old_passage_absent':True,'neighbours_attached_at_nominal_front_edges':True,'outer_alley_width_m':2.58,'lane_between_postoffice_wellbeing_m':3,'radiant_or_runtime_checked':False}
(ROOT/'build/street-v17-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
