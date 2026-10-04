from pathlib import Path
import bpy,bmesh,json,math
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];assert Path(bpy.data.filepath).name=='pharmacie-retail-detail-v39.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene;bpy.context.view_layer.update()
coll=bpy.data.collections['STREET v39 | Florist jeweller optician bakery and charity displays'];made=[];basis=Matrix.Identity(4)
helpers=(ROOT/'scripts/detail_street_v37.py').read_text();helpers=helpers[helpers.index('F=['):helpers.index('# Retain the shelter position')].replace('Street v37 |','Street v39 |');exec(compile(helpers,'support_helpers','exec'))
for cid in ('B002',):
 w=frontage(cid);rest=w-1.65;bayw=max(.8,(rest-.35)/2)
 for bay in range(2):
  x=-w/2+1.6+(bay+.5)*rest/2
  box('carpet swatch ledge',x-bayw*.40,x+bayw*.40,-.26,-.13,1.855,1.90,bpy.data.materials['Street v36 | weathered bench timber'])
p=ROOT/'recon/v39/changes.json';changes=json.loads(p.read_text());changes['new_solids']+=[o.name for o in made];p.write_text(json.dumps(changes,indent=2))
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);print('V39_SUPPORTS',len(made),flush=True)
