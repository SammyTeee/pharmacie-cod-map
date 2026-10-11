# Station / Holmdale working copy v45

Saved: `assets/blender/pharmacie-station-holmdale-v45.blend`.
Review: `recon/v45/index.html` links route, Midland and number 29 reviews and
shows four latest matched before/after pairs. Goal remains unfinished pending
Google overhead verification. Commit/push requested after completion.

## New geometry

Mapped station car-park polygon 220522771 connects to the retained approach.
Seven clipped OSM rail-way sections form the three main lines/crossover
context, with closed ballast beds, sleepers and rail profiles. Track levels,
profiles and switch appearance are estimates; trains do not operate.
The retained single platform now has a brick railward retaining edge and a
lowered rail bed. The former close enclosure walls were replaced with expanded
terrain, low station perimeter plinths and open metal panels. Boundaries are
gameplay adaptations, not surveyed real-world walls.

An estimated parallel ramp connects car park to platform, following the
official schematic’s arrangement without treating it as a scale drawing.
Handrail ends were shortened after they crossed the older perpendicular
approach samples. Both approaches remain clear in selected tests.

Holmdale has a modest widened turning end and brick/timber terminal boundary
based on the user’s September 2023 road screenshot. Exact outline, dimensions
and position remain estimates pending Google top-down comparison. Number 29’s
photo-led assembly is retained unchanged from v44; see its reference notes.

Five original v41 joined surfaces are archived unchanged, replaced by v45
surfaces. Four first-pass ramp posts are also archived unchanged. Final active
v45 mesh counts and manifold/volume checks are in `validation.json`.

## Verification

- 32,805 selected clearance rays and 3,645 support samples pass, including
  retained main/footway routes, station approach, parallel ramp, parking aisle,
  house/garage approaches, driveway crossing and widened turning end.
- Sampled support elevations range from -.08 to .03. This avoids treating
  low terrain backing as a valid pavement floor in these samples.
- These are short longitudinal rays at radius .42 and heights .35/1/1.7,
  not full capsule collision, every junction, AI, co-op or BO3 tests.
- Two of 50 limited lateral enclosure rays do not hit within 250m. Open metal
  fence gaps/range-limited rays do not prove continuous collision enclosure;
  no watertight or engine-boundary claim is made.
- Direct v40 comparison checks all 15,512 source objects: no missing or changed
  geometry/transform/material-slot fingerprints. Only the two intentionally
  retired v34 beyond-Taraj closures are absent from the active scene; their
  objects are retained unchanged in an archive.
- The direct audit covers parent/basis/inverse, vertex coordinates, polygon
  topology, font content/size/extrusion and material slot names. It does not
  audit shader graphs or game behavior. Source hash and full baseline are saved.
- Eight matched 720p Workbench images took about 58 seconds. Station corridor,
  approach and Holmdale images were inspected; these are model previews, not
  satellite evidence or final textured renders.

The isolated MCP baseline command timed out before producing a result and
its process exited. A separate factory-startup background Blender run loaded
v40 and completed the baseline, then the live v45 comparison passed. No
interactive Blender restart was needed.

## Remaining completion gate

Google top-down reference covering Taraj through station/Midland and Holmdale
must verify the road geometry, junctions, car park/platform and number 29’s
footprint/facing. No supported browser connection is available; a screenshot
in the reference folder was requested. The only existing overhead image covers
the older High Street–Taraj segment and cannot verify this extension.

Do not mark the full goal complete or call this geographically verified before
that comparison and any resulting corrections. BO3 unchanged. Original Google
source images remain local/ignored. Final commit/push remains authorized but
pending completion; unrelated prior working-tree changes should remain intact.
