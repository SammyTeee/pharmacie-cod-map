# Syston skating runtime contract

See [SKATE_PROTOTYPE.md](SKATE_PROTOTYPE.md) for the selected route and gates.

The prototype has one runtime process. The pinned Rust engine owns simulation,
input, camera, render state and lifecycle. The Blender file is an offline input,
with no live IPC channels, queues or network dependencies during gameplay.

Coordinates: one source BU is `1 / 1.0640686466` runtime metres. Flatten evaluated
world transforms once; then map Blender `(x,y,z)` to runtime `(x,z,-y)`. Apply
exactly the same conversion to geometry, collision, authored grind paths and
spawn. Preserve winding because this axis transform has positive determinant.

Use the pinned upstream little-endian SKATE v15 format through its own exporter
and reader. Rebuild from immutable source into `build/pharmacie-skate/`; parser
errors stop launch. Never silently substitute boxes for invalid concave surfaces.
Visual and collision sets are explicit: fine decorative meshes can stay visual
without colliding; ramps and rideable rails must participate in collision.

Collision `surface` is a packed contact tag, not an object identity:
`material.audio | (material.physics << 7) | (material.pattern << 12)`.
Physics category `(surface >> 7) & 31` must be below 16. The pinned exporter
requires a post-export repair for this custom-world runtime. Never skip it;
the old object IDs caused false water contacts and a contact-vote panic.
After the welding, material and lighting stages, run
`python scripts/rebuild_skate_floor.py --staging build/pharmacie-skate/NEW-CANDIDATE`.
Use a fresh directory. This applies the contact/floor repairs and verifies native
volumes/contact voting, unchanged presentation, unchanged rail/extension data
and unchanged authored skate-feature collision. It leaves the live map alone.
Rebuild both Rust probes from `scripts/skate_map_probe.rs` and
`scripts/skate_contact_probe.rs` after upstream changes. The contact probe runs
independent face-centre wheel contacts through the actual query and solver;
its limits do not include multi-body dynamics or complete landings.
This floor adaptation is specific to the v60 starter street; other layouts
require reviewed bounds and support samples. A candidate still needs actual
runtime initialization/capture and human riding validation before acceptance.

Boot directly into the custom map when prepared local data is available. Exit
closes the sole runtime; no control is handed to BO3 or the original Skate game.
Runtime extraction and saves must remain under the isolated local prototype
folder. Do not alter an existing game installation, user profile or game save.
