"""Read-only saved-scene inventory for the Blender demo pass."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'recon/v59';dest.mkdir(parents=True,exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
report={'source':bpy.data.filepath,'objects':len(scene.objects),'missing_images':[],
 'materials':[],'cameras':[],'survey_objects':[]}
for im in bpy.data.images:
 if im.source=='FILE' and not im.packed_file and im.filepath and not Path(bpy.path.abspath(im.filepath)).exists():report['missing_images'].append({'name':im.name,'path':im.filepath})
for m in bpy.data.materials:
 report['materials'].append({'name':m.name,'users':m.users,'nodes':[n.bl_idname for n in m.node_tree.nodes] if m.use_nodes else [],'color':list(m.diffuse_color)})
for o in scene.objects:
 if o.type=='CAMERA':report['cameras'].append({'name':o.name,'eye':list(o.matrix_world.translation),'rotation':list(o.rotation_euler),'lens':o.data.lens})
 if o.get('frontage_id') and 'enclosed shell' in o.name:report['survey_objects'].append({'name':o.name,'frame':[list(row) for row in o.matrix_world],'schedule':json.loads(o['schedule'])})
(dest/'baseline-inventory.json').write_text(json.dumps(report,indent=2))
print('AUDIT',report['objects'],'objects',len(report['missing_images']),'missing images',len(report['survey_objects']),'survey shells',flush=True)
