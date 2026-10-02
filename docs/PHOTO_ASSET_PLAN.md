# Photo-to-asset plan

## Recommendation

Use the photos in two different ways. Build the pub's shape, collision, doors, bar, cases, furniture, and boss arena as real Radiant geometry or validated game models. Use selected near-frontal photo regions as custom wall panels, posters, cabinet inserts, and small decals. Do not turn a full-room photo into the whole map, and do not use a Gaussian splat as gameplay geometry.

BO3 needs game-native materials and collision; a photo plane alone would not let Zombies navigate around the bar or furniture. A splat may later help with visual reference or a static showcase, but it is not the first asset route for the map.

## Ranked photo candidates

| Reference | Best use | Assessment |
|---|---|---|
| `great for texture.avif` | Feature-wall atlas/panel | 1973×1227. Strongest photo-texture candidate: broad, nearly frontal wall view, with vintage adverts and illuminated display cabinets. Use as a non-repeating hero panel; crop, straighten, color-correct, and decide whether to retain or separately model the cases/objects. Do not tile across many walls. |
| `textures wall.jpg` | Poster/instrument wall panel | Close view with a relatively square-on central optical instrument board and surrounding advert wallpaper. Crop a clean region; likely make the board and surrounding wallpaper separate pieces so one can be modelled and lit. |
| `53737352757_c7dacdf5d8_c.jpg` | Wide wall layout and smaller poster panels | Shows the themed wall, shelves, lit cabinets, table/chairs. Useful for composition; perspective and furniture at the bottom mean it needs a tight crop and is less clean as a flat whole-wall texture. |
| `bar front.jpg` | Bar model and possible cabinet-face material | Frontal, wide view of the dark drawer-front counter, taps, shelves, and top lighting. Prefer modelling taps/shelves and geometry; a cropped cabinet-face image may provide surface wear/detail. |
| `aaaa.jpg`, `2.jpg` | Prop modeling and decal references | Angled close-ups of instruments, bottles, skull, and wall adverts. Strong visual references; poor direct wall-texture candidates due to oblique view, occlusion, and mixed lighting. |
| `images.jpg`, `pharmacie-arms-syston-1.jpg`, `87288_9216d8f5.jpg` | Layout and circulation reference | Wide room views with people and tables. Use for room proportions and placement, not textures. |
| `87288_fa420e50.jpg` and skeleton-chair close-up | Skeleton prop reference | Use to shape a recognizable seat/skeleton set piece. A 2D image/decal could dress the wall behind it; gameplay prop should be 3D if it is visible from multiple sides or blocks movement. |

## Derivative workflow

1. Keep every supplied/downloaded source unchanged in `references/pharmacie-syston/`.
2. Pick a crop that is close to head-on, with the four wall edges as parallel as possible. Record the chosen source and pixel crop in a manifest.
3. Correct lens/perspective and uneven white balance gently. Avoid AI repainting text or inventing medical labels; tiny vintage text may be unreadable at game distance anyway.
4. Decide whether the photograph includes real 3D elements that should instead be modelled (display cases, bottles, chairs, instruments). For the main feature wall, a photo-baked panel can be an efficient first pass; later separate high-relief cases/props for stronger lighting and depth.
5. Inspect BO3 source texture dimensions and the Mod Tools material/build pipeline, then create a separate derivative at a compatible size/format. Do not guess final compression or format before checking the installed tools and sample assets.
6. Compile one material onto one test wall and view it in game. Adjust scale, mip/detail, brightness, and readability before creating the rest of the set.
7. Record derivative paths, source attribution/rights, edits, dimensions, material names, and in-game result in an asset manifest and `MODLOG.md`.

## Rights and quality

### Implemented prototype route — 2026-10-02

Sam approved flat photo panels. The clear frontage, bar, AVIF wall and full-length skeleton reference now have separate derivatives and map meshes. Crops use mesh UVs rather than modifying source photos. The skeleton cutout uses imagegen background isolation. See [PHOTO_MATERIAL_WORKFLOW.md](PHOTO_MATERIAL_WORKFLOW.md) and `assets/photos/manifest.json` for exact sources and settings; MODLOG.md records compilation and runtime evidence. The feature wall still includes photo-baked cabinets in this first pass.

Keep local reference copies for this project. Before releasing a map, confirm whether externally sourced photos/poster artwork may be redistributed or baked into the map; where permission is unclear, recreate original vintage-inspired adverts and use the photos only as reference. User-supplied photographs can be used as project references, but keep provenance with each source.

### Blender photo-led object pass (2026-10-02)

Editable Blender source now includes 34 photo-inspired groups and packed-photo UV surfaces. See PHOTO_OBJECT_PLACEMENT_PLAN.md for evidence, placements and assumptions. Originals remain unchanged; AVIF feature wall has a separate lossless PNG of original dimensions for Blender. This is modelling source only, not a newly verified BO3 material/export. Final glass, lighting and photo reflections remain to refine.
