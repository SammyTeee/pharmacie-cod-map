# Pharmacie / Syston street skating prototype

## Number 29 start and sound — v64, 15 October

Sam requested reaching 29 Holmdale Road. `PLAY-HOLMDALE-SKATE.cmd`, or
`scripts/open-pharmacie-skate.ps1 -Location Holmdale`, now starts directly on
the flat approach in front of the approved house. Street start remains available
through the original launcher. No Blender source or original placement changes.

The v60 house matrix was queried read-only from the actual .blend. The frontage
anchor is (−161.10289, 813.50189) BU; the final start shifts 0.75 m clear of the
driveway/road height transition. Nine support samples agree at −0.042290505 m.
An initial distant spawn v63 passed collision checks but its screenshot showed
no world geometry, so it was rejected. v64 translates the entire exported world
by the same X/Z offset to place this start near the engine origin: visuals,
collision, four grind paths, 25 lights and daylight probes all move together.
Layout, materials and UVs remain. The new origin's native 1 mm weld removes 282
newly collapsed collision triangles; 302,300 remain and pass the native volume,
packed-tag and contact-vote checks. Five feature supports and 2,136 independent
feature-face contact solver cases pass in translated coordinates.

`powershell.exe -NoProfile -File scripts/verify-skate-demo.ps1 -WithAudio -Location Holmdale`
passes `GAME_VERIFY_OK`, stable ground and audio-library initialization. Actual
1280×720 capture `recon/skate-v60/runtime-holmdale-v64.png` was inspected: number
29, its porch/garage, approach and skater render correctly. Interactive session
reopened from this package (parent 19412; recheck live state before acting).
This proves the requested start and rendering, not travel across the whole map,
ridden ramp landings or the underlying cause of distant-origin rendering loss.

Private audio now contains 4,142 validated PCM16 WAVs: 22 ambience beds, 14 rolling
grains, two wheel streams and 244 effect banks, plus native patch/mixer inputs.
All 4,412 referenced files exist and none of the decoded WAVs is silent. One
four-channel treatment clip is legitimate; the engine supports up to six channels.
The pinned r2117 decoder archive matches the upstream SHA-256. Native runtime
logs confirm MixMap, player, rolling, board/wheel and effect systems initialize.
The custom start uses an authored quiet-city fallback bed; no original district
emitters are applied. Original dialogue PCM is deferred. Sound during ridden
pushes, tricks and grinds still needs Sam's test. Source dump unchanged; all audio
stays ignored/private. Conversion cache and explicitly reviewed superseded map
packages were removed after validation to recover disk space.

## Latest floor / ramp-crash repair — v62, 14 October

Sam reported glitchy floor movement and repeated crashes on ramps. The interactive
log pins the crash to `native surface histogram index exceeded` in the physics
and audio contact-feedback systems. The exported collision field contained
sequential object IDs where this runtime expects packed audio/physics/pattern
tags. 90,949 triangles decoded to invalid physics categories and 13,232 falsely
decoded as water. `scripts/fix_skate_surface_tags_v61.py` corrects those fields
from the authored material channels, preserving geometry and presentation.

`scripts/flatten_skate_street_v62.py` then replaces the starter street collision
with a continuous level surface over source bounds x −34..66, y −10.4..−3 BU.
198 shallow collision triangles (paint, repairs, covers and overlapping base)
are removed; overlapping connector faces are clipped while preserving their
outside portions. Visible details remain. Ramps, rails, kerbs and the surrounding
map retain their geometry. This is an export collision repair; the original,
neutral v59 and skate v60 Blender files are unchanged.

Current launch target: `build/pharmacie-skate/pharmacie-street-session-floor-v62-r3.skate`.
Earlier v62 trials are superseded and must not be launched. The final package
SHA-256 is `5b6eab254aed961aa58875eaa37eeda4fe5074d182201fe28012cec0f10222d9`.

Validation: 1,588 clear-street support samples have a common floor height
−0.075183116 m (previous range extended up to −0.061086282 m). The native Rust
reader and core collision constructor accept all 302,582 triangles after the
runtime's 1 mm weld. Every tag matches its material, and every triangle passes
the actual contact surface voting function that previously panicked. Five
feature heights and four grind paths remain. `scripts/verify-skate-demo.ps1`
passes asset initialization and automatic screenshot capture with
`physics_failed:false`; see `recon/skate-v60/runtime-floor-v62.png`.
This verifies startup and the identified crash path, not ridden ramp landings.
Sam retains controls; a fresh riding/ramp retest remains pending.

Additional contact stress proof: `scripts/skate_contact_probe.rs`, built as the
skate-data example `pharmacie_contact_probe`, runs actual core sphere/triangle
queries, contact generation, Jacobian construction and 25 solver iterations.
178 upward-facing authored-feature triangles × four tangent speeds (0, 3, 8,
15 m/s) × three downward normal speeds (0, 2, 5 m/s) = 2,136 passing cases.
All contact points/reactions remain finite, the static world stays fixed, and
surface votes remain valid. Evidence: `recon/skate-v60/feature-contact-stress-v62.json`.
These are independent face-centre contacts with one-sided interior geometry;
they do not test edge adjacency, wheel-to-wheel constraints, board/body dynamics,
animation, controller state or complete ramp landings. The fresh staging rebuild
`repair-contact-repro-v62` runs this gate and reproduces the same accepted hash.

Sam requested a separate skate adaptation on 14 October 2026: skate around the
existing Syston map, with natural street rails and ramps, while retaining the
original for Zombies and other uses. This supplements the ongoing neutral
Blender visual/demo pass. It does not authorize changing or running BO3.

## Chosen route

Use the open-source Rust/Bevy skating implementation, loading our own map.
No original Skate 3 executable, recompilation or second game process is required.
Reuse its full skating controls/physics/tricks/grinds rather than claiming a
new simple movement controller is equivalent. The current upstream executable
still loads extracted original tuning data, animation graphs and character
assets. Sam's extracted source was found at `S:/Skate3Recomp-Windows/game/`,
including `default.xex` and the adjacent data. It is read only. A no-retail-data transplant
would require a separate integration effort and explicit fidelity limits.

- Source: https://github.com/SK8-ENGINE/skate-3-rust-engine
- Pinned checkout: `2e16697797c8358d16f747a8259354ff2921041a`
- Local checkout: `build/skate-3-rust-engine/` (ignored).
- Upstream original code: GPL-3.0-only. Preserve notices and corresponding source
  for any distributed modified runtime. No redistribution of original game data.
- Alternatives inspected: https://github.com/mchughalex/skate3recomp
  runs the original recompiled game; not selected for this custom-world prototype.
- Windows prototype; controller support is inherited from upstream SDL3/XInput.
  Keyboard skating is not currently promised.

## Independent Blender files

- Original approved route: `assets/blender/pharmacie-surveyed-route-v57.blend`.
- Shared visual pass: `assets/blender/pharmacie-demo-base-v59.blend`.
- Skate adaptation: `assets/blender/pharmacie-skate-street-v60.blend`.

The skate variant has its own additions/grind collections and an unlinked archive
of parked vehicle geometry. The neutral file retains those vehicles. All ramps,
ledges and rails are authored fictional gameplay adaptations, not surveyed facts.

## Contract and first proof

One Rust process owns player input, skating physics, tricks, collisions, camera,
and rendering. No inter-process bridge or CoD hooks. Blender is an offline asset
source; it never owns a runtime player.

Blender compatibility scale is 1.0640686466 BU per metre. The export copy divides
coordinates by this once, then the upstream exporter changes `(x,y,z)` to
`(x,z,-y)`. Runtime is Y-up, metres; exported rail points and spawn use the same
transform. Collision uses the actual triangulated surface, never concave bounds.
Original photo UV/image pairs stay paired. Procedural materials need explicit
portable PBR/image treatment; shader graph parity is not automatic.

First playable proof: load our street, spawn supported near the pub, push/turn/
brake/ollie, land on a bank, grind the authored flatbar and return to the road.
Then check the ledge, manual island and curved return. Capture runtime video and
logs. A Blender render, parser success or unit tests cannot prove this gate.

## Evidence so far

- Read-only v57 inventory: 24,107 assembled scene objects; zero missing external
  image dependencies (`recon/v59/baseline-inventory.json`).
- Neutral visual pass: authored seamless texture PNGs, physically projected UV
  layer, 831 closed rainwater/window-detail meshes. Saved separately; original
  shader graphs are copied into archive materials. See `recon/v59/build-validation.json`.
- Downloaded pinned upstream source and locked Cargo dependencies.
- Untouched upstream `cargo test --locked -p skate-core --offline --no-default-features`:
  **654 passed, one failed**, group-8 moving-body impact-feedback assertion.
  Log: `build/skate-core-tests.log`. No runtime or parity claim; no upstream physics
  changes made to make this test pass.
- Matching experimental build 49 downloaded from the official repository into
  `build/pharmacie-skate/runtime/skate3rust-windows-x64/`. No installer, original
  game launch or existing save/profile edits performed. Local data setup follows below.
- Neutral route check passes (39,771 rays / 4,419 supports), as does direct v40
  preservation. This is not skate-runtime verification.
- Separate skate Blender file saved: 24 closed new meshes, four grind paths,
  255 parked-vehicle objects archived unchanged only in this variant.
- Five skate and ten neutral 720p Cycles stills rendered. First three street
  camera positions were corrected after review found they were inside buildings.
  Final street views and the reel contact sheet visually reviewed.
- Local 25-second 720p/30fps **animated still reel**, with clear design-preview
  labels: `recon/skate-v60/street-session-design.webm`. It is not a continuous
  fly-through or gameplay video. Review page: `recon/skate-v60/index.html`.
- The first export rejected missing per-object collision material assignments.
  Added explicit `ow_material` in the temporary export adapter. Full export
  completed: 24,463 visual objects, 1,018,051 visual triangles, 305,208 collision
  triangles, 46 original textures, four rails, 61,569,577 bytes. Rust reader passes.

## Runtime integration — same session

- Prepared only core tuning/graphs, default character, runtime HUD and presentation
  parameters from the existing local dump, using pinned upstream conversion
  functions. No original game executable runs and no original disc maps were
  converted. Output only in ignored `build/pharmacie-skate/`. Native RefPack
  decoder was compiled locally for extraction. Source default.xex hash remains
  `1db39496585c521d17a2137804f42cf73ebed2b32cac166ec42dbf772f4dcf7f`.
- Runtime first rejected thin triangles after its 1 mm global collision weld.
  `repair_skate_collision_weld.py` applies that exact weld to the runtime copy and
  removes 2,440 collapsed triangles; max position adjustment 1.432 mm. All visual,
  material, original texture and authored-feature bytes are retained. Repaired
  collision has 302,768 triangles. The Rust probe now checks the real volume
  constructor after the runtime weld, plus spawn, obstacle heights and run-out floors.
- Repaired runtime `--check-assets` passes: map, physics, skater, controls and four
  grind primitives initialize; `SKATE_ASSETS_READY`. Core extraction also passes
  the stock test-world check. Logs in build/.
- Actual startup capture succeeds with `GAME_VERIFY_OK`: ground state, 299 physics/
  animation ticks and 16 resting contacts, no physics failure. First screenshot
  showed black colour-only surfaces because the native texture renderer ignores
  portable material tints. Fixed in `adapt_skate_render_materials.py`: authored
  small albedo textures for solid colours, supported explicit material definitions
  and an original procedural sky. Second capture succeeds and colours/sky are
  visually confirmed (`recon/skate-v60/runtime-materials.png`).
- Earlier captures had all four controller slots disconnected. The final lit
  capture reports slot 1 **Ready**, with an idle packet. No driving inputs sent.
  Pushing, steering, ollies, landings and grinds remain unverified.
- A third presentation stage adds an authored normal-orientation daylight map and
  character daylight probes (`light_skate_demo.py`). Final 1280×720 actual capture
  passes with `GAME_VERIFY_OK`, character lighting/sky loaded and stable ground
  state: `recon/skate-v60/runtime-demo.png` and `.input.txt`. Character shading
  and ground shadow visually reviewed. 299 physics/animation ticks, 16 contacts;
  not a movement, trick or performance benchmark.
  This is a simple lighting approximation, not a Blender bake or native fidelity claim.
- Runtime audio extraction is deferred; the first prototype is silent. No online
  session, original-game launch, CoD changes or external publishing.

Open the neutral file with `scripts/open-blender.ps1`; use `-Skate` for the
separate skate file. `PLAY-SYSTON-SKATE.cmd` / `scripts/open-pharmacie-skate.ps1`
target the isolated demo package and local assets. Controller required by this
upstream build. Launcher defaults to our own prepared assets; `-Assets` can override.
The first interactive launcher (PID 4412) split the title's spaces, producing
`Unknown argument "Street"` before engine startup. Sam shared that diagnostic
report; it was a launcher argument error. Quoted the title explicitly, closed
only our failed-launch diagnostic, and reopened successfully: parent PID 10176,
worker 19424 (recheck liveness before acting). Passive log confirms stable
PhysicsGround with physics_failed:false. The controller was initially present
but later reports disconnected; reconnect before the human trial.
No controls sent; keep Sam in control during his
trial. Passive output is in build/skate-interactive-stderr.log. Agent goal remains
active: actual riding checks and wider neutral-map finishing remain outstanding.

No publish, upload or Git push is part of this new prototype request.
