# Player recon and cleanup v18 — 2026-10-03

Current map: [pharmacie-player-cleanup-v18.blend](../../assets/blender/pharmacie-player-cleanup-v18.blend).
Open in Blender with `scripts/open-blender.ps1`; scene 03 opens at the player-height
entrance camera. The user's unsaved live v17 was copied locally to
`input-live-v17.blend` before editing. That safety snapshot is deliberately ignored
by Git; saved v17 and the final v18 remain tracked milestones.

[Offline gallery](index.html) · [All screenshots](SCREENSHOTS.md) ·
[Machine-readable changes](changes.json) · [Validation](validation.json)

## Coverage and method

36 views before and 36 after cover entrance/threshold, main room, displays,
platform, tables, bar and both approaches, service/rear areas, all stair sections,
upstairs rooms/hall, outer alley and rear connection, opposite row, crossing,
Natural Wellbeing lane, junction and street extension. Six contact sheets and
selected full-resolution problem views were reviewed. Each screenshot is a
1100x700 Cycles render with a 22mm camera and an eye 1.65m above the floor.
Temporary neutral room fills/daylight aid inspection and are never saved into
the `.blend`. The four new stair lights are persistent map lighting proposals.

`recon_blender_players.py` also samples ten proposed routes approximately every
0.20m. It casts floor-support rays, eight radial rays at three body heights with
0.35m radius, and an overhead ray. Final report: **572 route samples, no detected
blockers or missing support; all36 final inspection cameras supported/clear**.
The main aisle changed from chair contacts to zero contacts under those checks.

A second pass used a **0.42m radius / 0.84m diameter**, slightly larger than the
existing 0.82m-wide planning guide. It caught two stair-arrival samples against
the WC outer wall. Tapered that wall's rear end20cm without opening the partition;
all572 samples now pass at both radii. Before-fix sensitivity evidence is retained
in `sensitivity-radius-042-before-arrival-fix/`, final evidence in
`sensitivity-radius-042/`. Neither envelope is claimed as a verified game capsule.

These are **preliminary Blender mesh checks**, not capsule sweeps, game collision,
navmesh or four-player playtesting. Rays can miss thin/interior intersections;
scenery visibility flags can differ from eventual collision. The player dimensions
are inspection assumptions and need calibration against the real BO3 player.
Only the chosen routes were checked; this is not a claim that every possible path
or every room is safe or finished.

## Confirmed fixes

| ID | Evidence / problem | Applied change | Review image |
|---|---|---|---|
| R01 | Two dining chairs projected into the central aisle near Y6.7/Y10.2 | Rotated each aisle-side chair to its table end, including back/seat/all legs | [Main aisle](after/04_main_room_to_bar.png) |
| R02 | Right-wall advert text and camera imagery appeared reversed; UV covariance confirmed direction | Corrected15 photo quads, including upstairs posters; retained already-correct instrument face | [Display wall](after/06_right_platform.png) |
| R03 | Rear connector overlapped old landing and alley floor at the same height; black/flickering patches | Raised connector top8mm; original floor/landing retained | [Rear join](after/22_alley_rear.png) |
| R04 | Gameplay enlargement made each stair rise roughly267mm | Replaced18 treads with26 in same run/turn footprint; lower rises190mm, upper178mm; new nosings; rails/landings retained | [Stairs](after/12_stairs_start.png) |
| R05 | Raised seating edge was a single270mm climb | Added135mm intermediate front step outside the centre aisle | [Platform entry](after/35_stage_step.png) |
| R06 | Upstairs showed open sky/missing roof above rooms | Added removable upper ceiling/provisional roof cap following an angled outer perimeter | [Upper seating](after/17_upstairs_seating.png) |
| R07 | Closing that roof made stairs difficult to read | Added four warm light fixtures at lower run/turn/upper approach, with Blender area lights | [Stair turn](after/14_stairs_turn.png) |
| R08 | Larger84cm inspection envelope contacted WC outer-wall corner at upper stair arrival | Tapered rear wall end20cm left, retaining front junction and closed WC partition | [Upper arrival](after/16_upper_arrival.png) |

The staircase/step changes are gameplay adaptations, not surveyed venue facts.
The ceiling/cap is a finish proxy; its exact profile and rear roof design are
unverified. All60 new solid meshes passed closed-edge/outward-winding checks;
four fixture meshes initially had inward winding and were corrected before save.
All44 source photo hashes are unchanged. Validation also compares every untouched
pre-existing mesh's world vertices/faces with the live input snapshot.

## Rejected false positives and route corrections

- Original views18/19 stood inside a kitchen fitting or toilet partition. Original
  views10/11/16 faced nearby solid surfaces. Corrected the inspection cameras;
  did not delete or move those walls. Moving chairs also required shifting view05.
  Before/after pairs for05,10,11,16,18,19 are therefore not identical-pixel comparisons.
- The first lane-floor detector failed to recognise the named side-lane slab.
  Corrected the floor classifier; the actual Natural Wellbeing lane floor existed.
- A straight waypoint line through the service store intersected walls/solid stair
  undersides. That room is not the rear through-route. The rear approach goes
  around the **left** of the bar, outside the fridge/display, then along the left rear.
- A rear-return waypoint crossed the rear wall pier. The doorway itself is open:
  approach X=-3m via Y32.6m to clear its outward leaf, then enter through its centre.

## Zombies planning added with Sam's direction

[ZOMBIES_PROGRESSION_V18.md](../../docs/ZOMBIES_PROGRESSION_V18.md) proposes starting
in the main pub, buying street access at the front door or upstairs access at the
stair foot, and linking the rear exit with the street/alley loop. Three proposed
zones and21 named Empty markers reserve doors, starts, items, spawn candidates and
initial street limits. Old competing planning collections are archived/unlinked.
Prices and actual prefab footprints remain unset/unverified. **No working game
doors, zones, spawns, perks, power or scripts were implemented.**

## Remaining Blender work before conversion

1. Clean or replace photo occlusions, baked people/cars, Street View marker and
   misleading reflected shop imagery. Individual shop images are now isolated,
   but still contain photographic content that isn't geometry.
2. Refine geometry-only Papermoon/Pasha/distant shop placeholders, roof/chimney
   proportions and the rear roof cap against the reference notes. Current street
   widths/heights/straight road are gameplay estimates, not near-1:1 survey data.
3. Make intended open/closed states for progression doors and design physical
   street limits; current markers do not block anything. Review all small rooms
   for usefulness and rewards rather than adding arbitrary buyable dead ends.
4. Review every furniture group/door approach using eventual prefab/player sizes.
   The clearance pass covers chosen routes, not the whole map. Small cosmetic
   parts may need simplified collision for Zombies pathing.
5. Decide export treatment for procedural floor/brick materials, lights, text and
   complex props. Existing exporter simplification/UV issues remain unresolved.
   Renderer lighting and shader appearance are not an engine-ready promise.

No Radiant conversion, compiler, deployment or game installation writes occurred
in this pass. Do not describe the Blender model as fully finished or runtime-tested.

## Re-run

On the saved v17/live safety copy, run `fix_player_recon_v18.py`, then on v18 run
`light_recon_stairs_v18.py` and `plan_zombies_blender_v18.py` once. Their guards
prevent overwriting/reapplying completed stages. `ease_upper_arrival_v18.py`
applies the subsequent wider-envelope corner correction once. For inspection:

```powershell
$env:PHARMACIE_RECON_PHASE='after'
& '<Blender executable>' --background assets/blender/pharmacie-player-cleanup-v18.blend --python scripts/recon_blender_players.py
python scripts/recon_contact_sheets.py
python scripts/recon_gallery.py
```

Use `PHARMACIE_RECON_PROBES_ONLY=1` for measurements only;
`PHARMACIE_RECON_VIEWS` can contain comma-separated view IDs for targeted renders.
`check_player_recon_v18.py` compares the local live safety snapshot and final v18;
on another machine retain an equivalent baseline snapshot before applying fixes.
