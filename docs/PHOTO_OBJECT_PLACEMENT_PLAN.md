# Photo review and Blender object plan

Current file: `assets/blender/pharmacie-photo-interior-v03.blend`.
Source folder: `references/pharmacie-syston/`. All source contents preserved.

## Review evidence

Reviewed 28 reference images on four numbered contact sheets, including two
layout drawings and several duplicate/alternate photo encodings. Selected wide
interior, sofa/skeleton and bar views were also inspected at full size. Image IDs,
original filenames, dimensions and SHA256 hashes are in
`assets/blender/photo-review/catalog.json`. Contact sheets are separate derivatives
in that folder; their presence does not establish additional survey evidence.

| Image IDs | Observed content | Modelling use |
|---|---|---|
| 1, 5, 17 | Instrument boards, black shelves, medicine bottles, jars, skull/medical objects | Wall boards, shelves and bottle proxies; detailed instruments later |
| 2, 12, 20, 21 | Pharmacy adverts, paired lit medicine cabinets, clinical tables, tall stools, raised carpet area | Separate wall surfaces/case frames, medical tables and platform |
| 3, 19 | View towards bar from entrance; timber aisle; raised area on right; suspended tile ceiling; pendants/projector | Orientation of seating and preserved central circulation |
| 4, 9 | Seated skeleton in dentist chair; costume changes across photos | One chair/skeleton landmark, costume not inferred as permanent |
| 10, 22 | View towards entrance; sofa, skeleton and cream chairs along the display wall | Locate sofa/skeleton on left when facing bar; approximate spacing |
| 6, 23 | Drawer-front counter, brass beer pumps, central screen, bottles, black shelves, nearby doors | Bar-front photo surface, pump row, bottle shelves and screen proxies |
| 13, 14, 24 | Occupied room viewed towards street glazing | Density and types of tables/seating; people are not assets |
| 7, 8, 15, 25, 26, 28 | Exterior/entrance daylight views | Asymmetric recess, fixed left pane, double entrance doors offset right, angled displays, moulded black fascia/pilasters, upper sash windows |
| 11, 27 | Night frontage | Fascia lettering, FREEHOUSE, lighting appearance; no inferred geometry change |
| 16, 18 | Earlier user layout and photographed floor plan | Drawing references, not interior photo evidence |

## Coordinate convention and placements

Metres; street at Y=0, rear at increasing Y. X increases to the right when
viewing the frontage head-on. Seven-metre frontage remains an estimate.
Object roots carry their source filenames, observations and placement confidence.
Move the named root Empty to reposition a whole object group. Individual mesh
parts and UVs remain editable.

| Group | Current placement | Evidence and uncertainty |
|---|---|---|
| Finished frontage | Street face, Y approximately 0..0.95 | Photo-led joinery and UV-selected photo surfaces; dimensions estimated |
| Raised seating platform | Right side, X 4.52..6.55, Y 2.2..8.6 | Right-side raised area observed; exact bounds/height unmeasured |
| Medical tables and stools | Three platform groups and two left-side groups | Types directly observed; count and spacing are a practical first pass |
| Brown sofa sections | Left wall near Y=4.5 and 6.0 | Side established from paired forward/reverse views; exact arrangement provisional |
| Dentist chair/skeleton | Left wall near Y=7.7 | Directly observed beside sofa; skeleton is a simple 3D placeholder |
| Cream chairs | Near dentist chair | Directly observed; shapes simplified |
| Medicine display cases | Left wall, Y approximately 5.8..7.2 | Paired cabinets observed; matching photo backing follows the wall bend |
| Bottle shelves/instrument board | Left perimeter and right platform | Shapes observed; exact positions outside the hero wall remain provisional |
| Bar pumps/drawer face | Existing plan bar, Y approximately 10.54 | Photo references validate dressing; plan still governs U-shaped furniture footprint |
| Bottle shelves/screen | Behind bar near Y=13.62 | Contents observed; world spacing estimated |
| Pendant lights/ceiling | Main room and bar | Brass conical lights observed; ceiling hidden for cutaway inspection |

Object inventory and coordinates are machine-readable in
`assets/blender/photo-interior-v03-manifest.json` (34 named groups). These are
editable Blender meshes, not game-ready BO3 assets.

## User corrections incorporated

- Rear outside exit is back-left when facing the building head-on.
- Walk past the toilets towards that exit; the staircase starts on the right.
  Lower flight now climbs across the back (+X), then turns clockwise right and
  climbs towards the street (-Y). Start (0.85,19.85,0), landing
  (4.78,19.85,1.778), arrival (4.78,16.95,3.2). Heights/width are still estimates.
- Men and women have independent doors from the common area; their shared
  divider is continuous and has no connecting door.
- Finished frontage is included in the default interior scene again.

The staircase is an interpretation of the user's route description, rather than
an exact tracing of the contradictory stair symbols on the two drawings. Ground
service partition and upstairs store were adapted locally for this staircase;
upper store was shortened by 0.12m. Headroom/traversal still needs review.

## Texture sources and next detail pass

Original frontage JPEG supplies selected fascia/window/door faces through UVs.
Original bar JPEG supplies the cabinet-front surface. AVIF display wall is decoded
to a separate lossless 1973x1227 RGBA PNG for Blender; no crop, repaint or resizing.
Its original remains untouched. The instrument-board JPEG supplies a UV region.
Images are packed for portability; source rights remain as recorded in reference
README. Current preview lighting and photographic reflections are provisional.

Refine case glass/lighting, individual medical instruments, chair curves,
table glass and ceiling tile seams next. Do not invent upstairs decor from
ground-floor photos: no interior photographs establish kitchen/office/toilet/stair
finishes. Keep a clear central aisle and refine world placement from additional
evidence or user corrections. BO3 export/material conversion remains a separate
unverified step; no game files or playable map sources changed in this work.
