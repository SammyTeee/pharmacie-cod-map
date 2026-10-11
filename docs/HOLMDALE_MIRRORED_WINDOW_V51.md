# Matching porch windows — v51

Checkpoint: `assets/blender/pharmacie-holmdale-mirrored-window-v51.blend`.

Sam requested the approved right porch window mirrored on the left. The left
return now matches the right's 1.07 model-unit width, replacing its previous
0.68-unit width. Frame, lower panel, glass, transom and opening upper vent are
mirrored across the central door's normal axis. The matching left vent is an
explicit user correction, superseding v49's asymmetric photo interpretation.

The exact mirror initially extended 0.42 units inside the existing house wall.
The porch, central door and rounded landing therefore move forward together
0.45 units. Door remains over its own landing. Right window shape/dimensions are
retained. The separate right plant ledge, three pots and nearest multipart basket
follow to avoid overlap. Existing main bay window and house shell are unchanged.
All dimensions are estimates; this is not measured architectural survey data.

289 copied/new mesh parts are in `DETAIL v51 | Mirrored left porch window`.
Superseded own geometry is retained unchanged in the unlinked fake-user archive
`ARCHIVE v51 | Smaller left porch window`; v50 checkpoint also remains intact.
Original photos unchanged. No BO3 changes or functioning door implementation.

`recon/v51/validation.json` records the mirror transform, dimensions, fit and
archived objects. Closed positive-volume checks pass. Selected approach/corridor
checks pass 32,535 clearance rays and 3,615 support samples, with zero blocked or
unsupported samples. Porch endpoint follows the relocated threshold. These are
Blender ray samples, not continuous capsule or game navigation tests. Two known
enclosure-side misses remain documented by the inherited wider route checker.

Three current material viewport previews use the v50 camera setup:
`recon/v51/porch_front_after.png`, `porch_context_after.png` and
`porch_plan_after.png`. V50 images provide the preceding comparison. Scripts:
`scripts/holmdale_mirror_window_v51.py`, `check_holmdale_v51.py` and
`review_holmdale_v51.py`. Broader extension work and authorized final commit/push
remain pending.
