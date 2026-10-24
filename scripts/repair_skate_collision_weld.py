"""Canonicalize the exported collision to the runtime's actual 1 mm weld."""
from pathlib import Path
import struct,sys,json,zlib,math,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
import analyze_skate as reader
SOURCE=ROOT/'build/pharmacie-skate/pharmacie-street-session.skate'
OUT=SOURCE.with_name('pharmacie-street-session-runtime.skate');assert not OUT.exists()
capture={};original=reader.Reader.stored
class Captured(Exception):pass
def stored(self,expected,label,*args,**kwargs):
 start=self.offset;data=original(self,expected,label,*args,**kwargs)
 if label=='collision block':
  capture.update(start=start,end=self.offset,data=data);raise Captured()
 return data
reader.Reader.stored=stored
try:reader.analyze_package(SOURCE)
except Captured:pass
assert capture
blob=SOURCE.read_bytes();assert blob[:8]==b'SKATE15\0'
count_offset=16+struct.unpack_from('<I',blob,12)[0]+49*4
count=struct.unpack_from('<I',blob,count_offset+16)[0];assert len(capture['data'])==count*48
raw=np.frombuffer(capture['data'],dtype=np.uint8).reshape(count,48).copy()
points=np.ndarray((count,3,3),dtype='<f4',buffer=raw,strides=(48,12,4))
weld={};removed=[];maximum_shift=0.;inv=1/float(np.float32(.001))
for index,tri in enumerate(points):
 ids=[]
 for corner,p in enumerate(tri):
  key=tuple(math.floor(float(v)*inv+.5) if v>=0 else math.ceil(float(v)*inv-.5) for v in p)
  if key not in weld:weld[key]=(len(weld),p.copy())
  identity,value=weld[key];ids.append(identity);maximum_shift=max(maximum_shift,float(np.linalg.norm(p-value)));tri[corner]=value
 if len(set(ids))<3 or np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))==0:removed.append(index)
keep=np.ones(count,dtype=bool);keep[removed]=False;decoded=raw[keep].tobytes();compressed=zlib.compress(decoded,9)
prefix=bytearray(blob[:capture['start']]);struct.pack_into('<I',prefix,count_offset+16,int(keep.sum()))
OUT.write_bytes(prefix+struct.pack('<II',1,len(compressed))+compressed+blob[capture['end']:])
out=OUT.read_bytes();assert out[-len(blob[capture['end']:]):]==blob[capture['end']:]
# Only the collision count changed before the collision storage record.
check=bytearray(prefix);struct.pack_into('<I',check,count_offset+16,count);assert check==blob[:capture['start']]
report={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(blob).hexdigest(),'output':str(OUT.relative_to(ROOT)),'output_sha256':hashlib.sha256(out).hexdigest(),'collision_before':count,'collision_after':int(keep.sum()),'removed_collapsed_triangle_indices':removed,'maximum_canonical_position_shift_metres':maximum_shift,'visual_material_texture_and_authored_feature_bytes_unchanged':True,'runtime_rule':'The pinned engine uses round(f64(value)/f64(0.001_f32)) and retains the first position in each cell. This converter applies that exact weld before removing collapsed collision triangles.','limits':'Static canonicalization is not runtime skating verification.'}
(ROOT/'recon/skate-v60/collision-weld-repair.json').write_text(json.dumps(report,indent=2));print('WELDED_COLLISION_PACKAGE',count,int(keep.sum()),maximum_shift)
