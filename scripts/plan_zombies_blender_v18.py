"""Explicit progression anchors only; no BO3 entities or collision changes."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1];s=bpy.data.scenes['03 Both floors - assembled exterior']
assert not bpy.data.collections.get('GAMEPLAY v18 | Zombies progression - planning only')
for name in ('GAMEPLAY v17 | Proposed anchors - not exported','GAMEPLAY | Planned spawns and routes - not exported'):
    c=bpy.data.collections.get(name)
    if not c:continue
    for scene in bpy.data.scenes:
        if c.name in scene.collection.children:scene.collection.children.unlink(c)
    c.name='ARCHIVE | '+name;c.use_fake_user=True
c=bpy.data.collections.new('GAMEPLAY v18 | Zombies progression - planning only');s.collection.children.link(c)
records=[]
def anchor(id,label,location,kind,zone,**extra):
    o=bpy.data.objects.new('PLAN v18 | '+id+' | '+label,None);c.objects.link(o);o.location=location;o.empty_display_type='CUBE' if kind=='door' else 'ARROWS';o.empty_display_size=.45;o.show_in_front=True;o.hide_render=True
    o['status']='PROPOSAL; not a working BO3 entity';o['zone']=zone;o['kind']=kind
    for k,v in extra.items():o[k]=str(v)
    records.append(dict(id=id,label=label,location_m=location,kind=kind,zone=zone,status='proposed',**extra))
for i,y in enumerate((3.2,4.4,5.6,8.4)):anchor('S'+str(i+1),'Main pub co-op start',(5.5,y,0),'player_start','start_pub',footprint_verified=False)
anchor('D01','Front entrance buys street',(5.5,.55,0),'door','start_pub',unlocks='street',opening_width_m=1.996,opening_height_m=3.1,price=None,approach='Both sides of existing threshold',linked_rear_door='D03',orientation='Door plane across X; player exits toward -Y')
anchor('D02','Stair-foot gate buys upstairs',(-1.35,29.75,0),'door','start_pub',unlocks='upstairs',opening_width_m=1.41,price=None,approach='Flat floor before first tread; keep purchase trigger off stairs',orientation='Door plane across Y; player climbs toward +X',geometry='Planning marker only; create gate in Radiant or later model pass')
anchor('D03','Rear exit joins alley loop',(-3.05,30.74,0),'door','start_pub',unlocks='street',linked_to='D01',price=None,design='Default proposal: opens with front street purchase; independent price is an alternative')
anchor('P01','Quick Revive near start',(.2,2.7,0),'perk','start_pub',prefab_bounds_verified=False)
anchor('W01','First wall weapon',(-1.9,3.0,0),'weapon','start_pub',prefab_bounds_verified=False)
anchor('PWR','Power reward upstairs',(7.6,6,4.8),'power','upstairs',placement='Reserve a solid service wall after checking prefab dimensions; provisional')
anchor('BOX','Street-side mystery box',(-16,-1.3,0),'box','street',placement='Pavement placeholder; avoid alley entrance; prefab dimensions pending')
for id,loc,zone in [('Z01',(1,1.8,0),'start_pub'),('Z02',(9,1.4,0),'start_pub'),('Z03',(-2.8,25,0),'start_pub'),('Z04',(2,-11.5,0),'street'),('Z05',(23,-11.5,0),'street'),('Z06',(-14,-1.5,0),'street'),('Z07',(-1,12,4.8),'upstairs'),('Z08',(8,16,4.8),'upstairs')]:
    anchor(id,'Zombie entry candidate',loc,'zombie_entry',zone,placement='Candidate only: barrier/riser, visibility, clearance and paths still require design')
for id,x in [('B01',-18),('B02',30)]:anchor(id,'Initial street combat boundary',(x,-6.5,-.08),'scenery_boundary','street',design='Future visual barrier; scenery continues beyond; not a collider')
manifest={'version':18,'status':'Rough gameplay proposal only','start':'Main ground-floor pub room, not behind counter','zones':[{'id':'start_pub','initially_open':True,'includes':'Ground pub, left rear approach and stair-foot landing'},{'id':'street','initially_open':False,'bounds_x_m':[-18,30],'includes':'Short street section, outer alley and rear loop'},{'id':'upstairs','initially_open':False,'includes':'Upper hall/seating and selected service rooms'}],'anchors':records,'rules':['Closed front and rear street exits must share a coherent unlock rule','Upstairs zombie entries stay disabled until stair gate opens','Purchase volumes must be on flat, supported approaches with space to retreat','Scenery shop interiors stay blocked','All existing geometry doors remain static; markers do not implement locks','Price, prefab orientation/offset, zone volumes and script flags are unimplemented'],'radiant_changed':False,'runtime_verified':False}
(ROOT/'recon/v18/zombies-progression.json').write_text(json.dumps(manifest,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'saved':bpy.data.filepath,'planning_anchors':len(records),'zones':3,'working_game_entities':0}
