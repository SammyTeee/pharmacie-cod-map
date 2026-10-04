# Taraj interior: observations and modelling decisions

Source originals remain unchanged in `references/`. This note is selective
reconstruction evidence, not a surveyed floor plan. SHA256 values are recorded
by the v26 build in its validation manifest.

## Dining room — taraj interiopr.png

The photograph looks lengthwise down a long restaurant. Booth partitions repeat
on both sides, with a line of dining tables and high-backed chairs through the
centre. The rear is darker and appears to have a closed service door. The image
does not establish rear room connections, kitchen or toilets.

Each booth division has a solid dark wood lower panel, a transparent/etched upper
panel, thick horizontal timber rails and twisted timber columns at the inner
ends. The columns have squared/collared bases and capitals, with spiral relief
between. Dark polished joinery contrasts with pale line art on the panels.
Figures, peacocks, floral motifs and curving outlines appear in the etching;
the v26 fine-line floral/paisley treatment is an interpretation, not a copy of
those illustrations. Repeated scalloped/pointed arch shapes occupy the top band
between the column capitals and ceiling. Small pale table-number plaques sit
near the capitals.

Booth seats and chair backs have brown/gold floral fabric. Chairs have substantial
wood surrounds, separate legs and tall cushioned backs. Tables are dressed in
white/ivory cloths with hanging edges, individual plates, folded napkins, wine
glasses and cutlery. Small vases with flowers sit on the long central table run.
Central tables appear joined for a large group in this photographed arrangement;
that arrangement need not be permanent.

Ceiling boards/slats are glossy warm honey timber, running across the room in the
image. Small recessed downlights repeat along both sides. White ceiling cassette
air conditioners interrupt the timber. A square central pillar with patterned
lining and a heavier capital sits within/along the centre dining arrangement.
Walls have pale tan/gold ornamental wallpaper. The floor reads as dark brown
carpet. Exact fabric repeat, wallpaper motif, timber species and dimensions are
unknown; procedural stand-ins retain the colour/texture relationships.

## Bar — taraj bar inside right inside of the left side door -.png

The source filename locates this immediately inside, on the right after entering
through the left-side door. The photo shows a compact bar/service counter,
ornamental wallpaper, glossy timber ceiling and recessed downlights. A high rack
of inverted spirits bottles feeds separate optic dispensers. Brackets and dark
timber supports are independent of the bottles. Below are glass shelves, reflected
lights/bottles, and a partly mirrored corner with a diagonal division. Violet/pink
LED light traces the shelf edge. Lower bottles and a small register sit on a dark
countertop. A beer tap stands at the right. The cabinet below has illuminated
glass fridge doors, two visible shelves and assorted bottled/canned drinks.
The small food-allergy notice is a separate mounted plaque.

The photograph establishes fixtures and appearance well but not the full bar
footprint or how it connects to the main room. V26 places a compact model just
inside the passage-to-dining opening, leaving circulation around it. The mirrored
corner geometry is simplified; stock/brand identities are approximate.

## Requested booth guest

`inside taraj THIS MAN MUST FEATUURE SAT IN ONE OF THE BOOTHS.png` explicitly asks
for the photographed man in a booth. It shows a seated older man with glasses,
short grey hair, a pale checked short-sleeved shirt, and a beer glass in one hand.
The booth behind has etched figures and a twisted dark timber divider. The image
also has a large blank right margin and Google overlay; neither is architecture.

V26's first render used a rough seated reference model; review replaced it with
a static source-photo silhouette selected by mesh boundary and UVs, plus a
modelled beer glass. This is a likeness placeholder with no rig, animation or
BO3 actor setup. No full room image or
Google overlay is mapped onto a wall. Silhouette selection method and source hash are
recorded; source is never cropped/recompressed on disk.

## Estimated layout and playable-space decisions

Retain the approved opposite-road Taraj exterior. Replace the former solid
ground-floor closure with a fitted8.8m by13.85m restaurant shell. Those dimensions
come from the existing gameplay-scaled frontage/depth, not a building survey.
Eight booth bays are distributed down the side walls. Sixteen chairs surround
two central table runs, separated around a square pillar. Two longitudinal paths
remain between the booths and central dining furniture. The first left booth's
front bench is omitted to clear the entrance landing, a gameplay adaptation.
The left passage door
stands open, with a new side opening into the dining room. The right frontage
door remains closed scenery. Rear service door is a placeholder; no unseen
kitchen/toilet layout is asserted.

Future Zombies door purchases, navigation, collision and spawn/barrier placement
need explicit Radiant implementation. The current furniture is Blender scenery;
rendering successfully does not verify enemy pursuit or cooperative movement.
