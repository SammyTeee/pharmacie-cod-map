# Taraj interior and bridge — Blender v26

[Editable Blender checkpoint](../assets/blender/pharmacie-taraj-interior-bridge-v26.blend)
· [Detailed interior reference notes](TARAJ_INTERIOR_REFERENCE.md)

This pass fits a detailed restaurant into the approved Taraj exterior, retaining
its opposite-road placement and pub-scale upstairs windows. The pub, other
High Street fronts and fridge adjustment remain in the scene. V25 is preserved.

## Taraj dining room

Eight booth bays, twisted hardwood posts, smooth scalloped headers, transparent
etched dividers, floral fabric, damask-style walls, timber ceiling boards,
recessed practical lights, air-conditioning cassettes and a central pillar.
Two central dining-table runs have16 wood-framed upholstered chairs. Booth and
banquet tables have linen drops, plates, folded napkins, cutlery, wine glasses
and small flower vases. The left passage opens into the restaurant.

![Dining room at player height](../recon/v26/01_taraj_dining.png)

![Booth joinery and glass](../recon/v26/02_taraj_booths.png)

The first left booth's front bench is archived to form an arrival landing. This
is a deliberate gameplay adaptation. Two longitudinal aisles remain clear;
27 multi-height/width ray checks cover the entry and aisles, supplementing64
initial aisle segments. These are geometry checks, not BO3 navigation tests.

![Lit entrance from the passage](../recon/v26/05_taraj_entry.png)

![Temporary ceiling-hidden layout view](../recon/v26/10_taraj_cutaway.png)

## Bar and requested booth guest

The compact bar has a hollow cabinet, glass fridge doors, shelves and bottles,
interior fridge lights, countertop, register, beer tap, inverted spirits bottles,
connected optics, simple labels, glass shelving and violet LED strips.

![Bar and illuminated fridge](../recon/v26/03_taraj_bar.png)

The man requested in the source filename is placed in a booth as a static
reference-photo silhouette with a modelled beer glass. This remains a photo
cutout placeholder, not a rigged character or a finished3D likeness.

![Requested booth guest reference](../recon/v26/04_taraj_guest.png)

## Bridge, brook and side access

The shallow disconnected strip is replaced with a continuous87m watercourse,
estimated1.44m below the road, sloping/outer banks and an underside deck with
abutments. Pale railing bases and grey metal rails follow the observed treatment.
Simple trees/shrubs, heritage-style columns, fencing and parking context are
placed separately. Vegetation remains a modelled placeholder.

![Bridge and surroundings](../recon/v26/06_bridge_overview.png)

![Looking down the brook](../recon/v26/07_bridge_brook.png)

![Bridge supports and railing](../recon/v26/08_bridge_side.png)

![Road and brook plan](../recon/v26/09_bridge_access_plan.png)

The Banking Hub rear is shortened and its corner cleared around the retained
side road.19 centreline overhead samples pass. Pavement/kerb cuts clear the
branch mouth; its surface is raised6mm to separate the formerly coincident road
meshes. Final render review removed an isolated rear-wall sliver from the first
clearance operation and added ground beneath outer-bank trees.

## Source, limits and reproduction

Restaurant footprint8.8×13.85m, booth spacing, rear/service connections, bar
footprint, brook depth and supports are estimates. Unseen kitchen/toilets are
not invented. Fabric and etched art are procedural interpretations of the photo.
The rear service door is scenery; bought doors/zones/zombie routes need Radiant.

Build sequence, starting with saved v25:

1. `scripts/build_taraj_bridge_v26.py`
2. `scripts/review_taraj_v26.py`
3. `scripts/finish_bridge_v26.py`
4. `scripts/check_taraj_entry_v26.py`
5. `scripts/frame_taraj_entry_v26.py` — optional camera-only framing correction.
6. `scripts/verify_taraj_bridge_v26.py` — reads the final saved checkpoint.

Use Blender5.2 `--background <input.blend> --python <script.py>`. Each corrective
script is applied once to the preceding checkpoint state. Sources and generated
solids: [validation manifest](../recon/v26/validation.json). Final saved-file
checks: [final validation](../recon/v26/final-validation.json). Logs remain under
ignored build/. Original reference bytes are unchanged. Superseded meshes are
archived in unlinked collections. New images/materials needed by the scene are
packed; local reference screenshots are not newly distributed as separate files.

All ten images are Cycles Blender inspection renders,1400×1000,20 samples.
Exterior review sunlight and cutaway visibility changes are temporary; practical
restaurant lights are saved. No new Radiant export, compiler run, deployment or
BO3 test occurred.
