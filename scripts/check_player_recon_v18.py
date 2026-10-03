"""Measure completed recon, original preservation, and new solid mesh winding."""
from pathlib import Path
import bpy,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'recon/v18'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene;bpy.context.view_layer.update()
def snap(s):
    return {o.name:{'vertices':[[round(v,6) for v in o.matrix_world@p.co] for p in o.data.vertices],'faces':[list(p.vertices) for p in o.data.polygons]} for o in s.objects if o.type=='MESH'}
current=snap(scene);new=[o for o in scene.objects if o.type=='MESH' and o.name.startswith('Recon v18 |')]
for o in new:
    edges=collections.Counter(tuple(sorted((p.vertices[i],p.vertices[(i+1)%len(p.vertices)]))) for p in o.data.polygons for i in range(len(p.vertices)))
    assert all(count==2 for count in edges.values()),'Open solid: '+o.name
    o.data.calc_loop_triangles();volume=sum(o.data.vertices[t.vertices[0]].co.dot(o.data.vertices[t.vertices[1]].co.cross(o.data.vertices[t.vertices[2]].co))/6 for t in o.data.loop_triangles)
    assert volume>0,'Inward or degenerate solid: '+o.name
views=json.loads((R/'after/view-probes.json').read_text())['views']
routes=json.loads((R/'after/route-probes.json').read_text())['samples']
assert all(v['support'] and not v['body_clearance_hits'] and not v['headroom_hit'] for v in views)
assert all(p['floor_object'] and not p['blockers'] and not p['overhead'] for p in routes)
for phase in ('before','after'):assert len(list((R/phase).glob('[0-9][0-9]_*.png')))==36
changes=json.loads((R/'changes.json').read_text())
changed={n for c in changes['changes'] if c['id']=='R01' for n in c['objects']}
changed.add('Street v17 | Alley rear route connector')
changed.add('First | female WC bottom | wall end')
wide=json.loads((R/'sensitivity-radius-042/route-probes.json').read_text())['samples']
assert all(p['floor_object'] and not p['blockers'] and not p['overhead'] for p in wide)
sources=json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']
for r in sources:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
# Every pre-existing mesh except deliberate chair/floor/stair edits must retain
# its exact world vertices and polygon indices. UV corrections don't change shape.
bpy.ops.wm.open_mainfile(filepath=str(R/'input-live-v17.blend'));before_scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=before_scene;bpy.context.view_layer.update();before=snap(before_scene)
removed={n for n in before if (n.startswith('Stairs |') and 'tread' in n) or (n.startswith('Video | Stairs |') and 'metal nosing' in n)}
retired_guides={n for n in before if n.startswith('CLEARANCE |')}
protected={n:d for n,d in before.items() if n not in changed|removed|retired_guides}
for n,d in protected.items():assert current.get(n)==d,'Unplanned geometry change: '+n
report={'source_photos_hash_identical':len(sources),'protected_meshes_identical':len(protected),'intentional_moved_or_changed_meshes':len(changed),'archived_stair_meshes':len(removed),'retired_planning_guides':sorted(retired_guides),'new_closed_outward_meshes':len(new),'player_views_each_phase':36,'screenshots':72,'route_samples':len(routes),'wider_radius_sensitivity_samples':len(wide),'wider_radius_m':.42,'route_blockers_after':0,'unsupported_route_samples_after':0,'invalid_inspection_cameras_after':0,'zombies_plan':'21 Empty anchors / 3 proposed zones; no game entities','radiant_or_runtime_verified':False}
(R/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
