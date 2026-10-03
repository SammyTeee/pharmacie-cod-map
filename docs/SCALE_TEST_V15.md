# Second scale test — v15

Sam authorized the next Radiant conversion after the additional video detail pass on 2026-10-03. The earlier rebuild hold is lifted for this separate offline architecture test, `zm_pharmacie_scale`. Existing `zm_pharmacie` and `zm_pharmacie_blender` projects remain intact.

Blender source: `assets/blender/pharmacie-detailed-pub-v15.blend`. V14/V15 add 180 decorative meshes from the inspected video views: camera cabinets and camera bodies/lenses, medicine jars, ceramics/cartons, advert collages, dark dado, shelf lighting, ceiling grid, warm pendant diffusers, menu holders, coasters/glasses, counter drip trays, entrance notices and clock. Original diffuse colours now also drive unlinked render shader base colours; this fixes the previous white timber, upholstery, shelves and brass. New floor shader suggests timber planks. All placements are approximate within the widened gameplay layout. Originals remain untouched; four native additional crops and their manifest are under `assets/video-references/q0zBpicUXjg/textures-downstairs`.

Exporter reads final world transforms from the assembled scene, excludes guides/reference objects and hidden render objects, and adds a test-only upper roof. Gameplay scale is already in those transforms and is not applied again. Eight actual initial spawn positions are on the front pavement. Sky bounds and player volume now contain both floors and the street.

General photo quads retain explicit UV mapping through Radiant patches; separate TIFF/GDT derivatives register the packed image sources and material colours. Image textures are resized to power-of-two dimensions up to 2048 per axis. Constant textures approximate other material colours; procedural timber/carpet, transparency and mirror reflection are not faithfully exported. Convex meshes become brushes; high-facet details become bounding boxes, and unsupported/micro objects are listed in the export report. This remains a brush conversion rather than a complete xmodel pipeline.

The separate map GSC sets `level.round_spawn_func = &scale_test_no_spawns` before calling the normal usermap bootstrap. Installed stock `_zm.gsc` preserves a pre-existing callback and invokes it for round spawning. Our callback waits without spawning actors. Zombie template entities are retained for initialization compatibility; ordinary round spawning does not run. Actual loading and extended no-spawn observation must still be recorded below.

Commands:

```powershell
build/blender-mcp-env/Scripts/python.exe scripts/run_blender_script.py scripts/export_scale_test.py
python scripts/generate_scale_test.py
./scripts/build-map.ps1 -ToolsRoot 'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130' -MapName zm_pharmacie_scale -AssetFolder assets/scale-test -AssetNamespace pharmacie_scale -RebuildAssetDatabase
./scripts/launch-blender-test.ps1 -ToolsRoot 'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130' -GameRoot 'S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III' -MapName zm_pharmacie_scale
```

Initial `/update` failed on stale duplicate GDT registrations. Retry uses the existing build script's backed-up `/rebuild` recovery. Build/runtime results are recorded in MODLOG.md. Never claim traversal works merely because compilation succeeds.

Final conversion audit: 1,182 convex brushes,37 slab prisms,189 UV panels,zero skipped source objects;63 high-facet objects use box bounds. The skewed left outside passage required explicit slab decomposition. The no-spawn callback additionally enables player invulnerability once per second using the installed stock GSC method. Final build log: build/scale-test-build-verified.log.

## V16 correction
User runtime exposed a dev-only diagnostic PrintLn outside a devblock. Generator now wraps it in /# ... #/. Added a continuous front threshold slab spanning pavement into recessed entrance. Latest source pharmacie-entrance-fixed-v16.blend; bounds in front-threshold-v16-manifest.json. Rebuild log scale-test-v16-build.log. This supersedes the initial v15 runtime package; no successful runtime claim until checked.

V16 compiler/navmesh, fresh lighting export and both fastfile links passed; complete zone/sound tree hash-verified deployed. Steam launch is waiting for its ShowGameArgs confirmation; corrected runtime remains unverified. Original missing-FX warnings are also present in the earlier successfully loaded prototype log; fatal PrintLn script error is the specific repaired failure.
