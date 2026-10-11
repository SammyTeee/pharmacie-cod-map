"""Separate v57-derived Zombies exploration build; never overwrites v18."""
from pathlib import Path
import json, re, math
ROOT=Path(__file__).resolve().parents[1]
NAME='zm_pharmacie_v58'
# Reuse the previously compiler-proven photo/brush path and prefab bootstrap.
source=(ROOT/'scripts/generate_playtest_v18.py').read_text()
source=source.replace("NAME='zm_pharmacie_playtest'", "NAME='zm_pharmacie_v58'")
source=source.replace('playtest-v18','playtest-v58').replace('pharmacie_pt18','pharmacie_pt58')
source=source.replace('pt18_', 'pt58_')
# Remove the old short-test perimeter; reviewed v57 geometry supplies boundaries.
a=source.index('extras=['); b=source.index('\nworldblock=',a)
source=source[:a]+'extras=[]'+source[b:]
a=source.index('clipbounds=['); b=source.index('\nworldblock=',a)
source=source[:a]+'clipbounds=[]'+source[b:]
source=source.replace("('street',750,", "('street',0,").replace("('stairs',1000,", "('stairs',0,").replace("('crossing',1250,", "('crossing',0,")
exec(compile(source,str(ROOT/'scripts/generate_playtest_v18.py'),'exec'))
# Expand the old fixed sky to contain the actual current exported geometry.
text=path.read_text(); parsed=parse_entity_blocks(text); ws=parsed[0][2]
allverts=[world(v) for o in data['objects'] for v in o['vertices_m']]
ext=[(min(v[i] for v in allverts)-128,max(v[i] for v in allverts)+128) for i in range(3)]
(x0,x1),(y0,y1),(z0,z1)=ext
skyboxes=[(x0,x1,y0,y1,z0-32,z0),(x0,x1,y0,y1,z1,z1+32),
 (x0-32,x0,y0,y1,z0,z1),(x1,x1+32,y0,y1,z0,z1),
 (x0,x1,y0-32,y0,z0,z1),(x0,x1,y1,y1+32,z0,z1)]
skyre=re.compile(r'(?ms)^// brush \d+\n\{.*?^\}\n?')
ws=skyre.sub(lambda m:'' if re.search(r'\)\s+sky\s',m.group()) else m.group(),ws)
ws=ws[:ws.rfind('}')]+''.join(box_brush(500000+i,b,'sky','\n') for i,b in enumerate(skyboxes))+'}\n'
text=text[:parsed[0][0]]+ws+text[parsed[0][1]:]
path.write_text(text,newline='\n')
# Test-only server price override after the legitimate stock weapon table loads.
gsc=ROOT/'usermaps'/NAME/'scripts/zm'/f'{NAME}.gsc'
script=gsc.read_text()
needle='zm_weapons::load_weapon_spec_from_table("gamedata/weapons/zm/zm_levelcommon_weapons.csv", 1);'
assert script.count(needle)==1
script=script.replace(needle,needle+'\n\t// Sam requested free wall weapons and ordinary ammo for this test.\n\tforeach (weapon, spec in level.zombie_weapons)\n\t{\n\t\tlevel.zombie_weapons[weapon].cost = 0;\n\t\tlevel.zombie_weapons[weapon].ammo_cost = 0;\n\t}')
gsc.write_text(script,newline='\n')
csc=ROOT/'usermaps'/NAME/'scripts/zm'/f'{NAME}.csc'
client=csc.read_text()
assert client.count(needle)==1
client=client.replace(needle,needle+'\n\t// Keep the client-filled wall-buy price consistent with the server.\n\tforeach (weapon, spec in level.weapon_costs)\n\t{\n\t\tlevel.weapon_costs[weapon].cost = 0;\n\t\tlevel.weapon_costs[weapon].ammo_cost = 0;\n\t}')
csc.write_text(client,newline='\n')
summary=json.loads(report.read_text());summary.update({'sky_bounds_engine':ext,'test_economy':'Free wall guns, ordinary ammo and route gates; not final balance','source_geometry_objects':len(data['objects'])})
report.write_text(json.dumps(summary,indent=2)+'\n')
print('V58 separate test generated',NAME)
