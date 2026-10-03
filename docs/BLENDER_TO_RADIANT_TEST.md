# Blender to BO3 test

Detailed conversion behavior, official Radiant documentation findings and next-version requirements: [BLENDER_RADIANT_WORKFLOW.md](BLENDER_RADIANT_WORKFLOW.md). Commands below target the earlier v03 checkpoint; do not run them against ongoing Blender edits.

**Current editing state:** `pharmacie-backbar-photo-v08.blend` is newer than
the running game map. Sam requested holding the next Radiant conversion while
making further Blender changes. Do not regenerate/rebuild v04 until requested.
The scripts below describe the verified v03 conversion.

This is not a 1:1 Blender scene import. Geometry and selected photo UV surfaces
transfer through our brush generator; shaders, small details, curved models,
collision semantics and functioning gameplay entities do not transfer exactly.
Blender can remain the modelling source; the official BO3 toolchain still owns
game asset conversion, collision/navigation compilation, lighting and packaging.

The saved photo-led Blender checkpoint is commit `d7203b7`, pushed to
origin/master. Its source is `assets/blender/pharmacie-photo-interior-v03.blend`.
The conversion uses a separate project, `zm_pharmacie_blender`, and preserves
the older playable `zm_pharmacie` map.

## Conversion

With the saved Blender project open and the local bridge running:

```powershell
build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/export_blender_test_geometry.py
python scripts/generate_blender_test_map.py
```

The exporter reads assembled world-space meshes without changing the saved
Blender model. The generator writes `map_source/zm/zm_pharmacie_blender.map`
and a separate Zombies bootstrap under `usermaps/zm_pharmacie_blender`.
One metre becomes 39.37007874 map units.

Current output has 645 solid brushes and 12 photo patches. Convex meshes become
brushes; concave horizontal slabs become triangular prisms. Seven curved
details use bounding boxes to avoid the compiler's face winding limit.
Stock materials approximate prop surfaces. Tiny details and the unsupported
instrument photo panel are omitted. This is a brush blockout conversion;
Blender shaders and detailed models need a separate asset pipeline.

## Build and open

```powershell
./scripts/build-map.ps1 -ToolsRoot 'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130' -MapName zm_pharmacie_blender
./scripts/launch-blender-test.ps1 -ToolsRoot 'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130' -GameRoot 'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III'
```

These are Sam's local paths; adjust them on another machine. The launch script
backs up player state and any existing test map, copies the complete linked
zone tree including sound banks, verifies file hashes, and opens the offline
test. It refuses to replace a running BO3 session.

If the GDT database reports stale duplicate registrations, build with
`-RebuildAssetDatabase`; that option backs up the database first.

The source `.map` can be opened directly in official Radiant after the build
has registered its photo materials. Compiled game packages stay outside Git.

## Verification and known issues

Compiler, Zombie navmesh, fresh lighting export and both fastfile links passed.
The first launch crashed because deployment omitted `zone/snd` subfolders.
The game log explicitly reported failure loading `zm_pharmacie_blender.en`.
Deployment now recursively copies and verifies all linker output files.

The corrected deployment loaded successfully in BO3. Passive evidence:
[round-one screenshot](screenshots/blender-test-first-game.png),
[build log](build-results/blender-test-verified-build.log), and
[runtime log excerpt](build-results/blender-test-runtime-tail.log).
Rear zombie riser pathfinding reports an invalid start; gameplay routes are
unfinished even though the map now loads.

Runtime verification is recorded in `MODLOG.md`. Stair clearance, furniture
collision, upstairs routes, lighting and all photo surfaces still need in-game
inspection. Compiler warnings include tiny portals around small prop details
and a missing stock mystery-box wood material.

## Second scale test authorized 2026-10-03
The earlier hold is superseded for the requested separate no-zombie architecture test, zm_pharmacie_scale, from Blender v15. See SCALE_TEST_V15.md for current scripts/materials and MODLOG.md for build/runtime results. Earlier commands above still describe v03 and should not be used to regenerate v15.
