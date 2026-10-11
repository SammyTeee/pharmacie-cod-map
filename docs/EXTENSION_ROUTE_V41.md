# Melton / station / Holmdale route blockout — v41 (in progress)

Editable working checkpoint: `assets/blender/pharmacie-extension-route-v41.blend`.
Source v40 remains retained. The full requested extension is unfinished: number
29 has not been visually identified or modelled, and route architecture is at
blockout level. Keep the persistent extension goal active.

## Implemented

Joined Melton carriageway and footways continue from the retained v22 endpoint
to the station/Midland area. Holmdale branches from its mapped junction. Added
terrain backing, wide inferred gameplay boundaries, nine OSM building footprint
masses, the mapped station platform and an inferred final station walkway.
Widths, building heights, road markings, boundary walls and final walkway are
gameplay estimates, not observed Street View details. A continuous inferred
outer perimeter replaces the initial fragmented walls; this is not a finished
playable map or a confirmed real-world boundary layout.

All 15,512 parent objects retain mesh coordinates, faces, local transforms and
material-slot references. The two v34 road-end closure objects are retained
unchanged in an unlinked archive. v40's corrected Taraj bar is preserved.

The first 2,477-mesh pass had pavement corner gaps. Fragmented road/footway/kerb
surfaces were archived and replaced with planar polygon unions/differences and
closed extrusion meshes. See `recon/v41/surface-fix.json` for final active count.
Joined surface mesh checks have zero non-manifold edges and positive volumes.

27,999 sampled clearance rays and 3,111 downward support samples pass along
selected road/footway centrelines and the inferred station link. Radius .42,
heights .35/1.0/1.7m. These are Blender samples, not continuous capsule tests,
all-junction tests or BO3 collision/navigation/co-op verification. Main walk ends
.5m before its intentional terminal wall; old/new seam included. Of 50 lateral
enclosure rays limited to 250m, one Holmdale-junction ray continues along the main
road and reaches the range limit; it is not conclusive evidence of a wall leak.
BO3 unchanged. Final active extension comprises 89 closed meshes; 2,393 first-pass
fragments are archived, not deleted. Local comparison gallery: `recon/v41/index.html`.

## Sources and frame

OSM API snapshot retrieved 2026-10-10, attribution © OpenStreetMap contributors,
[ODbL](https://www.openstreetmap.org/copyright). Unchanged XML and private visual
references are under ignored `references/streetview-capture/extension-v41/`;
hashes and URLs in its manifest. Mapped platform way 309564449; Midland vicinity
building footprint way 173168754 is provisional association with pub node
30147285, not independently verified parcel identity.

[National Rail local-area map](https://assets.nationalrail.co.uk/e8xgegruud3g/sysOnwardTravelMap/4d251dc06b0548629e38ae47099f338d/Syston__SYS_.pdf)
visually confirms Melton/Holmdale/Station Approach topology. Map date April 2024;
contains OS and OSM attribution. Private render crop is separate from source.
[Midland official website](https://www.themidlandrailwayhotelsyston.co.uk/) supplies
address and an exterior image, downloaded unchanged and visually reviewed.
No image is baked into new geometry. Photo appearance/date may differ from today.

`scripts/audit_extension_frame_v41.py` reproduces v25's chainage scale:
1.06406865 Blender units per captured geographic metre, Taraj at chainage
280.47765 and old road endpoint at 321.56398. This is an estimated gameplay scale.
`prepare_extension_route_v41.py` uses OSM highway connectivity and rotates the
new route's local tangent onto the existing seam tangent (-139.2153 degrees).
This is an explicit rigid-frame adaptation; existing streets do not move.

House URL place pin is separate from panorama camera. No nearby mapped house
footprint was found in the OSM snapshot. The Yopa Holmdale listing is an
unidentified different candidate and must not be used as number 29.

## Environment / resume

Blender was initially closed. Opened v40; its installed MCP add-on auto-started
after loading. MCP works. Firefox is open, but Windows Computer Use rejected
browser control because URL-policy enforcement is unsupported for this browser.
The supported browser inventory also exposes no browsers; web reader cannot
open supplied Maps Street View. Do not bypass this control with pyautogui,
ctypes, another driver or direct panorama endpoints.

Continue public-reference modelling where evidence permits. Number 29 requires
an allowed visual reference route or user-provided images. Do not invent it.
Use minutes-scale Workbench/viewport previews; no publishing or engine deployment.

Sam's follow-up requires fidelity to Google top-down road view. Google satellite
comparison is a prerequisite for treating this provisional frame/layout as final.
Asked asynchronously for a supported browser connection while completing checks
and local previews. No live Google satellite or Street View verification occurred.

Reproduction: frame audit → route preparation → build_extension_v41 in v40 →
prepare_extension_surfaces_v41 (Shapely 2.1+) → join_extension_surfaces_v41 in v41
→ check_extension_v41 → review_extension_v41. Build refuses to overwrite an
existing checkpoint. Source OSM XML is read from the preserved private reference snapshot.
