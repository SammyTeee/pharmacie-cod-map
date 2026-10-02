# The Pharmacie Arms, Syston — map references

## Council-plan reference and estimated Blender scale (2026-10-02)

`floor plan of downstairs and upstairs council to scale.png` is a user-supplied 1264×874 raster floor-plan reference. Filename suggests council provenance, but document date, source URL, original page scale and as-built status have not been independently established. Source remains unchanged. Sam estimates frontage at 7m and has no confirmed measurement. Blender uses that estimate and the original plan's proportions in separate UV reference planes; see `../../docs/BLENDER_WORKFLOW.md` for pixel anchors, regions and verification. `hq floor plan ai.png` in the repository root is the clearer supplied composite reference; use the original council-plan raster for tracing rather than treating AI cleanup as surveyed geometry.

These images are for private visual reference while blocking out the Call of Duty: Black Ops III map. The exterior images came from the Acuitus listing for 3 High Street, Syston:

- `exterior-high-street.jpg` — street frontage and neighbouring shopfronts. Source: https://www.acuitus.co.uk/uploads/122-5498/3-syston-main-1600x900.jpg
- `exterior-pubfront.jpg` — wider view along High Street. Source: https://www.acuitus.co.uk/uploads/122-5498/Syston-3-High_9174.jpg

Useful pub-specific interior references are listed by CAMRA and Pubs Galore:

- CAMRA venue page, including bar photographs: https://camra.org.uk/pubs/pharmacie-arms-syston-174360
- Pubs Galore picture gallery and interior descriptions: https://www.pubsgalore.co.uk/pubs/87288/
- Restaurant Guru photo gallery: https://restaurantguru.com/Beer-Pharmacie-Cask-and-Tap-House-Queniborough

The web-hosted interior images are linked rather than copied here. The current public search results surfaced two useful exterior photographs but did not provide stable, downloadable interior image files. Your own photos will be especially valuable for room dimensions, door/window positions, the bar and display details.

## Additional collected photos

The project folder also contains the locally collected pub photos. Particularly useful for mapping:

- `pharmacie-arms-syston-1.jpg`, `images.jpg`, and `87288_9216d8f5.jpg` show the long main room from different positions. They establish a front-to-back sightline, entrance glazing at the street end, seating along the side walls, and the bar/display wall at the far end.
- `bar front.jpg` is a clear straight-on bar reference, including the broad dark cabinet-front counter, drawers, taps, shelves, and overhead lights.
- `eyJidWNrZXQiOiJ3aGF0cHViIiwia2V5IjoiTEVJXC9MRUkrNTI1LTExMjUxNy0yNDAwLTE4MDAuanBnIiwiZWRpdHMiOnsicmVzaXplIjp7IndpZHRoIjo4MDAsImhlaWdodCI6NjAwLCJmaXQiOiJjb3ZlciJ9LCJyb3RhdGUiOm51bGx9fQ==.jpg` and `eyJidWNrZXQiOiJ3aGF0cHViIiwia2V5IjoiTEVJXC9MRUkrNTI1LTE2ODI1NC0xNTAwLTIwMDAuanBnIiwiZWRpdHMiOnsicmVzaXplIjp7IndpZHRoIjoxNTAwLCJoZWlnaHQiOjIwMDAsImZpdCI6ImNvdmVyIn0sInJvdGF0ZSI6bnVsbH19.jpg` show the pharmacy-themed wall displays and skeleton/dentist chair.
- `87288_fa420e50.jpg` has another view of the skeleton character and its costume.
- `pharmacie-arms-syston-2.jpg` shows the current frontage and signage.
- `53737352757_c7dacdf5d8_c.jpg` is the strongest wide wall reference so far: it clearly shows the repeated vintage advert wallpaper, lit display cabinets, medical objects, and seating. It is useful as a texture source after cropping/straightening a clean wall section; the full photo has perspective and foreground furniture, so it should not be applied unchanged to a large flat surface.
- `textures wall.jpg` is a close, mostly head-on view of the advert wallpaper and optician display. Good for extracting small wall panels and prop/decal details, though it is portrait-oriented and includes display objects.
- `aaaa.jpg` and `2.jpg` are detail references for shelves, bottles, instruments, posters and the skeleton. Their perspective and lighting make them better as modelling/reference images than as direct wall textures.
- `great for texture.avif` is also in the folder; inspect it and make a separate derivative after confirming the BO3 material pipeline and accepted image format.

### First-pass blockout notes

Treat the main bar room as one long, narrow rectangle for the first Radiant blockout. Put the street entrance and front windows at one short end, the bar against the opposite end wall, and leave a readable central lane for Zombies and player circulation. Add seating/booths around the perimeter, then use the pharmacy display wall and skeleton chair as strong visual landmarks. The photos do not establish exact dimensions, side-room connections, stairs, or the upstairs plan; keep those as placeholders until we have a sketch or measurements.

For custom wall art, use the straight-on sections as source material, crop to a flat panel, correct any remaining perspective, and split dense display compositions into smaller wall panels/decals. Preserve the high-resolution originals as references and make separate game-ready derivatives for BO3 rather than replacing the originals.

CAMRA describes the venue as a former shop with a 1950s pharmacy theme, medical artefacts and a skeleton in a dentist's chair. Treat the downloaded exterior photos as visual reference; check image rights before redistributing them with a released map. The BO3 Mod Tools format/pipeline replaces the earlier WaW plan; originals remain unchanged and any game-ready derivatives should be separate files.

## Saved floor plan (2026-10-02)

`pharmacie-layout.svg`, `pharmacie-layout.jpg`, and `pharmacie-layout.json` are Sam's exports from the interactive planner, preserved unchanged. They are user-authored layout references, not venue photography. The SVG's rendered geometry now drives the blockout generator; see ../../docs/SVG_BLOCKOUT.md. JSON size metadata is inconsistent and is not used for map dimensions.

## Photo-panel derivatives (2026-10-02)

Sam approved flat photographic frontage, bar and wall panels, plus a skeleton cutout. `pharmacie-arms-syston-2.jpg` is the clearest head-on frontage source (1024×751); its central right-hand door is cut through the geometry. `bar front.jpg` supplies drawers and upper bar detail; `great for texture.avif` supplies non-tiling pharmacy panels. The supplied 1500×2000 skeleton/dentist-chair photo supplies an AI-isolated transparent cutout. Originals remain unchanged. Derivatives, hashes and conversion recipes are separate in `assets/photos/manifest.json`; see `docs/PHOTO_MATERIAL_WORKFLOW.md` for source-pixel UV crops, material settings and build steps. No distribution rights are inferred from private-use approval.

## Latest evacuation-plan source (2026-10-02)

Sam supplied root file `Architectural Fire Evacuation Floor Plans.png` (1393x1129) for a new Blender project. Source unchanged; origin/date/as-built status unverified. Packed original and UV reference regions are in assets/blender/pharmacie-evacuation-plan.blend. SHA256 and estimated 7m calibration are recorded in assets/blender/evacuation-plan-manifest.json; no source image edits made.

## Full Blender photo review (2026-10-02)

New WhatsApp images reviewed alongside all earlier photos. assets/blender/photo-review/catalog.json records 28 original reference images with SHA256 and dimensions (includes 2 layout drawings); four labelled review sheets are separate derivatives. Sources remain unchanged. Feature-wall AVIF decoded separately to assets/blender/photo-review/feature-wall-lossless.png (1973x1227 RGBA, no crop/resize/repaint). Packed originals/UV regions supply the Blender frontage, drawer front and instrument panel; see docs/PHOTO_OBJECT_PLACEMENT_PLAN.md and photo-interior-v03-manifest.json. WhatsApp provenance/date/ownership is user-supplied and not independently established; some views duplicate earlier pictures. No distribution permission inferred.
