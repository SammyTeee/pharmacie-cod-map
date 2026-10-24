"""Shared visual polish; preserve v57 and save a separate neutral checkpoint."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'recon/v59';DEST.mkdir(exist_ok=True)
SOURCE=Path(bpy.data.filepath);assert SOURCE.name=='pharmacie-surveyed-route-v57.blend'
OUT=ROOT/'assets/blender/pharmacie-demo-base-v59.blend';assert not OUT.exists()
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
ns={'__file__':str(ROOT/'scripts/audit_preservation_v45.py')};code=(ROOT/'scripts/audit_preservation_v45.py').read_text().split("if globals().get('BASELINE'")[0];exec(code,ns)
fingerprint=ns['fingerprint'];before={o.name:fingerprint(o) for o in scene.objects}
coll=bpy.data.collections.new('DEMO v59 | Estimated rainwater and window detail');scene.collection.children.link(coll)
made=[];shader_changes=[];uv_changes=[];slot_changes=[];texture_specs={}
manifest=json.loads((ROOT/'assets/materials/demo-v59/manifest.json').read_text())
for item in manifest['textures']:
 im=bpy.data.images.load(str(ROOT/'assets/materials/demo-v59'/item['file']),check_existing=True);im.pack()
 texture_specs[Path(item['file']).stem]=(im,item['repeat_metres'])

def textured(material,key):
 # Keep a complete copy of each previous shader graph in the new checkpoint.
 old=material.copy();old.name='ARCHIVE v59 shader | '+material.name;old.use_fake_user=True
 material.use_nodes=True;n=material.node_tree.nodes;l=material.node_tree.links;p=n.get('Principled BSDF')
 if p is None:return
 im,repeat=texture_specs[key];tex=n.new('ShaderNodeTexImage');tex.name='Demo v59 authored surface';tex.image=im;tex.extension='REPEAT'
 uv=n.new('ShaderNodeUVMap');uv.uv_map='Demo v59 metric surface';l.new(uv.outputs['UV'],tex.inputs['Vector']);l.new(tex.outputs['Color'],p.inputs['Base Color'])
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.24;bump.inputs['Distance'].default_value=.008
 l.new(tex.outputs['Color'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal']);p.inputs['Roughness'].default_value=.84
 n.active=tex;material['demo_v59_texture']=key;material['demo_v59_repeat']=repeat
 material['demo_v59_shader_archive']=old.name;shader_changes.append(material.name)

for name,key in [('Street v17 | slate','slate'),('Survey v54 | brown roof tiles','clay-tile'),('Syston v27 | concrete paving joints','paving'),('Street v17 | paving','paving'),('Extension v41 | footway paving','paving'),('Street v36 | aged asphalt Street v17 | asphalt','asphalt')]:
 m=bpy.data.materials.get(name)
 if m:textured(m,key)
bricks=[]
for i in range(3):
 m=bpy.data.materials['Shop v19 | brick relief'].copy();m.name='Demo v59 | survey brick '+str(i);textured(m,'brick-'+str(i));bricks.append(m)
for ob in scene.objects:
 if ob.type!='MESH':continue
 if ob.get('frontage_id') and ob.name.startswith(('Survey v54 |','Survey v57 |')):
  for slot in ob.material_slots:
   if slot.material and slot.material.name=='Shop v19 | brick relief':
    ident=str(ob.get('frontage_id'));slot.material=bricks[sum(map(ord,ident))%3];slot_changes.append(ob.name)
 if not any(m and m.get('demo_v59_texture') for m in ob.data.materials):continue
 uv=ob.data.uv_layers.new(name='Demo v59 metric surface')
 for p in ob.data.polygons:
  m=ob.data.materials[p.material_index] if p.material_index<len(ob.data.materials) else None
  if not m or not m.get('demo_v59_texture'):continue
  repeat=m['demo_v59_repeat'];normal=p.normal;axis=max(range(3),key=lambda i:abs(normal[i]))
  axes=(0,1) if axis==2 else (0,2) if axis==1 else (1,2)
  for li in p.loop_indices:
   v=ob.data.vertices[ob.data.loops[li].vertex_index].co
   uv.data[li].uv=(v[axes[0]]/(repeat[0]*1.0640686466),v[axes[1]]/(repeat[1]*1.0640686466))
 ob.data.uv_layers.active=uv;uv_changes.append(ob.name)

def mat(name,color,metal=0,rough=.7):
 m=bpy.data.materials.new('Demo v59 | '+name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
iron=mat('weathered zinc rainwater',(.12,.135,.14),.65,.48);stone=mat('warm stone lintel',(.55,.52,.45));dark=mat('window recess shadow',(.045,.05,.052));curtain=mat('muted curtain behind glazing',(.34,.325,.28),0,.95)
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def box(label,bounds,basis,m,ident):
 a,b,c,d,e,f=bounds
 me=bpy.data.meshes.new(label);me.from_pydata([(a,c,e),(b,c,e),(b,d,e),(a,d,e),(a,c,f),(b,c,f),(b,d,f),(a,d,f)],[],F);me.materials.append(m);me.update()
 ob=bpy.data.objects.new('Demo v59 | '+ident+' | '+label+' '+str(len(made)),me);coll.objects.link(ob);ob.matrix_world=basis.copy();ob['demo_detail_adaptation']='Estimated architectural finishing, not measured survey';made.append(ob);return ob
shells=[o for o in scene.objects if o.get('frontage_id') and 'enclosed shell' in o.name]
for shell in shells:
 ident=shell['frontage_id'];basis=shell.matrix_world;xs=[v.co.x for v in shell.data.vertices];zs=[v.co.z for v in shell.data.vertices];a,b,h=min(xs),max(xs),max(zs)
 box('front gutter',(a-.25,b+.25,-.34,-.22,h-.19,h-.095),basis,iron,ident)
 box('gutter shadow mouth',(a-.24,b+.24,-.325,-.23,h-.095,h-.08),basis,dark,ident)
 for x in (a+.15,b-.15):
  for z in (.55,2.4,h-.65):box('downpipe bracket',(x-.035,x+.09,-.12,-.07,z,z+.055),basis,iron,ident)
 windows=[o for o in scene.objects if o.get('frontage_id')==ident and 'window glass' in o.name and o.type=='MESH']
 for win in windows:
  vs=[v.co for v in win.data.vertices];x0,x1=min(v.x for v in vs),max(v.x for v in vs);z0,z1=min(v.z for v in vs),max(v.z for v in vs);y=min(v.y for v in vs)
  if z0<3:continue
  box('window head lintel',(x0-.11,x1+.11,y-.02,y+.04,z1+.08,z1+.18),win.matrix_world,stone,ident)
  # Opaque facade proxies remain opaque: restrained thin curtain strips suggest depth.
  for x in (x0+.025,x1-.15):box('upper curtain edge',(x,x+.12,y-.008,y-.003,z0+.03,z1-.03),win.matrix_world,curtain,ident)
bad=[]
for o in made:
 bm=bmesh.new();bm.from_mesh(o.data)
 if any(not e.is_manifold for e in bm.edges) or bm.calc_volume(signed=True)<=0:bad.append(o.name)
 bm.free()
assert not bad,bad
changed=[name for name,digest in before.items() if fingerprint(bpy.data.objects[name])!=digest]
assert set(changed)<=set(slot_changes),changed
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
scene['demo_v59_status']='Neutral Blender source. No skate additions or engine behavior.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
(DEST/'build-validation.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT)),'source_sha256':source_hash,'output':str(OUT.relative_to(ROOT)),'preserved_source_objects':len(before),'new_closed_meshes':len(made),'shader_updates':shader_changes,'added_metric_uv_objects':len(uv_changes),'survey_material_slot_changes':slot_changes,'changed_fingerprints':changed,'missing_original_objects':[],'nonmanifold_or_nonpositive':bad,'limits':['Shader graphs are a visual refinement; original graphs retained with ARCHIVE v59 shader prefix.','Existing mesh vertices, topology, transforms, UV layers and photo references retained.','Curtains are shallow facade details, not surveyed interiors.','Roof UV projection is approximate on sloping and hipped faces.','No engine export or gameplay verification.']},indent=2))
print('NEUTRAL_DEMO_SAVED',str(OUT),len(made),'new meshes',flush=True)
