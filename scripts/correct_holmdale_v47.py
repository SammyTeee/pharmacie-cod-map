"""Photo-observed forward right arm; estimated dimensions, originals in v46."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-holmdale-correction-v46.blend'
OUT=ROOT/'assets/blender/pharmacie-holmdale-depth-v47.blend';assert not OUT.exists()
dest=ROOT/'recon/v47';dest.mkdir(exist_ok=True)
root=bpy.data.objects['Holmdale v44 | Movable number 29 assembly']
coll=bpy.data.collections['DETAIL v44 | Number 29 photo-led bungalow']
changed=[]
# Local Y is positive away from street. Keep rear wall at Y=5, bring front
# forward 2.25 units. Facade details translate rigidly; roof/shell stretch.
for ob in list(coll.objects):
 if ob.type!='MESH':continue
 if any(s in ob.name for s in ('boundary','fence','driveway','hedge','foliage','plant','pot','porch')):continue
 matrix=ob.matrix_basis.copy();pts=[matrix@v.co for v in ob.data.vertices]
 if min(v.x for v in pts)<4.70:continue
 # Exclude left porch-side lantern/downpipe; the right wing begins X~4.9.
 if max(v.x for v in pts)<5.08 and not any(s in ob.name for s in ('roof','wing','plinth')):continue
 me=ob.data.copy();ob.data=me;inv=matrix.inverted()
 facade=max(v.y for v in pts)<.20
 for v,p in zip(me.vertices,pts):
  p.y=p.y-2.25 if facade else (p.y-2.25 if p.y<0 else p.y*1.45-2.25)
  v.co=inv@p
 me.update();changed.append(ob.name)
root['footprint']='Forward right bay/garage arm observed in five additional Sam screenshots; forward offset 2.25 scene units estimated; hidden rear footprint unresolved'
# Add a closed rendered return connecting the recessed porch with forward wing.
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
added=[]
def box(name,x0,x1,y0,y1,z0,z1,mat):
 me=bpy.data.meshes.new(name);me.from_pydata([(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[],F);me.materials.append(bpy.data.materials['Holmdale v44 | '+mat]);me.update()
 ob=bpy.data.objects.new('Holmdale v47 | '+name,me);coll.objects.link(ob);ob.parent=root;added.append(ob.name);return ob
box('cream porch return',4.9,5.10,-2.37,.03,.02,2.58,'cream rough render')
box('return brick plinth',4.88,5.12,-2.37,.03,.02,.55,'brown brick')
box('return eave fascia',4.70,4.79,-2.64,-.25,2.45,2.62,'white uPVC')
box('left brick chimney',.22,.65,2.3,2.8,3.4,5.05,'brown brick')
box('chimney cap',.16,.71,2.24,2.86,5.05,5.16,'concrete steps')
box('terracotta chimney pot',.30,.52,2.40,2.64,5.16,5.58,'terracotta pot')
box('rear white dormer estimated',.9,3.45,4.65,6.4,3.6,5.05,'white uPVC')
box('dormer dark flat cap',.80,3.55,4.55,6.5,5.05,5.15,'dark lamp and handles')
box('dormer front glazing',1.02,3.32,4.60,4.64,4.05,4.91,'grey blue opaque glazing')
for x in (1.02,1.73,2.50,3.30):box('dormer mullion',x,x+.045,4.57,4.60,4.03,4.94,'white uPVC')
bpy.context.view_layer.update()
bad=[]
for name in changed+added:
 ob=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(ob.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(name)
 bm.free()
assert not bad,bad
refs=[]
for f in sorted((ROOT/'references/holmdale-v47').glob('*.png')):refs.append({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
report={'changed_meshes':len(changed),'added_meshes':len(added),'changed':changed,'added':added,'bad_closed_meshes':bad,'forward_offset_estimated':2.25,'references':refs,'limits':['Forward projection observed, exact dimensions estimated','Dormer rear depth and concealed shape estimated','Not satellite alignment or BO3 validation']}
(dest/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result={k:v for k,v in report.items() if k not in ('changed','references')}
