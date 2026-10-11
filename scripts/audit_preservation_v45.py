"""Direct v40-to-current geometry audit. Baseline mode runs in isolated Blender."""
from pathlib import Path
import bpy,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v45'
def fingerprint(o):
 h=hashlib.sha256();basis=o.matrix_basis.copy();inverse=o.matrix_parent_inverse.copy()
 h.update(repr(([list(r) for r in basis],[list(r) for r in inverse],o.parent.name if o.parent else None,o.type)).encode())
 if o.type=='MESH':
  h.update(repr([tuple(v.co) for v in o.data.vertices]).encode());h.update(repr([tuple(p.vertices) for p in o.data.polygons]).encode())
 if o.type=='FONT':h.update(repr((o.data.body,o.data.size,o.data.extrude)).encode())
 h.update(repr([m.name if m else None for m in o.data.materials] if hasattr(o.data,'materials') else []).encode())
 return h.hexdigest()
if globals().get('BASELINE',False) or '--baseline' in sys.argv:
 assert Path(bpy.data.filepath).name=='pharmacie-taraj-bar-v40.blend'
 scene=bpy.data.scenes['03 Both floors - assembled exterior'];items={o.name:fingerprint(o) for o in scene.objects}
 data={'source':'assets/blender/pharmacie-taraj-bar-v40.blend','file_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'scene':scene.name,'objects':items}
 (dest/'v40-fingerprints.json').write_text(json.dumps(data,indent=2)+'\n');result={'baseline_objects':len(items),'source_sha256':data['file_sha256']}
else:
 assert Path(bpy.data.filepath).name=='pharmacie-station-holmdale-v45.blend'
 base=json.loads((dest/'v40-fingerprints.json').read_text());objects={o.name:o for o in bpy.data.objects};active=set(o.name for o in bpy.context.scene.objects);missing=[];changed=[];archived=[]
 for name,digest in base['objects'].items():
  ob=objects.get(name)
  if ob is None:missing.append(name)
  elif fingerprint(ob)!=digest:changed.append(name)
  if name not in active:archived.append(name)
 expected=['Mapping v34 | Beyond Taraj closed road boundary','Mapping v34 | Beyond Taraj boundary head']
 report={'source':base['source'],'source_sha256':base['file_sha256'],'target':str(Path(bpy.data.filepath).relative_to(ROOT)),'source_objects':len(base['objects']),'missing':missing,'changed':changed,'archived_from_active_scene':archived,'expected_archived_road_closures':expected,'scope':'Object basis/parent/inverse; mesh vertex coordinates and polygon topology; font body/size/extrusion; material slot names. Not shader graph or BO3 runtime audit.'}
 assert not missing and not changed,report
 assert set(archived)==set(expected),archived
 (dest/'v40-preservation.json').write_text(json.dumps(report,indent=2)+'\n');result=report
