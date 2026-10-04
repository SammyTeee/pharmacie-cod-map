# Town Square entrance and display detail v38

Checkpoint: `assets/blender/pharmacie-town-square-v38.blend`, built from v37.
[Matched review](../recon/v38/index.html).

Sam approved v37 and requested continued iterative detail. This pass resolves
the generic B031 lower shop into a geometric Town Square entrance and gives two
other shop displays individual contents. Pub/Taraj interiors, road layout,
building placement, shelter/cycles/delivery scenes and earlier detailing remain.

Native source 00270 and `docs/street-catalogue/entries/B031.md` inform the red/gold
sign with curved crest, projecting banner, brick opening and angled glazing.
Generic wing directories and crest initials substitute for unreadable specifics;
no source photo pixels were copied into new assets. The recess has a continuous
floor, brick walls with depth-facing texture coordinates, ceiling, skirtings,
three warm ceiling bulkheads and restrained high-level conduit. Its roughly
2.5m width/7m depth and closed rear service gate are gameplay approximations,
not surveyed dimensions or evidence of a connection to B028. The gate is static
scenery; there is no new purchase, unlock, zombie spawn or working route beyond.

The full generic B031 lower frontage and solid parcel are archived unchanged;
new side masses retain the outer parcel while creating the central recess.
Upper facade, windows, roof, neighbouring fronts and their positions remain.
New paving sits above the existing foundation top; side-wall skins sit inside
the parcel faces so surfaces do not coincide. Inspections caught hidden angled
glazing and overlapping backing in intermediate output; final generator and
rendered checkpoint incorporate the corrections.

B041 Syston DIY gains three tiers of individual paint tins, metallic lids and
paper labels. B039 Cardfactory gains three tiers of individual greeting cards,
coloured print panels, small generic titles and graphic stems. Business
categories follow the catalogue; product inventory and display arrangement are
modelling approximations. The previous generic shelf/merchandise solids are
archived unchanged. The shops remain scenery rather than accessible interiors.

Validation after reopening: 315 new manifold positive-volume mesh solids;
13,712 active parent-scene mesh geometries/transforms preserved (including 88
newly archived originals); 44 original source hashes unchanged. 3,429 road and
572 pub/alley samples pass, plus 351 selected local pavement/entry samples.
37 enclosure rays reach the new floor, side walls, ceiling/light fittings and
closed rear gate. Entrance is intentionally open. These are sampled visible
mesh rays at 42cm radial clearance, not continuous capsule sweeps,
watertightness certification, full pavement circulation, BO3 collision, AI
pursuit, stepping, purchases or co-op verification. Engine files remain unchanged.

Reproduce: `detail_street_v38.py` on v37, `check_street_v38.py`,
`check_local_street_v38.py`, `check_enclosure_v38.py` on v38, then
`inspect_street_v38.py` on v37/v38 and `highlight_street_v38.py` on v38 with
`V38_REVIEW_ONLY=01_town_square`, followed by `gallery_street_v38.py`.
Geometry helpers come from the retained v37 generator. Rebuilding its generated
intermediate requires explicit `V38_REBUILD=1`. Logs: `build/v38-*.log`.
Temporary comparison lighting/highlights are never saved into the checkpoint.

Remaining: more varied and faithful shop architecture/displays, worn plaster
and pavement surfaces, richer retail products, full pavement circulation and
eventual separate Radiant conversion. This is a detailed Blender checkpoint,
not a finished street or engine release.

All 224 v37 local shelter/cycle/delivery samples also rechecked: 575 combined local samples pass. Hosted review: https://sammyt.wtf/melton-v38/ . Nine uploaded gallery/image files match local SHA256; gallery and interior image HTTP200 confirmed. Existing preview.webm retained.
