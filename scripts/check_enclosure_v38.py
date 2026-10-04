from pathlib import Path
import bpy,json,os
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v38'
os.environ.update(PHARMACIE_RECON_PHASE='after',PHARMACIE_RECON_OUTPUT=str(dest/'enclosure-checks'),PHARMACIE_RECON_PROBES_ONLY='1',PHARMACIE_RECON_RADIUS='.42')
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),'enclosure_bvh','exec'))
except SystemExit:pass
anchor=bpy.data.objects['Street v38 | B031 | passage floor'];basis=anchor.matrix_world;tests=[]
for y in (1.6,3.7,6.1):
 for x in (-.75,0,.75):
  origin=basis@Vector((x,y,1.5))
  for label,direction,expected,limit in [('floor',(0,0,-1),('passage floor',),2),('ceiling',(0,0,1),('continuous passage ceiling','bulkhead'),2),('left',(-1,0,0),('passage side wall',),3),('right',(1,0,0),('passage side wall',),3)]:
   hit=ray(bvh,names,origin,basis.to_3x3()@Vector(direction),limit);tests.append(dict(label=label,local=[x,y,1.5],hit=hit,pass_check=bool(hit and any(part in hit['object'] for part in expected))))
hit=ray(bvh,names,basis@Vector((0,6.1,1.5)),basis.to_3x3()@Vector((0,1,0)),1);tests.append(dict(label='closed rear',hit=hit,pass_check=bool(hit and 'gate' in hit['object'])))
fails=[t for t in tests if not t['pass_check']];(dest/'enclosure-validation.json').write_text(json.dumps(dict(tests=tests,failures=fails,limits='Sampled enclosure rays; entrance intentionally open. Not a watertightness or engine collision certificate.'),indent=2));assert not fails,fails
print('V38_ENCLOSURE_PASS',len(tests),flush=True)
