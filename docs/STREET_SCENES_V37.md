# Melton street scenes v37

Checkpoint: `assets/blender/pharmacie-street-scenes-v37.blend`, from v36.
[Matched before/after gallery](../recon/v37/index.html).

Sam approved the v36 pictures and asked for more detail and more thought. The
next pass prioritises recognisable scenes and close-up prop construction over
repeating generic furniture across every shop.

The existing F006 shelter position is retained. Native reference 00101 and
`docs/street-catalogue/entries/F006.md` inform its green framing, segmented
sloping translucent canopy, glazed sides, timber seat and paved apron. New
details include canopy ribs/edges, back gutter/downpipe, lower kick panels,
glazing divisions/rails, visibility decals, bolted feet, seat supports/dividers,
a timetable cabinet and procedural block paving. Dimensions, joinery and the
generic timetable layout are approximations; no actual bus service times are
invented. The historic blockout shelter parts are archived unchanged.

Two original red/teal bicycles and steel stands form a shallow scene at B030.
Each includes tubular frame, tyres/rims, spokes, axles, saddle, handlebar/grips,
chainring/chain and pedal. At B038 a caster-mounted delivery cage, stacked taped
cartons and parcel handtruck give the frontage a service scene. These placements
are inferred Zombies street dressing, not surveyed real-world props. They stay
beside the facades, outside the sampled pavement through paths. Existing entry
doors remain retained; these particular shop interiors are scenery.

Three v36 planters receive irregular leaf tufts in four muted tones and small
flower heads. Original cube foliage is archived, while stems, planters and soil
remain. Original reference photos and shared source materials are unchanged.

375 new mesh solids are manifold with positive volume. 13,377 previous mesh
geometries/transforms are retained, including 40 newly archived blockout parts.
All 44 original reference hashes match. 3,429 road and 572 pub/alley samples
pass, plus 224 selected shelter/frontage samples at 10cm spacing, 42cm radius,
sixteen horizontal directions at three body heights and 1.95m headroom.
These are visible-mesh rays, not all pavement routes, continuous capsule
collision, player passing/revives, BO3 navigation, pursuit or co-op tests.
Engine files, builds and deployment remain unchanged.

Review caught the initial use of an already archived historical shelter roof as
the placement anchor, which evaluated at identity. The corrected generator uses
the retained active shelter post; the temporary incorrect preview was replaced.
Archived meshes have unevaluated world matrices after reload, so preservation
hashes use saved local matrices for unparented meshes and world space for
parented meshes. This checks actual saved geometry and transforms rather than
treating an unevaluated matrix as an edit.

Reproduce: `detail_street_v37.py` on v36, `check_street_v37.py` and
`check_local_street_v37.py` on v37, `inspect_street_v37.py` on v36/v37,
`highlight_street_v37.py` on v37 with `V37_REVIEW_ONLY=01_shelter`, then
`gallery_street_v37.py`. Build generator refuses overwrite unless explicitly
rebuilding its own generated intermediate with `V37_REBUILD=1`.
Logs: `build/v37-*.log`. Temporary render lighting/highlights never saved.

Remaining: Town Square still needs its enclosed recessed passage; many shop
glazing displays are simplified; general pavement wear and facade texture
variation need further work. This is another detailed Blender pass, not a
finished street or playable engine release.

Hosted review: https://sammyt.wtf/melton-v37/ . Ten uploaded gallery/image files match local SHA256; gallery and main shelter image HTTP200 confirmed. Existing preview.webm retained.
