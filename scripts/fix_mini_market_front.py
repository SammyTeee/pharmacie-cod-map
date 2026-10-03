"""Restore full Mini Market frontage using untouched source photo UVs."""
from pathlib import Path
import bpy, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-street-details-v13.blend'
assert Path(bpy.data.filepath).name=='pharmacie-street-details-v12.blend'
assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v12-before-mini-market-fix.blend'),copy=True)
o=next(o for o in bpy.data.objects if o.name.endswith('Syston Mini Market photographic front'))
source=ROOT/o['source'];sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert sha==o['source_sha256']
image=next(n.image for n in o.active_material.node_tree.nodes if n.type=='TEX_IMAGE')
w,h=image.size
corners=[(1010,238),(1770,260),(1750,840),(1030,840)]
tl,tr,br,bl=corners
for idx,(px,py) in zip(o.data.polygons[0].loop_indices,(br,bl,tl,tr)):
 o.data.uv_layers.active.data[idx].uv=(px/w,1-py/h)
o['uv_source_quad_pixels']=json.dumps(corners)
o['crop_revision']='v13: full roof, upper windows, fascia and shopfront to pavement; source car occlusion retained'
# The full-photo roof replaces the separately sampled generic slate strip.
strip=bpy.data.objects.get(o.name+' roof slates')
if strip:
 strip.hide_render=True
 strip.hide_viewport=True
for s in bpy.data.scenes:s['gameplay_version']='v13 - full Mini Market photo crop; Blender only'
for layer in bpy.context.scene.view_layers:layer.update()
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'assets/blender/mini-market-v13-manifest.json').write_text(json.dumps({'file':str(OUT),'source':o['source'],'sha256':sha,'pixel_quad_TL_TR_BR_BL':corners,'source_unchanged':True,'note':'Expanded upper and lower UV bounds; full shopfront and roof, original parked car retained. No Radiant rebuild.'},indent=2)+'\n')
result={'saved':str(OUT),'pixel_quad':corners,'source_unchanged':True}
