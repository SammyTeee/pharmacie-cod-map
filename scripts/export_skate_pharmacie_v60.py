"""Adapt a copy of our Blender scene to the pinned open-source SKATE exporter."""
from pathlib import Path
import bpy,json,sys,math,hashlib,time
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'recon/skate-v60';DEST.mkdir(parents=True,exist_ok=True)
SOURCE=Path(bpy.data.filepath);assert SOURCE.name=='pharmacie-skate-street-v60.blend'
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
TOOL=ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map';sys.path.insert(0,str(TOOL))
from owned_world_material_addon.exporter import export_scene
src=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=src;deps=bpy.context.evaluated_depsgraph_get()
scene=bpy.data.scenes.new('TEMP calibrated Skate export');groups={}
for name in ('OW_GROUP_1_PRESENTATION_COLLISION','OW_GROUP_2_NO_PRESENTATION','OW_GROUP_3_NO_COLLISION','OW_GROUP_4_GRINDS','OW_GROUP_5_PATHING'):
 assert bpy.data.collections.get(name) is None
 c=bpy.data.collections.new(name);scene.collection.children.link(c);groups[name]=c
scale=1/1.0640686466;transform=Matrix.Diagonal((scale,scale,scale,1))
fallbacks={};material_map={};images={};records=[];started=time.monotonic()
for p in (ROOT/'assets/materials/demo-v59').glob('*.png'):
 im=bpy.data.images.load(str(p),check_existing=True);im.pack();images[p.stem]=im
def material(source):
 if source.name in material_map:return material_map[source.name]
 m=source.copy();m.name='SKATE export | '+source.name
 p=source.node_tree.nodes.get('Principled BSDF') if source.use_nodes else None
 color=list(p.inputs['Base Color'].default_value[:3]) if p else list(source.diffuse_color[:3])
 m['ow_display_color']=color;m['ow_friction']=.82;m['ow_restitution']=0.;m['ow_roughness']=float(p.inputs['Roughness'].default_value) if p else .78;m['ow_emissive']=0.;m['ow_physics_surface']=1
 texture=None;uv_name=None
 if source.get('demo_v59_texture'):
  texture=images[source['demo_v59_texture']];uv_name='Demo v59 metric surface'
 else:
  texnodes=[n for n in source.node_tree.nodes if n.type=='TEX_IMAGE' and n.image] if source.use_nodes else []
  # Existing photo materials keep their image and original UVs.
  if texnodes:
   texture=texnodes[0].image
  else:
   low=source.name.lower();key='brick-0' if 'brick' in low else 'slate' if 'slate' in low else 'asphalt' if 'asphalt' in low else 'paving' if 'paving' in low else None
   if key:texture=images[key];uv_name='Export metric projection';fallbacks[source.name]=key
 if texture:
  m['ow_albedo_image']=texture.name;m['ow_display_color']=(1.,1.,1.)
  if uv_name:m['ow_uv_map']=uv_name
 material_map[source.name]=m;return m
for idx,ob in enumerate(list(src.objects)):
 if ob.type not in ('MESH','FONT','CURVE') or ob.hide_render:continue
 if ob.get('skate_grind_path'):continue
 ev=ob.evaluated_get(deps);me=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=deps)
 if not me.polygons:bpy.data.meshes.remove(me);continue
 basis=ob.matrix_world.copy();me.transform(transform@basis);me.update()
 if not me.materials:me.materials.append(next(iter(bpy.data.materials)))
 for i,m in enumerate(list(me.materials)):
  if m:me.materials[i]=material(m)
 if not me.uv_layers.get('UVMap'):
  active=me.uv_layers.active
  uv=me.uv_layers.new(name='UVMap')
  if active:
   for i,q in enumerate(active.data):uv.data[i].uv=q.uv
 # Explicit physical UV fallback for procedural surface families only.
 uv=me.uv_layers.new(name='Export metric projection')
 for p in me.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]));axes=(0,1) if axis==2 else (0,2) if axis==1 else (1,2)
  m=me.materials[p.material_index];key=fallbacks.get(m.name.removeprefix('SKATE export | '))
  repeat={'brick-0':(4.23,2.56),'slate':(4.8,4.8),'asphalt':(3,3),'paving':(4.8,3.6)}.get(key,(4,4))
  for li in p.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]/repeat[0],v[axes[1]]/repeat[1])
 low=ob.name.lower();dim=ob.dimensions*scale
 decorative=ob.type=='FONT' or ob.name.startswith('Demo v59 |') or any(t in low for t in ('curtain','flower','leaf','leaves','canopy foliage','road marking','road stripe','menu','poster','bottle','glass','window','bracket','coping lip','plant pot'))
 collidable=not decorative and max(dim)>.30 and sorted(dim)[1]>.04
 if ob.get('skate_addition'):collidable=True
 target=bpy.data.objects.new(ob.name,me);target['ow_material']=me.materials[0].name;groups['OW_GROUP_1_PRESENTATION_COLLISION' if collidable else 'OW_GROUP_3_NO_COLLISION'].objects.link(target)
 me.calc_loop_triangles();records.append({'source':ob.name,'triangles':len(me.loop_triangles),'collision':collidable})
 if idx%3000==0:print('SKATE_ADAPTER_PROGRESS',idx,len(records),flush=True)
for ob in src.objects:
 if not ob.get('skate_grind_path'):continue
 cu=ob.data.copy();o=bpy.data.objects.new(ob.name,cu);groups['OW_GROUP_4_GRINDS'].objects.link(o)
 for spline in cu.splines:
  for p in spline.points:p.co=(*((ob.matrix_world@Vector(p.co[:3]))*scale),1)
spawn=bpy.data.objects.new('OW_SPAWN',None);scene.collection.objects.link(spawn);spawn.location=bpy.data.objects['Skate v60 | Session spawn'].location*scale;spawn['ow_heading_radians']=math.pi/2
scene['ow_map_name']='Pharmacie — Syston Street Session';scene['ow_start_hour']=10.;scene['ow_end_hour']=10.;scene['ow_cycle_seconds']=86400.;scene['ow_day_ambient']=.42;scene['ow_sun_intensity']=1.4
bpy.context.window.scene=scene;bpy.context.view_layer.update()
OUT=ROOT/'build/pharmacie-skate/pharmacie-street-session.skate'
export_scene(OUT,force_rebuild=True,export_editable_objects=False,progress=lambda fraction,label:print('SKATE_EXPORT_PROGRESS',round(fraction,3),label,flush=True) if fraction>.90 else None)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
report={'source':str(SOURCE.relative_to(ROOT)),'source_sha256':source_hash,'output':str(OUT.relative_to(ROOT)),'package_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'bytes':OUT.stat().st_size,'objects':records,'visual_objects':len(records),'collision_objects':sum(r['collision'] for r in records),'visual_triangles':sum(r['triangles'] for r in records),'materials':len(material_map),'procedural_texture_adaptations':fallbacks,'unit_contract':'Blender BU / 1.0640686466 to metres; exporter maps (x,y,z) to runtime (x,z,-y). No second scale.','exporter_revision':'2e16697797c8358d16f747a8259354ff2921041a','seconds':time.monotonic()-started,'limits':['Temporary export copy; editable Blender files unchanged.','Generic PBR approximation for procedural materials; photos keep original images/UV.','Small decorative meshes remain visual, excluded from collision.','Map parser and real skating runtime validation remain separate gates.']}
(DEST/'export-manifest.json').write_text(json.dumps(report,indent=2));print('SKATE_PACKAGE_READY',report['bytes'],flush=True)
