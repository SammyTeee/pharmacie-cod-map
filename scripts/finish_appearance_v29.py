"""Render-discovered brick fix and reference window inserts, old checkpoints intact."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath)
assert source.name=='pharmacie-syston-detail-v28.blend'
OUT=ROOT/'assets/blender/pharmacie-syston-detail-v29.blend';assert not OUT.exists()
dest=ROOT/'recon/v29';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections.new('STREET v29 | Reference window detail');scene.collection.children.link(coll)
made=[];panels=[];basis=Matrix.Identity(4);current='B032'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
# Correct the render-discovered stripes on side walls: choose the local horizontal
# projection from the surface normal rather than using X on every wall.
for m in bpy.data.materials:
    if not m.name.startswith('Syston v27 | weathered brick'):continue
    n=m.node_tree.nodes;l=m.node_tree.links;sep=next(x for x in n if x.type=='SEPXYZ');combine=next(x for x in n if x.type=='COMBXYZ')
    geom=n.new('ShaderNodeNewGeometry');transform=n.new('ShaderNodeVectorTransform');transform.vector_type='NORMAL';transform.convert_from='WORLD';transform.convert_to='OBJECT';l.new(geom.outputs['Normal'],transform.inputs[0]);ns=n.new('ShaderNodeSeparateXYZ');l.new(transform.outputs[0],ns.inputs[0])
    ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(ns.outputs['X'],ab.inputs[0]);test=n.new('ShaderNodeMath');test.operation='GREATER_THAN';test.inputs[1].default_value=.5;l.new(ab.outputs[0],test.inputs[0])
    mix=n.new('ShaderNodeMixRGB');l.new(test.outputs[0],mix.inputs[0]);l.new(sep.outputs['X'],mix.inputs[1]);l.new(sep.outputs['Y'],mix.inputs[2]);l.new(mix.outputs[0],combine.inputs['X'])
photo=ROOT/'references/streetview-capture/taraj-to-pharmacie/originals/00270__route-021-left-frontage-detail.png';phash=hashlib.sha256(photo.read_bytes()).hexdigest();im=bpy.data.images.load(str(photo),check_existing=True);im.pack()
def panel(name,bounds,quad):
    x0,x1,z0,z1,y=bounds
    me=bpy.data.meshes.new(name);me.from_pydata([(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],[],[(0,1,2,3)]);me.update()
    uv=me.uv_layers.new(name='Original pixel quad')
    # Pixel quad supplied bottom-left,bottom-right,top-right,top-left; UV-only.
    for loop,xy in zip(me.loops,quad):uv.data[loop.index].uv=(xy[0]/1904,1-xy[1]/937)
    m=bpy.data.materials.new('Syston v29 | '+name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.55
    t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=im;m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color']);me.materials.append(m)
    o=bpy.data.objects.new('Syston v29 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['reference_only_photo_insert']=True;o['source']='00270 April2026';panels.append({'object':o.name,'source':str(photo.relative_to(ROOT)),'sha256':phash,'quad_pixels':quad,'bounds':bounds});return o
def box(name,x0,x1,y0,y1,z0,z1,m):
    me=bpy.data.meshes.new(name);me.from_pydata([(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]);me.materials.append(m);me.update();o=bpy.data.objects.new('Syston v29 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();made.append(o);return o
group=[o for o in scene.objects if o.get('catalogue_id')=='B032'];anchor=next(o for o in group if 'upper facade' in o.name);basis=anchor.matrix_world.copy()
xs=[v.co.x for v in anchor.data.vertices];x0,x1=min(xs),max(xs)
panel('salon left display with bunting',(x0+.22,-.78,.82,3.20,-.145),[(1180,711),(1325,709),(1320,559),(1180,563)])
panel('door floral glass',(-.46,.46,.82,2.60,.195),[(1425,657),(1491,653),(1488,579),(1423,580)])
# Curtains in upper glazing, preserving the pub-size frames.
for o in group:
    if 'upper sash glass' not in o.name:continue
    xs=[v.co.x for v in o.data.vertices];zs=[v.co.z for v in o.data.vertices]
    panel('upper curtain glazing '+str(len(panels)),(min(xs)+.055,max(xs)-.055,min(zs)+.06,max(zs)-.06,-.133),[(1420,437),(1480,438),(1476,361),(1418,358)])
pale=bpy.data.materials['Syston v27 | warm white window paint'];dark=bpy.data.materials['Syston v27 | outdoor metal'];slate=bpy.data.materials['Street v17 | slate']
# The photographed shared Amy/GLO retail row has a pitched tile roof and chimneys.
for current in ('B032','B033','B015'):
    anchor=next(o for o in scene.objects if o.get('catalogue_id')==current and 'upper facade' in o.name);basis=anchor.matrix_world.copy();xs=[v.co.x for v in anchor.data.vertices];zs=[v.co.z for v in anchor.data.vertices];a,c=min(xs),max(xs);h=max(zs)
    for sign in (-1,1):
        roof=box('pitched slate roof half',a-.12,c+.12,0,5.1,h+.26,h+.34,slate)
        for v in roof.data.vertices:
            if sign==1:v.co.z+=v.co.y*.19
            else:v.co.y+=5;v.co.z+=(10-v.co.y)*.19
    box('ridge capping',a-.15,c+.15,4.92,5.13,h+1.20,h+1.29,slate)
    if current!='B015':
        brick=bpy.data.materials['Syston v27 | weathered brick 2'];x=a+(c-a)*.72
        box('brick chimney',x-.30,x+.30,3.7,4.35,h+.3,h+2.00,brick);box('chimney cap',x-.35,x+.35,3.65,4.40,h+1.94,h+2.07,pale)
        for xx in (x-.16,x+.16):box('terracotta chimney pot',xx-.085,xx+.085,3.92,4.08,h+2.07,h+2.38,brick)
    if current=='B032':box('facade service cable',a,c,-.25,-.225,4.50,4.53,dark)
# Café display menus separate from the structural window and fascia.
current='B045';anchor=next(o for o in scene.objects if o.get('catalogue_id')==current and 'upper facade' in o.name);basis=anchor.matrix_world.copy();xs=[v.co.x for v in anchor.data.vertices];a,c=min(xs),max(xs)
menu=bpy.data.materials.new('Syston v29 | cafe menu cream');menu.diffuse_color=(.72,.66,.51,1)
for j in (0,1):
    x=a+2+(c-a-3)*(.25+j*.5)
    box('window menu frame',x-.23,x+.23,-.23,-.19,1.35,2.18,dark);box('window menu paper',x-.20,x+.20,-.235,-.231,1.38,2.15,menu)
    for z in (1.55,1.63,1.71,1.79,1.87):box('menu printed line',x-.14,x+.14,-.24,-.236,z,z+.012,dark)
for o in made:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0,o.name;bm.free()
assert hashlib.sha256(photo.read_bytes()).hexdigest()==phash
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
scene.camera=bpy.data.objects['Review v28 | amy_clarke'];bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(dest/'validation.json').write_text(json.dumps({'checkpoint':str(OUT.relative_to(ROOT)),'input_sha256':source_hash,'new_closed_solids':len(made),'reference_window_panels':panels,'original_unchanged':True,'material_fix':'Face-normal horizontal brick projection fixes striped side walls','limits':['Photo inserts remain private reference assets; no redistribution permission','Roof pitches/chimneys are photo-led estimates','Other shops still require individual reconstruction; not Pharmacie-level finished street','No Radiant or BO3 export/verification']},indent=2)+'\n')
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=1400;scene.render.resolution_y=950;scene.render.resolution_percentage=100;scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
ld=bpy.data.lights.new('Temporary v29 sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name,cam in [('01_amy_clarke',bpy.data.objects['Review v28 | amy_clarke']),('02_costa',bpy.data.objects['Review v25 | 02_costa_and_town_square']),('03_street',bpy.data.objects['Review v25 | 06_bridge_player'])]:
    scene.camera=cam;scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print('V29_COMPLETE',OUT)
