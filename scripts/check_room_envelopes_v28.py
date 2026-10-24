"""Interior enclosure rays using established evaluated mesh BVH; read-only."""
from pathlib import Path
import os,json,bpy
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v28-zombies/pub'
os.environ['PHARMACIE_RECON_PHASE']='after';os.environ['PHARMACIE_RECON_OUTPUT']=str(dest);os.environ['PHARMACIE_RECON_PROBES_ONLY']='1'
try:exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(),str(ROOT/'scripts/recon_blender_players.py'),'exec'))
except SystemExit:pass
results=[]
for level,z in [('ground',0),('upstairs',4.8)]:
    for x in (1,3,5,7,9):
        for y in (2,5,8,11,14,17,20):
            support=ray(floorbvh,floornames,(x,y,z+.3),(0,0,-1),.8)
            if not support:continue
            eye=(x,y,support['point'][2]+1.65)
            # Exclude sample points intersecting furniture/walls.
            close=[ray(bvh,names,eye,d,.15) for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]]
            if any(close):continue
            rays={name:ray(bvh,names,eye,d,60) for name,d in [('floor',(0,0,-1)),('ceiling',(0,0,1)),('east',(1,0,0)),('west',(-1,0,0)),('front',(0,-1,0)),('rear',(0,1,0))]}
            results.append({'level':level,'eye':eye,'rays':rays,'open_directions':[k for k,v in rays.items() if v is None]})
(dest/'room-envelope.json').write_text(json.dumps({'samples':results,'open_rays':sum(len(r['open_directions']) for r in results),'limits':['A mesh hit may be furniture or distant scenery; does not establish room sealing','Intentional doorways/windows can produce open rays','Only axial sparse samples; no full surface coverage or engine collision test']},indent=2))
print('ROOM_ENVELOPE_COMPLETE',len(results),[(r['level'],r['eye'],r['open_directions']) for r in results if r['open_directions']],flush=True)
