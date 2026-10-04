# Radiant gameplay placement and conversion specification

Planning only, 4 October 2026. Companion to [Zombies design](ZOMBIES_DESIGN_V29.md).
[Machine-readable registry](radiant-gameplay-plan.json) supplies stable IDs and
exact existing v18 anchors/bounds. It is documentation, not executable generator
input. No new Blender/Radiant geometry, script, package or game input is made.

## Baseline, coordinates and limits

Source: `scripts/generate_playtest_v18.py`, inherited conversion transform from
`scripts/generate_blender_test_map.py`, v18 progression markers and current
[reviewed v30 modelling notes](REAR_ALLEY_V30.md). V18 gameplay and later Blender appearance are
different sources; do not copy the old coordinates blindly into a new scene.

Registry coordinates are **Blender metres**, before translation. Existing engine
conversion is `(coordinate_m + (-3.5,-10,0)) * (100/2.54)` per axis. Bounds order
is xmin,xmax,ymin,ymax,zmin,zmax. Prefab angles are pitch,yaw,roll in degrees.
All given origins are existing authored values, not measured real-world locations
or guaranteed final mounting positions. Stock prefab origins may be floor pivots.
Future connector/Taraj/perk positions deliberately have no invented coordinates.

Latest documented engine baseline: doors and sharp windows user-confirmed;
crossing/bar package compiled but deployment pending. Full AI/co-op remains
unverified. Latest documented/reviewed Blender baseline is
`assets/blender/pharmacie-zombies-alley-v30.blend`: enclosed rear circulation,
parked rear-door leaf, sealed bar-side service door, reviewed gallery and saved-file
validation. Remeasure legacy gameplay anchors/volumes against v30 before conversion;
Blender validation does not establish engine collision/navigation. Use a backed-up
copy and preserve pub/Taraj geometry; this plan does not authorize deployment.

## Stable zone and gate IDs

| ID | Engine name / role | Unlock | Conversion handoff |
|---|---|---|---|
| Z01 | `start_zone`, pub/start/rear stair approach | Initial | Four supported starts, accessible first weapons/Quick Revive |
| Z02 | `street_zone`, near street and outer-left rear loop | G01 | Keep all front/alley/rear connections coherent; volume must follow reviewed ground |
| Z03 | `upstairs_zone` | G02 | Stair transition/landing ownership must not leave an ungated upper spawn |
| Z04 | `crossing_zone`, street extension and short lane | G03 | Lane dead end clearly bounded; do not imply a second escape loop |
| Z05 | Proposed bounded junction/Melton connector | G04, proposal | Extent/ground/route review before choosing coordinates or price |
| Z06 | Proposed Taraj combat/reward room | G05, proposal | Existing front arrival and both dining aisles; rear service door stays scenery |

| Gate | Price | Collision and visible removal group | Purchase approaches / cues |
|---|---|---|---|
| G01 street | 750 | `pt18_street_gate`, both front and rear blockers | Two existing pub-side use volumes; mark both exits as the same street access purchase |
| G02 upstairs | 1,000 | `pt18_stairs_gate`, stair-foot gate | Flat lower approach, not a tread; readable upstairs/power cue beyond gate |
| G03 crossing | 1,250 | `pt18_crossing_gate`, street wall at X30 | Existing triggers on both wall sides; signpost expanded street/reward |
| G04 connector | Unset | New future group, no entities yet | Clear street-end boundary; route review required |
| G05 Taraj | Unset | New future group, no entities yet | Existing front arrival, supported purchase landing clear of booth aisle |

G01 existing use volumes are pub-side only. Do not describe them as proven
two-sided purchases. G03 is authored with both-side triggers but its far side is
normally inaccessible until it opens. A second-side check needs an intentionally
reachable route/test context; it is not permission to drive the game or invent
an extra connection. Future two-sided requirements should be explicit.

Doors use one shared state per gate. G01 removes every linked front/rear visible
piece and collision piece in one purchase. Matching group membership is required;
removing only artwork leaves invisible collision, and removing only collision
leaves misleading visible gates. Stock audit reports debris deducts points from
the individual purchaser and changes shared level flags; team-consistent access
does **not** mean pooled player money. Simultaneous purchases must not double
charge. Preserve stock handling before introducing bespoke scripting.

## Closed/open state graph and power

Initial state: G01/G02/G03 closed; Z01 active; power off. Two independent branches:

| State / action | Accessible zones | Expected behavior |
|---|---|---|
| Buy G02 first | Z01 + Z03 | Upstairs can be reached; power is available; street remains blocked/inactive |
| Activate power upstairs | Same accessible zones | Shared power state changes; power must not open unpaid route gates |
| Buy G01 first | Z01 + Z02 | Both exits unlock and rear loop opens; upstairs/power remain inaccessible |
| Buy G01 and G02 in either order | Z01 + Z02 + Z03 | Same final geometry/zone state regardless of order |
| Buy G03 after reaching street | Add Z04 | Crossing risers/routes activate; upstairs still depends independently on G02 |
| Later G04 then G05 | Add Z05 then Z06 | Separate future route/reward states, requiring actual supported connections |

Flags are `pt18_street_open`, `pt18_stairs_open`, `pt18_crossing_open`; adjacency
is Z01↔Z02, Z01↔Z03, Z02↔Z04 under those flags in the existing source. Whether
adjacency registration alone behaves as intended is a runtime test, not a design
assumption. Door removal, active zones and navigation reconnection must agree.
Each player, including late/spawned/revived players, sees the same gate and power
state. Players in different rooms must not reactivate a closed-area spawner.

Power I03 is reached in the upstairs room: `(7.6,6,4.82)m`, legacy angles
`0 270 0`. This satisfies the requested reached-room progression without moving
the architecture. Confirm the complete stock switch footprint and usable face
on supported upper floor, with wall support and no overlap with furniture.
Provide an obvious switch silhouette/cable/light cue; optional power-dependent
machines can have readable inactive states. Do not create a new power quest for
the first survival version. The full stock switch links handle and use/FX parts;
reuse the complete prefab rather than a decorative handle and custom trigger.

## Conventional wall guns and stock interactables

| ID | Stock weapon / baseline price | Existing origin m | Legacy angles | Mount / approach intent |
|---|---|---|---|---|
| W01 | RK5 (`pistol_burst`), 500 | -1.84,3.5,0.02 | 0,92.87,0 | Left pub wall; face use area into supported main-room side |
| W02 | KRM (`shotgun_pump`), 750 | -4.53,26,0.02 | 0,98.22,0 | Left rear approach wall; keep escape path clear |
| W03 | Kuda (`smg_standard`), 1,250 | -15,-0.08,0.02 | 0,0,0 | Outside supported pavement wall; no overlap with alley arrival |
| W04 | KN-44 (`ar_standard`), 1,400 | -2.71,14,4.82 | 0,97.22,0 | Upstairs left wall; clear standing approach, not landing bottleneck |
| I01 | Quick Revive | 0.2,2.7,0.02 | 0,90,0 | Pub start; teammate can pass while another buys |
| I02 | Intended box site; authored static base only | -16,-1.3,0.02 | 0,0,0 | Outside; functional assembly still required |
| I03 | Power switch | 7.6,6,4.82 | 0,270,0 | Reached upstairs room, clear wall and floor |

Use stock `spawnable_weapon_*.map` prefabs (exact paths in JSON), including chalk,
model and purchase marker. These are conventional wall weapons, not loot props.
Audit evidence: RK5 chalk lies at local y=0, z50.5..62.5 engine units, with
weapon use struct at z56 (~1.422m above prefab floor pivot). An origin near floor
level therefore does not mean the gun should be mounted at ankle height. Rotate
the complete assembly around its stock pivot; do not move only the gun model.
Other weapon pivots still need individual comparison before treating this as a
universal mounting recipe.

Mounting procedure: identify the actual current wall plane; inspect stock local
chalk/model face and complete bounds; rotate that face toward the room/pavement
approach; place the assembly against the wall without burying it; verify use
marker and visible weapon sit at a readable height; keep standing floor beneath
the approach and line of sight unblocked. The legacy angles above are preserved
source data, not guaranteed face normals after scene revisions. Wall photo panels
must not accidentally obstruct use traces. Test chalk, buying a first weapon,
ammo purchase and swapping a held gun using the stock prefab's real prompts.

Stock weapon script derives use bounds from the model and requires look-at by
default; do not bolt an unrelated price trigger onto each gun. For the stock
power prefab, audit finds its local use box on the negative-Y side before rotation;
inspect that entire approach after applying the legacy yaw. Box has lid/reward
motion and stock 950 baseline spin when assembled; reserve its working footprint rather than
only its closed model bounds. Quick Revive solo and co-op behavior/prices differ;
retain and test the actual stock configuration before documenting final values.
The installed scripts also have solo-specific Quick Revive/power handling; do
not assume identical pre-power availability in solo and co-op.

**Box correction from installed-stock audit:** `buyable_magic_box_start.map`
contains static clip/rubble/cinderblocks, not a functional box. The generated
v18 map lacks `treasure_chest_use` and the corresponding site zbarrier. I02 is
therefore an authored location/base only. Before conversion, inspect the complete
stock `zm_giant/script/zm_giant_magicboxes.map` and implement the actual linked
use struct/zbarrier plus required scripts/assets. A box site's use marker and
matching `<site>_zbarrier` relationship must be checked against installed scripts;
do not claim box spins have worked. Keep 950 as stock baseline for a future
functional assembly, not a charge already present at the decorative base.

New reward IDs: I04 Juggernog in a supported Z02 pavement bay; I05 Speed Cola
upstairs clear of arrival; I06 Double Tap/alternative in Z04 open street, not
the dead-end lane; I07 Pack-a-Punch at a reviewed Taraj arrival/bar-adjacent bay.
These remain proposed, with no fabricated coordinates or asserted prefab setup.
For I07, power plus paid route access is the initial proposal; no additional
quest lock. Audit reports PaP use radius40/height70 engine units, but this is
interaction data, not a sufficient model/player clearance allowance.

## Spawn plan and navigation handoff

P01–P04: existing start origins X5.5, Y3.2/4.4/5.6/8.4, Z0.12m. Confirm supported
spawn landing and inherited template angles facing useful combat space; do not
infer facing from position. Keep starts outside furniture and immediate risers.

Existing risers have IDs Z01_R01–R03 (pub), Z02_R01–R03 (street), Z03_R01–R02
(upstairs), Z04_R01–R03 (crossing): eleven total. Exact anchors and legacy yaw90
are in JSON. They are authored stock riser candidates, not confirmed safe spawn
positions. Z01_R01 `(3.45,5.6,0.03)` is near the opening-player area: specifically
review first-round visibility/fairness rather than assuming the existing anchor
is ideal. Decorative floors/platforms require correct engine navigation support.

Review each riser: supported floor, actual emerge clearance, path to every
reachable local goal, no emergence directly inside props or revive standing
space, and inactivity before its gate. Long roads need local active approaches
to avoid delayed round ends. Do not immediately activate the full Melton strip.
The v30 rear pocket Z02_R04 `(-7.65,34.2,0)` is a future barrier candidate, not a
twelfth implemented riser. Check the barrier opening, zombie traversal and
repair semantics before choosing its final treatment.

Keep collision simple for chairs, glass, table legs and decorative displays,
but solid where combat cover/route blocking is intentional. Preserve visible
props; simplify engine collision without altering approved Blender placement.
The raised-platform clip ramp is an existing attempted fix, not verified AI
success. Stairs, front/rear thresholds, alley turns and kerb transitions need
actual navigation and player checks. Repairable window entries require stock
barrier connectivity, not just a boarded Blender opening.

## Economy and staged conversion

Essential first slice: stock rounds, four starts, G01/G02, Z01–Z03, supported
spawns/routes, existing four wall guns, Quick Revive/power and a complete functional
box replacing the current static base. G03/Z04 is the
already-built first expansion to verify. Later: extra perks, Taraj/PaP, moving
box, quest, bridge combat, Noseley. Cosmetic street completion can continue
without promoting all scenery into playable ground.

Keep baseline prices: G01 750, G02 1,000, G03 1,250 and existing wall guns.
Opening all three costs 3,000 **paid by whichever players buy them**, before
weapons/perks/box. Track each player's earned/spent points and round at first
street/upstairs/power/crossing access. Do not promise a fixed unlock round or
invent an economy target without observed play. Compare upstairs-first vs
street-first, solo vs shared purchases, and recovery after a death/down.

1. **Source reconciliation:** use the reviewed v30 Blender checkpoint; compare
   registry anchors against it. Preserve dirty files/older checkpoints. Resolve
   source/export parity, continuous terrain, closed service openings and visible
   bounds before conversion. Review current photo/material/export limitations.
2. **Gameplay layout review:** inspect all stable IDs in Radiant, complete prefab
   footprints, zone volumes at stairs/doorways, gate groups and use approaches.
   Avoid overlapping unrelated volumes/triggers. Include ground beyond sample
   points; checks of a centreline do not prove a continuous navigable surface.
3. **Small core conversion:** retain stock round/purchase scripts; explicitly map
   IDs to entities/flags; do not export Blender Empties as presumed functionality.
   Reuse actual stock prefabs, collision/nav cuts, and correct zone initialization.
4. **Source validation before build:** compare transformed anchors, target/flag
   links, gate-part membership, zone/spawner names and closed/open states. Keep
   original photos/game stock assets untouched; no no-spawn callback or inherited
   invulnerability from the architecture scale-test project.
5. **Official compile/navmesh/light/link:** under the agreed conversion scope,
   use the project workflow and record exact result. Check printed failures,
   lighting completion, navigation output and asset resolution, not exit0 alone.
6. **Controlled runtime review:** when authorized/ready, record package identity
   and hash-verified deployment; Sam moves/plays, agents observe passively. Test
   the small core before crossing and Taraj. Do not overwrite a running session.
7. **Tune then extend:** record regressions and adjust justified collisions,
   placements/spawn states/prices before adding rewards or extra combat zones.

## Acceptance checklist for Sam's manual tests

For every case record package/build, player count, buyer's points before/after,
gates/power state, route/direction, evidence and pass/fail.

- **Cold start:** each of four starts safe; correct facing; no immediate trapped
  teammate; stock round starts and finishes; locked zones do not spawn zombies.
- **Independent purchases:** G02-first and G01-first runs, then opposite order;
  same final shared gate states, correct single-payer deduction, no unintended
  power requirement on opening gates or power-caused free gate opening.
- **Linked exits:** G01 bought at front and separately at rear in a fresh run;
  both exits clear every visible/collision part; whole alley circuit passes in
  both directions with pursuing zombies and opposing teammates.
- **Team consistency:** two players try the same gate almost together; one
  successful charge/open state, sibling prompt disappears; all clients see same
  route. Split across pub/street/upstairs, then down/revive/rejoin as supported
  by the private test; no reopened lock or inactive-zone goal.
- **Power/items:** switch reachable after G02, visible/use face correct; shared
  power state; each gun's purchase/ammo/look-at works without climbing; box reward
  and lid clear; Quick Revive behavior appropriate in solo vs co-op.
- **Navigation:** upper zombie follows down stairs; ground zombie pursues upper
  player after gate opens; thresholds/platform/alley turns and furniture permit
  chase and teammate revives; persistent path failures explicitly logged.
- **Crossing:** G03 price/removal/zone activation correct, local risers reach
  players, lane retreat remains possible, outer ground/bounds prevent falling out.
- **Round completion/balance:** no unreachable last zombie after teammates split;
  record travel delays, early unlock choices and weapon recovery after down.
- **Later Taraj:** gate/power/PaP use and return escape clear, both booth aisles
  navigate; do not open a rear service exit or water route without design approval.

Passage/landing reservations and approvals for architectural gameplay changes
are in the [design handoff](ZOMBIES_DESIGN_V29.md). Online tutorials and the
installed-stock audit are separate evidence libraries maintained alongside this
plan; tutorial recipes must be checked against the installed build and runtime.
See [conversion playbook](RADIANT_CONVERSION_PLAYBOOK.md),
[research/library index](../research/radiant/README.md) and
[installed-stock audit](RADIANT_STOCK_GAMEPLAY_AUDIT.md) for those companion records.
