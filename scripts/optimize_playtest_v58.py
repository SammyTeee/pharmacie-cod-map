"""Make dressing detail brushes; repair route adjacency before official retry."""
from pathlib import Path
import json,re,math,uuid
from generate_blockout import parse_entity_blocks,kv,volume_brush
ROOT=Path(__file__).resolve().parents[1];NAME='zm_pharmacie_v58';UNIT=100/2.54
path=ROOT/'map_source/zm'/f'{NAME}.map';text=path.read_text();entities=parse_entity_blocks(text)
a,b,world=entities[0];count=0
world=re.sub(r'(\{\n) contents detail;\n( guid "[^\n]+\n)',r'\1\2 contents detail;\n',world)
data=json.loads((ROOT/'build/playtest-v58-geometry.json').read_text())
ns=uuid.UUID('a97a09a7-4d35-4953-b8c1-658d4f91f704')
structural={str(uuid.uuid5(ns,o['name'])) for o in data['objects'] if o['name'].startswith(('Ground shell','First shell'))}
def detail(match):
 global count
 brush=match[0]
 if re.search(r'\)\s+sky\s',brush) or '\n mesh\n' in brush or re.search(r'contents [^;]*\bdetail;',brush):return brush
 guid=re.search(r'guid "\{([^}]+)',brush)
 if guid and guid[1] in structural:return brush
 count+=1
 # Noncolliding decoration still remains visible detail, rather than BSP dividers.
 return re.sub(r'( guid "[^\n]+\n)',r'\1 contents detail;\n',brush,count=1)
world=re.sub(r'(?ms)^// brush \d+\n\{.*?^\}\n?',detail,world)
world=world.replace('contents detail;\n contents nonColliding;', 'contents nonColliding detail;')
text=text[:a]+world+text[b:]
if '// v58 street junction coverage' not in text:
 box=(-50,-18,-13,0,-.45,4.3)
 bound=((box[0]-3.5)*UNIT,(box[1]-3.5)*UNIT,(box[2]-10)*UNIT,(box[3]-10)*UNIT,box[4]*UNIT,box[5]*UNIT)
 text+='\n// v58 street junction coverage\n{\n"classname" "info_volume"\n"targetname" "street_zone"\n"target" "street_zone_spawners"\n"script_noteworthy" "player_volume"\n'+volume_brush(0,bound,'\n')+'}\n'
path.write_text(text,newline='\n')
p=ROOT/'docs/build-results/playtest-v58/placements.json';placements=json.loads(p.read_text())
zones=placements['route_zones']
def center(z):
 bb=z['bounds_BU'];return ((bb[0]+bb[1])/2,(bb[2]+bb[3])/2)
groups={key:[z for z in zones if z['name'].startswith('v58_route_'+key+'_')] for key in ('town','main','holmdale','station_access','barkby')}
links=[]
for key,group in groups.items():
 for z0,z1 in zip(group,group[1:]):links.append((z0['name'],z1['name']))
 if key in ('town','barkby'):parent='street_zone'
 elif key=='main':parent=groups['town'][-1]['name']
 else:parent=min(groups['main'],key=lambda z:math.dist(center(z),center(group[0])))['name']
 links.append((parent,group[0]['name']))
gsc=ROOT/'usermaps'/NAME/'scripts/zm'/f'{NAME}.gsc';script=gsc.read_text()
script=re.sub(r'(?m)^\s*zm_zonemgr::add_adjacent_zone\( "[^"]+", "v58_route_[^"]+", "always_on" \);\n?','\n',script)
needle='level flag::set( "always_on" );'
script=script.replace(needle,needle+'\n'+''.join(f'\tzm_zonemgr::add_adjacent_zone( "{x}", "{y}", "always_on" );\n' for x,y in links))
gsc.write_text(script,newline='\n')
out=ROOT/'docs/build-results/playtest-v58/optimization.json'
out.write_text(json.dumps({'detail_brushes_added':count,'detail_brushes_total':len(re.findall(r'contents [^;]*detail;',world)),'retained_structural_shell_guids':len(structural),'zone_adjacency':links,'reason':'First compiler crashed with access violation while emitting cells/portals; decorative solid world brushes should not partition the entire BSP. Stock contents detail and multi-flag syntax inspected locally. Detail collision/nav behavior still requires compiler and runtime checks.'},indent=2)+'\n')
print('Marked',count,'world brushes as detail; retained pub shells and sky as structural; corrected local adjacency')
