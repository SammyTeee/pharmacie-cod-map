# Numbered street reference catalogue

[Open the numbered map](index.html) · [Small building/feature index](INDEX.csv)

296 original captures were reviewed in contact sheets; selected close originals
were inspected at native resolution. The collection covers Taraj → brook/bridge
→ Melton Road retail rows → mini-roundabout. Sam stopped capture there; new close
High Street/pub images are **not** claimed. B050 links the existing pub references.

## Read only what you need

1. Search `INDEX.csv` for a name or ID, or click a marker on the map.
2. Read **one** `entries/Bxxx.md` building/shopfront file, plus its neighbouring
   entries only when they affect adjacency. `Fxxx.md` files cover street features.
3. Open the selected photo IDs linked in that file. Use `stops/route-xxx.json`
   for the other angles at that camera position. Each stop file is small.
4. Add new observations to that entry's matching JSON, then run
   `python research/streetview-pipeline/build_street_catalogue.py` to refresh pages.
   The individual JSON files are the source; Markdown/HTML are generated views.

Do not load every dossier, `PHOTO_INDEX.csv` or the entire raw manifest into an
agent's context. Search those indexes for an ID when needed. No giant combined
reconstruction document is required. Each entry page opens independently and
links unchanged originals. Shared terrace groups prevent duplicate upper masses.

## IDs, map and evidence

- **B001–B051:** named shopfront/building or explicitly unresolved frontage group.
  A storefront ID does not imply a separately owned whole building. Neighbouring
  units can share the same upper mass. IDs remain stable when more evidence arrives;
  append new IDs rather than renumbering existing entries.
- **F001–F017:** road, pavement, brook, bridge, bus shelter, crossings, passageways
  and other roadside features. Some are corridor-wide references, not point objects.
- **S01–S05:** route sections from Taraj to the junction. `S00` is pilot/map context.
- Camera positions are read from visible Maps URLs. **Building markers are rough
  camera offsets, not measured building footprints, boundaries or dimensions.**
  The map is north-up, can zoom/pan and filter IDs. B050 uses a Google place pin.
- Each photo distinguishes **observed IDs** in manually selected evidence from
  **nearby candidates** assigned by route area. A candidate does not mean every
  listed building is visible. Do not turn an uncertain label into an observed fact.
- Native reviewed dates include April2016, April2019, April2023, August2024 and
  April2026. A date is propagated only within the same resolved panorama ID with
  the inspected evidence photo recorded. Other dates remain unverified.
- Photos126/128 show the intended west row but their reported URL headings lagged
  the view. Their headings are excluded from building placement. Original files
  and immutable manifest remain intact; review annotations record the conflict.

Originals/gallery live locally in ignored
`references/streetview-capture/taraj-to-pharmacie/`. Notes, indexes and map pages
are trackable; raw images are not distributed. Browser image links work locally
and will be absent on a checkout without the original collection. Google imagery
rights are not established by the catalogue. Existing Blender v24 is unchanged.

[First observed route notes](../../research/streetview-pipeline/CAPTURE_REVIEW.md)
· [Capture workflow](../../research/streetview-pipeline/FIREFOX_CAPTURE.md)
· [Existing High Street specification](../STREET_PHOTO_RECONSTRUCTION.md)
