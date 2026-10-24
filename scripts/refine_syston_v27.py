"""First reference-led appearance pass; run on saved v26, preserves old milestone."""
from pathlib import Path
import bpy, bmesh, json, hashlib, math
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1]
source=Path(bpy.data.filepath)
assert source.name=='pharmacie-taraj-interior-bridge-v26.blend'
out=ROOT/'assets/blender/pharmacie-syston-appearance-v27.blend'
assert not out.exists()
dest=ROOT/'recon/v27';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
original_hash=hashlib.sha256(source.read_bytes()).hexdigest()
protected={o.name:([tuple(o.matrix_world@v.co) for v in o.data.vertices], [tuple(p.vertices) for p in o.data.polygons]) for o in scene.objects if o.type=='MESH'}
coll=bpy.data.collections.new('STREET v27 | Reference appearance');scene.collection.children.link(coll)
archive=bpy.data.collections.new('ARCHIVE v27 | Superseded Costa details');archive.use_fake_user=True
made=[];retired=[]
def retire(o):
    archive.objects.link(o)
    for c in list(o.users_collection):
        if c!=archive:c.objects.unlink(o)
    retired.append(o.name)
def material(name,color):
    m=bpy.data.materials.new('Syston v27 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
    m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*color,1)
    return m
def grain(m,lo,hi,scale,bump=.08):
    n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3
    l.new(tc.outputs['Object'],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB')
    r.color_ramp.elements[0].color=(*lo,1);r.color_ramp.elements[1].color=(*hi,1)
    l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs['Color'],p.inputs['Base Color'])
    b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.3;b.inputs['Distance'].default_value=bump
    l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal']);p.inputs['Roughness'].default_value=.85
    return tc
def brick_material(i):
    m=material('weathered brick '+str(i),(.37,.15,.075));n=m.node_tree.nodes;l=m.node_tree.links
    tc=grain(m,(.19+i*.018,.067+i*.007,.032),(.49+i*.013,.22+i*.006,.115),1.1,.015)
    sep=n.new('ShaderNodeSeparateXYZ');combine=n.new('ShaderNodeCombineXYZ')
    l.new(tc.outputs['Object'],sep.inputs[0]);l.new(sep.outputs['X'],combine.inputs['X']);l.new(sep.outputs['Z'],combine.inputs['Y']);l.new(sep.outputs['Y'],combine.inputs['Z'])
    b=n.new('ShaderNodeTexBrick');b.inputs['Scale'].default_value=1;b.inputs['Brick Width'].default_value=.235;b.inputs['Row Height'].default_value=.082
    b.inputs['Mortar Size'].default_value=.007;b.inputs['Mortar Smooth'].default_value=.002
    b.inputs['Color1'].default_value=(.31+i*.019,.105+i*.009,.05,1);b.inputs['Color2'].default_value=(.47+i*.017,.195+i*.008,.095,1);b.inputs['Mortar'].default_value=(.27,.245,.205,1)
    l.new(combine.outputs[0],b.inputs['Vector'])
    mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.3
    ramp=next(x for x in n if x.type=='VALTORGB');l.new(b.outputs['Color'],mix.inputs[1]);l.new(ramp.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.45;bump.inputs['Distance'].default_value=.012;l.new(b.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],n.get('Principled BSDF').inputs['Normal'])
    return m
bricks=[brick_material(i) for i in range(5)]
road=material('fine asphalt aggregate',(.11,.12,.12));grain(road,(.075,.079,.079),(.145,.15,.15),65,.006)
paving=material('concrete paving joints',(.4,.39,.35));tc=grain(paving,(.30,.29,.26),(.51,.49,.43),7,.008)
n=paving.node_tree.nodes;l=paving.node_tree.links;b=n.new('ShaderNodeTexBrick');b.inputs['Scale'].default_value=1;b.inputs['Brick Width'].default_value=.6;b.inputs['Row Height'].default_value=.45;b.inputs['Mortar Size'].default_value=.008;b.inputs['Mortar'].default_value=(.18,.18,.16,1);b.inputs['Color1'].default_value=(.42,.41,.36,1);b.inputs['Color2'].default_value=(.54,.52,.46,1);l.new(tc.outputs['Object'],b.inputs['Vector']);l.new(b.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
glazing=material('reflective charcoal glazing',(.065,.083,.09));p=glazing.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.16;p.inputs['Metallic'].default_value=.35
white=material('warm white window paint',(.78,.77,.71));dark=material('outdoor metal',(.055,.053,.046));burgundy=material('faded burgundy canvas',(.29,.048,.073));grain(burgundy,(.20,.029,.043),(.36,.065,.088),45,.001)
changed_materials=[]
for o in scene.objects:
    if o.type!='MESH':continue
    for slot in o.material_slots:
        m=slot.material
        if not m:continue
        replacement=None
        if o.name.startswith('Syston v25 |') and m.name=='Shop v19 | brick relief':replacement=bricks[int(o.get('catalogue_id','B000')[1:])%5]
        elif o.name.startswith('Syston v25 |') and m.name=='Syston v25 | opaque blue-grey glazing':replacement=glazing
        elif o.name.startswith('Street') and any(s in o.name.lower() for s in ('road','carriageway')) and 'asphalt' in m.name.lower():replacement=road
        elif o.name.startswith('Street') and 'pavement' in o.name.lower():replacement=paving
        if replacement:slot.material=replacement;changed_materials.append(o.name)
group=[o for o in scene.objects if o.get('catalogue_id')=='B045']
anchor=next(o for o in group if 'upper facade' in o.name);basis=anchor.matrix_world.copy()
xs=[v.co.x for v in anchor.data.vertices];x0,x1=min(xs),max(xs);w=x1-x0
def box(name,x0,x1,y0,y1,z0,z1,m):
    me=bpy.data.meshes.new(name);me.from_pydata([(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]);me.materials.append(m);me.update()
    o=bpy.data.objects.new('Syston v27 | B045 | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['evidence']='Street capture 00233, April2026';made.append(o);return o
for o in group:
    if 'burgundy awning' in o.name:retire(o)
    if o.type=='FONT' and o.data.body=='COSTA COFFEE':
        o.data.size=.9;bpy.context.view_layer.update();localw=max(v[0] for v in o.bound_box)-min(v[0] for v in o.bound_box);o.scale=Vector((1,1,1))*(w*.8/localw)
    if 'upper sash glass' in o.name:
        vx=[v.co.x for v in o.data.vertices];vz=[v.co.z for v in o.data.vertices];a,c=min(vx),max(vx);z0,z1=min(vz),max(vz)
        for t in (1/3,2/3):box('fine upper window division',a+(c-a)*t-.018,a+(c-a)*t+.018,-.19,-.135,z0,z1,white)
        for t in (.27,.75):box('fine upper window rail',a,c,-.19,-.135,z0+(z1-z0)*t-.018,z0+(z1-z0)*t+.018,white)
for j in range(2):
    a=x0+1.1+j*(w-1.1)/2;c=x0+1.1+(j+1)*(w-1.1)/2-.05
    aw=box('sloping fabric awning',a,c,-1.34,.02,2.89,2.95,burgundy)
    for v in aw.data.vertices:v.co.z+=(v.co.y+1.34)*.29
    box('awning hanging valance',a,c,-1.36,-1.31,2.72,2.92,burgundy)
    box('awning front metal bar',a,c,-1.39,-1.34,2.87,2.93,dark)
for j in range(3):
    x=x0+2.1+j*(w-3.1)/3;y=-.85
    box('cafe table top',x-.33,x+.33,y-.28,y+.28,.74,.79,white)
    box('cafe table pedestal',x-.035,x+.035,y-.035,y+.035,.05,.74,dark)
    box('cafe table foot',x-.26,x+.26,y-.06,y+.06,.04,.08,dark)
    for sign in (-1,1):
        cx=x+sign*.54
        box('cafe chair seat',cx-.19,cx+.19,y-.19,y+.19,.43,.48,dark)
        for dx in (-.16,.16):
            for dy in (-.16,.16):box('cafe chair leg',cx+dx-.018,cx+dx+.018,y+dy-.018,y+dy+.018,.02,.44,dark)
        for dx in (-.17,-.085,0,.085,.17):box('cafe chair back slat',cx+dx-.014,cx+dx+.014,y+.17,y+.20,.47,.91,dark)
bpy.context.view_layer.update()
for name,(vs,fs) in protected.items():
    o=bpy.data.objects[name];assert vs==[tuple(o.matrix_world@v.co) for v in o.data.vertices],name;assert fs==[tuple(p.vertices) for p in o.data.polygons],name
for o in made:
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0;bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==original_hash
scene.camera=bpy.data.objects['Review v25 | 02_costa_and_town_square']
bpy.ops.wm.save_as_mainfile(filepath=str(out))
(dest/'validation.json').write_text(json.dumps({'input_sha256':original_hash,'output':str(out.relative_to(ROOT)),'preserved_mesh_geometry':len(protected),'material_assignment_count':len(changed_materials),'new_closed_solids':len(made),'archived':retired,'limits':['First appearance pass; positions and building sizes retained','Glazing reflective opaque scenery; no invented interiors','Costa details interpreted from capture00233; not surveyed','Blender only; no BO3 verification']},indent=2)+'\n')
# Same inspection light/camera before and after, temporary and unsaved.
def lighting():
    scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
    scene.render.resolution_x=1200;scene.render.resolution_y=820;scene.render.resolution_percentage=100
    scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
    ld=bpy.data.lights.new('Temporary comparison sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
def renders(label):
    lighting()
    for short,name in [('costa','02_costa_and_town_square'),('street','06_bridge_player')]:
        scene.camera=bpy.data.objects['Review v25 | '+name];scene.render.filepath=str(dest/(short+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
renders('after')
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene;renders('before')
print('V27_COMPLETE',out)
