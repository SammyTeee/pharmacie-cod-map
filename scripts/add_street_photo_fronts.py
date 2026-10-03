"""Opposite High Street: simple photo-fronted scenery, preserve source PNGs."""
from pathlib import Path
import bpy,json,hashlib,ast,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/blender/pharmacie-street-fronts-v11.blend'
assert Path(bpy.data.filepath).name=='pharmacie-video-details-v10.blend';assert not OUT.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-v10-before-street-fronts.blend'),copy=True)
upper=bpy.data.collections.new('STREET | Opposite High Street photo fronts');lower=upper;made=[]
for name in ('01 Ground floor - mapped rooms','03 Both floors - assembled exterior','04 Photo frontage - inspection','05 Interior - photo-led dressing'):bpy.data.scenes[name].collection.children.link(upper)
tree=ast.parse((ROOT/'scripts/dress_video_pub_blender.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('mat','record','box','cyl','panel','update'):exec(compile(ast.Module(body=[node],type_ignores=[]),'<street modelling helper>','exec'))
brick=mat('street side brick',(.23,.115,.07));roof=mat('street slate roof',(.09,.10,.105));stone=mat('street pale plinth',(.43,.39,.31))
# Pixel corners are TL,TR,BR,BL on untouched original captures. Fronts face
# +Y towards pub, so photograph's left maps to world +X when viewed from pub.
specs=[('Fox and Hounds','opposite front.png',-15,-3,5.4,[(1090,390),(2260,446),(2268,806),(1090,838)]),
 ('Aston and Co','opposite front.png',-3,1,7.1,[(714,246),(1084,259),(1072,770),(690,807)]),
 ('Syston Mini Market','opposite front zoomed out better view flat for texture.png',1,10,7.2,[(1024,307),(1740,324),(1722,751),(1030,751)]),
 ('Lets Move estate agents','opposite fornt further left.png',10,17,6.9,[(902,335),(1500,390),(1500,824),(902,903)]),
 ('Floral Fantasy','opposite fornt further left.png',17,24,7.0,[(103,228),(902,335),(902,927),(100,974)])]
records=[]
for name,source,x0,x1,height,corners in specs:
 path=ROOT/source;sha=hashlib.sha256(path.read_bytes()).hexdigest();image=bpy.data.images.load(str(path),check_existing=True);image.pack();w,h=image.size
 material=mat('street photo '+name,(.5,.5,.5));tex=material.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image
 material.node_tree.links.new(tex.outputs['Color'],material.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
 material.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9
 # Shallow solid backs give silhouettes and side faces; photo face is separate.
 box(name+' simple building mass',((x0+x1)/2,-15.15,height/2),(x1-x0,4.2,height),stone if name=='Fox and Hounds' else brick)
 coords=[(x0,-12.985,.10),(x1,-12.985,.10),(x1,-12.985,height),(x0,-12.985,height)]
 o=panel(name+' photographic front',coords,material)
 tl,tr,br,bl=corners
 for idx,(px,py) in zip(o.data.polygons[0].loop_indices,(br,bl,tl,tr)):o.data.uv_layers.active.data[idx].uv=(px/w,1-py/h)
 o['source']=source;o['source_sha256']=sha;o['uv_source_quad_pixels']=json.dumps(corners);o['bo3_role']='Scenery facade; not an enterable shop'
 box(name+' simple roof',( (x0+x1)/2,-15.15,height+.13),(x1-x0+.16,4.35,.26),roof)
 box(name+' pavement plinth',((x0+x1)/2,-12.96,.09),(x1-x0,.12,.18),stone)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
 records.append({'building':name,'source':source,'source_sha256':sha,'source_dimensions':[w,h],'pixel_quad_TL_TR_BR_BL':corners,'world_x':[x0,x1],'front_y':-12.985,'height_m':height,'raster_derivative':'None; original packed image mapped with UV source quad','placement':'Inferred row opposite pub; observed order retained, gameplay widths not surveyed','limitations':'Perspective, occlusions and baked shadows remain; no functional doors/interiors'})
for o in made:o['evidence']='User-supplied Google Street View captures, Apr2026 visible UI';o['placement']='Simple approximate opposite-street scenery'
# Three lamp posts help connect flat fronts to the road; positions are illustrative.
metal=bpy.data.materials['Blockout - rails.001']
for x in (-11,4,19):
 cyl('opposite street lamp post',(x,-11.85,2.55),.06,5.1,metal)
 box('opposite street lamp arm',(x+.32,-11.85,5.12),(.7,.08,.08),metal)
 box('opposite street lamp head',(x+.62,-11.85,5.10),(.45,.22,.10),roof)
update()
assert all(o.matrix_world.translation.y==0 for o in made) # world-space mesh definitions
manifest={'file':str(OUT),'fronts':records,'new_objects':len(made),'preserved_sources':True,'radiant_rebuilt':False,'runtime_verified':False,'distribution_rights':'Reference captures; not established for publication'}
(ROOT/'assets/blender/street-fronts-v11-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for s in bpy.data.scenes:s['gameplay_version']='v11 - video interiors and opposite street photo fronts; Blender only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result={'saved':str(OUT),'fronts':len(records),'objects':len(made),'sources_unchanged':True}
