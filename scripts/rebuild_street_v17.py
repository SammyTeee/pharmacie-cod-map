"""Editable street reconstruction from the October photo notes; Blender only."""
from pathlib import Path
import bpy, json, math, hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-street-rebuilt-v17.blend'
assert not OUT.exists(), 'Refuse to overwrite a reviewed version'
scene=bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene=scene
bpy.context.view_layer.update()
old_fronts={o.name:o for o in scene.objects if o.name.endswith('photographic front')}
# Save original v16 unchanged. Remove old scenery from scene links, retain its
# objects in an unlinked archive collection, avoiding exporter/render duplicates.
archived=[]
for cname in ('STREET | Opposite High Street photo fronts','STREET | Simple UK two-way road + pavements'):
    coll=bpy.data.collections[cname]
    coll.use_fake_user=True
    coll.name='ARCHIVE v16 | '+cname
    archived.extend(o.name for o in coll.all_objects)
    for s in bpy.data.scenes:
        if coll.name in s.collection.children:s.collection.children.unlink(coll)
# The old passage was directly beside the pub and crossed the new neighbour.
passage=bpy.data.objects.get('Street | left side passage')
if passage:
    archive=bpy.data.collections.new('ARCHIVE v16 | old pub-side passage');archive.use_fake_user=True
    archive.objects.link(passage)
    for c in list(passage.users_collection):
        if c!=archive:c.objects.unlink(passage)
    archived.append(passage.name)
coll=bpy.data.collections.new('STREET v17 | Photo-led connected High Street')
for s in bpy.data.scenes:
    if s.name.startswith(('01 ','03 ','04 ','05 ')):s.collection.children.link(coll)
for o in list(bpy.data.objects):
    if 'threshold' in o.name.lower() or ('street' in o.name.lower() and 'rear' in o.name.lower()):
        if o.name not in scene.objects:coll.objects.link(o)
made=[]; buildings=[]
def mat(name,color):
    m=bpy.data.materials.new('Street v17 | '+name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.85
    return m
brick=mat('warm red brick',(.29,.115,.064)); cream=mat('cream render',(.68,.63,.48)); slate=mat('slate',(.105,.125,.145))
white=mat('painted white joinery',(.82,.80,.72)); dark=mat('iron charcoal',(.035,.045,.05)); glass=mat('dark blue glazing',(.09,.17,.20))
green=mat('flooring olive',(.18,.25,.13)); blue=mat('shop blue',(.08,.16,.24)); red=mat('post office red',(.62,.035,.035))
orange=mat('wellbeing orange',(.78,.20,.035)); road=mat('asphalt',(.10,.115,.125)); pavement=mat('paving',(.44,.43,.39)); markings=mat('road white',(.82,.80,.71))
pink=mat('tactile pink paving',(.50,.24,.21)); yellow=mat('bollard yellow',(.90,.61,.035))
def mesh(name,verts,faces,m):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    o=bpy.data.objects.new('Street v17 | '+name,data);coll.objects.link(o);data.materials.append(m);made.append(o)
    o['evidence']='docs/STREET_PHOTO_RECONSTRUCTION.md; approximate gameplay dimensions'
    o['bo3_role']='Architecture; conversion and collision not yet verified'
    return o
def box(name,x0,x1,y0,y1,z0,z1,m):
    return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)
def roof(name,x0,x1,y0,y1,eaves,rise,gable=False):
    if not gable:
        mid=(y0+y1)/2
        verts=[(x0,y0,eaves),(x1,y0,eaves),(x1,y1,eaves),(x0,y1,eaves),(x0,mid,eaves+rise),(x1,mid,eaves+rise)]
        faces=[(0,3,2,1),(0,1,5,4),(4,5,2,3),(0,4,3),(1,2,5)]
    else:
        mid=(x0+x1)/2
        verts=[(x0,y0,eaves),(x1,y0,eaves),(mid,y0,eaves+rise),(x0,y1,eaves),(x1,y1,eaves),(mid,y1,eaves+rise)]
        faces=[(0,2,1),(3,4,5),(0,1,4,3),(0,3,5,2),(1,2,5,4)]
    return mesh(name+' pitched slate roof',verts,faces,slate)
textures={f['name']:f for f in json.loads((ROOT/'assets/street/v17/manifest.json').read_text())['fronts']}
def photo(name,x0,x1,y,z0,z1,opposite):
    f=textures[name];m=mat(name+' isolated photo',(.5,.5,.5))
    image=bpy.data.images.load(str(ROOT/f['derivative']),check_existing=True);image.pack()
    tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;tex.extension='EXTEND'
    m.node_tree.links.new(tex.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    verts=[(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)]
    o=mesh(name+' isolated facade',verts,[(0,1,2,3)] if not opposite else [(3,2,1,0)],m)
    uv=o.data.uv_layers.new(name='UVMap')
    coords=[(0,0),(1,0),(1,1),(0,1)] if not opposite else [(1,0),(0,0),(0,1),(1,1)]
    for p in o.data.polygons:
        for li in p.loop_indices:uv.data[li].uv=coords[o.data.loops[li].vertex_index]
    o['source']=f['source'];o['source_sha256']=f['source_sha256'];o['derivative']=f['derivative'];return o
def window(name,x,y,z,width,height,opposite=False):
    # Set frame slightly ahead of opaque glazing; no scenery interiors.
    d=1 if opposite else -1
    box(name+' glass',x-width/2,x+width/2,y-.06,y+.06,z,z+height,glass)
    yf=y+d*.10
    for xx in (x-width/2,x,x+width/2):box(name+' sash upright',xx-.035,xx+.035,yf-.035,yf+.035,z,z+height,white)
    for zz in (z,z+height*.5,z+height):box(name+' sash rail',x-width/2,x+width/2,yf-.035,yf+.035,zz-.035,zz+.035,white)
    box(name+' stone sill',x-width/2-.12,x+width/2+.12,yf-.13,yf+.13,z-.10,z,cream)
    box(name+' pale lintel',x-width/2-.10,x+width/2+.10,yf-.06,yf+.06,z+height,z+height+.16,cream)
def building(name,x0,x1,height,depth=11,opposite=True,texture=None,render=brick,gable=False):
    yf=-13 if opposite else 0
    y0,y1=(yf-depth,yf) if opposite else (yf,yf+depth)
    mass=box(name+' solid scenery mass',x0,x1,y0,y1,0,height,render)
    mass['enterable']=False
    roof(name,x0-.12,x1+.12,y0-.16,y1+.16,height,1.65 if not gable else 3.0,gable)
    box(name+' gutter',x0-.1,x1+.1,yf-.10,yf+.10,height-.08,height+.02,dark)
    dx=x0+.18
    box(name+' corner downpipe',dx-.045,dx+.045,yf-.14,yf+.14,.2,height,dark)
    if texture:photo(texture,x0,x1,yf+(.018 if opposite else -.018),.03,height,opposite)
    # Chimney stacks and pots are separate editable masses.
    cx=x0+(x1-x0)*.20;cy=(y0+y1)/2
    box(name+' chimney stack',cx-.36,cx+.36,cy-.38,cy+.38,height+1.05,height+2.55,brick)
    for j in (-.18,.18):box(name+' chimney pot',cx+j-.075,cx+j+.075,cy-.085,cy+.085,height+2.55,height+2.95,cream)
    buildings.append(dict(name=name,x=[x0,x1],y=[y0,y1],eaves=height,depth=depth,texture=texture,placement='Photographic order; gameplay-scale estimate'))
    return yf
def shopfront(name,x0,x1,height,color):
    yf=-12.94;w=x1-x0
    box(name+' fascia',x0,x1,yf-.12,yf+.12,2.80,3.35,color)
    box(name+' plinth',x0,x1,yf-.08,yf+.08,0,.45,cream)
    box(name+' window',x0+.18,x1-w*.27,yf-.08,yf+.08,.45,2.80,glass)
    box(name+' door',x1-w*.23,x1-.17,yf-.10,yf+.10,.05,2.80,color)
    for xx in (x0+.13,x1-w*.25,x1-.13):box(name+' joinery',xx-.045,xx+.045,yf-.13,yf+.13,.1,3.35,white)
    # Geometric placeholder lettering converted to mesh for future export.
    curve=bpy.data.curves.new(name+' sign','FONT');curve.body=name.upper();curve.align_x='CENTER';curve.size=min(.26,w/max(len(name),1)*1.5);curve.extrude=.001
    text=bpy.data.objects.new('Street v17 | '+name+' sign lettering',curve);coll.objects.link(text);text.location=((x0+x1)/2,yf+.145,2.95);text.rotation_euler=(math.pi/2,0,math.pi);curve.materials.append(white)
    text['bo3_role']='Review lettering; convert to mesh before export';made.append(text)
    for i in range(2):window(name+' upstairs '+str(i),x0+w*(.28+.44*i),-12.91,4.1,w*.20,1.55,True)
# Neighbours touch nominal pub frontage (fascia includes an overhang).
PUB_LEFT=-2.16;PUB_RIGHT=10.50
WLEFT=PUB_LEFT-8
building('Wreake Valley Flooring',WLEFT,PUB_LEFT,8.3,depth=15,opposite=False,texture='Wreake Valley Flooring')
building('Syston Dry Cleaners',PUB_RIGHT,PUB_RIGHT+6.7,8.3,depth=13,opposite=False,texture='Syston Dry Cleaners')
building('Nail and Spa shop',PUB_RIGHT+6.7,PUB_RIGHT+13.1,7.9,depth=12,opposite=False,texture='Nail and Spa shop')
# Follow the widening/skewed pub footprint at the rear of its neighbours.
# Keep the photographed front edges fixed while tapering their hidden backs.
for name,front_edge,rear_edge,depth in [('Wreake Valley Flooring',PUB_LEFT,-5.0,15),('Syston Dry Cleaners',PUB_RIGHT,12.0,13)]:
    o=next(o for o in made if o.name=='Street v17 | '+name+' solid scenery mass')
    for v in o.data.vertices:
        if abs(v.co.x-front_edge)<.001 and v.co.y>.1:v.co.x=rear_edge
    o['side_boundary']='Tapered rear edge to clear skewed pub; approximate until floorplan survey'
# Shared roof above pub frontage only: preserve detailed interior and rear rooms.
roof('Pharmacie shared terrace',PUB_LEFT,PUB_RIGHT,-.18,9.5,8.3,1.65)
for z in (5.40,5.62):box('Wreake blue-grey brick band',WLEFT,PUB_LEFT,-.075,-.02,z,z+.09,blue)
box('Wreake alley return band',WLEFT-.04,WLEFT+.04,0,15,5.40,5.52,blue)
box('Wreake alley boundary low wall',WLEFT-2.80,WLEFT-2.58,.30,11,.0,.85,brick)
for y in (.4,5.5,10.5):box('Wreake alley boundary white post',WLEFT-2.88,WLEFT-2.50,y-.10,y+.10,0,1.15,white)
box('Wreake vertical side advertisement',WLEFT-.045,WLEFT-.02,.5,2.2,2,4.9,green)
# Move passage outside flooring shop; rear connector beyond neighbour's 15m depth.
box('Outer-left alley walkable floor',WLEFT-2.58,WLEFT,0,32,-.25,0,pavement)
box('Alley rear route connector',WLEFT-2.58,-5.8,31,33,-.25,0,pavement)
# Extended opposite row retains the approved five photo fronts.
for name,x0,x1,h in [('Fox and Hounds',-15,-3,5.4),('Aston and Co',-3,1,7.1),('Syston Mini Market',1,10,7.2),('Lets Move estate agents',10,17,6.9),('Floral Fantasy',17,24,7.0)]:
    building(name,x0,x1,h,depth=12,texture=name,render=cream if name in ('Fox and Hounds','Aston and Co') else brick)
# Protruding upper bays are real relief, rather than relying on flat photographs.
for name,cx in [('Lets Move',13.5),('Floral Fantasy',20.5)]:
    box(name+' white upper bay body',cx-1.3,cx+1.3,-13.08,-12.38,4.2,6.2,white)
    window(name+' upper bay',cx,-12.29,4.35,2.25,1.65,True)
    roof(name+' bay hood',cx-1.42,cx+1.42,-13.18,-12.22,6.20,.50)
box('Floral narrow blue access door',23.35,23.95,-12.96,-12.87,.03,2.80,blue)
box('Aston narrow dark access door',.15,.75,-12.96,-12.87,.03,2.80,dark)
building('Pasha Barber',24,29,6.9,depth=13);shopfront('Pasha Barber',24,29,6.9,dark)
building('HM private entrance',29,30,6.9,depth=13)
box('HM narrow white access door',29.15,29.85,-12.95,-12.87,0,2.8,white)
building('Papermoon',30,36,6.9,depth=13);shopfront('Papermoon',30,36,6.9,blue)
building('Post Office',36,45,6.9,depth=13,texture='Post Office')
box('Post Office ATM inset',36.35,37.1,-12.96,-12.86,.85,2.10,dark)
box('Post Office ATM screen',36.46,36.99,-12.86,-12.84,1.40,1.78,glass)
box('Red post box',35.7,36.05,-12.52,-12.10,0,1.5,red)
# Keep separate 3m lane between Post Office and Natural Wellbeing.
box('Natural Wellbeing side lane',45,48,-30,-13,-.25,0,pavement)
building('Natural Wellbeing',48,57,7.7,depth=17,gable=True)
photo('Natural Wellbeing',48,57,-12.96,.03,3.6,True)
for i in (0,1,2,3):window('Natural Wellbeing paired sash '+str(i),49.7+i*1.85,-12.92,4.35,1.18,1.85,True)
mesh('Natural Wellbeing cream gable infill',[(48,-12.96,7.7),(57,-12.96,7.7),(52.5,-12.96,10.6)],[(0,1,2)],cream)
for x in (49.5,50.5,51.5,52.5,53.5,54.5,55.5):
    top=10.6-abs(x-52.5)/4.5*2.9
    box('Natural Wellbeing gable timber',x-.08,x+.08,-12.96,-12.88,7.7,top,dark)
for x in (49,52,55):box('Natural Wellbeing grey bollard',x-.075,x+.075,-11.9,-11.75,0,.95,dark)
# Pub-side unspecified fronts: visibly documented placeholders, no invented names.
for i,(x0,x1,h) in enumerate([(23.6,30,8.0),(30,37,8.7),(37,44,8.0),(44,51,8.3),(51,59,7.9)]):
    name='Pub-side placeholder '+str(i+1);building(name,x0,x1,h,depth=14,opposite=False)
    box(name+' coloured fascia',x0,x1,-.16,-.02,2.8,3.5,green if i==1 else blue)
    for j in (0,1,2):
        wx=x0+(x1-x0)*(j+.5)/3
        window(name+' upper '+str(j),wx,-.09,4.8,1.25,1.85)
        box(name+' display',wx-.82,wx+.82,-.09,-.02,.50,2.80,glass)
for i,x0 in enumerate((-29,-22)):
    building('Junction distant placeholder '+str(i+1),x0,x0+7,7.0,depth=13,opposite=False)
# Fuller street with kerbs/build-out, crossing and junction stub.
box('High Street continuous road',-34,66,-10.4,-3,-.32,-.08,road)
box('Pub-side extended pavement',-34,66,-3,0,-.25,0,pavement)
box('Opposite extended pavement',-34,66,-13,-10.4,-.25,0,pavement)
for y in (-3.03,-10.37):box('Long street kerb',-34,66,y-.075,y+.075,-.18,0,cream)
box('Floral pavement build-out',10.2,24.5,-10.4,-9.65,-.25,0,pavement)
box('Floral build-out kerb',10.2,24.5,-9.72,-9.60,-.18,0,cream)
# Parking bay on opposite side; repeated tiny tiles avoided for exporter size.
for y in (-9.40,-7.30):box('Opposite parking bay white edge',-1,9.7,y-.045,y+.045,-.075,-.065,markings)
for x in (-1,9.7):box('Parking bay end',x-.045,x+.045,-9.4,-7.3,-.075,-.065,markings)
box('Crossing tactile pub side',39,43,-3,-1.8,.002,.012,pink)
box('Crossing tactile opposite',39,43,-11.65,-10.4,.002,.012,pink)
for x in (39.3,42.7):box('Crossing carriageway transverse line',x-.045,x+.045,-10.4,-3,-.075,-.065,markings)
for x in (28,30,32,34,36,46,48,50,52,54):
    # Alternating slanted approach strips, represented as shallow convex meshes.
    y0=-6.9; y1=-5.9 if int(x)%4==0 else -7.9
    mesh('Crossing zigzag approach',[(x,y0,-.07),(x+.10,y0,-.07),(x+1.30,y1,-.07),(x+1.20,y1,-.07)],[(0,1,2,3)],markings)
for x,y in ((39,-2.65),(43,-10.85)):
    box('Crossing signal pole',x-.065,x+.065,y-.065,y+.065,0,3.2,dark)
    box('Crossing signal head',x-.19,x+.19,y-.17,y+.17,2.40,3.15,dark)
    box('Crossing push button',x-.14,x+.14,y-.14,y+.14,1.0,1.25,yellow)
    for z,c in ((2.52,green),(2.78,orange),(3.03,red)):box('Crossing lamp',x-.105,x+.105,y+.17,y+.185,z-.085,z+.085,c)
box('Fox junction branch road',-30,-19,-37,-3,-.32,-.08,road)
box('Fox junction traffic island',-25.5,-23,-13.5,-10.5,-.20,.04,pavement)
box('Junction keep-left bollard',-24.7,-24.1,-12.25,-11.8,.04,1.1,yellow)
box('Junction keep-left blue face',-24.64,-24.16,-11.80,-11.77,.45,.96,blue)
# Scenery setbacks fill distant ends without implying surveyed shop identities.
for x0 in (59,66):building('Crossing distant placeholder '+str(x0),x0,x0+7,7.5,depth=12,opposite=True)
# Purposeful review anchors; never claim stock prefabs have been fitted here.
anchors=bpy.data.collections.new('GAMEPLAY v17 | Proposed anchors - not exported')
scene.collection.children.link(anchors)
anchor_specs=[('Street start / player review',(5.5,-2,.10)),('Quick Revive proposal',(12,-1.6,.1)),('Rear yard box proposal',(-5.5,32,.1)),('Rear service power proposal',(7,28,.1))]
for name,loc in anchor_specs:
    o=bpy.data.objects.new('PLAN v17 | '+name,None);anchors.objects.link(o);o.location=loc;o.empty_display_type='ARROWS';o.empty_display_size=.65;o.hide_render=True;o['status']='Proposed anchor only; prefab bounds and gameplay unverified'
# Persistent review cameras make the updated file immediately inspectable.
cameras=[]
for name,pos,target,lens in [('Pub frontage',(4,-8.5,4.8),(4,0,4.7),14),('Whole street',(18,-6,52),(18,-6,0),19),('Alley and rear route',(-25,21,24),(-9,16,0),23),('Crossing row',(42,-3,5),(40,-13,3.8),22)]:
    data=bpy.data.cameras.new('Review v17 | '+name);data.lens=lens
    o=bpy.data.objects.new(data.name,data);scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();cameras.append(o)
scene.camera=cameras[1]
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.shading.type='SOLID'
        area.spaces.active.shading.color_type='TEXTURE'
    elif area.type=='CONSOLE':area.type='VIEW_3D'
bpy.context.view_layer.update()
assert abs(buildings[0]['x'][1]-PUB_LEFT)<1e-6
assert abs(buildings[1]['x'][0]-PUB_RIGHT)<1e-6
assert WLEFT-2.58 < WLEFT and buildings[0]['y'][1]<31
assert bpy.data.objects.get('Ground | continuous front entrance threshold') or any('threshold' in o.name.lower() for o in scene.objects)
assert len([b for b in buildings if b['name']=='Natural Wellbeing'])==1
for f in textures.values():assert hashlib.sha256((ROOT/f['source']).read_bytes()).hexdigest()==f['source_sha256']
manifest={'version':17,'input':'pharmacie-entrance-fixed-v16.blend','output':OUT.name,'new_objects':len(made),'buildings':buildings,'alley':{'x':[WLEFT-2.58,WLEFT],'y':[0,32],'rear_connector_y':[31,33],'width_m':2.58},'archived_v16_objects':archived,'anchors':[{'name':n,'location':p,'status':'Proposal, not placed BO3 prefab'} for n,p in anchor_specs],'preserved':'Pub interior, stairs and v16 threshold; source photo hashes verified','limitations':['Approximate gameplay-scaled blockout, not survey or 1:1','New Papermoon/Pasha fronts are geometry placeholders','Original photo occlusions/perspective and some cropped roof pixels remain','Rear alley connection inferred, not photographed','No Radiant export, compiler, collision or gameplay verification'],'radiant_rebuilt':False,'runtime_verified':False}
(ROOT/'assets/blender/street-rebuilt-v17-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
scene['gameplay_version']='v17 photo-led connected street; Blender review only'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
print(json.dumps({'saved':str(OUT),'new_objects':len(made),'buildings':len(buildings),'alley_width':2.58,'sources_unchanged':True}))
