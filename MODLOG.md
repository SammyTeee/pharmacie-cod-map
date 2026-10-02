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
- Created the first project in the Mod Tools launcher on 2026-10-02 using the Zombies map setup: `zm_pharmacie`. It generated `map_source\zm\zm_pharmacie.map` and `usermaps\zm_pharmacie\scripts\zm\zm_pharmacie.gsc` / `.csc`, confirming the ZM template rather than an MP-only project. No build has run yet. The launcher's map list contains `zm_pharmacie` plus stock maps after creation.
- User wants the editor/game visible beside the 2K desktop. Radiant is a resizable app window; use BO3 at 1600×900 windowed for game checks, without changing desktop resolution.
- BO3/Steam source notes: Steam BO3 page https://store.steampowered.com/app/311210/Call_of_Duty_Black_Ops_III/ ; Mod Tools hub https://steamcommunity.com/app/455130 ; mapping guide https://steamcommunity.com/sharedfiles/filedetails/?id=3737598953 .
- No map source, project scripts, compiled map, or game-ready custom texture has been created yet.
- The installed Universal Modder plugin is a helper for reconnaissance/asset preparation; it does not replace Radiant or the BO3 Mod Tools build pipeline.
- Handoff portability: paths under `S:\SteamLibrary` and `C:\Users\sam` above are observations from Sam's PC, not portable project paths. On another PC, install BO3 and app 455130 through Steam and locate the actual library. The generated `zm_pharmacie` map/scripts currently reside in Sam's Mod Tools directory and are not tracked in this repository; this repo currently provides project notes and photo references, not a ready-to-open map project. Copy/transfer the generated project before expecting to continue the map itself.

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
- [ ] Open Radiant, shape a basic long pub room, then build it and verify multiplayer Zombies in a 1600×900 window; keep optional DLC disabled unless a needed asset is unavailable.
- [ ] Build and launch the unmodified template/blockout; record exact steps and failures.
- [ ] Replace one wall area with a custom photo-derived material and verify in game.
- [ ] Expand the pub layout, then implement and test the Noseley boss.

## Next action

Open `zm_pharmacie` in Radiant, create the first playable pub-room blockout, and build it. Then prepare it for BO3 co-op testing at 1600×900 windowed; ask before copying generated map files into the game install. Keep all stock tool sources and pub photos unchanged.
