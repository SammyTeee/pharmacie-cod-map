"""Structural checks, explicitly not engine/runtime acceptance."""
from pathlib import Path
import json,re,collections,hashlib
from generate_blockout import parse_entity_blocks,kv
ROOT=Path(__file__).resolve().parents[1];name='zm_pharmacie_v58'
p=ROOT/'map_source/zm'/f'{name}.map';s=p.read_text()
# Legacy entity() omits optional comments; index every top-level block for audit.
lines=[];depth=0;number=0
for line in s.splitlines():
 if re.match(r'^// entity \d+$',line):continue
 if line.strip()=='{' and depth==0:
  lines.append(f'// entity {number}');number+=1
 lines.append(line);depth+=line.count('{')-line.count('}')
assert depth==0
s='\n'.join(lines)+'\n';p.write_text(s,newline='\n');entities=parse_entity_blocks(s)
guids=re.findall(r'guid "\{([^}]+)\}"',s)
duplicates=[v for v,n in collections.Counter(guids).items() if n>1]
assert not duplicates,duplicates[:5]
mounts=json.loads((ROOT/'docs/build-results/playtest-v58/placements.json').read_text())
variety=sorted({m['weapon'] for m in mounts['wall_mounts']})
assert len(variety)>=9
zones={kv(b,'targetname') for _,_,b in entities if kv(b,'classname')=='info_volume'}
risers=collections.Counter(kv(b,'targetname') for _,_,b in entities if kv(b,'script_noteworthy')=='riser_location')
assert all(risers[z+'_spawners'] for z in zones if z and z.startswith('v58_route_'))
prefabs=[kv(b,'model') for _,_,b in entities if kv(b,'classname')=='misc_prefab']
offset=(0,-18000,0) if '// v58 engine translation' in s else (0,0,0)
prefab_origins=[(kv(b,'model'),tuple(map(float,kv(b,'origin').split()))) for _,_,b in entities if kv(b,'classname')=='misc_prefab']
for m in mounts['wall_mounts']:
 pos=m['origin_BU'];expected=((pos[0]-3.5)*(100/2.54)+offset[0],(pos[1]-10)*(100/2.54)+offset[1],pos[2]*(100/2.54)+offset[2])
 assert any(model.endswith('spawnable_weapon_'+m['weapon']+'.map') and max(abs(pos[i]-expected[i]) for i in range(3))<.002 for model,pos in prefab_origins),m
tools=Path('S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130/map_source')
assert all((tools/p).is_file() for p in prefabs)
scripts=ROOT/'usermaps'/name/'scripts/zm'
gsc=(scripts/f'{name}.gsc').read_text();csc=(scripts/f'{name}.csc').read_text()
assert 'EnableInvulnerability' not in gsc and 'round_spawn_func' not in gsc
assert 'level.zombie_weapons[weapon].cost = 0' in gsc
assert 'level.weapon_costs[weapon].cost = 0' in csc
gates=[kv(b,'zombie_cost') for _,_,b in entities if kv(b,'targetname')=='zombie_debris']
assert gates and set(gates)=={'0'}
result={'map':name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'map_bytes':p.stat().st_size,'entity_blocks':len(entities),'duplicate_guids':duplicates,'wall_gun_prefabs':sum('spawnable_weapon_' in p for p in prefabs),'variety':variety,'local_route_zones':len(mounts['route_zones']),'road_risers':len(mounts['road_risers']),'noncolliding_small_decor':len(mounts['noncolliding_small_decor']),'free_gate_triggers':len(gates),'engine_offset':offset,'status':'structural checks passed; compiler/runtime pending'}
(ROOT/'docs/build-results/playtest-v58/source-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
