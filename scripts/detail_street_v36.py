"""Street surface variation and shallow frontage furniture; original geometry retained."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib,random
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1]
source=Path(bpy.data.filepath);assert source.name=='pharmacie-melton-detail-v35.blend'
out=ROOT/'assets/blender/pharmacie-street-life-v36.blend';assert not out.exists()
dest=ROOT/'recon/v36';dest.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections.new('STREET v36 | Surface wear and street life');scene.collection.children.link(coll)
made=[];basis=Matrix.Identity(4);current='road'
def mat(name,c,scale=8):
 m=bpy.data.materials.new('Street v36 | '+name);m.diffuse_color=(*c,1);m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;p=n['Principled BSDF'];p.inputs['Roughness'].default_value=.88
 tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3;l.new(tc.outputs['Object'],noise.inputs['Vector'])
 r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*(x*.65 for x in c),1);r.color_ramp.elements[1].color=(*(x*1.2 for x in c),1);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.006;b.inputs['Strength'].default_value=.25;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal']);return m
patch=mat('repaired asphalt',(.075,.082,.084),60);seal=mat('tar seams',(.025,.029,.028),20)
wood=mat('weathered bench timber',(.28,.17,.085),12);iron=mat('painted iron',(.035,.05,.048),35);stone=mat('buff concrete planter',(.42,.39,.31));soil=mat('planter soil',(.055,.038,.023));leaf=mat('muted foliage',(.085,.18,.048));pale=mat('notice paper',(.7,.66,.51));orange=mat('maintenance cone',(.75,.20,.035));white=mat('reflective cone band',(.74,.73,.66))
F=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
def mesh(name,vs,fs,m):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(m);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new('Street v36 | '+current+' | '+name,me);coll.objects.link(o);o.matrix_world=basis.copy();o['engine_implemented']=False;made.append(o);return o
def box(name,a,b,c,d,e,f,m):return mesh(name,[(a,c,e),(b,c,e),(b,d,e),(a,d,e),(a,c,f),(b,c,f),(b,d,f),(a,d,f)],F,m)
# Copy materials before adding broad weathering; no shared interior materials edited.
replaced=[];cache={}
for o in scene.objects:
 if o.type!='MESH':continue
 if not o.name.startswith(('Street','Syston','Mapping')):continue
 for slot in o.material_slots:
  m=slot.material
  if not m or 'asphalt' not in m.name.lower():continue
  if m.name not in cache:cache[m.name]=mat('aged asphalt '+m.name,(.115,.12,.118),55)
  slot.material=cache[m.name];replaced.append(o.name)
path=[Vector(p) for p in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']];lengths=[0]
for a,b in zip(path,path[1:]):lengths.append(lengths[-1]+(b-a).length)
def frame(s,off):
 i=next(i for i in range(len(path)-1) if lengths[i+1]>=s);u=(path[i+1]-path[i]).normalized();n=Vector((-u.y,u.x));p=path[i]+u*(s-lengths[i])+n*off
 return Matrix(((u.x,n.x,0,p.x),(u.y,n.y,0,p.y),(0,0,1,0),(0,0,0,1)))
for j,s in enumerate(range(48,int(lengths[-1])-8,19)):
 if 195<s<230:continue
 basis=frame(s,(-1 if j%2 else 1)*2.15)
 box('utility trench repair',-2.6,2.6,-.36,.36,-.079,-.075,patch)
 for y in (-.38,.37):box('repair sealed edge',-2.63,2.63,y,y+.025,-.078,-.073,seal)
 box('inspection cover',-.38,.38,-.29,.29,-.075,-.068,iron)
 for k in range(5):box('cover ribs',-.32,.32,-.24+k*.10,-.225+k*.10,-.068,-.064,stone)
# Deliberate clusters at selected frontage ends, staying within 70cm of the facade.
for idx,cid in enumerate(('B010','B012','B017','B023','B025','B030','B038','B042','B043','B051')):
 current=cid;src=bpy.data.objects.get('Syston v25 | '+cid+' | upper facade')
 if not src:continue
 old=src.matrix_world;cols=[old.to_3x3().col[i].normalized() for i in range(3)];lo=min(v.co.x for v in src.data.vertices);hi=max(v.co.x for v in src.data.vertices);sx=old.to_3x3().col[0].length;w=(hi-lo)*sx
 basis=Matrix(((cols[0].x,cols[1].x,cols[2].x,old.translation.x),(cols[0].y,cols[1].y,cols[2].y,old.translation.y),(cols[0].z,cols[1].z,cols[2].z,old.translation.z),(0,0,0,1)));basis.translation+=cols[0]*((lo+hi)*.5*sx)
 x=w/2-1.15
 if idx%3==0:
  for k in range(4):box('bench seat slat',x-.85,x+.85,-.65+k*.10,-.57+k*.10,.46,.52,wood)
  for k in range(3):box('bench back slat',x-.85,x+.85,-.25,-.19,.62+k*.14,.71+k*.14,wood)
  for dx in (-.67,.67):
   box('bench leg',x+dx-.035,x+dx+.035,-.61,-.22,.02,.46,iron);box('bench back upright',x+dx-.025,x+dx+.025,-.26,-.19,.45,1.02,iron)
 elif idx%3==1:
  box('planter body',x-.43,x+.43,-.67,-.18,.01,.46,stone);box('soil',x-.37,x+.37,-.61,-.24,.46,.48,soil)
  rng=random.Random(idx)
  for k in range(12):
   xx=x+rng.uniform(-.29,.29);yy=rng.uniform(-.56,-.29);zz=rng.uniform(.61,.91)
   box('plant stem '+str(k),xx-.012,xx+.012,yy-.012,yy+.012,.48,zz,wood)
   box('leaf cluster '+str(k),xx-.065,xx+.065,yy-.06,yy+.06,zz-.08,zz+.08,leaf)
 else:
  box('litter bin',x-.23,x+.23,-.62,-.19,.02,.86,iron);box('bin opening',x-.17,x+.17,-.633,-.62,.67,.77,seal);box('bin cap',x-.25,x+.25,-.64,-.17,.86,.91,iron)
  for k in range(7):box('bin vertical rib',x-.20+k*.06,x-.185+k*.06,-.637,-.63,.09,.59,stone)
 # Layered community notices on a shallow glazed cabinet.
 box('community notice case',x-.40,x+.40,-.24,-.17,1.35,2.10,iron)
 for k in range(3):box('notice '+str(k),x-.33+k*.22,x-.15+k*.22,-.251,-.24,1.46+(k%2)*.12,1.88+(k%2)*.12,pale)
bpy.context.view_layer.update()
(dest/'changes.json').write_text(json.dumps(dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),new_solids=[o.name for o in made],material_changes=sorted(set(replaced)),engine_implemented=False,scope='Inferred street dressing and procedural surface wear, not surveyed real-world furniture.'),indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(out));print('V36_COMPLETE',len(made),flush=True)
