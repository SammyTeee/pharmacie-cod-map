"""Translate the full custom world to put Holmdale at the render origin."""
from pathlib import Path
import hashlib,json,struct,sys,zlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
from analyze_skate import Reader
SOURCE=ROOT/'build/pharmacie-skate/pharmacie-holmdale-29-v63.skate';OUT=SOURCE.with_name('pharmacie-holmdale-29-v64.skate');assert not OUT.exists()
blob=SOURCE.read_bytes();r=Reader(blob);r.skip(12,'header');r.string('name');spawnoff=r.offset
spawn=np.array(struct.unpack('<3f',blob[spawnoff:spawnoff+12]),np.float32);offset=spawn.copy();offset[1]=0
r.skip(196,'environment');countoff=r.offset;counts=struct.unpack('<9I',r.take(36,'counts'));assert counts[6]==0 and counts[8]==0
def skip_storage():r.u32('method');r.skip(r.u32('size'),'payload')
r.u32('material length');skip_storage()
for _ in range(counts[1]):r.string('texture');r.skip(12,'dimensions');skip_storage()
vertex_start=r.offset;vertices=bytearray(r.stored(counts[2]*56,'vertices'));vertex_end=r.offset
skip_storage();collision_start=r.offset;collision=bytearray(r.stored(counts[4]*48,'collision'));collision_end=r.offset
v=np.ndarray((counts[2],3),dtype='<f4',buffer=vertices,strides=(56,4));v-=offset
p=np.ndarray((counts[4],3,3),dtype='<f4',buffer=collision,strides=(48,12,4));p-=offset
# Reapply the exact runtime weld after moving the grid origin.
records=np.frombuffer(collision,np.uint8).reshape(-1,48);keep=[];weld={};step=float(np.float32(.001))
for i,tri in enumerate(p):
    for point in tri:
        scaled=point.astype(np.float64)/step;key=tuple((np.sign(scaled)*np.floor(abs(scaled)+.5)).astype(np.int64))
        canonical=weld.setdefault(key,point.copy());point[:]=canonical
    cross=np.cross(tri[1]-tri[0],tri[2]-tri[0])
    if float(cross@cross)>1e-10:keep.append(i)
collision=records[keep].tobytes()
tail=bytearray(blob[collision_end:]);tr=Reader(tail)
for _ in range(counts[5]):
    tr.string('rail');tr.u32('closed');assert tr.u32('representation')==0
    number=tr.u32('points');pos=tr.offset
    rp=np.ndarray((number,3),dtype='<f4',buffer=tail,offset=pos);rp-=offset;tr.skip(number*12,'points')
for _ in range(counts[7]):
    tr.string('light');tr.u32('kind');pos=tr.offset
    lp=np.ndarray((3,),dtype='<f4',buffer=tail,offset=pos);lp-=offset;tr.skip(56,'light fields')
for _ in range(tr.u32('extensions')):
    tag=tr.take(4,'tag');schema=tr.u32('schema');length=tr.u32('length');data=tr.stored(length,'extension')
    assert tag==b'BMAT' or (tag==b'WCFG' and data in (b'\0\0\0\0',b'\1\0\0\0')) or (tag==b'MOBJ' and data==b'\0\0\0\0'),'Review world-space extension before rebasing'
assert tr.offset==len(tail)
def stored(data):payload=zlib.compress(data,6);return struct.pack('<II',1,len(payload))+payload
prefix=bytearray(blob[:vertex_start]);struct.pack_into('<3f',prefix,spawnoff,*(spawn-offset));struct.pack_into('<I',prefix,countoff+16,len(keep))
OUT.write_bytes(prefix+stored(vertices)+blob[vertex_end:collision_start]+stored(collision)+tail)
probe=bytearray(SOURCE.with_suffix('.irradiance').read_bytes());n=struct.unpack_from('<I',probe,8)[0]
for i in range(n):
    pos=12+i*160+144;xyz=np.array(struct.unpack_from('<3f',probe,pos),np.float32)-offset;struct.pack_into('<3f',probe,pos,*xyz)
OUT.with_suffix('.irradiance').write_bytes(probe)
skies=ROOT/'build/pharmacie-skate/assets/private/native-skies'
for suffix in ('.json','.rgba','.sun.rgba'):
    path=skies/(SOURCE.stem+suffix)
    if path.exists():(skies/(OUT.stem+suffix)).write_bytes(path.read_bytes())
OUT.with_suffix('.audio.json').write_bytes(SOURCE.with_suffix('.audio.json').read_bytes())
report={'source':str(SOURCE.relative_to(ROOT)),'output':str(OUT.relative_to(ROOT)),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'runtime_translation_offset_metres':offset.tolist(),'spawn_metres':(spawn-offset).tolist(),
        'removed_rebased_weld_degenerate_triangles':counts[4]-len(keep),'collision_triangles':len(keep),
        'scope':'Entire map translated together: visuals, collision, grind paths, spawn and lighting probes. Materials, UVs and layout retained. Blender unchanged.',
        'runtime_validation':'pending'}
(ROOT/'recon/skate-v60/holmdale-rebase-v64.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
