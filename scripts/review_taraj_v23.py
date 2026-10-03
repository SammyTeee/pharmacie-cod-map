"""Correct first-pass Taraj handedness, visible upper glazing and camera position."""
from pathlib import Path
import bpy,json,math,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-taraj-front-v23.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
report=json.loads((ROOT/'recon/v22/validation.json').read_text());path=[Vector(p) for p in report['melton_centreline']]
front=Vector(report['placeholder_buildings'][-1]['front_centre']);u=(path[-2]-path[-3]).normalized();out=Vector((-u.y,u.x))
for ob in bpy.data.collections['STREET v23 | Taraj Palace photo-led exterior'].objects:
    if ob.type=='MESH':
        for v in ob.data.vertices:
            p=Vector((v.co.x,v.co.y));p-=u*2*(p-front).dot(u)
            if 'upper recessed glass' in ob.name:p+=out*.06
            v.co.x=p.x;v.co.y=p.y
        for poly in ob.data.polygons:poly.flip()
        bm=bmesh.new();bm.from_mesh(ob.data);assert all(e.is_manifold for e in bm.edges);assert bm.calc_volume(signed=True)>0;bm.free()
    elif ob.type=='FONT':
        p=Vector((ob.location.x,ob.location.y));p-=u*2*(p-front).dot(u);ob.location.x=p.x;ob.location.y=p.y
views=[('01_taraj_front',front+out*10,front),('02_taraj_entry_depth',front+u*8+out*9,front+u*2),('03_taraj_street_context',front-u*20+out*11,front)]
for name,eye,target in views:
    cam=bpy.data.objects['Review v23 | '+name];cam.location=(*tuple(eye),3.8 if 'front' in name else 2.0);cam.rotation_euler=(Vector((*tuple(target),4.7 if 'front' in name else 2.7))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=20 if 'front' in name else 26
scene.camera=bpy.data.objects['Review v23 | 01_taraj_front'];bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.55;bg.inputs['Color'].default_value=(.65,.72,.84,1)
ld=bpy.data.lights.new('Temporary review sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.4,-.5,-.4)
for name,eye,target in views:
    scene.camera=bpy.data.objects['Review v23 | '+name];scene.render.filepath=str(ROOT/'recon/v23'/(name+'.png'));bpy.ops.render.render(write_still=True)
