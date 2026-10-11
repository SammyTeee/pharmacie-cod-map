# Melton Road / station / Holmdale extension handover

## User request

Extend the existing map from Taraj along Melton Road all the way to Syston
train station / the Midland area, and include 29 Holmdale Road (Sam describes
it as the last house on the left). Give number 29 substantial recognisable
detail, checked against Blender renders. Open Google Maps satellite view for
the road layout and Street View for the house and route architecture.

User-supplied Maps reference:
https://www.google.com/maps/place/29+Holmdale+Rd,+Syston,+Leicester+LE7+2JN/@52.6933309,-1.0789429,59a,75y,35.71h,85.39t/data=!3m7!1e1!3m5!1sw-Fo9fp2S5U4DlN7wtr5Ng!2e0!6shttps:%2F%2Fstreetviewpixels-pa.clients6.google.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D4.610616555239218%26panoid%3Dw-Fo9fp2S5U4DlN7wtr5Ng%26yaw%3D35.71090458597149!7i16384!8i8192!4m6!3m5!1s0x487762068e2391b1:0xa8be3b3674cf4876!8m2!3d52.693457!4d-1.0800171!16s%2Fg%2F11c3s8ym0l?entry=ttu

URL place coordinates: 52.693457, -1.0800171. Embedded camera coordinates:
52.6933309, -1.0789429; panorama w-Fo9fp2S5U4DlN7wtr5Ng.
These are supplied URL values, not independently verified building geometry.

## Work actually completed in this session

- Checked working-tree status and current checkpoint notes. Latest source is
  `assets/blender/pharmacie-taraj-bar-v40.blend`; preserve the corrected bar side
  and all existing street/pub/retail geometry. No new modelling has been done.
- Read v39/v40 notes and examined the existing street-reference workflow and
  route-to-scene code. Existing tooling is in `research/streetview-pipeline/`.
  `scripts/model_syston_v25.py` maps capture stop distances to the existing
  Melton centreline in `recon/v22/validation.json`, with estimated gameplay
  scale. Reconcile this frame before extending; do not assume geographic metres
  directly equal current Blender coordinates.
- Tried opening the supplied Maps URL through browser automation. Its runtime
  exited with Windows code -1073741502 before opening a tab. Reset the runtime;
  no successful browser opening or screenshot collection occurred.
- Web reader also could not access the Maps page. No satellite or house features
  have been visually verified. Do not invent a house from the address alone.
- Blender MCP read-only connection check failed at 127.0.0.1:9876 (no connected
  server). Python 3.11.0 and shell `rg` work; some PowerShell commands also
  failed with -1073741502. Desktop/session cause is not conclusively diagnosed.
- No Blender saves, game changes, uploads, commits or pushes in this session.
  Existing working tree contains many prior modified/untracked files: retain them.

## Resume on the local Windows desktop

1. Open this project in local Codex and read root `AGENTS.md`, this handover and
   `docs/TARAJ_BAR_V40.md`. Recheck Git status and the current Blender file.
2. Open Maps with the supplied link. Inspect Street View to verify number 29,
   then satellite top-down to establish the whole Taraj–station/Midland–Holmdale
   road connection. Record actual observed route and reference dates.
3. Collect unchanged reference screenshots with attribution/provenance, including
   multiple house angles, roof footprint, boundaries, neighbouring context and
   the route junctions. Preserve originals and distinguish estimated dimensions
   and gameplay adaptations from visible facts.
4. Open v40 in Blender, enable/start the existing Blender MCP server if using it,
   and save the extension as a new checkpoint. Preserve approved placements.
   Build continuous road/pavements and coherent boundaries along the full route;
   develop number 29 from reviewed evidence with matching comparison renders.
5. Verify geometry and route clearance separately from any BO3 claims. Keep this
   extension Blender-only unless the user authorises engine conversion/deployment.
   Show matched review images; use minutes-long preview methods, not an unmeasured
   hours-long render. This new task does not itself authorise media publishing.

The full extension objective remains unfinished. This handover is preparation,
not evidence that the route or house has been built.
