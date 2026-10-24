"""One flat riding plane; shallow road dressing remains visible but non-colliding."""
from pathlib import Path
import sys,struct,zlib,json,hashlib,argparse
import numpy as np
from shapely.geometry import Polygon,box as rectangle
from shapely import constrained_delaunay_triangles
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
from analyze_skate import Reader
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source',type=Path,default=ROOT/'build/pharmacie-skate/pharmacie-street-session-floor-v61.skate')
parser.add_argument('--output',type=Path,default=ROOT/'build/pharmacie-skate/pharmacie-street-session-floor-v62-r3.skate')
parser.add_argument('--report',type=Path,default=ROOT/'recon/skate-v60/flat-floor-v62.json')
args=parser.parse_args();SOURCE=args.source.resolve();OUT=args.output.resolve();REPORT=args.report.resolve()
assert OUT.is_relative_to(ROOT) and REPORT.is_relative_to(ROOT),'Outputs must stay in the project'
assert not OUT.exists(),'Refusing to overwrite an existing package'
OUT.parent.mkdir(parents=True,exist_ok=True);REPORT.parent.mkdir(parents=True,exist_ok=True)
blob=SOURCE.read_bytes();r=Reader(blob);r.skip(12,'header');r.string('name');r.skip(196,'environment');countoff=r.offset;nm,nt,nv,ni,nc,*_=struct.unpack('<9I',r.take(36,'counts'))
n=r.u32('material length');mr=Reader(r.stored(n,'material'));names=[]
for i in range(nm):
 names.append(mr.string('material'));mr.skip(80,'fields/depth');enabled=mr.u32('definition')
 if enabled:
  mr.skip(16,'identity');mr.string('shader');mr.skip(8,'family flags')
  for j in range(mr.u32('bindings')):mr.string('role');mr.skip(16,'binding')
  for j in range(mr.u32('parameters')):
   mr.string('parameter')
   for k in range(mr.u32('values')):mr.string('value')
  mr.string('source')
def skip_storage():r.u32('method');size=r.u32('size');r.skip(size,'payload')
for i in range(nt):r.string('texture');r.skip(12,'dimensions');skip_storage()
skip_storage();skip_storage();start=r.offset;raw=r.stored(nc*48,'collision');end=r.offset
records=np.frombuffer(raw,np.uint8).reshape(nc,48);points=np.ndarray((nc,3,3),dtype='<f4',buffer=raw,strides=(48,12,4));fields=np.frombuffer(raw,'<u4').reshape(nc,12)
sc=1.0640686466;h=-.08/sc;lo=np.min(points,axis=1);hi=np.max(points,axis=1)
inside=(lo[:,0]>=-34/sc-.003)&(hi[:,0]<=66/sc+.003)&(lo[:,2]>=3/sc-.003)&(hi[:,2]<=10.4/sc+.003)
normal=np.cross(points[:,1]-points[:,0],points[:,2]-points[:,0]);flat=(normal[:,1]>0)&(np.abs(normal[:,0])+np.abs(normal[:,2])<np.maximum(normal[:,1],1e-8)*1e-5)
old_base=inside&flat&(np.abs(lo[:,1]-h)<.002)&(np.abs(hi[:,1]-h)<.002)
decor_mats=[i+1 for i,name in enumerate(names) if any(t in name.lower() for t in ('road white','worn double yellow','repaired asphalt','tar seams','drain dark','v32 utility metal','road paint'))]
protected_skate=[i+1 for i,name in enumerate(names) if 'Skate v60 |' in name]
dressing=inside&~np.isin(fields[:,10],protected_skate)&(lo[:,1]>h-.07)&(hi[:,1]<h+.04)
remove=old_base|dressing;assert old_base.sum()>=2
overlap=(hi[:,0]>-34/sc)&(lo[:,0]<66/sc)&(hi[:,2]>3/sc)&(lo[:,2]<10.4/sc)
partial=overlap&~inside&flat&~np.isin(fields[:,10],protected_skate)&(lo[:,1]>h-.002)&(hi[:,1]<h+.04)
outside=[];cut=rectangle(-34/sc,3/sc,66/sc,10.4/sc)
for index in np.flatnonzero(partial):
 poly=Polygon([(float(p[0]),float(p[2])) for p in points[index]])
 if not poly.intersects(cut):continue
 remainder=poly.difference(cut);remove[index]=True
 if remainder.is_empty:continue
 for piece in constrained_delaunay_triangles(remainder).geoms:
  coords=list(piece.exterior.coords)[:3];tri=[(x,float(points[index,0,1]),z) for x,z in coords]
  if np.cross(np.subtract(tri[1],tri[0]),np.subtract(tri[2],tri[0]))[1]<0:tri[1],tri[2]=tri[2],tri[1]
  tri=np.asarray(tri,dtype='<f4')
  scaled=tri.astype(np.float64)/float(np.float32(.001))
  keys=(np.sign(scaled)*np.floor(np.abs(scaled)+.5)).astype(np.int64)
  cross=np.cross(tri[1]-tri[0],tri[2]-tri[0])
  if len(set(map(tuple,keys)))<3 or float(cross@cross)<=1e-10:continue
  data=bytearray(records[index].tobytes());struct.pack_into('<9f',data,0,*tri.flatten());outside.append(data)
asphalt=next(i+1 for i,name in enumerate(names) if name.endswith('Street v36 | aged asphalt Street v17 | asphalt'))
template=bytearray(records[np.flatnonzero(old_base)[0]].tobytes());struct.pack_into('<II',template,36,131,asphalt)
a=(-34/sc,h,3/sc);b=(-34/sc,h,10.4/sc);c=(66/sc,h,10.4/sc);d=(66/sc,h,3/sc)
added=[]
for tri in ((a,b,c),(a,c,d)):
 data=bytearray(template);struct.pack_into('<9f',data,0,*[v for p in tri for v in p]);added.append(data)
decoded=records[~remove].tobytes()+b''.join(outside)+b''.join(added);prefix=bytearray(blob[:start]);struct.pack_into('<I',prefix,countoff+16,len(decoded)//48);payload=zlib.compress(decoded,6)
# Dense support samples across the clear street, avoiding intended obstacles/aprons.
obstacles=[(-6.5,-2.8,-9,-6.5),(-20.2,-11.8,-9.8,-8.5),(11.2,20,-8.1,-7.5),(28.8,37.2,-9,-6.2),(-26.2,-22.1,-8.5,-5.1),(4.3,6.7,-4,-2.9),(39,41,-4,-2.9)]
def levels(data):
 p=np.ndarray((len(data)//48,3,3),dtype='<f4',buffer=data,strides=(48,12,4));norm=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]);sel=(norm[:,1]>0)&(p[:,:,1].max(axis=1)<.3)&(p[:,:,1].min(axis=1)>-.4)&(p[:,:,0].max(axis=1)>-32)&(p[:,:,0].min(axis=1)<50)&(p[:,:,2].max(axis=1)>3)&(p[:,:,2].min(axis=1)<11)
 mf=np.frombuffer(data,'<u4').reshape(-1,12)[sel,10];p=p[sel];a,b,c=p[:,0],p[:,1],p[:,2];det=(b[:,2]-c[:,2])*(a[:,0]-c[:,0])+(c[:,0]-b[:,0])*(a[:,2]-c[:,2]);valid=np.abs(det)>1e-10;det=np.where(valid,det,1);results=[];diagnostics=0
 for x in np.arange(-30,48,.5):
  for y in np.arange(-9.3,-3.9,.45):
   if any(x0<=x<=x1 and y0<=y<=y1 for x0,x1,y0,y1 in obstacles):continue
   xx,zz=x/sc,-y/sc;u=((b[:,2]-c[:,2])*(xx-c[:,0])+(c[:,0]-b[:,0])*(zz-c[:,2]))/det;v=((c[:,2]-a[:,2])*(xx-c[:,0])+(a[:,0]-c[:,0])*(zz-c[:,2]))/det;w=1-u-v;hit=valid&(u>=-1e-5)&(v>=-1e-5)&(w>=-1e-5)
   heights=u*a[:,1]+v*b[:,1]+w*c[:,1]
   assert hit.any(),(x,y)
   results.append(float(heights[hit].max()))
   if results[-1]>h+.001 and diagnostics<3:
    index=np.where(hit,heights,-100).argmax();print('RAISED_FLOOR_SAMPLE',x,y,names[int(mf[index])-1],p[index].tolist(),flush=True);diagnostics+=1
 return results
before=levels(raw);after=levels(decoded);assert max(abs(v-h) for v in after)<.001,(min(after),max(after),h)
OUT.write_bytes(prefix+struct.pack('<II',1,len(payload))+payload+blob[end:])
report={'source':str(SOURCE.relative_to(ROOT)),'output':str(OUT.relative_to(ROOT)),'output_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'removed_old_base_triangles':int(old_base.sum()),'removed_shallow_dressing_triangles':int(dressing.sum()),'clipped_partial_overlap_triangles':int(partial.sum()),'retained_outside_fragments':len(outside),'new_riding_triangles':2,'floor_height_metres':h,'dense_clear_street_support_samples':len(after),'before_height_range_metres':[min(before),max(before)],'after_height_range_metres':[min(after),max(after)],'source_bounds_BU':[-34,66,-10.4,-3],'preserved':'Visual vertex/index/material/texture blocks and all authored rail records unchanged; ramp and kerb geometry retained. Original/neutral Blender files unchanged.','runtime_test':'pending'}
REPORT.write_text(json.dumps(report,indent=2));print('FLAT_STREET',report)
for suffix in ('.irradiance',):
 p=SOURCE.with_suffix(suffix)
 if p.exists():OUT.with_suffix(suffix).write_bytes(p.read_bytes())
skies=ROOT/'build/pharmacie-skate/assets/private/native-skies'
for suffix in ('.json','.rgba','.sun.rgba'):
 p=skies/(SOURCE.stem+suffix)
 if p.exists():(skies/(OUT.stem+suffix)).write_bytes(p.read_bytes())
