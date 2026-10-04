[Latest enclosure fixes, service-lane detail and player-height fly-through](docs/ENCLOSURE_DETAIL_V33.md).

Latest Blender checkpoint: `assets/blender/pharmacie-enclosure-detail-v33.blend`.
Closes ground/upstairs seams and diagonal ceiling escapes; enclosed service lane,
rear threshold details and readable closure signs. V32 street, v30 rear loop and
approved pub/Taraj placement retained. Blender-only; engine package unchanged.
Saved route and visibility rays are not BO3 collision, navigation or co-op tests.
Older latest/checkpoint statements below are historical.

[Latest enclosed rear-alley mapping, before/after previews and highlight video](docs/REAR_ALLEY_V30.md). Current Blender source: `assets/blender/pharmacie-zombies-alley-v30.blend`; v29 street/Taraj work retained. New geometry is Blender-only; engine deployment remains unchanged.

[Taraj interior/bridge v26 and render review](docs/TARAJ_BRIDGE_V26.md).

Latest complete Blender checkpoint: `assets/blender/pharmacie-taraj-interior-bridge-v26.blend`. Detailed Taraj restaurant/bar and bridge/brook/access refinements are saved; earlier pub/street work is retained. Estimated dimensions and current guest placeholder are documented. New geometry is Blender-only; engine deployment remains unchanged. Older latest/current statements below are historical.

# Call of Duty: Black Ops III modding plan

Before the next Radiant conversion, read the
[conversion playbook](docs/RADIANT_CONVERSION_PLAYBOOK.md),
[placement specification](docs/RADIANT_GAMEPLAY_PLACEMENT_PLAN.md),
[installed-stock audit](docs/RADIANT_STOCK_GAMEPLAY_AUDIT.md) and
[saved tutorial library](research/radiant/README.md). This 4 October research
pass distinguishes the documented v30 Blender baseline from legacy v18 engine
placements. The outside mystery-box prefab is a static base; complete working
box assembly remains a conversion task. No new engine changes/build/deployment.

Latest Blender work: `assets/blender/pharmacie-shopfronts-v19.blend`, three
modelled neighbouring shopfronts. Read docs/SHOPFRONTS_V19.md. Sam requested
matching pub scale: seven upstairs window assemblies clone the first pub window
geometry/dimensions and sill/head heights. Six new renders and geometry checks
are saved. No v19 Radiant build; pending crossing/bar engine package unchanged.

Latest handover: [docs/HANDOVER_2026-10-03.md](docs/HANDOVER_2026-10-03.md).
Sharp-window result is user-confirmed. Crossing-wall/bar-region package built
successfully but awaits deployment after BO3 closes. Preserve the modified
working-tree .blend; our engine scripts did not save it. Older status below
is historical where it conflicts with the handover.

Latest authorized engine work (2026-10-03): separate `zm_pharmacie_playtest` from
v18 compiled/linked/deployed and loaded to solo combat/rounds. Corrective lighting,
texture settings, four stock wall buys and platform ramp built; user reports
some textures improved but many remain poor, and door purchase prompts absent.
Sam now confirms doors work. Latest sharp-window build passed and was deployed:
full photo bitmaps retain Blender UVs, with two new high-resolution typeset
drinks plaques. Latest texture quality still awaits runtime inspection.
See docs/PLAYTEST_V18.md and MODLOG.md. Earlier conversion-hold text below is historical.
Blender remains unchanged. User retains BO3 controls; passive observation only.

Photo reconstruction specification (2026-10-03): docs/STREET_PHOTO_RECONSTRUCTION.md and docs/PUB_PHOTO_RECONSTRUCTION.md contain detailed source-tagged rebuilding descriptions; docs/RECONSTRUCTION_SOURCE_INDEX.md and reconstruction-sources.json resolve 44 images with dimensions/review coverage/hashes. Read before the planned texture/street repair. Distinguish observed facade proportions from the intentionally enlarged gameplay scene; exact 1:1 dimensions still require calibration.

Current priority (2026-10-03): finish/reference-check Blender before another
Radiant conversion. Neighbour/alley geometry was corrected in v17, player cleanup
in v18. The v16 engine UV/material defect still needs calibration; investigation
and conversion plan: docs/TEXTURE_LAYOUT_FIX_PLAN.md. No v17/v18 engine build yet.

Latest editable Blender source: assets/blender/pharmacie-player-cleanup-v18.blend.
Recon/fixes/evidence: recon/v18/README.md. Zombies progression proposal:
docs/ZOMBIES_PROGRESSION_V18.md (start pub; front street purchase; stair-foot
purchase; linked rear alley loop; zones/items/spawns are planning markers only).
V17 street implementation and Blender validation: docs/STREET_REBUILD_V17.md.
Attached neighbours, outer-left alley, fuller roofed street rows and crossing/junction
blockout are saved and open. Per-facade derivatives are ready for Blender review;
Radiant UV/exporter calibration and runtime verification remain pending.
Enlarged skewed footprint, street and all seven selected layout fixes are saved.
Radiant rebuild remains on hold while Blender is reviewed. The separate engine
scale test is still the v16 architecture package; earlier playable prototypes are
retained. Engine UV correctness, traversal and co-op remain unverified for v18.

## Latest direction — Blender first (2026-10-02)

Current conversion documentation: [docs/BLENDER_RADIANT_WORKFLOW.md](docs/BLENDER_RADIANT_WORKFLOW.md). The v03 brush/photo conversion has loaded in BO3; detailed model export remains unverified. Newer gameplay Blender work is awaiting a requested conversion. Historical reference-only/export-pending statements below refer to earlier stages.

Sam requested Blender modelling from the new `hq floor plan ai.png` and installed Blender/MCP setup. Blender 5.2.2 LTS and official Blender Lab MCP are installed; a live MCP inspection/edit/save test passed. Reference-only starter: `assets/blender/pharmacie-reference-base.blend`. See `docs/BLENDER_WORKFLOW.md` for exact versions, paths, setup and plan observations. Blender becomes the modelling workspace; BO3 still uses Radiant/official Mod Tools for gameplay and builds. A Blender-to-BO3 asset export route remains to be selected and verified. Preserve the existing playable source until that route works.

- **Local machine observations (Sam's PC, checked 2026-10-02):** Steam app 311210 is at `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III`; `BlackOps3.exe` exists. The app manifest marked the game installed, though it still reported pending transfer/staging bytes. Executable version metadata was blank. These drive paths and install state apply only to that PC; recheck Steam on another machine.
- **Local toolchain (Sam's PC, checked 2026-10-02):** Official Call of Duty: Black Ops III - Mod Tools (Steam tool app 455130), at `S:\SteamLibrary\steamapps\common\Call of Duty Black Ops III 455130` (build 5284267; 28.1 GB on disk). `bin\Radiant_modtools.exe`, `bin\modlauncher.exe`, and `map_source\zm\zm_giant.map` were present. Optional DLC 499270 was disabled. Preserve stock source files. On another PC, install the official Steam tool and verify its library path/build.
- **Project source and build (Sam's PC, checked 2026-10-02):** The launcher-created `zm_pharmacie` template, generated blockout map, GSC/CSC, zone manifest, and sound-zone config are in this repository. `scripts/generate_blockout.py` regenerates the blockout; `scripts/prepare_photo_assets.py` prepares four photo materials. The latest two-storey furnished photo-panel source compiled, lit and linked with build 5284267 and a Zombie navmesh. Earlier SVG and upstairs-only packages loaded in BO3; latest photo verification is recorded in MODLOG.md. See `docs/PHOTO_MATERIAL_WORKFLOW.md` for reproduction and asset-index gotchas. Compiled outputs and absolute paths remain local to Sam's PC and are not in Git.
- **Game mode/safety:** User-owned PC game. Target cooperative multiplayer Zombies, tested offline/private. No anti-cheat bypass or public multiplayer modifications.
- **Chosen route:** Official BO3 Mod Tools and Zombies map template. This avoids WaW's legacy patch sequence, which copies files into the game root and overwrites files. Original Black Ops (BO1) is not the target: its community mapping route is less straightforward and not the official BO3 toolchain.
- **Map naming:** Lowercase BO3 Zombies name `zm_pharmacie`, confirmed by the launcher-created Zombies template.
- **Milestones:** (1) install/launch the Mod Tools and create/build the untouched Zombies template (project created as `zm_pharmacie`); (2) block out the main pub room; (3) prove co-op player spawns, zombie navigation, rounds, and doors; (4) apply one photo-derived pharmacy feature-wall material; (5) expand and dress the pub; (6) add and tune the Noseley boss; (7) package with provenance/credits after rights and build checks.
- **Asset approach:** Keep originals in `references/pharmacie-syston/`. Derive selected custom wall panels from front-on photos, while modelling architecture, bar, display cabinets, and gameplay objects as geometry or validated models. Inspect BO3 source assets and the Mod Tools material/build pipeline before choosing final dimensions or format.
- **Local display preference:** Sam wants the editor/game visible beside the 2K desktop. Radiant is resizable; test BO3 at 1600×900 windowed without changing desktop resolution. This is a preference for Sam's setup, not a requirement for another contributor.
- **Still to resolve:** Open the project in Radiant for visual review; resolve/accept the missing mystery-box wood material and optional nav_volume warnings; verify every route, upstairs stairs and co-op in BO3; tune the layout from Sam's interactive corrections; photo-texture dimensions/format; Noseley model/animation constraints; licensing for web-sourced images. Lighting exports and a two-round solo test have succeeded for the earlier SVG build. Verify Steam installs and paths on whichever PC continues the work.

## External references

- [Official Steam listing and BO3 Mod Tools information](https://store.steampowered.com/app/311210/Call_of_Duty_Black_Ops_III/)
- [Official BO3 Mod Tools Steam community hub](https://steamcommunity.com/app/455130)
- [BO3 Zombies mapping guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3737598953)
- [Modme WaW install guide, retained for the route comparison](https://wiki.modme.co/wiki/world_at_war/Installing-The-Modtools.html)

### SVG blockout update — 2026-10-02

Sam's saved SVG now drives world geometry through `scripts/svg_blockout.py`; see `docs/SVG_BLOCKOUT.md`. Compile, fresh lighting export and final link succeeded after removing an obstructed tutorial barricade. Mod Tools and game remain separate S: installations on Sam's PC. `scripts/build-map.ps1` takes ToolsRoot explicitly for collaborators. Runtime validation is tracked in MODLOG.md.

Latest reference: `Architectural Fire Evacuation Floor Plans.png`; new standalone project `assets/blender/pharmacie-evacuation-plan.blend`. Estimated 7m frontage, shared scale for both floors; tracing setup verified, building meshes and export pending. See docs/BLENDER_WORKFLOW.md.

Latest Blender source is assets/blender/pharmacie-photo-interior-v03.blend: both floors, photo frontage, corrected L stairs and 34 grouped interior objects. Photo evidence/assumptions: docs/PHOTO_OBJECT_PLACEMENT_PLAN.md. Existing playable BO3 source preserved; model export route remains unverified.

Blender brush conversion test now compiles, lighting-exports and links as separate `zm_pharmacie_blender`. See docs/BLENDER_TO_RADIANT_TEST.md. First runtime attempt failed because deployment omitted nested sound banks; recursive, hash-verified deployment fixes that omission. Runtime and stair traversal verification remain tracked in MODLOG.md.

Current Blender source:assets/blender/pharmacie-video-details-v10.blend, incorporating both video references. Texture derivatives are Blender-only; native BO3 conversion and gameplay verification remain pending while rebuild is on hold. See docs/VIDEO_INTERIOR_PASS.md.


Latest source supersedes v10:assets/blender/pharmacie-street-details-v12.blend, with eight photo-textured street fronts and user-preview roof/backing correction. Video interior retained; engine rebuild still held. See docs/STREET_PHOTO_FRONTS.md.

Latest Blender source: assets/blender/pharmacie-street-details-v13.blend, correcting Mini Market photo crop. Radiant rebuild remains held.

Latest Blender source pharmacie-detailed-pub-v15.blend. User lifted rebuild hold for a separate zombie-free scale test zm_pharmacie_scale after the new video detail pass; implementation/build/runtime evidence in SCALE_TEST_V15.md and MODLOG.md.

Current Blender source pharmacie-entrance-fixed-v16.blend. Fixes front threshold and developer-only diagnostic in zm_pharmacie_scale. See MODLOG.md for actual build/runtime state.
[Latest opened road to Taraj and review](docs/TARAJ_ROAD_V34.md).
Current Blender source: `assets/blender/pharmacie-taraj-road-v34.blend`.
Retained Melton route opened; terrain/frontage foundations and bounded gaps
added without moving the approved architecture. BO3 remains unchanged.
