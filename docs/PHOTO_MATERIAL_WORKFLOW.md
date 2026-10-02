# Photo materials and the two-storey blockout

Updated 2026-10-02. This is the handover for the photo-panel iteration; exact build and runtime outcomes are in MODLOG.md.

## User decisions

- The stairs form an L and lead to one large empty upstairs room, approximately the downstairs pub footprint. Keep that room undressed for now.
- Flat photo panels are acceptable for the frontage, bar, pharmacy wall and skeleton. Cut a real entrance opening where the door is in the frontage photo.
- Add more tables and seating, retaining clear gameplay routes.

## Reproduce the source

1. Install Python with Pillow (including AVIF support). Preserve every original in `references/pharmacie-syston/`.
2. Run `python scripts/prepare_photo_assets.py`. It creates RGBA TIFFs and a small original GDT in `assets/photos/`. No source photo is cropped or repainted. Pixel crops are expressed as mesh UV coordinates in `scripts/photo_panels.py`.
3. The skeleton's transparent input is `assets/photos/skeleton-cutout.png`, generated using the imagegen skill from the supplied 1500×2000 skeleton/dentist-chair photo. This is an AI-isolated derivative, not an unchanged photographic cutout. Keep it so regenerating textures does not require another generation call.
4. Run `python scripts/generate_blockout.py` to regenerate brushes, gameplay entities and photo meshes from the preserved template and SVG.
5. Run `./scripts/build-map.ps1 -ToolsRoot '<your BO3 Mod Tools installation>'`. This stages only project-owned source and derived assets into the dedicated tools installation. Compiled packages remain there until explicitly deployed to the game.

The build script now stages the complete repository `usermaps/zm_pharmacie` source tree as well as the map/materials, so a fresh tools installation does not need Sam's previously created project. The included TIFFs/GDT allow building without regenerating assets. Python regeneration requires `python -m pip install -r requirements.txt`; the full rebuild log is preserved in `docs/build-results/photo-pass-verified-build.log`.

## Source mapping

| Material | Reference | Use |
| --- | --- | --- |
| `pharmacie_frontage` | `pharmacie-arms-syston-2.jpg`, 1024×751 | Three meshes around the actual doorway; photo crop (28,190)–(1000,674). Door pixels (535,435)–(700,674). |
| `pharmacie_bar` | `bar front.jpg`, 2000×1325 | Drawer front crop (50,745)–(1900,1230); upper taps/shelves crop (50,270)–(1900,745). Separate solid counter retains collision. |
| `pharmacie_feature_wall` | `great for texture.avif`, 1973×1227 | One non-tiling panel on each main-room side wall. Cabinets and lights remain photo-baked in this prototype. |
| `pharmacie_skeleton` | Full-length 1500×2000 supplied skeleton photo | Transparent flat seated skeleton and dentist chair, facing the central aisle near its SVG marker. |

Asset files, dimensions, source SHA-256 hashes and conversion steps are recorded in `assets/photos/manifest.json`. The three original photographs remain pixel-identical. TIFFs are square/power-of-two storage; explicit normalized source UVs determine the displayed crop. World dimensions are provisional and some bar/facade proportions are stretched for the blockout.

## Materials and geometry

The installed `Images.pdf` recommends compressed high-color images with default average mipmaps; `Materials.pdf` identifies Lit as the basic opaque surface material. Stock GDTs use `image.gdf`, TIFF `baseImage` paths, `sRGB3chAlpha`, `diffuseMap`, and the `material.template` definition. Our original GDT uses `lit_nocull` for flat photo panels and `lit_alphatest_nocull` for the skeleton. No stock material definitions or extracted game textures are committed.

Text map mesh syntax was observed in the stock `zm_giant_geo.map`: `mesh`, two material names, `2 2 0 8`, then four `v x y z t imageU imageV lightmapU lightmapV` vertices. Image coordinates are pixel units in the converted TIFF; this avoids guessing brush scale/offset behavior. Photo materials are non-solid and non-colliding. Walls and the bar have separate solid brushes; the skeleton is scenery rather than an AI actor.

Frontage spans x=-352..352 at y=-657, z=0..320. Its photographic opening is approximately x=15.21..134.72 and 158.02 units high. The previous narrow vestibule is replaced by a bounded outdoor forecourt, allowing players to view the front. Photo alignment supersedes the SVG's approximate entrance position at Sam's request.

Eight tables now have tops and legs, with two simple chairs each. Three tables were added: west of the central aisle behind the bar, on the front-right platform, and on the patio. The central aisle is kept clear; route clearance still requires an actual in-game walk-through and zombie test.

Upstairs floor height is 336, underside 320, roof underside 640. The room has no furniture, with 304 units clear height. The east flight rises north to 168, turns west, and reaches 336 through an L-shaped floor opening. Both flights use 13 rises of approximately 12.92 units. The installed scale guide recommends 8-unit stair rises; our taller blockout stairs are provisional and require runtime testing rather than being described as standard stairs.

## Asset database and build gotchas

- Merely copying a new GDT does not guarantee the compiler knows its materials. Explicitly run `<ToolsRoot>/gdtdb/gdtdb.exe /update` from `<ToolsRoot>/bin` before compiling. A build can succeed with missing materials; check its log.
- For GDT indexing, set `TA_GAME_PATH` and `TA_TOOLS_PATH` to the normalized **Mod Tools root without a trailing slash**. The retail game root fails because it lacks `deffiles`. On Sam's existing database, changing between doubled/trailing paths produced duplicate registrations. A backed-up `/rebuild` with normalized paths succeeded: 355 GDTs, 16070 assets. Backup: ignored `build/gdt-before-photo-rebuild.db`.
- Compiler, Radiant lighting and linker use the earlier verified environment **with trailing slashes**. Removing them let compilation run but made the linker fail to open `zone_source/zm_mod_level.class`. This linker printed errors despite eventually returning zero; logs must be checked in addition to exit codes.
- Starting GdtDBTray without the environment immediately exits. The separate `gdtdb.exe` CLI is a more repeatable route; its help lists `/update`, `/rebuild`, and `/export`.
- The lighting wait tracks the actual bake PID, not every Radiant process. An unrelated editor can stay open without preventing completion.
- Flying-AI nav_volume and missing stock mystery-box plywood warnings remain separate from the custom materials. Ground navmesh generation succeeds; no flying units are part of this prototype.

## Remaining verification

Confirm actual photo rendering, UV orientation, skeleton alpha, exposure, and doorway/stair traversal in BO3. Verify zombie pursuit from upstairs and the forecourt, all player spawns, and co-op. Do not treat a successful link or a screenshot of the results screen as proof of every route. Rights for distributing externally sourced photographs remain unresolved; this is private prototype work.

Final photo build passed full compile, fresh lighting and both links (see `build/photo-pass-verified-build.log`). `docs/screenshots/photo-frontage-first-game.png` verifies the frontage renders with readable, correctly oriented signage and its doorway opening. The scene is still too dark, with overexposed/white weapon and sky; lighting/exposure/probes need repair. Other photo panels and the stair route remain pending individual runtime inspection. Sam was actively using/pausing BO3, so the agent only took passive screenshots and left that session running.
