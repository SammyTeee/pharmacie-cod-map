# The Pharmacie Arms: BO3 Zombies Map

A Call of Duty: Black Ops III custom Zombies map inspired by The Pharmacie Arms in Syston, Leicestershire. The first milestone is a small cooperative playable blockout; the Noseley-inspired boss and detailed pub dressing come later.

## Current status

- The project uses the official BO3 Mod Tools and the Zombies template named `zm_pharmacie`.
- A code-authored first-pass blockout is in `map_source/zm/zm_pharmacie.map`, with its preserved BO3-generated template, repeatable generator, and GSC/CSC/zone source files in this repository.
- The first geometry version compiled and linked successfully with BO3 Mod Tools on Sam's PC. The current layout iteration follows Sam's Paint sketch; rebuild results for that iteration are recorded in `MODLOG.md`.
- The map has not yet been launched in BO3. Compiled `.d3dbsp`, navmesh, and `.ff` outputs live in Sam's local Mod Tools installation and are not tracked here.
- The reference photos are preserved under `references/pharmacie-syston/`. Do not overwrite them or distribute them in a released map without checking rights.

## Continue on another computer

1. Install Call of Duty: Black Ops III and the official **Call of Duty: Black Ops III - Mod Tools** through Steam (tool app 455130).
2. Find the Steam library paths on that computer; paths recorded elsewhere in these notes are specific to Sam's PC.
3. Clone this repository and install Python 3.11+; regenerate with `python scripts/generate_blockout.py` if needed.
4. Copy the tracked map source and `usermaps/zm_pharmacie` project source into that PC's Mod Tools tree, preserving the original generated template as a rollback/reference.
5. Compile and link with that PC's official Mod Tools Launcher, inspect the layout in Radiant, then run the map from the BO3 Mods menu for local/private testing.
6. Record exact build/test steps and results in `MODLOG.md`; generated outputs and absolute paths are machine-specific.

Keep work offline/private. Do not edit stock tool maps or game files. Use simple geometry and stock assets for the first blockout; add photo-derived materials only after checking the BO3 material pipeline. See `AGENTS.md` for project rules.

## Project notes

- [Mod log and next action](MODLOG.md)
- [BO3 setup and handoff plan](MODDING_PLAN.md)
- [Radiant workflow and automation findings](docs/RADIANT_WORKFLOW.md)
- [Blockout layout and clean plan](docs/BLOCKOUT_LAYOUT.md)
- [Editable SVG floor plan](docs/pharmacie-layout-v1.svg)
- [Interactive layout editor](docs/layout-editor.html) (open in a browser to drag and label items)
- [Photo-based layout observations](docs/THE_PHARMACIE_MAP_NOTES.md)
- [Photo gallery with previews and descriptions](docs/PHOTO_GALLERY.md)
- [Photo-to-game-asset plan](docs/PHOTO_ASSET_PLAN.md)
- [Photo sources and provenance](references/pharmacie-syston/README.md)

## Photo previews

These reference photos guide the exterior, room layout, bar, and pharmacy feature wall. Select a preview to open the full image; see the [photo gallery](docs/PHOTO_GALLERY.md) for all collected references and descriptions.

| Street frontage | Main room | Bar front | Pharmacy feature wall |
|---|---|---|---|
| [![Pub frontage](references/pharmacie-syston/pharmacie-arms-syston-2.jpg)](references/pharmacie-syston/pharmacie-arms-syston-2.jpg) | [![Long main room](references/pharmacie-syston/pharmacie-arms-syston-1.jpg)](references/pharmacie-syston/pharmacie-arms-syston-1.jpg) | [![Bar front](<references/pharmacie-syston/bar%20front.jpg>)](<references/pharmacie-syston/bar%20front.jpg>) | [![Feature wall preview](references/pharmacie-syston/_great-for-texture-preview.jpg)](<references/pharmacie-syston/great%20for%20texture.avif>) |

## Goal for the first playable version

Build the main pub room with player spawns, zombie routes, round logic, and enough space to move and fight. Verify those basics before expanding into side rooms, custom textures, detailed props, or the boss encounter.
