# Number 29 — photo-led working exterior v44

Saved: `assets/blender/pharmacie-holmdale-house-v44.blend`.
Source: `assets/blender/pharmacie-station-detail-v43.blend`.
Review: `recon/v44/index.html`, four matched before/after views.

Sam supplied and identified the Google Street View collage in
`references/29 holmdale.png`. Observations and remaining unknowns are recorded
in `docs/HOLMDALE_REFERENCE_V44.md`. Original sources remain unchanged/local;
no Google image pixels are embedded in geometry/materials or the gallery.

The assembly contains 1,692 active closed positive-volume manifold meshes and
one number-plate text object. Individual weathered roof tiles, two hipped
roof volumes, projecting bays with angled glazing/white joinery, pale side
curtains, brick plinth relief, white porch/transom/sidelight, curved step,
narrow side door, green ribbed garage door, gutters/downpipes, lamps,
wall ornaments, pots, driveway, hedge/tree and brick/timber boundary follow
visible features. The rear/garage depth, dimensions and landscape positions
are estimates. It is a static closed exterior, not an accessible interior.

All 16,141 parent scene objects retained their transforms and data references
in the build check. Approved pub/Taraj/bar and prior street work are retained.
The house is parented to `Holmdale v44 | Movable number 29 assembly`. Its
translation/facing currently use the supplied address pin and the provisional
OSM road end; this does not prove geographic footprint alignment.

Initial checks caught nine rays at the inferred right fence crossing the
retained pavement route. Eleven fence pieces were archived unchanged and
the remaining boundary trimmed to a clear setback. Thirty thin curtain
proxies were archived and replaced by twelve pale side panels after render
review. Forty-one archived detail pieces remain available in the .blend.
The final geometry validator covers the active assembly after refinements.

Final route check: 29,025 selected clearance rays and 3,225 floor-support
samples, zero blocked/unsupported samples. Includes main route, Holmdale,
station approach/inferred link, house/garage driveway approaches and a
driveway crossing. Radius .42; heights .35/1/1.7. These are selected Blender
samples, not full capsule collision, all transitions or BO3 runtime tests.

Matched 720p Workbench previews were visually inspected against the collage.
Material-colour previews do not represent final textured lighting. Four
after views take about 29 seconds; no hours-long render was started.

Still required for the full extension: Google top-down alignment, the
photo-observed widened cul-de-sac end, coherent station rail corridor,
car park and parallel access ramp. BO3 unchanged. Sam requested committing
and pushing the finished extension; no commit/push has been made yet.

Build script includes the final curtain/foliage/fence choices. The two
refinement scripts describe the one-off changes made to the first saved
build; do not rerun them on a new build that already includes those choices.
