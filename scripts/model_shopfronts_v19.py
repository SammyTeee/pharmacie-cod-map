"""Reference-led neighbouring shop relief; preserve v18 and original photos."""
from pathlib import Path
import bpy,math,json,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-shopfronts-v19.blend'
assert not OUT.exists(), 'Preserve the existing v19 checkpoint'
assert Path(bpy.data.filepath).name=='pharmacie-player-cleanup-v18.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene=scene
old=bpy.data.collections['STREET v17 | Photo-led connected High Street']
coll=bpy.data.collections.new('STREET v19 | Modelled neighbour shopfronts')
for s in bpy.data.scenes:
    if old.name in s.collection.children:s.collection.children.link(coll)
protected={o.name:([tuple(o.matrix_world@v.co) for v in o.data.vertices], [tuple(p.vertices) for p in o.data.polygons]) for o in scene.objects if o.type=='MESH' and not o.name.startswith('Street v17 |')}
anchor=bpy.data.objects['Front | sash recessed glass']
anchor_pts=[anchor.matrix_world@v.co for v in anchor.data.vertices]
pub_cx=(min(v.x for v in anchor_pts)+max(v.x for v in anchor_pts))/2
pub_window_parts=[]
for o in scene.objects:
    if o.type!='MESH' or not o.name.startswith(('Front | sash','Front | stone sash')):continue
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    if min(v.x for v in pts)>=pub_cx-1.25 and max(v.x for v in pts)<=pub_cx+1.25:pub_window_parts.append(o)
assert len(pub_window_parts)>=8
archive=bpy.data.collections.new('ARCHIVE v18 | Neighbour flat facade panels');archive.use_fake_user=True
made=[]
def material(name,color):
    m=bpy.data.materials.new('Shop v19 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.72
    return m
green=material('sage joinery',(.20,.28,.135));cream=material('cream sign',(.72,.71,.59))
charcoal=material('cleaner grey',(.19,.23,.25));white=material('painted white',(.79,.79,.73))
blue=material('spa blue',(.055,.28,.49));dark=material('dark backing',(.025,.033,.032))
tile=material('pale recess tile',(.58,.58,.50));terra=material('terracotta entry',(.39,.16,.085))
brick=material('brick relief',(.34,.135,.071));glass=material('upper glazing',(.11,.17,.19))
nodes=brick.node_tree.nodes;tex=nodes.new('ShaderNodeTexBrick');tex.inputs['Scale'].default_value=2.4
tex.inputs['Color1'].default_value=(.39,.15,.075,1);tex.inputs['Color2'].default_value=(.23,.075,.035,1)
tex.inputs['Mortar'].default_value=(.24,.23,.20,1);tex.inputs['Mortar Size'].default_value=.025
coords=nodes.new('ShaderNodeTexCoord');sep=nodes.new('ShaderNodeSeparateXYZ');combine=nodes.new('ShaderNodeCombineXYZ');add=nodes.new('ShaderNodeMath');add.operation='ADD'
brick.node_tree.links.new(coords.outputs['Object'],sep.inputs[0])
brick.node_tree.links.new(sep.outputs['X'],add.inputs[0]);brick.node_tree.links.new(sep.outputs['Y'],add.inputs[1])
brick.node_tree.links.new(add.outputs[0],combine.inputs['X']);brick.node_tree.links.new(sep.outputs['Z'],combine.inputs['Y'])
brick.node_tree.links.new(combine.outputs[0],tex.inputs['Vector'])
brick.node_tree.links.new(tex.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
def mesh(name,verts,faces,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();me.materials.append(mat)
    o=bpy.data.objects.new('Shop v19 | '+name,me);coll.objects.link(o);made.append(o)
    o['evidence']='docs/STREET_PHOTO_RECONSTRUCTION.md B01/B03/B04; existing v17 facade derivatives'
    o['status']='Static scenery; approximate depth; Blender only, BO3 conversion pending'
    return o
def box(name,x0,x1,y0,y1,z0,z1,mat):
    return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat)
def beam(name,a,b,z0,z1,width,mat):
    vec=Vector((b[0]-a[0],b[1]-a[1],0));n=Vector((-vec.y,vec.x,0)).normalized()*width/2
    pts=[(a[0]-n.x,a[1]-n.y),(b[0]-n.x,b[1]-n.y),(b[0]+n.x,b[1]+n.y),(a[0]+n.x,a[1]+n.y)]
    return mesh(name,[(x,y,z) for z in (z0,z1) for x,y in pts],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat)
sources=json.loads((ROOT/'assets/street/v17/manifest.json').read_text())['fronts']
source_by_name={s['name']:s for s in sources}
photo_mats={};panels=[]
def photo(name,shop,a,b,z0,z1,crop):
    if shop not in photo_mats:
        m=material(shop+' selected window display',(.3,.3,.3));im=bpy.data.images.load(str(ROOT/source_by_name[shop]['derivative']),check_existing=True);im.pack()
        t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=im;t.extension='EXTEND'
        m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);photo_mats[shop]=m
    o=mesh(name,[(a[0],a[1],z1),(b[0],b[1],z1),(b[0],b[1],z0),(a[0],a[1],z0)],[(0,1,2,3)],photo_mats[shop])
    uv=o.data.uv_layers.new(name='UV_Display_Photo');x0,y0,x1,y1=crop
    for li,p in zip(o.data.polygons[0].loop_indices,[(x0/1024,1-y0/1024),(x1/1024,1-y0/1024),(x1/1024,1-y1/1024),(x0/1024,1-y1/1024)]):uv.data[li].uv=p
    uv.active_render=True;o['source_derivative']=source_by_name[shop]['derivative'];o['source_pixel_crop']=crop
    panels.append({'object':o.name,'shop':shop,'derivative':source_by_name[shop]['derivative'],'crop_pixels':crop})
def pane(name,shop,a,b,z0,z1,crop,mat):
    photo(name+' display inset',shop,a,b,z0,z1,crop)
    for p in (a,b):box(name+' upright',p[0]-.055,p[0]+.055,p[1]-.08,p[1]+.08,z0-.08,z1+.08,mat)
    beam(name+' sill',a,b,z0-.09,z0,.14,mat);beam(name+' head',a,b,z1,z1+.09,.14,mat)
def text(name,body,x,y,z,width,mat,height=.30):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=height;cu.extrude=.001
    ob=bpy.data.objects.new('Shop v19 | '+name,cu);coll.objects.link(ob);ob.location=(x,y,z);ob.rotation_euler=(math.pi/2,0,0);cu.materials.append(mat);made.append(ob)
    bpy.context.view_layer.update()
    if ob.dimensions.x>width:ob.scale*=width/ob.dimensions.x
    ob['status']='Sharp geometric lettering; future engine mesh/material export required'
    return ob
def begin(shop,x0,x1,h):
    flat=bpy.data.objects['Street v17 | '+shop+' isolated facade'];archive.objects.link(flat)
    for c in list(flat.users_collection):
        if c!=archive:c.objects.unlink(flat)
    mass=bpy.data.objects['Street v17 | '+shop+' solid scenery mass'];mass.data=mass.data.copy()
    for v in mass.data.vertices:
        if abs(v.co.y)<.001:v.co.y=1.05
        if abs(v.co.z-h)<.001:v.co.z=9.5
    for ob in list(old.objects):
        if ob.type!='MESH' or not ob.name.startswith('Street v17 | '+shop+' ') or ob==mass or ob==flat:continue
        if any(s in ob.name for s in ('roof','gutter','chimney')):
            ob.data=ob.data.copy()
            for v in ob.data.vertices:v.co.z+=9.5-h
        elif 'downpipe' in ob.name:
            ob.data=ob.data.copy()
            for v in ob.data.vertices:
                if v.co.z>h-.2:v.co.z+=9.5-h
    # Real upper facade restores the front edge; ground-floor mass sits behind
    # modelled recesses. Entire building remains non-enterable scenery.
    box(shop+' upper brick face',x0,x1,0,1.05,3.45,9.5,brick)
    box(shop+' opaque rear display backing',x0,x1,1.00,1.04,0,3.45,dark)
def sash(name,x,y,z,w,h,mat):
    # User-directed scale: clone the actual first pub window, not an estimate.
    # Preserve world size/sill/head levels; only translate to the shop position.
    for part in pub_window_parts:
        verts=[tuple(part.matrix_world@v.co+Vector((x-pub_cx,y-.03,0))) for v in part.data.vertices]
        m=glass if 'glass' in part.name else cream if 'stone' in part.name else mat
        mesh(name+' | '+part.name,verts,[tuple(p.vertices) for p in part.data.polygons],m)
# Wreake: broad windows angle back to closed central double doors.
shop='Wreake Valley Flooring';x0,x1=-10.16,-2.16;begin(shop,x0,x1,8.3)
for x in (x0+.13,x1-.13):
    box('Wreake pilaster',x-.13,x+.13,-.18,.15,0,3.55,green)
    box('Wreake pilaster base',x-.17,x+.17,-.23,.18,0,.25,green)
box('Wreake fascia body',x0,x1,-.22,.07,3.45,4.48,green)
box('Wreake cream sign inset',x0+.22,x1-.22,-.245,-.23,3.65,4.28,cream)
for z in (3.43,4.42):box('Wreake moulded fascia rail',x0-.04,x1+.04,-.31,.08,z,z+.10,green)
text('Wreake sign','wreake valley flooring',-6.16,-.258,3.97,6.9,green,.42)
leftfront=(-8.05,0);leftback=(-6.95,.78);rightback=(-5.39,.78);rightfront=(-4.28,0)
pane('Wreake left window',shop,(x0+.27,0),leftfront,.25,3.35,(48,537,262,971),green)
pane('Wreake left angled return',shop,leftfront,leftback,.25,3.35,(297,540,395,966),green)
pane('Wreake right angled return',shop,rightback,rightfront,.25,3.35,(626,540,729,966),green)
pane('Wreake right window',shop,rightfront,(x1-.27,0),.25,3.35,(759,538,985,972),green)
box('Wreake recessed tile threshold',leftfront[0],rightfront[0],0,.90,-.015,.002,tile)
for i,(a,b,crop) in enumerate([(-6.95,-6.17,(406,654,497,855)),(-6.17,-5.39,(506,654,597,855))]):
    box('Wreake door lower panel',a,b,.74,.83,.06,1.00,green)
    pane('Wreake closed door '+str(i),shop,(a,.72),(b,.72),1.0,2.65,crop,green)
    box('Wreake handle',b-.13,b-.105,.635,.70,1.35,1.75,cream)
pane('Wreake door transom',shop,(-6.95,.72),(-5.39,.72),2.77,3.35,(407,541,599,645),green)
for x in (-8.60,-6.16,-3.72):
    sash('Wreake upstairs sash',x,-.04,5.5,1.20,2.28,charcoal)
# Cleaner: recessed door at left and a projecting chamfered three-pane display.
shop='Syston Dry Cleaners';x0,x1=10.50,17.20;begin(shop,x0,x1,8.3)
box('Cleaner fascia',x0,x1,-.23,.08,3.42,4.20,charcoal)
for z in (3.42,4.18):box('Cleaner sign moulding',x0-.04,x1+.04,-.31,.09,z,z+.08,white)
letters='Syston Dry Cleaners and Laundry';palette=[(.75,.61,.12),(.61,.16,.12),(.32,.49,.16),(.17,.34,.64)]
letter_mats=[material('sign letter '+str(i),c) for i,c in enumerate(palette)]
sign=text('Cleaner multicolour sign',letters,13.85,-.25,3.84,6.23,letter_mats[0],.32)
for m in letter_mats[1:]:sign.data.materials.append(m)
for i,f in enumerate(sign.data.body_format):f.material_index=i%4
box('Cleaner tiled entry',10.66,12.09,-.04,.85,-.015,.002,terra)
pane('Cleaner closed entry door',shop,(10.82,.68),(11.95,.68),.15,3.29,(153,466,260,873),charcoal)
for x in (10.62,12.04,17.07):box('Cleaner fluted post',x-.09,x+.09,-.16,.16,.02,3.44,charcoal)
points=[(12.15,-.06),(13.10,-.36),(15.73,-.36),(16.94,-.06)]
for i,(a,b,crop) in enumerate(zip(points,points[1:],[(290,476,506,846),(558,476,770,846),(811,476,950,847)])):
    beam('Cleaner brick display base '+str(i),a,b,.04,.57,.30,brick)
    pane('Cleaner display pane '+str(i),shop,a,b,.59,3.32,crop,charcoal)
for x in (13.0,16.05):sash('Cleaner white upper window',x,-.04,4.75,1.36,2.65,white)
# Nail/spa: white ground-floor frames, real grille and projecting upper bays.
shop='Nail and Spa shop';x0,x1=17.20,23.60;begin(shop,x0,x1,7.9)
box('Spa blue fascia',x0,x1,-.25,.09,3.43,4.17,blue)
spa_sign=text('Spa sharp sign','Syston Nails & Spa',21.42,-.27,3.81,3.92,white,.35);spa_sign.data.shear=.18
box('Spa pale left sign panel',17.32,19.27,-.28,-.26,3.55,4.09,white)
pane('Spa left display behind grille',shop,(17.40,-.03),(19.35,-.03),.58,3.30,(34,505,318,807),white)
pane('Spa right display',shop,(19.60,-.03),(22.10,-.03),.15,3.30,(452,480,723,874),white)
pane('Spa closed right entry',shop,(22.27,.36),(23.42,.36),.15,3.30,(762,505,963,855),white)
box('Spa lower brick plinth',17.32,19.40,-.12,.16,.03,.57,brick)
for row in range(5):
    z=.65+row*.51
    for column in range(4):
        a=17.45+column*.46
        # Slanted closed prism bars, using a local cube rotated in the facade plane.
        for angle in (-.65,.65):
            ob=box('Spa diagonal grille',-.018,.018,-.014,.014,-.35,.35,white)
            ob.location=(a+.22,-.14,z+.25);ob.rotation_euler.y=angle
for i,cx in enumerate((18.7,21.8)):
    box('Spa projecting white upper bay '+str(i),cx-1.15,cx+1.15,-.37,.12,5.45,8.78,white)
    sash('Spa upper bay sash '+str(i),cx,-.41,4.75,2.05,2.46,white)
    box('Spa upper bay cornice',cx-1.24,cx+1.24,-.58,.16,8.77,8.95,white)
    box('Spa upper bay lower apron',cx-1.18,cx+1.18,-.48,.13,5.39,5.57,white)
bpy.context.view_layer.update()
for name,(verts,faces) in protected.items():
    o=bpy.data.objects[name]
    assert verts==[tuple(o.matrix_world@v.co) for v in o.data.vertices] and faces==[tuple(p.vertices) for p in o.data.polygons],name
for s in json.loads((ROOT/'docs/reconstruction-sources.json').read_text())['sources']:
    assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
report={'checkpoint':str(OUT),'new_objects':len(made),'protected_pub_meshes_unchanged':len(protected),'original_photos_hash_identical':44,
 'user_scale_reference':{'object':anchor.name,'glass_width_m':max(v.x for v in anchor_pts)-min(v.x for v in anchor_pts),'glass_height_m':max(v.z for v in anchor_pts)-min(v.z for v in anchor_pts),'glass_bottom_z':min(v.z for v in anchor_pts),'glass_top_z':max(v.z for v in anchor_pts),'copied_window_parts':len(pub_window_parts),'new_window_instances':7,'shop_eaves_z':9.5},
 'shops':['Wreake Valley Flooring','Syston Dry Cleaners','Nail and Spa shop'],'window_regions':panels,
 'estimated_depths_m':{'Wreake recess':.78,'Cleaner entry':.68,'Cleaner display projection':.36,'Spa door recess':.36,'Spa upper bays':.37},
 'limitations':'Photographic displays/reflections remain opaque and contain baked detail; depths inferred; spa sign transcribed from reviewed image using approximate typeface; no shop interiors; no Radiant/game build'}
(ROOT/'assets/blender/shopfronts-v19-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
# Retain review cameras so opening this checkpoint presents the new frontage.
views=[('01_wreake_front',(-6.16,-12,2.2),(-6.16,.2,4.8)),('02_wreake_recess',(-9,-4,1.65),(-6.2,.65,1.8)),
 ('03_cleaner_front',(13.85,-12,2.0),(13.85,0,4.8)),('04_spa_front',(20.4,-12,2.0),(20.4,0,4.8)),
 ('05_neighbour_row',(6,-12,3.1),(5,0,4)),('06_right_shop_depth',(11,-5,1.65),(17,-.05,2.5))]
review_cameras=[]
for name,eye,target in views:
    data=bpy.data.cameras.new('Review v19 | '+name);data.lens=12 if name=='05_neighbour_row' else 28
    obj=bpy.data.objects.new(data.name,data);coll.objects.link(obj);obj.location=eye
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler();review_cameras.append(obj)
scene.camera=review_cameras[0]
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
# Save editable scene before temporary render lighting/settings.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
renders=ROOT/'recon/v19';renders.mkdir(parents=True,exist_ok=True)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world=scene.world.copy() if scene.world else bpy.data.worlds.new('v19 render world');scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.65,.72,.84,1)
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.55
ld=bpy.data.lights.new('v19 review sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new('v19 review sun',ld);scene.collection.objects.link(lo);lo.rotation_euler=(.5,-.5,-.4)
camera=bpy.data.cameras.new('v19 review camera');co=bpy.data.objects.new('v19 review camera',camera);scene.collection.objects.link(co);scene.camera=co;camera.lens=28
for name,eye,target in views:
    camera.lens=12 if name=='05_neighbour_row' else 28
    co.location=eye;co.rotation_euler=(Vector(target)-co.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(renders/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(report))
