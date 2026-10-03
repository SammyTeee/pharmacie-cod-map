"""Player-height photographic recon and measured route probes; no map writes."""
from pathlib import Path
import bpy,json,math,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
PHASE=os.environ.get('PHARMACIE_RECON_PHASE','before')
RADIUS=float(os.environ.get('PHARMACIE_RECON_RADIUS','0.35'))
OUT=ROOT/'recon/v18'/os.environ.get('PHARMACIE_RECON_OUTPUT',PHASE);OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
verts=[];faces=[];names=[];floorverts=[];floorfaces=[];floornames=[]
def add_mesh(o,vlist,flist,nlist):
    evaluated=o.evaluated_get(deps);me=evaluated.to_mesh();offset=len(vlist)
    vlist.extend(evaluated.matrix_world@v.co for v in me.vertices)
    for p in me.polygons:flist.append(tuple(offset+i for i in p.vertices));nlist.append(o.name)
    evaluated.to_mesh_clear()
def is_floor(o):
    return any(w in o.name.lower() for w in ('floor','tread','landing','threshold','pavement','road','alley','side lane','platform slab','intermediate step')) and not any(w in o.name.lower() for w in ('flooring','roof','post box','post office','wall','advert','kerb','bay white','bay end','tactile','fascia','ceiling'))
for o in scene.objects:
    if o.type!='MESH' or o.hide_render:continue
    add_mesh(o,verts,faces,names)
    if is_floor(o):add_mesh(o,floorverts,floorfaces,floornames)
bvh=BVHTree.FromPolygons(verts,faces);floorbvh=BVHTree.FromPolygons(floorverts,floorfaces)
def ray(tree,nlist,origin,direction,distance):
    loc,normal,index,dist=tree.ray_cast(Vector(origin),Vector(direction),distance)
    return {'object':nlist[index],'point':list(loc),'normal':list(normal),'distance':dist} if loc is not None else None
# Foot coordinates and look-at direction: camera always 1.65m above specified floor.
views=[
('01_street_to_pub',(5.5,-2,0),(5.5,3,1.65)),
('02_threshold_inward',(5.5,.5,0),(5.5,8,1.65)),
('03_entrance_reverse',(5.5,3,0),(5.5,-3,1.4)),
('04_main_room_to_bar',(5.5,6,0),(4.5,16,1.65)),
('05_left_display_wall',(4.8,8,0),(-.7,9,1.6)),
('06_right_platform',(5.5,10,0),(9,11,1.6)),
('07_medical_tables',(4.3,12,0),(2.7,12,1)),
('08_bar_front',(4.5,14,0),(3.7,17,1.65)),
('09_bar_route_right',(8.8,16,0),(8.7,22,1.65)),
('10_rear_service',(7.3,22,0),(5,27,1.65)),
('11_rear_exit',(-3.9,30,0),(-7.5,32,1.65)),
('12_stairs_start',(-1.5,29.75,0),(3,29.75,2.6)),
('13_stairs_lower_mid',(2.7,29.75,1.6),(6.4,29.7,4)),
('14_stairs_turn',(6.6,29.75,2.667),(6.6,26,5.5)),
('15_stairs_upper',(6.6,26.65,4.267),(6.6,24,6.45)),
('16_upper_arrival',(6.6,24.85,4.8),(4,21,6.45)),
('17_upstairs_seating',(4.5,18,4.8),(3,8,6.45)),
('18_upstairs_front',(4.5,5,4.8),(4.5,15,6.45)),
('19_upstairs_rear',(3,23,4.8),(2,28,6.45)),
('20_alley_entrance',(-11.4,1,0),(-11.4,12,1.65)),
('21_alley_mid',(-11.4,13,0),(-11.4,25,1.65)),
('22_alley_rear',(-11.4,31.8,0),(-6.5,31.8,1.65)),
('23_rear_connector',(-7,32,0),(-4,30.5,1.65)),
('24_opposite_row',(5.5,-6.5,-.08),(5.5,-13,2.4)),
('25_crossing',(40,-6.5,-.08),(40,-13,2.4)),
('26_wellbeing_lane',(46.5,-14,0),(46.5,-26,1.65)),
('27_fox_junction',(-22,-6.5,-.08),(-12,-13,2.2)),
('28_street_right',(20,-1.5,0),(42,-1.5,1.65)),
('29_upper_hall_clear',(7.7,24.85,4.8),(7.7,20,6.45)),
('30_upper_front_clear',(6.5,5,4.8),(4.5,14,6.45)),
('31_upper_rear_clear',(7.7,23.5,4.8),(7.7,27,6.45)),
('32_rear_exit_clear',(-3,29.75,0),(-3,32,1.65)),
('33_service_store',(6.6,23.6,0),(6.5,26,1.65)),
('34_left_bar_route',(-1.5,14,0),(-2,23,1.65)),
('35_stage_step',(7,2.3,0),(7,4,.9)),
('36_alley_connection',(-6.5,32.6,.008),(-3,32.6,1.65))]
if PHASE=='after':
    corrections={'05_left_display_wall':((5.5,8,0),(-.7,9,1.6)), '10_rear_service':((7.0,23.6,0),(6.5,26,1.65)), '11_rear_exit':((-3,29.75,0),(-3,32,1.65)), '16_upper_arrival':((7.7,24.85,4.8),(7.7,20,6.45)), '18_upstairs_front':((6.5,5,4.8),(4.5,14,6.45)), '19_upstairs_rear':((7.7,23.5,4.8),(7.7,27,6.45))}
    views=[(name,*corrections[name]) if name in corrections else (name,feet,target) for name,feet,target in views]
audits=[]
for name,feet,target in views:
    eye=(feet[0],feet[1],feet[2]+1.65)
    support=ray(floorbvh,floornames,(feet[0],feet[1],feet[2]+.32),(0,0,-1),.85)
    if support and PHASE=='after':eye=(feet[0],feet[1],support['point'][2]+1.65)
    head=ray(bvh,names,(feet[0],feet[1],feet[2]+.1),(0,0,1),2.1)
    shoulders=[ray(bvh,names,(feet[0],feet[1],feet[2]+z),(math.cos(a),math.sin(a),0),RADIUS) for z in (.45,1.0,1.65) for a in [i*math.pi/4 for i in range(8)]]
    audits.append({'view':name,'feet':feet,'eye':eye,'look_at':target,'support':support,'headroom_hit':head,'body_clearance_hits':[h for h in shoulders if h],'assumptions':f'Eye 1.65m, radius {RADIUS}m; rays only, not a BO3 capsule sweep'})
(OUT/'view-probes.json').write_text(json.dumps({'phase':PHASE,'blend':bpy.data.filepath,'views':audits},indent=2)+'\n')
legs=[('entrance',[(5.5,-2,0),(5.5,3,0)]),('main_aisle',[(5.5,3,0),(5.5,14,0)]),('bar_right',[(8.8,14,0),(8.8,21,0)]),('service_store',[(7.0,21.5,0),(7.0,24.9,0)]),('bar_left_to_rear',[(-2.0,14,0),(-2.0,15.3,0),(-2.5,23.7,0),(-3,29.75,0),(-1.35,29.75,0)]),('lower_stairs',[(-1.35,29.75,0),(5.7,29.75,2.667),(6.6,29.75,2.667)]),('upper_stairs',[(6.6,29.0,2.934),(6.6,25.55,4.8),(6.6,24.85,4.8)]),('upper_hall',[(7.7,24.85,4.8),(7.7,20,4.8),(4.5,18,4.8)]),('outer_alley',[(-11.4,0,0),(-11.4,31.8,0),(-7,31.8,0)]),('rear_connector',[(-7,31.8,0),(-6.5,32.6,0),(-3,32.6,0),(-3,29.5,0)])]
route_samples=[]
for route,points in legs:
    for start,end in zip(points,points[1:]):
        a,b=Vector(start),Vector(end);count=max(1,math.ceil((b-a).length/.20))
        for i in range(count+1):
            p=a.lerp(b,i/count);support=ray(floorbvh,floornames,(p.x,p.y,p.z+.40),(0,0,-1),1.0)
            floor=support['point'][2] if support else p.z
            blockers=[]
            for z in (.45,1.0,1.65):
                for ang in [j*math.pi/4 for j in range(8)]:
                    hit=ray(bvh,names,(p.x,p.y,floor+z),(math.cos(ang),math.sin(ang),0),RADIUS)
                    if hit:blockers.append(hit['object'])
            overhead=ray(bvh,names,(p.x,p.y,floor+.08),(0,0,1),1.95)
            route_samples.append({'route':route,'nominal':list(p),'floor_z':floor,'floor_object':support['object'] if support else None,'blockers':sorted(set(blockers)),'overhead':overhead})
(OUT/'route-probes.json').write_text(json.dumps({'assumptions':f'0.20m route spacing; {RADIUS}m radial rays at three heights; 1.95m overhead check; no game collision simulation','samples':route_samples},indent=2)+'\n')
if os.environ.get('PHARMACIE_RECON_PROBES_ONLY')=='1':
    print('Route probes only:',len(route_samples));raise SystemExit(0)
data=bpy.data.cameras.new('Temporary recon camera');cam=bpy.data.objects.new(data.name,data);scene.collection.objects.link(cam);scene.camera=cam
data.lens=22;data.sensor_width=36;data.clip_start=.05;data.clip_end=250
scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=True
scene.render.resolution_x=1100;scene.render.resolution_y=700;scene.render.resolution_percentage=100
world=bpy.data.worlds.new('Temporary recon daylight');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65;scene.world=world
sun_data=bpy.data.lights.new('Temporary recon sun','SUN');sun_data.energy=2;sun_data.angle=.15
sun=bpy.data.objects.new(sun_data.name,sun_data);scene.collection.objects.link(sun);sun.rotation_euler=(.5,-.4,-.5)
# Neutral inspection fill is documented, distinct from proposed final game lighting.
for x,y,z in [(4,4,3.8),(4,10,3.8),(5,16,3.8),(4,23,3.8),(4,7,8.0),(4,17,8.0),(3,26,8.0)]:
    light=bpy.data.lights.new('Temporary recon room fill','AREA');light.energy=160;light.size=4
    o=bpy.data.objects.new(light.name,light);scene.collection.objects.link(o);o.location=(x,y,z)
for o in scene.objects:
    if o.type=='FONT' and not o.name.startswith('Street v17 |'):o.hide_render=True
selected=os.environ.get('PHARMACIE_RECON_VIEWS','')
for name,feet,target in views:
    if selected and name not in selected.split(','):continue
    support=next(a['support'] for a in audits if a['view']==name)
    floor_z=support['point'][2] if support and PHASE=='after' else feet[2]
    cam.location=(feet[0],feet[1],floor_z+1.65);cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps({'phase':PHASE,'views':len(views),'support_missing':[a['view'] for a in audits if not a['support']],'body_hits':[(a['view'],len(a['body_clearance_hits'])) for a in audits if a['body_clearance_hits']]}))
