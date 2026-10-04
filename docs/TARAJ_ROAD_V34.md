# Opened Melton road and Taraj approach — v34

[Matched review gallery](../recon/v34/index.html) ·
[Blender checkpoint](../assets/blender/pharmacie-taraj-road-v34.blend).

[Watch the hosted tour](https://sammyt.wtf/preview.webm): 60 seconds, 720p/30
distinct fps. Capture took392.3seconds; 19,928,547-byte WebM averages2.66Mbit/s,
about three times v33. Full decode/frame count and remote SHA/HTTP checks pass.
Evidence: [delivery verification](../recon/v34/delivery-validation.json).

Sam asked why the road towards Taraj was closed and requested carrying the
finished High Street approach into that branch. The v31 west boundary was
explicitly a future Melton unlock proposal. V34 archives its complete assembly
and v33 sign/kick details, opening the retained junction and road to Taraj.
No working purchase, zone or scripted unlock is implemented by this change.

Initial player-height views showed floating parcel/building edges, incomplete
ground support and unbounded gaps between the shops. New deep terrain supports
the road and footways, while wider parcel backing stops short of the retained
brook. Original bridge deck, rails, banks and water remain. Closed foundation
skirts sit below the shops; frontage aprons connect their recessed approaches
to the existing footway. Frontage gaps receive masonry backing and coping;
the narrow gaps close at upper-storey height. Larger gaps read as walled plots.

Outer walls sit behind the shop masses, with closures beyond Taraj and down
the unfinished southern junction/Brookside branches. The retained main road
has no new roadblock. Shallow frontage lamps/drips/fixings and flush road-edge
drain grilles add detail without filling the carriageway.

The preview caught overlap when infill initially used historical catalogue
widths. Some current façades retain a scaled transform and an older local mesh
width. Final infill uses the saved façade mesh endpoints transformed into world
space, avoiding that stale-width assumption. Approved pub, Taraj, bridge and
shop architecture remains in place; these additions are inferred Zombies
mapping, not claims about unseen real-world Syston parcels.

## Checks and remaining work

662 new closed meshes pass manifold/positive-volume checks after reopening.
3,429 road samples at 10cm spacing pass floor support, 42cm radial clearance
in sixteen directions at three body heights, and 1.95m overhead checks. The
572 retained pub/rear-alley samples pass. All parent active-scene mesh geometry,
including the archived west boundary, and all 44 catalogued original reference
hashes are preserved. Evidence: [validation](../recon/v34/validation.json).

The presentation camera path has 7,458 samples and passes a separate 20cm
six-axis camera clearance check. The aerial portions are not walking routes.
These checks sample visible Blender meshes; they are not a continuous capsule
sweep, engine collision, Zombies pursuit or co-op verification. Pavement
passing/revives, kerb stepping, individual shop apertures, zones, purchases and
Taraj entry/interior navigation still need conversion and actual BO3 tests.
Road/parcel dimensions remain estimates. The junction apron is still a broad
blockout shape rather than a newly surveyed street reconstruction.

## Tour and reproduction

Sam requested a higher-quality tour over High Street, through the pub and out
via the rear alley, past the street shops, along Melton Road and over to Taraj,
then explicitly requested uploading it to `https://sammyt.wtf/preview.webm`.
Sam rejected the measured hours-long offline render and requested completion
in minutes. The delivered target is a 60-second, 1280×720, 30 distinct-frame
textured GPU viewport capture, VP9 CRF18 with a 6Mbit/s target. Studio shading,
shadows/cavity and source UV textures replace ray-traced lighting. A temporary
capture mesh combines evaluated solids/fonts/curves and preserves per-face
materials/UVs; the editable source remains unchanged. There are cuts between
five continuous camera sections. This is Blender footage. Final measured
encoding facts and upload verification are recorded with delivery.

Benchmarks showed repeated headless renders remained slow even with simpler
shading. The cached merged viewport tests averaged about 0.21sec/frame. The
first offscreen test against an inactive scene crashed Blender at
`BKE_view_layer_active_object_get`; the saved checkpoint was intact. Reopened
it and corrected capture to activate/evaluate the temporary scene/view layer
and active object before drawing. The repaired benchmark and capture work.

Temporary camera/light/sky settings are not saved into the editable checkpoint.
Matched comparison stills use eight-sample Cycles inspection lighting. Original
photos are neither altered nor replaced. No game files, engine export, build,
deployment or BO3 controls are involved.

Scripts, using Blender5.2 in background:

1. `inspect_taraj_road_v34.py` renders the six matched views from v33/v34.
2. `build_taraj_road_v34.py` builds the new checkpoint from v33; refuses overwrite
   unless `V34_REBUILD=1` is explicitly set for the generated intermediate.
3. `check_taraj_road_v34.py` reopens and validates geometry/routes/preservation.
4. `plan_tour_v34.py` makes the inspected camera plan.
5. `viewport_tour_v34.py` runs in the connected Blender GUI and streams raw GPU
   frames directly into FFmpeg using a responsive timer. The temporary merged
   scene is never saved. `render_tour_v34.py` retains the slower offline route
   and its benchmarks for explicit future use.
6. `deliver_tour_v34.py` decodes the capture, checks metadata/hashes and makes
   the local gallery/contact sheet before the requested upload.

Render/build logs are in ignored `build/v34-*.log`. Earlier unrelated local
changes and checkpoints are preserved. Video quality/frame-rate preferences
are now recorded in AGENTS.md for future requests.
