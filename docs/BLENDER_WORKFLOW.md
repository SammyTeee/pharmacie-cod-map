# Blender workspace — 2026-10-02

Current editable map (2026-10-03): `assets/blender/pharmacie-syston-street-v25.blend`.
Latest street base and review views: [SYSTON_V25.md](SYSTON_V25.md).
Use `scripts/open-blender.ps1`. Player recon, fixes, measured limits and72 review
screenshots: [recon/v18/README.md](../recon/v18/README.md). Proposed Zombies
progression: [ZOMBIES_PROGRESSION_V18.md](ZOMBIES_PROGRESSION_V18.md). Earlier
"current/latest" statements below document historical milestones.

Sam requested a Blender-first modelling workflow using `hq floor plan ai.png`, then requested Blender and an MCP installation.

## Installed and verified on Sam's PC

- Blender **5.2.2 LTS**, official Blender Foundation winget package, executable `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
- uv **0.12.22**, official astral-sh winget package.
- Official [Blender Lab MCP](https://projects.blender.org/lab/blender_mcp), source commit `dbbf836ad4b1025f14a2b3b504c43903f39e0b04`. Selected over the community ahujasid implementation for its Blender-maintained, minimal Python/API/documentation interface; this is a project choice, not a universal ranking.
- Add-on extension `bl_ext.user_default.mcp` version **1.0.0**, enabled in Blender 5.2 preferences with auto-start on **127.0.0.1:9876**. Installed from the official source using `blender --background --command extension build --source-dir build/blender-mcp-official/addon/blender_mcp_addon --output-dir build`, then `blender --background --online-mode --python scripts/setup_blender.py`.
- Server package **1.0.2**, installed into isolated `build/blender-mcp-env` using `uv pip install --python build/blender-mcp-env/Scripts/python.exe ./build/blender-mcp-official/mcp`. Source checkout, dependencies and build archives are ignored local setup files.
- Codex server name **blender**, registered with `codex mcp add blender`, using the absolute local server executable and `BLENDER_MCP_HOST=127.0.0.1`, `BLENDER_MCP_PORT=9876`, `BLENDER_PATH=<executable above>`.
- Verified using `build/blender-mcp-env/Scripts/python.exe scripts/verify_blender_mcp.py`: MCP initialization, **26 tools**, live scene inspection, Python execution and save all succeeded. Report: `build/blender-mcp-verification.json`. The running bridge listener belongs to Blender PID 6580 at verification time.

Codex may need a fresh session/app restart to load the newly registered tool list. The independent MCP client test already proves the actual server-to-Blender connection works. These paths are machine-specific; keep the local build environment available because Codex points into it.

## Starter scene

`assets/blender/pharmacie-reference-base.blend` contains the original full plan sheet as a packed reference image, metre units, an orthographic top view, and collections for ground floor, first floor, props and BO3 collision guides. Source image unchanged. Reproduce with `blender --background --python scripts/create_blender_base.py`; this recreates the starter, so do not run over later modelling work. Open with `scripts/open-blender.ps1`; avoid duplicate instances because they compete for the bridge port.

The seven-metre frontage written on the sheet is Sam's estimate. Initial image display scale uses roughly 280 image pixels across the ground-floor frontage. This is a tracing aid, not a measured survey. No building meshes or BO3 export are included yet.

## New plan observations

### Scaled tracing base — 2026-10-02

Sam has no measured dimension and authorized proceeding with an estimated 7m frontage. `assets/blender/pharmacie-scaled-plan.blend` is now the active tracing base, created in a separate scene without deleting the starter. Uses the original `references/pharmacie-syston/floor plan of downstairs and upstairs council to scale.png` (1264×874), packed unchanged. Two mesh reference planes show different regions through UV coordinates; no source crops or image repainting.

Ground calibration endpoints approximately (205,119) and (205,341): 222 pixels = 7m, **0.0315315315m/pixel**. Both floors share this uniform factor. First-floor front corner (208,516) is translated to the same origin; drawing skew/perspective are uncorrected. Ground region (190,60)..(1028,393); first-floor region (190,460)..(900,748). Plan-based overall depth is roughly 21m, an implication of the estimated frontage, not a measured venue dimension.

Both planes are at Z=-0.02 for tracing: upstairs is hidden by default, accessible with its Outliner eye control. No floor elevation has been guessed. A 7m frontage line and metre ticks establish visible scale. Collections are ready for traced geometry; references are locked against selection. Viewport uses material preview and a top orthographic view.

Created via `build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/scale_blender_plan.py`, live official Blender bridge, success. Check script `scripts/check_scaled_blender_plan.py` verified both planes, packed source, shared scale and actual guide length 7m; screenshot `build/blender-scaled-plan.png` visually inspected. `scripts/open-blender.ps1` now opens the scaled base. Re-running the creation script creates another scene; use it for reproduction, not ongoing model editing.

- Ground-floor sheet shows a long room with an angled outline, inset/bay-style frontage, U-shaped bar, rear service space, disabled WC, store, rear stairs, external pathway and a **proposed** external seating area.
- First-floor sheet shows a seating room plus kitchen/prep area, offices, stores, toilets and rear stairs. This differs from the earlier simplified empty upstairs room.
- Red lines and fire call-point marks are drawing annotations; do not extrude the red outline indiscriminately as physical walls.
- Drawing date, approval/as-built status, room heights, exact scale and current use of upstairs spaces remain unverified. The proposed seating area is not evidence it was built.

## Modelling and BO3 route

Trace structural walls/openings on each floor, align stairs vertically, and use photos for frontage/bar/detail. Keep separate modular meshes and simple collision guides. First validate the export of one small asset against installed BO3 model/material documentation before detailing the whole building.

Blender is the modelling source; a `.blend` is not a ready-to-play BO3 map. The exact model exporter/importer is **not yet selected or tested**. Preserve the existing playable `zm_pharmacie` source. Radiant/official Mod Tools remain responsible for playable world/collision, entities, Zombies zones/spawns/scripts, navigation, lighting and final compilation. Do not assume importing one giant building mesh creates any of those systems.

## Active project: evacuation plan (2026-10-02)

The latest user-supplied `Architectural Fire Evacuation Floor Plans.png` supersedes earlier images for new Blender work. Open `assets/blender/pharmacie-evacuation-plan.blend` with `scripts/open-blender.ps1`. Packed original, two aligned UV reference planes, estimated 7m ruler and approximate footprint guides; no building wall meshes yet. Ground calibration 316px (82,85)..(82,401) = 7m; upstairs anchor (76,558), same uniform scale. Both floors remain at tracing level; height and skew unresolved. Creation script refuses to overwrite an existing output. Manifest: assets/blender/evacuation-plan-manifest.json. Blender background creation succeeded with exit 0 and dimension/ruler assertions. Model export and playable conversion remain unverified.

## Current photo-led Blender model (2026-10-02)

Active file is assets/blender/pharmacie-photo-interior-v03.blend; open-blender.ps1 defaults to it. Default scene '05 Interior - photo-led dressing' includes finished frontage, ground rooms, 34 grouped interior furnishings and corrected stairs. Switch to '02 First floor - mapped rooms' for upstairs, '03 Both floors - assembled exterior' for stacked building, or '04 Photo frontage - inspection' for frontage detail. Object roots are named Empty groups with source evidence; move root to reposition its parts. Earlier saved versions retained.

See PHOTO_OBJECT_PLACEMENT_PLAN.md and assets/blender/photo-interior-v03-manifest.json. Seven-metre frontage and all heights remain estimates. Upstairs geometry explicitly rectified 316/327 in width and 934/1044 in depth; original plan preserved. Stair position now follows Sam's explicit rear-left exit / stairs on right / right turn description. No connecting men/women door. Front uses 3D joinery plus original-photo UV faces; interior props are simple editable proxies, including skeleton. Images packed, photo UV maps active for render; removable ceiling hidden. Source hashes unchanged. Blender preview/save verified; BO3 conversion/gameplay unverified.
