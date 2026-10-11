# Draw a street route → Blender reconstruction pipeline

**Selected-route survey completed, 11 October 2026:** the supported in-app CUA
collector captured 368 reviewed views across Sam's 1.09 km route, with immutable
originals, hashes, resolved browser URLs and a local evidence browser.
`inapp_capture.cua.js` is the resumable runtime template; browser work must run
through CUA, not an external browser-control library. The earlier metadata
caveat and panorama/position distinctions are recorded in
`../../docs/AUTHORED_ROUTE_SURVEY_2026-10-11.md`. The v57 Blender working copy,
dimensions, limits and review gallery are in `../../docs/SURVEYED_ROUTE_V57.md`.
This used a supervised collector, not a claim of an unattended legacy walk.

**11 October 2026:** [A-to-B planner implemented](ROUTE_PLANNER.md), generated
at `recon/route-planner/index.html`. Click road nodes for A/B/via points, inspect
four directions per proposed stop and export JSON/GeoJSON. Current in-app Maps
and Street View render successfully. Legacy Firefox walker remains available;
new `--output` and cross-route resume rejection keep surveys separate. No new
unattended capture run or in-app collector port is claimed. Older statements
below describing route drawing as future work are historical.

Sam clarified the desired workflow on 3 October 2026: draw a line along roads,
bring that route into Blender, move through street-level views to collect the
surroundings, then build 3D shopfronts like the Pharmacie/Taraj work.

[Concrete pipeline plan and verified sources](PIPELINE_PLAN.md).

Current implementation: [working Firefox capture workflow](FIREFOX_CAPTURE.md).
Sam authorised visible-browser screenshot collection for the personal project.
The collector walks geographic waypoints, saves twelve surroundings/detail views
per stop, records camera coordinates and produces a searchable labelling gallery,
CSV catalogue, contact sheets and camera-route GeoJSON. Originals stay locally
inside the repository under ignored `references/streetview-capture/`.
The [numbered street catalogue](../../docs/street-catalogue/index.html) now
organises all296 captures into68 individual building/feature dossiers, with
separate per-camera files and CSV lookup. Drawing a route remains a future stage;
the first catalogue-led Blender scenery pass is underway. No paid API requests.
The Google usage restrictions recorded in the research plan remain unresolved;
the implementation does not establish redistribution rights.

The earlier idea notes below are historical proposals, not verified permissions.

Sam requested a folder for investigating this after the Melton Road/Taraj pass.
These earlier proposals predate the authorised Firefox screenshot implementation.

Possible workflow to investigate:

1. Input an address, map pin or street segment and identify each desired facade.
2. Find available panorama positions/dates through a supported access route.
3. Estimate frontage heading and choose the panorama closest to its normal.
4. Produce a consistent perspective view, retaining capture location/date.
5. Offer manual corner adjustment for a rectified modelling reference.
6. Store unchanged source, separate derivative and a manifest with provenance,
   coordinates, camera angles, dimensions, edits and confidence.
7. Feed reviewed references into the existing Blender facade workflow.

Limitations to investigate: panorama availability/resolution, occlusion by cars
and trees, facade depth, lens/panorama distortion, capture-date differences,
supported export routes and permitted image storage/use. An angled or obstructed
panorama cannot reliably supply a perfect unobstructed head-on photograph.
Check current official documentation before choosing an implementation.

Follow-up: should the first prototype use manually selected Street View views
and automate rectification/cataloguing, or discover views from an address too?
Budget and API/account preferences matter only if the supported route needs them.

Status: idea recorded; implementation follows completion/review of map work.
