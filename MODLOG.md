# Mod log

## 2026-10-03 — Detailed photographic text reconstruction specifications

- Sam requested as much useful photo-to-text description as possible for near-1:1 rebuilding. Re-inspected all 16 supplied street views, all four existing pub contact sheets, 22 pub references directly at full-image level, and existing lossless AVIF derivative; alternate copies/drawings/contact-only coverage recorded honestly. Existing video notes cross-referenced, not represented as a fresh full-video review.
- Added docs/STREET_PHOTO_RECONSTRUCTION.md: source map; explicit orientation/adjoining-shop and access-lane topology; detailed 13 building descriptions and separate alley/doorways; shared terrace modules; upper-window counts, facade/recess/glass/sign profiles, roof heights/bays/chimneys, crossing/parking/kerb/junction/island, street furniture; tracing anchors, state/occlusion hazards, visual acceptance and targeted missing evidence.
- Added docs/PUB_PHOTO_RECONSTRUCTION.md: all 28-source descriptive ledger; room orientation/sightlines; collage/dado, paired lit cabinets, distinct apparatus/dental/optician boards, shelf props, clinical tables/trolley/stool/chair/sofa families, skeleton/dentist chair, platform, five visible bar drawer rows, pumps/backbar/screen, ceiling/projector/lighting, structural evidence boundaries and rendering checks. Observations distinguished from existing model placements and gameplay modifications.
- Added read-only source-catalog script and docs/RECONSTRUCTION_SOURCE_INDEX.md / reconstruction-sources.json: 44 original references, exact paths/dimensions/SHA256/review levels. Command `python scripts/catalog_reconstruction_sources.py` exit0; all28 prior source hashes match, no source mutation during inspection. AVIF original unchanged. No new raster assets or live Street View capture.
- Linked specifications from starting notes, asset plan, provenance README and current repair plan. Documentation/metadata only; no Blender/map regeneration, compiler/game run, deployment or push. Exact world dimensions/rear connections still unresolved; no claimed 1:1 survey or repair success.

## 2026-10-03 — Gameplay prefab placement and new street-photo review

- Checked actual scale-map prefab anchors against generator: power (5.8,9.8,0)m, box (0.7,-1.4,0), Quick Revive (1,1.2,0), shotgun (6.4,9.6,0), all angles 0/90/0. These are original hard-coded test placements, not updated Blender wall/marker placements; no prefab bounds/clearance verification exists. Proposed named anchors, placement manifest and deliberate street/rear-service positions documented in docs/TEXTURE_LAYOUT_FIX_PLAN.md. No gameplay changes yet.
- Visually inspected seven new references/*.png captures, three alt/nattywells/*.png views and two root v16 game screenshots. Confirmed adjoining Wreake Valley/pub with alley outside neighbour; Post Office/Papermoon/Pasha/Natural Wellbeing/crossing and Fox & Hounds junction support fuller street blockout with closed placeholder masses and pitched roofs. Screenshots show extensive source-photo content on individual fronts; exact texture-conversion fault still unproven.
- Added extended street and gameplay placement plan; originals unchanged. No Blender/map edits, regeneration, build, game input/deployment or push. New reference provenance recorded in reference README.

## 2026-10-03 — Texture/layout investigation and repair plan

- Sam reports incorrect shopfront texture display after Blender-to-Radiant conversion and corrects street order: facing pub, alley then left neighbour then Pharmacie then right neighbours. Reviewed v16 export/material manifest and conversion/street scripts; eight shopfront source-image bindings match expected originals. Wrong-image selection not confirmed; shared screenshot UV crops and actual compiled dimensions require visual comparison.
- Confirmed exporter weaknesses: material slot zero only, first linked image node, active UV only, no per-face material indices or shader Mapping resolution. Left-neighbour script deliberately retained alley beside pub, explaining wrong layout. Detailed findings and planned derivative-per-front/material/UV audit and alley relocation: docs/TEXTURE_LAYOUT_FIX_PLAN.md.
- Investigation/planning only; no Blender modification, map regeneration, compiler/game run, deployment or push. Runtime texture cause remains unresolved.

## 2026-10-02 — Radiant documentation and conversion review

- Sam requested documentation research while Blender work continues. Read installed official Radiant_Launcher_QuickStart (8 pages), Scale_Standards (7), Generate_LED (1), Build_light (3), Images (3), and relevant material guidance via existing local pypdf; checked official Treyarch Steam announcement online. Bundled quick-start contains historical beta caveats; verified local builds take precedence.
- Added docs/BLENDER_RADIANT_WORKFLOW.md with primary-source page references, actual v03 export/generator behavior, transform/unit conversion, collision/material/geometry limitations, and next-version street/spawn/clearance requirements. Linked from workflow/test/plan notes. Suggested four-player clearance and progression/mood questions; existing outside-spawn/wider-layout choices preserved.
- Official suggested single door hole is 56×96 units; standing hull 32×72; stairs minimum width 80, default rise/run 8/12. These guide the next clearance pass rather than proving traversal. Highlighting the Launcher map row, rather than only checking it, may explain the earlier unnamed.map; GUI confirmation pending.
- Documentation-only work: no Blender bridge call, source regeneration, Radiant launch, build, deployment or push. Newer Blender edits remain on Sam's requested conversion hold. Reviewed scripts/evidence; git diff --check used for documentation validation.

## 2026-10-02 — Estimated-scale Blender tracing base

- Sam confirmed no measurement is available; proceed with approximately **7m frontage**. Inspected original council-plan raster and used it instead of AI-cleaned geometry for tracing.
- Created `assets/blender/pharmacie-scaled-plan.blend` using original packed 1264×874 council image, two separate UV reference planes, uniform **7/222m per pixel**, aligned front corners, 7m frontage guide and 1m ticks. Upstairs reference hidden initially; both tracing planes at Z=-0.02, floor elevation unresolved. Existing starter retained; no BO3 map changes.
- Live bridge command `build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/scale_blender_plan.py` succeeded. Ran `scripts/check_scaled_blender_plan.py` through same runner: actual guide length 7m, 2 planes, identical scale and packed original verified. Screenshot `build/blender-scaled-plan.png` inspected; enlarged viewport framing afterwards. All scale remains approximate. No building geometry or export/build claimed.
- Next: trace wall/opening outlines into the prepared geometry collections, then add heights and stair connections with assumptions documented. Scale can be recalibrated later. Details/provenance in `docs/BLENDER_WORKFLOW.md` and reference README.

## 2026-10-02 — Blender and official MCP setup

- Sam requested Blender-first modelling from `hq floor plan ai.png`, then installation of Blender and the best suitable MCP. Inspected the full original sheet: two floors, rear stairs/service/WCs/stores, subdivided upstairs and proposed external seating. Seven-metre frontage is an estimate; drawing date/as-built status unresolved.
- Installed official winget packages BlenderFoundation.Blender **5.2.2 LTS** and astral-sh.uv **0.12.22**, both successful. Installed official Blender Lab MCP extension **1.0.0** and isolated server **1.0.2**, source commit `dbbf836ad4b1025f14a2b3b504c43903f39e0b04`; local bridge **127.0.0.1:9876**. Registered global Codex MCP name `blender` without changing existing entries.
- Created `assets/blender/pharmacie-reference-base.blend`: packed untouched original sheet, metric units, top view, separate modelling collections. Reference-only; no building geometry/export claimed. Existing BO3 map and game/tool install untouched.
- Verification command `build/blender-mcp-env/Scripts/python.exe scripts/verify_blender_mcp.py` exited 0: initialization, 26 tools, inspection, Python edit and save succeeded. Report `build/blender-mcp-verification.json`. Blender GUI PID 6580; may need fresh Codex session to expose newly configured tools.
- Exact setup/reproduction and plan caveats: `docs/BLENDER_WORKFLOW.md`. Next: trace the new plan, establish height/scale assumptions, then prove one Blender asset export through BO3 before wider detailed modelling. No BO3 build attempted for this reference-only setup; no push/publication.

## Project

- Goal: create a cooperative multiplayer Zombies map based on The Pharmacie Arms in Syston, with a later boss inspired by Noseley. The user approved switching the target from World at War to Black Ops III on 2026-10-02 because BO3 has an official, more direct Mod Tools path.
- Game install: Steam app 311210 at `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III`; `BlackOps3.exe` is present.
- Local project/repository: `C:\Users\sam\pharmacie-cod-map` (GitHub remote is configured as `git@github.com:SammyTeee/pharmacie-cod-map.git`).
- User is new to map-making and wants agents to carry most implementation work, keep clear handover notes, and ask when real choices or permission are needed.

## Chosen route

Use the official Black Ops III Mod Tools (Steam tool app 455130) and Radiant Zombies map workflow. BO3 is preferred over WaW because the official tools are distributed through Steam and support a current Zombies template/build workflow; the WaW guide reviewed requires copying patches into the game root and overwriting files. BO1 is not selected because its mapping route is community-built and less straightforward. Do not attempt to use a Gaussian splat as playable level geometry.

Start with a stock-asset blockout and a working BO3 Zombies template, then add pub-specific geometry/textures/props, and only then build the Noseley boss. Provisional map name: `zm_pharmacie`; confirm against the BO3 template before creating tool-generated files.

## Environment observations

- `CoDWaW.exe` exists at the stated Steam path. Its Windows file/product version properties reported `1.7` / `1.7x`.
- The adjacent `version.inf` reports `ExtVersion=1.6`; this differs from the executable properties and should be resolved by checking the running game's displayed version before compiling.
- A separate Mod Tools directory was not visible in `S:\SteamLibrary\steamapps\common` during the initial check. Verify Steam Tools library/install state before assuming Radiant or the compiler is available.
- Follow-up check on 2026-10-02: `S:\SteamLibrary\steamapps\common` contains the WaW game but no Mod Tools folder. Steam manifests in `S:\SteamLibrary\steamapps` include `appmanifest_10090.acf` for WaW and no manifest identified as WaW Mod Tools. This confirms the tools are not installed in that library; other Steam library locations have not yet been ruled out.
- Rechecked executable metadata on 2026-10-02: `CoDWaW.exe` reports file version `1.7` and product version `1.7x`; the game's `version.inf` still reports `ExtVersion=1.6`, so the discrepancy remains unresolved. The running game's displayed version has not been checked.
- BO3 install check on 2026-10-02: the game is present at `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III`; `BlackOps3.exe` exists. Steam reports the game installed (75.6 GB on disk); its manifest still lists pending transfer/staging bytes, so recheck Steam if game files appear incomplete.
- BO3 Mod Tools check on 2026-10-02: Steam app 455130 is fully installed at `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130` (build 5284267; 28.1 GB on disk). `bin\Radiant_modtools.exe`, `bin\modlauncher.exe`, and `map_source\zm\zm_giant.map` are present. Optional content DLC 499270 is disabled. Preserve the stock source map; do not edit it in place.
- Created the project in the Mod Tools launcher on 2026-10-02 using the Zombies map setup: `zm_pharmacie`. Its generated template is preserved in this repository at `map_source/zm/zm_pharmacie.template.map`; working `.map`, GSC/CSC, `.zone`, and `.szc` source files are also tracked. The code generator creates the first pub room and follows the user's Paint layout (see `docs/BLOCKOUT_LAYOUT.md`).
- User wants the editor/game visible beside the 2K desktop. Radiant is a resizable app window; use BO3 at 1600×900 windowed for game checks, without changing desktop resolution.
- BO3/Steam source notes: Steam BO3 page https://store.steampowered.com/app/311210/Call_of_Duty_Black_Ops_III/ ; Mod Tools hub https://steamcommunity.com/app/455130 ; mapping guide https://steamcommunity.com/sharedfiles/filedetails/?id=3737598953 .
- The first generated room compiled and linked on 2026-10-02 using BO3 Mod Tools build 5284267. Exact commands and findings are below; that first successful build preceded the latest layout iteration.
- The current sketch-based layout also compiled, generated an AI navmesh, and linked on 2026-10-02. It has not yet been launched in BO3.
- The installed Universal Modder plugin is a helper for reconnaissance/asset preparation; it does not replace Radiant or the BO3 Mod Tools build pipeline.
- Handoff portability: all paths under `S:\SteamLibrary` and `C:\Users\sam` are Sam-PC observations. The editable source and generator are in this repository; another contributor needs BO3 and Mod Tools installed, then must stage source into their own tool tree and rebuild there. Compiled game/tool assets are intentionally not tracked.
- Radiant reconnaissance (2026-10-02): the Launcher lists `zm_pharmacie`; a direct launch and Launcher Level Editor attempt opened `unnamed.map` (0 brushes, 0 entities), so opening the project in Radiant remains unresolved. A single editor used about 4.6 GB RAM. Found third-party [mcp-radiant](https://github.com/hetri-courses/mcp-radiant), whose README claims geometry/entity/script/build automation; we used its published captured command syntax to run official build executables directly, without installing its code. See `docs/RADIANT_WORKFLOW.md`.

## First code-authored build record

- Working source: repository `map_source/zm/zm_pharmacie.map`, staged byte-for-byte to `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130\map_source\zm\zm_pharmacie.map`.
- Working directory: `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130\bin`; process environment set to `TA_GAME_PATH=<Mod Tools root>\`, `TA_LOCAL_ASSET_CACHE=<Mod Tools root>\share\assetconvert\`, and `TA_TOOLS_PATH=<Mod Tools root>\`.
- Compile command: `cod2map64.exe -platform pc -navmesh -navvolume -loadFrom "<Mod Tools root>\map_source\zm\zm_pharmacie.map" "<Mod Tools root>\share\raw\maps\zm\zm_pharmacie.d3dbsp"`.
- Result (first simple room): compile succeeded in about one second, writing `zm_pharmacie.d3dbsp` and `zm_pharmacie_navmesh.hkt`; `nav_volume.hkt` was an empty placeholder because the map has no `nav_volume` brush. The compiler warned that material `jun_art_wood_plywood_dark03` is missing on template geometry. Zombie navmesh generation did run.
- Link command: `linker_modtools.exe -language english -modsource zm_pharmacie`.
- Result: link succeeded in 2m57.92s for `zm_pharmacie` plus 2.62s for `en_zm_pharmacie`; `usermaps\zm_pharmacie\zone\zm_pharmacie.ff` was 48,513,728 bytes. Stock asset conversion emitted dropped-vertex warnings. Linker reported no Radiant lighting export and used preview lighting, so the map needs a proper Radiant lighting bake.
- Current layout rebuild used the same full compile command after staging the regenerated map. Result: exit code 0 in about 1.6 seconds, `surfCount` 4→110, a `zm_pharmacie_navmesh.hkt` was written, and the `nav_volume` brush warning remained. The six missing `jun_art_wood_plywood_dark03` material warnings remain on retained template barricade geometry.
- Current link command: `linker_modtools.exe -language english -modsource zm_pharmacie`.
- Current result: link exit code 0; `zm_pharmacie` finished in 9.93s and `en_zm_pharmacie` in 3.19s using the warmed asset cache. The first link built cached assets in about three minutes. Current Mod Tools outputs: `zm_pharmacie.ff` 23,928,512 bytes and `en_zm_pharmacie.ff` 231,680 bytes; build products are not tracked.
- Lighting: `Radiant_modtools.exe -ledSilent +medium +localprobes +forceclean +recompute "<Mod Tools root>\\map_source\\zm\\zm_pharmacie.map"` returned exit code 0; it completed asynchronously and wrote `share\\raw\\maps\\zm\\zm_pharmacie.led` (1,718,907 bytes). The subsequent successful linker run followed that artifact's creation, so this package includes the medium-quality Radiant lighting export.
- Not verified: no game launch, screenshot, spawn, round, door, collision, or zombie route has been checked. AGENTS.md requires asking before copying generated map files into the BO3 game install. The compiled package is currently under the Mod Tools installation only.

## References and asset decisions

- Pub photo set and provenance: `references/pharmacie-syston/README.md`.
- The locally supplied `great for texture.avif` is 1973×1227 and visually shows a near-frontal run of vintage pharmacy advertisements, display cases, bottles, and medical objects. It is the best current source for one custom feature-wall panel. Keep the original untouched; crop/straighten and convert a derivative only after establishing the BO3 material pipeline.
- `bar front.jpg` is a clear frontal view of the dark cabinet-front bar; use it to model a bar prop and possibly as a carefully cropped front-face texture.
- Wide interior views show a long, narrow principal room with the street entrance/windows at one end, bar at the far end, central tables, perimeter seating, and decorated display walls. Exact dimensions and the complete upstairs/side-room layout remain unknown.
- Use photos as both direct texture sources (selected flat wall panels) and modelling/layout references. Do not flatten the whole pub into a photograph: retain 3D geometry for collision, circulation, doors, the bar, and significant objects.

## Progress

- [x] Connected Git repository to the requested GitHub remote.
- [x] Created a local pub-reference folder with sourced exterior images and source links.
- [x] User added pub frontage, room, bar, display-wall, and skeleton photographs to the reference folder.
- [x] Wrote shared agent instructions and initial map/photo notes.
- [x] Install BO3 and the official BO3 Mod Tools; confirm install paths and core files.
- [x] Create the `zm_pharmacie` project from the BO3 Zombies map template; confirm the generated GSC/CSC and map source paths.
- [x] Regenerate, full-compile, and link the current Paint-layout blockout; zombie navmesh file is generated.
- [x] Bake medium-quality Radiant lighting. Resolve the missing retained template barricade material and optional nav_volume warnings if they cause an in-game issue.
- [ ] Get approval to install the linked mod files into the game usermaps folder, then launch offline/private and verify spawn, round progression, zombie routes, doors, and collision.
- [ ] Replace one wall area with a custom photo-derived material and verify in game.
- [ ] Expand the pub layout, then implement and test the Noseley boss.

## Next action

The current photo-panel/two-storey source is compiled, lit and linked. Continue runtime verification of the photo UVs/alpha, actual entrance and L-shaped stairs, zombie routes and co-op. Current implementation details and build gotchas are in `docs/PHOTO_MATERIAL_WORKFLOW.md`; latest evidence is in the session record below. Keep stock tool sources and source photos unchanged.

## 2026-10-02 — SVG-driven playable blockout build

- Source is Sam's saved `references/pharmacie-syston/pharmacie-layout.svg`; original SVG/JPEG/JSON preserved. See `docs/SVG_BLOCKOUT.md` for interpretation and scale.
- Generator now reads rendered SVG footprints/rotations, builds rear patio, hollow toilet, connected rear/east stairs, relocated bar/platform/furniture, and bounded entrance vestibule. Ceiling 320 units; simple concrete placeholders.
- Corrected actual `actor_spawner_zm_factory_zombie` placement, moved initial player markers into the aisle, enlarged start zone, and added interior lights.
- First link reported one bad path node at (320,255,16), from the retained tutorial barricade overlapping the power switch. Removed that unused barricade, switched its riser to `find_flesh`, rebuilt and relit.
- Final compile exit 0, navigation mesh written, no duplicate triangles. Lighting export 1,728,318 bytes at 18:55:24 UTC. Final linker exit 0 at approximately 18:56 UTC, both map and English packages generated, no bad-node report in final output.
- Commands from Mod Tools bin, with TA_GAME_PATH/TA_TOOLS_PATH pointing to Mod Tools and TA_LOCAL_ASSET_CACHE to share/assetconvert: `cod2map64.exe -platform pc -navmesh -navvolume -loadFrom <map> <share/raw/maps/zm/zm_pharmacie.d3dbsp>`; `Radiant_modtools.exe -ledSilent +medium +localprobes +forceclean +recompute <map>`; after fresh LED and bake process exit, `linker_modtools.exe -language english -modsource zm_pharmacie`.
- Remaining compiler warnings: stock mystery-box plywood material missing; no flying-AI nav_volume; two retained utility brush entities ignored. Ground navmesh builds.
- Added parameterized `scripts/build-map.ps1 -ToolsRoot <installation>` for subsequent builds. Sam's S: paths are machine-specific, not required by generator.
- Player directory backed up under ignored `build/profile-backup/` before game launch. With approval, staged generated zone package into game usermaps/zm_pharmacie and launched `BlackOps3.exe +set fs_game zm_pharmacie +set logfile 2 +devmap zm_pharmacie`. Runtime result pending below.
- Runtime observed: map loaded with pistol, 500 points and round-one HUD. User input was active, so no automated movement was sent (game-automation skill requires confirmation before taking over). A later passive screenshot shows GAME OVER, 2 rounds survived, 6 kills, 1170 score and 4 headshots. This verifies solo loading, zombie combat and round progression; not every route or co-op. Evidence: docs/screenshots/svg-blockout-first-game.png. The current blockout is visually rough/dark and still needs materials, lighting polish and route testing.

## 2026-10-02 — Upstairs, photo panels and furniture

- Sam clarified that the stairs form an L and lead to one big empty upstairs room of roughly the downstairs footprint. Implemented two connected 13-rise flights, a 168-unit turn landing and 336-unit upper floor, with an L-shaped opening. Upper clear dimensions are 704×1440×304; provisional gameplay scale, not venue measurements. The installed scale guide specifies 8-unit risers; these 12.92-unit prototype risers need traversal testing.
- Stock-material pass uses `t7_wood_planks_damaged_teak` and `t7_brick_worn_heavy_grout_red`, observed in installed stock map source. That pass compiled/linked. The upstairs-only build also compiled, lit and linked (lighting 1,757,921 bytes, link 10.43s plus English 3.14s). Deployed and launched after the existing approval. A passive screenshot (`build/upstairs-runtime.png`) shows GAME OVER, one round, zero kills; this proves loading and a zombie reaching an idle player, not successful stair traversal.
- Sam explicitly approved flat photographic frontage, bar, feature wall and skeleton; door opening aligned to the actual photographed door; more tables. Source photos remain unchanged. Four separate derivatives and an original minimal GDT are under `assets/photos/`; see its manifest and `docs/PHOTO_MATERIAL_WORKFLOW.md`.
- `scripts/prepare_photo_assets.py` converts original photos to compressed-at-build RGBA TIFF inputs, with mipmaps enabled. Three photographs are only encoded/resized; UV crop regions live in `scripts/photo_panels.py`. Skeleton derivative uses the imagegen skill for transparent isolation of the skeleton and dentist chair from the full-length supplied photo. AI processing is documented explicitly.
- Eight photo meshes: three frontage sections around the door, bar drawers, upper bar display, two pharmacy-wall panels, one skeleton. These are non-solid surfaces over separate collision geometry. Replaced the narrow entrance vestibule with a bounded front forecourt so the exterior can be viewed. Physical doorway is approximately x=15.21..134.72, height 158.02. User-requested photographic placement supersedes the SVG entrance position.
- Furniture now has tabletops and legs with two chairs per table. Eight tables total, including three additions (west behind bar, front-right platform, patio); sixteen generated chairs. Upstairs remains empty apart from lighting and stair opening. Central main-room route is intentionally clear; all side routes still need game verification.
- Initial photo build (`build/photo-pass-build.log`) returned zero but compiler warned all custom materials were missing; rejected as a photo verification result. New GDTs require explicit registration. `gdtdb.exe -help` lists `/update`, `/rebuild`, `/export`.
- GDT index troubleshooting: `/update` with trailing/doubled environment paths emitted thousands of duplicate errors; a normalized update registered the eight custom image/material entries but still found stale duplicates. Backed up database to `build/gdt-before-photo-rebuild.db`. Trying the retail game path failed because it lacks `deffiles`. **Successful fix:** run `<ToolsRoot>/gdtdb/gdtdb.exe /rebuild` from `<ToolsRoot>/bin`, `TA_GAME_PATH=TA_TOOLS_PATH=<ToolsRoot>` without trailing slash, asset cache normalized. Exit 0, 355 GDTs/16070 assets, `build/gdtdb-rebuild-normalized.log`. Stock source files were not edited.
- Compiler/Radiant/linker need the earlier verified trailing-slash environment. Removing those slashes produced linker `Could not open zone_source/zm_mod_level.class`, despite a zero linker exit; see `build/photo-pass-final-build.log`. The build script now uses normalized paths for the database and trailing slashes for actual build tools, checks missing custom-material warnings and printed linker errors, and waits for the bake PID rather than unrelated editors.
- **Verified final build:** `.\scripts\build-map.ps1 -ToolsRoot 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130'`, log `build/photo-pass-verified-build.log`. Exit 0; cod2map 1.122s, ground navmesh written, no duplicate triangles, no missing custom material or bad-node report. Fresh LED 1,762,053 bytes at 19:21:23 UTC; map link 9.51s and English 3.65s. Packages: map FF 35,786,304 bytes at 19:21:34 UTC, English FF 231,680 bytes at 19:21:37 UTC. Stock mystery-box plywood and no flying-AI navvolume warnings remain.
- Deployed final package after backing up previous game zone to `build/before-photo-zone/`; restarted only the earlier test PID 13948 and launched `BlackOps3.exe +set fs_game zm_pharmacie +set logfile 2 +devmap zm_pharmacie`. Prior package backup for upstairs iteration is `build/before-upstairs-zone/`; existing profile backup remains `build/profile-backup/`. No desktop resolution or persistent graphics setting changed. Runtime photo inspection pending below.
- Reusable findings, exact UV source crops, paths, assumptions and remaining checks are in `docs/PHOTO_MATERIAL_WORKFLOW.md`. No push or publication performed.
- **Latest runtime evidence:** `docs/screenshots/photo-frontage-first-game.png` shows round-one HUD and the player in the forecourt facing the correctly oriented, readable Pharmacie fascia/windows with a real central opening. This verifies loading and actual frontage texture rendering. All custom materials compiled without missing-material warnings, but bar/feature-wall appearance and skeleton alpha have not been individually inspected in game. Source hashes rechecked unchanged; generated skeleton alpha extrema are (0,255).
- **Observed visual issue:** frontage is too dark and weapon/arms and sky are overexposed/white. Lighting/exposure/probe setup needs investigation against stock light definitions and the installed lighting docs. Do not claim visual polish complete. Passive second capture showed the pause menu; input-idle check was 0 seconds, so no automated input was sent to take over Sam's active session. Leave the running game for Sam to inspect.
- Final source checks: regenerated map, Python asset pipeline completed, PowerShell AST parse passed, `git diff --check` passed (only CRLF normalization notices). Log-based build checks were added after the successful source build; map/material source did not change afterward.

## 2026-10-02 — Brownie repository handover

- Sam requested pushing the entire current project so Brownie can continue with his installed BO3 game and Mod Tools. Include all source, photo references/derivatives, material definitions, screenshot evidence and notes. Keep local profiles/backups, asset databases, compiled game packages and cache files out of Git; these are machine-local and can be rebuilt.
- Updated README with fresh-machine build/deploy steps, current visual defects and next verification priorities. Added Pillow requirements for regenerating assets. Build script now stages the complete `usermaps/zm_pharmacie` source (GSC/CSC, zone and sound config), removing reliance on Sam's already-created tool project; installation checks run before staging. This source-staging addition does not change map geometry or materials.
- Preserved successful full photo-build log in `docs/build-results/photo-pass-verified-build.log`; paths inside that evidence describe Sam's PC. Read `docs/PHOTO_MATERIAL_WORKFLOW.md` for portable commands and GDT indexing/trailing-slash differences.

## 2026-10-02 — New evacuation-plan Blender project

Sam requested a new project from `Architectural Fire Evacuation Floor Plans.png`, retaining the estimated 7m frontage. Created `assets/blender/pharmacie-evacuation-plan.blend` with the untouched packed 1393x1129 image, UV references for both floors, approximate outer footprint curves, metre ruler and separate modelling collections. First reference/guide are hidden initially; toggle their object eye controls and hide the ground reference/guide to trace upstairs. Both planes are at Z=-0.02; storey height remains undecided.

Calibration: ground frontage (82,85) to (82,401), 316 pixels = estimated 7m; 0.022151898734177215 m/pixel. Ground anchor (82,85), upstairs (76,558), shared scale and translation only. Rough building depth about 21m follows from this estimate. No survey accuracy, skew correction or drawing provenance is implied. Red evacuation lines are not wall geometry; external seating is labelled proposed.

Command: `& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python scripts/create_evacuation_plan.py`. Exit 0; save succeeded; packed image dimensions and ruler length asserted. Manifest records original SHA256 and scale. Existing Blender projects and playable BO3 source preserved. Updated open-blender.ps1 default to this file. No wall meshes, BO3 conversion/build or game verification performed for this new plan. Next: trace structural walls and openings, resolve stair alignment/storey heights, then validate one Blender asset export using installed BO3 documentation.

## 2026-10-02 — Editable Blender blockout, photo frontage and interior

Created standalone versions `assets/blender/pharmacie-floorplan-blockout.blend`, `pharmacie-floorplan-blockout-v02.blend` and current `pharmacie-photo-interior-v03.blend`; earlier reference/project files preserved. Both floors have separate rooms, wall pieces, doorway lintels, open hinged doors, window proxies, bar and kitchen proxies. Initial counts 14 doors / 13 window openings; frontage entrance was subsequently replaced by photo-based double doors. UV_Metres and UV_Face_01 added to 290 initial structural meshes. Upstairs model rectified in width by 316/327 and depth by 934/1044 to align drawing envelopes; this is explicitly an assumption, not survey scale. Storey 3.2m, walls 2.9m, 0.22m external / 0.14m internal thickness remain assumed.

Sam corrected stairs: rear outside exit is back-left when viewing frontage head-on; go past toilets, staircase begins on your right, climbs and turns right. Revised start (0.85,19.85,0), corner (4.78,19.85,1.778), arrival (4.78,16.95,3.2); lower +X, clockwise right turn to -Y. 18 risers of 0.177778m, 0.94m estimated width; real L-shaped upper slab void. Earlier ground/service adaptation retained; upper rear store shortened 0.12m. Stair traversal/headroom is not verified. Men/female shared divider is solid; separate entry doors from common area, no connecting door.

Inspected all 28 images in the current source folder via numbered contact sheets (26 photos plus 2 layout references; some alternate encodings/duplicates), and selected bar/wide room/sofa photos at full size. Added 34 grouped photo-led objects: sofa sections, medical tables, low/high stools, raised right seating platform, dentist chair + simple skeleton placeholder, cream chairs, medicine cabinet frames, shelves/bottles, instrument board, taps, backbar screen/shelves and pendant lights. Group roots retain source names and observations; exact furniture dimensions/positions are inferred. No upstairs photo decor invented. Detailed placement evidence: docs/PHOTO_OBJECT_PLACEMENT_PLAN.md; catalog and hashes: assets/blender/photo-review/catalog.json.

Photo frontage remodelled from original pharmcie-arms-syston-2.jpg (actual filename pharmacie-arms-syston-2.jpg): asymmetric 0.95m recess, fixed pane left of offset double doors, angled display bays, blue lower panels, pilasters, layered fascia/cornice, three upper sash windows and pale stone sills. Fascia/glazing/door faces use packed original JPEG with UV regions. Bar drawer face and instrument-board region also use original packed photos. Feature-wall AVIF separately decoded to lossless RGBA PNG, original dimensions 1973x1227, no crop/repaint/resize; wall photo split at structural bend. Visual finish/glass/reflections need further work. Photo UV layers explicitly marked active for render.

Commands: `python scripts/catalog_interior_references.py`; `build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/model_evacuation_blockout.py`, `scripts/finish_floorplan_blockout.py`, `scripts/revise_blockout_frontage.py`, and `scripts/add_photo_led_interior.py`. All eventually returned bridge status ok. Initial mesh triangulation helper hit Blender 5 index-return behavior; fixed. Interior generator initially lacked label material binding and, after reload, exact unsuffixed orphan material names; fixed and rerun from saved v02. Subsequent live project-owned adjustments restored frontage to interior scene, repaired upstairs camera, aligned wall photo segments and activated render UVs. No user reference contents modified; 28 hashes checked unchanged.

Saved/rendered and inspected ground, first-floor, assembled frontage and interior previews. Current overview: assets/blender/photo-interior-with-front-v03.png; photo front closeup: photo-frontage-v02.png. Current Blender scene is '05 Interior - photo-led dressing' with frontage restored; first-floor scene includes shared upper facade. Removable ceiling hidden for cutaway. open-blender.ps1 now opens v03. No BO3 source mutation, compile, export or game test for this Blender work; no push/publication performed. Next: refine interior objects/material visibility, check stair clearances, then validate a small BO3 export route before converting building geometry.

## 2026-10-02 — Requested repository checkpoint

Sam explicitly requested saving and pushing the current Blender work before attempting a BO3 conversion test. Saved v03 again through live Blender; frontage, interior groups, corrected stairs and six packed file images verified in the live scene. Independent background CLI reopen check timed out after 120 seconds; no background verification claimed. Reference/project versions, previews, manifests, source images and scripts included; automatic .blend-number backup files and ignored build/cache/game packages excluded. Origin/master fetched successfully; local HEAD matched remote before checkpoint.

## 2026-10-02 — Blender conversion test and runtime crash

Checkpoint d7203b7 was pushed successfully to origin/master. Read-only Blender geometry export generated separate map_source/zm/zm_pharmacie_blender.map: 645 brushes and 12 photo patches; seven curved details approximated with boxes, original Blender file preserved. Parameterized build-map.ps1 with MapName and optional backed-up GDT rebuild. Initial GDT update failed duplicate registrations; rebuild succeeded. Initial geometry compile exceeded winding limit64; simplified seven curved details. Final build command: scripts/build-map.ps1 -ToolsRoot 'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130' -MapName zm_pharmacie_blender; log build/blender-test-build-geometry-fix.log. Compiler/navmesh, fresh lighting export and both link packages succeeded; minor tiny-portal and stock mystery-box material warnings remain.

User-approved launch-blender-test.ps1 backed up player state and deployed separate test packages to GameRoot/usermaps/zm_pharmacie_blender. Steam gameprocess_log.txt confirms PID11864 launched at22:59:24 and exited at23:00:02 with code -1073741819 (0xC0000005 access violation). This is a confirmed runtime crash, not a verified map load. No visible game-window capture was obtained and no automated input was sent. No matching Windows Application event was found. Cause remains unresolved; distinguish map compilation success from runtime success.

## 2026-10-02 — Fix incomplete test deployment

Found the actual game log at GameRoot/console_mp.log. Its final fatal error was `sound bank - name: zm_pharmacie_blender.en ... failed to load`, preceded by `ERROR: sound read failed`. The deployment script copied only root zone files, omitting the four linked banks under zone/snd/all and zone/snd/en. Updated scripts/launch-blender-test.ps1 to preserve the full directory tree and compare every deployed file's SHA256 against its tool output. This fixes deployment without changing the map or saved Blender geometry.

Reran the approved launch script at 23:07 local with both explicit roots. All eight output files copied and matched; existing test map/player state backed up to build/before-blender-test-20261002-230702. Steam restarted the initial process as PID19960. BO3 showed its post-crash Safe mode prompt; asked Sam to choose No to retain graphics settings. Runtime verification pending prompt dismissal. PowerShell AST parse and git diff --check passed.

The prompt subsequently cleared without agent input. PID19960 became the actual game window and the new console log reported successful ModLoad for zm_pharmacie_blender and Sam connected. Passive gfxcapture screenshot docs/screenshots/blender-test-first-game.png shows the Blender-derived furnished frontage interior, weapon, 500 points and round-one HUD. Sound banks now load; the original fatal error is resolved. Left the running game for Sam. No graphics settings changes or game input sent by the agent. Runtime log still reports PATHFIND_FAILURE_INVALID_START for a rear riser near map coordinates (-3,185,2); route/collision verification is unfinished. Visible photos/props use provisional brush materials. Current .blend is modified relative to the pushed checkpoint by an external/live save; conversion did not overwrite or revert it. Build/export/runtime evidence preserved under docs/build-results.

## 2026-10-02 — Gameplay space changes in Blender; rebuild on hold

Sam confirmed map loads but player cannot fit some doors/passage left of bar. Requested larger overall scale, street outside with UK-style two-way markings, outside player spawn, zombies entering from outside and potentially upstairs. Then explicitly requested NOT rebuilding Radiant yet while making more Blender changes; Sam will close BO3 himself. No game closure, deployment or rebuild performed for these changes.

Inspected live Blender v03 including unsaved changes, then saved a safety copy pharmacie-v03-before-gameplay-edit.blend. Script scripts/add_gameplay_space_blender.py created pharmacie-gameplay-space-v04.blend: original geometry/references/furniture parented to one adjustable 1.5x root, original hierarchy retained. Estimated gameplay frontage now10.5m; deliberate gameplay exaggeration, not survey correction. All 13 interior/rear doorway openings below0.95m widened before scaling; estimated minimum frame-to-frame gap1.305m after scaling. Door leaves opened90degrees, including both entrance leaves. Bar return cabinet/counter shifted0.25m toward its interior before scaling to enlarge left aisle. These are geometric clearance estimates, not in-game traversal verification.

Added19 editable street objects:50m road, two-way dashed white centre line, double yellow edges, pavements/kerbs and side/rear exit landing. Generic illustrative street proportions, not a measured High Street reconstruction. Player marker outside at(6.37,-2,0.1), zombie route markers for street left/right, rear outside and upstairs; wire player hull guide. Markers are planning data, not functioning BO3 entities. Conversion must explicitly handle them and preserve the new street materials in the next authorized export.

Command: build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/add_gameplay_space_blender.py, bridge status ok, saved both files. Rendered and visually inspected gameplay-street-v04.png. Manifest records changes/assumptions. Default open-blender.ps1 updated to v04. Current BO3 map remains earlier v03 conversion, and exporter presently targets v03 only. Explained transfer is not1:1: stock prop materials, seven curve simplifications, small omissions, engine-specific collision/pathing/gameplay setup remain. No further push requested or performed.

## 2026-10-02 — Wider front and corrected local transforms in v05

Sam selected widening front to match building's widest part while keeping Radiant rebuild on hold. Live dimensions confirmed overall1.5x scale included main bar:6.313m wide vs4.209m before. Found local jamb/hinge/bar-return transforms had been reset by reading stale world matrices during v04 reparenting. Repaired local transforms and updated every scene view layer before measuring. World-space jamb centre gaps minus0.12m framing now estimated at least1.305m across13 door groups; traversal remains untested. Source generator fixed to update dependency graphs before parenting.

Created pharmacie-gameplay-space-v05.blend with script scripts/widen_gameplay_frontage.py via live bridge, statusok. Additional reversible frontage X-scale1.205696 anchored at rear footprint left edge makes nominal frontage12.6598m wide (fascia overhang12.7502m), while fascia height remains1.365m after overallscale.162 front-region meshes tapered to source layout over9.4m, UV layers preserved. New rig initially double-scaled parent transforms; detected via rendered height/dimensions and corrected before final save; source now updates new rig before parenting. Outside spawn marker moved to(5.518,-2,0.1) opposite new entrance centre. Rendered and inspected final gameplay-street-v05.png. Default opener and notes updated to v05. Previous files retained. No Radiant export/rebuild, game restart or push performed; BO3 still uses oldv03 export.

## 2026-10-02 — Wider skewed building body in v06

Sam clarified body should be slightly wider than front and retain the plan's rhombus-like skew. Re-inspected untouched evacuation plan and live Blender viewport screenshot: side walls are angled/offset, with rear steps and rooms, not an exact rhombus. V05 frontage taper made body too narrow relative to front. Script scripts/widen_gameplay_body.py reverses that taper on affected vertices, carries front width factor1.205696 through the body, and applies another8% width behind entrance over9.4m transition. Moves origins and geometry consistently across parent hierarchy; leaves completed frontage and street intact. Door/stair geometry and bar follow widened body. Source-image reference planes retained unchanged; widened model is gameplay exaggeration.

Bridge command build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/widen_gameplay_body.py returned statusok and saved pharmacie-gameplay-space-v06.blend;606 body objects adjusted. Ground floor boundary section widths at depths3/8/15/22/29m:12.74/13.11/13.54/14.09/13.35m; nominal frontage12.66m. Main bar counter8.22m wide. Rendered and visually inspected gameplay-street-v06.png and gameplay-interior-v06.png. Disabled relationship-line overlay to make editable viewport clearer. Saved, updated default opener/notes. No game rebuild, deployment, closure, traversal verification or push performed; hold remains in effect.

## 2026-10-02 — Read-only layout review for Sam's selection

Sam requested reviewing awkward placements/blocking furniture and listing issues before choosing fixes, then asked whether upstairs exists. Confirmed scene02 contains upstairs and scene05 is downstairs cutaway. Read live world-space bounds across all scene layers; exported ignored build/layout-review-v06.json for review, rendered assets/blender/review-upstairs-v06.png with render settings restored, left active scene05 and model unchanged. Read-only headroom BVH rays across three positions per stair tread/landing found no structural surface within1.83m above them; limited geometric check only.

Recorded seven findings and proposed fixes in docs/LAYOUT_REVIEW_V06.md:0.40m stool-to-bar pinch; misplaced1.19m-high coffee table; front stool/table off platform edge;1.67m counter too tall relative to approximate1.83m player; conservative chair/table overlap and0.58m gap; exterior side path fails to track skewed wall (path endsX=-5m, wall reaches-5.69m); unguarded upstairs floor-void edges. Floor ray confirms void at(3.5,29.5)m; office samples(-2.5/0/1,29)m still hit floor, so no claimed missing office floor. No fixes or game rebuild applied; awaiting Sam's choice.

## 2026-10-02 — All seven selected layout fixes saved in v07

Sam approved all findings from docs/LAYOUT_REVIEW_V06.md. Inspected live v06 (unsaved state present), preserved that state as pharmacie-v06-before-layout-fixes.blend, and ran scripts/fix_layout_review_blender.py through the live bridge. Statusok; saved pharmacie-layout-fixed-v07.blend. No stale-file reload or original-photo edits.

Moved medical table9.0 and both stools +2.8mX/-1.2mY, giving1.596m between rear stool and bar. Separated cream chairs; placed the coffee table at(0.5,12.2), footprint1.0x0.65m and top0.45m. Front platform table/stools moved0.9m rearward onto support. Preserved widened footprints but lowered bar/cabinet/photo/taps/backbar consistently to counter1.10m, medical tables0.78m above their floors, platform furniture to top1.05m/table and1.02m/stool including0.27m platform, low stools0.50m, sofa cushions0.50m and cream chair backs0.90m. Dentist/skeleton proxy height1.80m; upstairs kitchen worktops0.90m above first-floor slab.

Reshaped side passage as1.8m-wide polygon following skewed wall and extended rear landing to meet it. Added55 rail/post meshes guarding7 upper floor-void boundary segments; stair arrival edge intentionally stays open. Parenting/world transforms updated across all scene layers. Meaningful geometric checks passed: bar gap>1.5m, front set within platform Y bounds, bar top1.10m, guard edges>=5; additional36 samples across approximate player-width footprints hit side-path floor. Upward1.83m rays across three positions per tread/landing found no overhead structural/guard obstruction. These are static checks, not engine traversal/navmesh verification.

Rendered and inspected layout-fixed-interior-v07.png, layout-fixed-upstairs-v07.png and layout-fixed-exterior-v07.png. Manifest records adjustments and validation. Default opener/project notes updated. Radiant/game rebuild remains on hold; no BO3 closure, game deployment or push performed. Next authorized conversion must support new concave passage polygon, guard geometry, material/marker semantics and complete live v07 geometry.

## 2026-10-02 — Requested photo-backed bar in v08

Sam supplied bar front.jpg and WhatsApp Image 2026-10-02 at10.19.05 PM(5).jpeg and requested behind-bar texture. Scripts/add_backbar_photo.py through live bridge returned statusok, saved pharmacie-backbar-photo-v08.blend, retaining v07 fixes. Loaded/reused and packed original2000x1325 bar front.jpg. No source raster changes; both supplied SHA256 values verified unchanged and stored in backbar-photo-v08-manifest.json.

Added editable back-bar photo plane atY20.72m behind modelled shelves/bottles, X=-0.225..7.784, Z=1.08..3.61. Normalised UV crop(left,top,right,bottom)=(0.205,0.215,0.985,0.585) excludes most ceiling and lower cabinet front. TV region(0.435,0.262,0.575,0.402) textures a separate menu surface; aligned existing screen geometry with pictured TV to avoid mismatched screens. Photo's staff-door depiction remains visual detail, not a new functional opening. No derivative image/crop/recompression created.

Rendered and inspected backbar-photo-detail-v08.png with temporary camera removed and original render settings restored. Updated default opener/provenance/current notes. No Radiant rebuild or push; new backbar material requires explicit BO3 conversion in next authorized export (current v03-only generator would otherwise confuse it with drawer-front material).

## 2026-10-02 — Video reference extracted and reviewed
Downloaded Sam's supplied YouTube q0zBpicUXjg with yt-dlp (720p, 19 minutes, Blue Van Man, upload 2019-05-16). Raw MP4 remains in ignored build/video-reference. scripts/review_reference_video.py and scripts/select_reference_video.py succeeded: 114 ten-second samples, additional selected timestamps, five overview sheets and a 20-frame selected-tour sheet. Visually reviewed sheets. Useful downstairs displays, rear corridor/stairs and new upstairs furnishing evidence; no useful exterior street views identified in samples. Source metadata/hash/manifests retained separately; originals unchanged. See docs/VIDEO_REFERENCE_REVIEW.md. No Blender change, game build or push; rebuild hold remains.

## 2026-10-03 — Both video references applied in Blender v10
Sam requested many sharp views, approved the older upstairs decor and supplied Facebook video share/v/18ZXq1yVKY. Downloaded both references successfully with yt-dlp. YouTube dense tour extraction:471 additional native720p frames and95 sharpness candidates, all4 dense review sheets inspected. Facebook metadata:Great British Pub Crawl, upload2026-09-18,146.703s,1080x1920 portrait edit with landscape picture strip. Extracted294 half-second frames,25 portrait sheets and11 readable detail sheets; reviewed all11 detail sheets and opening/sample interview views. Twelve YouTube and8 Facebook native PNG crops inspected and packed; source stills/photos unchanged.
Live Blender scripts dress_video_pub_blender.py and dress_facebook_pub_blender.py returned statusok, saving v09 then pharmacie-video-details-v10.blend with live safety copies. Added353+101 meshes:upstairs banquettes, tables/stools/chairs, carpet, music posters, TV, darts, mirror, books/games, piano/radios; downstairs fridge, photo details, tap bank, dining groups;18 stair nosings. finish_video_dressing.py corrected bookcase overlap, integrated new objects with scale root, passed limited placement assertions. Rendered and inspected previews; temporary lights/cameras removed. See docs/VIDEO_INTERIOR_PASS.md and manifests. No BO3 compile/deployment/game closure or push; rebuild hold remains.


## 2026-10-03 — Street photo fronts and user preview correction in v12
Sam requested simple street-photo fronts, supplied six root Street View PNGs and blender preview.png, then reported fronts appeared too low. All six originals inspected. add_street_photo_fronts.py through live bridge saved v11:five opposite buildings with separate UV photo faces, simple backing/roof and three lamp posts, source hashes unchanged. User screenshot/live world bounds showed the broad grey strip was exposed4.2m-deep backing top/4.35m roof; photo face already covered pavement-to-eaves height. fix_street_fronts_and_neighbours.py returned statusok and saved pharmacie-street-details-v12.blend with live safety copy. Reduced backing/cap to0.32/0.40m, added five source-photo slate strips and three newly supplied pub-side neighbours. Left passage gap retained. Pixel quads/hashes/dimensions in v11/v12 manifests; originals packed unchanged. See docs/STREET_PHOTO_FRONTS.md. Default opener/latest README updated. No Radiant rebuild, engine verification, deployment, game closure or push.

## 2026-10-03 — Mini Market crop correction v13
User identified clipped Mini Market and confirmed the zoomed-out flat source. Expanded UV quad to (1010,238),(1770,260),(1750,840),(1030,840) on untouched opposite front zoomed out better view flat for texture.png. Includes roof, upstairs windows and full shopfront down to pavement; source car occlusion remains. Disabled redundant separate Mini Market slate strip. Live script fix_mini_market_front.py succeeded, saved pharmacie-street-details-v13.blend plus v12 safety copy. Rendered street-photo-fronts-v13.png and visually inspected. Default opener updated. No Radiant rebuild or push.

## 2026-10-03 — Further downstairs video detail v14/v15 and second scale test authorized
User requested as much reference detail as practical and then an updated Radiant scale test without zombies. Re-reviewed YouTube 06:35/07:29 full frames and Facebook detail sheet10. Added83+97 decorative meshes, four native crop derivatives, material-colour correction and procedural timber floor. Saved pharmacie-detailed-pub-v15.blend with live safety copies. V14 initially hit an unsupported MATERIAL viewport enum after geometry work; corrected to SOLID/TEXTURE, saved live result and fixed reproduction script. Rendered downstairs/right-side previews and inspected; temporary setup removed. See docs/SCALE_TEST_V15.md. Exported1375 meshes with79 image-linked objects. Prepared75 TIFF/GDT materials and separate zm_pharmacie_scale with outside spawns, expanded sky/player volumes and custom no-spawn callback. First build asset /update failed with stale duplicate GDT entries; backed-up /rebuild retry underway. No push.

First /rebuild build succeeded (compiler/navmesh, fresh lighting, both fastfile links), build/scale-test-build-retry.log. Final generator refinement preserves all single-quad decorative surfaces (189 patches; only1 unsupported object), with all8 player spawns outside. A normal /update again failed on stale duplicate index entries, so final build uses backed-up /rebuild; log build/scale-test-build-final-retry.log. Prior prototype maps untouched.

Final export audit found the angled outside passage was the only unsupported mesh; classified its horizontal concave slab for triangle-prism conversion. Export now contains1182 convex brushes,37 slab prisms,189 UV panels,0 skipped objects (63 curved/high-facet shapes simplified to bounds). Added stock EnableInvulnerability calls inside the no-spawn callback so scale inspection is protected from damage. Final build log build/scale-test-build-verified.log; intermediate successful build build/scale-test-build-final-retry.log.

## 2026-10-03 — Runtime script error and front threshold v16
Initial v15 scale package compiled/linked/deployed, but direct executable launch deferred to Steam's argument-confirmation dialog. User manually loaded map and supplied fatal GSC error: dev-only PrintLn outside developer block. Corrected generator to wrap diagnostic in /# ... #/; EnableInvulnerability is used outside devblocks in installed stock hostmigration script. User also requested removing front entrance floor gap. Added continuous solid threshold X4.18–6.85,Y-0.08–2.60,Z-0.27–0.003m overlapping pavement/interior; clear doorway stays1.996m. Saved live pharmacie-entrance-fixed-v16.blend plus safety copy. Export1376objects/1183convex brushes/37slab prisms/189UV patches/0skipped. Rebuild log build/scale-test-v16-build.log; runtime and traversal pending.

V16 official compiler/navmesh, fresh LED and both fastfile links succeeded (exit0), scale-test-v16-build.log. Complete zone/snd tree deployed with per-file hashes via launch-blender-test.ps1 -MapName zm_pharmacie_scale; backup before-blender-test-20261003-010241. Threshold preview rendered/inspected; temporary objects removed. Attempted relaunch; successful runtime not yet confirmed.

Steam console confirms launch Action12 is waiting for user response to ShowGameArgs for +set fs_game zm_pharmacie_scale +set logfile2 +devmap zm_pharmacie_scale. No game window yet; user may accept Steam's confirmation or load manually. No automatic game/UI input sent.

## 2026-10-03 — Photo-led street rebuild v17, opened in Blender
Sam requested opening Blender and updating the map to the expanded photo notes.
Existing unsaved Blender PID13784 had no MCP listener; a targeted console recovery
attempt did not establish a connection. Left that unsaved session intact and used
the saved v16 as baseline. Created isolated facade derivatives with
`python scripts/prepare_street_v17.py`: ten 1024x1024 RGB PNGs, source hashes verified.
Background Blender `--background assets/blender/pharmacie-entrance-fixed-v16.blend
--python scripts/rebuild_street_v17.py` saved 499 new objects / 22 building masses.
Initial runs stopped on unsupported MATERIAL viewport enum and a threshold check;
fixed enum and explicitly retained the threshold/rear landing from archived street.
Opened `assets/blender/pharmacie-street-rebuilt-v17.blend` visibly; its official MCP
connected and ran `refine_street_v17.py` live, saving a safety copy before refinements.

Neighbours attached to nominal pub edges; alley relocated outside Wreake with
rear connector; neighbour backs tapered to clear skewed pub. Added deeper pitched
roof/chimney street rows, upper bay relief, Post Office/Papermoon/Pasha/HM blockout,
Natural Wellbeing gable and separate lane, crossing/parking/build-out/junction and
unnamed placeholder fronts. Proposed gameplay anchors only, no stock entity changes.
Four camera previews rendered with `--background assets/blender/pharmacie-street-rebuilt-v17.blend
--python scripts/preview_street_v17.py`, exit0, and inspected. Corrected blocked
cameras, shared roof height, side brick projection and coplanar junction asphalt.
`--background assets/blender/pharmacie-street-rebuilt-v17.blend --python
scripts/check_street_v17.py` passed, exit0:1315 preserved pub meshes exact versus
v16, all44 reference hashes identical, threshold retained, old passage absent,
2.58m outer alley / 3m separate Natural Wellbeing lane. See STREET_REBUILD_V17.md,
street-rebuilt-v17-manifest.json, facade manifest and build/street-v17-check.json.
Default opener updated. Distances remain gameplay estimates; procedural brick
requires baking/replacement and photo occlusions remain. No Radiant conversion,
compiler/game verification, deployment, game installation write or push this pass.

## 2026-10-03 — Player recon, v18 cleanup and Zombies progression proposal
Sam requested a recon folder, programmatic player-perspective inspection, practical
Blender fixes before Radiant, full Blender control, then explicitly asked to push
the latest work and update project documentation. Saved dirty live v17 as local
`recon/v18/input-live-v17.blend` before edits. Safety snapshots remain local/ignored;
numbered v17/v18 milestones and screenshot/report evidence are tracked.

`scripts/recon_blender_players.py` run with background Blender on the live input
and final `assets/blender/pharmacie-player-cleanup-v18.blend`:36 viewpoints each,
72 saved1100x700 player-eye renders plus six contact sheets/offline comparison
gallery. Inspected all contact sheets and targeted full frames. Inspection uses
temporary fill/daylight, never saved into model. Final route sampling covers ten
chosen routes /572 samples at0.20m spacing; 0.35m radial and overhead/support rays
pass. Wider0.42m radius sensitivity caught an upper-arrival corner; tapered WC
outer-wall rear end20cm and rechecked all572 samples successfully. Prior sensitivity
evidence retained. These are preliminary mesh/ray checks, not BO3 collision/navmesh.

Live official Blender bridge ran `fix_player_recon_v18.py`, `light_recon_stairs_v18.py`,
`plan_zombies_blender_v18.py`, and `ease_upper_arrival_v18.py`, saving v18. Cleared
two aisle chairs; corrected15 mirrored image quads; raised rear floor join8mm;
replaced18 tall stair treads with26 at190/178mm rises in same footprint, retaining
rails/landings; added135mm platform intermediate step; closed upper ceiling/roof
with removable proxy cap; added four stair lights; eased upper-arrival corner.
New fixtures' inward face winding was found and corrected. Camera/route false
positives were resolved by actual doorway/left-bar approaches rather than removing
valid walls. Existing MEN/WOMEN divider remains solid with no connecting door.

Sam then asked to plan play/doors before Radiant. Added three proposed zones and
21 named Empty anchors: start in main pub, buy street at front or upstairs at stair
foot, linked rear/alley escape loop, provisional items/spawn entries/street limits.
Archived/unlinked competing old planning collections, including the old clearance
guide. No actual door locks, prices, game zones, prefab placements or scripts changed.
See `docs/ZOMBIES_PROGRESSION_V18.md` / `recon/v18/zombies-progression.json`.

Validation command: Blender `--background assets/blender/pharmacie-player-cleanup-v18.blend
--python scripts/check_player_recon_v18.py`. Report `recon/v18/validation.json`:
all44 original hashes unchanged; untouched pre-existing meshes retain exact world
vertices/faces; deliberate chair/connector/wall/stair edits excluded explicitly;
all60 new solid meshes closed with outward winding;72 images; final camera support
and route checks pass. First comparison rejected the intentionally retired clearance
guide; explicitly excluded that non-render planning guide, retaining architectural
checks. `python scripts/recon_gallery.py` / `recon_contact_sheets.py` build review
artifacts. Current source/opener and README, AGENTS, workflow/reference/asset notes
updated. Portable v16 facade input metadata now tracked for cross-machine reproduction.

Remaining: photo occlusions/Street View artefacts, detailed placeholder fronts and
roof geometry, exact gameplay/prefab sizes, collision design, progression door states,
exporter/material calibration and eventual compiler/game/co-op verification. No
Radiant conversion/deployment/game installation writes. User authorized repository
commit/push for this checkpoint; no map release or external publication requested.

## V18 separate Radiant playtest and corrective builds — 2026-10-03

Sam lifted conversion hold for a private test that plays as Zombies. New project
`zm_pharmacie_playtest` preserves all earlier maps and the unchanged v18 Blender.
Read `docs/PLAYTEST_V18.md` for details/limits and continuing runtime investigation.

Read-only live export command:
`build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/export_playtest_v18.py`.
Generator `python scripts/generate_playtest_v18.py` creates separate photo crops,
GDT/manifest, brushes/patches and stock Zombies progression. Evaluated geometry,
actual Base Color links and face material are inspected; unsupported image mapping
fails explicitly. Dominant solid material used for upstairs multi-material floor.
1,837 objects: 1,598 convex brushes,103 slab prisms,76 photo patches,60 boxed curved
details,123 reported thin/nonconvex omissions. All major structural floors,
ceilings, stairs and route connector remain; no source photos overwritten.

Three stock managed zones;750-point purchase links front street and rear alley
exits;1000-point stair gate;8 risers; stock rounds/damage. No invulnerability or
no-spawn callback. Quick Revive pub, box street,power upstairs. User additionally
requested weapons: stock RK5 500 pub,KRM750 rear stair approach,Kuda1250 street,
KN-44 1400 upstairs, using referenced stock weapon_upgrade prefabs. Interior
mounting wall planes measured with read-only Blender BVH raycasts. Prefab/game
content not copied into Git.

Build command:
`.\scripts\build-map.ps1 -ToolsRoot 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130' -MapName zm_pharmacie_playtest -AssetFolder assets/playtest-v18 -AssetNamespace pharmacie_pt18 -RebuildAssetDatabase`.
First full build `build/playtest-v18-build.log` exit0: compiler/ground navmesh,
fresh Radiant LED,both fastfile links. Initial deployment command:
`.\scripts\launch-blender-test.ps1 -ToolsRoot 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130' -GameRoot 'S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III' -MapName zm_pharmacie_playtest`.
Players/previous package backed up;entire zone/snd tree copied with per-filehash
verification. Steam deferred launch to its argument dialog; actual game PID24520
loaded map and registered both costs. Passive capture shows round4 combat/revive;
log exposed raised-platform `PATHFIND_FAILURE_UNREACHABLE` near X6.2,Y5.6.

Sam explicitly chose `Leave the controls to me` when recent input activity
required a game-automation skill check. No input,console commands,purchases,
movement or scripted control sent; passive C:\ffmpeg\ffmpeg.exe gfxcapture only.

First corrective build fixes legacy lights (`light=140` replaced by25 proper BO3
white_light omni definitions using radius/stops),raises photo storage resolution,
sets explicit material tiling/filtering,adds wall buys and shallow platform
navigation ramp. `/update` failed duplicate GDT registrations(exit1,
`build/playtest-v18-fix-build.log`); backed-up `/rebuild` succeeded(exit0,
`build/playtest-v18-fix-rebuild.log`) and complete package redeployed/launched.
Actual game PID25984; passive screenshot shows substantially brighter pub.
Sam reports texture improvement incomplete and absent door purchase prompts.

Approach-side trigger correction: move use-volume centres outside solid blockers,
explicit origins/cursor hint,stock DYNAMICPATH/spawnflags on clip models; cleaner
framed visible blockers. `build/playtest-v18-doors-build.log` exit0. Added optional
`--calibrate-uv` three reference panels (spans1,128,2048,same image/material);
`build/playtest-v18-uv-calibration-build.log` exit0,deployed/launched(actualPID24288).
Passive requested screenshot `build/bo3-current-screenshot.png` shows streaked
wall/diagnostic images and enlarged backwards text from oblique/rear view. Does
not establish full frontal UV normalization. AI still reports unreachable/invalid
goals when players stand on furniture or unsupported geometry; full AI/stairs
and co-op are not verified.

Sam added untouched `references/broken fronty textures.png`: Wreake Valley square
facade image readable while pub fascia lettering absent. Exported fascia bitmap
contains correct lettering but uses1024x128 storage. Next test makes all97
photo/colour TIFFs square,retains world panel aspect and original UV ordering,
uses new photo asset identities;diagnostic panels removed. This is a supported
scaling hypothesis,not a confirmed engine cause. `build/playtest-v18-square-build.log`
exit0. Restored nondegenerate 0/1 photo-patch lightmap corners matching our earlier
working photo exporter;latest build `build/playtest-v18-square-lightmap-build.log`
in progress at this entry. Original glazed-door crops contain only83x239 source
pixels each; enlarging cannot recover missing source detail. Game graphics read
only: TextureQuality1 drops a streamed mip,TextureFilter2 forces16x;no settings
changed. Custom images use streamable0.

No public release or Git push for this engine test. Current package must not be
overwritten while Sam's BO3 session is running;launcher explicitly checks this.
Continue final build/deploy and passive texture/purchase verification after exit.

Follow-up: square/lightmap build completed successfully (exit0, full compile,
fresh lighting and both links), then hash-verified deployment after BO3 exited.
Latest actual game PID15872. Sam confirms the Pharmacie entrance fascia/logo
now renders, but windows remain blurry/cropped relative to Blender. This confirms
an improvement, not full texture fidelity or verified door purchases.

Read-only live Blender inspection: all frontage photo panes use the unchanged
1024x751 JPG, Base Color only, Alpha1 and Transmission0. Their apparent interior
view/reflections are photographic, not real transparent glass. Render and active
UV layers both resolve to UV_Source_Photo for these panes; their mismatch is not
the cause here. Door crops contain approximately83x239 original pixels; main
display crops are approximately132x317. Resizing cannot create finer lettering.
Exporter now resolves render/explicit shader UV maps instead of assuming the
editor-selected layer, and rejects non-UV coordinate-node links. This safeguard
has not been rebuilt and is not claimed to correct these matching window UVs.
Passive capture build/window-texture-current.png shows the BO3 title screen,
so it supplies no evidence of the current window crop. Need a frontal runtime
view to distinguish mapping/occlusion from low photographic resolution before
another targeted texture build. No game inputs sent, Blender source unchanged.

Sam directed inspection of Steam screenshots. Found three originals under
C:/Program Files (x86)/Steam/userdata/111563730/760/remote/311210/screenshots;
unchanged copies retained in docs/build-results/playtest-v18/screenshots.
20261003153501_1.jpg shows the latest readable Pharmacie fascia, but visible
window lettering ends abruptly at pane edges. Remaining crop/mapping/framing
must be compared against Blender; low source resolution alone does not explain
all the visible truncation. Neighbouring full-facade image is substantially
clearer. The entrance gives a real view into the lit room through its opening;
this does not establish transparent glass material.
Earlier 20261003151524_1.jpg and 20261003151536_1.jpg show the UV diagnostic
panels and an explicit Hold F to clear Debris [Cost: 750] prompt. Street purchase
prompt is now screenshot-verified; successful removal and upstairs purchase
remain unverified. Earlier wall streaking belongs to the pre-square diagnostic
build and must not be attributed to the latest build without new evidence.

Sam subsequently confirms doors work. Treat reported door purchases as working;
automated route/co-op checks still unrun. User requests sharp textures. New pass
preserves full original photo bitmaps in square storage and original Blender UVs
for all image panes, removing per-pane crop/UV rebounding as an engine mismatch
variable. Photos remain source-resolution-limited; this is not invented detail.
Live frontal raycasts across both outer display panes hit their photo quads,
not oversized trim in Blender. Runtime mapping still needs comparison.

Added project-created 1024-square typeset drinks plaque PNG plus editable SVG
and provenance in assets/signage; exact observed wording, approximate border,
colour and serif font, rasterized from local Times New Roman without distributing
the font. Two thin non-solid overlays interpolate onto the source-photo plaque
regions of evaluated outer panes, offset12mm outward to avoid coincident faces.
Only test-map conversion receives overlays; saved v18 Blender remains unchanged.
Applied asset-pipeline skill for engine derivative preparation. Source checks
verify original photo UVs retained, two sharp plaques and source hash integrity;
full build underway in build/playtest-v18-sharp-window-build.log. Need actual
runtime to judge crop repair, clarity and overlay placement; no claim all textures
are fixed. Current user-controlled BO3 must exit before deployment.

Sharp-window build completed exit0: full cod2map/navmesh, fresh LED bake, map
link36.54s and locale link3.05s. Exact command: scripts/build-map.ps1 -ToolsRoot
'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130' -MapName
zm_pharmacie_playtest -AssetFolder assets/playtest-v18 -AssetNamespace
pharmacie_pt18 -RebuildAssetDatabase (log copied to
docs/build-results/playtest-v18/sharp-window-build.log). Source checks pass,
44 original hashes unchanged,87 referenced square images,78 photo patches.
Game was absent, so scripts/launch-blender-test.ps1 deployed the complete zone
tree with per-file hashes and relaunched the test (requested PID25728,
14:54:12UTC). Backup build/before-blender-test-20261003-155410. User retains
controls; latest rendering remains unverified until inspected in game.

Sam confirms the sharp-window build looks good; continuing with explicit sharp
static signage where supported by references. Latest Steam screenshots
20261003163211_1.jpg confirm uncropped frontage/plaques;20261003163248_1.jpg shows
the bar front incorrectly includes upper shelving. Live Blender UVs correctly
separate drawer crop(50,745,1900,1230),backbar normalized(.205,.215,.985,.585),
and TV(.435,.262,.575,.402). Engine crop rendering still mismatched, so converted
these three regions into separate PNGs with full-panel UVs and separate hashed
materials. Crops/provenance in assets/bar-regions/manifest.json; tests compare
each derivative pixel-for-pixel to its specified unchanged original crop.

Implemented user-requested wooden crossing wall purchase:1250points,stock
zombie_debris with use volumes on both sides,linked removable wood and dynamic
navigation clip. Replaced old static X30 end wall; street extends toX60. New
crossing_zone covers road/pavements X30..60 and existing3m Post Office/Natural
Wellbeing lane X45..48,Y-30..-13. Adds3 zone-gated risers,3 lights,new zone
adjacency pt18_crossing_open; shop interiors stay scenery. Far/lane ends bounded
and invisible clips prevent leaving supported pavement or bypassing gate via
placeholder buildings. Lane is a dead end, not a new loop; balance and runtime
pursuit pending. Source checks pass:5 use triggers,4 linked collision models,
3 gate targets,89 square assets,44 original reference hashes unchanged.
Full build running:build/playtest-v18-crossing-bar-build.log. No game controls
sent; cannot deploy while Sam's BO3 session is active.

Crossing/bar full build exit0: cod2map/navmesh,fresh lighting,map link19.20s,
locale link3.86s. Log copied docs/build-results/playtest-v18/crossing-bar-build.log;
export report refreshed. Existing BO3 PID21404 still active, so no deployment.
Requested session closure before hash-verified deployment; user controls retained.
Current game still runs the successful sharp-window version. New purchase,
zombie crossing pursuit and separated bar appearance are not runtime-verified.

Sam requested notes in the repo to pick up later. Saved consolidated handover
docs/HANDOVER_2026-10-03.md and linked it from AGENTS.md. User-confirmed improved
textures/working doors distinguished from built-but-undeployed crossing/bar
fixes; exact resume command, asset provenance, source-vs-conversion differences,
remaining runtime checks and user-controlled game constraint recorded. No new
deployment, game input, Git commit/push or public release for this notes request.
Final status also shows assets/blender/pharmacie-player-cleanup-v18.blend modified.
Our engine scripts never saved it; origin of that change is unresolved. Handover
explicitly records this and instructs preserving the working copy.

Sam authorized pushing the latest work and requested a Blender screenshot page.
Added docs/BLENDER_RENDER_GALLERY.md with12 saved v18 Cycles views, full-size
links and explicit distinction from subsequent engine-only additions. README
links gallery/current handover. All gallery targets exist; source checks pass
with44 original hashes intact. Obsolete generated TIFFs moved into ignored
build/obsolete-playtest-assets-before-push, preserving local copies; only89
currently referenced textures retained in asset folder. Includes existing
modified v18 .blend as requested latest work; our conversion scripts did not
save it. Git commit/push follows. Pending crossing/bar deployment remains
pending; no game takeover, installation change or release publishing here.

Sam requested more Blender gallery shots. Expanded docs/BLENDER_RENDER_GALLERY.md from12 to36 saved v18 renders, adding24 entrance, platform, bar approaches, service/rear rooms, complete stairs/upstairs, alley/rear connection and wider street views. All added image targets verified. These are existing Cycles inspection renders, not newly rendered or current BO3 screenshots. No model/game changes. Gallery update committed/pushed under existing authorization.

