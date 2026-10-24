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

## Runtime floor collision correction — 11 October, evening

Sam loaded the map successfully and reported spawning inside the floor; supplied a screenshot showing the viewpoint beneath the street/frontage slab. Passive capture runtime-floor-01.png is retained. This supersedes the earlier startup-unverified observation: the first attempt exited, but a later launch reached gameplay. Purchases and AI remain unverified.

The converter's high-facet fallback filled the bounds of concave perimeter/road meshes. Spawn half-space inspection of the original export found the player body inside brush 22205; the original spawn position itself was supported by the pub floor. This is a conversion defect, not evidence that the approved Blender floor should move.

repair_playtest_v58_bounds.py replaces twelve large high-facet bounds with upward-surface triangular prisms, preserving narrow walls and road footprints. Run after lite_playtest_v58.py and before check_playtest_v58.py. Legacy box formatting uses six significant digits, accounted for when matching the substitutes. check_playtest_v58_spawn.py compares the original committed export to the repair: one explicit player spawn checked at five lateral positions / three body heights, originally intersecting solid geometry, now clear and supported. This source check is not runtime verification.

Corrected compiler/lighting/link status is recorded in floor-repair-rebuild.log. Runtime retest required before calling the floor issue fixed. Original v57 Blender remains unchanged.

### Compiler resolution for the floor repair

Two raw/simplified world-prism attempts failed at cell emission; later attempts exposed `MAX_MAP_NODES` explicitly. The final representation dissolves top-surface triangles, simplifies curves within 0.08 BU (about 7.5 cm), and merges adjacent convex regions: 897 solids in 57 stationary script_brushmodel groups, up to 16 solids per group. No movement script is attached. 2,910 additional fine non-core brushes and 26,084 tiny non-colliding render patches are deferred in this engine copy; building shells, circulation, house and pub architecture remain. Tiny ornaments are therefore less complete than the Blender review. The temporary small-box proxy attempt also failed and is not in the final map.

Final reproduction adds `repair_playtest_v58_bounds.py`, `trim_playtest_v58_detail.py`, `group_playtest_v58_surfaces.py`, then `check_playtest_v58.py` and `check_playtest_v58_spawn.py` after the original lean pipeline. The repair uses installed Shapely 2.2 (constrained triangulation). Geometry compilation passed in 23 seconds and wrote ground navmesh. Flying navvolume remains absent. Final successful-build log: `floor-repair-convex-build.log`. Lighting/link/deployment confirmation follows below.

Final repair build completed with exit 0: geometry, ground navmesh, fresh lighting and both links. Deployed with recursive per-file hash checks and backed up the previous test package. Launched 20:59:35 London, PID 70224. Spawn correction remains pending runtime observation/manual verification; no input sent.


Passive capture runtime-repaired-start.png after launch shows an above-ground street view with player HUD and weapon, rather than the earlier below-floor view. Manual traversal confirmation remains pending. Outdoor lighting appears overexposed with black sky in this capture and remains a separate defect to investigate. No controls were sent.

Sam confirmed normal movement from the pub onto the street after this repair. He rejected the engine visual quality (missing/poor textures and resemblance) and explicitly requested leaving Radiant aside. Engine work is stopped at this checkpoint; do not continue conversion/build/deployment without renewed direction. Blender remains the visual source of truth and current work returns to its previews. AI, purchases and co-op remain unverified.

