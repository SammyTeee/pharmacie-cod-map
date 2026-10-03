# Blender → Radiant workflow

Checked 2026-10-02 against the installed official BO3 documentation, conversion scripts and recorded build/runtime evidence. This review does not export, rebuild or deploy the active Blender work. Sam's rebuild hold remains in effect.

## What Radiant does

Radiant edits the game-native `.map`: world brushes, mesh surfaces, models, lights and entities. The 2D grid is for precise construction; the 3D camera is for inspection and placement. APE defines game assets such as images, materials and models; the Launcher coordinates building. The official [Treyarch announcement](https://store.steampowered.com/news/posts/?appids=311210&enddate=1475054677) identifies these separate tools. This is historical documentation, not a newly released Radiant version.

Primary reference is the documentation shipped with Sam's installed tool build 5284267, under `<ToolsRoot>/docs_modtools/`. Read on this review:

| Document | Relevant finding |
|---|---|
| `Radiant_Launcher_QuickStart.pdf`, pp. 2–5 | Highlight the map row before clicking Level Editor; checking its box alone is insufficient. Drag in the 2D view to draw a brush; Ctrl+Tab cycles top/front/side. Escape deselects. F4 moves camera to selection; F8 shows real lighting. Bindings can be customized. |
| Same, pp. 6–8 | Lighting preview/build and LED export are separate steps; APE edits assets/GDTs and changes must be saved. |
| `Generate_LED.pdf`, p. 1 | Geometry or lighting changes require a new LED, then relinking. Export from the top map using File → Lighting Export, or the Launcher's Light option. |
| `Scale_Standards.pdf`, pp. 1, 5–6 | One map unit is one inch; typical world scale is about 120% of reality. Standing hull is 32 wide × 72 high. Suggested single door hole is 56 × 96; minimum stair width 80, default rise/run 8/12; short pinch point 64 wide. These are design standards, not proof of traversal. |
| `Images.pdf`, pp. 1–2 | Start with compressed images and default compression; inspect in game before exceptions. |
| `Build_light.pdf`, pp. 1–3 | Build lights provide simple lighting, but can be excluded from LED export. |

The quick-start contains early-beta text saying builds will arrive later and gives `mp_` names for its multiplayer example. Our installed tools demonstrably compile/link/run, and our Zombies projects retain the verified `zm_` convention. Do not follow those old statements literally. The map-row highlighting instruction may explain the earlier blank `unnamed.map`; this remains a hypothesis until checked in the GUI.

## Our implemented conversion

```text
Saved Blender v03 assembled scene
    → world-space vertices + faces + selected UVs (JSON)
    → iwmap brushes/photo patches + Zombies template entities
    → official compile/navmesh → fresh Radiant LED → linker
    → complete zone tree, including sound banks → BO3 test
```

This route is implemented by `scripts/export_blender_test_geometry.py` and `scripts/generate_blender_test_map.py`. Exact reproduction commands and previous evidence are in [BLENDER_TO_RADIANT_TEST.md](BLENDER_TO_RADIANT_TEST.md).

- Exporter currently asserts the filename `pharmacie-photo-interior-v03.blend` and selects `03 Both floors - assembled exterior`. It reads base meshes and `matrix_world`; it does not evaluate a general modifier stack or export every scene. It also adds an upper test roof to JSON without editing Blender.
- Position conversion is `(Blender metres + (-3.5, -10, 0)) × 39.37007874`, retaining X/Y/Z orientation. Existing world matrices include parent scaling: never apply the gameplay enlargement again in the generator.
- Closed convex meshes become solid world brushes. Named horizontal floor/ceiling slabs are decomposed into triangular prisms. More than 32 faces triggers a bounding-box substitute. Unsupported thin pieces under 0.6 map units and other concave meshes are skipped and reported.
- Recognized frontage, bar-front and feature-wall photo quads become explicit UV mesh patches with BO3 material names. Their visual faces do not provide the structural collision; underlying brushes must do that. General Blender UVs/materials are not preserved on brushes.
- Prop materials are assigned from names to stock wood, brick or concrete. Only the first mesh material name is read. Blender transparency, lighting, cameras, detailed shaders and arbitrary per-face materials do not transfer.
- The generator preserves template sky brushes and creates/repositions actual Zombies entities, lights and project scripts. Blender Empty markers do not automatically become spawns, doors, zones or zombie routes.
- Output is the separate `zm_pharmacie_blender` project. Regeneration replaces its generated map; manual Radiant edits there must first be captured in source data or a preserved patch. Keep the older `zm_pharmacie` and stock templates intact.

Verified v03 output: 645 solid brushes, 12 photo patches, seven boxed curve substitutes; compiler, navmesh, LED and linker passed and BO3 loaded to round one. Door passages were reported too tight; a rear zombie riser reported an invalid pathfinding start. Loading is not route/co-op verification.

## Next conversion, when requested

The documented latest saved gameplay version is v05; further live Blender work may be newer. Identify and save the actual intended checkpoint first. The exporter still targets v03 and must not simply be run against the active session.

1. Select the intended assembled scene and explicitly exclude reference planes, hull guides and route markers. Validate final world transforms and intended visibility; the present exporter does not filter hidden objects generally.
2. Measure doorway/frame gaps, bar aisle, stair width/rise/headroom against the fixed BO3 hull and the official standards. The estimated 1.305m doorway gap is about 51.4 units, below the recommended 56-unit door hole; global enlargement alone is insufficient evidence of comfortable co-op play.
3. Expand the sky/world boundary and playable volumes to contain the street. Map the outside player marker to real player spawns and street/rear/upstairs markers to validated Zombies spawn/zone logic. Current template positions and volume are hard-coded for v03.
4. Preserve road/pavement/white/yellow marking materials explicitly; the present stock-material name mapping does not reproduce them. Check which small objects should be non-solid dressing instead of solid obstructions.
5. Generate a conversion report, inspect the `.map` diff and open it in Radiant. Use simple collision around complex furniture; resolve unsupported objects deliberately. Detailed prop model export remains a separate, unverified route.
6. Compile geometry/navigation, bake a fresh LED and wait for actual bake completion, then link with `scripts/build-map.ps1`. Inspect logs as well as exit codes. Deploy the complete recursive zone tree only within existing user authorization.
7. Test outside spawn, entrance, every door, bar aisle, stairs in both directions, rear exit, upstairs zombie routes, rounds and intended co-op player count. Record exact commands/results in MODLOG.md.

## Useful design questions

Already settled: wider gameplay layout, front widened to building's widest part, street outside, player starts outside, zombie approach from outside with possible upstairs routes. No need to ask these again.

Remaining choices: expected player count (especially four-player clearance); initial unlock sequence and paid doors; whether upstairs zombies begin immediately or after unlocking; desired lighting/mood and must-recognize pub details. These guide route design, pacing and where to spend detail work. Dimensions remain estimates; measurements would help later but are not required to continue.
