"""One-time saved-v29 review correction: close exposed roof ends."""
from pathlib import Path
import bpy,bmesh,json
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-syston-detail-v29.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections['STREET v29 | Reference window detail']
assert not any('roof gable end' in o.name for o in coll.objects)
count=0
for ident in ('B032','B033','B015'):
    anchor=next(o for o in scene.objects if o.get('catalogue_id')==ident and 'upper facade' in o.name);xs=[v.co.x for v in anchor.data.vertices];h=max(v.co.z for v in anchor.data.vertices)
    for x in (min(xs),max(xs)-.09):
        name='Syston v29 | '+ident+' | roof gable end'
        me=bpy.data.meshes.new(name);me.from_pydata([(xx,y,z) for xx in (x,x+.09) for y,z in [(0,h+.25),(10,h+.25),(5,h+1.20)]],[],[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]);me.materials.append(bpy.data.materials['Syston v27 | weathered brick 2']);me.update()
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);assert bm.calc_volume(signed=True)>0;bm.to_mesh(me);bm.free()
        o=bpy.data.objects.new(name,me);coll.objects.link(o);o.matrix_world=anchor.matrix_world.copy();count+=1
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
p=ROOT/'recon/v29/validation.json';r=json.loads(p.read_text());r['review_closed_roof_ends']=count;p.write_text(json.dumps(r,indent=2)+'\n')
print('V29_ROOF_REVIEW_COMPLETE',count)
