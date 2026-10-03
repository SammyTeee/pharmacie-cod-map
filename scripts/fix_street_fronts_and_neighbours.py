"""Shallow photo scenery and newly supplied pub-side neighbours; preserve v11."""
from pathlib import Path
import bpy,json,hashlib,ast,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-street-details-v12.blend'
assert Path(bpy.data.filepath).name=='pharmacie-street-fronts-v11.blend';assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v11-before-front-height-fix.blend'),copy=True)
upper=bpy.data.collections['STREET | Opposite High Street photo fronts'];lower=upper;made=[]
tree=ast.parse((ROOT/'scripts/dress_video_pub_blender.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('mat','record','box','cyl','panel','update'):exec(compile(ast.Module(body=[node],type_ignores=[]),'<street helpers>','exec'))
update()
# The broad dark strips were 4.35m-deep horizontal roofs exposed in Sam's
# elevated editor view. Shallow backing suits the requested 2D scenery.
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.endswith('simple building mass'):
  for v in o.data.vertices:v.co.y=-13.05+(v.co.y+13.05)*(.32/4.2)
 if o.type=='MESH' and o.name.endswith('simple roof'):
  for v in o.data.vertices:v.co.y=-12.975+(v.co.y+12.975)*(.40/4.35)
brick=bpy.data.materials['Video | street side brick'];stone=bpy.data.materials['Video | street pale plinth'];slate=bpy.data.materials['Video | street slate roof']
# Roof strips sampled from actual slates in the supplied originals, UV only.
source=ROOT/'opposite front.png';im=bpy.data.images.load(str(source),check_existing=True);im.pack()
roofmat=mat('street photo roof slates',(.15,.15,.15));tex=roofmat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im;roofmat.node_tree.links.new(tex.outputs['Color'],roofmat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
for o in list(bpy.data.objects):
 if o.type!='MESH' or not o.name.endswith('photographic front'):continue
 pts=[o.matrix_world@v.co for v in o.data.vertices];x0=min(p.x for p in pts);x1=max(p.x for p in pts);z=max(p.z for p in pts)
 strip=panel(o.name+' roof slates',[(x0,-12.995,z+.02),(x1,-12.995,z+.02),(x1,-13.12,z+.65),(x0,-13.12,z+.65)],roofmat)
 w,h=im.size
 for idx,(px,py) in zip(strip.data.polygons[0].loop_indices,((2000,410),(1200,365),(1200,313),(2000,350))):strip.data.uv_layers.active.data[idx].uv=(px/w,1-py/h)
# New photos face -Y, the same way as the pub. Keep a gap on the left for
# Sam's rear-exit passage rather than closing the previously approved route.
specs=[('Wreake Valley Flooring','left of pub front.png',-13.2,-5.2,8.3,[(633,0),(1987,0),(1950,1010),(658,1010)]),
 ('Syston Dry Cleaners','right side of pub front.png',11.4,18.1,8.3,[(864,0),(1490,187),(1485,835),(873,943)]),
 ('Nail and Spa shop','right side of pub front.png',18.1,24.5,7.9,[(1496,160),(1848,310),(1848,724),(1500,810)])]
records=[]
for name,filename,x0,x1,height,corners in specs:
 path=ROOT/filename;sha=hashlib.sha256(path.read_bytes()).hexdigest();image=bpy.data.images.load(str(path),check_existing=True);image.pack();w,h=image.size
 m=mat('street photo '+name,(.5,.5,.5));tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;m.node_tree.links.new(tex.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
 box(name+' shallow scenery backing',((x0+x1)/2,.2,height/2),(x1-x0,.36,height),brick)
 o=panel(name+' photographic front',[(x0,-.015,.10),(x1,-.015,.10),(x1,-.015,height),(x0,-.015,height)],m)
 tl,tr,br,bl=corners
 for idx,(px,py) in zip(o.data.polygons[0].loop_indices,(bl,br,tr,tl)):o.data.uv_layers.active.data[idx].uv=(px/w,1-py/h)
 o['source']=filename;o['source_sha256']=sha;o['uv_source_quad_pixels']=json.dumps(corners)
 box(name+' shallow roof edge',((x0+x1)/2,.2,height+.05),(x1-x0+.1,.4,.1),slate)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
 records.append({'building':name,'source':filename,'source_sha256':sha,'dimensions':[w,h],'pixel_quad_TL_TR_BR_BL':corners,'world_x':[x0,x1],'height_m':height,'front_y':-.015,'edits':'Untouched packed original, UV quad only; top of source is cropped by supplied screenshot','placement':'Approximate scenery. Left passage gap retained. No enterable shops.'})
for o in made:o['evidence']='User Street View captures Apr2026';o['bo3_role']='Scenery photo front, no functional doorway'
update()
assert min(v.co.y for o in upper.objects if o.type=='MESH' and o.name.endswith('simple building mass') for v in o.data.vertices)>-13.4
for s in bpy.data.scenes:s['gameplay_version']='v12 - video interiors, shallow street fronts and adjacent neighbours; Blender only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(ROOT/'assets/blender/street-details-v12-manifest.json').write_text(json.dumps({'file':str(OUT),'additional_neighbours':records,'opposite_backing_depth_m':.32,'opposite_roof_cap_depth_m':.4,'opposite_photo_roof_strips':5,'reason':'Remove broad exposed blank top surfaces seen in user blender preview.png; photo faces already span pavement to eaves','radiant_rebuilt':False,'runtime_verified':False},indent=2)+'\n')
result={'saved':str(OUT),'new_neighbours':len(records),'shallow_backing_fix':True}
