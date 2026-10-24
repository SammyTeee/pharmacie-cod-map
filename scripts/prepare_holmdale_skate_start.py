"""Start beside number 29; preserve all repaired street geometry and systems."""
from pathlib import Path
import hashlib,json,math,struct,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
from analyze_skate import Reader
SOURCE=ROOT/'build/pharmacie-skate/pharmacie-street-session-floor-v62-r3.skate'
OUT=SOURCE.with_name('pharmacie-holmdale-29-v63.skate');assert not OUT.exists()
blob=SOURCE.read_bytes();r=Reader(blob);r.skip(12,'header');r.string('name');spawnoff=r.offset;r.skip(196,'environment');counts=struct.unpack('<9I',r.take(36,'counts'))
def skip_storage():r.u32('method');r.skip(r.u32('size'),'payload')
r.u32('material decoded length');skip_storage()
for _ in range(counts[1]):r.string('texture');r.skip(12,'dimensions');skip_storage()
skip_storage();skip_storage();raw=r.stored(counts[4]*48,'collision')
p=np.ndarray((counts[4],3,3),dtype='<f4',buffer=raw,strides=(48,12,4))
normal=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]);p=p[(normal[:,1]>0)&(p[:,:,1].max(axis=1)<1.)]
a,b,c=p[:,0],p[:,1],p[:,2];det=(b[:,2]-c[:,2])*(a[:,0]-c[:,0])+(c[:,0]-b[:,0])*(a[:,2]-c[:,2]);valid=np.abs(det)>1e-9;det=np.where(valid,det,1)
scale=1.0640686466
# Actual matrix queried read-only from the v60 Blender file; local frontage point.
xBU,yBU=-161.10289001464844,813.5018920898438
x,z=xBU/scale,-yBU/scale+.75 # Clear the driveway/road height transition.
def support(x,z):
    u=((b[:,2]-c[:,2])*(x-c[:,0])+(c[:,0]-b[:,0])*(z-c[:,2]))/det
    v=((c[:,2]-a[:,2])*(x-c[:,0])+(a[:,0]-c[:,0])*(z-c[:,2]))/det;w=1-u-v
    hit=valid&(u>=-1e-5)&(v>=-1e-5)&(w>=-1e-5);assert hit.any(),'Holmdale spawn lacks collision support'
    return float((u*a[:,1]+v*b[:,1]+w*c[:,1])[hit].max())
samples=[support(x+dx,z+dz) for dx in (-.35,0,.35) for dz in (-.35,0,.35)]
assert max(samples)-min(samples)<.025,('Spawn patch is uneven',samples)
floor=support(x,z);spawn=[x,floor+.2631409277,z]
# Face the house, along the assembly's positive local Y axis.
heading=math.atan2(.27957397699,.96012401581)
changed=bytearray(blob);struct.pack_into('<4f',changed,spawnoff,*spawn,heading)
assert changed[:spawnoff]==blob[:spawnoff] and changed[spawnoff+16:]==blob[spawnoff+16:]
OUT.write_bytes(changed)
for suffix in ('.irradiance',):
    path=SOURCE.with_suffix(suffix)
    if path.exists():OUT.with_suffix(suffix).write_bytes(path.read_bytes())
skies=ROOT/'build/pharmacie-skate/assets/private/native-skies'
for suffix in ('.json','.rgba','.sun.rgba'):
    path=skies/(SOURCE.stem+suffix)
    if path.exists():(skies/(OUT.stem+suffix)).write_bytes(path.read_bytes())
OUT.with_suffix('.audio.json').write_text(json.dumps({'ems':[],'fallback_bed':'02_dt_less_busy'},indent=2))
report={'output':str(OUT.relative_to(ROOT)),'sha256':hashlib.sha256(changed).hexdigest(),
        'spawn_metres':spawn,'heading_radians':heading,'Blender_frontage_point_BU':[xBU,yBU],
        'support_patch_metres':samples,'floor_metres':floor,'all_nonspawn_package_bytes_unchanged':True,
        'runtime_capture':'pending','location':'Front of approved number 29 Holmdale assembly; approximate surveyed placement'}
(ROOT/'recon/skate-v60/holmdale-start-v63.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
