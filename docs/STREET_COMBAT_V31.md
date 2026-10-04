# V31 street combat layout — 2026-10-04

Checkpoint: `assets/blender/pharmacie-zombies-street-v31.blend`.
Preview: [before/after gallery and compact video](../recon/v31/index.html).

Four original procedural vehicles give the road useful cover and interrupt long
sightlines: a pub-side hatchback, opposite-side delivery van, damaged car farther
along and a wreck near the closed east end. These are Blender preview props,
not imported BO3 models. The installed Mod Tools contain the civilian compact
car model, textures and collision source; future Radiant conversion can evaluate
that stock asset without copying it into this repository.

Closed road-end boundaries, a service-lane gate, entrance bollards, shallow
planters and supply crates replace indefinite empty stretches with bounded
spaces. Deep terrain backing closes downward views into the surrounding void;
it does not finish the junction's accurate pavement/road outline.

The v30 rear alley, pub and Taraj remain. Zombies is the priority; possible PvP
reuse is future work. Gate/reward markers are proposals only. Parking positions
and road closures are gameplay adaptations, not photographed facts.

Saved-file checks: 572 retained pub/alley samples and 1,248 street samples at
0.42m radial clearance pass. Opposite pavement route bends around existing
Natural Wellbeing bollards; it avoids the crossing pole. The legacy floor-name
classifier excluded kerb tops, so crossing checks explicitly include their
upward-facing support. Existing 8cm steps need approach improvement and game
stepping verification. Three boundary rays hit geometry; all 8,879 parent scene
meshes and 44 reference hashes are preserved. Sparse rays are not capsule sweeps.

330 new meshes passed positive-volume/manifold generation checks. No compiler,
engine conversion, purchases, zombie pursuit or co-op runtime test was performed.
Build/check/render scripts are named `*_street_combat_v31.py`; logs live in
ignored `build/street-combat-v31-*.log`. Comparison: 26s, 720p, 24fps, 668,909 bytes,
labelled animated stills rather than continuous traversal.

One separately requested fal skeleton generation completed locally. Sam then
reaffirmed street detail as the priority; the asset was not integrated into this
map and is not part of this street delivery.
