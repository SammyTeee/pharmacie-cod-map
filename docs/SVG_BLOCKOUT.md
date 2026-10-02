# SVG blockout

The user-authored `references/pharmacie-syston/pharmacie-layout.svg` is the layout source. Its companion JPEG and JSON are preserved unchanged.

Run `python scripts/generate_blockout.py` to regenerate the map. `scripts/svg_blockout.py` reads rendered rectangle bounds and quarter-turn transforms. Screen-to-world conversion is `x=(svg_x-466)*2`, `y=(550-svg_y)*2`. The planner's size metadata is inconsistent between original and added objects, so it is deliberately not used.

Implemented: relocated bar, hollow toilet with doorway, rear-left outdoor smoking patio, rear stairs and connecting east flight, raised front-right platform, tables, sofa and feature-prop placeholders. Original template Zombies scripts, perks, weapon purchase and mystery box remain.

Gameplay interpretations, not measured architectural facts:

- Rear stair labels describe one connected route; stair height is 104 units and ceiling height is 320 for clearance. No upstairs room yet.
- The off-canvas `stauir` marker is ignored.
- The fixed SVG entrance is offset east. A bounded vestibule outside it prevents walking into empty space.
- Patio threshold bridges the small drawn gap. Patio walls bound playable space.
- Toilet door faces the bar; source has no door marked.
- Furniture uses solid placeholders. Photo detail and bespoke skeleton are deferred.
- Initial player markers are moved into the central aisle. Zombie spawner classname is corrected and risers redistributed inside reachable floor space.

Compilation is necessary but does not establish runtime playability. See MODLOG.md for actual build and game results.

## First runtime result

BO3 loaded this SVG build on 2026-10-02. The user's local play session reached the results screen with 2 rounds survived and 6 kills. This establishes solo loading, zombie combat and round progression; full route coverage and co-op remain unverified.

![First SVG blockout game result](screenshots/svg-blockout-first-game.png)
