# Project instructions

This repository is a Call of Duty: Black Ops III custom Zombies map inspired by The Pharmacie Arms in Syston, Leicestershire. The user is new to mapping and wants agents to do as much of the implementation as practical, explaining important choices plainly.

## Start here

1. Read `MODLOG.md` for current state and next actions.
2. Read `MODDING_PLAN.md` for the game/toolchain route and unresolved environment checks.
3. Read `docs/THE_PHARMACIE_MAP_NOTES.md` for photo-based observations and blockout guidance.
4. Read `docs/PHOTO_ASSET_PLAN.md` and `references/pharmacie-syston/README.md` before editing or converting reference images.

Keep those notes current when new evidence, decisions, or build results appear. Distinguish observed facts from guesses and unresolved questions.

## Project priorities

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
