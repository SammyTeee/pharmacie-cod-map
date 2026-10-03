"""Continuous entrance floor bridge from pavement through recessed doorway."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-entrance-fixed-v16.blend'
assert Path(bpy.data.filepath).name=='pharmacie-detailed-pub-v15.blend';assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v15-before-entrance-threshold.blend'),copy=True)
x0,x1,y0,y1,z0,z1=4.18,6.85,-.08,2.60,-.27,.003
me=bpy.data.meshes.new('Front entrance continuous threshold')
me.from_pydata([(x,y,z) for z in (z0,z1) for y in (y0,y1) for x in (x0,x1)],[],[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)])
me.materials.append(bpy.data.materials['Video | downstairs timber planks']);me.update()
o=bpy.data.objects.new('Front | continuous entrance threshold - no floor gap',me)
bpy.data.collections['STREET | Simple UK two-way road + pavements'].objects.link(o)
o['purpose']='Solid floor bridge overlaps pavement and interior at front recessed doorway; 3mm raised top avoids coplanar flicker'
for s in bpy.data.scenes:
 for layer in s.view_layers:layer.update()
 s['gameplay_version']='v16 - continuous front entrance threshold and v15 detail'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'assets/blender/front-threshold-v16-manifest.json').write_text(json.dumps({'file':str(OUT),'bounds_m':[x0,x1,y0,y1,z0,z1],'clear_door_width_m':1.996,'purpose':o['purpose'],'runtime_verified':False},indent=2)+'\n')
result={'saved':str(OUT),'threshold_bounds':[x0,x1,y0,y1,z0,z1]}
