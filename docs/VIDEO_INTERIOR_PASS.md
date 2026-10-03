# Video-led Blender interior — 2026-10-03

Latest file: `assets/blender/pharmacie-video-details-v10.blend`. Earlier v08/v09 and live safety copies preserved. Radiant rebuild remains on hold. No game installation writes, game closure, compilation, deployment or push performed.

## Detailed reference extraction

- YouTube q0zBpicUXjg: 471 additional full-resolution 1280×720 frames at one-second intervals over 05:50–09:00 and 10:10–14:51. Four dense sheets show 95 candidates selected for local sharpness over five-second windows. All four reviewed, alongside full-size chosen source frames. Earlier 114 ten-second samples and selected tour retained.
- Facebook share/v/18ZXq1yVKY resolves to video 4498935063696316, uploader The Great British Pub Crawl, upload metadata 2026-09-18, duration 146.703s. Downloaded 1080×1920 MP4 into ignored build/video-reference. Its actual picture is a landscape strip inside a portrait edit with caption bars; resolution of the downloaded container does not mean a 1080×1920 pub photograph.
- Extracted 294 full-size Facebook frames every half second across the entire video. Twenty-five portrait sheets retained. Eleven additional detail sheets omit the editorial bars from previews only, showing every half-second from 54s onward at a readable size. Reviewed all eleven detail sheets plus opening exterior and sampled interview sheets. Original decoded stills untouched. Raw videos remain local ignored files.
- Laplacian variance is a blur-selection heuristic; visual inspection determined usable crops. Sharp editorial text can inflate scores. Neither source is a measured survey.

## Observations and implemented objects

| Evidence | Implemented in Blender | Placement confidence |
| --- | --- | --- |
| YouTube 10:52–13:30 upstairs | Six banquette sections, six side tables, twelve stools; carpet, music posters, TV, circular dartboard, bookcase, games, upright piano with keys/bench, four radios and recessed-light trim | Decor observed; positions/counts adapted to current plan and enlarged gameplay footprint |
| YouTube stair climb 10:31–10:42 | Timber stair material and eighteen thin metal nosings | Appearance observed; existing user-corrected stair direction retained |
| Facebook 61–69s | Tall beer fridge with framed door, handle, vent and photo shelf contents beside bar | Prop observed; approximate position leaves left passage available |
| Facebook 87–108s | Tap-bank photo backing, mug/glass props | Observed behind bar; current counter geometry retained |
| Facebook 71.5s | Mild and Original pump-badge crops on separate editable surfaces | Names/appearance observed; approximate placement |
| Facebook 123–140s | Dental instrument board, medical adverts and Band-Aid panel | Observed wall detail; small surfaces placed on existing wall |
| Facebook 114–146s | Two downstairs table/chair groups; two centre groups upstairs using older upstairs evidence | Furniture observed; expanded spacing retained for playability |
| YouTube 11:24–12:48 | Reflective upstairs framed mirror | Modelled reflection instead of baking the camera operator into a photograph |

V09 added 353 meshes and twelve packed native PNG crops; v10 added 101 meshes and eight further packed crops. Each crop manifest records exact source frame, SHA256, pixel rectangle, dimensions and status. Crops retain actual lighting/perspective/reflections; no invented detail, upscaling or AI repaint. Posters and radio faces are usable at their modelled size; video crops are not seamless/PBR or verified BO3 materials.

## Review and limitations

Rendered upstairs/downstairs with temporary cameras/lights removed afterwards. Corrected bookcase/banquette overlap by moving thirteen bookcase/game parts into clear rear corner. New objects parented to existing gameplay scale with inverse transform preserving placement. Static assertions confirm upstairs centre furniture ends before Y17m, rear doorway approach row stays available, bookcase beyond banquette, and fridge left of counter. Room planning text remains visible in viewport but hidden in renders.

Positions remain inferred; the latest plan's kitchen/offices/toilets/doors remain in place. Video room proportions differ from deliberately widened gameplay space. Tiny props are simplified. Compile/navmesh/player traversal and custom BO3 material conversion remain pending the next authorized Radiant pass. Historical upstairs decor was explicitly selected by Sam. Original source photographs were not edited. Reference-source redistribution rights are not established.

Reproduction scripts: prepare_video_textures.py, crop_video_panels.py, dress_video_pub_blender.py, review_facebook_video.py, facebook_detail_sheets.py, crop_facebook_panels.py, dress_facebook_pub_blender.py, finish_video_dressing.py, preview_video_details.py. Blender scripts use the project live bridge and version guards; do not rerun them over existing versions.
