# The Pharmacie Arms: BO3 Zombies Map

A Call of Duty: Black Ops III custom Zombies map inspired by The Pharmacie Arms in Syston, Leicestershire. The first milestone is a small cooperative playable blockout; the Noseley-inspired boss and detailed pub dressing come later.

## Current status

- Latest saved version: [pharmacie-entrance-fixed-v16.blend](assets/blender/pharmacie-entrance-fixed-v16.blend), with a continuous front threshold, eight street photo fronts and another 180 downstairs decorative objects. [Downstairs](assets/blender/video-downstairs-v15.png), [display wall](assets/blender/video-right-displays-v15.png), [upstairs](assets/blender/video-upstairs-v10.png). A separate zombie-free second scale test is `zm_pharmacie_scale`; see [conversion and results](docs/SCALE_TEST_V15.md).

- **Current Blender edits:** [pharmacie-layout-fixed-v07.blend](assets/blender/pharmacie-layout-fixed-v07.blend) includes the enlarged skewed pub/street and all seven layout-review fixes: clearer seating/bar approaches, usable furniture heights, supported platform seating, corrected outside passage and upstairs stairwell guards. Spawn/zombie locations are planning markers. [Interior preview](assets/blender/layout-fixed-interior-v07.png), [upstairs preview](assets/blender/layout-fixed-upstairs-v07.png). The next Radiant rebuild is on hold at Sam's request; BO3 still uses the v03 conversion below.

- **Latest modelling workspace:** open [pharmacie-photo-interior-v03.blend](assets/blender/pharmacie-photo-interior-v03.blend) in Blender. It includes the photo-based frontage, both floor layouts, corrected rear L-shaped stairs and 34 grouped interior furnishings. The default interior view includes the finished frontage. A separate [Blender-to-Radiant test](docs/BLENDER_TO_RADIANT_TEST.md), `zm_pharmacie_blender`, now compiles and loads in BO3; gameplay routes and collision still need inspection. The existing playable BO3 source below is an earlier prototype.
- Read [Blender workflow](docs/BLENDER_WORKFLOW.md) and [photo/object placement plan](docs/PHOTO_OBJECT_PLACEMENT_PLAN.md). The `.blend` packs its reference images; [current preview](assets/blender/photo-interior-with-front-v03.png) shows the saved arrangement. Frontage is estimated at 7m; heights and furniture positions remain provisional.

- The project uses the official BO3 Mod Tools and the Zombies template named `zm_pharmacie`.
- A code-authored first-pass blockout is in `map_source/zm/zm_pharmacie.map`, with its preserved BO3-generated template, repeatable generator, and GSC/CSC/zone source files in this repository.
- The first geometry version compiled and linked successfully with BO3 Mod Tools on Sam's PC. The current layout iteration follows Sam's Paint sketch; rebuild results for that iteration are recorded in `MODLOG.md`.
- The saved SVG layout now compiles, lights, links, and plays in BO3. The first local session reached **2 rounds survived and 6 kills** on 2026-10-02. Full route coverage and co-op still need verification. Compiled outputs are local and not tracked here.
- Latest source adds L-shaped stairs to an empty upstairs room, photo frontage with a real doorway, photo bar and pharmacy walls, a transparent skeleton/chair, and eight tables with sixteen chairs. The photo build compiled and loaded; [frontage screenshot](docs/screenshots/photo-frontage-first-game.png) confirms the front texture. Lighting/exposure is currently poor; stairs, other panels and co-op need individual runtime checks.
- The reference photos are preserved under `references/pharmacie-syston/`. Do not overwrite them or distribute them in a released map without checking rights.

## Continue on another computer

1. Install Call of Duty: Black Ops III and the official **Call of Duty: Black Ops III - Mod Tools** through Steam (tool app 455130).
2. Find the Steam library paths on that computer; paths recorded elsewhere in these notes are specific to Sam's PC.
3. Clone/pull this repository. The map, TIFF inputs, custom GDT, photo references and skeleton derivative are included. You can build these directly; to regenerate, install Python 3.11+ and `python -m pip install -r requirements.txt`, then run `python scripts/prepare_photo_assets.py` followed by `python scripts/generate_blockout.py`.
4. From the repo root in PowerShell, run `./scripts/build-map.ps1 -ToolsRoot '<your Steam library>\steamapps\common\Call of Duty Black Ops III 455130'`. Use the actual folder containing `bin/Radiant_modtools.exe`; some installations may use a different folder name. The script stages the map, complete Zombies project source, TIFFs and GDT into the tools workspace, registers the assets, then compiles, lights and links. It does not deploy to the retail game. See [photo material workflow](docs/PHOTO_MATERIAL_WORKFLOW.md) for the asset database repair if needed.
5. Inspect the layout in Radiant. For testing, close BO3, back up any existing `usermaps/zm_pharmacie` package in the retail game, and copy the built `zone` folder from the tools' `usermaps/zm_pharmacie` into the game's `usermaps/zm_pharmacie`. Then launch the game executable from its game directory with `+set fs_game zm_pharmacie +set logfile 2 +devmap zm_pharmacie` for a solo test. Ask your machine's owner before an agent writes into the game installation or takes over input. Do not change desktop resolution.
6. Record exact build/test steps and results in `MODLOG.md`; generated outputs and absolute paths are machine-specific.

Keep work offline/private. Do not edit stock tool maps or game files. Read `AGENTS.md` and `MODLOG.md` first. Brownie's next priority is lighting/exposure/probes (dark photo panels and white weapon/sky), followed by testing the L-shaped stairs and zombie pursuit upstairs. The original photos remain unchanged; distribution rights remain unresolved.

## Project notes

- [Mod log and next action](MODLOG.md)
- [BO3 setup and handoff plan](MODDING_PLAN.md)
- [Radiant workflow and automation findings](docs/RADIANT_WORKFLOW.md)
- [Blockout layout and clean plan](docs/BLOCKOUT_LAYOUT.md)
- [Editable SVG floor plan](docs/pharmacie-layout-v1.svg)
- [Sam's saved layout](references/pharmacie-syston/pharmacie-layout.svg) and [SVG-to-map implementation notes](docs/SVG_BLOCKOUT.md)
- [Interactive layout editor](docs/layout-editor.html) (open in a browser to drag and label items)
- [Photo-based layout observations](docs/THE_PHARMACIE_MAP_NOTES.md)
- [Photo gallery with previews and descriptions](docs/PHOTO_GALLERY.md)
- [Photo-to-game-asset plan](docs/PHOTO_ASSET_PLAN.md)
- [Latest photo materials, reproduction steps and build gotchas](docs/PHOTO_MATERIAL_WORKFLOW.md)
- [Successful photo-build log](docs/build-results/photo-pass-verified-build.log)
- [Photo sources and provenance](references/pharmacie-syston/README.md)

## Photo previews

These reference photos guide the exterior, room layout, bar, and pharmacy feature wall. Select a preview to open the full image; see the [photo gallery](docs/PHOTO_GALLERY.md) for all collected references and descriptions.

| Street frontage | Main room | Bar front | Pharmacy feature wall |
|---|---|---|---|
| [![Pub frontage](references/pharmacie-syston/pharmacie-arms-syston-2.jpg)](references/pharmacie-syston/pharmacie-arms-syston-2.jpg) | [![Long main room](references/pharmacie-syston/pharmacie-arms-syston-1.jpg)](references/pharmacie-syston/pharmacie-arms-syston-1.jpg) | [![Bar front](<references/pharmacie-syston/bar%20front.jpg>)](<references/pharmacie-syston/bar%20front.jpg>) | [![Feature wall preview](references/pharmacie-syston/_great-for-texture-preview.jpg)](<references/pharmacie-syston/great%20for%20texture.avif>) |

## Goal for the first playable version

Build the main pub room with player spawns, zombie routes, round logic, and enough space to move and fight. Verify those basics before expanding into side rooms, custom textures, detailed props, or the boss encounter.

## Credits and source scope

Built with Codex assistance and official BO3 Mod Tools. The transparent skeleton/chair derivative was isolated with OpenAI image generation; other photo derivatives use deterministic format conversion and UV crops. Sources and provenance are recorded in the reference README and `assets/photos/manifest.json`.

This is an in-progress source handover, not a packaged Workshop release. Local profiles/backups, asset databases/caches, and compiled game packages remain ignored under `build/` or in the installations; rebuild those on your own machine. The repository includes project source, reference/derived art, screenshots and selected text build evidence.
