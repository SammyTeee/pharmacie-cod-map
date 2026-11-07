# Separate mutated boss Dave — 25 October 2026

Sam approved the ordinary Dave in game and explicitly keeps that replacement.
He requested a mutated, recognisable Dave boss roughly three times human height.
The accepted normal Dave66 map and all v1/v2 normal character assets are preserved.

## Design

Built-in imagegen used the approved ordinary Dave concept and unchanged original
photo 2 as identity references. The separate design retains his broad face,
rectangular glasses, grey hair/goatee, belly, tattoos and dark collared shirt.
The right arm and shoulder are enlarged with organic stony plates and subtle
purple accents. The face remains intact and recognisable. No blood or wounds.
Saved concept and exact successful prompt: assets/generated/dave-boss-v1/.

Intended height: 5.25 m, three times the ordinary studio reference of 1.75 m.
This is an authored game scale, not Dave's measured height. A boss at this size
requires an outdoor encounter and cannot follow ordinary pub door routes.
Final bind-mesh bounds are approximately 1.88 m for the normal model and 5.84 m
for the mutated model at entity scale 3. Animation poses change those bounds.

## Separate native trial: zm_pharmacie_dave67

The generated body/rig is complete. Raw generated hair/beard geometry failed
visual review, so the native candidate uses the exact approved Dave head plus
its matching upper neck, with the new head regions removed by skin weights.
The old horizontal head-cut trial visibly cut the armoured shoulders; that
trial was discarded. The final body keeps those shoulders and all normal Dave
source assets remain unchanged. Collar/skin seams remain prototype quality.

The prepared model has 78 stock-compatible bones and 46,188 render triangles.
All 78 match inspected stock idle, walk and attack source frames, with finite
mesh bounds. Native version-7 token and bind-hierarchy/position checks pass.
Source generation and rigging cost $0.35 + $0.20 listed, with provenance/jobs
under assets/generated/dave-boss-v1. Stock-derived private intermediates remain
under ignored build/dave-boss, not in distributable source.

The bundled SetScale API explicitly supports script movers. This boss is an
animated damageable script_model at scale 3, with its own animtree using installed
idle/attack clips. It is a **stationary street sentinel**, not a giant actor
attempting to navigate pub doors. It spawns at authored street position X43/Y-7
after both pt18_street_open and pt18_crossing_open have been purchased.
Vertical placement compensates for the inspected idle foot bounds.

- 12,000 HP per connected player at activation; player bullets/grenades feed
  its damage handler. Health is reported at approximately 10% intervals.
- Players within 310 engine units trigger a two-second attack warning. The
  delayed slam does 65 damage within 235 units, with a cover trace outside its
  own body/collider. Downed players are excluded. Recovery is 4.1 seconds.
- Native collision uses a separate authored 96-triangle bone-weighted hitbox
  source instead of the render mesh. A coarse solid body prevents walking
  through the sentinel; it becomes solid only at activation and is removed
  on defeat. Precise visual/hitbox fit still requires a human trial.
- Defeat awards 2,000 points to each player and clears the model after a pause.
  A bespoke death animation, moving pursuit and advanced attacks are not implemented.
- Normal Dave round spawning, core geometry, prices and story script remain.

## Natural exterior enclosure

Sam requested fixing the floating-looking outside and placing the boss down
the street after opening doors. assets/layout/dave-street67.json defines 311
closed scenery additions: deep brick end buildings with windows/delivery gates,
rear wings, coping/pier boundary walls, and continuous outer ground backing.
These are authored game closures, not claims about real Syston buildings.

Five additive rigid XModels contain 3,732 new visual triangles. 59 independent
collision solids back the enclosure. All elevated new scenery collision stays
outside the retained playable core; the apron sits under the original floors.
All 187 original map entities and the original world geometry prefix compare
unchanged against the accepted Dave66 source. Existing 35,238 ground, 11,813
visible-floor and 1,592 route checks are inherited through that preservation;
these remain source checks, not a new runtime traversal claim.

Matched before/after street, plan/aerial and actual boss mesh previews are in
recon/dave-street67 and recon/dave-boss-bo3. Studio/Blender previews are not BO3
captures and do not establish native shader parity or combat behavior.

## Build evidence and manual acceptance

First native trial failed script declaration order (#using after animtree).
Second compiled scripts but rejected dense render-mesh bullet collision
(exit 1000). The final low-poly hitbox build exits 0, with fresh geometry,
navigation, lighting and both localized packages confirmed. Failed packages
were never accepted or deployed. Exact receipts/logs:
build/dave-street67/source-checks.json, map-build-r3.log,
native-build-result.json and build-acceptance.json (seven package hashes).

Launcher: PLAY-BOSS-DAVE-ZOMBIES.cmd. Manual map: zm_pharmacie_dave67.
The original PLAY-DAVE-ZOMBIES.cmd still opens zm_pharmacie_dave66.
No game controls were sent. Seven files were deployed and independently
hash-verified, without launching the game. Backup:
build/before-blender-test-20261025-133251; receipt:
build/dave-street67/deployment.json. Actual runtime results must be
recorded separately. Pending: native appearance/scale/grounding, both purchases,
bullet/grenade damage, slam timing/cover/range, defeat/reward, ordinary rounds,
co-op and performance. A successful build does not certify those cases.

## Sources

- TRELLIS pricing checked: https://fal.ai/models/fal-ai/trellis-2 — $0.35 at 1536.
- Rigging pricing checked: https://fal.ai/models/fal-ai/meshy/rigging — $0.20.
- Ordinary character evidence: [DAVE_BO3_ZOMBIES.md](DAVE_BO3_ZOMBIES.md).
