# Melton Road street life v36

Checkpoint: `assets/blender/pharmacie-street-life-v36.blend`, built from v35.
[Matched player-height review](../recon/v36/index.html).

Sam asked for more street content and textures to make the Melton Road walk more
interesting. This first street-dressing pass adds 300 closed solids: intermittent
asphalt utility-trench repairs with sealed edges and ribbed inspection covers,
and ten shallow frontage clusters alternating timber benches, concrete planters
and ribbed litter bins, with layered notice cabinets. New procedural asphalt
aggregate, timber grain, concrete, soil and painted-metal materials give these
features separate surface character. Asphalt replacements are separate materials;
shared originals and the pub/Taraj interior materials are retained.

These are inferred Zombies street adaptations, not surveyed furniture locations.
Frontage furniture is within 70cm of selected facades; carriageway repairs have
only millimetres of relief. Existing buildings, vehicles, crossings, bridge,
street layout and interiors remain retained. Notice sheets are generic shapes,
not claims about actual shop notices. Plants are simple placeholder geometry.

Reopened-file checks: 300 manifold positive-volume solids, 13,077 parent mesh
geometries preserved, all 44 original reference hashes unchanged. 3,429 road
and 572 retained pub/alley ray samples pass at 0.42m radius. These do not check
all pavement routes, benches for passing/revives, continuous collision, or BO3
navigation. Engine files and deployment remain unchanged.

The long street still needs stronger distinct focal scenes and more individually
finished pavement/frontage surfaces. Possible next work: a reference-led shelter,
cycle parking, a delivery/loading scene and the enclosed Town Square passage.
These remain future proposals, not included or implemented gameplay.

Reproduce: `scripts/detail_street_v36.py` on v35;
`scripts/check_street_v36.py` on v36; `scripts/inspect_street_v36.py` on v35/v36.
Use `V36_REVIEW_ONLY=03_melton` or `05_taraj` for compact matched renders.
Logs: `build/v36-*.log`. No hours-long render, engine conversion or upload.
