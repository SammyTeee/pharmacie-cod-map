# V06 layout review — no fixes applied

Historical review. Sam subsequently approved all seven fixes; they are applied
in pharmacie-layout-fixed-v07.blend. See MODLOG.md and the v07 manifest for
verification. No new BO3 build yet.

Reviewed current live pharmacie-gameplay-space-v06.blend using world-space
mesh bounds, the ground-floor preview, an upstairs render, and the original
evacuation plan. This is a Blender review; v06 has not been game-tested.
Measurements below are approximate. Bounding-box gaps identify candidate
bottlenecks, rather than prove a complete route cannot be traversed.

| ID | Finding | Evidence | Suggested change |
|---|---|---|---|
| 1 | Stool pinches the approach to the bar | Left-side stool9.0B ends atY14.88m; front counter startsY15.28m, with overlapping X ranges. About0.40m between them, smaller than the approximate0.81m player hull. A detour around the seating is possible. | Move that stool/table group toward the wall or forward, opening a direct route to the left bar passage. |
| 2 | Coffee table is misplaced and too tall | Dentist seating low coffee table lies atY7.14–8.76m beside the two sofa sections; dentist chairs are atY10.94–13.06m. Tabletop is1.19m high, matching a medical table rather than a low table. | Place it with the intended seating group and lower it; separate sofa and dentist seating arrangements. |
| 3 | Front platform furniture overhangs its support | Raised platform beginsY3.30m, but front high stoolA occupiesY2.75–3.35m and its legs end beforeY3.30m. Legs startZ0.27m above the main floor. Front table also extends toY3.17m. | Move the front table/stool set rearward onto the platform, or extend the platform. |
| 4 | Uniform scale made the bar too tall | Main counter topZ1.55–1.67m; approximate standing player hull1.83m tall. Medical table tops1.19m; platform table tops1.46m including platform. | Keep the wider footprints, but reduce fixture/furniture heights independently of building height. |
| 5 | Tight chair/table cluster by dentist seating | Cream chair2 bounds overlap the nearby medical table9.0 bounds aroundX0.21–0.63m, Y12.69–13.06m. Chair1-to-chair2 gap in Y is only about0.58m. These are conservative bounds, not a solid-mesh intersection proof. | Pull the nearby table/stools forward, or rotate/move the cream chairs as one seating area. |
| 6 | Left exterior passage no longer follows the angled wall | Path outer edge isX=-5m. Rear left wall outer edge reachesX=-5.69m; even its inner edge reachesX=-5.27m. Near the back the path lies inside the wall/building rather than outside it. | Rebuild the side passage floor along the sloping outer wall and join it cleanly to the rear landing/street. |
| 7 | Upstairs stair opening needs edge protection and route review | Upstairs render shows exposed voids next to the rear rooms. Downward floor ray at(3.5,29.5)m confirms an opening. Stair rails follow flights but do not guard every surrounding floor edge. | Add landing/void edge rails and confirm approach from upstairs seating to the stair arrival. |

The main centre aisle is broadly clear in the current model; the problems are
specific seating clusters, bar approaches and the exterior passage. Do not
describe all tables as blocking the whole pub.

Upstairs exists in scene02 First floor - mapped rooms: seating area, kitchen,
front/rear offices, stores, separate toilets, and L-stair arrival. Scene05 is a
ground-floor cutaway. Scene03 combines both floors. Evidence:
assets/blender/review-upstairs-v06.png and gameplay-interior-v06.png.

Sampled upward rays at three positions across every stair tread/landing found
no first/ground structural obstacle within1.83m overhead. That is a limited
headroom check, not proof of game traversal, navmesh connectivity or collision.
Photo glazing, small furniture collision and planned zombie/player markers
also need explicit engine conversion before the next game test.

Suggested first selection:1,2,3,6; then decide whether to reduce the furniture
heights in4. No model, game package or source photo was changed in this review.
