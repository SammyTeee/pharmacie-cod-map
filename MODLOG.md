# Mod log

## Project

- Goal: create a World at War custom Zombies map based on The Pharmacie Arms in Syston, with a later boss inspired by Noseley.
- Game install: `S:\SteamLibrary\steamapps\common\Call of Duty World at War`.
- Local project/repository: `C:\Users\sam\pharmacie-cod-map` (GitHub remote is configured as `git@github.com:SammyTeee/pharmacie-cod-map.git`).
- User is new to map-making and wants agents to carry most implementation work, keep clear handover notes, and ask when real choices or permission are needed.

## Chosen route

Use the community-supported World at War Mod Tools (Radiant, Asset Manager, compile/light/link/fastfile workflow) for a single-player Zombies map. This is the native map-authoring path and supports the required geometry, collision, navigation, and Zombies scripting. Do not attempt to use a Gaussian splat as the playable level.

Start with a stock-asset blockout and a working Zombies template, then add pub-specific geometry/textures/props, and only then build the Noseley boss. The intended map name must use the `nazi_zombie_` prefix; final suffix not chosen.

## Environment observations

- `CoDWaW.exe` exists at the stated Steam path. Its Windows file/product version properties reported `1.7` / `1.7x`.
- The adjacent `version.inf` reports `ExtVersion=1.6`; this differs from the executable properties and should be resolved by checking the running game's displayed version before compiling.
- A separate Mod Tools directory was not visible in `S:\SteamLibrary\steamapps\common` during the initial check. Verify Steam Tools library/install state before assuming Radiant or the compiler is available.
- No map source, project scripts, compiled map, or game-ready custom texture has been created yet.
- The installed Universal Modder plugin is a helper for reconnaissance/asset preparation; it does not replace Radiant or the WaW Mod Tools map compiler.

## References and asset decisions

- Pub photo set and provenance: `references/pharmacie-syston/README.md`.
- The locally supplied `great for texture.avif` is 1973×1227 and visually shows a near-frontal run of vintage pharmacy advertisements, display cases, bottles, and medical objects. It is the best current source for one custom feature-wall panel. Keep the original untouched; crop/straighten and convert a derivative only after establishing the WaW asset pipeline.
- `bar front.jpg` is a clear frontal view of the dark cabinet-front bar; use it to model a bar prop and possibly as a carefully cropped front-face texture.
- Wide interior views show a long, narrow principal room with the street entrance/windows at one end, bar at the far end, central tables, perimeter seating, and decorated display walls. Exact dimensions and the complete upstairs/side-room layout remain unknown.
- Use photos as both direct texture sources (selected flat wall panels) and modelling/layout references. Do not flatten the whole pub into a photograph: retain 3D geometry for collision, circulation, doors, the bar, and significant objects.

## Progress

- [x] Connected Git repository to the requested GitHub remote.
- [x] Created a local pub-reference folder with sourced exterior images and source links.
- [x] User added pub frontage, room, bar, display-wall, and skeleton photographs to the reference folder.
- [x] Wrote shared agent instructions and initial map/photo notes.
- [ ] Confirm/install the separate official WaW Mod Tools (ask before writing into the game directory).
- [ ] Confirm the running game version and discover the installed Mod Tools version/build workflow.
- [ ] Choose final map suffix and create a template Zombies project.
- [ ] Build and launch the unmodified template/blockout; record exact steps and failures.
- [ ] Replace one wall area with a custom photo-derived material and verify in game.
- [ ] Expand the pub layout, then implement and test the Noseley boss.

## Next action

Check whether the official “Call of Duty: World at War Mod Tools” Steam tool is already installed and identify its path/version. Then use the template workflow to produce the smallest playable Zombies test map. Before first compile, resolve the game-version discrepancy and record the map source/output/mod paths.
