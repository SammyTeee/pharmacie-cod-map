# Latest-design Zombies exploration test — built and deployed

Sam requested this on 11 October 2026, including free varied wall weapons.
Source: `assets/blender/pharmacie-surveyed-route-v57.blend`, assembled scene.
Output project: `zm_pharmacie_v58`; previous playtest/map packages are retained.

The established official BO3 brush/photo-patch conversion is reused. Scale is
the existing compatibility scale, with final engine transform
`(BU + (-3.5,-10,0)) * 39.37007874015748 + (0,-18000,0)`,
without a second global enlargement. The route still has the v57 documented
geographic estimates and Barkby compromise. This is not perfect visual parity.

Export: 23,580 objects; 17 warnings. First generated geometry: 22,101 convex
brushes, 340 slab prisms, 102 photo patches; 1,685 curved details boxed and
1,216 thin/unsupported objects omitted. Detailed report is local under `build/`.
Unsupported multi-face seated-guest photo uses a flat substitute.

Stock wall-gun assemblies are mounted on exported wall faces with supported
approaches. Server purchase/ordinary ammo costs and corresponding client price
records are zero for this test. Existing route debris gates also cost zero.
Power and stock rounds remain; no invulnerability or no-spawn callback is added.
Road zones/risers are an initial exploration implementation, not balanced survival.

29 wall-gun prefabs cover 10 weapon types, with the complete variety available
around the pub and further repeated mounts upstairs and along the streets.
61 local road zones contain 122 supported riser candidates, in addition to the
existing core zones/risers. 7,379 source decorative meshes were made non-colliding before the lean filter; many are deferred in the final export.
32 solid triangular prisms recover two omitted curved Melton ground surfaces.

The first geometry compile crashed with access violation `0xc0000005` while
emitting cells/portals. The retry marks 22,412 dressing brushes as `detail`,
retaining the pub shells/sky as structural. Compiler flag-order and combined
contents syntax were corrected against installed stock examples. No package
from failed attempts was deployed. Logs preserve each attempt.

Full brush and render-decoration retries still crashed at cell/portal emission.
The final lean export retains 32,182 world brushes/patches and defers 51,677
fine street dressing brush/face elements. The full route, large architecture,
v18 pub objects and corrected porch are retained. This is a coarser street
playtest than the Blender gallery, not a full-detail engine conversion.
The final compiler portal file contains 17,910 cells (full export: 66,149).
The exact internal cause/limit behind the access violations is not established.

Official lean geometry compilation and ground navmesh passed in 48 seconds.
Fresh lighting exported (1,904,767 bytes). Both links completed with exit 0. The complete separate package, including sound banks, was deployed with per-file hash checks. Launch at 20:12 London returned PID 23784, but exited before a window or fresh console log was observed. Runtime remains unverified. Missing flying navvolume is recorded separately
from the successfully generated ground zombie navigation.
Sam retains game controls. No automated movement, purchases or console input.
The old mystery-box base remains decorative; no working box is claimed.

Reproduce from the reviewed saved source with `export_playtest_v58.py`, then
`generate_playtest_v58.py`, `augment_playtest_v58.py`,
`repair_playtest_v58_surfaces.py`, `optimize_playtest_v58.py`,
`recenter_playtest_v58.py`, `mesh_decor_playtest_v58.py`,
`lite_playtest_v58.py`, then
`check_playtest_v58.py`. Generation replaces
only the separate v58 generated project. Preserve manual edits before regeneration.
