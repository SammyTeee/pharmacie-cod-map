"""Photo-led Melton scenery from the small, numbered street dossiers.

Run in background Blender with the saved v24 checkpoint. No source images are
embedded: signs are geometric lettering, depths/chainages are gameplay estimates.
"""
from pathlib import Path
import bpy, math, json, hashlib, bmesh
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/blender/pharmacie-syston-street-v25.blend'
assert Path(bpy.data.filepath).name=='pharmacie-taraj-opposite-v24.blend'
assert not OUT.exists(), 'Never overwrite an editable milestone'
scene=bpy.data.scenes['03 Both floors - assembled exterior']; bpy.context.window.scene=scene
source=Path(bpy.data.filepath); source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
report22=json.loads((ROOT/'recon/v22/validation.json').read_text())
path=[Vector(p) for p in report22['melton_centreline']]
lengths=[0]
for a,b in zip(path,path[1:]): lengths.append(lengths[-1]+(b-a).length)

def frame(s,side=1,offset=7.2):
    s=max(0,min(s,lengths[-1]-.001))
    i=next(i for i in range(len(path)-1) if lengths[i+1]>=s)
    u=(path[i+1]-path[i]).normalized(); n=Vector((-u.y,u.x))*side
    return path[i]+u*(s-lengths[i])+n*offset,u,n

state=json.loads((ROOT/'references/streetview-capture/taraj-to-pharmacie/walk-state.json').read_text())
stops=state['completed_stops']; distances=[0]
for a,b in zip(stops,stops[1:]):
    dx=(b['longitude']-a['longitude'])*111320*math.cos(math.radians(a['latitude']))
    dy=(b['latitude']-a['latitude'])*111320
    distances.append(distances[-1]+math.hypot(dx,dy))
# Tie the photographed route to retained, gameplay-enlarged road and Taraj.
taraj=json.loads((ROOT/'recon/v24/validation.json').read_text())
tp=Vector(taraj['road_pivot']); nearest=[]
for i,(a,b) in enumerate(zip(path,path[1:])):
    u=(b-a).normalized(); t=max(0,min((tp-a).dot(u),(b-a).length))
    nearest.append(((tp-(a+u*t)).length,lengths[i]+t))
taraj_s=min(nearest)[1]; route_scale=(taraj_s-18)/distances[-1]
stop_s={r['stop']:taraj_s-d*route_scale for r,d in zip(stops,distances)}

archive=bpy.data.collections.new('ARCHIVE v24 | Generic Melton scenery');archive.use_fake_user=True
retired=[]
for ob in list(scene.objects):
    if ob.name.startswith(('Street v22 | Melton placeholder','Street v22 | Costa vicinity','Street v22 | Roundabout central low island','Street v22 | Roundabout white island marking')):
        archive.objects.link(ob)
        for col in list(ob.users_collection):
            if col!=archive:col.objects.unlink(ob)
        retired.append(ob.name)
protected={ob.name:([tuple(ob.matrix_world@v.co) for v in ob.data.vertices],[tuple(p.vertices) for p in ob.data.polygons]) for ob in scene.objects if ob.type=='MESH'}
coll=bpy.data.collections.new('STREET v25 | Catalogue-led Syston scenery')
for sc in bpy.data.scenes:
    if 'STREET v22 | Melton Road and Taraj blockout' in sc.collection.children:sc.collection.children.link(coll)
made=[]; current='F001'; basis=Matrix.Identity(4)

def mat(name,color,roughness=.7):
    m=bpy.data.materials.new('Syston v25 | '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=roughness
    return m

cream=mat('stone and cream',(.72,.69,.58));white=mat('white joinery',(.83,.83,.78))
dark=mat('dark metal',(.035,.043,.042));glass=mat('opaque blue-grey glazing',(.105,.17,.20),.28)
brick=bpy.data.materials['Shop v19 | brick relief'];slate=bpy.data.materials['Street v17 | slate']
blue=mat('retail blue',(.035,.11,.42));green=mat('retail green',(.025,.27,.12));red=mat('retail red',(.49,.028,.035));burgundy=mat('Costa burgundy',(.24,.027,.064));teal=mat('Bistro teal',(.025,.24,.24))
orange=mat('B and M orange',(.92,.22,.035));grey=mat('painted grey',(.27,.29,.28));water=mat('brook',(.07,.21,.19));roadwhite=bpy.data.materials['Street v17 | road white']

def mesh(name,verts,faces,m):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();me.materials.append(m)
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new('Syston v25 | '+current+' | '+name,me);coll.objects.link(ob);ob.matrix_world=basis.copy();made.append(ob)
    ob['catalogue_id']=current;ob['evidence']='docs/street-catalogue/entries/'+current+'.md'
    ob['status']='Approximate closed static scenery; Blender only; engine export pending'
    return ob

def box(name,x0,x1,y0,y1,z0,z1,m):
    assert x1>x0 and y1>y0 and z1>z0, name
    return mesh(name,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)

def setframe(s,side=1,offset=7.2):
    global basis
    p,u,n=frame(s,side,offset)
    # x follows the frontage; y points into building. Right handed on both sides.
    x=Vector((n.y,-n.x))
    basis=Matrix(((x.x,n.x,0,p.x),(x.y,n.y,0,p.y),(0,0,1,0),(0,0,0,1)))

def lettering(body,z,width,m=white,y=-.20,size=.42,x=0):
    cu=bpy.data.curves.new(current+' '+body,'FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=size;cu.extrude=.006;cu.materials.append(m)
    ob=bpy.data.objects.new('Syston v25 | '+current+' | '+body,cu);coll.objects.link(ob)
    ob.matrix_world=basis@Matrix.Translation((x,y,z))@Matrix.Rotation(math.pi/2,4,'X');made.append(ob)
    ob['catalogue_id']=current;ob['status']='Sharp geometric text; wording/occupancy follows photographed date'
    bpy.context.view_layer.update()
    if ob.dimensions.length>0:
        # Local text width remains independent of world frontage orientation.
        xs=[v[0] for v in ob.bound_box];w=max(xs)-min(xs)
        if w>width:ob.scale*=width/w
    return ob

def window(name,x,z,w,h,joinery=white,y=-.12,divisions=2):
    box(name+' glass',x-w/2,x+w/2,y,y+.07,z,z+h,glass)
    for xx in (x-w/2,x+w/2):box(name+' upright',xx-.045,xx+.045,y-.055,y+.045,z-.06,z+h+.06,joinery)
    for zz in (z,z+h):box(name+' rail',x-w/2-.06,x+w/2+.06,y-.055,y+.045,zz-.045,zz+.045,joinery)
    box(name+' sill',x-w/2-.13,x+w/2+.13,y-.16,y+.06,z-.14,z-.065,cream)
    for j in range(1,divisions):
        xx=x-w/2+w*j/divisions;box(name+' mullion',xx-.027,xx+.027,y-.045,y+.01,z,z+h,joinery)
    box(name+' transom',x-w/2,x+w/2,y-.045,y+.01,z+h*.51-.027,z+h*.51+.027,joinery)

def gable(name,x,w,base,rise,depth=10):
    pts=[(x-w/2,base),(x+w/2,base),(x,base+rise)]
    mesh(name,[(xx,y,z) for y in (0,depth) for xx,z in pts],[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],brick)
    for sign in (-1,1):
        a=Vector((x+sign*w/2,-.07,base));b=Vector((x,-.07,base+rise));u=(b-a).normalized();n=Vector((-u.z,0,u.x))*.085
        vs=[a-n,b-n,b+n,a+n]
        mesh(name+' roof verge',[(v.x,y,v.z) for y in (-.17,depth+.12) for v in vs],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],slate)

short={'B002':'Costcutter Carpets & Beds','B003':'MAN-MADE','B004':'HALLS OF SYSTON','B006':'THE STUDIO','B007':'delish','B008':'GROVE','B009':'FOX BARBERS','B010':'Newton Fallowell','B011':'SYSTON HOUSE','B012':'VISTA','B013':'FLAMES','B014':'BANKING HUB','B015':'SPECSAVERS','B016':"TODAY'S CATCH",'B017':'Age UK','B018':'mind','B019':'LOROS','B020':'SUBWAY','B021':'William HILL','B022':'SMITH HAMYLTON','B023':'BYRITE','B024':'GREGGS','B025':'Hays Travel','B026':'Sunlit Chemist','B027':'B&M','B028':'TOWN SQUARE','B029':'MARINE','B030':'WE VAPE','B031':'TOWN SQUARE','B032':'AMY CLARKE HAIR','B033':'GLO','B034':'GOLDEN BARBER','B035':'Designer Daisies','B036':'SYSTON JEWELLERS','B037':'','B038':'THE FOOD WAREHOUSE','B039':'cardfactory','B040':'SAVERS','B041':'SYSTON DIY','B042':'Spencers','B043':'SYSTON SIZZLER','B044':'BETFRED','B045':'COSTA COFFEE','B046':'JOSIAH HINCKS','B047':'BISTRO OGGI','B051':'Oxfam'}
blueids={'B002','B010','B012','B016','B024','B025','B027','B028','B042'}
greenids={'B004','B015','B018','B020','B031','B051'}
redids={'B011','B013','B038','B044','B046'}
specs=[]
for sideword,side in [('east',1),('west',-1)]:
    es=[json.loads(p.read_text()) for p in sorted((ROOT/'docs/street-catalogue/entries').glob('B*.json'))]
    es=[e for e in es if e['id'] in short and e['side']==sideword]
    es.sort(key=lambda e:stop_s[e['anchor_stop']]-e['along_offset_m_estimate']*route_scale)
    ss=[stop_s[e['anchor_stop']]-e['along_offset_m_estimate']*route_scale for e in es]
    # The small markers are estimates. Preserve order, resolve compressed IDs,
    # fit contiguous facade cells; avoid inventing independently overlapping parcels.
    for i in range(1,len(ss)):ss[i]=max(ss[i],ss[i-1]+5.0)
    if side==1:
        maxs=taraj_s-13
        if ss[-1]>maxs:
            for i in reversed(range(len(ss))):ss[i]=min(ss[i],maxs-(len(ss)-1-i)*5.0)
    for i,(e,s) in enumerate(zip(es,ss)):
        left=(ss[i-1]+s)/2 if i else s-5.5
        right=(ss[i+1]+s)/2 if i+1<len(ss) else s+5.5
        w=right-left-.30;s=(left+right)/2;current=e['id'];setframe(s,side)
        fascia=blue if current in blueids else green if current in greenids else red if current in redids else grey
        if current=='B045':fascia=burgundy
        if current=='B047':fascia=teal
        if current in ('B033','B041'):fascia=dark
        upper=cream if current in ('B041','B044') else grey if current=='B043' else brick
        h=9.1 if current in ('B027','B028','B045') else 8.9
        box('rear scenery mass',-w/2,w/2,.9,10,0,h,brick)
        box('upper facade',-w/2,w/2,0,1.05,4.1,h,upper)
        box('display backing',-w/2,w/2,.75,.90,0,4.1,dark)
        box('fascia',-w/2,w/2,-.15,.20,3.38,4.1,fascia)
        box('fascia crown',-w/2-.04,w/2+.04,-.24,.24,4.06,4.17,cream if current in ('B014','B033') else fascia)
        lettering(short[current],3.73,w-.5)
        box('lower plinth',-w/2,w/2,-.10,.80,0,.38,fascia)
        # Closed recessed door at the end, separate from two display bays.
        doorx=-w/2+.70
        window('recessed entrance',doorx,.38,.95,2.83,fascia,y=.38,divisions=1)
        box('door kickplate',doorx-.45,doorx+.45,.29,.42,.10,.70,fascia)
        box('door handle',doorx+.23,doorx+.26,.22,.28,1.15,1.6,cream)
        rest=w-1.65;displayw=max(.8,(rest-.35)/2)
        for j in range(2):window('display bay',-w/2+1.6+(j+.5)*rest/2,.45,displayw,2.83,fascia,divisions=1)
        for xx in (-w/2+.07,w/2-.07):box('front pilaster',xx-.065,xx+.065,-.19,.32,0,4.17,fascia)
        count=max(1,int(w/2.9));uw=min(1.68016,w/count-.55)
        for j in range(count):
            x=-w/2+(j+.5)*w/count
            window('upper sash',x,5.865,uw,2.61,white if current in ('B041','B044','B045') else dark)
        box('eaves gutter',-w/2-.10,w/2+.10,-.23,.14,h-.08,h+.12,dark)
        box('roof cap',-w/2-.12,w/2+.12,-.05,10.15,h,h+.25,slate)
        box('rainwater pipe',w/2-.16,w/2-.09,-.22,-.13,.25,h,dark)
        if current in ('B027','B028','B045'):
            for j in range(2 if current in ('B027','B045') else 1):
                num=2 if current in ('B027','B045') else 1
                gable('brick gable',-w/2+(j+.5)*w/num,w/num,h,1.5)
        if current=='B027':
            box('projecting upper bay apron',-.90,.90,-.45,.08,5.5,5.85,brick)
            window('projecting tall bay',0,5.865,1.68016,2.61,dark,y=-.45,divisions=1)
            lettering('BIG BRANDS  BIG SAVINGS',1.9,w*.75,orange,y=-.21,size=.27)
            for xx in (-w/2+.15,w/2-.15):box('tall brick pier',xx-.12,xx+.12,-.32,.24,0,h+.9,brick)
        if current=='B045':
            # Projected canopy, patio wall and handrail; no photographic plane.
            aw=box('burgundy awning',-w/2+1.1,w/2,-1.25,.05,2.90,3.06,burgundy)
            box('patio low wall',-w/2+1.4,w/2,-1.75,-1.50,0,.60,brick)
            for x in [(-w/2+1.5)+i*.55 for i in range(max(1,int((w-1.5)/.55)))]:box('patio rail',x,x+.035,-1.7,-1.65,.6,1.04,dark)
            box('patio handrail',-w/2+1.4,w/2,-1.73,-1.63,1.02,1.08,dark)
        if current=='B031':
            box('passage dark recess',-.8,.8,.72,.75,.05,3.37,dark)
        if current=='B044':
            gable('ornamented pale pediment',0,w*.65,h,1.1,depth=.28)
        specs.append({'id':current,'name':e['name'],'chainage_m_estimate':round(s,3),'width_m_estimate':round(w,3),'side':sideword,'photos':e['primary_photos'],'terrace_group':e['terrace_group']})

# Street details use separate geometry and remain clear of the 8m carriageway.
current='F013';basis=Matrix.Translation((*path[0],0))
def disk(name,r,z0,z1,m):
    n=48;ps=[(r*math.cos(i*2*math.pi/n),r*math.sin(i*2*math.pi/n)) for i in range(n)]
    return mesh(name,[(x,y,z) for z in (z0,z1) for x,y in ps],[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],m)
disk('painted mini-roundabout centre',1.4,-.077,-.069,roadwhite)
current='F012';setframe(14,1,0)
for x in range(-3,4):box('zebra stripe',x-.32,x+.32,-1.9,1.9,-.075,-.065,roadwhite)
for side in (-1,1):
    setframe(14,side,4.85);box('beacon pole',-.045,.045,-.045,.045,0,2.9,dark);box('yellow beacon',-.16,.16,-.16,.16,2.85,3.16,orange)

current='F006';setframe(stop_s['route-008']+5,1,5.7)
for x in (-2.1,2.1):
    for y in (-.50,.50):box('shelter post',x-.045,x+.045,y-.045,y+.045,0,2.35,green)
box('shelter glass back',-2.1,2.1,.43,.48,.35,2.20,glass)
box('shelter bench',-1.65,1.65,.0,.36,.45,.53,grey)
box('shelter roof',-2.3,2.3,-.7,.7,2.30,2.48,green)
lettering('BUS STOP',2.35,2.4,white,y=-.72,size=.16)

current='F003';bridge_s=stop_s['route-007']
for side in (-1,1):
    setframe(bridge_s,side,5.5)
    for x in (-5.2,5.2):box('bridge end pier',x-.25,x+.25,-.2,.28,0,1.15,brick)
    for i in range(42):
        x=-5.1+i*.25;box('bridge vertical rail',x-.018,x+.018,-.02,.035,.12,1.17,dark)
    for z in (.15,1.17):box('bridge horizontal rail',-5.2,5.2,-.055,.065,z,z+.07,dark)
current='F014'
for s in (32,79,128,173,223,259):
    setframe(s,-1,4.9);box('street lamp column',-.045,.045,-.045,.045,0,6.2,dark)
    box('street lamp outreach',-.04,.04,-.85,.05,6.1,6.18,dark);box('street lamp head',-.14,.14,-1.1,-.65,6.02,6.16,grey)
    box('litter bin',.40,.86,-.20,.24,0,.90,dark)

bpy.context.view_layer.update()
for name,(vs,fs) in protected.items():
    ob=bpy.data.objects[name]
    assert vs==[tuple(ob.matrix_world@v.co) for v in ob.data.vertices],name
    assert fs==[tuple(p.vertices) for p in ob.data.polygons],name
solids=[o for o in made if o.type=='MESH']
for ob in solids:
    bm=bmesh.new();bm.from_mesh(ob.data)
    assert all(e.is_manifold for e in bm.edges),ob.name
    assert bm.calc_volume(signed=True)>0,ob.name
    assert ob.matrix_world.determinant()>0,ob.name
    bm.free()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
dest=ROOT/'recon/v25';dest.mkdir(exist_ok=True)
views=[]
def camera(name,eye,target,ortho=None):
    cd=bpy.data.cameras.new('Review v25 | '+name);ob=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(ob)
    ob.location=eye;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();cd.lens=26
    if ortho:cd.type='ORTHO';cd.ortho_scale=ortho
    views.append((name,ob));return ob
camera('01_syston_overview',(-25,150,310),(-25,150,0),350)
for ident,name in [('B045','02_costa_and_town_square'),('B027','03_bm_gables'),('B015','04_bridge_shop_row'),('B033','05_roundabout_approach')]:
    sp=next(s for s in specs if s['id']==ident);s=sp['chainage_m_estimate'];side=1 if sp['side']=='east' else -1
    target,_,_=frame(s,side,7.2);eye,_,_=frame(s+8,-side,3)
    camera(name,(*eye,2.0),(*target,4.0))
p,_,_=frame(bridge_s+10,1,1.2);q,_,_=frame(bridge_s-8,1,0)
camera('06_bridge_player',(*p,1.7),(*q,1.9))
camera('07_junction_player',(-31,-18,1.7),(-43,22,3.5))
scene.camera=views[0][1]
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
report={'checkpoint':str(OUT.relative_to(ROOT)),'input_sha256':source_hash,'catalogue_frontages':specs,'frontage_count':len(specs),'closed_outward_solids':len(solids),'preserved_meshes':len(protected),'archived_generic_objects':len(retired),'route_scale_estimate':route_scale,'retained_taraj_chainage':taraj_s,'limits':['Approximate gameplay scale/parcel widths; catalogue markers are not surveyed footprints.','Historical shop occupancy mixed between dated panoramas; final occupancy requires chosen date.','Opaque scenery glazing, no invented shop interiors.','No Radiant compiler or in-game verification in this Blender-only pass.'],'radiant_or_game_verified':False}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
# Review lighting is temporary and is deliberately not saved into the scene.
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_percentage=100;scene.world=scene.world.copy();scene.world.use_nodes=True
bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
ld=bpy.data.lights.new('Temporary v25 daylight','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name,cam in views:
    scene.camera=cam;scene.render.resolution_x=1200 if cam.data.type=='ORTHO' else 1400;scene.render.resolution_y=1600 if cam.data.type=='ORTHO' else 950
    scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps({'checkpoint':str(OUT),'frontages':len(specs),'solids':len(solids),'preserved_meshes':len(protected)}))
