# Opposite street shopfronts — v20

Latest checkpoint: [pharmacie-opposite-shopfronts-v20.blend](../assets/blender/pharmacie-opposite-shopfronts-v20.blend).
It includes the [three v19 pub neighbours](SHOPFRONTS_V19.md) and adds basic
3D fronts for **Fox & Hounds, Aston & Co, Syston Mini Market, Let's Move and
Floral Fantasy**. No shop interiors were added.

Each front has solid backing, projecting frames/sign boards, modelled windows
and a recessed closed doorway. Main signs use sharp geometry lettering with
approximate typefaces. Mini Market retains yellow/white wording on red; the estate
agent is navy, florist black/cream, Aston red and Fox cream/sage. Estate agent
and florist upper bays have real projection and simple roof hoods.

Five full-building photo planes are archived and unlinked. Only selected window
display/door regions remain photographic: product advertising, property cards,
floral screening and pub glazing. Crops avoid the prominent full-facade cars,
people and Street View markers where possible; some baked reflections/detail
remain. This is simple architectural relief, not a final asset reconstruction.

The nine new upstairs windows use the same1.680m×2.610m pub template as v19,
with shared sill/head levels. Building upper masses/roofs are adjusted around
that gameplay scale with modest height variation; these are estimated dimensions.
Recess depths are approximately.48m, fascia projection.23m and bay projection.57m.

## Reviewed Blender renders

New1200×800 Cycles inspection renders,20 samples with denoising and temporary
daylight. Six `Review v20` cameras are saved; the wide street view opens by default.
These show Blender geometry, not the deployed BO3 build.

[![Fox and Hounds frontage](../recon/v20/01_fox_and_hounds.png)](../recon/v20/01_fox_and_hounds.png)

[![Aston and Mini Market](../recon/v20/02_aston_market.png)](../recon/v20/02_aston_market.png)

[![Estate agent and florist](../recon/v20/03_estate_florist.png)](../recon/v20/03_estate_florist.png)

[![Opposite street row](../recon/v20/04_opposite_row.png)](../recon/v20/04_opposite_row.png)

[![Window and bay depth](../recon/v20/05_display_and_bay_depth.png)](../recon/v20/05_display_and_bay_depth.png)

[![Recessed Fox entrance](../recon/v20/06_fox_door_depth.png)](../recon/v20/06_fox_door_depth.png)

## Checks and remaining work

Generator verifies2,003 retained mesh objects against v19, including the pub
and its new neighbours;44 original references stay hash-identical. New solids
are checked for closed manifold edges and outward volume. Separate validation
checks nine equal-size/height upstairs panes and casts a street ray to the Fox
recessed doorway. The first preview exposed a wall hiding that door; the wall was
split around its opening and the renders corrected.

Source/provenance:assets/blender/opposite-shopfronts-v20-manifest.json.
Checks:recon/v20/validation.json and source-checks.json.
Reproduction:scripts/model_opposite_shopfronts_v20.py with v19 input; it imports
only geometry helper definitions from model_shopfronts_v19.py. Separate check:
scripts/check_opposite_shopfronts_v20.py. Earlier v18/v19 checkpoints remain intact.

No Radiant/BO3 conversion or deployment occurred. Sharp FONT lettering and
procedural brick still need engine-ready conversion. Existing gameplay progress,
user control preference and pending crossing/bar test package remain unchanged.
Farther Post Office/Natural Wellbeing/Papermoon/Pasha fronts are outside this pass.
