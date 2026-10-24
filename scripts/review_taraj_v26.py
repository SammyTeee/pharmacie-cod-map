"""Native render corrections: hollow fridge, visible fabric, arches and guest."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v26'
assert Path(bpy.data.filepath).name=='pharmacie-taraj-interior-bridge-v26.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections['DETAIL v26 | Bridge brook and Taraj restaurant'];made=[]
anchor=next(o for o in coll.objects if '| Taraj | carpet floor' in o.name);basis=anchor.matrix_world.copy()
archive=bpy.data.collections.new('ARCHIVE v26 | First render Taraj details');archive.use_fake_user=True
def retire(ob):
    archive.objects.link(ob)
    for c in list(ob.users_collection):
        if c!=archive:c.objects.unlink(ob)
for o in list(coll.objects):
    if any(s in o.name for s in ('| bar cabinet','| scalloped arch header','guest torso','guest head','guest sleeve','guest forearm','guest trouser','guest shoe','requested booth guest source face')):retire(o)
wood=bpy.data.materials['Detail v26 | dark polished hardwood'];linen=bpy.data.materials['Detail v26 | ivory linen'];cream=bpy.data.materials['Detail v26 | damask wallpaper'];dark=bpy.data.materials['Detail v26 | dark backing'];iron=bpy.data.materials['Detail v26 | galvanised rail']
def mesh(name,verts,faces,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new('Detail v26 | Taraj | '+name,me);coll.objects.link(ob);ob.matrix_world=basis.copy();made.append(ob);return ob
def box(name,x0,x1,y0,y1,z0,z1,m):return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)
def cylinder(name,x,y,z,r,h,mat):
    n=20;vs=[(x+r*math.cos(i*math.tau/n),y+r*math.sin(i*math.tau/n),zz) for zz in (z,z+h) for i in range(n)]
    return mesh(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)
box('bar rear carcass',-2.6,-2.45,1.6,3.9,.025,.96,wood)
for z0,z1 in ((.025,.12),(.85,.96)):box('bar cabinet rail',-2.45,-.90,1.6,3.9,z0,z1,wood)
for y0,y1 in ((1.6,1.70),(2.60,2.80),(3.70,3.90)):box('bar cabinet partition',-2.45,-.90,y0,y1,.12,.85,wood)
for o in coll.objects:
    if 'bar fridge inset' in o.name:
        for v in o.data.vertices:v.co.x-=.39
    if 'carved spiral booth column' in o.name:
        for p in o.data.polygons:p.use_smooth=True
g=bpy.data.materials['Detail v26 | glass'].node_tree.nodes['Principled BSDF'];g.inputs['Transmission Weight'].default_value=1;g.inputs['Base Color'].default_value=(.93,.97,.94,1);g.inputs['Roughness'].default_value=.075;g.inputs['IOR'].default_value=1.45
# Repeating six-lobed floral motif in local horizontal/vertical coordinates.
def floral(mat,scale,c0,c1):
    ns=mat.node_tree.nodes;ls=mat.node_tree.links
    def calc(op,*inputs):
        n=ns.new('ShaderNodeMath');n.operation=op
        for i,v in enumerate(inputs):
            if isinstance(v,(int,float)):n.inputs[i].default_value=v
            else:ls.new(v,n.inputs[i])
        return n.outputs[0]
    coord=ns.new('ShaderNodeTexCoord');sep=ns.new('ShaderNodeSeparateXYZ');ls.new(coord.outputs['Object'],sep.inputs[0])
    h=calc('ADD',sep.outputs['X'],sep.outputs['Y']);x=calc('SUBTRACT',calc('FRACT',calc('MULTIPLY',h,scale)),.5);z=calc('SUBTRACT',calc('FRACT',calc('MULTIPLY',sep.outputs['Z'],scale)),.5)
    radius=calc('SQRT',calc('ADD',calc('MULTIPLY',x,x),calc('MULTIPLY',z,z)))
    angle=calc('ARCTAN2',z,x);petals=calc('ADD',.23,calc('MULTIPLY',.085,calc('COSINE',calc('MULTIPLY',angle,6))))
    mask=calc('LESS_THAN',radius,petals);ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*c0,1);ramp.color_ramp.elements[1].color=(*c1,1)
    ls.new(mask,ramp.inputs[0]);bs=ns['Principled BSDF'];ls.new(ramp.outputs[0],bs.inputs['Base Color'])
floral(bpy.data.materials['Detail v26 | floral upholstery'],3.7,(.065,.041,.018),(.35,.24,.073))
floral(cream,6.5,(.57,.46,.30),(.68,.58,.39))
for x0,x1 in ((-2.75,-.75),(3.65,5.55)):
    for y in (6.62,8.87,11.12,13.37):
        outline=[(x0+i*(x1-x0)/32,2.68+.30*math.sin(i*math.pi/32)+.022*math.sin(i*math.pi*7/32)) for i in range(33)]+[(x1,3.14),(x0,3.14)]
        n=len(outline);mesh('smooth scalloped arch header',[(x,yy,z) for yy in (y-.055,y+.055) for x,z in outline],[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],cream)
for j in range(8):
    y=1.6+j*.30;cylinder('optic neck connection',-2.52,y,2.17,.018,.21,dark)
    cylinder('spirit bottle label band',-2.52,y,2.53,.066,.13,linen)
    cu=bpy.data.curves.new('spirit label','FONT');cu.body=('RUM','GIN','VODKA','WHISKY')[j%4];cu.size=.029;cu.align_x='CENTER';cu.materials.append(dark)
    ob=bpy.data.objects.new('Detail v26 | Taraj | spirit label',cu);coll.objects.link(ob);ob.matrix_world=basis@Matrix.Translation((-2.448,y,2.56))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Rotation(math.pi/2,4,'X');made.append(ob)

# Static cutout uses silhouette mesh and UVs; never edits/recompresses source PNG.
gm=bpy.data.materials['Detail v26 | guest photographic face'];im=next(n.image for n in gm.node_tree.nodes if n.type=='TEX_IMAGE')
pixels=[(448,237),(515,224),(589,234),(633,256),(668,296),(684,349),(674,418),(651,464),(626,497),(669,516),(724,548),(766,596),(799,659),(811,732),(792,844),(746,897),(721,913),(298,913),(219,848),(174,810),(136,780),(128,735),(151,691),(196,680),(247,648),(262,595),(302,559),(370,530),(393,497),(377,454),(363,406),(365,348),(385,297),(409,263)]
vs=[(4.55+(x-535)*.00138,8.47,.52+(913-y)*.00146) for x,y in pixels]
me=bpy.data.meshes.new('requested guest silhouette');me.from_pydata(vs,[],[tuple(reversed(range(len(vs))))]);me.materials.append(gm);me.update();uv=me.uv_layers.new(name='UV_unchanged_guest_source')
for p in me.polygons:
    for li in p.loop_indices:
        x,y=pixels[me.loops[li].vertex_index];uv.data[li].uv=(x/im.size[0],1-y/im.size[1])
ob=bpy.data.objects.new('Detail v26 | Taraj | requested seated guest reference cutout',me);coll.objects.link(ob);ob.matrix_world=basis;ob['photo_insert']=True;ob['status']='Static photo-reference cutout; replace with rigged character later';ob['source']=im.filepath;made.append(ob)
bpy.context.view_layer.update()
solids=[o for o in coll.objects if o.type=='MESH' and not o.get('photo_insert')]
for ob in solids:
    bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges),ob.name;assert bm.calc_volume(signed=True)>0 and ob.matrix_world.determinant()>0,ob.name;bm.free()
modified=[o for o in scene.objects if o.type=='MESH' and o.name.startswith(('Syston v25 | B014 |','Street v22 | Melton pavement','Street v22 | Melton kerb'))]
for ob in modified:
    if not len(ob.data.vertices):continue
    bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges),ob.name;assert bm.calc_volume(signed=True)>0,ob.name;bm.free()
# Verify the visible fridge insert now lies behind, rather than before bottles.
dep=bpy.context.evaluated_depsgraph_get();rays=[]
for y in (1.8,2.96):
    hit,loc,n,i,o,ma=scene.ray_cast(dep,basis@Vector((-.82,y,.66)),(basis.to_3x3()@Vector((-1,0,0))).normalized(),distance=1)
    assert hit and 'fridge glazing' in o.name,(y,o.name);rays.append(o.name)
r=json.loads((dest/'validation.json').read_text());r['closed_outward_new_solids']=len(solids);r['modified_scenery_manifold_checks']=len(modified);r['guest']='Static seated source-photo silhouette; no rig or animation';r['review_fixes']=['Hollow bar cabinet and inset behind bottles','Clear glass','Repeating floral fabric/wallpaper','Smooth scalloped headers and spiral posts','Optic connections and bottle labels','Replace rough guest with reference cutout']
(dest/'validation.json').write_text(json.dumps(r,indent=2)+'\n')
camdata=bpy.data.cameras.new('Review v26 | 10_taraj_cutaway');cam=bpy.data.objects.new(camdata.name,camdata);scene.collection.objects.link(cam);cam.location=basis@Vector((1.3,8,20));cam.rotation_euler=(basis@Vector((1.3,8,0))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=16
scene.camera=bpy.data.objects['Review v26 | 01_taraj_dining'];bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100;scene.render.resolution_x=1400;scene.render.resolution_y=1000
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary review sun','SUN');ld.energy=2.2;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name in ('01_taraj_dining','02_taraj_booths','03_taraj_bar','04_taraj_guest','05_taraj_entry','10_taraj_cutaway'):
    hidden=[]
    if name.endswith('cutaway'):
        for o in scene.objects:
            if o.name.startswith('Taraj v23 | upper cream mass') or o.name.startswith('Taraj v23 | roof flat placeholder cap') or ('| Taraj |' in o.name and any(t in o.name for t in ('ceiling backing','ceiling board','ceiling AC','AC louvre','downlight','smooth scalloped arch header','booth top beam'))):hidden.append((o,o.hide_render));o.hide_render=True
    scene.camera=bpy.data.objects['Review v26 | '+name];scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
    for o,state in hidden:o.hide_render=state
print(json.dumps({'new_closed_solids':len(solids),'modified_scenery_checked':len(modified),'fridge_front_rays':rays}))
