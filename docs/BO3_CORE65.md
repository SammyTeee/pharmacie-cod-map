# Pharmacie core Zombies copy — 24 October 2026

Sam resumed BO3 work and requested a separate playable copy covering the pub,
nearest shopfronts and surrounding road. The longer Syston route is excluded
temporarily; Taraj is excluded from this first copy. Sam selected normal paid
progression. Preserve the complete Blender scene and older game projects.

Project: `zm_pharmacie_core65`. Visual source:
`assets/blender/pharmacie-demo-base-v59.blend`, assembled exterior scene.
Engine controls remain with Sam. No movement, purchases or console input are
authorized for the agent by this request. A launch/capture is not a gameplay pass.

## Definitive transfer method

Blender **can** supply the detailed geometry and photo textures. BO3 does not
open a `.blend` directly. The appropriate division is:

```text
Blender evaluated triangles + per-face materials + per-corner UVs
  -> spatially divided rigid XModel files -> official export2bin -> BO3 models
Packed/source photos -> lossless TIFF derivatives -> image/material GDT assets
Procedural base colour -> explicit texture baking -> image/material GDT assets
Separate conservative collision + zones + stock Zombies assemblies -> .map
  -> official geometry/navmesh -> fresh lighting export -> linker -> private test
```

This preserves visual geometry without representing each visible ornament as a
BSP brush. Model chunks use local origins and placement entities; together they
reconstruct the unchanged source dimensions. Photographs retain normalized crop
coordinates. Non-power-of-two photo storage uses padding and adjusted UVs, not
photo resizing. The photographic pixels inside that padding compare exactly.

The existing exporter was a different, deliberately lossy route:
`export_playtest_v18.py` rejects image surfaces unless they consist of one quad;
`export_playtest_v58.py` substitutes a flat material for unsupported image shapes.
The generator also substitutes stock textures for procedural materials and boxes
some detailed meshes. Later lean passes omit decoration to stay within compiler
limits. Those failures do **not** establish that Blender photo/model transfer is
impossible. See `PLAYTEST_V58.md` for the actual old compiler/runtime history.

“1:1” must distinguish source transfer from rendered appearance. We can check
dimensions, triangle accounting, material assignments, photo pixels and UVs.
Blender's shader graphs, Cycles lighting, exposure, glass, procedural bump and
BO3's compressed textures/mipmaps are different rendering systems. Base-colour
baking does not prove matching normals, metallic response or lighting. A source
photo also retains its photographed shadows/reflections. Runtime visual review
is therefore required before calling the complete result faithful.

## This copy

- Clipped visual bounds: X −55..68, Y −30..38, Z −4..24 source BU.
- 4,194 evaluated source objects; 148,596 exported visual triangles; 91 rigid
  model chunks. No visual bounding-box substitutes or deliberate detail decimation.
- 43 direct image materials, 11 procedural base-colour bakes and 141 constant
  colour materials. Photo surfaces bypass baking. Procedural bakes retain original
  object/generated coordinates through mesh attributes before joining surfaces.
- Corrected v58 collision contributes the in-bounds solids; a local road slab
  provides continuous road support. Four outer clip walls and two visible road
  barriers close the area. The larger route is absent from the generated map.
- Four distinct co-op initial starts; stock round setup and weapon prices.
  Street/rear exits cost 750 together; upstairs costs 1,000; the short further
  street/crossing section costs 1,250. These are retained v18 progression values.
- Stock RK5, KRM, Kuda, KN-44, Quick Revive and upstairs power assemblies are
  retained. The decorative mystery-box base is removed; no functional box is
  claimed. Purchases, AI and co-op need individual runtime tests.
- Engine transform: `(BU + (-3.5,-10,0)) * 39.37007874015748`. Source world
  matrices already include the approved gameplay scale; do not enlarge again.
  This is fidelity to the Blender source, not a new real-world dimensional survey.

## Reproduce

From this repository, using the saved v59 source and Blender 5.2.2 LTS:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background assets/blender/pharmacie-demo-base-v59.blend --python scripts/export_bo3_core.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background assets/blender/pharmacie-demo-base-v59.blend --python scripts/bake_bo3_core.py
python scripts/prepare_bo3_core_models.py --export2bin '<ToolsRoot>/bin/export2bin.exe'
python scripts/generate_bo3_core.py
python scripts/check_bo3_core.py
python scripts/audit_bo3_core_ground.py --require-pass
python scripts/audit_bo3_core_routes.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background assets/blender/pharmacie-demo-base-v59.blend --python scripts/audit_bo3_core_visual_floors.py
./scripts/build-bo3-core.ps1 -ToolsRoot '<ToolsRoot>' -RebuildAssetDatabase
./scripts/relink-bo3-core.ps1 -ToolsRoot '<ToolsRoot>'
python scripts/accept_bo3_core_build.py --tools-root '<ToolsRoot>' --compile-log '<saved build log>'
```

Derived photo pixels, binaries and intermediate geometry remain in ignored
`build/bo3-core/`; scripts/manifests/reports carry the reproducible work. No
source `.blend` is saved by export/bake. The staging script adds only the
`pharmacie_core65` asset namespace and `zm_pharmacie_core65` project in Mod Tools.
It never stages or deploys to the retail game itself.

Use a backed-up GDT rebuild on this installation: `/update` reproduced the
already documented duplicate-path registrations after linking. GDT strings need
escaped backslashes. On this installed `export2bin`, explicit input/output mode
compressed plain text instead of invoking the model token converter. Use its
batch pattern mode from the model directory. The verifier expands the LZ4
envelope and requires real MODEL/VERSION tokens and BO3 version 7; an existing
file or exit-zero command alone is not acceptance.
Keep model **origins**, as well as visible bounds, inside the sky enclosure.

Chunking is spatial and multi-material. Flat chunks are merged with nearby
volumetric chunks, retaining their triangles/UVs rather than adding visible
thickness or discarding the surface. Initial isolated planar assets triggered
the linker's `boxside of 0` static-model assertion. Model origins now use their
own bounds centres. Solid-colour materials receive valid planar UVs so the
native compiler can derive tangents; photo/baked UVs are unaffected.

The new entity reader counts all top-level entities, including historical
generated blocks without `// entity` comments. The older helper only reads
commented entities and would silently omit the later paid gates/zones. Generated
core entities are all numbered, and all four actual stock initial starts are
checked against collision half-spaces.

## Evidence and acceptance

Source checks currently pass: unchanged source hash; native photographic pixels
for all 43 image materials; triangle counts and model references; all 91 binary
hashes; normal gate prices; five clear/supported spawn checks (four initial
starts plus `info_player_start`). These are source checks, not gameplay tests.

Build/runtime results are appended below as they are observed. Do not infer a
successful current package from an earlier failed build or existing output file.

## Primary sources and research

- [UGX custom-model authoring guide](https://wiki.ugx-mods.com/en/Modding/Black-Ops-3-Modtools/Asset-Conversion/Adding-custom-models):
  separate model conversion, rigid asset definition and material setup.
- [Maintained Blender exporter source](https://github.com/prov3ntus/pv_blender_cod):
  format/UV/winding reference. Its advertised Blender versions do not establish
  compatibility with our 5.2 installation; this project uses its own static
  exporter and installed official conversion tools.
- Installed `deffiles/xmodel.awi` and stock source GDTs: actual rigid-model,
  filename and collision property names. Stock sources remain unmodified.
- Installed `export2bin.exe` usage and actual outputs: explicit output syntax.
- [Treyarch Mod Tools announcement](https://store.steampowered.com/news/posts/?appids=311210&enddate=1475054677):
  official toolchain, editor and asset editor roles.
- [Universal Modder knowledge index](https://github.com/rehan-remade/universal-modder/blob/main/knowledge/INDEX.md):
  reviewed; no direct BO3 Blender-shopfront conversion proof found there.

Queries used: `Blender COD Black Ops 3 xmodel_bin textures UV export`,
`Black Ops 3 mod tools custom material image Asset Property Editor color map`,
`github Blender-CoD XMODEL_EXPORT export UV`, `export2bin command line`.
Online guidance is supporting evidence; local source checks, official tool
outputs and inspected runtime captures decide acceptance.

## Private trial and entrance repair — 24/25 October

The first accepted native package compiled fresh geometry, navigation and
lighting. A reviewed cached relink exited 0. The initial model conversion gave
15 pre-bone degenerate and 48 non-planar/stretch triangle warnings on terrain
backing and charcoal fittings; exported triangle accounting does not prove those
degenerate triangles survived native conversion. None of these were photo
materials. Eight package files (including nested sound banks) were hash checked
on deployment. Sam reached gameplay and bought the front street door, then fell
through the ground just outside. This is a failed traversal trial, not acceptance
of a fully playable map. The earlier trial backup is
`build/before-blender-test-20261024-204252`.

The source audit reproduced 42 unsupported body-width samples in the front
entrance strip (three lateral positions at 14 steps, source y .1 to 1.4). Named
static v58 floor groups had been excluded by the collision import's targetname
filter. The generator now retains `v58_static_surface_*` groups and adds a
permanent entrance slab, pavement/road support, and a continuous safety
foundation across the bounded core. These never belong to purchased door groups.
The repaired source has zero missing support across 35,238 samples. This checks
vertical support, not player clearance, visual seams or native runtime movement.

The GSC adds 27 passive native ground traces around the front exit, logging
`CORE65_GROUND_RESULT`. They do not move players. A fresh compiled trial and
Sam's purchased-door walk-through must confirm the repair in BO3.

## Story opening and remaining gameplay

See [BO3_PUB_STORY.md](BO3_PUB_STORY.md). The first-wave preparation callback is
60 seconds, superseding the earlier 30-second suggestion. It displays Sam's
bartender line about getting to Taraj for a Chicken Jalfrezi and a follow-up
about securing the pub first. Dialogue is subtitles only. Taraj remains excluded
from this copy and is a future story destination, not a reachable current goal.

The defendable bartender, loss of bar ammo/discount service on his death,
purchasable bar turret, exterior spawns and window climbing remain unimplemented.
The current stock floor-riser entities are still present. Do not describe the
story subtitles or preparation timer as implementation of those systems.

Build acceptance now also records script hashes. The launcher refuses changed
map/scripts or package hashes instead of trusting an older acceptance receipt.

## Wider floor and route audit — 25 October

Sam reiterated that continuous floors and a usable copy take priority. Added
two checks beyond the broad foundation grid:

- `audit_bo3_core_visual_floors.py`, run in Blender against unchanged v59,
  compares the evaluated ground pub, upstairs, outer alley and rear-turn floor
  meshes with exported solid support every .2 BU. All **11,813** samples have
  support, with no discrepancy over .05 BU. The actual stairwell opening is
  excluded naturally where the visible upstairs floor has no surface.
- `audit_bo3_core_routes.py` checks **1,592** positions along connected open
  routes: entrance/road, pub aisle and both bar approaches, rear loop, both stair
  flights and turn, upper arrival/hall/front-room door, and both street arms.
  It clips a conservative 16-sided standing body against nearby convex solids
  and checks floor steps. All checked routes pass. Assumptions: radius 15,
  height 70, step allowance 18 engine units. This is not native capsule physics
  and does not expand stock prefab collision.

Straight initial probes correctly hit seating, a stair guard and an upstairs
door frame; the connected audited paths go around those visible obstacles.
No rail, chair or architectural door frame was deleted to force a passing test.
The original straight east-street probe also crossed a wreck and the old closed
scenery boundary. The east clip boundary is now x=56 BU with a visible street
barrier at x=55.6..56, ahead of them; detailed visuals beyond remain scenery.
The obsolete extra crossing-zone volume at x=60..68 is removed. Visual bounds
remain x=-55..68; this is intentionally distinct from the bounded playable road.

Fresh geometry, navigation, lighting and both links passed after this boundary
adjustment. Package acceptance also requires matching current-map hashes for
the visible-floor and route reports and no failures in either report. Full
native traversal, purchases, AI and co-op remain separate tests. The preceding
passive launch capture showed the BO3 title screen with core65 loaded, not
gameplay or a successful floor retest; no controls were sent.

The final floor/boundary candidate passed exact-process relink with exit 0 and
was accepted as eight package files totalling 245,442,560 bytes. Deployed
25 October 11:08:30 UTC using `open-pharmacie-zombies.ps1 -DeployOnly`; recursive
hashes passed and the prior package/profile backup is
`build/before-blender-test-20261025-110828`. No game launch or controls were sent
for this final deployment. Use `PLAY-PHARMACIE-ZOMBIES.cmd` for the checked copy.
Sam's current manual entrance/alley/stair retest remains pending.
