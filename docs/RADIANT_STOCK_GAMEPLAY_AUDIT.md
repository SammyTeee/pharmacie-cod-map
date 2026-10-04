# BO3 stock gameplay audit for the next Radiant conversion

Checked read-only on 2026-10-04 against the installed official Mod Tools and
repository v18 playtest sources. This is an implementation reference, not a
runtime certification. No stock game source/assets were copied, no map changed,
no build/deployment performed and no game/editor input sent.

## Evidence locations and limits

Local root `S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130/`
is abbreviated **TOOLS** below. Project notes identify this installation as
Steam tool app455130 build5284267; the build identifier was not rechecked here.
Line numbers refer to files read from that installation, not web tutorials.
Stock files remain outside Git; collaborators must obtain the official tools.

Bundled primary documentation is present under `TOOLS/docs_modtools/`:
`Radiant_Launcher_QuickStart.pdf`, `Scale_Standards.pdf`, `Generate_LED.pdf`,
`Build_light.pdf`, `Materials.pdf`, `Images.pdf`, `GSC_Language.pdf`,
`Sound_Mod_Docs.pdf` and `bo3_scriptapifunctions.htm`. Quick-start SHA256:
`85a0ade80993b71e0f1aab216061d7983d290387f227b23f827a9f37bbcef62c`.
PDF contents/pages were not newly extracted in this audit; prior project
reading is indexed by [BLENDER_RADIANT_WORKFLOW.md](BLENDER_RADIANT_WORKFLOW.md).

Primary local references:

| Reference | Relevant lines / purpose |
|---|---|
| `TOOLS/share/raw/scripts/zm/_zm_blockers.gsc` | 73–98 initialization;1179–1410 debris purchases, navigation, linked removal |
| `TOOLS/share/raw/scripts/zm/_zm_zonemgr.gsc` | 283–428 volumes/spawner registration;595–625 adjacency;675–807 flags/connections;810–988 management |
| `TOOLS/share/raw/scripts/zm/_zm_power.gsc` | 39–125 switch assembly;173–227 powered items;723–764 global/zone power |
| `TOOLS/share/raw/scripts/zm/_zm_weapons.gsc` | 836–1018 spawnable wall buys and derived interaction bounds |
| `TOOLS/share/raw/scripts/zm/_zm_perks.gsc` | 113–168 machine power;376–612 hints/purchase;661–683 power loss |
| `TOOLS/share/raw/scripts/zm/_zm_magicbox.gsc` | 56–96 initial chest;113–255 sites/cost;266–304 assembly links;546–891 purchases/weapon presentation |
| `TOOLS/share/raw/scripts/zm/_zm_pack_a_punch.gsc` | 82–146 generated interaction/collision/power;578–594 prices |
| `TOOLS/map_source/_prefabs/zm/zm_giant/script/zm_giant_magicboxes.map` | 108–141 complete starting zbarrier/interaction struct example |
| `scripts/generate_playtest_v18.py` | 7 scale;113–220 positions, zones, buys, debris and adjacency |
| `scripts/check_playtest_v18.py` | structural checks; explicitly does not certify runtime mechanics |
| `usermaps/zm_pharmacie_playtest/scripts/zm/zm_pharmacie_playtest.gsc` | stock map initialization, perk imports, weapon table and adjacency |

The latest documented Blender source is [v30](REAR_ALLEY_V30.md),
`assets/blender/pharmacie-zombies-alley-v30.blend`. Existing engine content is
derived from v18; v30 appearance/geometry is not already present in Radiant. Preserve approved
pub/Taraj placement and interiors while reserving gameplay space.

## Important correction: the current box reference is incomplete

`TOOLS/map_source/_prefabs/zm/zm_core/buyable_magic_box_start.map` contains
worldspawn collision and four static cinder-block models. Its 101-line file has
no `treasure_chest_use` struct and no magic-box zbarrier. The generated repository
`map_source/zm/zm_pharmacie_playtest.map` likewise has no `treasure_chest_use`
or magic-box zbarrier marker. Calling this a working mystery box in older notes
was unsupported. Treat the placed outside prefab as a base/rubble reference.

A future functional site needs the complete stock arrangement. Local Giant
example: `zbarrier_zmcore_MagicBox`, `script_noteworthy=start_chest_zbarrier`,
with a colocated `script_struct`, `targetname=treasure_chest_use`,
`script_noteworthy=start_chest`. Stock initialization searches these structs and
matches `<site>_zbarrier` by script_noteworthy. The full animation/model KVPs
must be retained through legitimate stock reference/editor construction;
merely naming a model or placing the decorative base does not supply them.

Default ordinary purchase is950, read at `_zm_magicbox.gsc`135–142. Distinct
moving sites need unique names and matching zbarriers/rubble, and zone ownership
must be checked. Never duplicate the whole Giant prefab at Pharmacie coordinates:
it contains multiple widely separated sites. First prove one complete site,
then add relocations, teddy departure, Fire Sale and eligible-zone checks.

## Coordinate contract and prefab placement

Current exporter uses39.37007874015748 BO3 units per metre and translation
`(-3.5,-10,0)` metres: engine position = (Blender position + translation) × scale.
This is the implemented project conversion, not a universal BO3 design rule.
Prefab placement origin is not necessarily its purchase marker or model centre.

Reference paths below are relative to `TOOLS/map_source/` and must be retained
as stock references rather than copied game files. `misc_prefab` stores the
reference in `model`, with placement `origin` and `angles`. Rotate/place complete
assemblies. Do not rotate the chalk while leaving its interaction behind.

| Feature | Stock reference | Existing v18 origin in Blender metres / Euler angles |
|---|---|---|
| Power | `_prefabs/zm/zm_core/power_switch.map` | (7.6,6,4.82) / 0 270 0 |
| Quick Revive | `_prefabs/zm/zm_core/vending_revive_struct.map` | (0.2,2.7,0.02) / 0 90 0 |
| RK5 | `_prefabs/zm/zm_core/spawnable_weapon_pistol_burst.map` | (-1.84,3.5,0.02) / 0 92.87 0 |
| KRM | `_prefabs/zm/zm_core/spawnable_weapon_shotgun_pump.map` | (-4.53,26,0.02) / 0 98.22 0 |
| Kuda | `_prefabs/zm/zm_core/spawnable_weapon_smg_standard.map` | (-15,-0.08,0.02) / 0 0 0 |
| KN44 | `_prefabs/zm/zm_core/spawnable_weapon_ar_standard.map` | (-2.71,14,4.82) / 0 97.22 0 |
| Box base only | `_prefabs/zm/zm_core/buyable_magic_box_start.map` | (-16,-1.3,0.02) / 0 0 0 |

These are existing authored angles. Visual mounting and interaction on the
playable side of every wall still need Radiant/player-height and runtime review.

## Paid blockers and routes

The project uses stock **debris removal**, not animated hinged doors. A
`trigger_use` has `targetname=zombie_debris`, `target=<gate group>`,
`zombie_cost=<integer>` and `script_flag=<unlock flag>`. Visible debris and its
invisible collision are `script_brushmodel` entities sharing that targetname.
Collision additionally has `script_noteworthy=clip`, `DYNAMICPATH=1`,
`spawnflags=1`. The generator uses brush material `clip` for collision and
`trigger` for use volumes. Explicit trigger origin equals its volume centre.

Local `_zm_blockers` reads the linked clip objects, disconnects their paths at
initialization, checks the valid purchaser/use state and available personal
score, deducts that player's points, sets level unlock flags, reconnects paths,
removes or moves the linked objects and deletes sibling triggers targeting the
same group. Team pool charging is commented out in the inspected debris path.
One player buys; the route and level flag are shared. Simultaneous purchases
still need co-op testing; do not promise race-free behavior from source reading.

| Group | Price | Level flag | Result |
|---|---:|---|---|
| `pt18_street_gate` |750| `pt18_street_open` | both pub front/rear blockers clear; street/alley adjacency opens |
| `pt18_stairs_gate` |1000| `pt18_stairs_open` | stair-foot blocker clears; upstairs adjacency opens |
| `pt18_crossing_gate` |1250| `pt18_crossing_open` | street-end barrier clears; crossing/lane adjacency opens; triggers on both sides |

The front and rear are deliberately one purchase in v18. Future independently
priced shortcuts require separate groups/flags and an explicit adjacency graph.
Do not use a permanent worldspawn wall as paid debris: scripts cannot remove it
with the linked entity group. Do not add a debris movement target unless an
actual destination struct and collision behavior are designed.

Known project failure: use-volume centres inside solid blockers suppressed
prompts. Fixed volumes sit entirely on approach sides; Sam subsequently
confirmed existing pub/stair doors work. A compile cannot verify a purchase.
The current five triggers/four clip objects are checked structurally, but that
does not check animations, all client synchronization or successful AI traversal.

## Zones and spawn ownership

A zone needs at least one `info_volume`, `targetname=<zone name>`,
`target=<zone spawner group>`, `script_noteworthy=player_volume`.
Multiple volume pieces can share one zone; keep the same target on all pieces.
Stock registration reads the first registered volume's target for its spawn
group, so inconsistent targets are unsafe even if the visual volumes look right.

Basic rise points are `script_struct` with
`targetname=<zone spawner group>`, `script_noteworthy=riser_location`,
`script_string=find_flesh`, positioned on supported navigable ground.
These are actual engine entities, distinct from Blender planning markers.

V18 has start/street/upstairs/crossing zones with3/3/2/3 risers respectively.
`level.zone_manager_init_func` installs adjacency; `manage_zones` begins with
`start_zone`. Connections call `zm_zonemgr::add_adjacent_zone` using precisely
the debris flag names above. Enabling a zone and having active player-relevant
spawn locations are distinct states: do not describe all eleven risers as
always spawning. Multi-zone height separation must not leave stair landings
outside every player volume or let upstairs points belong to ground-floor zones.

Preserve launcher-created actor spawner and player entities when replacing
geometry. Template has `info_player_start`, `player_respawn_point` and
`actor_spawner_zm_factory_zombie`; placing rise markers alone is not a complete
Zombies template. Review four-player startup, respawn and spectator behavior.

Template lines230–232 set the editor start at(0,-448,40), yaw90. Lines340–343
define start-room respawn struct target`initial_spawn_points` with
`script_string=zclassic_start_room zcleansed_start_room zgrief_start_room`.
These are template examples, not proposed v30 spawn coordinates; preserve
their functional relationships and explicitly position the four initial points.

## Repairable windows versus ground risers

`_prefabs/zm/zm_core/barricade_reciever_wood.map` (stock spelling **reciever**)
is a repairable receiver reference. It includes an `exterior_goal` struct
targeting the receiver group, a `node_pathnode`, and a
`zbarrier_zmcore_basicwoodbarrier` with six board pieces and animations.
Local positions include exterior_goal(0,50,16), pathnode(0,63,16),
receiver zbarrier(0,47,31), and another struct(0,3,23).

A visually boarded window is not automatically a spawn/repair system. Complete
exterior navigation, approach, traversal and zone association are necessary.
Zone registration matches receiver `script_string` to the zone name and uses
exterior goal/path-node relationships for matching spawn locations. Do not
invent individual traversal-node KVPs from memory: inspect the whole local
stock setup in Radiant, test one window, then replicate the verified assembly.
Ensure inaccessible exterior spawns cannot get stuck outside the map.

## Wall weapons

Stock spawnable prefabs supply chalk and two linked structs: the purchase struct
has `targetname=weapon_upgrade`, `zombie_weapon_upgrade=<weapon id>`, and a
target to the model struct. RK5 example local purchase origin(0,0,56),
model struct(-3,0,55), chalk plane y0 at z50.5..62.5. The pivot is approximately
floor level, with purchase height1.4224m above it under the project conversion.
The local traverse brush is nonColliding; it does not replace the wall itself.

Runtime `_zm_weapons` derives an interaction box from weapon model bounds,
uses the prefab angles, applies an AnglesToRight offset and requires look-at
by default. Adding a separate generic paid trigger would bypass the intended
wall-buy system. Spawn-list matching must stay consistent with the stock CSC
clientfield setup; do not patch only server initialization.

Stock prices checked in
`TOOLS/share/raw/gamedata/weapons/zm/zm_levelcommon_weapons.csv`:
RK5500(line20), KRM750(line24), Kuda1250(line30), KN441400(line15).
The project loads that table in custom_add_weapons. Verify weapon purchase,
ordinary ammo, upgraded ammo, client prompt, chalk/model alignment and alternate
weapon-slot behavior. Never bury the weapon/model-derived interaction box in
the backing wall or an added trim/display case.

## Power, perks and Pack-a-Punch

Power-switch prefab supplies its clip body, `trigger_use` named
`use_elec_switch`, linked server-side handle with `script_noteworthy=elec_switch`,
and `elec_switch_fx` struct. Before rotation its use brush spans approximately
x-8..9,y-24..-5,z38..60 units; its approach is on local negative Y. Handle
origin(-1,-7,45), FX(0.6,-8.3,58.3). Preserve the linkage and FX point.
Stock `_zm_power` sets global `power_on` when no `script_int` power-zone override
exists, updates clientfield power and powers dependent systems. Setting a
custom flag called power is not equivalent to using that stock system.

Perk references available in `zm_core`:
`vending_juggernaut_struct.map`, `vending_doubletap_struct.map`,
`vending_sleight_struct.map`, `vending_marathon_struct.map`,
`vending_revive_struct.map`, `vending_deadshot_struct.map`,
`vending_additionalprimaryweapon_struct.map`. Inspect each full assembly.
Juggernog's machine struct has `targetname=zm_perk_machine`,
`script_noteworthy=specialty_armorvest`, model reference, and linked attack spots;
stock script registration creates behavior. A static machine model alone does
not purchase a perk. Installed `_zm_perk_juggernaut.gsh`4 sets price2500.
Quick Revive has solo-specific behavior; verify solo and co-op separately.
Map GSC already imports the corresponding standard perk scripts.

Quick Revive price override is checked in `_zm_perk_quick_revive.gsc`100–111:
500 solo,1500 otherwise. `_zm_perks.gsc`214–230 chooses solo from player count
or a force/override setting; a solo screenshot does not establish co-op behavior.

PaP reference `_prefabs/zm/zm_core/vending_weapon_upgrade_spawnable.map` contains
`zbarrier_zmcore_packapunch`, targetname`zm_pack_a_punch`, animation/model fields
and supporting light/audio markers. Stock script generates use radius40 units
(minimum documented in that source), height70, vertical offset35, and collision
model `zm_collision_perks1`, with stock power dependency. These are interaction
dimensions, not a measured total machine footprint. Ordinary upgrade5000 and
repeat alternate-ammo2500 are read at lines583–584; mode-dependent alternatives
exist. A bespoke Taraj unlock should control access/availability explicitly;
adding an arbitrary script_flag to the prefab is not proven to implement it.

Reserve space for approach, machine collision, animation and gun retrieval.
Machine mesh bounds were not measured; allow player retreat and a teammate
passage, then measure in Radiant. Test no-power hint, valid purchase, one-user
occupancy, ejection/retrieval, timeout, death/disconnect and upgraded ammo.

## Practical implementation order and acceptance

1. Freeze the reviewed v30 Blender source, or a later explicitly selected
   checkpoint, as a separate conversion export. Compare
   pub/Taraj bounds and key openings with approved source; keep v18 playable
   source/package available. Export markers using the explicit coordinate rule.
2. Import architecture/collision and validate a simple player path before adding
   detail collision. Review stairs, kerbs, platform and both alley exits in
   Radiant. Navigation needs supported walkable surfaces, not visual polygons.
3. Keep stock template main/CSC/zone/sound assets and rounds. Preserve stock
   player/actor scaffolding; remove inherited scale-test callbacks or god mode.
4. Add start zone and one verified stock wall buy/Quick Revive. Build using
   official compiler/navmesh, fresh LED and linker. Read errors, not just exit0.
5. Add one paid route, its clip, a second zone and spawn group. Observe blocked
   pursuit before purchase, cost once, visible/collision removal, prompt removal,
   shared unlock and pursuit afterward. Repeat for stairs and crossing.
6. Add complete power/perks, then complete box assembly and PaP. Each feature
   gets its own runtime acceptance row before further decoration or scripting.
7. Expand to two-player then four-player private testing, including separate
   players in pub/upstairs/Taraj, simultaneous use, revive near doors, respawn,
   migration/disconnect where applicable and rounds beyond early testing.

Use `scripts/build-map.ps1` and its current documented asset-database procedure,
fresh-lighting wait and error checks; do not run those actions in this planning
task. Future authorized deployment must include the whole linked zone/snd tree,
hash verification and backup, with BO3 closed; Sam retains game controls.

Failures to specifically inspect: missing trigger prompts; nav cuts persisting
after purchase; hidden fixed collision in decorative geometry; furniture goals
off navmesh; unowned spawn groups; upstairs floor/ceiling zone overlap; zombies
trapped behind windows; box rubble mistaken for box functionality; model-only
perks; PaP animation intersecting walls; omissions from asset/CSC/sound linkage.

Current evidence supports compiler/solo combat/rounds for earlier v18 packages,
Sam's pub/stair door confirmation and sharp-window approval. Crossing/bar is
built but pending deployment in the recorded handover. All individual wall-buy,
power, box, PaP, pursuit-route and co-op acceptance remains to be recorded from
actual observations. Never upgrade these statuses based on this source audit.
