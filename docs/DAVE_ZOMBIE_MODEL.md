# Dave zombie character — 24 October 2026

**25 October update:** [BO3 replacement trial](DAVE_BO3_ZOMBIES.md) now provides
a stock-skeleton conversion and separately built/deployed `zm_pharmacie_dave66`.
The initial Meshy rig described below is preserved. Actual gameplay is unverified.

Sam requested a recognizable zombie version of Dave from three supplied photos,
then a usable 3D character with white-background front, left, right, rear and arm
close-up previews. This task creates a separate character asset, with no map or
engine deployment.

## Sources and design

- [Original photo index](../references/pharmacie-syston/dave-boss-2026-10-24/README.md).
  The three originals remain unchanged and Git-ignored; SHA-256 manifest retained.
- Built-in image generation used all three photos, with Photo 2 the primary face
  reference and Photos 1/3 supporting build, tattoos, clothing and poses.
- Generated concept:
  `assets/generated/dave-zombie-v1/dave-zombie-concept.png`.
  Exact prompt: `assets/generated/dave-zombie-v1/concept-prompt.txt`.
- Design retains rectangular glasses, short grey hair, pale goatee, broad build
  and tattooed forearms; dark short-sleeved shirt/trousers are torn and stained.
  Zombie appearance is fictional. Tattoos and unseen rear details are inferred,
  not exact photographic reconstructions; shoes and height are design estimates.

## Actual 3D assets

Two bounded fal.ai TRELLIS.2 generations used the generated concept, not the raw
photo background. V1 used 1024 resolution / 2048 textures / 70,000 target vertices
($0.30 listed). V2 uses 1536 / 4096 textures / 120,000 target vertices ($0.35
listed). V1 was retained as a softer preliminary mesh. Request IDs, seeds,
parameters and input hashes are in each asset folder's `fal_manifest.jsonl`.
Prices checked against https://fal.ai/models/fal-ai/trellis-2 on 24 October.

V2 `assets/generated/dave-zombie-v2/dave-zombie.glb` contains one UV-mapped mesh,
97,871 imported vertices / 115,577 triangles, one material and two 4096-square
textures. This is the review-quality mesh; engine LODs/optimization remain
separate. Original GLB SHA-256:
`f190637c9f587d74cad077012a03e8c678cb7bd18e74ad1e1515dae36df201bf`.

The reconstruction softens the face and turns the glasses into opaque dark
surfaces. The source concept preserves the face/eyes more clearly. This is a
visible limitation of the current mesh, not an exact likeness guarantee.
The rear hair surface also has irregular reconstructed areas visible in review.

## White studio preview

[Local gallery](../recon/dave-zombie-v2/index.html), with eight inspected actual
Cycles mesh renders, full-size dialog and angle switching. Rendered in a separate
factory-startup Blender process; no existing map file was loaded or saved.
Studio source: `assets/generated/dave-zombie-v2/dave-zombie-studio.blend`.
The review-only height normalization is an estimated 1.75 m.

- `recon/dave-zombie-v2/angles-sheet.jpg`: front, Dave's left, Dave's right, back.
- `recon/dave-zombie-v2/detail-sheet.jpg`: face and both tattooed arms.
- `recon/dave-zombie-v2/inspection.json`: imported geometry, texture and render data.
- `recon/dave-zombie-v2/gallery-manifest.json`: render hashes and gallery checks.

Reproduce the high-detail job with `python scripts/fal_dave_zombie.py submit --high`
(existing-job guard prevents a second request). `status --high` fetches results.
`rig-submit --high` requests one Meshy humanoid rig plus included basic walk/run
files ($0.20 listed at https://fal.ai/models/fal-ai/meshy/rigging);
`rig-status --high` fetches it. No account credit purchase or top-up was made.
Credentials are read from the existing external file/environment, never logged.

Render with Blender background `--python scripts/render_dave_zombie.py -- --high`.
Build review sheets/gallery with `python scripts/gallery_dave_zombie.py`.
Preview locally with `python -m http.server 8766 --bind 127.0.0.1 --directory .`
at `http://127.0.0.1:8766/recon/dave-zombie-v2/index.html`.

## Rig and engine status

Meshy rigging completed after about 416 seconds of service processing. All eight
returned rig/animation files were downloaded, including GLB and FBX versions of
the rigged character, basic walking and running clips, plus armature-only GLBs.
Primary files in `assets/generated/dave-zombie-v2/`:

- `dave-rigged_character_glb.glb` — 24-bone skinned character.
- `dave-rigged_character_fbx.fbx` — corresponding FBX handoff.
- `dave-zombie-rigged.blend` — separate packed editable Blender source.
- `dave-walking_glb.glb` / `dave-walking_fbx.fbx` — basic human walk.
- `dave-running_glb.glb` / `dave-running_fbx.fbx` — basic human run.
- `textures/` — separately saved imported texture images.

`scripts/verify_dave_rig.py` successfully imports the character and both animated
GLBs. Each has one armature, 24 deform bones and one character mesh with 98,061
imported vertices / 115,577 triangles. Zero unweighted vertices, zero invalid
weight sums and at most four bone influences per vertex. Sampled evaluated
walking/running positions are finite with plausible bounds and changing poses.
Evidence: `recon/dave-zombie-v2/rig-validation.json`.

The first check incorrectly counted Blender's generated 42-vertex Icosphere
bone-control custom shape as character geometry. Corrected the validator to
exclude objects explicitly assigned as pose-bone custom shapes; no skin-weight
repair or model alteration was needed. These are structural/sampled checks,
not a complete deformation-quality or gameplay verdict. No finger or facial rig
was supplied, and the included basic walk/run clips are not authored zombie moves.

Final gallery checks: eight decoded PNGs, three inspected review sheets, valid
local image/download links, browser angle switching and full-size dialog verified.
The browser screenshot API timed out; source render images were inspected directly.
Total listed fal request cost was $0.85 across the two generations and one rig job;
this is recorded pricing, not an account-balance audit or credit purchase.

An auto-rig does not provide a BO3-compatible skeleton, zombie attack/death set,
hitboxes, damage behavior or gameplay implementation. Engine-specific retargeting,
material conversion, optimization and actual runtime verification remain pending.
The existing Blender map, skate prototype and BO3 files were not edited by this
character task. Other concurrent map work must remain separate.
