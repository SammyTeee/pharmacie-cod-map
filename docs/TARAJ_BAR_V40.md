# Taraj bar side correction — v40

Latest checkpoint: `assets/blender/pharmacie-taraj-bar-v40.blend`.

On 5 October 2026 Sam corrected the Taraj bar to the opposite side, while
looking across the side entrance at the right wall in Blender. Moved the complete
115-object assembly from the left front wall to the right front wall and rotated
it 180 degrees to face inward. Counter, hollow fridge, drinks, shelves, optics,
labels, register, tap and three practical lights move together. Front-bay depth
is retained to avoid overlapping the first booth. No mesh data is changed;
all other object transforms are retained. V39 street/retail detail is retained.

Matched screenshots: `recon/v40/taraj-before.png`, `recon/v40/taraj-after.png`.
Reproduce by running `scripts/fix_taraj_bar_v40.py` once on v39 in interactive
Blender. Manifest: `recon/v40/validation.json`. Current viewport and material
preview retained, overlays hidden. Default opener now selects v40.

36 visible-mesh rays pass across the side entrance, two dining aisles and bar
approach at three heights. These are sampled Blender checks, not continuous
collision, AI/navigation or BO3 verification. Engine unchanged; no deployment,
push or media upload.
