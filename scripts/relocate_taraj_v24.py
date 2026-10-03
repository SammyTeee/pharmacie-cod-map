"""User correction: move Taraj to opposite roadside, preserving chainage and scale."""
from pathlib import Path
import bpy,json,math,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-taraj-front-v23.blend'
OUT=ROOT/'assets/blender/pharmacie-taraj-opposite-v24.blend';assert not OUT.exists()
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
r=json.loads((ROOT/'recon/v22/validation.json').read_text());path=[Vector(p) for p in r['melton_centreline']]
u=(path[-2]-path[-3]).normalized();n=Vector((-u.y,u.x));oldfront=Vector(r['placeholder_buildings'][-1]['front_centre']);pivot=oldfront+n*7.2;newfront=pivot+n*7.2
archive=bpy.data.collections.new('ARCHIVE v23 | Placeholder buildings at relocated Taraj');archive.use_fake_user=True
names=[]
for b in r['placeholder_buildings'][:-1]:
    d=Vector(b['front_centre'])-pivot
    if abs(d.dot(u))<12 and 4<d.dot(n)<12:names.append(b['name'])
retired=[]
for ob in list(scene.objects):
    if any(ob.name.startswith('Street v22 | '+name+' ') for name in names):
        archive.objects.link(ob)
        for col in list(ob.users_collection):
            if col!=archive:col.objects.unlink(ob)
        retired.append(ob.name)
protected={ob.name:[tuple(ob.matrix_world@v.co) for v in ob.data.vertices] for ob in scene.objects if ob.type=='MESH' and not ob.name.startswith('Taraj v23 |')}
p=Vector((*tuple(pivot),0));transform=Matrix.Translation(p)@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation(-p)
group=list(bpy.data.collections['STREET v23 | Taraj Palace photo-led exterior'].objects)
for ob in group:
    ob.matrix_world=transform@ob.matrix_world
    ob['placement_note']='v24 user correction: opposite road side at unchanged Melton Road chainage'
for ob in scene.objects:
    if ob.type=='CAMERA' and ob.name.startswith('Review v23 |'):ob.matrix_world=transform@ob.matrix_world
bpy.context.view_layer.update()
for name,verts in protected.items():assert verts==[tuple(bpy.data.objects[name].matrix_world@v.co) for v in bpy.data.objects[name].data.vertices]
solids=[ob for ob in group if ob.type=='MESH']
for ob in solids:
    bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges);assert bm.calc_volume(signed=True)>0;bm.free()
scene.camera=bpy.data.objects['Review v23 | 01_taraj_front'];bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
dest=ROOT/'recon/v24';dest.mkdir(exist_ok=True)
report={'user_directed_correction':'Move Taraj to opposite road side; same chainage and scale','old_front':list(oldfront),'road_pivot':list(pivot),'new_front':list(newfront),'rigid_rotation_degrees':180,'moved_objects':len(group),'closed_outward_taraj_solids':len(solids),'preserved_meshes':len(protected),'cleared_placeholder_buildings':names,'archived_objects':len(retired),'radiant_or_game_verified':False}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary moved Taraj review daylight','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.4,-.5,-.4)
for name in ('01_taraj_front','02_taraj_entry_depth','03_taraj_street_context'):
    scene.camera=bpy.data.objects['Review v23 | '+name];scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
scene.camera=bpy.data.objects['Review v22 | 01_route_overview'];scene.render.resolution_x=1200;scene.render.resolution_y=1600;scene.render.filepath=str(dest/'04_route_overview.png');bpy.ops.render.render(write_still=True)
print(json.dumps(report))
