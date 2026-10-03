# Blender street rebuild v17 — 2026-10-03

Current editable file: `assets/blender/pharmacie-street-rebuilt-v17.blend`.
Opened in Blender 5.2.2 LTS, scene **03 Both floors - assembled exterior**,
with the **Review v17 | Pub frontage** camera. The prior unconnected unsaved
Blender session was left intact; the saved v16 source was used as the baseline.
The new editor's official Blender bridge connected successfully and saved the
review refinements live. The saved v16 and a pre-refinement v17 safety copy remain.

## Applied from the reference notes

- Wreake Valley Flooring ends at X=-2.16m and Dry Cleaners starts at X=10.50m,
  the enlarged pub's nominal frontage edges. Nail/Spa follows Dry Cleaners.
- The alley now runs outside Wreake Valley Flooring, X=-12.74..-10.16m,
  width 2.58m, Y=0..32m. A rear connector at Y=31..33m reaches the existing
  rear landing beyond the neighbour's 15m depth. Its rear connection is inferred.
- Neighbour backing masses taper at their rear edges to clear the skewed pub.
  Closed scenery masses replace the former shallow backing strips. Pitched
  slate roofs, chimneys/pots, gutters and downpipes establish building depth.
  The shared pub/Wreake roof height follows the current enlarged pub model.
- Opposite photo fronts retain Fox, Aston, Mini Market, Let's Move and Floral
  Fantasy order. Added real upper-bay relief at Let's Move/Floral, narrow access
  doors, Pasha and Papermoon blockout fronts, HM private doorway, Post Office,
  and gabled Natural Wellbeing with paired upper sashes and timber infill.
- The Post Office / Natural Wellbeing access lane is a separate 3m gap.
  Pub-side and distant unnamed buildings are explicit placeholders.
- Added crossing signals/buttons, tactile pads and zigzag approach marks,
  a pavement build-out, parking-bay outline and Fox junction road/island stub.
  The road remains a straight blockout; its photographed bend and precise
  kerb/crossing/parking geometry still need calibration.
- Ten isolated 1024x1024 RGB facade derivatives use full-panel UVs. Each has
  one clearly named image/material. Original files remain hash-identical.
  See `assets/street/v17/manifest.json` for exact sources and pixel quadrilaterals.
- Added clearly labelled **proposed** gameplay anchor Empties. These are
  planning markers only; no BO3 power/perk/box prefab was moved or validated.

## Review and limits

Four saved camera previews are in `assets/blender/street-v17-{frontage,street,
alley,crossing}.png`. First renders exposed blocked camera views and a roof-height
mismatch; corrected these live and rendered again. Also removed coplanar asphalt
overlap at the junction and corrected brick projection on side walls.

The original pub interior, stairs and threshold geometry are retained. Earlier
street collections are unlinked from scenes and retained as archive datablocks,
so they do not duplicate the new street during scene export/rendering.
`scripts/check_street_v17.py` compares preserved pub geometry with v16, verifies
all 44 original-photo hashes, checks adjacency/alley/lane constraints and writes
`build/street-v17-check.json`. These are Blender checks, not gameplay tests.

This is a reference-led **gameplay-scaled blockout**, not a surveyed 1:1 rebuild.
New shop interiors are solid scenery. The photo fronts retain some perspective,
cars/people/poles and baked shadows; the Post Office photo includes an occluding
Street View marker. Further clean joinery/detail modelling is still required.
Procedural brick is a Blender preview shader: bake it or replace it with an
engine texture before exporting. Corrected per-shop derivatives reduce crop
ambiguity, but the Radiant UV/material fault has not yet been verified in game.

No Radiant map, BO3 install, compiled package or gameplay script was changed.
The next conversion still needs the exporter fixes and small engine UV calibration
in `TEXTURE_LAYOUT_FIX_PLAN.md`, expanded map/player bounds and runtime traversal.

## Reproduction

`extract_street_v16_facades.py` on saved v16 writes portable source UV metadata
to `assets/street/v17/input-facades.json`. `prepare_street_v17.py` reads that
catalogue and makes derivatives without changing sources. Then run
`rebuild_street_v17.py` on v16 and `refine_street_v17.py` on that initial v17.
Creation refuses to overwrite an existing v17; refinement refuses a second run
after its completion flag is set. Run `preview_street_v17.py` in background on
the final v17; it renders without saving temporary lighting into the file.
Full placements and limitations: `assets/blender/street-rebuilt-v17-manifest.json`.
