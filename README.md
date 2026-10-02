# The Pharmacie Arms: BO3 Zombies Map

A Call of Duty: Black Ops III custom Zombies map inspired by The Pharmacie Arms in Syston, Leicestershire. The first milestone is a small cooperative playable blockout; the Noseley-inspired boss and detailed pub dressing come later.

## Current status

- The project uses the official BO3 Mod Tools and the Zombies template named `zm_pharmacie`.
- The template was created in Radiant's Mod Tools launcher, but no map build or in-game test has been completed.
- The actual `.map` and GSC/CSC project files currently live in Sam's Mod Tools installation and are **not included in this repository**. This repo contains project notes and reference photos, not a ready-to-build map project. Arrange to transfer those generated files or recreate the template before continuing on another computer.
- The reference photos are preserved under `references/pharmacie-syston/`. Do not overwrite them or distribute them in a released map without checking rights.

## Continue on another computer

1. Install Call of Duty: Black Ops III and the official **Call of Duty: Black Ops III - Mod Tools** through Steam (tool app 455130).
2. Find the Steam library paths on that computer; paths recorded elsewhere in these notes are specific to Sam's PC.
3. Get the generated `zm_pharmacie` map and scripts from Sam, or create a Zombies map template with that name in the Mod Tools launcher.
4. Open the map in Radiant, make a simple long pub-room blockout with a clear central lane, then build and test it.
5. Record the exact build/test steps and results in `MODLOG.md`.

Keep work offline/private. Do not edit stock tool maps or game files. Use simple geometry and stock assets for the first blockout; add photo-derived materials only after checking the BO3 material pipeline. See `AGENTS.md` for project rules.

## Project notes

- [Mod log and next action](MODLOG.md)
- [BO3 setup and handoff plan](MODDING_PLAN.md)
- [Photo-based layout observations](docs/THE_PHARMACIE_MAP_NOTES.md)
- [Photo-to-game-asset plan](docs/PHOTO_ASSET_PLAN.md)
- [Photo sources and provenance](references/pharmacie-syston/README.md)

## Goal for the first playable version

Build the main pub room with player spawns, zombie routes, round logic, and enough space to move and fight. Verify those basics before expanding into side rooms, custom textures, detailed props, or the boss encounter.
