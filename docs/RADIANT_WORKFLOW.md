# BO3 Radiant and automation notes

**Research update, 2026-10-04:** before the next conversion, read the
[conversion playbook](RADIANT_CONVERSION_PLAYBOOK.md),
[detailed placement plan](RADIANT_GAMEPLAY_PLACEMENT_PLAN.md),
[installed-stock audit](RADIANT_STOCK_GAMEPLAY_AUDIT.md) and
[offline tutorial packet](../research/radiant/README.md). Current documented
Blender source is [v30](REAR_ALLEY_V30.md); v18 entity anchors/volumes are legacy
data to reconcile with it. This research did not export/build/deploy a map.
The stock audit corrects an older assumption: the existing outside mystery-box
reference is its static base only; functional chest-use/zbarrier assembly is
missing. Older latest-source and verification statements below are historical.

Latest authorized test: [PLAYTEST_V18.md](PLAYTEST_V18.md), `zm_pharmacie_playtest`.
Full compiler/navmesh/LED/link/deployment and solo loading verified; user feedback
requires further texture/door-prompt correction. Earlier rebuild hold is superseded
for this separate test. Game controls remain with Sam.

Before the next conversion, read [player recon](../recon/v18/README.md) and
[Zombies progression proposal](ZOMBIES_PROGRESSION_V18.md). Blender v18 is the
current source. Named door/zone/item markers require explicit Radiant/game
implementation; they are not automatic entity exports. Conversion remains held
while Blender/reference refinements and UV/export calibration are addressed.

**Documentation review, 2026-10-02:** Read the installed official quick-start, scale, LED, build-light and image guides. See [Blender → Radiant workflow](BLENDER_RADIANT_WORKFLOW.md) for the current conversion, source/page references, verified v03 runtime and requirements for the next gameplay version. Earlier statements below about unverified lighting/runtime describe historical builds. Further conversion remains on Sam's requested hold.

Separate Blender-derived test source: `map_source/zm/zm_pharmacie_blender.map`.
Build/deploy and conversion limits are in [BLENDER_TO_RADIANT_TEST.md](BLENDER_TO_RADIANT_TEST.md).
Deployment must include the entire linked zone tree, especially `zone/snd`;
copying only root files caused a confirmed fatal sound-bank load error.

**Purpose:** reusable findings for building `zm_pharmacie` efficiently, with the editor used where its visual tools matter and repeatable file/build work automated where practical.

**Last checked:** 2026-10-02 on Sam's PC, BO3 Mod Tools build 5284267. Machine-specific install paths are recorded in [MODDING_PLAN.md](../MODDING_PLAN.md). Online project/tool claims below are attributed and still need to be checked against this installed build before adopting them.

**Latest workflow:** two-storey blockout with four custom photo materials compiles, lighting-exports and links. See [PHOTO_MATERIAL_WORKFLOW.md](PHOTO_MATERIAL_WORKFLOW.md) for explicit mesh UV syntax and the GDT database registration fix. Use `scripts/build-map.ps1`: normalized environment paths for GDT update, trailing slashes for compiler/lighting/linker, actual bake-PID wait, and printed-error checks as well as exit codes. Statements below about older untested builds are historical; current evidence is in MODLOG.md.

## Findings so far

- The BO3 Mod Tools project map is a readable `iwmap 4` text file. We preserved the launcher-created template in the repo, generated a first pub-room blockout from Python, and staged it in Sam's Mod Tools directory. This confirms axis-aligned room geometry can be authored by script without using the editor for every wall and floor.
- The official Mod Tools installation includes `docs_modtools/Radiant_Launcher_QuickStart.pdf`, plus guides for scale standards, materials, images, and lighting. Read the bundled quick-start before relying on community hotkeys or build details.
- The Mod Tools Launcher visibly lists `mp_combine`, `zm_giant`, and `zm_pharmacie`. Its build panel has Compile (Full), Light (Medium), Link, and Run options, plus Build. Startup output showed many duplicate-asset messages followed by `gdtDB: processed (354 GDTs) (16062 assets) in 12.013 sec`.
- The installed `cod2map64.exe` accepts `-platform pc -navmesh -navvolume -loadFrom <map-source> <bsp-output>`. Running it from Mod Tools `bin` with the expected `TA_GAME_PATH`, `TA_LOCAL_ASSET_CACHE`, and `TA_TOOLS_PATH` environment produced a BSP and Zombie navmesh in under two seconds for this blockout. `linker_modtools.exe -language english -modsource zm_pharmacie` then linked the map. The first link was slower while stock assets converted; the warmed second link completed in about 13 seconds.
- Compiler warnings remain for missing `jun_art_wood_plywood_dark03` material on retained stock mystery-box prefab geometry and no explicit `nav_volume` brush. Zombie `navmesh.hkt` generation succeeds; the separate navvolume output is only a zero-byte placeholder because this room has no `nav_volume` brush.
- The silent Radiant LED invocation returned before its output appeared, but it completed asynchronously and produced `share/raw/maps/zm/zm_pharmacie.led` (1,718,907 bytes). The following linker run completed after the LED appeared, so the current package has a lighting export. The earlier unlit link used preview lighting.
- Directly starting `Radiant_modtools.exe` opened an empty `unnamed.map` (0 brushes, 0 entities) with an outdoor sky preview. The Level Editor toolbar button was then tried from the launcher, but the resulting Radiant window was still `unnamed.map`. The intended project-open action is therefore **not yet verified**. Do not save the blank map. A community BO3 guide says to select the map in the Launcher and use the Level Editor button; it also describes right-clicking a map for `Open Map Folder`.
- Radiant's visible layout has a large 3D Camera view, an XY Top grid, Entity Info, and Entity Browser. A single editor process used about 4.6 GB of working memory during inspection on this PC. Two accidentally opened instances used roughly 9.2 GB combined, so avoid launching extra copies while iterating.

## Is a code-first map feasible?

Yes. A third-party lead is [hetri-courses/mcp-radiant](https://github.com/hetri-courses/mcp-radiant), a BO3 map-authoring MCP, not an MCP that drives Radiant's GUI. Its README describes text-based map scaffolding, box geometry, Zombies entity placement, GSC/CSC helpers, asset-zone files, and compile/link wrappers. We did not install or copy its code; we used its published captured official compiler/linker argument patterns as a starting point and verified the official tools locally. Our small project generator is in `scripts/generate_blockout.py`.

This is a promising candidate, not a verified dependency. It is a third-party project, targets a Mod Tools path configured by environment variable, and its README describes a file layout that may differ from the launcher-created project in this repository. The repository's top-level listing does not show a license file, so resolve its reuse terms before adopting or copying code. Its build and edits have **not** been run against build 5284267 or `zm_pharmacie`. Before adoption:

1. Read its source, tests, license, dependencies, and file-writing behavior.
2. Work on a copy of the generated template, not the only copy in the live Mod Tools install.
3. Compare the candidate's scaffold with our existing map/scripts; do not scaffold over `zm_pharmacie`.
4. Start with one generated box room and a small entity-only change, inspect the `.map`/GSC diff, then use the official compiler and game as the oracle.
5. Keep Lighting and final visual checks in Radiant unless an independently verified automation route is found.

If the third-party MCP's license or compatibility does not fit, the same split can be implemented as a small project-specific Python/PowerShell generator: calculate dimensions in BO3 units, emit conservative axis-aligned brush blocks and entity KVPs, and patch the template without reserializing unrelated brush text. A diff and backup before each generation keep iteration reviewable. Use the stock `zm_giant` source as a syntax/reference file; never edit it.

## Recommended workflow for this map

1. **Preserve the generated template.** Keep the launcher-created map as `map_source/zm/zm_pharmacie.template.map`; generated source and scripts are in this repo. Keep stock tool sources and game files out of Git.
2. **Describe rooms declaratively.** Store room bounds, wall thickness, openings, spawn positions, and zombie-zone extents as data, in BO3 world units. For the first blockout, use one long main room, a clear central lane, front openings, and a simple far-end bar wall.
3. **Generate simple geometry and mechanics.** Use scripts/MCP for box brushes, spawn entities, zone volumes, and repetitive markers. Keep stable GUIDs and do not replace unrelated entities or prefab geometry.
4. **Inspect the text diff before compiling.** Check brush winding, extents, textures, entity GUIDs, and GSC references against the installed template and stock examples.
5. **Open the working `.map` in Radiant for visual review.** Confirm scale, openings, visibility, and collision. Use the editor for curved/detail geometry and lighting; avoid duplicate Radiant processes.
6. **Build with the official toolchain.** The direct compiler/linker command is now known and documented in `MODLOG.md`; lighting remains unverified. Never copy outputs into the BO3 game install without the user's approval.
6. **Build from the Mod Tools Launcher.** Keep the exact build options/command and outcome in `MODLOG.md`. Never copy outputs into the BO3 game install without the user's approval.
7. **Iterate by change type.** Use a fast entity-only build only if the official pipeline confirms it is valid for the change; rebuild geometry after brush edits and bake lighting when the blockout is stable.

## Radiant learning notes

The community [BO3 Zombies Mapping Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3737598953) describes the common workflow: create a `zm_` project in the Launcher, select it, open the Level Editor, build brushes in 2D orthographic views, then compile through the Launcher. Its page currently includes a Steam removal/incompatibility notice, so treat its steps as community guidance and verify them locally.

The guide describes the four-pane roles and basic brush workflow: top/side views help place geometry; the 3D view is for visual navigation; drag a shape in a 2D view and press Escape to finish a brush; use the texture browser (`T` per the guide) to assign material. It recommends adding an XZ side view from **View → New View Window → New XZ View**. These shortcuts have not yet been checked against our installed Radiant version.

## Sources

- Installed primary documentation: `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130\docs_modtools\Radiant_Launcher_QuickStart.pdf` (Sam's PC only).
- [BO3 Zombies Mapping Guide on Steam](https://steamcommunity.com/sharedfiles/filedetails/?id=3737598953) (community guide; page shows a removal/incompatibility notice).
- [mcp-radiant repository](https://github.com/hetri-courses/mcp-radiant) (third-party implementation; not yet audited or tested here).
- [gscode Radiant community wiki](https://wiki.gscode.net/docs/launcher/radiant) (interface summary).

## Next useful verification

Open the current map in Radiant for visual inspection and run the compiled mod in BO3 after approval to copy the generated package into the game install. A first blockout is generated, fully compiled with Zombie navmesh, lighting-exported, and linked; it has not yet been game-tested.

## SVG build runtime verification (2026-10-02)

The SVG-derived rebuild completed compiler + lighting + linker, then loaded using `BlackOps3.exe +set fs_game zm_pharmacie +set logfile 2 +devmap zm_pharmacie` after the linked zone folder was copied to the separate game installation's usermaps/zm_pharmacie. The user played two rounds with six kills (results screenshot in docs/screenshots). The earlier “not game-tested” statements above describe older builds. See scripts/build-map.ps1 for a parameterized build sequence that waits for actual LED completion.

Second scale test now authorized after v15 detail pass: separate zm_pharmacie_scale with custom no-spawn round callback. General photo/material conversion and enlarged street bounds are implemented by export_scale_test.py/generate_scale_test.py. See SCALE_TEST_V15.md and MODLOG.md for actual build/runtime results.
