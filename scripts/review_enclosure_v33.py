"""Read-only enclosure survey and matched player-height views of v32/v33."""
from pathlib import Path
import bpy, json, os, math
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[1]
dest = ROOT / 'recon/v33'
dest.mkdir(exist_ok=True)
phase = os.environ.get('V33_PHASE', 'before')
scene = bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene = scene
os.environ.update(PHARMACIE_RECON_PHASE='after', PHARMACIE_RECON_OUTPUT=str(dest / phase),
                  PHARMACIE_RECON_PROBES_ONLY='1', PHARMACIE_RECON_RADIUS='0.42')
try:
    exec(compile((ROOT/'scripts/recon_blender_players.py').read_text(), 'retained_route_survey', 'exec'))
except SystemExit:
    pass
inventory = []
for obj in scene.objects:
    if obj.type != 'MESH' or obj.hide_render:
        continue
    if any(word in obj.name.lower() for word in ('wall', 'floor', 'ceiling', 'roof', 'ground', 'door', 'boundary', 'closure')):
        pts = [obj.matrix_world @ Vector(p) for p in obj.bound_box]
        low = [min(p[i] for p in pts) for i in range(3)]
        high = [max(p[i] for p in pts) for i in range(3)]
        if low[0] < 70 and high[0] > -65 and low[1] < 40 and high[1] > -42:
            inventory.append(dict(name=obj.name, low=low, high=high))
(dest / (phase+'-architecture.json')).write_text(json.dumps(inventory, indent=2))
survey = []
jamb0=bpy.data.objects['Ground shell 03 | door 0 | jamb 0']
jamb1=bpy.data.objects['Ground shell 03 | door 0 | jamb 1']
def centre(obj):
    return sum((obj.matrix_world@Vector(p) for p in obj.bound_box),Vector())/8
a,b=centre(jamb0),centre(jamb1)
portal_centre=(a+b)/2;portal_axis=b-a;portal_axis.z=0
portal_width=portal_axis.length;portal_axis.normalize()
portal_normal=Vector((-portal_axis.y,portal_axis.x,0))
def through_rear_exit(eye,direction):
    eye,direction=Vector(eye),Vector(direction)
    den=direction.dot(portal_normal)
    if den<=1e-8:return None
    t=(portal_centre-eye).dot(portal_normal)/den
    if t<0:return None
    point=eye+direction*t
    if abs((point-portal_centre).dot(portal_axis))<=portal_width/2+.02 and 0<=point.z<=3.15:
        return list(point)
    return None
for sample in route_samples[::2]:
    if sample['route'] in ('outer_alley', 'rear_connector', 'entrance'):
        continue
    x,y,_ = sample['nominal']
    eye = (x,y,sample['floor_z']+1.65)
    rays = []
    for slope in (0, .15, .4, .75, 1.5, 3):
        for k in range(32):
            ang = k*math.tau/32
            direction = Vector((math.cos(ang), math.sin(ang), slope)).normalized()
            hit = ray(bvh, names, eye, direction, 60)
            if hit is None or hit['distance'] > 24:
                exit_point=through_rear_exit(eye,direction) if hit is None else None
                rays.append(dict(direction=list(direction),hit=hit,
                    classification=('intentional rear doorway to outdoor sky' if exit_point else
                                    'unexplained open ray' if hit is None else 'distant geometry hit'),
                    doorway_intersection=exit_point))
    ceiling = ray(bvh,names,eye,(0,0,1),15)
    survey.append(dict(route=sample['route'],eye=eye,ceiling=ceiling,suspicious_rays=rays))
ground = []
for x in range(-58,69,3):
    for y in range(-41,41,3):
        hit = ray(bvh,names,(x,y,1.65),(0,0,-1),8)
        ground.append(dict(x=x,y=y,hit=hit))
report = dict(checkpoint=bpy.data.filepath,interior_samples=survey,ground=ground,
              interior_ray_count=len(survey)*32*6,
              unexplained_open_rays=sum(r['classification']=='unexplained open ray' for s in survey for r in s['suspicious_rays']),
              intentional_rear_exit_sky_rays=sum(r['classification']=='intentional rear doorway to outdoor sky' for s in survey for r in s['suspicious_rays']),
              limits='Visible-mesh rays; not watertightness, collision or BO3 AI verification')
(dest / (phase+'-enclosure-survey.json')).write_text(json.dumps(report,indent=2))
views = [
 ('01_pub_entrance',(5.5,1.5,1.65),(5.5,13,1.65)),
 ('02_bar_service',(8.8,15,1.65),(10.3,17,2)),
 ('03_back_stairs',(-3,29.75,1.65),(5.5,29.75,2.3)),
 ('04_upper_front',(6.5,5,6.45),(4.5,1,6.9)),
 ('05_upper_rear',(7.7,23.5,6.45),(7.7,30,6.8)),
 ('06_upper_side',(4.5,18,6.45),(-2,18,6.8)),
 ('07_alley_mouth',(-11.4,2,1.65),(-11.4,20,1.65)),
 ('08_alley_turn',(-11.4,31.8,1.65),(-6.5,32,1.8)),
 ('09_rear_threshold',(-3,31.8,1.65),(-3,27,1.65)),
 ('10_lane_end',(46.5,-24,1.65),(46.5,-29.8,2)),
 ('11_west_boundary',(-15.5,-6.7,1.57),(-19,-6.7,2)),
 ('12_east_boundary',(54,-6.7,1.57),(62,-6.7,2)),
 ('13_fox_junction',(-31,-18,1.65),(-23,-10,0)),
 ('14_street_roofline',(12,-10.7,1.65),(6,0,6)),
 ('15_shop_side_lane',(46.5,-18,1.65),(43,-23,4)),
 ('16_rear_context',(-7.65,31.8,1.65),(-7.65,34,2)),
 ('17_stair_seam',(6.6,29,4.49444475),(9.5,31,4.65)),
 ('18_diagonal_ceiling',(5.5,7.8,1.65),(10.5,12.8,4.48)),
 ('19_rear_ceiling',(-2.5,23.3,1.65),(-4.5,28,4.5)),
]
(dest/'review-views.json').write_text(json.dumps(views,indent=2))
if not os.environ.get('V33_AUDIT_ONLY'):
    if phase=='highlight':
        gold=bpy.data.materials.new('Temporary v33 added walls gold');gold.use_nodes=True
        gold.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.95,.43,.035,1)
        green=bpy.data.materials.new('Temporary v33 ceiling backing green');green.use_nodes=True
        green.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.12,.55,.23,1)
        for obj in scene.objects:
            if obj.type=='MESH' and obj.name.startswith('Mapping v33 |'):
                obj.data.materials.clear();obj.data.materials.append(green if obj.get('mapping_role')=='ceiling_backing' else gold)
    scene.render.engine='CYCLES'
    scene.cycles.samples=12
    scene.cycles.use_denoising=True
    scene.cycles.denoiser='OPTIX'
    pref=bpy.context.preferences.addons['cycles'].preferences
    pref.compute_device_type='OPTIX';pref.get_devices()
    for device in pref.devices:device.use=device.type=='OPTIX'
    scene.cycles.device='GPU';scene.render.use_persistent_data=True
    scene.render.resolution_x=1280;scene.render.resolution_y=720
    scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
    world=bpy.data.worlds.new('Temporary v33 survey daylight');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.82,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;scene.world=world
    sun=bpy.data.lights.new('Temporary survey sun','SUN');sun.energy=2.5
    obj=bpy.data.objects.new(sun.name,sun);scene.collection.objects.link(obj);obj.rotation_euler=(.45,-.55,-.45)
    for x,y,z in ((4,4,3.8),(4,12,3.8),(5,23,3.8),(4,7,8),(4,18,8),(4,27,8)):
        light=bpy.data.lights.new('Temporary room survey fill','AREA');light.energy=180;light.size=4
        obj=bpy.data.objects.new(light.name,light);scene.collection.objects.link(obj);obj.location=(x,y,z)
    data=bpy.data.cameras.new('Temporary v33 survey camera');data.lens=24
    camera=bpy.data.objects.new(data.name,data);scene.collection.objects.link(camera);scene.camera=camera
    for name,eye,target in views:
        selected=os.environ.get('V33_VIEWS','')
        if selected and name not in selected.split(','):
            continue
        camera.location=eye;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(dest/(name+'_'+phase+'.png'));bpy.ops.render.render(write_still=True)
print('V33_SURVEY_COMPLETE',phase,len(survey),sum(len(s['suspicious_rays']) for s in survey),flush=True)
