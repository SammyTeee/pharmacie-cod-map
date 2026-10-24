"""Authored orientation lightmap and character daylight for our custom world."""
from pathlib import Path
import sys,struct,zlib,json,hashlib,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
import analyze_skate as A
SOURCE=ROOT/'build/pharmacie-skate/pharmacie-street-session-playable.skate';OUT=SOURCE.with_name('pharmacie-street-session-demo.skate');assert not OUT.exists()
blob=SOURCE.read_bytes();r=A.Reader(blob);r.skip(12,'magic/endian');name=r.string('map');r.skip(196,'metadata');countoff=r.offset;counts=struct.unpack('<9I',r.take(36,'counts'));nm,nt,nv=counts[:3]
mat_start=r.offset;matlen=r.u32('material size');matdata=bytearray(r.stored(matlen,'material'));tex_start=r.offset;payloads=[]
for i in range(nt):
 r.string('texture');w,h,cs=struct.unpack('<3I',r.take(12,'dimensions'));payloads.append(r.stored(w*h*4,'texture',payloads))
tex_end=r.offset;vertex_start=r.offset;vertices=bytearray(r.stored(nv*56,'vertices'));vertex_end=r.offset
mr=A.Reader(matdata)
for i in range(nm):
 mr.string('material');fieldoff=mr.offset;mr.skip(80,'fields/depth');enabled=mr.u32('definition');assert enabled
 mr.skip(16,'identity');mr.string('shader');mr.skip(8,'family/flags')
 for j in range(mr.u32('bindings')):mr.string('role');mr.skip(16,'binding')
 for j in range(mr.u32('parameters')):
  mr.string('parameter')
  for k in range(mr.u32('values')):mr.string('value')
 mr.string('source');struct.pack_into('<I',matdata,fieldoff+36,nt+1)
assert mr.offset==len(matdata)
normals=np.ndarray((nv,3),dtype='<f4',buffer=vertices,offset=12,strides=(56,4));uv=np.ndarray((nv,2),dtype='<f4',buffer=vertices,offset=32,strides=(56,4))
sun=np.array((.48,.80,.36),np.float32);sun/=np.linalg.norm(sun)
shade=np.clip(normals@sun,0,1);uv[:,0]=.01+.98*shade;uv[:,1]=.5
brightness=np.sqrt(.42+.50*np.linspace(0,1,256));rgba=np.zeros((4,256,4),np.uint8);rgba[:,:,:3]=np.uint8(brightness[None,:,None]*255);rgba[:,:,3]=255
def string(s):b=s.encode();return struct.pack('<I',len(b))+b
def stored(b):c=zlib.compress(b,6);return struct.pack('<II',1,len(c))+c
texture=string('Original Syston daylight orientation ramp')+struct.pack('<3I',256,4,0)+stored(rgba.tobytes())
prefix=bytearray(blob[:mat_start]);struct.pack_into('<I',prefix,countoff+4,nt+1)
out=prefix+struct.pack('<I',len(matdata))+stored(matdata)+blob[tex_start:tex_end]+texture+stored(vertices)+blob[vertex_end:];OUT.write_bytes(out)
# Position, normal, albedo UV, index, collision and all authored feature data retained.
src=A.Reader(blob);src.offset=vertex_start;old=src.stored(nv*56,'vertices')
oldrows=np.frombuffer(old,np.uint8).reshape(nv,56);newrows=np.frombuffer(vertices,np.uint8).reshape(nv,56)
assert np.array_equal(oldrows[:,:32],newrows[:,:32]) and np.array_equal(oldrows[:,40:],newrows[:,40:]);assert out.endswith(blob[vertex_end:])
assets=ROOT/'build/pharmacie-skate/assets';skies=assets/'private/native-skies';sky=json.loads((skies/(name+'.json')).read_text())
sky['sun_width']=16;sky['sun_height']=16;sky['environment']={'anchor_height':0,'sun_direction':sun.tolist(),'sun_scale':.02,'multiplier':1.,'location_chain':['Original authored Syston daylight']}
sunbytes=bytes((0,0,0,255))*256
for key in (name,OUT.stem):
 (skies/(key+'.json')).write_text(json.dumps(sky));(skies/(key+'.sun.rgba')).write_bytes(sunbytes)
 if key!=name:(skies/(key+'.rgba')).write_bytes((skies/(name+'.rgba')).read_bytes())
data=json.loads((assets/'private/character-lighting.json').read_text());sh=data['default_sh'];probes=[]
for x in (-1000.,1000.):
 for y in (-10.,40.):
  for z in (-2000.,2000.):
   values=[v for rgb in sh for v in (*rgb,0.)]+[x,y,z,0.];assert len(values)==40;probes.append(struct.pack('<40f',*values))
OUT.with_suffix('.irradiance').write_bytes(b'SHP1'+struct.pack('<II',1,len(probes))+b''.join(probes))
report={'source':str(SOURCE.relative_to(ROOT)),'output':str(OUT.relative_to(ROOT)),'sha256':hashlib.sha256(out).hexdigest(),'lighting':'Original orientation lightmap, 42% ambient plus 50% cosine sun term; not an occlusion bake. Original constant daylight probe placement uses local extracted character shader coefficients.','positions_normals_albedo_uv_indices_collision_features_unchanged':True,'world_source_render_colour_textures_retained':nt,'sun_runtime_y_up':sun.tolist(),'limits':['No baked architectural occlusion; no Blender lighting parity claim.','Ride, ollie, landing and grind input tests still required.']}
(ROOT/'recon/skate-v60/daylight-adaptation.json').write_text(json.dumps(report,indent=2));print('DAYLIGHT_DEMO_PACKAGE_READY',len(out))
