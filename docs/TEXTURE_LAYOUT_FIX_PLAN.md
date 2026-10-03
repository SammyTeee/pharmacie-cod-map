# Texture and street-layout repair review — 2026-10-03

Detailed visual specification now available: [STREET_PHOTO_RECONSTRUCTION.md](STREET_PHOTO_RECONSTRUCTION.md), [PUB_PHOTO_RECONSTRUCTION.md](PUB_PHOTO_RECONSTRUCTION.md) and [RECONSTRUCTION_SOURCE_INDEX.md](RECONSTRUCTION_SOURCE_INDEX.md). Use these source-tagged descriptions for the repair implementation; they describe intended appearance rather than the broken current panels.

Sam requested investigation and a plan before the next repair pass. Reviewed v16 scale export JSON, generated material manifest, exporter/generators and street/passage source scripts. No Blender edit, regeneration, build or deployment performed in this review.

## Findings

- All eight exported shopfronts reference the expected original screenshot, and their generated material entries resolve to the same source. An actual wrong-image assignment is not yet established.
- Several shops intentionally share one complete screenshot texture: Fox/Aston, Lets Move/Floral Fantasy, Dry Cleaners/Nail and Spa. Only their per-panel UV crops distinguish them. An incorrect UV crop or compiled texture-size mismatch could therefore show another shop from the same image. This is a hypothesis requiring Radiant/game comparison.
- `export_scale_test.py` reads only material slot zero and the active UV layer. It chooses the first image node whose Color output has any link, rather than tracing the rendered shader Base Color input. It does not export polygon material indices, shader-selected UV maps, image-node Mapping transforms or evaluated modifiers. These are confirmed conversion limitations, not confirmed causes for these eight panels.
- `generate_scale_test.py` resizes whole screenshots to power-of-two RGB TIFFs (these street images become 2048x1024), keys assets by source path and shares them across materials. Normalized UVs are converted to pixel coordinates using those new dimensions. Resize alone does not prove a crop error; actual converted engine dimensions and patch coordinates must be compared.
- The left neighbour was deliberately placed at X=-13.2..-5.2m to preserve a passage beside the pub. The passage runs X=-4.26..-2.46m at the frontage and follows the skewed pub wall further back. This reflects the previous assumption and conflicts with Sam's new direction.
- Sam's authoritative order, viewed facing the pub: **alley → left neighbouring building → Pharmacie → right neighbouring buildings**. Neighbours should adjoin the pub. Dimensions and rear route remain approximate.

## Planned repair and verification

1. Preserve the latest live Blender state as a safety copy. Inspect material assignments, rendered UV layers and shader links for every affected face. Produce an object/face → image → UV → BO3 material audit; reject ambiguous image selection explicitly.
2. Prove one visibly affected frontage through the existing conversion, comparing Blender, TIFF, generated patch and actual Radiant/BO3 display. Check compiled image dimensions, V orientation, corner order, crop bounds and current deployed package. Diagnose before applying a blanket UV flip.
3. Give each shopfront a separate derivative texture containing its selected facade, with recorded source quadrilateral and perspective rectification where needed. Use full-panel UVs and stable per-front asset identities. This removes dependence on different crops within a shared street screenshot. Preserve source photos and record derivative provenance.
4. Correct exporter material/UV resolution and fail clearly for unsupported shader mappings or per-face assignments until handled. Keep material creation and geometry output tied to the same audited binding; validate actual TIFF dimensions against patch pixel coordinates.
5. Seat both neighbouring buildings against the pub frontage using measured world-space edges. Move the alley to the outer left edge of the left neighbour, provide simple backing/side walls, and reconnect it to the rear exit without crossing the neighbour's mass. Retain street, entrance threshold and interior layout.
6. Render street-level and top-down Blender previews; check front contact, alley width, collision backing, rear connection and outside spawns. Regenerate the separate no-zombie scale test, run official compiler/navmesh, fresh LED and linker, inspect asset warnings and verify complete deployment within existing authorization.
7. Compare actual game shop signs/windows against Blender and walk entrance/alley/rear route. Record exact commands/results and remaining limits. A successful compiler/linker is not visual or traversal verification.

This review establishes the layout cause and conversion weaknesses. It does not yet establish the precise runtime texture failure or claim a working repair.

## Gameplay placement audit and expanded street — subsequent review

Inspected actual `zm_pharmacie_scale.map` prefab origins and matched them to generator coordinates. These are metres in Blender world space before map translation/unit conversion, not prefab geometry centres:

| Object | Current anchor (X,Y,Z)m | Source of placement |
|---|---|---|
| Power switch | (5.8,9.8,0) | Hard-coded original conversion test |
| Mystery box | (0.7,-1.4,0) | Hard-coded, pub-side pavement |
| Quick Revive | (1,1.2,0) | Hard-coded near front interior |
| Shotgun wall buy | (6.4,9.6,0) | Hard-coded original conversion test |

All four prefab rotations are `0 90 0`. The generator has no current-wall attachment, prefab-bound, interaction-clearance or floor-support check. Geometry transforms use the current Blender world coordinates, but these entity coordinates did not follow subsequent layout changes. Blender planning markers are excluded by the scale exporter, and the scale generator moves player spawns separately through source-string replacement. Zombie risers remain inherited interior coordinates; the no-spawn callback disables rounds' spawn loop in this architecture test. This explains the absence of an intentional gameplay layout; exact intersections must be measured using the prefabs' real local offsets/bounds.

Planned placement correction: use explicit named Blender planning anchors and a versioned gameplay placement manifest, rather than inherited arbitrary coordinates. For the next scale test, omit optional power/perk/box/weapon dressing so architecture can be inspected clearly. For the playable map, propose Quick Revive in a sheltered street-start alcove, first wall buy against a solid start-area wall, power on a rear service wall, and box on a rear-yard pad. These are proposed gameplay choices, not venue facts. Preview stock prefab footprints/orientations, snap support to actual floors, provide accessible interaction space, keep entrance/stairs/alley clear, and test activation/purchases in the playable build. Preserve complete required template logic and entity dependencies when omitting optional prefabs.

### New images actually inspected

Seven root `references/*.png` street captures: alley/Wreake Valley/pub continuity; view down High Street from Natural Wellbeing/Post Office; Post Office head-on; right of Post Office; opposite pub; Floral Fantasy; Fox & Hounds/junction. Also inspected three `alt/nattywells/*.png` views and both root v16 broken-shopfront game screenshots. Originals untouched.

Observed street structure: attached brick shop terraces with pitched slate roofs/chimneys, projecting upper bay windows above Floral Fantasy/Let's Move, Post Office beside Papermoon and Pasha Barber, side access between Natural Wellbeing and Post Office, signal-controlled crossing with zigzag approaches, kerbs and varying pavement edges, parking markings opposite the pub, and a junction/traffic island beside Fox & Hounds. The supplied alley image directly shows Wreake Valley adjoining Pharmacie with alley beyond Wreake Valley. Exact distances and full pub-side extended shop order are unresolved. 'Floral Fantasy shut down' comes from Sam's filename; the screenshot shows obscured display windows and does not independently establish trading status.

Street proposal: replace the isolated 50m straight strip and thin facades with a connected blockout reaching the Post Office/crossing end and Fox & Hounds junction, with Natural Wellbeing as a landmark at the crossing end. Use simple closed building masses, pitched roofs and side walls on both sides; photo fronts only for recognizable visible shops, stock-material placeholders for gaps and distant buildings. Model crossing/road bend/parking/kerbs from observed references; do not copy the generic centre dashes and continuous yellow lines indiscriminately. Keep an explicit playable street area and block scenery interiors/distant exits deliberately. Set gameplay-scaled distances from a consistent street plan, with uncertain dimensions recorded. Expand sky/player bounds and review navmesh/spawn locations after geometry changes.

The v16 game screenshots confirm architecture loads and that individual panels show extensive source-street content, including adjacent shops/sky, instead of the intended isolated facade. This strengthens the UV/crop interpretation but does not yet isolate whether patch pixel-coordinate interpretation, asset dimensions/cache or another stage causes it. Per-facade derivatives plus a small engine UV calibration remain the planned repair.

Current images suffice for an initial extended street blockout. Additional Street View capture should target only missing pub-side frontage/order or the alley's rear connection if required; no live Street View session performed in this review.
