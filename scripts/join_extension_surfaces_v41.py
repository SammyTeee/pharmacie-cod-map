"""Apply precomputed closed union surfaces to the new v41 collection only."""
import bpy,bmesh,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-extension-route-v41.blend'
d=json.loads((ROOT/'recon/v41/joined-surfaces.json').read_text())
coll=bpy.data.collections['MAPPING v41 | OSM Melton station Holmdale route blockout']
archive=bpy.data.collections.get('ARCHIVE v41 | First fragmented pavement surfaces')
if not archive:
 archive=bpy.data.collections.new('ARCHIVE v41 | First fragmented pavement surfaces');archive.use_fake_user=True
for ob in list(coll.objects):
 if any(s in ob.name for s in ('continuous carriageway',' footway ',' kerb ','continuous terrain backing',' outer boundary ')):
  archive.objects.link(ob);coll.objects.unlink(ob)
checks=[]
materials={'road':'Street v36 | aged asphalt Street v17 | asphalt','kerb':'Extension v41 | pale concrete kerbs','footway':'Syston v27 | concrete paving joints','terrain':'Extension v41 | earth backing','boundary':'Shop v19 | brick relief'}
for key,material in materials.items():
 me=bpy.data.meshes.new('Final joined '+key);me.from_pydata(d[key]['vertices'],[],d[key]['faces']);me.materials.append(bpy.data.materials[material]);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True)
 assert bad==0 and volume>0,(key,bad,volume)
 bm.to_mesh(me);bm.free()
 ob=bpy.data.objects.get('Extension v41 | Joined '+key)
 if ob:ob.data=me
 else:ob=bpy.data.objects.new('Extension v41 | Joined '+key,me);coll.objects.link(ob)
 ob['evidence']='OSM alignment; estimated widths; final station walkway inferred';ob['engine_implemented']=False
 checks.append({'surface':key,'nonmanifold_edges':bad,'volume':volume})
bpy.context.view_layer.update()
report={'archived_fragments':len(archive.objects),'active_extension_meshes':sum(o.type=='MESH' for o in coll.objects),'checks':checks,'station_final_link':d['station_final_link']}
(ROOT/'recon/v41/surface-fix.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result=report
