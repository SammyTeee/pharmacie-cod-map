# Zombies geometry review — v28

Source: `assets/blender/pharmacie-syston-detail-v28.blend`.
[Preview gallery and compact WebM](../recon/v28-zombies/index.html).
This is a read-only Blender review; the saved source and engine deployment are unchanged.

## Fix before expanding gameplay

1. **Right-hand doorway beside the bar exposes unfinished space.** The targeted
   inside render shows the world background and neighbouring building geometry
   through the opening. Five eastward rays from Y=17m also leave the scene without
   a hit. Give this opening a complete service-room floor/walls/ceiling, or block
   it with an opaque scenery door until that room is built. Do not make it an
   accessible purchase leading into empty space.
2. **Junction terrain is incomplete.** The retained junction camera at
   (-31,-18,1.7)m has no surface beneath it within 8m. The downward preview shows
   separate pavement pieces and exposed background around them. Complete the
   road/terrain footprint and pavement joins; bound the playable area deliberately.
   Continuous visible ground and separate engine collision are both required.
   Rear-alley/connector previews also show exposed background around the narrow
   retained route. Floor support along the route does not cover its surroundings;
   extend terrain and add scenery that blocks these views beyond playable bounds.
3. **Define where combat stops.** The long Melton Road extension and bridge are
   scenery at present. Choose a compact first playable extent and model visible
   boundaries rather than allowing players toward unfinished ground, brook banks
   or scenery parcels. Use view-blocking buildings/terrain beyond combat bounds.

![Unfinished opening beside bar](../recon/v28-zombies/gap_bar_east.png)

![Junction ground coverage](../recon/v28-zombies/gap_junction_ground.png)

## What the checks support

- 572 route samples through the retained pub entrance/main aisle, bar approaches,
  service store, stairs, upstairs hall, outer alley and rear connector have named
  floor support, no recorded radial blockers and no low overhead hit under the
  existing 0.35m-radius/1.95m-height ray assumptions.
- All sampled Melton centreline/lateral points have a downward geometry hit.
  That does not establish a continuous surface between samples or distinguish
  road from every other possible mesh hit.
- 64 supported interior sample positions were tested along six axial directions.
  No sampled floor/ceiling rays are open; five horizontal rays are open at the
  bar-side doorway. A hit on furniture or distant scenery does not prove a room
  wall exists, so this is not a watertightness certificate.
- Twelve fresh pub/stair/upstairs/alley renders, eleven wider street/Taraj views
  and three targeted gap views give 26 still previews. Some retained street
  cameras sit above player height; the gallery labels the camera locations.

Evidence: [route probes](../recon/v28-zombies/pub/route-probes.json),
[view probes](../recon/v28-zombies/pub/view-probes.json),
[room envelope](../recon/v28-zombies/pub/room-envelope.json),
[street and camera rays](../recon/v28-zombies/geometry-review.json).

## Zombies design priorities

- Preserve the front-door → outside → outer-left alley → rear-door → pub escape
  loop. Verify it with zombies pursuing in both directions after door purchases.
- Upstairs is a branch with a stair bottleneck. Give it a useful reward and test
  whether four players can pass/revive there; another escape route is a design
  option, not an observed building connection.
- Simplify collision on tables/chairs/bar props and keep the tested aisles clear.
  Decorative detail should not catch players or stop zombie pursuit.
- Treat the Taraj entrance and booth aisles as a separate future combat design:
  add deliberate zones/spawn entrances and validate pursuit before opening the
  whole road. A clear Blender aisle alone does not establish Zombies navigation.
- Keep usable weapons, perks, power and purchases on reachable supported floor
  with interaction triggers outside solid blockers. Existing engine prefab
  placements and new Blender details do not automatically stay aligned.
- Repair the Syston street proportions from wide references before more facade
  decoration. This review does not establish geographic accuracy.

The first runtime checks after conversion should be: floor/wall collision and
unwanted sky views; purchases from both sides; stair/door traversal; zombie
pursuit across every unlocked connection; furniture snags; and four-player
spawns/revives. No compiler/game run was performed here.

## Video and reproduction

The WebM is a 640×360 solid-material inspection animation: thirteen short forward
camera moves with cuts, 26 seconds, eight distinct rendered frames per second.
Final VP9 WebM is 688,798 bytes (about 0.69 MB); repeated frames provide 24fps
playback. Encoding uses FFmpeg `-framerate 8 -t 26 -vf fps=24 -c:v libvpx-vp9
-b:v 260k -crf 38 -row-mt 1 -deadline good -cpu-used 4 -pix_fmt yuv420p -an`.
FFprobe duration/codec/dimensions and all gallery media paths pass verification;
stills and final-video contact sheets were visually inspected. Exact results:
[review validation](../recon/v28-zombies/review-validation.json).
It shows silhouettes and enclosure; the Cycles stills show textures and lighting.
Camera movement is not a demonstrated walkable route. Temporary inspection
lighting/cameras are never saved to the source.

Read-only Blender scripts: `review_zombies_v28.py`, `review_pub_v28.py`,
`check_room_envelopes_v28.py`, `render_gap_review_v28.py` and
`render_review_video_v28.py`, run with Blender 5.2 `--background <v28.blend>
--python <script>`. Earlier slow solid-animation passes were stopped after
stills/probes completed; the final video uses the dedicated faster renderer.
Logs remain in ignored `build/zombies-*-v28.log`.
