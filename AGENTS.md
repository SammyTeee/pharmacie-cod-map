[Latest street vehicles, furniture, opposite shopfront detail and videos](docs/STREET_FRONTAGES_V32.md).

Latest Blender checkpoint: `assets/blender/pharmacie-street-frontages-v32.blend`.
V31 vehicles and bounded street, V32 frontage relief/furniture/crossing approaches;
v30 enclosed rear alley and prior pub/Taraj work retained. Zombies first,
possible PvP later. Engine unchanged; Blender route checks are not game tests.
Sam explicitly requested pushing the completed mapping/media pass on 2026-10-04,
superseding the earlier no-push instruction. Skeleton work is deferred.

[Latest rear-alley mapping and review](docs/REAR_ALLEY_V30.md) — read first.

## User-approved mapping approach — 2026-10-04

Sam strongly approved the v30 rear-alley preview and explicitly asked to carry
its approach into future changes. Follow the requested layout, then develop it
as a deliberate CoD Zombies space: enclosing walls and continuous floors,
clear escape routes, useful doorways/boundaries, plausible barricade locations,
and restrained service props/lighting that keep circulation clear. Resolve
empty or unfinished areas as coherent spaces rather than adding decoration alone.
Use v30 as the quality reference. Preserve recognizable venue architecture and
explicit user corrections; record gameplay adaptations separately from observed
real-world facts. Show substantial changes with matched before/after previews
and clear highlights; a compact labelled video is useful where practical.
Keep Blender geometry checks distinct from implemented engine behavior and
actual game verification. This preference does not authorize engine deployment
or override existing game-control/publishing restrictions.

Latest checkpoint: `assets/blender/pharmacie-zombies-alley-v30.blend`.
Enclosed narrow rear alley, boundary/infill walls, ground backing, wall-side
utilities, enclosed barricade pocket, parked rear-door leaf and closed bar-side
Staff Only door. V29 street/Taraj work retained. Engine remains unchanged;
new door/barricade/spawn markers are proposals. Before/after highlight video:
`recon/v30/index.html`. Wider-radius Blender routes pass, not BO3 navigation.

[Current street detail and recovery notes](docs/SYSTON_DETAIL_V29.md).

Latest checkpoint: `assets/blender/pharmacie-syston-detail-v29.blend`.
Sam wants individual shops and the streetscape detailed to the Pharmacie standard,
including pavements/kerbs/road markings. V27–v29 are an initial detail pass, not
completion of that broader target. Firefox reference collection is authorised.
Preserve approved building placement and pub/Taraj interiors. Blender-only.

[Taraj renders and placement plan](docs/TARAJ_V24.md) — earlier checkpoint.

Latest complete Blender checkpoint: `assets/blender/pharmacie-taraj-opposite-v24.blend`. Melton Road, roundabout, rough street buildings and the photo-led Taraj exterior are saved; pub/shopfront/fridge work is retained. See [3D shopfront gallery](docs/3D_SHOPFRONT_GALLERY.md). New geometry is Blender-only; engine deployment remains unchanged.

# Project instructions

Before future Radiant conversion/gameplay placement, read
`docs/RADIANT_CONVERSION_PLAYBOOK.md`, `docs/RADIANT_GAMEPLAY_PLACEMENT_PLAN.md`,
`docs/RADIANT_STOCK_GAMEPLAY_AUDIT.md` and `research/radiant/README.md`.
The offline BO3 tutorial snapshot is source-linked/licensed, with original HTML,
readable text and hashes. Check tutorial recipes against installed stock and
actual runtime. Legacy v18 coordinates require reconciliation with current
Blender geometry. The existing outside box prefab is static base/rubble only;
functional chest entities are missing. Do not call it a working mystery box.

This repository is a Call of Duty: Black Ops III custom Zombies map inspired by The Pharmacie Arms in Syston, Leicestershire. The user is new to mapping and wants agents to do as much of the implementation as practical, explaining important choices plainly.

## Start here

Latest Blender checkpoint: `assets/blender/pharmacie-shopfronts-v19.blend`.
Read `docs/SHOPFRONTS_V19.md`: three neighbouring shopfronts modelled, with
user-requested upstairs windows copied at the pub's scale. V18 engine test and
pending crossing/bar package remain separate; v19 has no engine conversion yet.

Latest handover: read `docs/HANDOVER_2026-10-03.md` before resuming. Sharp-window
result and existing doors are user-confirmed; crossing-wall/bar-region package
is built but not deployed. User retains BO3 controls. Working-tree changes are
being committed/pushed at Sam's request; check Git status/history for completion.

1. Read `MODLOG.md` for current state and next actions.
2. Read `MODDING_PLAN.md` for the game/toolchain route and unresolved environment checks.
3. Read `docs/THE_PHARMACIE_MAP_NOTES.md` for photo-based observations and blockout guidance.
4. Read `docs/PHOTO_ASSET_PLAN.md` and `references/pharmacie-syston/README.md` before editing or converting reference images.
5. Read `docs/RADIANT_WORKFLOW.md` before starting Radiant or automating map geometry/build steps.

Keep those notes current when new evidence, decisions, or build results appear. Distinguish observed facts from guesses and unresolved questions.

## Project priorities

Current direction (2026-10-03): Sam authorized the separate `zm_pharmacie_playtest`
Radiant conversion and private game test. Read `docs/PLAYTEST_V18.md` for current
builds, texture calibration and missing purchase-prompt investigation. User chose
to keep game controls; use passive captures/logs and do not drive BO3.
Latest Blender file is `assets/blender/pharmacie-player-cleanup-v18.blend`.
Read `recon/v18/README.md` and `docs/ZOMBIES_PROGRESSION_V18.md` before new edits.
Progression is implemented in the separate test, but door purchases, traversal,
AI pursuit, wall buys and co-op need individual runtime verification.
Do not treat Blender ray checks or a successful build as runtime validation.

- First goal: a small, playable cooperative Zombies blockout using the official BO3 Mod Tools and Radiant, with player spawns, playable space, zombie routes, and round logic. Use stock assets and simple geometry first.
- Use the BO3 Zombies map naming/template conventions (normally a lowercase `zm_` name); settle the name before creating tool-generated project files.
- Build the recognizable pub from the outside inward: frontage, long main room, bar wall, pharmacy-ad display wall, then side spaces and bespoke props.
- Add the Noseley boss after the basic map loads and plays. Use stock placeholders for the first encounter and investigate models/animation requirements before generating character assets.
- Do not start a Gaussian splat as the map geometry. Photos are references and possible texture sources; Radiant geometry, collision, and pathing are required for gameplay.

## Reference photos and assets

- Treat files in `references/pharmacie-syston/` as source references. Never overwrite, recompress, crop, or rename a source photo; create a separate derivative and record how it was made.
- `great for texture.avif` (1973×1227) is the leading candidate for a custom, non-tiling feature wall panel: it is nearly head-on and captures the vintage-ad collage and illuminated display cases. It still needs inspection/cropping and game-format conversion.
- `textures wall.jpg` and `53737352757_c7dacdf5d8_c.jpg` are supporting wall-art references. `bar front.jpg` is a strong front-on bar/cabinet modelling reference. Room-wide photos are for layout and prop placement, not direct wall textures.
- Preserve provenance in `references/pharmacie-syston/README.md`. Keep game-ready derivatives in a separate assets folder with a small manifest (source, crop/edits, dimensions, target format, and status).
- Study stock BO3 textures and the actual Mod Tools asset path before committing to dimensions, compression, or final image format. A photo is not automatically a game-ready texture.
- Do not include other people's photos or game files in a distributed map without checking rights. Never commit extracted or copied game assets.

## Safe work and verification

- Game target: Call of Duty: Black Ops III on Steam. The game is being downloaded to the Steam library; confirm the completed install path before using the tools. Keep source and generated project work in this repository or a dedicated tools workspace unless the user directs otherwise.
- Do not install Mod Tools into the game folder, change game settings, or write/replace files in the game installation without the user's approval. Prefer the official Steam Mod Tools and their normal project output locations.
- Work offline/single-player only. Do not build cheats or touch public multiplayer.
- Do not publish, upload, or push changes unless the user asks.
- Verify any map change with the actual compiler/game once the Mod Tools are available. Record the exact command, result, and any failure in `MODLOG.md`; never claim an unrun build works.
- Do not delete user reference files. Keep original photo names and contents intact.

## Instructions for agent harnesses

`AGENTS.md` is the shared source of project instructions for Codex and OpenClaw. Claude Code should also load it through the root `CLAUDE.md` import. Other agents should read this file and the four project notes listed above before making changes.
