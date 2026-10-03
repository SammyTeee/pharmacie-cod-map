"""Preserve live v03, make editable gameplay-scale v04; never build Radiant."""
from pathlib import Path
import json
import math
import bpy
from mathutils import Matrix, Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-gameplay-space-v04.blend'
BACKUP=ROOT/'assets/blender/pharmacie-v03-before-gameplay-edit.blend'
assert Path(bpy.data.filepath).name=='pharmacie-photo-interior-v03.blend'
if OUT.exists() or BACKUP.exists():
    raise RuntimeError('Preserve existing gameplay versions before rerunning')
if bpy.context.mode!='OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
# Include unsaved user changes in the safety copy; do not reload a stale file.
bpy.ops.wm.save_as_mainfile(filepath=str(BACKUP),copy=True)
scene=bpy.data.scenes['05 Interior - photo-led dressing']
bpy.context.window.scene=scene
bpy.context.view_layer.update()

door_records=[]
for hinge in [o for o in bpy.data.objects if o.name.endswith('| hinge')]:
    base=hinge.name[:-len(' | hinge')]
    jamb0=bpy.data.objects[base+' | jamb 0']
    jamb1=bpy.data.objects[base+' | jamb 1']
    a=jamb0.matrix_world.translation.copy()
    b=jamb1.matrix_world.translation.copy()
    direction=b-a; direction.z=0
    width=direction.length
    direction.normalize()
    extra=max(0,.95-width)
    left=a-direction*extra/2
    right=b+direction*extra/2
    center=(a+b)/2
    if extra>0:
        jamb0.location-=direction*extra/2
        jamb1.location+=direction*extra/2
        hinge.location-=direction*extra/2
        # Extend lintel and frame head along the wall, preserving UV data.
        for ending in ('frame head',):
            obj=bpy.data.objects[base+' | '+ending]
            obj.data=obj.data.copy()
            inv=obj.matrix_world.inverted()
            for v in obj.data.vertices:
                p=obj.matrix_world@v.co
                p+=direction*(p-center).dot(direction)*(extra/width)
                v.co=inv@p
        group=base.split(' | door ')[0]
        lintel=bpy.data.objects.get(group+' | lintel '+base.split(' | door ')[1])
        if lintel:
            lintel.data=lintel.data.copy(); inv=lintel.matrix_world.inverted()
            for v in lintel.data.vertices:
                p=lintel.matrix_world@v.co
                p+=direction*(p-center).dot(direction)*(extra/width)
                v.co=inv@p
        # Trim adjacent wall ends at the old portal edges.
        for obj in list(bpy.data.objects):
            if obj.type!='MESH' or not obj.name.startswith(group+' | '):continue
            if not any(s in obj.name for s in ('| pier','| wall end')):continue
            inv=obj.matrix_world.inverted(); edits=[]
            for v in obj.data.vertices:
                p=obj.matrix_world@v.co
                coordinate=(p-a).dot(direction)
                if abs(coordinate)<.025:edits.append((v.index,p-direction*extra/2))
                elif abs(coordinate-width)<.025:edits.append((v.index,p+direction*extra/2))
            if edits:
                obj.data=obj.data.copy()
                for index,p in edits:obj.data.vertices[index].co=inv@p
        for child in hinge.children:
            child.location.x*=((width+extra)/width)
            child.scale.x*=((width+extra)/width)
    tangent_angle=math.atan2(direction.y,direction.x)
    old_angle=hinge.rotation_euler.z-tangent_angle
    sign=1 if math.sin(old_angle)>=0 else -1
    hinge.rotation_euler.z=tangent_angle+sign*math.pi/2
    hinge['gameplay_open_degrees']=90
    door_records.append({'name':base,'opening_before_m':width,'opening_after_m':width+extra,
                         'approx_clear_after_scale_m':(width+extra-.08)*1.5})

# Fully open both front leaves against the recessed side walls.
for name in ('Front | entrance leaf 1 hinge','Front | entrance leaf 2 hinge'):
    bpy.data.objects[name].rotation_euler.z=math.pi/2
    bpy.data.objects[name]['gameplay_open_degrees']=90

# The bar's return is the tightest section of the left-hand circulation aisle.
for name in ('Bar | cabinet run 1','Bar | counter top 1'):
    bpy.data.objects[name].location.x+=.25
    bpy.data.objects[name]['gameplay_adjustment']='Moved 0.25m toward bar interior to widen left route'

# One editable root scales original geometry, references and furnishings once.
# Existing parent/child groups remain intact.
for model_scene in bpy.data.scenes:
    for model_layer in model_scene.view_layers:model_layer.update()
scale_collection=bpy.data.collections.new('GAMEPLAY | Adjustable pub scale')
for s in bpy.data.scenes:s.collection.children.link(scale_collection)
root=bpy.data.objects.new('GAMEPLAY | Pub scale 1.50 - frontage 10.5m',None)
scale_collection.objects.link(root)
root.empty_display_type='PLAIN_AXES';root.empty_display_size=2
roots=[o for o in bpy.data.objects if o!=root and o.parent is None and o.type not in ('CAMERA','LIGHT')]
for obj in roots:
    matrix=obj.matrix_world.copy()
    obj.parent=root
    obj.matrix_parent_inverse=Matrix.Identity(4)
    obj.matrix_world=matrix
root.scale=(1.5,1.5,1.5)
root['estimated_original_frontage_m']=7.0
root['gameplay_scale_factor']=1.5
root['note']='Gameplay exaggeration requested after first BO3 test; not a survey correction'
for obj in bpy.data.objects:
    if obj.type in ('CAMERA','LIGHT') and obj.parent is None:
        obj.location*=1.5
        if obj.type=='CAMERA' and obj.data.type=='ORTHO':obj.data.ortho_scale*=1.5
        if obj.type=='LIGHT':obj.data.energy*=2.25

street=bpy.data.collections.new('STREET | Simple UK two-way road + pavements')
markers=bpy.data.collections.new('GAMEPLAY | Planned spawns and routes - not exported')
for s in bpy.data.scenes:
    if s.name.startswith(('01','03','04','05')):s.collection.children.link(street)
    if s.name.startswith(('01','02','03','05')):s.collection.children.link(markers)

def material(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.85
    return m
asphalt=material('Street | charcoal asphalt',(.055,.06,.066))
paving=material('Street | grey pavement',(.28,.29,.30))
white=material('Street | worn white road paint',(.82,.82,.77))
yellow=material('Street | double yellow road paint',(.84,.58,.025))

def box(name,bounds,mat,collection=street):
    x0,x1,y0,y1,z0,z1=bounds
    verts=[(x,y,z) for z in (z0,z1) for y in (y0,y1) for x in (x0,x1)]
    faces=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);collection.objects.link(obj)
    mesh.materials.append(mat)
    obj['role']='Editable street blockout; inferred scenery, not photo-surveyed'
    return obj

box('Street | two-way carriageway',(-20,30,-10.4,-3,-.30,-.08),asphalt)
box('Street | pub-side pavement',(-20,30,-3,0,-.25,0),paving)
box('Street | opposite pavement',(-20,30,-13,-10.4,-.25,0),paving)
box('Street | pub-side kerb',(-20,30,-3.12,-3,-.13,0),paving)
box('Street | opposite kerb',(-20,30,-10.4,-10.28,-.13,0),paving)
for i,x in enumerate(range(-18,30,6)):
    box(f'Street | dashed white centre line {i+1:02}',(x,x+3,-6.76,-6.64,-.079,-.073),white)
for edge,ys in [('pub',(-3.28,-3.48)),('opposite',(-10.12,-9.92))]:
    for j,y in enumerate(ys):
        box(f'Street | {edge} double yellow {j+1}',(-20,30,y-.045,y+.045,-.079,-.073),yellow)
# A simple side/rear floor connects the rear-left outside door to the street.
box('Street | left side passage',(-5,-.55,0,33,-.25,0),paving)
box('Street | rear exit landing',(-5,2,30.5,34,-.25,0),paving)

def marker(name,p,role,facing=90):
    o=bpy.data.objects.new(name,None);markers.objects.link(o)
    o.location=p;o.rotation_euler.z=math.radians(facing)
    o.empty_display_type='ARROWS';o.empty_display_size=.8
    o['bo3_role']=role;o['facing_degrees']=facing;o['status']='Planned; no Radiant rebuild yet'
    return o
player=marker('SPAWN | player outside - facing pub',(6.37,-2,0.1),'initial_spawn')
spawn_records=[]
for i,p in enumerate([(-12,-6.7,.1),(20,-6.7,.1),(-3.5,32,.1),(5.2,22.5,4.9)]):
    o=marker(f'ZOMBIES | planned {i+1} '+['street left','street right','rear outside','upstairs'][i],p,'riser_location')
    o['route_goal']='Pub entrance' if i<2 else ('Rear-left door' if i==2 else 'L stair arrival, then descend')
    spawn_records.append({'name':o.name,'position_m':p,'route_goal':o['route_goal']})
guide_mat=material('Gameplay | player clearance guide',(.15,.8,.25))
guide=box('CLEARANCE | BO3 player 32x32x72 map units',(5.96,6.78,-2.41,-1.59,.1,1.929),guide_mat,markers)
guide.display_type='WIRE';guide.hide_render=True
guide['note']='0.813m square by 1.829m high approximate player hull; guide only'

bpy.context.view_layer.update()
# Widen the view to include the street while preserving the interior camera.
assembled=bpy.data.scenes['03 Both floors - assembled exterior']
cam=assembled.camera
cam.location=(26,-28,25)
cam.rotation_euler=(Vector((4,7,2))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=53
for s in bpy.data.scenes:
    s['gameplay_version']='v04 - Blender edits only; BO3 still runs v03 export'
    s['gameplay_scale_factor']=1.5
manifest={'file':str(OUT),'safety_copy':str(BACKUP),'scale_factor':1.5,
    'estimated_gameplay_frontage_m':10.5,'scale_is_gameplay_exaggeration':True,
    'door_open_angle_degrees':90,'doorways':door_records,'bar_return_shift_m':.25,
    'street':'50m long; two-way asphalt, dashed white centre, double yellow edges, pavements; illustrative proportions',
    'player_spawn_m':list(player.location),'zombie_markers':spawn_records,
    'radiant_rebuilt':False,'runtime_verified':False}
(ROOT/'assets/blender/gameplay-space-v04-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
bpy.context.window.scene=scene
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'saved':str(OUT),'backup':str(BACKUP),'doorways_adjusted':len(door_records),
        'min_estimated_clear_width_m':min(d['approx_clear_after_scale_m'] for d in door_records),
        'street_objects':len(street.objects),'scale_factor':1.5,'radiant_rebuilt':False}
