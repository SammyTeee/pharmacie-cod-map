# Syston detail — recovered state and latest checkpoint

Latest editable source: [Blender v29](../assets/blender/pharmacie-syston-detail-v29.blend).
Sam confirmed building placement, but wants the whole streetscape and individual
shopfronts as detailed as the Pharmacie, including pavements and road markings.
Firefox/Google Maps reference capture is explicitly authorised.

## Recovered and completed work

V26 Taraj interior/bridge was complete, with ten renders and final validation,
although MODLOG still ended at the v25 bridge review. It remains uncommitted,
alongside pre-existing user changes. Old checkpoints are preserved.

V27 improves metric brick/asphalt/pavement/glazing materials, Costa's sloping
awnings, divided upper windows and café furniture. V28 adds double yellow lines,
zebra zigzags/dotted boundaries, tactile landings/beacon globes, kerb seams,
gullies/utility covers, circulation arrows and individual Amy/GLO/Specsavers
refinements. [V28 notes and four renders](SYSTON_V28.md).

V29 fixes side-wall brick striping discovered in renders; adds Amy Clarke's
photo-guided display/bunting, door flowers and upstairs curtains inside modelled
frames; adds photo-led pitched roofs on Amy/GLO/Specsavers, two chimneys, façade
cable and Costa menu boards. The oversized v27 Costa sign was corrected in v28.

![Amy Clarke detail](../recon/v29/01_amy_clarke.png)

![Costa detail](../recon/v29/02_costa.png)

![Street materials and lining](../recon/v29/03_street.png)

UV-only photo inserts use unchanged native00270. Source hashes, pixel quads and
new-solid checks are in [v29 validation](../recon/v29/validation.json).
Photo inserts are intentionally non-solid private reference scenery. V27 verifies
6659 original mesh geometries unchanged; v28 verifies6749 unchanged,2031 new
closed solids and390 overhead road samples. V29 checks new solids and source
hashes. All three generation logs show completion; rendered images were inspected.
Temporary review daylight is unsaved. These checks are not BO3 verification.

## Satellite evidence and remaining target

New untouched satellite viewport and its separate URL/timestamp/hash manifest:
ignored `references/streetview-capture/syston-overhead-v28/`.
Capture was visually inspected. Attribution is retained; personal sidebar is
visible, so do not publish this screenshot. Imagery acquisition date unverified.
Exact clipboard paste resolved Firefox URL typing failures; historical296-image
walk catalogue remains untouched.

Observed: irregular three-arm junction, curved corners, zebra refuge/rails,
pitched terrace roofs and large rear retail/parking footprints. Satellite tracing
has NOT yet been applied. Existing road/parcel widths remain estimated.

Required next work toward Sam's requested standard:

1. Trace road/footway outlines using satellite and native273/283/284, replace
   circular apron, add refuge, pedestrian rails, actual dropped-kerb ramps and
   calibrated give-way markings. Tactile tops alone do not make the crossing done.
2. Correct GLO's corner apertures; rebuild Amy/Town Square/We Vape terrace and
   genuine passage depth rather than a dark closed panel.
3. Individually reconstruct remaining shops: unique window/door sizes and spacing,
   recesses, displays, roof silhouettes, wall finishes and observed props. Most
   still share the v25 template and are below the Pharmacie detail standard.
4. Revisit Costa upper-window proportions, awning/patio depth and outdoor furniture
   against00233. This is improved, not a finished1:1 reconstruction.
5. Compare each section at player height with matching references before export.

Drain/utility-cover positions, roof pitches and chimney positions are indicative.
No engine export, compiler run, deployment or BO3 input/test in this work.
No new commit/push requested or performed.

## Reproduction

Use Blender5.2 `--background <input.blend> --python <script.py>` in this order:

- v26 → `scripts/refine_syston_v27.py` → v27
- v27 → `scripts/detail_street_v28.py` → v28
- v28 → `scripts/finish_appearance_v29.py` → v29

Scripts refuse to overwrite new milestones. Exact logs are
`build/syston-v27.log`, `build/syston-v28.log`, `build/syston-v29.log`.
Default `scripts/open-blender.ps1` now opens v29.

`scripts/review_appearance_v29.py` then adds six closed brick roof ends after
render review found dark open triangular roof ends. Applied once to saved v29;
log `build/syston-v29-review.log`. Gallery images precede this roof-end correction.
