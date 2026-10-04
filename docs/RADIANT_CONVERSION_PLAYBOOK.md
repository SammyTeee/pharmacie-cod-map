# Pharmacie: BO3 Radiant conversion playbook

Prepared 4 October 2026 at Sam's request: turn the detailed Blender scene into
a conventional Zombies map with properly placed wall weapons, reached-room
power, perks and paid routes. **This pass researches and specifies the work;
it does not export, compile, deploy or change the running game.**

## Read this packet before converting

| Document | Use |
|---|---|
| [Current rear-alley handover](REAR_ALLEY_V30.md) | Latest documented Blender checkpoint; approved architecture and actual geometry checks |
| [Zombies design](ZOMBIES_DESIGN_V29.md) | Combat scope, progression, future rewards and modelling constraints |
| [Placement specification](RADIANT_GAMEPLAY_PLACEMENT_PLAN.md) | Each door, zone, gun, power/item site and manual acceptance case |
| [Placement registry](radiant-gameplay-plan.json) | Stable IDs, legacy exact anchors, bounds and proposed locations still unset |
| [Installed stock audit](RADIANT_STOCK_GAMEPLAY_AUDIT.md) | Actual prefab paths, entity relationships, script lines and known gaps |
| [Saved tutorial library](../research/radiant/tutorial-library/README.md) | Offline licensed text tutorials and supporting author links |
| [Existing workflow](RADIANT_WORKFLOW.md) / [conversion constraints](BLENDER_RADIANT_WORKFLOW.md) | Tool operations, exporter limitations and recorded build failures/results |
| [Last engine handover](HANDOVER_2026-10-03.md) | Actual deployed vs built state; Sam's controls and deployment procedure |

Evidence labels used below: **LOCAL** means inspected installed stock/repo
source; **RECORD** means earlier documented build or user observation;
**GUIDE** means authored tutorial/bundled-doc guidance; **PLAN** means proposed
behavior; **PENDING** means not proved in the actual editor or game. File names
are not proof of functionality. A compiler success is not a gameplay pass.

## The intended player experience

The player starts in the pub and can immediately recognize a starter wall gun
and Quick Revive. The first meaningful choices are street access (750) or
upstairs access (1,000). Street access opens both pub exits and the alley escape
loop. Upstairs leads to a visible power switch in a room the player had to
reach. Power enables its stock dependent machines but does not buy doors for
free. A later crossing purchase (1,250) rewards expansion. Taraj is proposed as
a later Pack-a-Punch destination, with the bridge initially scenery.

Those three gate prices and four weapon sites are the existing v18 source
baseline. Additional perks, Taraj gameplay and the longer connector are
proposals. Use the detailed placement plan for IDs and state tables. We have
user confirmation for existing pub/stair doors and earlier solo rounds, not
complete weapon/power/navigation/co-op acceptance.

## Radiant, assets and scripts each have a job

Radiant edits the native `.map`: brushes, surfaces, entity volumes, prefab
references, lights and collision. APE defines custom images/materials/models
through asset data. GSC/CSC and the stock Zombies systems supply server/client
behavior, round flow, purchases, state and effects. The Launcher/build scripts
compile navigation and geometry, export lighting and link assets.

A Blender gun mesh is decoration; a stock wall-buy assembly contains the
markers and references that make a weapon purchase. A Blender Empty named
power is a plan; the stock power-switch assembly contains the working parts.
A volume called upstairs is not enough: it needs matching registration,
spawners and purchased adjacency. Keep this separation explicit at export.

## Prepare the source without losing work

1. Choose the actual reviewed saved source and record its hash, scene name,
   visible/archived collections and date. Current handover points to v30; its
   complete enclosure changes are newer than the legacy v18 gameplay anchors.
2. Preserve dirty live files and older checkpoints. Keep the earlier playable
   source/package available for comparison. Use a separate conversion output;
   do not scaffold over `zm_pharmacie` or edit stock `zm_giant`.
3. Record whether generation owns the whole map or selected prefab layers.
   Existing generators replace their generated source: manual Radiant changes
   must be captured in source data/a preserved patch before regeneration.
4. Compare architecture, collision and gameplay separately. Exclude reference
   planes, photo-only scenery, cameras, diagnostic hulls and archived objects
   from gameplay collision. Do not make every bottle/chair leg a solid brush.
5. Retain the current position transform exactly once. Legacy conversion is
   `(Blender metres + (-3.5,-10,0)) × 39.37007874015748`. World transforms already
   contain the gameplay enlargement. Do not enlarge everything a second time.
6. Recheck origins/volumes against the chosen source. In particular, old alley
   volumes may extend outside the new enclosed route. Keep supported floors,
   player volumes, zone ownership and actual playable collision consistent.

Do not assert full Blender parity: the existing conversion approximates curved
objects, skips some thin/concave pieces and does not transfer general procedural
materials or all per-face assignments. Account for each unsupported object in
the conversion report. Detailed prop model export is a separate route to prove.

## Use the editor deliberately

Bundled `Radiant_Launcher_QuickStart.pdf` pp.2–5 is the primary operational guide
already reviewed in the project. These are **GUIDE** steps until the current map
has actually been opened and the operations observed on this installation.

1. In the Launcher, highlight the intended map row, then select **Level Editor**.
   Merely checking its build checkbox is not selecting the row. Confirm the
   opened filename and visible pub geometry before editing. An empty
   `unnamed.map` is not the conversion; do not save it over project source.
2. Use top and side grid views together for placement, with the 3D camera for
   orientation, readable height and approach review. The QuickStart describes
   Ctrl+Tab to cycle orthographic views and F4 to move the camera to a selection.
   Confirm customized bindings rather than firing guessed shortcuts.
3. Make simple structural/collision brushes on the grid, using orthographic
   dimensions. Avoid slivers, coincident floors and unsupported bounds-box
   substitutions that close a passage. Inspect complex export substitutions.
4. For stock interactables, place a complete `misc_prefab` assembly from the
   installed core library. Inspect its `model`, `origin` and `angles`; inspect
   contents in context before changing pivot/face direction. Keep stock assets
   referenced, not copied into Git.
5. Inspect visible geometry **and** clip/use/zone volumes. A normal textured
   view can conceal a clip wall, misplaced trigger or missing player volume.
   Use Entity Info for actual KVPs and confirm exact property spelling.
6. Inspect from player height at the approach, use location and retreat path.
   An attractive overhead view cannot prove the gun faces the room or the use
   marker sits outside its backing wall.
7. Review lighting in the built-light preview (QuickStart identifies F8). This
   differs from exporting the LED and from the game's final appearance.

Official scale guidance already recorded in `BLENDER_RADIANT_WORKFLOW.md`:
one map unit is one inch; standing hull32×72; suggested single-door hole56×96;
stair width80; default rise/run8/12; short pinch64. These are **GUIDE** design
standards, not measured real venue sizes or runtime guarantees. Compare actual
gaps after frames, leafs and props, and test co-op passing/revives explicitly.

## Feature recipe: wall guns that behave like Zombies wall buys

**LOCAL:** use the `spawnable_weapon_*.map` assemblies listed in the stock audit,
not a static gun plus a generic paid trigger. W01 RK5, W02 KRM, W03 Kuda and W04
KN-44 are the baseline. Their configured price comes from the installed stock
weapon table loaded by the map script.

- Measure the wall plane after conversion; choose its playable side. Keep the
  assembly's chalk/model/use markers together when rotating or translating.
- Inspect each prefab's pivot. RK5 has its purchase marker56 units above its
  approximately floor-level origin; raising that origin to eye level would
  put the gun much too high. Do not generalize that pivot to every prefab.
- Place the visible weapon/chalk against the wall without sinking the model or
  its script-derived use bounds into masonry, trim or a photo panel. Support
  the player at the use face with flat reachable floor.
- Keep buying space outside the main escape path. Another player should pass
  while someone buys; preserve the rear approach and upstairs arrival.
- Review GSC/CSC/weapon-table references together. Do not add a server-only
  weapon identity that conflicts with clientfield/spawn-list setup.

**PENDING acceptance:** face the gun, see its real prompt, buy with sufficient
points, verify correct deduction/weapon, try insufficient points, buy ammo,
change held slots and later test upgraded ammo. Observe both clients in co-op.
Record wall ID, package identity and exact failure instead of saying guns work
because their prefab references exist.

## Feature recipe: paid route with shared unlock

**LOCAL:** current gates use stock debris-removal behavior. A `trigger_use`
targets the gate group, with `targetname=zombie_debris`, an integer
`zombie_cost` and the unlock `script_flag`. Visible pieces and removable clip
pieces are linked `script_brushmodel` entities sharing the group targetname.
The checked collision setup adds `script_noteworthy=clip`, `DYNAMICPATH=1`
and `spawnflags=1`. Exact existing groups/flags are in the stock audit.

1. Define the closed opening, every visible part, every clip part, approach-side
   use volume(s), price, flag and the two zones connected by that flag.
2. Keep the trigger volume and its origin accessible outside the solid blocker.
   This project already had missing prompts from buried use centres.
3. G01's front and rear blockers share one purchase group: both must clear.
   G02 blocks the lower stair approach. G03 expands the street. Preserve that
   grouping unless a new design explicitly changes the progression.
4. Match zone adjacency to the same flag used by the purchase. Path cuts must
   reconnect; removing a visible mesh alone does not reconnect zombie paths.
5. Preserve stock one-purchaser/shared-level-state behavior. Ordinary purchases
   deduct personal points, not a communal pool. Test near-simultaneous use.
6. For the first version, reliable removal is enough. Rotating/sliding doors
   need their own stock movement setup, destination/pivot and collision tests;
   do not mix a rotating tutorial into the debris recipe halfway through.

**PENDING acceptance:** blocked before purchase; correct prompt/price; insufficient
funds denied; exactly one successful charge; all linked visible/clip parts
clear; sibling prompts disappear; correct area becomes accessible; zombies
chase through in both directions; all clients agree. Test G01-first/G02-first
and buying G01 at the rear in a separate fresh run. Power must not bypass price.

## Feature recipe: zones, risers and repairable windows

**LOCAL:** start/street/upstairs/crossing each have `info_volume` pieces with
matching zone names, spawn groups and `script_noteworthy=player_volume`. The
map's stock zone-manager initialization and adjacency establish unlock logic.
Legacy v18 has11 risers, grouped3/3/2/3. Keep factory actor/player template
scaffolding; rise structs alone are not the complete game setup.

**GUIDE:** the saved [BO3 zone tutorial](../research/radiant/tutorial-library/vendor/ugx/zones.txt)
emphasizes player-volume coverage, and the
[spawn/barrier tutorial](../research/radiant/tutorial-library/vendor/ugx/zombie-spawners-risers-barriers.txt)
explains spawn-group and receiver associations. Compare the whole installed
setup rather than transplant its linked WaW recipe.

- Cover intended floors, stairs and landings with the correct player volumes;
  keep upper/lower floors separated and all pieces of one zone consistently
  targeted. Review transition seams, not just volume centres.
- Place each spawn on supported, navigable ground with emergence clearance
  and a reachable local player path. Prevent spawning in still-locked areas.
- Reserve local street approaches so the last zombie does not trek from distant
  scenery. Test split teammates and movement back toward earlier zones.
- A repairable window needs the complete stock receiver/boards/goal/traversal
  arrangement and matching entry/zone associations. The v30 boarded pocket is
  a future site, not a completed repair system. Do one complete window first.
- Do not fix pathfinding by adding guessed nodes or ignoring repeated
  `PATHFIND_FAILURE_UNREACHABLE`. Distinguish off-nav furniture goals, invalid
  emergence points, closed clips, zone mismatches and unsupported floor.

**PENDING acceptance:** entries activate at the right unlock/player state;
zombies reach local and cross-zone players; upper/lower stair chase works;
window boards tear/repair and traverse; no inaccessible final zombie prevents
round completion. Blender rays are preliminary clearance evidence only.

## Feature recipe: power in a room you have to reach

**PLAN/LOCAL baseline:** I03 is in the upstairs room reached through G02. Use
`power_switch.map` complete: its use trigger, handle, FX point and collision.
The stock script handles global `power_on` and dependent systems when no local
power-zone override is configured. An arbitrary custom flag named power does
not substitute for it.

Place the complete switch against a solid wall with the use face toward flat
floor. The stock audit identifies the prefab's local approach on negative Y;
check the actual rotated assembly. Keep the switch off treads and away from
stair arrival; make it recognizable with the switch silhouette and practical
electrical dressing. Preserve the room's approved layout.

First prove functional power. Power-dependent lighting is a separate visual
choice: the [Modme power guide](https://wiki.modme.co/wiki/black_ops_3/basics/Setting-up-a-proper-power-switch.html)
discusses multiple lighting states and a replacement prefab. We have not adopted
its archive or script. Configure light states only after comparing installed
stock and the intended mood; a readable route must remain navigable pre-power.

**PENDING acceptance:** switch unreachable until G02 bought; use from supported
floor; switch/FX/power state changes once; standard dependent machines update
on every client; unpaid doors stay closed. Test solo/co-op differences rather
than infer Quick Revive behavior from one solo screenshot.

## Feature recipe: perks, real box and Pack-a-Punch

For perks, use the audited stock `vending_*_struct.map` assembly. The model,
machine marker, attack spots and stock script registration supply behavior.
I01 Quick Revive is the early pub site; I04 Juggernog outside, I05 Speed Cola
upstairs and I06 crossing reward are proposed new placements. Confirm each
machine's whole footprint/interaction face, supported floor, pass-by clearance
and power behavior. Quick Revive stock price/behavior varies solo vs co-op.

**Important LOCAL correction:** the current outside
`buyable_magic_box_start.map` is static rubble/cinder blocks, with no functional
chest-use marker or zbarrier in the generated map. I02 is a site/base, not a
verified box. The saved
[box tutorial](../research/radiant/tutorial-library/vendor/ugx/mystery-box-locations.txt)
also warns about incomplete beta-era box prefabs.

For a real box, inspect the complete installed Giant starting site. Construct
the legitimate stock arrangement at I02 using the paired `treasure_chest_use`
struct and matching `<site>_zbarrier`, full animation/model settings and stock
script/assets. Do not bring the entire Giant multi-location prefab into our
map at its original coordinates or copy stock source into Git. Prove one
functional starting site before designing relocation/Fire Sale states.

For later I07 Taraj PaP, use audited
`vending_weapon_upgrade_spawnable.map` with stock scripts/power dependency.
Reserve machine collision, animation, stand/use/retrieval and teammate passing
space; its generated use radius40/height70 is not the full clearance footprint.
Initial proposal: reach Taraj via paid routes after power, with no bespoke quest
lock. Unknown prices/coordinates for the later routes remain unset.

**PENDING acceptance:** perks give the intended effect and charge correctly;
box spins, presents a reachable weapon and handles denial/occupancy; PaP
accepts/ejects/retrieves a weapon without wall clipping; timers, death/disconnect
and alternate ammo behave correctly. Test no-power and multiple-client use.

## Build and deploy once the conversion stage is requested

This packet does not run the following process. Use the existing authorized
project workflow when conversion resumes; choose intended source/output before
running a generator, and avoid staging over the live engine package blindly.

1. Validate exported object/collision/material counts, unsupported items,
   transformed IDs, prefab existence, unique GUIDs, group/flag links and volume
   coverage. Inspect the `.map` in Radiant as above.
2. Use official geometry/navigation compilation. Inspect outputs/logs,
   including actual ground navmesh; an omitted flying navvolume is a different
   issue from a ground zombie unable to chase.
3. Export fresh LED after geometry/light changes, wait for the actual lighting
   process/output and relink. Do not link stale lighting because the initial
   launcher invocation returned early.
4. Use `scripts/build-map.ps1` and its current documented asset-database handling.
   Historical `/update` failed duplicate registrations; the backed-up rebuild
   procedure resolved them. Do not reinstall tools or edit stock GDTs to guess
   around a map asset failure.
5. Check logs for printed failures and expected outputs as well as exit codes.
   Missing optional stock assets and critical missing map assets are different
   findings; record each unresolved warning and its observed consequence.
6. Deploy only with BO3 closed and within the existing scope, preserving backup
   and verifying every package file. Include the entire recursive `zone/snd`
   tree: earlier root-only copying caused a fatal sound-bank failure.
7. Sam retains movement/purchases/game controls. Agents inspect passive captures
   and logs. Record the exact package/build, player count and results.

## Conversion completion means observable gameplay

Test in small slices: supported start/rounds → one wall buy → one gate/zone →
linked loop → stairs/power/perk → complete box → crossing → co-op → Taraj/PaP.
Run both opening purchase orders. Review supported floors/bounds before
requiring combat in a new area. Tune placement/spawn timing from evidence.

Use the [manual-test record](../research/radiant/manual-test-record.csv) for
actual results, leaving `not_run` until observed. Keep one row per case/run;
copy rows for different builds/player counts. Attach evidence and record
remaining failures in MODLOG. Structural verification and gameplay acceptance
have separate statuses.

Before marking a slice complete, demonstrate: real interaction on supported
floor; correct personal charge/shared state; supported passage with pursuing
zombies; consistent multi-client behavior; round completion; no scenery escape.
For each unverified feature, keep the failure/test visible instead of widening
the map and hoping the next build resolves it.

## Known gaps to resolve at conversion

| Gap | Next concrete action |
|---|---|
| Legacy v18 anchors/volumes vs v30 architecture | Reconcile saved source and remeasure all reserved approaches/volume pieces |
| Outside box base only | Assemble/test the complete stock starting chest site |
| Junction ground/bounds incomplete | Continuous terrain/collision review before connector gameplay |
| Narrow stair and alley/bin section | Pursuit, opposing teammate and revive tests; simplify prop collision as justified |
| Upstairs/Taraj one main exit | Test risk/reward; discuss a new architectural exit before adding one |
| Crossing/bar package not documented deployed | Recheck actual package state before another deployment; preserve old evidence |
| General visual parity unproved | Report approximations/skips, inspect selected export views and actual runtime |
| Four-player startup/purchases/revives unproved | Separate private co-op acceptance after solo/core checks |
| Radiant current-map open/control details unproved | Observe correct file/selection and required operations before editor automation |

The purpose of the packet is a reviewable, evidence-backed conversion, not a
claim that reading tutorials has already demonstrated editor or game behavior.
