# Neighbouring 3D shopfronts — v19

Latest Blender checkpoint: [pharmacie-shopfronts-v19.blend](../assets/blender/pharmacie-shopfronts-v19.blend).
Scene **03 Both floors - assembled exterior**, with six saved `Review v19`
cameras. V18 remains preserved. This pass changes Blender scenery only; the
pending BO3 crossing/bar build is still separate and has not been replaced.

## Modelled features

- **Wreake Valley Flooring:** sage pilasters, cream fascia and sharp lettering,
  projecting mouldings, angled window returns, recessed closed double doors,
  transom, handles and tiled threshold. Three upstairs sash assemblies.
- **Syston Dry Cleaners:** grey joinery, sharp multicolour fascia lettering,
  recessed left door and terracotta threshold, projecting three-pane chamfered
  display bay and brick base. Two white upstairs sash assemblies.
- **Syston Nails & Spa:** blue fascia with rebuilt lettering (approximate
  typeface), white window/door frames, recessed closed entrance, modelled diamond
  security grille and projecting upper white bays. Two upstairs sash assemblies.

Sam requested consistent scale with the pub. All seven neighbouring upstairs
windows copy the first pub window's actual geometry: glass approximately
**1.680m wide ×2.610m tall**, bottom Z5.865m/top Z8.475m, with matching sill,
lintel and pane divisions. Shop trim colours remain distinct. Upper masses/roofs
were raised to fit those shared levels; this is a user-directed gameplay-scale
choice, not a claim of surveyed building heights.

Window displays retain selected UV regions from the unchanged v17 rectified
facade images. Full-building photo planes are archived and unlinked from scenes;
they no longer supply the shop architecture. Displays remain opaque photographic
proxies with baked reflections/detail. Shops have backing masses and no interiors.
Recess/projection depths are estimates (.78m Wreake recess, .68m cleaner entrance,
.36m cleaner window projection and spa entrance, .37m spa upper bay).

## New renders

Six1200×800 Cycles renders,20 samples with denoising and temporary review
daylight. Frontal review cameras use28mm, wide row12mm. Temporary render lighting
is not saved into the map. These are new v19 views, not BO3 screenshots.

[![Wreake frontage](../recon/v19/01_wreake_front.png)](../recon/v19/01_wreake_front.png)

[![Wreake recessed doorway and angled returns](../recon/v19/02_wreake_recess.png)](../recon/v19/02_wreake_recess.png)

[![Dry cleaner frontage](../recon/v19/03_cleaner_front.png)](../recon/v19/03_cleaner_front.png)

[![Nail and spa frontage](../recon/v19/04_spa_front.png)](../recon/v19/04_spa_front.png)

[![Neighbouring street row](../recon/v19/05_neighbour_row.png)](../recon/v19/05_neighbour_row.png)

[![Right-hand shopfront depth](../recon/v19/06_right_shop_depth.png)](../recon/v19/06_right_shop_depth.png)

## Verification and reproduction

Generator:scripts/model_shopfronts_v19.py, launched in background Blender with
v18 input. It refuses to overwrite a v19 checkpoint. Review camera refinement:
scripts/render_shopfronts_v19.py. Geometry checks:scripts/check_shopfronts_v19.py.
Manifest:assets/blender/shopfronts-v19-manifest.json; validation:recon/v19/validation.json.

Generator verifies1,339 existing non-street pub meshes retain identical world
vertices/faces and44 original reference hashes remain unchanged. Separate checks
inspect closed/outward solids, seven identical-size/height window assemblies,
and removal of three old facade planes from the assembled scene. Original photo
files are neither cropped on disk nor overwritten; crops are mesh UV metadata.

No Radiant export, compiler/game test, new shop interior or gameplay-door change
is included. Procedural brick and sharp FONT lettering still require appropriate
engine material/mesh conversion; do not assume the v18 exporter preserves them.
