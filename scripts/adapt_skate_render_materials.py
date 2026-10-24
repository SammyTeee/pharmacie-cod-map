"""Portable Blender colours -> the pinned engine's explicit texture renderer."""
from pathlib import Path
import sys,struct,zlib,json,hashlib,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
import analyze_skate as analyzer
SOURCE=ROOT/'build/pharmacie-skate/pharmacie-street-session-runtime.skate';OUT=SOURCE.with_name('pharmacie-street-session-playable.skate');assert not OUT.exists()
blob=SOURCE.read_bytes();r=analyzer.Reader(blob);assert r.take(8,'magic')==b'SKATE15\0';r.u32('endian');map_name=r.string('name');r.skip(196,'environment');count_offset=r.offset;counts=struct.unpack('<9I',r.take(36,'counts'));material_count,texture_count=counts[:2]
material_start=r.offset;decoded_size=r.u32('material decoded size');material_bytes=r.stored(decoded_size,'materials');material_end=r.offset
textures_start=r.offset;texture_payloads=[]
for i in range(texture_count):
 r.string('texture');w,h,cs=struct.unpack('<3I',r.take(12,'texture fields'));texture_payloads.append(r.stored(w*h*4,'texture',texture_payloads))
textures_end=r.offset
def string(value):
 value=value.encode('utf-8');return struct.pack('<I',len(value))+value
def stored(value):
 comp=zlib.compress(value,6);return struct.pack('<II',1,len(comp))+comp
mr=analyzer.Reader(material_bytes);new_materials=[];textures=[];solids={};changed=[]
for i in range(material_count):
 name=mr.string('material');fields=bytearray(mr.take(76,'fields'));depth=mr.take(4,'depth');enabled=mr.u32('native definition');assert enabled==0,'Preserve genuine existing shader definitions'
 albedo=struct.unpack_from('<I',fields,32)[0]
 if not albedo:
  rgb=struct.unpack_from('<3f',fields,12);pixel=tuple(int(round(math.sqrt(max(0,min(1,c)))*255)) for c in rgb)+(255,)
  if pixel not in solids:
   solids[pixel]=texture_count+len(textures)+1
   texture_name='Syston authored solid '+'-'.join(map(str,pixel[:3]));rgba=bytes(pixel)*16
   textures.append(string(texture_name)+struct.pack('<3I',4,4,1)+stored(rgba))
  struct.pack_into('<I',fields,32,solids[pixel]);changed.append(name)
 # The runtime reads the explicit environment shader inputs, ignoring portable tint.
 # This is an authored adapter definition, not recovered retail provenance.
 definition=struct.pack('<QI i',0,0,-1)+string('environment.default')+struct.pack('<4I',1,0,0,0)+string('Original Syston Blender material adapter; no retail material provenance')
 new_materials.append(string(name)+fields+depth+struct.pack('<I',1)+definition)
assert mr.offset==len(material_bytes)
new_material_bytes=b''.join(new_materials);prefix=bytearray(blob[:material_start]);struct.pack_into('<I',prefix,count_offset+4,texture_count+len(textures))
output=prefix+struct.pack('<I',len(new_material_bytes))+stored(new_material_bytes)+blob[textures_start:textures_end]+b''.join(textures)+blob[textures_end:]
OUT.write_bytes(output)
# All visual vertex/index, collision and authored feature records remain byte-identical.
assert output.endswith(blob[textures_end:])
# Original procedural sky, using the engine's supported sky-package contract.
base=ROOT/'build/pharmacie-skate/assets/private/native-skies';base.mkdir(exist_ok=True)
W,H=512,256;yy,xx=np.mgrid[:H,:W];t=yy/(H-1);horizon=np.array((.67,.73,.79));zenith=np.array((.30,.47,.68))
weight=np.clip((.5-t)*2,0,1)**.65;rgb=horizon[None,None,:]*(1-weight[:,:,None])+zenith[None,None,:]*weight[:,:,None]
cloud=(.012*np.sin(xx*.035+np.sin(yy*.05)*2)*np.sin(yy*.043))[:,:,None];rgb=np.broadcast_to(rgb,(H,W,3)).copy()+cloud
rgba=np.concatenate((np.uint8(np.clip(rgb,0,1)*255),np.full((H,W,1),255,np.uint8)),axis=2)
positions=[];uvs=[];indices=[];rows,cols=24,64
for j in range(rows+1):
 lat=-math.pi/2+j*math.pi/rows
 for k in range(cols+1):
  a=k*math.tau/cols;positions.append([5000*math.cos(lat)*math.cos(a),5000*math.sin(lat),5000*math.cos(lat)*math.sin(a)]);uvs.append([k/cols,1-j/rows])
for j in range(rows):
 for k in range(cols):
  a=j*(cols+1)+k;b=a+cols+1;indices.extend((a,b,a+1,a+1,b,b+1))
(base/(map_name+'.rgba')).write_bytes(rgba.tobytes());(base/(map_name+'.json')).write_text(json.dumps({'width':W,'height':H,'positions':positions,'uvs':uvs,'indices':indices,'environment':None}))
report={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(blob).hexdigest(),'output':str(OUT.relative_to(ROOT)),'output_sha256':hashlib.sha256(output).hexdigest(),'solid_colour_materials_adapted':changed,'added_solid_colour_textures':len(textures),'original_textures_retained':texture_count,'visual_collision_and_authored_feature_bytes_unchanged':True,'sky':'Original procedural blue-grey panorama/dome; no game or reference imagery','limits':['Generic texture renderer approximation; not full Blender shader parity.','Solid material colours are explicit small texture assets because the pinned renderer ignores portable tint.','Skating and trick/grind input verification remain separate.']}
(ROOT/'recon/skate-v60/render-material-adaptation.json').write_text(json.dumps(report,indent=2));print('RENDER_MATERIALS_ADAPTED',len(changed),'materials',len(textures),'textures')
