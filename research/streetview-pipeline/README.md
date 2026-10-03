# Automated head-on frontage references — deferred idea

Sam requested a folder for investigating this after the Melton Road/Taraj pass.
No downloader, paid API, scraping process or account setup has been started.

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
