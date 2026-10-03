"""Readable enclosed stairs; authored Blender fixtures, BO3 lights still pending."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1];s=bpy.data.scenes['03 Both floors - assembled exterior']
assert not s.get('v18_stair_lighting_added')
c=bpy.data.collections['RECON v18 | Player clearance and finishing']
m=bpy.data.materials.new('Recon v18 | warm stair diffuser');m.use_nodes=True;m.diffuse_color=(.85,.72,.45,1)
bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(.85,.72,.45,1);bs.inputs['Emission Color'].default_value=(1,.8,.52,1);bs.inputs['Emission Strength'].default_value=3
fixtures=[]
for i,(x,y,z,energy) in enumerate([(0,29.75,4.30,90),(4,29.75,4.30,90),(6.6,29.75,8.85,180),(7.7,23.6,8.85,90)]):
    verts=[(x+dx,y+dy,z+dz) for dz in (-.025,.025) for dy in (-.11,.11) for dx in (-.20,.20)]
    me=bpy.data.meshes.new('Stair diffuser');me.from_pydata(verts,[],[tuple(reversed(p)) for p in [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]]);me.materials.append(m)
    o=bpy.data.objects.new('Recon v18 | Stair light fixture '+str(i+1),me);c.objects.link(o)
    data=bpy.data.lights.new('Recon v18 | Stair light '+str(i+1),'AREA');data.energy=energy;data.shape='RECTANGLE';data.size=.6;data.size_y=.3;data.color=(1,.86,.65)
    light=bpy.data.objects.new(data.name,data);c.objects.link(light);light.location=(x,y,z-.06)
    light['bo3_role']='Lighting intent; requires explicit Radiant light placement later'
    o['evidence']='Recon QoL lighting addition, not a surveyed venue fixture';fixtures.append({'position':[x,y,z],'watts_blender':energy})
s['v18_stair_lighting_added']=True
path=ROOT/'recon/v18/changes.json';manifest=json.loads(path.read_text());manifest['changes'].append({'id':'R07','action':'Four warm stair/arrival light fixtures after roof closure exposed poor visibility','fixtures':fixtures,'runtime_verified':False})
manifest['new_meshes']+=4;path.write_text(json.dumps(manifest,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'saved':bpy.data.filepath,'stair_fixtures_added':4}
