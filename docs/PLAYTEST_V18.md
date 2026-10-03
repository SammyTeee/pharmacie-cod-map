# V18 Radiant Zombies playtest

Latest state and resume instructions: [HANDOVER_2026-10-03.md](HANDOVER_2026-10-03.md).
Sam confirms doors work and sharp-window pass looks good. New crossing/bar
package is built but not deployed. Earlier three-zone/crop descriptions below
are historical; latest source has four zones, eleven risers and separate bar
regions. The .blend is modified in the working tree; preserve it.

2026-10-03. Sam authorized a separate conversion, build and private BO3 test.
Project: `zm_pharmacie_playtest`. Blender source remains unchanged:
`assets/blender/pharmacie-player-cleanup-v18.blend`.

## Implemented progression

- Main pub starting area; stock rounds and damage, no scale-test no-spawn callback.
- 750-point street purchase deletes both front/rear blockers and enables street/alley spawn group.
- 1,000-point stair purchase removes the stair-foot blocker and enables upstairs spawn group.
- Three zone groups, eight riser locations. Stock `_zm_blockers` debris logic handles purchases, linked triggers and navigation reconnection. Stock zone manager adjacency is keyed to purchase flags.
- Quick Revive in pub; mystery box outside; power upstairs.
- Four stock weapon prefabs: RK5/pistol_burst 500 at left pub wall Y3.5; KRM/shotgun_pump 750 at left rear approach Y26; Kuda/smg_standard 1250 outside X-15,Y-0.08; KN-44/ar_standard 1400 upstairs left wall Y14. Prices read from installed `zm_levelcommon_weapons.csv`. Interior wall planes measured through read-only Blender raycasts. Chalk/model/purchase functionality comes from stock referenced prefabs; stock files are not copied into this repository. Weapon mounting/access still requires individual runtime review.
- Street restricted to X-18..30 with scenery beyond physical barricades.

## Conversion and corrective pass

`export_playtest_v18.py` reads evaluated meshes/FONT geometry and the active material output/Base Color image connection, preserves world transforms and rejects unsupported image mappings. Solid meshes with multiple materials use the dominant material; this explicit limitation is reported for the upstairs floor. Image patches retain their face material and UV order. Original photos and Blender file remain unchanged.

`generate_playtest_v18.py` uses the existing brush/prism conversion, adds gameplay entities, and creates separate cropped panel TIFFs/GDT/manifest. 1,837 objects produce 1,598 convex brushes, 103 slab prisms and 76 photo patches. 60 curved details are represented by bounds; 123 thin/concave details are skipped and individually reported. Stock wood/brick replace procedural Blender shaders. This is a playtest conversion, not full visual parity with Blender.

First runtime loaded successfully, registered 750/1000 purchase prompts, and passive captures show combat, Quick Revive and round-four HUD. Log reports a zombie repeatedly unable to path from raised seating around Blender X6.2,Y5.6 to rear players. Added shallow `clip` ramp along the platform aisle edge for the corrective build. This fix is not yet runtime-proven.

Sam reported blurry/unreadable photo textures and excessive darkness. First conversion used implicit material tiling sizes, nearest power-of-two resize, and legacy light-only intensity fields. Corrective pass:

- Explicit material `tilingWidth`/`tilingHeight` match converted image dimensions, `tileColor=no tile`, `filterColor=aniso8x (mip linear)`, valid opaque `alphaTest=Always`.
- Resize rounds upward, capped at 4096, retaining more crop detail. Higher output resolution does not invent detail absent from the source image.
- 25 explicit BO3 `white_light` omni lights using `radius=300`, `stops=8`, lighting-state keys, positioned through pub, upstairs, stairs and alley/street.
- Four wall buys and platform navigation ramp included.

The lighting field mismatch is supported by installed stock `zm_giant_light.map`. The exact cause of the texture collapse is **not yet established**: implicit tiling/mipmap selection and UV interpretation need runtime comparison. Do not describe increased resolution or successful linking as proof the texture defect is fixed. Read-only graphics inspection found TextureQuality=1 (drops one mip on streamed textures), TextureFilter=2 (16x); custom images use streamable=0. Game settings were not edited.

## Build/deploy evidence

Commands from repository root:

```powershell
build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/export_playtest_v18.py
python scripts/generate_playtest_v18.py
.\scripts\build-map.ps1 -ToolsRoot 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130' -MapName zm_pharmacie_playtest -AssetFolder assets/playtest-v18 -AssetNamespace pharmacie_pt18 -RebuildAssetDatabase
.\scripts\launch-blender-test.ps1 -ToolsRoot 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130' -GameRoot 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III' -MapName zm_pharmacie_playtest
```

First full build: `build/playtest-v18-build.log`, exit0. Corrective `/update` failed duplicate asset registrations: `build/playtest-v18-fix-build.log`, exit1. Backed-up `/rebuild` followed by full compile/navmesh, fresh LED and both links succeeded: `build/playtest-v18-fix-rebuild.log`, exit0. Complete zone/snd tree recursively deployed and every file hash compared, players/previous package backed up by launch script. First actual Steam game PID24520; corrective launch request PID25612 may be replaced by Steam's actual game process.

Compiler warnings: missing stock mystery-box `jun_art_wood_plywood_dark03`, small geometry/portal warnings, skipped flying-AI navvolume; ground navigation produced. Runtime stock template emits unrelated missing optional assets. Distinguish these from actual `PATHFIND_FAILURE_UNREACHABLE` defects.

User chose **Leave the controls to me**. No game input, console commands, automatic purchases or movement sent. Passive gfxcapture only. Solo combat and rounds observed in first build; linked purchases, all weapons/power, fixed platform/stair pursuit, texture correction and co-op remain unverified until observed in corrective runtime. No Git push or public map release performed for this test.

## Follow-up evidence and second corrections

Corrective build loaded as actual game PID25984. Passive capture
`build/playtest-v18-fix-runtime.png` shows substantially brighter pub lighting,
but photo detail still inconsistent. Sam confirmed some images improved, many
still bad, original doors/blockers unattractive and no purchase option.

Door triggers initially overlapped the solid blockers, putting their centres
behind the use trace obstruction. Moved trigger volumes entirely onto pub-side
approaches, supplied explicit centre origins/cursor hints, and matched stock
clip brushmodel `DYNAMICPATH=1` / `spawnflags=1`. Replaced full wood walls with
framed visible brush pieces plus separate invisible collision. All pieces retain
linked targets, so a street purchase removes both exits. This is a supported
cause hypothesis and source correction, not yet a verified purchase.
`build/playtest-v18-doors-build.log` passed; diagnostic follow-up
`build/playtest-v18-uv-calibration-build.log` passed and was deployed/launched
(actual game PID24288).

Temporary non-solid panels used a single 2048-square image with texture-coordinate
spans 1/128/2048. Sam requested passive capture: `build/bo3-current-screenshot.png`.
That view is from behind/oblique to the boards and shows streaking and enlarged,
reversed text, so it does not establish the correct scale for a frontal view.
Normal Zombies remained enabled; navigation errors also occurred when players
stood on furniture or other unsupported goals. Do not claim the platform ramp
eliminates all AI failures.

Sam saved unchanged runtime evidence `references/broken fronty textures.png`.
It shows readable Wreake Valley imagery but a blank Pharmacie fascia. The exported
fascia bitmap (`build/pub-fascia-export.png`) contains the expected white lettering;
its storage was 1024x128, whereas the successful shop fronts use square storage.
Next correction standardizes **every photo TIFF to square power-of-two storage**,
retains crop aspect on the world geometry and uses new asset identities to avoid
stale cached materials. Originals are unchanged. This addresses a plausible
non-square coordinate scaling defect; precise engine normalization is still not
proven. The original door photos each contain only ~83x239 source pixels; resizing
alone cannot restore that missing photographic detail.

Square build passed (`build/playtest-v18-square-build.log`). Photo patch lightmap
coordinates were also corrected from all-zero to distinct 0/1 grid corners,
matching the earlier photo-panel exporter that rendered correctly. Latest build
log: `build/playtest-v18-square-lightmap-build.log`; inspect completion before
deploying. Diagnostic panels are removed in this normal regeneration. Do not
overwrite the active BO3 package or close the user's game to deploy: wait for Sam
to close BO3, then use the hash-verified launcher script. Continue passive captures.

Follow-up result: that square/lightmap build passed and was deployed after the
game exited. Sam confirms the entrance fascia lettering now appears, while
window imagery is still blurry/cropped. Door purchases remain unconfirmed.
Live Blender inspection establishes the panes themselves are opaque JPG photo
proxies (Alpha1, Transmission0), with matching active/render UV_Source_Photo
layers. Actual transparent glazing would require a separate material/geometry
change. Main display crops have only about132x317 source pixels, doors83x239.
The exporter now respects render or explicit shader UV maps; this safeguard is
not a demonstrated fix for the matching frontage UVs. A frontal game screenshot
is needed for the remaining crop diagnosis; latest passive capture is title
screen only. No new build or source-Blender change from this inspection.

Steam screenshots subsequently found and preserved unchanged in
`docs/build-results/playtest-v18/screenshots/`. Latest `20261003153501_1.jpg`
confirms readable fascia and remaining abruptly truncated window lettering;
mapping/framing still needs direct Blender comparison. Earlier diagnostic-build
screenshots `20261003151524_1.jpg` / `20261003151536_1.jpg` explicitly show the
750-point debris purchase prompt. Prompt appearance is verified, successful
opening and upstairs purchase are not. Those older wall streaks are not evidence
of the latest square/lightmap build's rendering.

Sam confirms doors now work. Sharp-window follow-up removes per-pane raster
crops and retains original Blender UVs on full source bitmaps in square storage.
Two original high-resolution drinks-plaque artworks are added as non-solid
outer-window overlays; exact photographed wording, approximate font/border,
with PNG/SVG/provenance in assets/signage. Source Blender stays unchanged.
Source checks compare all exported image UVs with the original evaluated export
and verify both plaque assets. Build log:
`build/playtest-v18-sharp-window-build.log`. Runtime sharpness/cropping remains
pending; photographic interiors and reflections still have source limitations.

Sharp-window full build passed exit0, including fresh lighting and both links.
Verified log copied to `docs/build-results/playtest-v18/sharp-window-build.log`.
With BO3 closed, package hash-verified and launched at14:54:12UTC, requested
PID25728, backup `build/before-blender-test-20261003-155410`. Ready for Sam's
manual inspection; no claim of runtime texture success from compiler results.

Sam confirms sharp-window result looks good. New crossing/bar iteration:
- Wooden street-end wall becomes1250-point debris purchase from either side.
- crossing_zone opens X30..60 road/pavements and Post Office/Natural Wellbeing
  lane X45..48,Y-30..-13;3 additional risers activate on unlock,3 fill lights.
- Fixed outer boundaries stop leaving ground; lane is a dead end. Shop interiors
  remain scenery. New crossing chase/navigation and balance need manual testing.
- Separate documented lower-drawer/backbar/TV crops in assets/bar-regions avoid
  showing upper shelving on the counter face. Source checks verify exact pixels
  against the original and retain original UVs on all other photo surfaces.
Build log:build/playtest-v18-crossing-bar-build.log. No active game overwrite.

Full crossing/bar build passed exit0 (fresh lighting and both links); archived
log docs/build-results/playtest-v18/crossing-bar-build.log. Deployment pending:
BO3 PID21404 remains active. User asked to close session when ready. The current
game is the preceding sharp-window build, not this crossing/bar package.
