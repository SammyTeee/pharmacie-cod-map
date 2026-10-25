"""Separate paid-progression pub/nearest-street copy with textured model visuals.

Retains corrected v58 collision inside the chosen core and v18 stock gameplay.
The full route and all original projects remain unchanged.
"""
from pathlib import Path
import hashlib
import json
import re
from generate_blockout import parse_entity_blocks, kv, box_brush, volume_brush
from bo3_map_io import parse_map_entities

ROOT = Path(__file__).resolve().parents[1]
NAME = 'zm_pharmacie_core65'
OUT = ROOT/'build/bo3-core'
UNIT = 100/2.54
SHIFT = (-3.5, -10, 0)
report = json.loads((OUT/'model-report.json').read_text())
number = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
brush_re = re.compile(r'(?ms)^// brush \d+\n\{.*?^\}\n?')
point_re = re.compile(r'\(\s*('+number+r')\s+('+number+r')\s+('+number+r')\s*\)')


def world(p):
    return tuple((p[i]+SHIFT[i])*UNIT for i in range(3))


def bounds(b):
    lo, hi = world((b[0],b[2],b[4])), world((b[1],b[3],b[5]))
    return (lo[0],hi[0],lo[1],hi[1],lo[2],hi[2])


def entity(values, brush=''):
    return '{\n'+''.join(f'"{k}" "{v}"\n' for k,v in values.items())+brush+'}\n'


def origin(p):
    return ' '.join(f'{v:.6f}' for v in p)


source_path = ROOT/'map_source/zm/zm_pharmacie_v58.map'
source = source_path.read_text()
# Undo only v58's documented whole-map translation, for this separate core.
def undo(m):
    p = list(map(float,m.groups()))
    p[1] += 18000
    return '( '+' '.join(f'{v:.6f}' for v in p)+' )'

source = point_re.sub(undo,source)
old_entities = parse_map_entities(source)
collision_text = old_entities[0][2]+'\n'+''.join(b for _,_,b in old_entities[1:] if kv(b,'classname')=='script_brushmodel' and (not kv(b,'targetname') or (kv(b,'targetname') or '').startswith('v58_static_surface_')))
collision, rejected = [], 0
core_lo, core_hi = world((-55,-30,-4)), world((68,38,24))
for match in brush_re.finditer(collision_text):
    b = match[0]
    if '\n mesh\n' in b or 'nonColliding' in b or re.search(r'\)\s+sky\s',b):
        continue
    points = [tuple(map(float,p)) for p in point_re.findall(b)]
    if not points:
        continue
    if not all(core_lo[i]-.2 <= p[i] <= core_hi[i]+.2 for p in points for i in range(3)):
        rejected += 1
        continue
    # Keep geometry/contents exactly, using invisible collision backing.
    b = re.sub(r'(\)\s+)[^\s()]+(?=\s+128\s+128)',r'\1caulk',b)
    collision.append(b)

base_path = ROOT/'map_source/zm/zm_pharmacie_playtest.map'
base = base_path.read_text()
entities = parse_map_entities(base)
old_world = entities[0][2]
prefix = old_world[:brush_re.search(old_world).start()]
sky = []
for i,b in enumerate([(-65,80,-40,50,-14,-13.5),(-65,80,-40,50,30,30.5),
                       (-65.5,-65,-40,50,-14,30.5),(80,80.5,-40,50,-14,30.5),
                       (-65,80,-40.5,-40,-14,30.5),(-65,80,50,50.5,-14,30.5)]):
    sky.append(box_brush(900000+i,bounds(b),'sky','\n'))
# Explicit continuous support is independent of clipped visual models and paid
# blockers. No cellar/brook lies in this core. The safety foundation also backs
# otherwise closed/scenery plots, so an unexpected escape cannot reach the void.
collision.append(box_brush(910000,bounds((-55,68,-30,38,-2,-.16)),'t7_concrete_trowelled','\n'))
collision.append(box_brush(910001,bounds((-55,68,-13,-3,-.45,-.08)),'caulk','\n'))
collision.append(box_brush(910002,bounds((-34,66,-3,.02,-.45,0)),'caulk','\n'))
# Bridge the actual missing front entrance strip (y .1..1.4 in the source
# audit), overlapping the retained pub floor and forecourt. This never belongs
# to the paid door group, so buying street access cannot remove its support.
collision.append(box_brush(910003,bounds((4.40,6.55,-.10,1.62,-.45,0)),'caulk','\n'))
closure = []
# Solid walls close every outer edge, visible barriers identify street exits.
for i,b in enumerate([(-55.25,-55,-30,38,-2,24),(56,56.25,-30,38,-2,24),
                       (-55,68,-30.25,-30,-2,24),(-55,68,38,38.25,-2,24)]):
    collision.append(box_brush(920000+i,bounds(b),'clip','\n'))
for i,b in enumerate([(-55,-54.3,-13,0,-.12,1.65),(55.6,56,-13,0,-.12,1.65)]):
    closure.append(box_brush(930000+i,bounds(b),'t7_concrete_trowelled','\n'))
world_block = prefix+''.join(sky+collision+closure)+'}\n'

kept = []
initial_origins = set()
for _,_,block in entities[1:]:
    model = kv(block,'model') or ''
    if 'buyable_magic_box_start.map' in model:
        continue  # Existing base/rubble is not a working mystery box.
    if kv(block,'script_noteworthy') == 'initial_spawn':
        p = kv(block,'origin')
        if p in initial_origins:
            continue
        initial_origins.add(p)
    if kv(block,'classname') == 'light':
        # Lower the earlier fill intensity; tune with the actual lit runtime.
        block = block.replace('"stops" "8"','"stops" "5"')
    kept.append(block)

for m in report['models']:
    kept.append(entity({'classname':'misc_model','model':m['asset'], 'origin':origin(m['origin_engine']),
                        'angles':'0 0 0','modelscale':'1','static':'1',
                        'lightingstate1':'1','lightingstate2':'1','lightingstate3':'1','lightingstate4':'1'}))

# Extend the local street volumes to the explicit visible end barriers.
for zone,b in [('street_zone',(-55,-18,-13,0,-.5,4.35))]:
    kept.append(entity({'classname':'info_volume','targetname':zone,'target':zone+'_spawners',
                        'script_noteworthy':'player_volume'},volume_brush(0,bounds(b),'\n')))
for x in (-44,-28):
    kept.append(entity({'classname':'script_struct','origin':origin(world((x,-6.5,-.10))),
                        'angles':'0 90 0','script_noteworthy':'riser_location','script_string':'find_flesh',
                        'targetname':'street_zone_spawners'}))

header = base[:base.index('// entity 0')]
map_text = header+'// entity 0\n'+world_block+'\n'+''.join(f'// entity {i}\n'+b+'\n' for i,b in enumerate(kept,1))
map_path = ROOT/'map_source/zm'/f'{NAME}.map'
map_path.write_text(map_text,newline='\n')

# Copy the original project source with its normal costs and round loop.
old_project = ROOT/'usermaps/zm_pharmacie_playtest'
project = ROOT/'usermaps'/NAME
for path in old_project.rglob('*'):
    if not path.is_file():
        continue
    relative = str(path.relative_to(old_project)).replace('zm_pharmacie_playtest',NAME)
    dest = project/relative
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(path.read_text().replace('zm_pharmacie_playtest',NAME))
zone_path = project/'zone_source'/f'{NAME}.zone'
zone_path.write_text(zone_path.read_text()+'\n// Detailed core model assets\n'+''.join('xmodel,'+m['asset']+'\n' for m in report['models']))
gsc = project/'scripts/zm'/f'{NAME}.gsc'
script = gsc.read_text()
script = script.replace('zm_usermap::main();','level.round_prestart_func = &core65_first_round_prestart;\n\tzm_usermap::main();\n\tlevel thread core65_ground_diagnostics();',1)
script += '''
function core65_first_round_prestart()
{
\tif (!IsDefined(level.core65_prep_done))
\t{
\t\tlevel.core65_prep_done = true;
\t\tIPrintLnBold("Prepare: first wave in 60 seconds");
\t\t/# PrintLn("CORE65_PREPARATION_BEGIN seconds=60"); #/
\t\twait(4);
\t\tIPrintLnBold("Bartender: You need to get down to Taraj for a Chicken Jalfrezi.");
\t\t/# PrintLn("CORE65_STORY_INTRO taraj_jalfrezi"); #/
\t\twait(7);
\t\tIPrintLnBold("Bartender: First, keep this pub standing. We will sort the road out after.");
\t\twait(49);
\t\t/# PrintLn("CORE65_PREPARATION_COMPLETE"); #/
\t}
\telse
\t{
\t\twait(2);
\t}
}
'''
points = [world((x,y,0)) for x in (5.08,5.5,5.92) for y in (1.4,1.0,.6,.2,-.2,-.6,-1,-2,-3.5)]
script += '\nfunction core65_ground_diagnostics()\n{\n\tlevel endon("end_game");\n\twait(4);\n\tpoints = [];\n'
for i,p in enumerate(points):
    script += '\tpoints['+str(i)+'] = ('+', '.join(f'{v:.6f}' for v in p)+');\n'
script += '''\tmissing = 0;
\tforeach (p in points)
\t{
\t\ttrace = BulletTrace(p + (0,0,8), p - (0,0,28), false, undefined);
\t\tif (trace["fraction"] >= 1)
\t\t{
\t\t\tmissing++;
\t\t\t/# PrintLn("CORE65_GROUND_MISS " + p); #/
\t\t}
\t\twait(.01);
\t}
\t/# PrintLn("CORE65_GROUND_RESULT points=" + points.size + " missing=" + missing); #/
}
'''
gsc.write_text(script)
assert 'round_spawn_func' not in gsc.read_text() and 'EnableInvulnerability' not in gsc.read_text()
assert '"zombie_cost" "750"' in map_text and '"zombie_cost" "1000"' in map_text
result = {'map':str(map_path.relative_to(ROOT)), 'source_visuals':report['source'],
          'visual_triangles':report['triangles'], 'visual_models':len(report['models']),
          'collision_brushes':len(collision), 'excluded_noncore_collision_brushes':rejected,
          'visual_bounds_BU':report['bounds_BU'], 'paid_gates':{'street':750,'upstairs':1000,'crossing':1250},
          'source_collision_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
          'map_sha256':hashlib.sha256(map_path.read_bytes()).hexdigest(),
          'scope':'Pub, nearest shopfronts and street only. Full route is excluded; four outer clip walls and two visible road barriers.',
          'pending':['Official asset/map compilation','Fresh lighting/link','Runtime texture and gameplay verification']}
(OUT/'map-report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('visual_triangles','visual_models','collision_brushes','excluded_noncore_collision_brushes')}))
