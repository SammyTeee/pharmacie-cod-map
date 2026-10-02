# Mod log

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
