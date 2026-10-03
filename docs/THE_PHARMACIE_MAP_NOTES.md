# The Pharmacie Arms — map reference notes

## New floor-plan reference — 2026-10-02

Sam supplied `hq floor plan ai.png` and requested it as the Blender base. It shows both floors with rear service/toilet/store/stairs and subdivided upstairs spaces, superseding the simplified sketch for new modelling. Its provenance/date/as-built status and scale remain unverified; the seven-metre frontage is an estimate. External seating is explicitly labelled proposed. See `BLENDER_WORKFLOW.md` for observations and the packed reference-only Blender scene. Do not treat red fire-safety annotations as wall geometry.

These notes separate what the collected images show from geometry that still needs confirming. The source images and links live in `references/pharmacie-syston/README.md`.

## Confirmed from the reference set

### Street frontage

- The venue is The Pharmacie Arms, at 3 High Street, Syston, LE7 1GP.
- It occupies the ground floor of a red-brick, two-storey High Street building in a continuous row of shopfronts.
- The pub frontage has a broad, nearly black fascia with large white serif “The Pharmacie Arms” lettering and a smaller “FREEHOUSE” line.
- The ground floor has a central glazed entrance with large display windows to either side. The lower portions of the windows are pale blue patterned panels; dark trim/pilasters frame the pub frontage.
- Three tall multi-pane sash windows are visible above the shopfront in the brick upper storey. The pub shares the surrounding street facade with neighbouring retail units.
- Exterior daylight and night/evening photos show how the fascia and shop windows read when illuminated. Preserve the entrance/window rhythm even if gameplay uses boarded windows.

### Main room and circulation

- Several wide interior views show a long, narrow main room with a strong line of sight from the street glazing to the bar at the far end.
- The bar occupies most of the far short wall. A broad dark counter/cabinet face carries multiple rows of drawers and brass-coloured pulls; taps, bottles, shelves, a display/counter and a screen sit above it.
- Small tables and chairs occupy the middle of the room. Bench/sofa seating and themed displays hug the side walls. Preserve a generous central circulation lane for players and zombie movement.
- The ceiling appears low and flat, made of suspended square panels, with regularly spaced pendant lights. The floor is warm-toned wood/laminate in the available images.
- There are signs for rooms upstairs and a door marked “Cash Chemist” in one view. The photos hint at additional rooms or access, but do not establish their layout. Treat these as unknown until the user supplies a floor plan or more views.

### Pharmacy theme and memorable set dressing

- The walls are densely covered with overlapping/repeating vintage medical, beauty, dental, and pharmacy advertisements in muted cream, grey, faded blue, and brown.
- Wall-mounted boards display medical and optical instruments. Lit glass cabinets contain old bottles and packaged products. Shelves hold bottles, jars, tins, and oddities.
- A prominent skeleton sits in a black dentist's chair. It is a distinctive landmark and natural candidate for a creepy set piece or an easter-egg/boss foreshadowing prop.
- Other visible props include dental/optician chairs and equipment, lamps, medicine containers, posters, framed displays, tables, stools, and old cabinets.
- The strongest visual contrast is warm wood and brass against dark cabinetry, pale advert-covered walls, and small pools of yellow cabinet/pendant light.

## Recommended first Radiant blockout

1. Make the pub one long rectangular play space. Put the front door and shop windows on one short end, with the bar wall at the opposite end.
2. Keep a clear central lane from the entrance toward the bar; put tables and movable clutter in side clusters so the room remains playable.
3. Add perimeter seating and one narrow side route/door only after the main loop works.
4. Reserve one wall for the dense pharmacy-ad feature texture and place lit display-case geometry in front where the photo includes cabinets.
5. Use the skeleton in the dentist chair as a silhouette landmark. It can later change state for a scare or boss reveal; it should not block zombie navigation in the first build.
6. Keep the exterior shell and recognizable fascia/windows, but prioritize interior traversal over reproducing the neighbouring shops.

## Still unknown — don't invent as fact

- Exact room dimensions, wall heights, door widths, window spacing, and bar depth.
- Which interior photo is from which end/viewpoint; exact orientation of every side wall.
- Complete ground-floor layout, upstairs layout, back exit, stairs, toilets, and how “Cash Chemist” connects to the main room.
- Current versus older decor; some images may be from different years.
- Desired map scale, start room, intended number of unlockable areas, perks, power, Pack-a-Punch, and whether the map will include an easter egg.
- Noseley's final design, attacks, boss arena, and likeness/style constraints.

## Questions to settle from photos or a sketch

- Which way do you face when you enter from High Street? Is the bar directly ahead, and which side is the stair/side-room access on?
- Are there usable rooms upstairs or behind the bar that should become playable areas?
- What should the first map version include: only the main pub room, or one extra room/yard as well?
- Which details are most personally recognizable and must be preserved even if the playable layout is expanded?

### User layout supersedes earlier inferred blockout

The saved `references/pharmacie-syston/pharmacie-layout.svg` places the bar centrally, toilet and stairs at the back, smoking patio beyond the rear-left wall, and platform at front-right. Use this explicit user layout for the blockout instead of earlier room-wide-photo guesses. Dimensions remain provisional; see SVG_BLOCKOUT.md for implementation assumptions.

Sam subsequently clarified the L-shaped stairs lead to one large empty upstairs room, roughly the downstairs footprint. Sam also approved flat photo frontage/bar/wall/skeleton panels, with the entrance opening positioned from the clear frontage photograph rather than the approximate SVG entrance. Those changes and extra furniture are implemented in the current generator; see PHOTO_MATERIAL_WORKFLOW.md and MODLOG.md for precise assumptions and actual verification.

### Latest supplied plan (2026-10-02)

Use `Architectural Fire Evacuation Floor Plans.png` for the new Blender project. Ground plan labels rear Mens WC/service and stairs; first plan labels kitchen/prep, offices, stores, male/female WC and seating. This supersedes earlier layout guesses for new modelling. Seven-metre street frontage remains Sam's estimate. Proposed external seating and red fire annotations must not be treated as confirmed built geometry. See BLENDER_WORKFLOW.md.

### Photo-led interior evidence (2026-10-02)

All current images, including new WhatsApp files, reviewed and catalogued. Forward/reverse room views place sofa/skeleton along left display wall and raised seating on right when facing bar. Visible objects include medical/glass tables, dark and red-frame stools, cream chairs, paired medicine cabinets, boards/shelves, brass pumps and pendants. Exact positions/counts are inferred; see PHOTO_OBJECT_PLACEMENT_PLAN.md. Sam explicitly located rear exit at back-left when looking head-on, with stairs on right after passing toilets; revised model climbs across back then turns right towards front. Men/women shared wall is solid. These user corrections supersede earlier provisional stair interpretation.

### Historical video evidence (reviewed 2026-10-02)
Blue Van Man's 2019 video shows rear stairs and upstairs banquettes, tables/stools/chairs, carpet, recessed lights, TV, dartboard, bookcase, piano and vintage radios. These are observed historical details, not verified current placement. Compare with supplied plan and newer photos before changing structure. Timestamped review: docs/VIDEO_REFERENCE_REVIEW.md.

Video dressing applied in v10:Sam selected historical upstairs decor. Newer Facebook views show tall fridge beside bar, tap bank, medical panels and dining chairs/tables. Appearance is observed; object coordinates/counts are inferred within enlarged plan. See VIDEO_INTERIOR_PASS.md for timestamps, implementation and limits.


### Street captures supplied 2026-10-03
Observed opposite row includes Floral Fantasy, Let's Move, Syston Mini Market, Aston and Co and Fox and Hounds. Pub-side shots show Wreake Valley Flooring on left, dry cleaners and nail/spa shop on right. V12 uses simple photo scenery with approximate dimensions; left exterior passage stays available. See STREET_PHOTO_FRONTS.md.

V15 second downstairs pass follows observed camera/medicine displays, advert collage, dark dado, jars/ceramics, ceiling grid, pendants and counter/table details in YouTube06:14–07:32 and Facebook135–143s. Counts/coordinates adapted to widened layout. See SCALE_TEST_V15.md.
