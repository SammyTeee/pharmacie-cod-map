# Number 29 central corner porch — v50

Working checkpoint: `assets/blender/pharmacie-holmdale-corner-porch-v50.blend`.

Sam corrected v49: the door must occupy the middle face above the walkable
rounded landing. The raised strip on the right is for plants. Original user
photos 2 and 8 were re-inspected alongside the survey in
`HOLMDALE_PHOTO_SURVEY_V49.md`; source photographs remain unchanged.

## Corrected arrangement

The central door is diagonal across the corner, approximately 45 degrees to
both glazed returns. The door projects forward, and each side window returns
towards the house. This replaces the straight-facing bay arrangement in v49.
The left side has a tall obscure pane and opaque lower panel; the right has
an obscure pane, upper vent and opaque lower panel. The middle door retains
its black lever and letter slot, brass peephole and flower ornament.

The fascia, cap and gutter follow the three faces. A rounded lower landing sits
under the door and threshold. A separate, higher ledge follows the right wall
for pots; one left pot was relocated out of the diagonal walking approach.
The nearby hanging basket was moved clear of the door. Dimensions and angles
remain estimated from perspective photographs, not a measured survey.

In house-local coordinates, the three fronts run:

- Left glazing: `(3.10, 0.03)` to `(3.10, -0.65)`.
- Central door: `(3.10, -0.65)` to `(3.85, -1.40)`.
- Right glazing: `(3.85, -1.40)` to `(4.92, -1.40)`.

The rounded landing stones reach z=0.082, mortar z=0.070. The separate plant
ledge stones reach z=0.142. These are model units. Door geometry is static;
opening, interaction and collision in BO3 have not been implemented.

## Preservation and checks

305 closed positive-volume meshes are in
`DETAIL v50 | Diagonal central door and porch`. Superseded own porch/landing
parts and the moved source pot are preserved unchanged in the unlinked
`ARCHIVE v50 | Straight-facing porch revision` collection. Affine remapping is
baked into copied vertices to preserve the new corner geometry without losing
shear through Blender transform decomposition. The main house placement,
flat right window, perpendicular garage and seven opposite houses are retained.

- `recon/v50/validation.json`: final topology and closed-mesh checks.
- `recon/v50/route-checks.json`: 32,535 selected clearance rays and 3,615 support
  samples, zero blocked/unsupported. Porch route approaches diagonally.
- `recon/v50/porch-support.json`: six explicit landing samples, all supported
  on stone or its mortar joints.
- `recon/v50/v40-preservation.json`: 15,512 original fingerprints,
  zero missing or changed; the two previously archived closures stay archived.

These are selected Blender ray checks, not continuous capsule sweeps or game
navigation tests. BO3 remains unchanged. Broader roof, plot and overhead
alignment work remains pending; final extension commit/push is authorized once
the extension is finished.

## Matched previews

Six 1280×900 material viewport renders are recorded in `recon/v50/review.json`:

- `porch_front_before.png` / `porch_front_after.png`: facing the middle door.
- `porch_context_before.png` / `porch_context_after.png`: house corner context.
- `porch_plan_before.png` / `porch_plan_after.png`: porch plan and paving.

Generation, checking and review scripts are `scripts/holmdale_corner_porch_v50.py`,
`scripts/check_holmdale_v50.py` and `scripts/review_holmdale_v50.py`.
