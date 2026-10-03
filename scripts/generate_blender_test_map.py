"""Convert exported Blender geometry into BO3 iwmap brushes and photo patches."""
from pathlib import Path
import json
import math
import re
import uuid
from generate_blockout import parse_entity_blocks, kv, box_brush, volume_brush

ROOT=Path(__file__).resolve().parents[1]
NAME='zm_pharmacie_blender'
UNIT=100/2.54
SHIFT=(-3.5,-10,0)
NS=uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704')
WOOD='t7_wood_planks_damaged_teak'
CONCRETE='t7_concrete_trowelled'
BRICK='t7_brick_worn_heavy_grout_red'

def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def dot(a,b):return sum(a[i]*b[i] for i in range(3))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def length(a):return math.sqrt(dot(a,a))
def world(v):return tuple((v[i]+SHIFT[i])*UNIT for i in range(3))
def f(v):return f'{v:.6f}'.rstrip('0').rstrip('.') or '0'
def guid(name):return str(uuid.uuid5(NS,name))
def texture(o):
    text=(o['material']+' '+o['name']).lower()
    if 'brick' in text:return BRICK
    if any(s in text for s in ('wood','timber','cabinet','bar','sofa','brown','stair','black','dark','door','brass')):return WOOD
    return CONCRETE

def convex_brush(name,verts,faces,material,number):
    center=tuple(sum(v[i] for v in verts)/len(verts) for i in range(3))
    planes=[]
    signatures=set()
    for face in faces:
        a=verts[face[0]]
        pair=None
        for j in range(1,len(face)-1):
            b,c=verts[face[j]],verts[face[j+1]]
            n=cross(sub(b,a),sub(c,a))
            if length(n)>1e-6:pair=(b,c,n);break
        if pair is None:continue
        b,c,n=pair
        norm=length(n)
        n=tuple(x/norm for x in n)
        if dot(n,sub(center,a))>0:
            b,c=c,b
            n=tuple(-x for x in n)
        # n is outward. Any vertex outside means this mesh needs decomposition.
        if any(dot(n,sub(v,a))>.015 for v in verts):return None
        signature=tuple(round(x,5) for x in n)+(round(dot(n,a),4),)
        if signature in signatures:continue
        signatures.add(signature)
        planes.append((a,c,b))  # BO3 inward plane winding
    if len(planes)<4:return None
    rows=[f'// brush {number}','{',f' guid "{{{guid(name)}}}"']
    for points in planes:
        coords=' '.join('( '+' '.join(f(x) for x in v)+' )' for v in points)
        rows.append(f' {coords} {material} 128 128 0 0 0 0 lightmap_gray 16384 16384 0 0 0 0')
    return '\n'.join(rows+['}'])+'\n'

def photo_patch(o,number,material,dims):
    verts=[world(v) for v in o['vertices_m']]
    face=o['faces'][0]
    uv=o['face_uvs'][0]
    if len(face)!=4:return ''
    rows=[f'// brush {number}','{',f' guid "{{{guid(o["name"])}}}"',' mesh',' {','  toolFlags;',f'  {material}','  lightmap_gray','  2 2 0 8']
    for indices in ((0,1),(3,2)):
        rows.append('  (')
        for i in indices:
            p=verts[face[i]]
            u,v=uv[i]
            rows.append('   v '+' '.join(f(x) for x in p)+f' t {f(u*dims[0])} {f((1-v)*dims[1])} 0 0')
        rows.append('  )')
    return '\n'.join(rows+[' }','}'])+'\n'

data=json.loads((ROOT/'build/blender-test-geometry.json').read_text(encoding='utf-8'))
template=(ROOT/'map_source/zm/zm_pharmacie.template.map').read_text(encoding='utf-8')
entities=parse_entity_blocks(template)
old=entities[0][2]
brush_re=re.compile(r'(?ms)^// brush (\d+)\r?\n\{.*?^\}\r?\n?')
matches=list(brush_re.finditer(old))
prefix=old[:matches[0].start()]
sky=[m.group(0) for m in matches if re.search(r'\)\s+sky\s',m.group(0))]
assert len(sky)==6
pieces=[]
number=100
stats={'convex_mesh_brushes':0,'slab_triangle_brushes':0,'photo_patches':0,'skipped':[],'source_objects':len(data['objects'])}
stats['simplified_high_facet_details']=0
for o in data['objects']:
    verts=[world(v) for v in o['vertices_m']]
    material=o['material']
    photo=None
    if material.startswith('Frontage photo'):photo=('pharmacie_frontage',(1024,1024))
    if material.startswith('Interior photo | bar front'):photo=('pharmacie_bar',(2048,2048))
    if material.startswith('Interior photo | great for texture'):photo=('pharmacie_feature_wall',(2048,2048))
    if photo:
        patch=photo_patch(o,number,*photo)
        if patch:pieces.append(patch);number+=1;stats['photo_patches']+=1
        continue
    if o['slab']:
        low=min(v[2] for v in verts)
        high=max(v[2] for v in verts)
        for j,tri in enumerate(o['triangles']):
            points=[verts[i] for i in tri]
            if not all(abs(p[2]-high)<.005 for p in points):continue
            if length(cross(sub(points[1],points[0]),sub(points[2],points[0])))<.05:continue
            prism=points+[(p[0],p[1],low) for p in points]
            faces=[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)]
            text=convex_brush(o['name']+f' triangle {j}',prism,faces,texture(o),number)
            if text:pieces.append(text);number+=1;stats['slab_triangle_brushes']+=1
        continue
    if min(max(v[i] for v in verts)-min(v[i] for v in verts) for i in range(3))<.60:
        stats['skipped'].append({'name':o['name'],'reason':'Micro-detail or unsupported non-solid photo surface under 0.6 map units'})
        continue
    if len(o['faces'])>32:
        # The legacy compiler caps intermediate face windings at 64 points.
        # Tiny sphere details are represented by simple bounds for this test;
        # a later xmodel export can preserve their full curved geometry.
        bounds=tuple(x for i in range(3) for x in (min(v[i] for v in verts),max(v[i] for v in verts)))
        text=box_brush(number,bounds,texture(o),'\n')
        stats['simplified_high_facet_details']+=1
    else:
        text=convex_brush(o['name'],verts,o['faces'],texture(o),number)
    if text:pieces.append(text);number+=1;stats['convex_mesh_brushes']+=1
    else:stats['skipped'].append({'name':o['name'],'reason':'Non-convex mesh requires model export'})

def position(block,p,angles=None):
    origin=' '.join(f(x) for x in world(p))
    if kv(block,'origin') is None:block=block[:block.rfind('}')]+'"origin" "'+origin+'"\n}'
    else:block=re.sub(r'(?m)^(\s*"origin"\s+")[^"]*"',lambda m:m[1]+origin+'"',block,count=1)
    if angles:
        if kv(block,'angles') is not None:block=re.sub(r'(?m)^(\s*"angles"\s+")[^"]*"',lambda m:m[1]+angles+'"',block,count=1)
        else:block=block[:block.rfind('}')]+'"angles" "'+angles+'"\n}'
    return block

new_entities=[]
spawn=0
riser=0
prefabs={'power_switch.map':(5.8,9.8,0),'buyable_magic_box_start.map':(.7,-1.4,0),'vending_revive_struct.map':(1,1.2,0),
         'spawnable_weapon_shotgun_pump.map':(6.4,9.6,0)}
for _,_,block in entities[1:]:
    cls=kv(block,'classname') or ''
    note=kv(block,'script_noteworthy') or ''
    model=kv(block,'model') or ''
    target=kv(block,'targetname') or ''
    if cls=='misc_prefab':
        p=next((v for k,v in prefabs.items() if model.endswith(k)),None)
        if p is None:continue
        block=position(block,p,'0 90 0')
    elif note=='initial_spawn':
        p=(2.7+(spawn%2)*.85,2.5+(spawn//2)*.85,.72)
        block=position(block,p,'0 90 0');spawn+=1
    elif cls=='info_player_start' or target=='player_respawn_point':block=position(block,(3.45,3.3,.72),'0 90 0')
    elif note=='riser_location':
        p=[(3.1,8.8,.05),(2.5,14.7,.05),(3.45,5.6,.05)][riser%3]
        riser+=1
        block=position(block,p)
        block=block.replace('"receiver_set_entry_a"','"find_flesh"')
    elif cls in ('actor_spawner_zm_factory_zombie','actor_zm_nuked_basic_01'):block=position(block,(3.2,8.9,.20))
    elif cls=='reflection_probe':block=position(block,(3.45,5.0,1.45))
    elif target in ('intermission','intermission_b'):block=position(block,(4,-1.5,1.8),'0 90 0')
    elif cls=='info_volume' and note=='player_volume':
        block=brush_re.sub(volume_brush(0,(-280,380,-520,520,-12,300),'\n'),block,count=1)
    elif cls in ('umbra_volume','volume_fpstool'):continue
    new_entities.append(block)

header=template[:entities[0][0]]
worldspawn=prefix+''.join(sky)+''.join(pieces)+'}\n'
for i,(x,y,z) in enumerate([(3.35,2.5,2.5),(3.35,5.5,2.5),(3.35,8.5,2.5),(3.3,12.5,2.5),(2.0,18.4,2.6),
                           (3.4,4.0,5.7),(3.4,9.0,5.7),(3.4,15.0,5.7),(3.4,-1.0,3.2)]):
    p=world((x,y,z))
    new_entities.append(f'// entity {200+i}\n{{\n"classname" "light"\n"origin" "'+ ' '.join(f(v) for v in p)+'"\n"_color" "1 0.91 0.78"\n"light" "140"\n}\n')
output=header+worldspawn+'\n'.join(new_entities)+'\n'
dest=ROOT/'map_source/zm'/f'{NAME}.map'
dest.write_text(output,encoding='utf-8',newline='\n')
# Reuse the working Zombies bootstrap under a separate name and project tree.
source=ROOT/'usermaps/zm_pharmacie'
target=ROOT/'usermaps'/NAME
for path in source.rglob('*'):
    if not path.is_file():continue
    relative=path.relative_to(source)
    renamed=Path(str(relative).replace('zm_pharmacie',NAME))
    out=target/renamed
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(path.read_text(encoding='utf-8').replace('zm_pharmacie',NAME),encoding='utf-8')
stats.update({'map':str(dest),'project':NAME,'scale_map_units_per_metre':UNIT,'translation_metres':SHIFT,
              'source_blend':data['blend'],'initial_spawns':spawn,'riser_locations':riser,'conversion':'Convex meshes -> brushes, concave horizontal slabs -> triangle prisms, known photo quads -> iwmap meshes',
              'limitations':'Stock placeholder materials on props; micro-detail omitted; photo instrument board omitted; no xmodel export; collision and traversal pending'})
(ROOT/'build/blender-test-export-report.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in stats.items() if k!='skipped'},indent=2))
print('Skipped',len(stats['skipped']),'micro or unsupported details')
