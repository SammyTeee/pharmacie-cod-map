# Saved Blender work

Open **pharmacie-entrance-fixed-v16.blend** for the current editable model. Reference
images are packed into the file. Blender 5.2.2 LTS was used locally.

Scenes:

- 01 Ground floor - mapped rooms
- 02 First floor - mapped rooms
- 03 Both floors - assembled exterior
- 04 Photo frontage - inspection
- 05 Interior - photo-led dressing (default, frontage included)

Select a named object root Empty to move its whole furniture group. Geometry,
photo surfaces and UV maps remain editable. The suspended ceiling is hidden
for cutaway viewing. Earlier `.blend` files are preserved milestones; numbered
automatic Blender backups are excluded from Git.

Read ../../docs/PHOTO_OBJECT_PLACEMENT_PLAN.md for photo evidence and modelling
assumptions, and ../../docs/BLENDER_WORKFLOW.md for reproduction/tool setup.
photo-interior-v03-manifest.json records sources, object positions and corrected
stairs. photo-interior-with-front-v03.png is the current overview. The frontage
inspection preview is photo-frontage-v02.png.

V04 added an adjustable 1.5x gameplay scale root (estimated frontage 10.5m),
fully open door leaves, widened small doorways, more clearance left of the bar,
and a simple two-way street with pavements and UK-style road markings.
gameplay-street-v04.png is the exterior preview. gameplay-space-v04-manifest.json
records changes and provisional spawn positions. Player/zombie markers and
the wire player clearance box are planning guides, not functioning game entities.

V03 was converted and successfully loaded as zm_pharmacie_blender. V04 has
not been exported or rebuilt, at Sam's request. Keep editing in Blender before
the next conversion. The v03-before-gameplay-edit file preserves live changes
present immediately before the new version was made.

V05 widens the frontage to the building's widest footprint, about12.66m,
with side walls/floor tapering into the existing layout over the first9.4m.
The sign and shopfront UVs are preserved. Main bar counter is6.31m wide after
the overall scale increase. Local door/bar transforms lost in v04 reparenting
were repaired; all scene layers are now updated before transform reads.
gameplay-street-v05.png and gameplay-space-v05-manifest.json describe the
current saved version. No v05 game export or traversal test yet.

V06 carries the wider frontage scale through the building body, restores the
plan's skewed wall directions and rear steps, and adds 8% width behind the
entrance. Front remains12.66m nominal; body sections are about13.1–14.1m wide,
and main counter8.22m wide. gameplay-street-v06.png and gameplay-interior-v06.png
show the saved result. Geometry is deliberately enlarged for gameplay, not
survey-accurate. Radiant rebuild remains on hold.

V07 fixes all seven items from docs/LAYOUT_REVIEW_V06.md: seating rearranged,
bar lowered to1.10m, tables to0.78m, coffee table repositioned/lowered to0.45m,
front platform set moved onto its support, exterior passage reshaped along the
angled wall, and upstairs stairwell edge rails added. Main bar approach has
about1.60m between the moved stool and counter. Body/frontage widths retained.
Current previews: layout-fixed-interior-v07.png, layout-fixed-upstairs-v07.png,
layout-fixed-exterior-v07.png. Manifest: layout-fixed-v07-manifest.json.
pharmacie-v06-before-layout-fixes.blend preserves live pre-edit changes.
Radiant/BO3 still uses the earlier v03 export; these fixes have not been tested
in game. Upstairs is scene02; the default scene05 is a downstairs cutaway.

V08 packs original bar front.jpg and uses UV-only back-bar and TV regions on
new photo surfaces behind the existing shelves/bottles and on the modelled
screen. backbar-photo-detail-v08.png shows the result. Raster sources remain
unchanged; backbar-photo-v08-manifest.json records both supplied reference
hashes and crop coordinates. All v07 layout fixes are retained. BO3 material
conversion and the next Radiant rebuild remain pending.
