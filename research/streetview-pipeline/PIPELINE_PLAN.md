# Route drawing, street references and Blender generation

## Intended user experience

1. Search or pan to the neighbourhood; draw road-centre lines and optional branches.
2. Set road/pavement widths, choose both sides or one side, mark detailed destinations.
3. Preview route length, proposed observation stops and building guide positions.
4. Review available street-level imagery at each stop, looking left/right and
   ahead/back at junctions. Collect reusable references only from an image source
   that permits that operation. The app links every approved reference to its stop.
5. Export to Blender: metre-scaled road ribbons, pavements, junction guides,
   building footprint placeholders where available, reference cameras and markers.
6. Model detailed fronts using reviewed images/notes, with the rest kept basic.
7. Inspect player-height renders and iterate before a separate Radiant/gameplay pass.

The goal is a guided modelling workflow. A road line and a panorama do not by
themselves provide measured building height/depth, interiors or clean hidden
surfaces. Those need additional geometry data, photos or labelled estimates.

## What is technically available

Google's Street View JavaScript service can locate panoramas and expose nearby
navigation links. Static requests can set heading, pitch and field of view.
These capabilities could support a live review interface. They do not grant
permission to download an offline building-reference library or derive game
assets from imagery. Official references:

- [Street View service](https://developers.google.com/maps/documentation/javascript/streetview)
- [Street View request controls](https://developers.google.com/maps/documentation/streetview/request-streetview)
- [Maps URLs](https://developers.google.com/maps/documentation/urls/get-started)

Maps URLs can open a panorama near a latitude/longitude with camera settings
without an API key. A link is not panorama discovery, a coverage guarantee or an
image exporter. A Google review viewer should remain separate from the
reconstruction data source and comply with the relevant display/integration rules.

## Material restriction found in the research

Google's published Geo Guidelines prohibit screenshots/offline downloads and
analysing or extracting data from Street View imagery. Maps Platform terms
also restrict scraping, caching and creating content from Maps Content. An API
key does not remove those restrictions. This is why the proposed automatic
Google screenshot-to-Blender collector is not a supported default design.

- [Geo Guidelines, Street View section](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- [Maps Platform terms, section 3.2.3](https://cloud.google.com/maps-platform/terms)
- [Street View Static policies](https://developers.google.com/maps/documentation/streetview/policies)

Checked 3 October 2026. Do not infer that manual screenshotting, a paid API or
browser clicking resolves the same usage restrictions. Preserve existing user
reference files; this research did not change their provenance or establish rights.

## Recommended architecture

### A. Route editor

Small local browser app. Use an OpenStreetMap-based map for authored route
geometry, subject to attribution and data licence obligations. No bulk download
of the public tile server. The user's road-centre strokes and detail tags export
as GeoJSON, independently of the background map image.

- [OpenStreetMap licence and attribution](https://www.openstreetmap.org/copyright)
- [Public tile-server policy](https://operations.osmfoundation.org/policies/tiles/)

Street centre lines can be manually drawn or later snapped using an appropriate
open-data routing provider. A complete automatic footprint layer is optional;
OSM coverage and height information must be checked locally rather than assumed.

### B. Observation planner

Proposed spacing: 8–12 m initially, configurable. This is a design choice, not a
Street View panorama interval. Generate left/right target headings relative to
each route segment and extra junction views. For a reusable panorama source,
select real available camera positions and deduplicate repeated panoramas.
Route-normal headings are a first guess: skewed facades need their own normal.

For the Google-only viewing mode, observation stops produce links to the
provider's viewer; they do not store screenshots or extract imagery-derived
geometry. Missing coverage remains explicitly missing.

### C. Reusable reference collection

Provider interface with clear capabilities: live viewing, saving originals,
processing crops, deriving geometry, distributing resulting assets. Enable
collection only for a source whose licence/permission covers the needed uses.
Initial option: user-owned photos/panoramas, including a phone/360-camera survey.
Investigate any third-party street-image provider's actual current licence,
regional coverage and API before recommending it; no alternative is approved yet.

Where collection is permitted, save unchanged originals separately from corrected
facade views. Associate each with capture position, camera direction, source/date,
licence, building/route stop, confidence and obstruction notes. Keep building IDs
stable when images or panoramas change. Avoid baking cars/people into facades.

### D. Blender importer

GeoJSON coordinates are geographic longitude/latitude, not Blender metres.
Use a suitable metre-based projection/local coordinate transform; preserve
origin, CRS, north direction and transform in the manifest. Z is up.

Import into a new collection/file. Generate continuous mitred road ribbons,
pavements, editable junctions and placeholder masses. Tag guessed heights/depths.
Use actual footprints if licensed data is available; a route line alone cannot
locate every facade correctly. An adjustable setback is the fallback.

To align to this project, select a pub-front anchor and another independent
landmark plus a confirmed length if available. Keep geographic scale separate
from the existing enlarged gameplay scale. Preview differences before merging;
do not stretch or overwrite the reviewed pub to force a match.

Reusable photo references become positioned Blender image/camera guides. Facade
fronts then get modelled frames, signs, sills and recesses using the workflow
already demonstrated. Sharp sign lettering is geometry or purpose-made signage,
not a promise that blurry source pixels can be recovered.

### E. Review and engine conversion

Generate route overview and player-height inspection cameras. Check road gaps,
geometry overlap, frontage order, blocked passages and estimated dimensions.
Blender placement does not implement BO3 collision, navigation, purchase doors,
zones or rounds; the established Radiant workflow remains a later step.

## First practical slice

Start with one short route and a branch, not an entire town:

- Route drawing, width controls and GeoJSON export.
- Blender road/pavement/marker import using synthetic/authored data.
- Attach user-owned photos to three frontage markers.
- Create one simple detailed 3D frontage and render the route for review.
- Add provider discovery/capture only once the imagery access route is settled.

Acceptance: export/reimport preserves metre distances and orientation; branch
junction is continuous; existing map source is untouched; each image has provenance;
missing facade dimensions are labelled; no hidden credentials or paid background
requests. This is an implementation plan, not an already working collector.

## Open question

Sam has been asked whether an OpenStreetMap route editor is acceptable or whether
the drawing interface must use Google Maps. This affects the frontend and data
boundary; it does not resolve image capture rights. Image-source preferences and
API budget can be discussed after choosing the basic interface.
