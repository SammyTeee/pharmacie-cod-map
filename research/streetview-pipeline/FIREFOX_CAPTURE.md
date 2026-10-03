# Working Firefox capture workflow

Sam explicitly authorised driving the existing Firefox Street View tab and a
dense personal screenshot run from Taraj to the Pharmacie, including both road
sides, bridge, bus stops, shopfronts and roadside detail. The user is AFK.
The published Google restrictions found in PIPELINE_PLAN.md still apply; this
records the requested workflow/provenance, not permission or redistribution rights.

## Local output

`references/streetview-capture/taraj-to-pharmacie/` inside this repository:

- `originals/`: unretouched PNG screenshots of the map viewport at native resolution.
- `manifest.jsonl`: one immutable capture record per original with URL, position,
  panorama ID when available, heading, pitch, field of view, timestamp, role and hash.
- `walk-state.json`: completed panorama stops and route progress.
- `catalogue.csv` / `catalogue.json`: flat metadata for bulk labelling.
- `index.html`: searchable local gallery; labels/notes saved in browser storage
  and exported with **Export labels JSON**. Put exported `review.json` alongside
  the manifest and rebuild the gallery to incorporate annotations.
- `contact-sheets/`: separate labelled thumbnail derivatives for quick inspection.
- `summary.json`: counts, sizes and hash-verification status.
- `camera-route.geojson`: observed camera positions/angles and travelled route.
- `integrity-report.json`: original hashes and completed-stop coverage checks.

The raw collection is ignored by Git and stays local; scripts/documentation are
trackable. No Google image endpoints, API keys, billing or tile downloads are used.
Google overlays and attribution remain visible in the saved viewport. Firefox
chrome/bookmarks are excluded. The originals are never replaced by later labelling.

## Run on Windows

Dependencies already found on Sam's machine: Python, Pillow, pyautogui and mss.
Desktop access is required. Firefox must contain a visible Google Maps Street
View tab; the helper verifies foreground Firefox before inputs. It does not drive
BO3. Avoid simultaneous user/browser interaction during a capture run.

```powershell
python research/streetview-pipeline/firefox_capture.py status
python research/streetview-pipeline/firefox_capture.py capture --label manual-detail --stop manual-01
python research/streetview-pipeline/walk_capture.py --route research/streetview-pipeline/routes/taraj-pharmacie.json --stops 3
python research/streetview-pipeline/build_capture_gallery.py --verify
python research/streetview-pipeline/test_capture_helpers.py
python research/streetview-pipeline/audit_capture.py
```

The walker starts from the currently displayed resolved panorama, captures eight
overlapping 45-degree surroundings views plus four frontage/pavement detail
views, then visibly steps to the next panorama toward its route waypoint.
Targets are authored `[latitude, longitude]` points with arrival radii; they are
not navigation instructions returned by Google. Intermediate points in this
first route were estimates and require observation of actual road/junction links.

Stop a run with Ctrl+C or create a file named `STOP` in the capture folder.
PyAutoGUI's corner fail-safe remains enabled. Stale/missing panoramas, navigation
loops, unexpected large jumps and inability to focus Firefox cause the driver
to stop. An OS-held driver lock rejects concurrent capture/control commands;
the lock releases when the process exits, even after an error. A stopped partial
sweep remains in the originals and manifest; it can
be labelled/reviewed rather than deleted. Never launch two drivers simultaneously.
Restarting at the last completed panorama advances once; an already completed
route exits. Restarting during a partial sweep recaptures that stop with new IDs.

## Accuracy and quality

Canonical Street View URLs supply camera viewpoints and view angles, not surveyed
facade positions. Requested Maps URL parameters are stored distinctly from a
resolved viewpoint. Place/map URLs do not supply a panorama ID. The first pilot
map record predates that parser correction; catalogue normalisation excludes
place IDs from panorama counts. Screenshot overlays may show a different capture
date from today's screenshot timestamp; dates are only recorded as observed.

Road-normal left/right shots are useful frontage candidates, not guaranteed true
facade-normal images. Angled buildings, trees, poles, parked cars, pedestrians,
panorama seams and source blur remain. Nearby panorama overlap and detail shots
provide alternative evidence. Stability checks reduce loading frames; visual
contact-sheet review remains necessary before trusting modelling references.

Current scope is screenshot collection and cataloguing. Drawing a line on a map,
importing that route into Blender and automatic semantic labelling/3D generation
are separate next stages. No existing Blender scene changes in this capture run.

[Observations from reviewed capture views](CAPTURE_REVIEW.md) provide a first
modelling checklist. The gallery's labels export preserves imported review notes
alongside browser edits; place the exported file in the collection directory.
