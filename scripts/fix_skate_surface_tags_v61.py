"""Correct portable exporter object IDs to packed runtime contact surface tags."""
from pathlib import Path
import struct,zlib,json,hashlib,sys,argparse
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
from analyze_skate import Reader
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source',type=Path,default=ROOT/'build/pharmacie-skate/pharmacie-street-session-demo.skate')
parser.add_argument('--output',type=Path,default=ROOT/'build/pharmacie-skate/pharmacie-street-session-floor-v61.skate')
parser.add_argument('--report',type=Path,default=ROOT/'recon/skate-v60/surface-tag-fix-v61.json')
args=parser.parse_args();SOURCE=args.source.resolve();OUT=args.output.resolve();REPORT=args.report.resolve()
assert OUT.is_relative_to(ROOT) and REPORT.is_relative_to(ROOT),'Outputs must stay in the project'
assert not OUT.exists(),'Refusing to overwrite an existing package'
OUT.parent.mkdir(parents=True,exist_ok=True);REPORT.parent.mkdir(parents=True,exist_ok=True)
blob=SOURCE.read_bytes();r=Reader(blob);assert r.take(8,'magic')==b'SKATE15\0';r.skip(4,'endian');r.string('name');r.skip(196,'environment');counts=struct.unpack('<9I',r.take(36,'counts'));nm,nt,nv,ni,nc=counts[:5]
n=r.u32('material length');mr=Reader(r.stored(n,'material'));tags=[]
for i in range(nm):
 mr.string('material');fields=mr.take(76,'fields');audio,physics,pattern=struct.unpack_from('<3I',fields,64);assert physics<16
 tags.append(audio|(physics<<7)|(pattern<<12));mr.skip(4,'depth');enabled=mr.u32('definition')
 if enabled:
  mr.skip(16,'identity');mr.string('shader');mr.skip(8,'family flags')
  for j in range(mr.u32('bindings')):mr.string('role');mr.skip(16,'binding')
  for j in range(mr.u32('parameters')):
   mr.string('name')
   for k in range(mr.u32('values')):mr.string('value')
  mr.string('source')
def skip_storage(label):
 method=r.u32(label+' method');size=r.u32(label+' size');r.skip(size,label)
for i in range(nt):r.string('texture');r.skip(12,'dimensions');skip_storage('pixels')
skip_storage('vertices');skip_storage('indices');start=r.offset;raw=bytearray(r.stored(nc*48,'collision'));end=r.offset
records=np.ndarray((nc,12),dtype='<u4',buffer=raw);old=records[:,9].copy();materials=records[:,10]
assert materials.min()>=1 and materials.max()<=nm
packed=np.asarray(tags,np.uint32)[materials-1];records[:,9]=packed
hist=np.bincount((old>>7)&31,minlength=32)
payload=zlib.compress(raw,6);OUT.write_bytes(blob[:start]+struct.pack('<II',1,len(payload))+payload+blob[end:])
after=OUT.read_bytes();assert after[:start]==blob[:start] and after[-len(blob[end:]):]==blob[end:]
# Every collision point, native-edge record and material identity is retained.
points=np.ndarray((nc,3,3),dtype='<f4',buffer=raw,strides=(48,12,4))
a,b,c=points[:,0],points[:,1],points[:,2];normal=np.cross(b-a,c-a)
zone=(normal[:,1]>0)&(np.max(points[:,:,1],axis=1)<.2)&(np.min(points[:,:,1],axis=1)>-.25)&(np.max(points[:,:,0],axis=1)>-30)&(np.min(points[:,:,0],axis=1)<55)&(np.max(points[:,:,2],axis=1)>2)&(np.min(points[:,:,2],axis=1)<12)
floor=points[zone];levels=np.round(floor[:,:,1].reshape(-1),5);unique,number=np.unique(levels,return_counts=True)
report={'source':str(SOURCE.relative_to(ROOT)),'output':str(OUT.relative_to(ROOT)),'source_sha256':hashlib.sha256(blob).hexdigest(),'output_sha256':hashlib.sha256(after).hexdigest(),'collision_triangles':nc,'corrected_contact_tags':int(np.sum(old!=packed)),'old_physics_category_histogram':hist.tolist(),'old_out_of_range_category_triangles':int(hist[16:].sum()),'old_false_water_category_triangles':int(hist[12]),'new_contact_tags':np.unique(packed).tolist(),'new_physics_categories':np.unique((packed>>7)&31).tolist(),'starter_street_upward_surface_vertex_heights_metres':dict(zip(map(str,unique.tolist()),number.tolist())),'root_cause':'Upstream Blender exporter surface_id is a sequential object identity. Runtime contact queries consume that field as packed audio/physics/pattern. Object IDs yielded false water categories and histogram indices >=16. Resolve contact tags from authored material channels instead.','preservation':'Visuals, all collision coordinates, topology, materials, textures, ramps and rails unchanged. Only collision contact tags replaced.','runtime_retest':'pending'}
REPORT.write_text(json.dumps(report,indent=2));print('CONTACT_TAG_FIX',report['corrected_contact_tags'],'invalid',report['old_out_of_range_category_triangles'],'false_water',report['old_false_water_category_triangles'])
# Same authored sky/probe data under the new package stem.
for suffix in ('.irradiance',):
 p=SOURCE.with_suffix(suffix)
 if p.exists():OUT.with_suffix(suffix).write_bytes(p.read_bytes())
skies=ROOT/'build/pharmacie-skate/assets/private/native-skies'
for suffix in ('.json','.rgba','.sun.rgba'):
 p=skies/(SOURCE.stem+suffix)
 if p.exists():(skies/(OUT.stem+suffix)).write_bytes(p.read_bytes())
