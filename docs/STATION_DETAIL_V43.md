# Station detail v43 — provisional saved checkpoint

Update: saved `assets/blender/pharmacie-station-detail-v43.blend`. 118 closed
positive-volume manifold meshes plus three text objects; 16,020 parent objects
retain transforms/datablock references. Initial post/mast approach collisions
were corrected. Final 27,999 selected clearance rays and 3,111 support samples
pass. Not full platform clearance or BO3 gameplay verification.

Mapped shelter 1428872589 exposed a v41 error: it had been treated as a six-metre
building proxy. The unchanged proxy is archived and the schematic low shelter
now occupies its mapped footprint. Matched before views restore the old mass.
Provisional boundary walls still hug the platform; rail corridor, access ramp
and car park remain unfinished. Review: `recon/v43/index.html`.

Sam supplied number 29 and approach images; inspected observations are in
`docs/HOLMDALE_REFERENCE_V44.md`. House modelling and Google overhead comparison
remain unfinished. Sam requested committing/pushing the finished extension.
BO3 unchanged. The build-in-progress notes below are historical.

The current verified saved checkpoint remains
`assets/blender/pharmacie-midland-frontage-v42.blend` until the station build
finishes and its output is inspected.

`scripts/detail_station_v43.py` adds a separately parented station-platform
assembly using OSM platform way 309564449 in the provisional v41 frame. It
adds closed coping/tactile-strip overlays, benches, nameboards, light masts
and a schematic shelter. Furniture positions, dimensions, counts and shelter
design are estimates. Existing road and platform geometry is not moved.

Evidence is recorded in `recon/v43/station-reference.json`: the official
National Rail schematic (not to scale), David Howard's 20 April 2025 station
entrance photograph and Nigel Thompson's 22 September 2012 track/platform
photograph. Source files and rights are in the private extension reference
manifest. The older photograph is historical, not current-state proof.

The first build is running in Blender PID 47036. Read-only stack inspection
confirmed it executing the parent-preservation assertion; CPU time continued
increasing. Do not restart from a tool timeout. Recheck the live process and
saved output, then run `scripts/check_extension_v41.py` and
`scripts/review_station_v43.py` through Blender MCP. Build the local review
with `python scripts/catalogue_station_v43.py`. Inspect the images before
calling the pass visually reviewed. The preservation assertion was optimized
in the on-disk script for future runs; the active run uses the original code.

Still unfinished: station access ramp, car park, rail corridor, Google
overhead comparison of the entire route, visual identification and detailed
modelling of 29 Holmdale Road. Supported-browser inventory remains empty.
No Google alignment has been verified. No BO3 or publishing changes.
