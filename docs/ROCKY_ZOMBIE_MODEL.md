# Rocky zombie character — 25 October 2026

Sam requested a recognisable zombie version of Rocky from three supplied photos,
using the separate Dave character workflow. This is a separate character asset;
no map edit, BO3 conversion, deployment or game launch is part of this request.

## References and likeness

Unmodified originals are preserved locally and ignored in
`references/pharmacie-syston/rocky-zombie-2026-10-25/` with SHA-256 provenance and
photo-by-photo observations. Photo 2 guides the face; Photo 3 supplies the pale
checked short-sleeved shirt. Photo 1 supplies jeans, belt, shoes and left watch.
The concept retains bald head/short grey side fringe, broad clean-shaven face,
heavy brows, rounded nose, full cheeks and stocky build. Height is an estimated
1.75 m for review, not a measurement. Rear surfaces are inferred.

Built-in image generation used all three references. The initial wounded/bloodied
concept was rejected by the image service's violence filter. The successful
revised prompt uses intact skin, pale eyes, tired shading and dusty/frayed clothes.
No blood or wounds are present. Exact successful prompt:
`assets/generated/rocky-zombie-v1/concept-prompt.txt`.
Concept: `assets/generated/rocky-zombie-v1/rocky-zombie-concept.png`.

## Actual textured 3D model

One fal.ai TRELLIS.2 generation used the isolated generated concept, resolution
1536, 4096 textures, remesh enabled, target 120,000 vertices, seed 251026.
Listed generation cost $0.35, checked 25 October at
https://fal.ai/models/fal-ai/trellis-2. Credentials remain external and are never
logged. Job IDs, input hash and parameters are in `fal_manifest.jsonl`.

`assets/generated/rocky-zombie-v1/rocky-zombie.glb` contains one UV-mapped mesh,
85,639 imported vertices / 116,722 triangles, one material and two 4096-square
textures. SHA-256:
`aeccbdb57e9688a020abb77836752b3f1d8fd087c4cec29131d46805f7a5bd5f`.

The face is visibly softer than the concept; reconstructed eyelids/eyebrows and
short side hair are simplified, and the bald crown has an angular silhouette.
Shirt underarm/rear creases have small dark reconstruction artifacts. Fingers
are approximate. This is a first review mesh, not an exact likeness guarantee
or an optimized game LOD. The zombie treatment is intentionally mild.

## Review and reproduction

[Local gallery](../recon/rocky-zombie-v1/index.html) contains eight actual Cycles
mesh renders with front, both sides, rear, three-quarter, face and arms. Angle,
detail and combined sheets are available. All eight PNGs decode; local gallery
image/download links are checked by the gallery script. The rendered angle and
detail sheets have been visually inspected. Browser interactions are untested.

Separate packed editable studio source:
`assets/generated/rocky-zombie-v1/rocky-zombie-studio.blend`.
`recon/rocky-zombie-v1/inspection.json` records geometry/UV/texture information;
`gallery-manifest.json` records render hashes.

- `python scripts/fal_rocky_zombie.py submit` submits once (existing-job guard).
- `python scripts/fal_rocky_zombie.py status` retrieves the existing model.
- `rig-submit` / `rig-status` manage one Meshy humanoid rig request ($0.20 listed
  at https://fal.ai/models/fal-ai/meshy/rigging, checked 25 October).
- Blender background `--python scripts/render_rocky_zombie.py -- --high` renders.
- `python scripts/gallery_rocky_zombie.py` rebuilds review sheets and gallery.

## Completed rig and checks

Meshy completed in approximately 147 seconds of service processing. All eight
returned GLB/FBX character/basic-animation/armature files are downloaded.
Primary handoffs in `assets/generated/rocky-zombie-v1/`:

- `rocky-rigged_character_glb.glb` and `rocky-rigged_character_fbx.fbx`.
- `rocky-zombie-rigged.blend`: separate packed editable rigged source.
- `rocky-walking_glb.glb` / `rocky-running_glb.glb` and FBX counterparts.
- `textures/`: separately saved imported texture images.

`verify_rocky_rig.py` imported the character and both animated GLBs: one armature,
24 deform bones, one character mesh, 85,794 imported vertices / 116,722 triangles
per file. Zero unweighted vertices, zero invalid weight sums, maximum four
influences. Three sampled frames per clip have finite plausible deformation
bounds. Evidence: `recon/rocky-zombie-v1/rig-validation.json`. Blender's Icosphere
bone-control custom shape is correctly excluded from character mesh checks.
These are structural/sampled checks; no full motion quality verdict is claimed.
No facial/finger rig or authored zombie motions were supplied.

Gallery regenerated after rig delivery; all 14 local links resolve. Total listed
fal cost is $0.55 (one model and one rig), not an account-balance audit. Assets
were generated using built-in image_gen, fal TRELLIS.2 and Meshy rigging.

Auto-rigging does not supply BO3 stock skeleton compatibility, zombie attack/death
animations, hitboxes, AI or gameplay. Engine conversion and runtime checks remain
separate work.
Dave, map sources, reference originals and skate prototype are
preserved. No push or publication was performed.
