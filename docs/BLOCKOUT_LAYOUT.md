# Blockout layout

Sam's editable Paint reference is preserved as [`Untitled.png`](../Untitled.png). The clean redraw at [`pharmacie-layout-v1.svg`](pharmacie-layout-v1.svg) shows the initial interpretation. The [interactive layout planner](layout-editor.html) lets you drag and rotate the entrance, rooms, and props; rename existing items; add named rooms and floor objects; and save the result as SVG, JPEG, or JSON. The JSON contains BO3 coordinates for applying your revised plan to the generated map.

## Reading the sketch

The street entrance is at the south/front end, and the pub runs north to the bar. The toilet is to the left/west of the stairs; the stairs are on the right/east and rise toward the rear. A side door connects to the smoking area on the west near the stairs. Tables fill the main hall, with a slightly raised table platform in the middle. These are interpreted from the sketch, not measured from the real building.

## Current code-authored pass

- Main hall interior bounds: x -352..352, y -640..800, z 0..256 BO3 units.
- Front entrance: 192-unit opening at the south end.
- Toilet: enclosed side room in the rear half, with a doorway into the pub.
- Stairs: east-side passage with eight simple rising solid treads and an upper landing. The actual upper floor and connection are not built yet.
- Smoking area: covered side annex west of the main room, reached through an opening near the stair/toilet area; its outer side is open to the surrounding sky shell.
- Bar and backbar: placeholder block geometry at the north end.
- Four table placeholders and a slightly raised platform: rough circulation markers, not finished furniture.
- Existing Zombies template entities and scripts are retained and adjusted to the first room bounds.

This is a compact playable-space blockout, not a faithful measured floor plan. The main room dimensions are an initial scale guess. The SVG is intended for correcting relationships and door locations before further dressing.

## Regenerate

From the repository root, run `python scripts/generate_blockout.py`. This reads the preserved generated template at `map_source/zm/zm_pharmacie.template.map` and rewrites `map_source/zm/zm_pharmacie.map`. Keep the template untouched and review the source diff before staging it in the local Mod Tools installation.
