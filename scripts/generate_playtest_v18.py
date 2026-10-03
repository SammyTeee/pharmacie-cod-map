"""Separate playable v18 conversion; stock Zombies progression, not the scale-test callback."""
from pathlib import Path
from PIL import Image
import json, hashlib, re, math, sys
from generate_blockout import parse_entity_blocks, kv, box_brush, volume_brush
ROOT=Path(__file__).resolve().parents[1]
NAME='zm_pharmacie_playtest'; UNIT=100/2.54; SHIFT=(-3.5,-10,0)
CALIBRATE='--calibrate-uv' in sys.argv
data=json.loads((ROOT/'build/playtest-v18-geometry.json').read_text())
# Explicit standalone bar regions: BO3 must never sample the upper photo on
# the drawer front. Preserve corner orientation while rebounding only these
# documented assets; all other photos retain their original Blender UVs.
bar_out=ROOT/'assets/bar-regions';bar_out.mkdir(exist_ok=True)
bar_records=[]
for o in data['objects']:
    if o['name'] not in ('Bar | drawer-front photo face','Bar | photo-backed bottles, shelves and staff-door detail','Bar | photo menu on 3D screen'):continue
    uv=o['face_uvs'][0];u0=min(p[0] for p in uv);u1=max(p[0] for p in uv);v0=min(p[1] for p in uv);v1=max(p[1] for p in uv)
    source=Path(o['image']['path'])
    slug={'Bar | drawer-front photo face':'lower-drawers','Bar | photo-backed bottles, shelves and staff-door detail':'upper-backbar','Bar | photo menu on 3D screen':'tv-menu'}[o['name']]
    derivative=bar_out/f'{slug}.png'
    with Image.open(source) as im:
        w,h=im.size;crop=(round(u0*w),round((1-v1)*h),round(u1*w),round((1-v0)*h))
        region=im.convert('RGB').crop(crop);region.save(derivative)
    bar_records.append({'object':o['name'],'derivative':str(derivative.relative_to(ROOT)),
        'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'crop_pixels':crop,'dimensions':list(region.size),'edits':'Exact recorded photo region; no repaint, original unchanged',
        'original_uvs':uv})
    o['face_uvs']=[[[round((u-u0)/(u1-u0),8),round((v-v0)/(v1-v0),8)] for u,v in uv]]
    o['image']={'path':str(derivative),'dimensions':list(region.size),'name':slug}
(bar_out/'manifest.json').write_text(json.dumps({'regions':bar_records},indent=2)+'\n')
# Independent crisp lettering replaces the low-resolution photographed plaques.
# Reference bounds are in the unchanged 1024x751 facade photo; geometry is
# interpolated on the actual evaluated pane, not an assumed shopfront width.
for pane_name,pixels in [('Front | left display photo glass',(100,474,215,550)),
                         ('Front | right display photo glass',(821,474,943,549))]:
    pane=next(o for o in data['objects'] if o['name']==pane_name)
    uv=pane['face_uvs'][0]; verts=[pane['vertices_m'][i] for i in pane['faces'][0]]
    x0,y0,x1,y1=pixels
    corners=[]
    for u,v in ((x0/1024,1-y0/751),(x1/1024,1-y0/751),(x1/1024,1-y1/751),(x0/1024,1-y1/751)):
        s=(u-uv[0][0])/(uv[1][0]-uv[0][0]);t=(v-uv[0][1])/(uv[3][1]-uv[0][1])
        assert 0<s<1 and 0<t<1
        p=[verts[0][i]+s*(verts[1][i]-verts[0][i])+t*(verts[3][i]-verts[0][i]) for i in range(3)]
        p[1]-=.012 # outside the glazing plane, avoiding coincident surfaces
        corners.append(p)
    data['objects'].append({'name':pane_name+' | sharp drinks plaque','vertices_m':corners,'faces':[[0,1,2,3]],
        'triangles':[[0,1,2],[0,2,3]],'face_uvs':[[[0,1],[1,1],[1,0],[0,0]]],
        'material':'Reconstructed drinks plaque','color':[1,1,1,1],
        'image':{'path':str(ROOT/'assets/signage/drinks-plaque.png'),'dimensions':[1024,1024],'name':'Reconstructed drinks plaque'},
        'procedural':False,'slab':False})
OUT=ROOT/'assets/playtest-v18'; OUT.mkdir(exist_ok=True)
template=(ROOT/'assets/photos/pharmacie.gdt').read_text()
ib=re.search(r'\s*"i_pharmacie_frontage" \( "image.gdf" \).*?\n\s*\}',template,re.S).group()
mb=re.search(r'\s*"pharmacie_frontage" \( "material.gdf" \).*?\n\s*\}',template,re.S).group()
materials={}; blocks=[]; records=[]
for o in data['objects']:
    if o['procedural']:
        materials[o['material']]={'name':'t7_brick_worn_heavy_grout_red' if 'brick' in o['material'].lower() else 't7_wood_planks_damaged_teak','dimensions':[128,128]}
        continue
    source=o['image']['path'] if o['image'] else None
    if source:
        # Keep Blender's original UVs on the full bitmap. Per-pane crops changed
        # storage dimensions and made the remaining engine alignment ambiguous.
        uv=o['face_uvs'][0]; u0=min(p[0] for p in uv); u1=max(p[0] for p in uv)
        v0=min(p[1] for p in uv); v1=max(p[1] for p in uv)
        assert u1-u0>1e-7 and v1-v0>1e-7, o['name']
        identity='full-source-square-v3:'+hashlib.sha256(Path(source).read_bytes()).hexdigest()
        o['material']='Panel | '+o['name']
        with Image.open(source) as original:
            w,h=original.size
            crop=None
            image=original.convert('RGB')
            side=min(4096,max(32,2**math.ceil(math.log2(max(image.size)))))
            dims=(side,side)
            image=image.resize(dims,Image.Resampling.LANCZOS)
    else:
        identity='color:'+repr(o['color']); dims=(256,256);crop=None
        image=Image.new('RGB',dims,tuple(round(max(0,min(1,c))*255) for c in o['color'][:3]))
    key=o['material']
    if key in materials: continue
    asset='pharmacie_pt18_'+hashlib.sha256(identity.encode()).hexdigest()[:12]
    materials[key]={'name':asset,'dimensions':list(dims)}
    if any(r['asset']==asset for r in records):continue
    image.save(OUT/f'{asset}.tif')
    blocks.append(ib.replace('i_pharmacie_frontage','i_'+asset).replace('texture_assets\\pharmacie\\frontage.tif',f'texture_assets\\pharmacie_pt18\\{asset}.tif'))
    block=mb.replace('i_pharmacie_frontage','i_'+asset).replace('"pharmacie_frontage"','"'+asset+'"')
    block=block.replace('"alphaTest" "0.5"',f'"alphaTest" "Always"\n\t\t"tilingWidth" "{dims[0]}"\n\t\t"tilingHeight" "{dims[1]}"\n\t\t"filterColor" "aniso8x (mip linear)"\n\t\t"tileColor" "no tile"')
    if not source:
        for prop in ('nonColliding','nonSolid','noCastShadow'):block=block.replace(f'"{prop}" "1"',f'"{prop}" "0"')
    blocks.append(block)
    records.append({'asset':asset,'source':source,'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest() if source else None,'crop_pixels':crop,'dimensions':list(dims),'edits':'Full source bitmap stored in square power-of-two RGB TIFF; original Blender UVs retained without rebounding or pane cropping; source unchanged' if source else 'Blender flat-colour placeholder'})
(OUT/'pharmacie_pt18.gdt').write_text('{\n'+''.join(blocks)+'\n}\n')
(OUT/'manifest.json').write_text(json.dumps({'assets':records,'materials':materials},indent=2)+'\n')
(ROOT/'build/playtest-v18-panels.json').write_text(json.dumps(data))
# Use the proven brush/prism converter, with explicit substitutions checked below.
code=(ROOT/'scripts/generate_blender_test_map.py').read_text()
code=code.replace("NAME='zm_pharmacie_blender'",f"NAME='{NAME}'").replace('build/blender-test-geometry.json','build/playtest-v18-panels.json').replace('build/blender-test-export-report.json','build/playtest-v18-export-report.json')
start=code.index('def texture(o):');end=code.index('\ndef convex_brush',start)
code=code[:start]+"def texture(o):\n    return materials[o['material']]['name']\n"+code[end:]
start=code.index("    if material.startswith('Frontage photo')");end=code.index('    if photo:',start)
code=code[:start]+"    if o['image'] and len(o['faces'])==1:\n        item=materials[material];photo=(item['name'],item['dimensions'])\n"+code[end:]
code=code.replace('))<.60:', '))<.15:')
# Match the valid 2x2 lightmap coordinates used by our first verified photo map.
code=code.replace('for indices in ((0,1),(3,2)):', 'for row,indices in enumerate(((0,1),(3,2))):')
code=code.replace('for i in indices:', 'for col,i in enumerate(indices):')
code=code.replace("{f((1-v)*dims[1])} 0 0')", "{f((1-v)*dims[1])} {col} {row}')")
code=code.replace('assert len(sky)==6',"assert len(sky)==6\nsky=[box_brush(9000+i,b,'sky','\\n') for i,b in enumerate([(-2800,3000,-2500,2300,-140,-120),(-2800,3000,-2500,2300,1100,1120),(-2820,-2800,-2500,2300,-140,1120),(3000,3020,-2500,2300,-140,1120),(-2800,3000,-2520,-2500,-140,1120),(-2800,3000,2300,2320,-140,1120)])]")
code=code.replace("p=(2.7+(spawn%2)*.85,2.5+(spawn//2)*.85,.72)","p=(5.5,[3.2,4.4,5.6,8.4][spawn%4],.12)")
code=code.replace('(3.45,3.3,.72)','(5.5,3.2,.12)')
# Prefabs below are rewritten after conversion; never inherit scale-test invulnerability.
exec(compile(code,str(ROOT/'scripts/generate_blender_test_map.py'),'exec'),globals())
path=ROOT/'map_source/zm'/f'{NAME}.map'; text=path.read_text(); entities=parse_entity_blocks(text)
def world(p):return tuple((p[i]+SHIFT[i])*UNIT for i in range(3))
def bounds(b):
    lo=world((b[0],b[2],b[4]));hi=world((b[1],b[3],b[5]))
    return (lo[0],hi[0],lo[1],hi[1],lo[2],hi[2])
def entity(props,brush=''):
    return '{\n'+''.join(f'"{k}" "{v}"\n' for k,v in props.items())+brush+'}\n'
def point(p):return ' '.join(f'{v:.6f}' for v in world(p))
kept=[]; prefabs={
    'power_switch.map':((7.6,6,4.82),'0 270 0'),
    'buyable_magic_box_start.map':((-16,-1.3,.02),'0 0 0'),
    'vending_revive_struct.map':((.2,2.7,.02),'0 90 0'),
    'spawnable_weapon_shotgun_pump.map':((-4.53,26,.02),'0 98.22 0')}
for _,_,block in entities[1:]:
    cls=kv(block,'classname');note=kv(block,'script_noteworthy')
    if cls in ('info_volume','light') or note in ('riser_location','dog_location'):continue
    if cls=='misc_prefab':
        match=next((v for k,v in prefabs.items() if (kv(block,'model') or '').endswith(k)),None)
        if not match:continue
        block=position(block,*match)
    kept.append(block)
# Stock chalk/model/weapon_upgrade prefabs include the real wall-buy logic.
wallbuys=[('pistol_burst',(-1.84,3.5,.02),'0 92.87 0'),
          ('smg_standard',(-15,-.08,.02),'0 0 0'),
          ('ar_standard',(-2.71,14,4.82),'0 97.22 0')]
for weapon,p,angles in wallbuys:
    kept.append(entity({'classname':'misc_prefab','model':f'_prefabs/zm/zm_core/spawnable_weapon_{weapon}.map','origin':point(p),'angles':angles}))
# BO3 lights use stops/radius/def; the legacy 'light=140' field is insufficient.
lights=[(x,y,z) for z in (3.65,8.25) for y in (4,9,14,19) for x in (.3,7.4)]
lights += [(-2.8,25,3.65),(1.2,29.75,3.8),(4.6,29.75,7.7),(6.6,26,8.4),(-11.4,11,3.5),(-11.4,27,3.5),(5,-5,5),(-15,-4,5),(24,-4,5)]
lights += [(39,-5,5),(54,-5,5),(46.5,-21,4)]
for p in lights:
    kept.append(entity({'classname':'light','origin':point(p),'_color':'1 0.86 0.68','def':'white_light',
       'PRIMARY_TYPE':'PRIMARY_OMNI','radius':'300','stops':'8','bulbRadius':'4','penumbraRadius':'4',
       'ENABLE_FALLOFF':'1','falloffdistance':'12','lightingstate1':'1','lightingstate2':'1','lightingstate3':'1','lightingstate4':'1',
       'client_server':'ClientSide','name':'pt18_warm_fill','shadowUpdate':'Never','spawnflags':'0'}))
# Distinct non-overlapping heights; street loop uses several connected volumes.
zones={'start_zone':[(-8,11,-.02,31.1,-.5,4.35)],
       'street_zone':[(-18,30,-13,-.02,-.5,4.35),(-13.1,-9.8,0,33.1,-.5,4.35),(-13.1,2,31.1,34.5,-.5,4.35)],
       'upstairs_zone':[(-8,11,0,31.1,4.35,9.1)],
       'crossing_zone':[(30,60,-13,0,-.5,4.35),(45,48,-30,-13,-.5,4.35)]}
for zone,volumes in zones.items():
    for b in volumes:
        kept.append(entity({'classname':'info_volume','targetname':zone,'target':zone+'_spawners','script_noteworthy':'player_volume'},volume_brush(0,bounds(b),'\n')))
risers={'start_zone':[(3.45,5.6,.03),(2.5,14.7,.03),(-2.8,25,.03)],
        'street_zone':[(2,-11.5,.03),(23,-11.5,.03),(-14,-1.5,.03)],
        'upstairs_zone':[(3.45,5.6,4.83),(3.45,14.7,4.83)],
        'crossing_zone':[(36,-11.8,.03),(55,-11.4,.03),(46.5,-24,.03)]}
for zone,positions in risers.items():
    for p in positions:
        kept.append(entity({'classname':'script_struct','origin':point(p),'angles':'0 90 0','script_noteworthy':'riser_location','script_string':'find_flesh','targetname':zone+'_spawners'}))
# Stock debris removes linked brushmodels and reconnects navigation on purchase.
gates=[('street',750,[(4.50,6.50,.45,.65,0,3.15),(-4.20,-1.90,30.62,30.86,0,3.15)],[(4.50,6.50,.90,2.10,.1,2.1),(-4.2,-1.9,29.30,30.35,.1,2.1)]),
       ('stairs',1000,[(-1.48,-1.25,29.02,30.53,0,3.15)],[(-2.85,-1.65,29.02,30.53,.1,2.1)]),
       ('crossing',1250,[(30,30.35,-13.1,0,-.2,4)],[(28.65,29.65,-7,-4,.1,2.1),(30.70,31.70,-7,-4,.1,2.1)])]
trim=materials['Blockout - dark shopfront trim']['name']
for name,cost,solids,triggers in gates:
    target='pt18_'+name+'_gate'
    for b in solids:
        kept.append(entity({'classname':'script_brushmodel','targetname':target,'script_noteworthy':'clip','DYNAMICPATH':'1','spawnflags':'1'},box_brush(0,bounds(b),'clip','\n')))
        if name=='crossing':
            kept.append(entity({'classname':'script_brushmodel','targetname':target},box_brush(0,bounds(b),'t7_wood_planks_damaged_teak','\n')))
            continue
        # Visible framed gate; separate invisible collision owns the nav cut.
        x0,x1,y0,y1,z0,z1=b
        pieces=[(x0,x1,y0,y1,z0,.80),(x0,x1,y0,y1,2.85,z1)]
        if x1-x0>y1-y0:
            pieces += [(x0,x0+.10,y0,y1,.8,2.85),(x1-.10,x1,y0,y1,.8,2.85),((x0+x1)/2-.045,(x0+x1)/2+.045,y0,y1,.8,2.85),(x0,x1,y0,y1,1.35,1.45)]
        else:
            pieces += [(x0,x1,y0,y0+.10,.8,2.85),(x0,x1,y1-.10,y1,.8,2.85),(x0,x1,y0,y1,1.35,1.45),(x0,x1,y0,y1,2.1,2.2)]
        for piece in pieces:
            kept.append(entity({'classname':'script_brushmodel','targetname':target},box_brush(0,bounds(piece),trim,'\n')))
    for b in triggers:
        center=((b[0]+b[1])/2,(b[2]+b[3])/2,(b[4]+b[5])/2)
        kept.append(entity({'classname':'trigger_use','origin':point(center),'cursorhint':'HINT_ACTIVATE','targetname':'zombie_debris','target':target,'script_flag':'pt18_'+name+'_open','zombie_cost':str(cost)},box_brush(0,bounds(b),'trigger','\n')))
# Short playable street; closed scenery remains visible beyond end barricades.
extras=[(-18.35,-18,-13.1,0,-.2,4),(60,60.35,-13.1,0,-.2,4),
        (-18,45,-13.35,-13,-.2,4),(48,60,-13.35,-13,-.2,4),
        (45,48,-30.35,-30,-.2,4),(-13.1,2,34.5,34.85,-.2,4)]
worldblock=entities[0][2]
# Invisible shallow collision ramp joins the platform's aisle edge to main floor.
# It covers the observed AI island at x6.2,y5.6; visible platform stays unchanged.
rampverts=[(x,y,z) for y in (3.30,12.90) for x,z in ((5.65,-.03),(6.12,-.03),(6.12,.27),(5.65,.003))]
rampfaces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
ramp=convex_brush('PT18 platform navigation ramp',[world(v) for v in rampverts],rampfaces,'clip',10100)
assert ramp
worldblock=worldblock[:worldblock.rfind('}')]+''.join(box_brush(10000+i,bounds(b),'t7_wood_planks_damaged_teak','\n') for i,b in enumerate(extras))+ramp+'}\n'
clipbounds=[(30,60,0,.2,-.2,4),(44.8,45,-30,-13,-.2,4),(48,48.2,-30,-13,-.2,4)]
worldblock=worldblock[:worldblock.rfind('}')]+''.join(box_brush(10120+i,bounds(b),'clip','\n') for i,b in enumerate(clipbounds))+'}\n'
if CALIBRATE:
    # Same bitmap/material/lighting/geometry size; only texture coordinates vary.
    # Initial pub spawn faces these non-solid reference surfaces. Remove after
    # the full-image scale is established in actual BO3, not guessed from docs.
    key='Panel | Left wall | pharmacy display backing segment 1'
    material=materials[key]['name']
    panels=[]
    for i,scale in enumerate((1,128,2048)):
        x=2.55+i*1.65
        panel={'name':f'UV calibration {scale}', 'vertices_m':[(x,6.05,2.9),(x+1.5,6.05,2.9),(x+1.5,6.05,.65),(x,6.05,.65)],'faces':[[0,1,2,3]],'face_uvs':[[[0,1],[1,1],[1,0],[0,0]]]}
        panels.append(photo_patch(panel,10200+i,material,(scale,scale)))
    worldblock=worldblock[:worldblock.rfind('}')]+''.join(panels)+'}\n'
path.write_text(text[:entities[0][0]]+worldblock+'\n'.join(kept),newline='\n')
gsc=ROOT/'usermaps'/NAME/'scripts/zm'/f'{NAME}.gsc'
script=gsc.read_text()
script=script.replace('level flag::set( "always_on" );','level flag::set( "always_on" );\n\tzm_zonemgr::add_adjacent_zone( "start_zone", "street_zone", "pt18_street_open" );\n\tzm_zonemgr::add_adjacent_zone( "start_zone", "upstairs_zone", "pt18_stairs_open" );\n\tzm_zonemgr::add_adjacent_zone( "street_zone", "crossing_zone", "pt18_crossing_open" );')
assert 'round_spawn_func' not in script and 'EnableInvulnerability' not in script
gsc.write_text(script)
report=ROOT/'build/playtest-v18-export-report.json';summary=json.loads(report.read_text())
summary.update({'zones':zones,'risers':risers,'purchases':{'street_front_and_rear':750,'stairs':1000},'assets':len(records),'uv_calibration':{'enabled':CALIBRATE,'left_to_right_texture_coordinate_spans':[1,128,2048]},'wallbuys':wallbuys+[('shotgun_pump',(-4.53,26,.02),'0 98.22 0')],'lights':len(lights),'navigation_fix':'Shallow clip ramp along raised platform aisle edge; runtime retest required','limitations':'Brush conversion boxes curved detail; procedural brick/wood use stock placeholders; explicit material tiling and higher resolution await runtime UV verification; collision/AI/co-op pending','zombie_spawning':'Stock rounds, zone-gated risers; no no-spawn callback or invulnerability'})
report.write_text(json.dumps(summary,indent=2)+'\n')
summary['purchases']['crossing']=1250
summary['bar_regions']=bar_records
report.write_text(json.dumps(summary,indent=2)+'\n')
print('PLAYTEST',NAME,'assets',len(records),'zones',len(zones),'risers',sum(map(len,risers.values())))
