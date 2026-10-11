# Authored Holmdale–Melton–Barkby route working copy — 11 October 2026

Latest editable checkpoint: `assets/blender/pharmacie-surveyed-route-v57.blend`.
Local review: `recon/v57/index.html`. This is a reference-led Blender street
working copy, with approximate scenery and documented adaptations, not an
engine deployment or an exact architectural survey.

## Survey delivered

Sam selected the route in the A/B planner. It starts at
`52.6933508,-1.0789163`, follows Holmdale and Melton, and turns into **Barkby
Road**, ending at `52.698169,-1.0721588`. Length 1,090.7686 m; 92 stops.

368 accepted views (four directions per stop), 381 attempts retained,
90 observed panorama IDs. Originals and hashes are preserved locally in
`references/streetview-capture/authored-route-2026-10-11/`; no source imagery is
embedded in the model. `recon/v53/capture-manifest.json` records source links,
dates, requested and resolved positions, hashes and the early metadata caveat.
The first 45 positions were checked again through the visible Maps URL; that
does not prove every directional frame used the same panorama. Stop 035 ahead
uses the reviewed r3 replacement for a black r2 image. The detailed notes are
`docs/AUTHORED_ROUTE_SURVEY_2026-10-11.md`.

Holmdale imagery is September 2023; Melton includes March 2026 and some April
2023 views. Dates are per image. The 2026 satellite copyright is not an imagery
capture date. Google references stay ignored by Git. OSM-derived geometry
retains attribution to OpenStreetMap contributors, ODbL, in the route data.

## Reconstruction

- V53 corrected the mistaken address pin. Number 29 moved rigidly from
  `(-75.8951,830.6506)` to `(-152.5464,805.5781)`, approximately 75.8 physical
  metres towards the actual end plot. Its approved central diagonal porch,
  mirrored windows, separate plant ledge and perpendicular garage were retained.
- The missing Holmdale stretch is connected. V56 replaces the symmetric
  provisional turning bulb with an approximately 104.2 m² asymmetric carriageway
  outline traced from the north-up end-plot screenshot. The trace, viewport
  calibration and limitations are in `recon/v56/prepared-final.json`.
- V54 adds 60 frontage assemblies: Holmdale houses, station-junction shops and
  green, Victorian bays/retail, modern flats, church/hall, workshop/cafe vicinity,
  supermarket, low commercial strip and the Barkby stretch. The older detailed
  Taraj–town-centre frontages remain. Street furniture includes static crossings,
  lamps, a post box and planted islands. Unreadable business names were not
  invented; shop and house detail is approximate scenery, not surveyed interiors.
- V55 opens redundant boundary infill at Barkby, moves a service wing clear,
  corrects crossing stripe orientation and adjusts a garden rail. V57 moves the
  nine newly added Holmdale assemblies to the correct side relative to the
  retained opposite placeholders; it also rebuilds the terrace dormers at a
  lower, visible height. Trial geometry remains archived unchanged.

## Scale and limits

The retained compatibility frame is **1.0640686466 Blender units per metre**.
Blender's METRIC unit display alone is not physical calibration. New dimensions
use that factor; approved old geometry was not globally rescaled.

Holmdale carriageway width is 5.6 BU = 5.26 m, against an overhead estimate of
5.3 ± 0.6 m. The left house roof frontage is 5.54 BU = 5.21 m, against a rough
5.8 ± 1.0 m estimate. Position tolerance at the traced house corner is about
1.5–2 m. These are pixel/proportion estimates, not tape measurements. The two
geographic length baselines in v53 are consistency checks in the same frame,
not independent surveying evidence. Frontage chainages may differ by 5–12 m
because panorama positions and visible facade projections differ.

The older town layout conflicts with the geographic Barkby centreline. Its
approved buildings were preserved; a short joining bend has a **20.25 m maximum
offset** from the geographic line. This is an explicit layout compromise, not
corrected by calling the model metric. The rest of that new stretch follows the
recorded geographic direction. A closed, labelled static boundary beyond B and
outer containment walls are gameplay adaptations, not observed real fences.

Concealed rear building footprints, roof/plot depth at number 29, individual
retail detail and some station vertical levels remain approximate. This pass
delivers the selected route as a connected, reviewable Blender working copy;
those limitations remain visible for later refinement.

## Verification

- V54: 2,942 new closed meshes / five text objects; V55: 104 closed meshes /
  one text; V56: four closed replacement surfaces; V57: 435 closed copied/new
  meshes. Every new mesh in each build passed manifold and positive-volume
  checks. Superseded objects are archived; no source reference was removed.
- Final selected eleven-route check: **39,771 clearance rays, 4,419 support
  samples; zero blocked and zero unsupported**. Three lateral lanes, radius
  0.42 BU and heights 0.35/1/1.7 BU. Includes the old-map seam, road/pavement,
  station approaches, number 29 drive/porch and the actual traced turning apron.
  The old symmetric-head test endpoint was updated to walk inside the traced
  apron, rather than beyond its new edge.
- Two long lateral enclosure rays miss at junctions (`main/18/-1`,
  `holmdale/0/-1`). This is not a claim of complete map containment. Selected
  ray checks are not continuous capsule collision, BO3 navigation, co-op or
  gameplay tests.
- Direct v40 audit: all **15,512 fingerprints unchanged**, none missing. Five
  obsolete boundary/infill objects are archived, including the original two
  beyond-Taraj closures and three Barkby-opening pieces; remainder infill is
  rebuilt separately. Approved buildings and pub interiors are retained.
- Nine latest Workbench views and earlier fixed-camera before images are in
  the review gallery. Workbench material previews are not photographs.

BO3 files and deployment are unchanged. Git delivery includes the latest
self-contained editable v57 checkpoint, modelling/capture scripts, evidence
manifests, notes and previews. Intermediate v40–v56 Blender milestones remain
locally preserved; they are not all duplicated in this Git delivery. The v57
file includes retained/archived source geometry for future editing.
