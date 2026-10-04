# V32 street and opposite shopfront detail — 2026-10-04

Latest checkpoint: `assets/blender/pharmacie-street-frontages-v32.blend`.
Preview: [comparison and continuous exterior flight](../recon/v32/index.html).
Retains the [v31 vehicle layout](STREET_COMBAT_V31.md) and v30 enclosed rear alley.

Added two wall-side benches, three litter bins, flush service covers, road-edge
drain grilles and flower buckets outside Floral Fantasy. Opposite shopfronts
receive shallow plinths, sill drips, fascia trim, entrance bulkheads, alarm boxes
and louvred vents. These fittings are original inferred gameplay dressing;
confirmed shop signage and existing photo-led frontage geometry remain intact.
Props hug the building edge rather than filling the walking route.

Four solid approach wedges bridge the 8cm road-to-kerb rise at the pub crossing
and marked crossing. They are a practical blockout adaptation, not a final
surveyed accessible crossing design. Engine collision, stepping and AI routing
remain untested. The saved scene contains no scripted new purchases or spawns.

227 new closed meshes pass generation-time manifold/positive-volume checks.
Saved-file checks retain 572 pub/alley and 1,248 street route samples, 0.42m
radial clearance at three body heights and 1.95m overhead checks. All parent
scene mesh geometry and 44 original photo hashes remain unchanged. Reference
hashes and checkpoint preservation are recorded in `recon/v32/validation.json`.
Sparse rays do not establish continuous collision or BO3 gameplay validity.

Before/after renders use temporary daylight and material highlights; these are
never saved back to the checkpoint. The separate continuous exterior camera
flight is a presentation path, not proof of player traversal. Exact media
dimensions, duration and bytes are recorded with the preview artifacts.

Crash recovery completed the interrupted flight and rerendered its 12–20 second
roof-to-alley turn using the corrected exterior camera path. The finished
flight is 28 seconds at 1280×720/24fps. Delivery checks and SHA256 hashes are in
`recon/v32/delivery-validation.json`; reproduce with
`python scripts/verify_delivery_v32.py`. These check media, gallery links,
checkpoint provenance and original references, not game behavior.

Scripts: `build_frontage_detail_v32.py`, `check_frontage_detail_v32.py`,
`render_frontage_detail_v32.py`, `render_flythrough_v32.py` and
`gallery_frontage_detail_v32.py`. Blender5.2 background execution; logs are in
ignored `build/`. No game input, deployment or engine build. Sam's latest request
authorizes pushing this finished mapping/media pass, superseding the earlier
no-push instruction. No fal credentials or generated skeleton asset included.
