# A-to-B survey planner — 11 October 2026

Open `recon/route-planner/index.html`, or serve the repository locally:

```powershell
python research/streetview-pipeline/build_route_planner.py
python -m http.server 8766 --bind 127.0.0.1
```

Then open http://127.0.0.1:8766/recon/route-planner/ . The generated page is
self-contained: no external scripts, tiles, account or API key. Its road/building
map comes from the unchanged project OSM snapshot under
`references/streetview-capture/extension-v41/osm-original.xml`. Attribution and
source hash are included. Snapshot extent/coverage is finite and may be stale.

Click near a road for A, then B. Pins snap to existing road nodes. The shortest
connected road route appears, with review stops every 12 metres by default.
Add via points to choose a particular street; reverse A/B or adjust spacing
between 5 and 100 metres. This is a modelling survey planner, not traffic or
turn-by-turn navigation. The graph is bidirectional; restrictions are not used.

Each proposed stop has Ahead/Right/Back/Left Google Maps viewer links. Opening
a link may resolve to a different nearby panorama: actual position/date/heading
must be checked. A proposed stop does not prove coverage or imagery collection.
No screenshots or geometry are automatically extracted by this page.

Export route JSON includes `[latitude, longitude]` waypoints at every road node,
so the old walker follows the road bends, plus `[longitude, latitude]` route
coordinates and observation metadata. GeoJSON uses longitude/latitude order.
Both exports also appear in a text field for copying if browser downloads fail.
The in-app download event timed out during validation; the JSON text fallback
was inspected successfully, so do not claim native download delivery verified.

## Existing Firefox walker

`walk_capture.py` and `firefox_capture.py` are still present, with the original
12-view sweep, panorama deduplication, resume state and stop/loop checks.
Sam explicitly requested reusing this automated personal-project collection.
The original tool requires visible Firefox and the existing Windows desktop
driver; it has not been ported to the current in-app browser controls.
Do not run both controls concurrently. There was no new unattended bulk run.

The walker now accepts a separate output folder, selected before its driver
lock is acquired. It rejects resuming a completed-stop ledger with different
waypoints. Existing captures remain unchanged. Example after saving an export
and displaying the resolved starting panorama A in Firefox:

```powershell
python research/streetview-pipeline/walk_capture.py --route research/streetview-pipeline/routes/syston-survey-route.json --output references/streetview-capture/melton-station-new --label melton-station --stops 3
```

The example route filename is user-exported, not preinstalled. Start with a
small reviewed batch. Planner spacing is a proposed review interval; the legacy
walker captures actual navigation panoramas, so it does not guarantee 12-metre
capture spacing. Browser automation/rendering and current Google usage terms
remain distinct from user authorization; no redistribution rights are established.

## Verified in this session

- Road map generated with 653 nodes / 155 road ways; no network during generation.
- Visible browser A/B selection and reversal: about 702 metres / 60 stops.
- Export fallback parsed: 25 waypoints / 60 stops / four directions per stop;
  first `[52.6974358,-1.0751575]`, last `[52.6933508,-1.0789163]`.
- Google in-app Maps and Street View rendered successfully after a slow initial
  load. DR Electrical panorama inspected, informing the v52 boundary detail.
- Eight helper tests pass, including cross-route resume rejection and output
  directory selection before locking. These do not validate live Firefox input.

Next: finish a supported, resumable in-app collection adapter, with capture
provenance and blank-image detection, then collect the full selected route.
