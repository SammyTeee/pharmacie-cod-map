# Resumed street references and DR Electrical boundary — v52

Checkpoint: `assets/blender/pharmacie-station-frontage-v52.blend`.
Sam requested more street/Melton work and reuse of A-to-B Street View collection.
The current in-app browser now works; the prior empty-browser blocker is stale.

## Observed source

Google Maps Street View, inspected 11 October 2026: visible label **2012 Melton
Rd**, imagery **Sept 2023**. Resolved camera 52.6940665, -1.0815764; panorama
`dVYPkj-O2QW9N0UbzcxnJQ`; heading 40, pitch 0, field of view 90.
Viewer request: https://www.google.com/maps/@?api=1&map_action=pano&pano=dVYPkj-O2QW9N0UbzcxnJQ&heading=40&pitch=0&fov=90

Observed: low red/brown brick wall with coping; taller brick piers; vivid blue
pointed palisade fence and horizontal rails; blue appliance-category boards;
small DR Electrical sign; industrial brick/clad buildings behind; paved footway
and roadside double yellow markings. No screenshot file was saved in this pass;
the visible view was inspected through the supported browser tool. No image
pixels are embedded in the new Blender geometry.

## Modelled scope

Added the wall, individual brick faces/coping, piers, blue steel pales/rails and
five text labels in a movable assembly. 1,792 new closed meshes and five text
objects. Boundary is an estimated 34.2 model units long, from `(19,863)` to
`(52,872)`. Exact dimensions, pier/pale counts, geographic fit and lettering
spacing are estimates. Final assembly is offset 2.5 units outward from that
baseline to clear the retained coarse warehouse mass; route checks pass after
the offset. This is the first frontage detail, not completion of the
industrial premises, roofs, access gates or neighbouring station streetscape.
Existing background blockout masses still require reference-led correction.
The nearby OSM building tag says Buildbase; do not silently reinterpret that
as independently verified DR Electrical footprint or current business identity.

The v51 porch/house, perpendicular garage, opposite houses and all prior map
objects are retained. New assembly:
`DETAIL v52 | Station approach blue appliance frontage`.

## Checks and review

`recon/v52/validation.json`: all 19,359 active v51 scene object fingerprints
unchanged; no nonmanifold/nonpositive new meshes. Fingerprints cover world
transform, parent name, geometry/topology, font content and material slot names;
not shader graphs or engine behavior. Superseded archives remain in the file.

`recon/v52/route-checks.json`: 32,535 selected clearance rays and 3,615 support
samples, zero blocked or unsupported, including house/station ramp/parking/end
routes. Two inherited limited enclosure-side misses remain recorded. These are
Blender ray samples, not continuous capsule or BO3 navigation tests.

Four matched Workbench previews in `recon/v52`: `frontage_before/after.png` and
`context_before/after.png`. Scripts: `station_frontage_v52.py`,
`check_station_v52.py`, `review_station_v52.py`. BO3 unchanged. Full extension
alignment/completion and authorized final commit/push remain pending.

## A-to-B tooling

New self-contained planner: `recon/route-planner/index.html`.
Instructions and exact verification limits:
`research/streetview-pipeline/ROUTE_PLANNER.md`.
Existing Firefox walker remains available and now accepts separate output
folders with cross-route resume rejection. No new unattended bulk capture run
has been performed; current browser adapter remains the next implementation step.
