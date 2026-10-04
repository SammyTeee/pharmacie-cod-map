"""Street furniture, shopfront relief and crossing approaches; no engine writes."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math,ast
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];source=Path(bpy.data.filepath);assert source.name=='pharmacie-zombies-street-v31.blend'
OUT=ROOT/'assets/blender/pharmacie-street-frontages-v32.blend';assert not OUT.exists()
dest=ROOT/'recon/v32';dest.mkdir(exist_ok=True);scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections.new('MAPPING v32 | Street furniture and frontage relief');scene.collection.children.link(coll);made=[];basis=Matrix.Identity(4);current='frontage'
tree=ast.parse((ROOT/'scripts/build_street_combat_v31.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('mat','mesh','box','cylinder')],type_ignores=[]),'v31_original_helpers','exec'),globals())
metal=mat('v32 cast metal',(.035,.05,.055),.65);wood=mat('v32 weathered bench wood',(.26,.17,.09));cream=mat('v32 limestone',(.59,.56,.48));brass=mat('v32 shop brass',(.48,.35,.13),.75);black=mat('v32 sign chalkboard',(.025,.035,.028));grey=mat('v32 utility metal',(.27,.29,.30),.6);rust=mat('v32 drain dark',(.055,.058,.045));road=bpy.data.objects['Street v17 | High Street continuous road'].data.materials[0];green=mat('v32 florist foliage',(.055,.15,.045));pink=mat('v32 muted flowers',(.41,.12,.18));white=mat('v32 lamp diffuser',(.64,.63,.49));paper=mat('v32 cream paper',(.68,.66,.55))
# Keep props in the shop-side furnishing strip, away from the measured route.
for x in (-6,25.8):
 current='wall-side bench'
 for z in (.40,.91):
  for k in range(4):box('timber seat slat' if z<.5 else 'timber back slat',x-.85,x+.85,-12.66+k*.095,-12.59+k*.095,z,z+.045,wood)
 for dx in (-.65,.65):
  box('bench support',x+dx-.035,x+dx+.035,-12.70,-12.27,.04,.43,metal)
  box('back upright',x+dx-.035,x+dx+.035,-12.70,-12.64,.39,1.12,metal)
for x in (-1.8,28.3,53.0):
 current='litter bin'
 cylinder('ribbed bin body',(x,-12.48,.44),.21,.84,metal,axis='Z',vertices=16)
 cylinder('bin lid',(x,-12.48,.89),.225,.055,grey,axis='Z',vertices=16)
 box('bin opening surround',x-.12,x+.12,-12.255,-12.24,.62,.78,grey);box('dark bin opening',x-.09,x+.09,-12.238,-12.23,.64,.76,black)
 for dx in (-.12,0,.12):box('bin raised rib',x+dx-.012,x+dx+.012,-12.275,-12.26,.12,.56,grey)
# Shallow facade relief: inferred fittings, keep the confirmed fascia geometry.
shops=[('Aston',-2.85,.85),('Mini Market',1.2,9.8),('Lets Move',10.2,16.8),('Floral Fantasy',17.2,23.8)]
for label,a,b in shops:
 current=label+' facade details'
 for x in (a+.14,b-.14):
  box('pier plinth',x-.13,x+.13,-13.16,-12.85,.02,.19,cream)
  box('pier cap',x-.13,x+.13,-13.16,-12.85,3.80,3.95,cream)
  box('wall lamp mounting',x-.07,x+.07,-12.91,-12.87,3.37,3.65,metal)
  box('shielded entrance bulkhead',x-.10,x+.10,-12.86,-12.77,3.40,3.61,grey)
  box('lamp diffuser',x-.075,x+.075,-12.765,-12.755,3.43,3.58,white)
 box('weathered sill drip',a+.3,b-.3,-13.02,-12.87,.47,.52,cream)
 box('fascia underside trim',a+.05,b-.05,-13.13,-12.71,4.25,4.29,metal)
 box('alarm box',b-.47,b-.20,-12.90,-12.82,4.47,4.71,cream)
 box('alarm lens',b-.42,b-.25,-12.813,-12.804,4.51,4.56,brass)
 box('small facade vent',a+.3,a+.63,-12.94,-12.88,.24,.41,grey)
 for i in range(5):box('vent louvre',a+.32,a+.61,-12.865,-12.852,.26+i*.028,.27+i*.028,black)
# Florist merchandise stays wall-side; no hidden open interiors introduced.
current='Floral Fantasy flower display'
for x in (18.0,18.55):
 cylinder('flower bucket',(x,-12.50,.21),.16,.4,grey,axis='Z',vertices=12)
 for dx,dy in ((-.06,0),(.06,.04),(0,-.06)):
  cylinder('flower stem',(x+dx,-12.50+dy,.59),.013,.46,green,axis='Z',vertices=6)
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.065);o=bpy.context.object;o.name='Street v31 | Floral Fantasy flower display | blossom';o.location=(x+dx,-12.50+dy,.82);o.data.materials.append(pink)
  for c in list(o.users_collection):c.objects.unlink(o)
  coll.objects.link(o);made.append(o)
# Road wear and drainage remain shallow solid details, away from vehicle tyres.
current='street drainage and service covers'
for x in (-10,12,31,48):
 for y in (-3.40,-9.98):
  box('gully rim',x-.28,x+.28,y-.13,y+.13,-.079,-.075,grey)
  for j in range(8):box('gully dark slot',x-.245+j*.065,x-.22+j*.065,y-.095,y+.095,-.074,-.072,rust)
for x,y in ((7,-1.55),(30,-1.55),(14,-11.5),(36,-11.5)):
 box('flush service cover',x-.23,x+.23,y-.18,y+.18,.001,.006,grey)
 for dx in (-.14,.14):box('cover lifting socket',x+dx-.025,x+dx+.025,y-.016,y+.016,.006,.008,black)
# Solid approach wedges cover the 8cm road-to-kerb rise at both crossing points.
current='crossing approach ramps'
for x in (5.5,40):
 for y0,y1,z0,z1 in [(-3.65,-3.18,-.08,0),(-10.22,-9.75,0,-.08)]:
  mesh('road crossing approach ramp',[(x-1,y0,-.16),(x+1,y0,-.16),(x+1,y1,-.16),(x-1,y1,-.16),(x-1,y0,z0+.002),(x+1,y0,z0+.002),(x+1,y1,z1+.002),(x-1,y1,z1+.002)],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],road,'walkable_floor')
for o in made:
 if o.type=='MESH':
  bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)*o.matrix_world.determinant()>0,o.name;bm.free()
for o in made:o.name=o.name.replace('Street v31 |','Street v32 |')
for n,eye,target in [('09_opposite_shop_detail',(12,-9.5,1.65),(17,-13,2.2)),('10_fox_street_furniture',(-10,-9,1.65),(-5,-13,1.5)),('11_crossing_approach',(36,-6.7,1.65),(40,-11,0.3))]:
 cd=bpy.data.cameras.new('Review v32 | '+n);o=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(o);o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();cd.lens=28
scene['gameplay_version']='v32 street and frontage relief; Zombies priority'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));(dest/'changes.json').write_text(json.dumps(dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),output=str(OUT),new_closed_solids=len(made),engine_verified=False,changes=['Wall-side benches and litter bins','Opposite shopfront plinths, sill trims, lamps, alarm boxes and vents','Florist flower buckets','Drain grilles and flush service covers','Solid crossing approach wedges'],provenance='Original procedural meshes. New fittings inferred gameplay dressing, not confirmed photo reconstruction.'),indent=2));print('V32_BUILD_COMPLETE',len(made),flush=True)
