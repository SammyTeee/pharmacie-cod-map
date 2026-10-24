# Neutral Blender demo pass — 14 October 2026

Saved editable file: `assets/blender/pharmacie-demo-base-v59.blend`.
Original `pharmacie-surveyed-route-v57.blend` remains unchanged. A separate
skate variant is described in [SKATE_PROTOTYPE.md](SKATE_PROTOTYPE.md).

This is a visual pass toward Sam's requested demo, not a claim that the whole
1.09 km route is finished. The later surveyed shops still have repeated opaque
window proxies, blank fascias and estimated hidden building volumes. These are
visible completion items. No BO3/Radiant changes or new engine choice for the
neutral map have been made.

## Changes

- Seven original seamless texture assets: slate, clay tile, three brick tones,
  paving and asphalt. Generation code, repeat dimensions and hashes in
  `assets/materials/demo-v59/manifest.json`.
- Eight material shader updates, with complete previous shader copies retained
  under `ARCHIVE v59 shader | ...`; a separate physical projection UV layer
  retains existing UV layers. Roof projections remain approximate on slopes.
- Material variation on 222 newer surveyed objects. Original approved v40
  material slot names are retained.
- 831 closed meshes: gutters, downpipe fixings, upper-window lintels and thin
  curtain edge details. These are estimated architectural finishing, not a
  new measured survey or modelled shop interiors.

## Checked

- Read-only baseline inventory: 24,107 assembled objects, zero missing external
  images. This proves dependency availability, not material quality.
- Every new detail mesh is manifold with positive volume.
- All source object vertices/topology/transforms retained. Only the listed
  surveyed material slots changed in the source-object fingerprint comparison.
- Selected eleven-route check: 39,771 clearance rays and 4,419 support samples,
  zero blocked/unsupported. Same documented sample limits as v57; not continuous
  collision or any engine/gameplay test.
- Direct v40 audit: 15,512 object fingerprints unchanged; five previously
  documented boundary/infill archives. Fingerprint scope excludes shader graphs
  and UV layers; those visual changes are separately recorded above.
- Ten 1280×720 Cycles material renders: `recon/v59/render-report.json`.
  Street, newer terrace and approved house images visually reviewed. Matched
  neutral/skate street cameras support comparison in `recon/skate-v60/index.html`.

Reproduce: generate textures with `python scripts/make_demo_surface_textures.py`,
then Blender background on v57 with `scripts/build_blender_demo_v59.py`.
The builder refuses to overwrite an existing checkpoint. Check with
`scripts/check_demo_base_v59.py` and render with `scripts/render_demo_v59_v60.py`.
