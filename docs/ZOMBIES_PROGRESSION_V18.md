# Proposed Zombies progression — plan before Radiant

Implementation update 2026-10-03: Sam authorized the separate `zm_pharmacie_playtest`.
Three zones, linked 750-point street exits, 1000-point stair access, four stock wall
buys and item placements are now authored and built. Sam confirms pub/stair doors
work. A new1250-point crossing-wall purchase extends street access to Post Office
and Natural Wellbeing with its own zone/risers; runtime test pending. Full route,
AI and co-op checks remain pending. See
[PLAYTEST_V18.md](PLAYTEST_V18.md); the proposal below remains design intent.

Sam's direction: start in the pub/bar, buy access outside and upstairs, and plan
the map's play before conversion. These are explicit **proposals**, not working
doors, zones or game scripts. Blender collection `GAMEPLAY v18 | Zombies
progression - planning only` holds named Empty markers. Exact coordinates/status
are in `recon/v18/zombies-progression.json`. Old competing planning collections
are archived/unlinked; no architectural doorway was closed or moved for this plan.

## Starting area and the first choices

Start in the main ground-floor pub room, rather than behind the counter. Four
provisional start anchors sit along the checked main aisle. Reserve a first wall
weapon and Quick Revive near the front; validate actual stock prefab footprints,
interaction ranges and orientation before fixing those locations.

| Marker | Proposed role | Placement / design constraint |
|---|---|---|
| D01 | Buy street access | Existing front doorway/threshold; offer purchase from supported floor, clear of swinging leaves |
| D02 | Buy upstairs access | Flat landing before the first lower stair tread; a new gate, not a trigger midway up the stairs |
| D03 | Connect rear exit to street/alley | Existing rear doorway; default proposal is linked to D01 so opening outside creates a loop |

D01 and D02 provide two early branches. Street access rewards space and the
alley loop; upstairs access rewards power and a later perk/weapon. Power upstairs
is a provisional gameplay choice, not a venue feature. Door prices are deliberately
unset until the round economy and starting weapons can be tested.

For D03, linking to the front-door purchase avoids a confusing route that looks
open but terminates at another unmarked lock. A separately priced rear door is
also possible, but that would need a clear explanation and a consistent zone
unlock whichever outside door is purchased first. Do not accidentally leave the
static rear leaf open when the street is supposed to be locked.

## Combat space and routing

- The decorated pub is a compact opening arena. Keep the measured central aisle
  and both bar approaches clear. Photo-reference furniture does not need to act
  as solid snagging collision in the eventual game; choose appropriate simplified
  collision while keeping its visible shape.
- The main rear/stair approach is around the **left** of the bar, through the rear
  left passage. The room to the right is a service/store area terminating before
  the stair mass, not a through-route to the stairs.
- Street -> outer-left alley -> rear landing -> rear pub door -> main pub creates
  the proposed escape/revive circuit once the street unlock is active. The rear
  doorway's approach must go around its open leaf; tested waypoints turn at
  Y=32.6m before entering the doorway centre near X=-3m.
- Initially bound street combat approximately between X=-18m and X=30m. The full
  photographed street remains scenery beyond that. Later crossing/junction
  expansions are possible; exposing the entire 100m strip immediately would add
  long, empty sightlines and make spawn distances harder to control.
- The 1.41m lower stairs are a deliberate choke. Preserve retreat space before
  D02 and around the turn/upper arrival. A purchase or perk should not require
  standing on a tread. Upstairs has one main escape path; test whether this is
  fair under pressure before adding encounters that trap the whole team there.
- Small toilets/service rooms do not automatically need their own buyable door
  or combat zone. Decide which are useful gameplay space and which remain
  decorative/utility areas. Do not create lots of costly dead ends without rewards.

## Zombie and item planning

Eight zombie-entry candidate markers reserve perimeter approaches in the pub,
street and upstairs. They are not risers or functioning windows. For each, select
an actual barrier/window or riser treatment, check local furniture, ensure a path
to players, and test stock spawning/visibility rules. Do not put a spawn in the
centre of a revive space simply because there is empty floor there.

Upper entries must remain inactive until upstairs is unlocked. Street entries
must remain inactive until outside is unlocked. Door state, active-zone state and
the AI route through each opening must change together. Closed routes must not
leave Zombies trying to chase a player through unavailable geometry.

The mystery-box marker reserves a street-side pavement location away from the
alley entrance. Check its real footprint and player interaction space in Radiant.
Power, box, perks and wall weapons need deliberate floor/wall support and angles;
the earlier arbitrary hard-coded generator positions should not be reused.

## Radiant implementation and actual verification

Convert the named proposals into proper game-native door geometry/entities,
purchase interactions, zone volumes, spawns and script state using the installed
BO3 Zombies template. Blender Empties will not automatically implement any of
this. Preserve the original pub architecture and create intentional open/closed
door states; account for collision, AI navigation and both-side purchases.

Test in sequence: starting-area survival; each branch bought independently;
front/rear linked-door behaviour; upstairs spawning and stair chase; complete
street/alley loop; power and purchases; then two-player revives and co-op movement.
The Blender recon's clearance rays are preliminary evidence only, not a substitute
for these tests or for checking actual player and prefab bounds in the game.
