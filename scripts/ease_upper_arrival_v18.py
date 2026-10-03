"""Remove a stair-arrival corner snag detected with the larger player envelope."""
from pathlib import Path
import bpy,json,shutil
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'recon/v18';s=bpy.context.scene
assert not s.get('v18_upper_arrival_eased')
prior=R/'sensitivity-radius-042';saved=R/'sensitivity-radius-042-before-arrival-fix'
saved.mkdir(exist_ok=True)
for filename in ('view-probes.json','route-probes.json'):shutil.copy2(prior/filename,saved/filename)
o=bpy.data.objects['First | female WC bottom | wall end'];world=o.matrix_world.copy();inverse=world.inverted()
points=[world@v.co for v in o.data.vertices];y0=min(p.y for p in points);y1=max(p.y for p in points)
before=[list(p) for p in points]
for v,p in zip(o.data.vertices,points):
    p.x-=.20*(p.y-y0)/(y1-y0);v.co=inverse@p
o.data.update();o['recon_fix']='Taper rear end 20cm left to ease stair-arrival corner; front junction and solid partition retained'
s['v18_upper_arrival_eased']=True
path=R/'changes.json';manifest=json.loads(path.read_text());manifest['changes'].append({'id':'R08','action':'Ease upper stair-arrival corner by tapering female WC outer wall rear end 20cm; no connecting door or divider removal','object':o.name,'before_world_vertices':before,'radius_probe_m':.42,'design':'Gameplay clearance adaptation, not surveyed venue dimension'});path.write_text(json.dumps(manifest,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'saved':bpy.data.filepath,'upper_arrival_corner_eased_m':.20}
