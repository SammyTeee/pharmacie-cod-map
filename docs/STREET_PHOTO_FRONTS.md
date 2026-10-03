# Street photo fronts — 2026-10-03

Current Blender source: `assets/blender/pharmacie-street-details-v12.blend`. Includes all v10 video interiors and v11 opposite-street scenery. Live safety copies preserve unsaved user state before each pass.

Five opposite fronts: Fox and Hounds, Aston and Co, Syston Mini Market, Let's Move estate agents and Floral Fantasy. Three new pub-side neighbours: Wreake Valley Flooring to the left; Syston Dry Cleaners and nail/spa shop to the right. Building order comes from photos. Widths, heights and offsets are approximate gameplay scenery rather than surveyed geography.

All six supplied root Street View PNGs inspected. Three opposite views supply chosen UV regions; the further-right view is supporting/overlapping evidence. The two new adjacent-shop views supply their own panels. Originals are packed unchanged; no raster crop, repaint or recompression. Pixel quadrilaterals, original dimensions, SHA256 and placements are recorded in `assets/blender/street-fronts-v11-manifest.json` and `street-details-v12-manifest.json`. Captures show Google Street View Apr2026 UI; source rights are not established for distribution.

Faces are separate editable photo meshes with shallow solid backing. Windows, signs and depicted doors are visual details; shops have no playable interiors or functional doors. Perspective, baked shadows, occlusions and occasional map pins remain in source regions. Crops omit browser UI and most road/car content, though a partial car remains at the bottom of Fox/Aston region. Small source details cannot be reconstructed through UV mapping.

Sam's `blender preview.png` showed broad blank surfaces above the opposite fronts. Live world-space inspection confirmed photo faces already extended from Z0.1m to wall/eaves height. The broad strips were exposed 4.2m-deep backing tops and 4.35m-deep flat roofs seen from above. V12 reduces opposite backing depth to0.32m and cap depth to0.40m, adds five photo slate roof strips, and preserves photo face/door height. This suits the requested simple 2D scenery. Pub-side backing is0.36m deep. Left neighbour ends atX-5.2m to preserve the approved exterior passage beside the pub.

Street fronts linked into scenes01/03/04/05. New lamp-post positions are illustrative. Existing road, pavements, outside-spawn/zombie planning markers and detailed Pharmacie frontage retained. Preview renders use temporary cameras/lights removed afterward; they are not game screenshots. No Radiant rebuild, compile, deployment, game closure or push performed. BO3 photo material/mesh conversion and traversal still pending the next authorized engine pass.

Scripts: add_street_photo_fronts.py; fix_street_fronts_and_neighbours.py; preview_street_details.py. Use version guards and preserve existing saves when reproducing.

V13 Mini Market correction: the v11/v12 crop clipped the lower shopfront and roof. Expanded the UV selection on the same original zoomed-out flat screenshot to include the full building face. Exact corners and original hash: assets/blender/mini-market-v13-manifest.json. Original parked car remains an occlusion; redundant sampled slate strip hidden. Latest Blender file: pharmacie-street-details-v13.blend.
