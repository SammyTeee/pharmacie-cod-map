"""Bounded asset inspection before considering map placement."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'assets/generated/skeleton-chair';dest=ROOT/'recon/v31/skeleton';dest.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene
bpy.ops.import_scene.gltf(filepath=str(out/'skeleton-chair.glb'))
objects=[o for o in scene.objects if o.type=='MESH'];pts=[o.matrix_world@v.co for o in objects for v in o.data.vertices];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)])
height=hi.z-lo.z;scale=1.7/height;centre=(lo+hi)/2;centre.z=lo.z
root=bpy.data.objects.new('Skeleton chair normalization',None);scene.collection.objects.link(root)
for o in [o for o in scene.objects if o!=root and o.parent is None]:o.parent=root
root.scale=(scale,scale,scale);root.location=-centre*scale;bpy.context.view_layer.update()
report={'source_glb_bytes':(out/'skeleton-chair.glb').stat().st_size,'meshes':len(objects),'vertices':sum(len(o.data.vertices) for o in objects),'triangles':sum(len(o.data.polygons) for o in objects),'original_bounds':[list(lo),list(hi)],'normalization_height_m':1.7,'materials':[m.name for m in bpy.data.materials],'rigged':any(o.type=='ARMATURE' for o in scene.objects),'source':'fal-ai/trellis-2; existing photo-led isolated source; inferred back geometry'}
(out/'inspection.json').write_text(json.dumps(report,indent=2))
scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=True;scene.render.resolution_x=720;scene.render.resolution_y=720;scene.render.resolution_percentage=100
w=bpy.data.worlds.new('Inspection studio');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Strength'].default_value=.7;scene.world=w
for loc,energy,size in [((2,-3,4),250,3),((-2,1,3),180,3)]:
    ld=bpy.data.lights.new('Studio','AREA');ld.energy=energy;ld.size=size;o=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.9))-o.location).to_track_quat('-Z','Y').to_euler()
cd=bpy.data.cameras.new('Asset review');cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);cd.lens=50;scene.camera=cam
for name,eye in [('01_front',(0,-3.1,1.25)),('02_back',(0,3.1,1.25)),('03_side',(3.1,0,1.25)),('04_three_quarter',(2,-2.7,1.3))]:
    cam.location=eye;cam.rotation_euler=(Vector((0,0,.85))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print('FAL_SKELETON_INSPECTED',json.dumps(report),flush=True)
