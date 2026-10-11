# Midland exterior — v42 (extension still in progress)

Saved checkpoint: `assets/blender/pharmacie-midland-frontage-v42.blend`.
Built from v41; v40 and v41 remain retained. The requested full extension is
unfinished. Google satellite alignment verification and number 29 remain pending.

## Photo evidence and implementation

Reviewed unchanged official-site exterior reference:
`references/streetview-capture/extension-v41/midland-official-exterior.jpg`.
Source URL, hash and rights/date limits are in the private reference manifest.
The image shows dark blue rough lower masonry and white upper render, four upper
white sash windows, two broad lower window assemblies, smaller left windows,
two glazed entrance bays, fascia text, garden plaques, hipped slate roof and
chimneys, dark gutter/downpipes, hanging baskets, raised timber frontage deck
with dark railings, picnic furniture and navy umbrella. These visible motifs
guide separate closed meshes and geometric lettering; no photo pixels are baked.

The OSM footprint association remains provisional. The frontage uses its
16.7197-unit front edge and an estimated upper front wing. Rear wing heights,
rear flat roof, facade dimensions, roof rise, windows, furniture counts and
setbacks are estimates informed by one oblique photo, not a measured survey.
The exterior is static closed scenery; doors/windows are shallow relief, with
no accessible or claimed reference-accurate interior. Capture date and present
appearance are unverified. Do not substitute this pub for number 29.

All new facade parts are parented to `Midland v42 | Movable reference assembly`.
That allows the whole pub to be repositioned if Google's top-down view requires
a road-frame correction. v41's road and footway layout is not altered. The
provisional footprint mass is retained in an unlinked archive. Prior map/pub/
Taraj objects retain transforms and datablock references.

## Verification and review

`recon/v42/validation.json` records saved output, mesh/manifold/volume checks,
parent-preservation assertion and source photo hash. `recon/v42/route-checks.json`
repeats v41's selected seam/road/footway/station-link rays against the new exterior.
Blender checks do not establish BO3 collision, AI navigation or runtime behavior.

Final assembly: 405 closed positive-volume meshes, 13 geometric text objects and
one movable root. All 15,602 prior scene object transforms and datablock references
are retained; the source v41 file was not overwritten. 27,999 selected clearance
rays and 3,111 floor samples pass. Visual review corrected the blue upper side
wall, separated fascia wording, added the M wreath and side painted title.
The initial build MCP call timed out at 300 seconds; a subsequent read-only
stack inspection showed Blender idle, and independent MCP/file checks confirmed
successful save and clean state. Do not rerun the initial build to recover it.

Matched before/after material-colour previews: `recon/v42/index.html`. They show
geometry and rough material colour; procedural surface texture/final lighting
are not being evaluated by Workbench. Keep previews local; no publishing.

Reproduce once on v41 with `scripts/detail_midland_v42.py`, then run
`scripts/check_extension_v41.py` (accepts v41 or v42 and selects report folder),
and `scripts/review_midland_v42.py`. Build refuses to overwrite a checkpoint.
BO3 unchanged. Full task goal stays active until satellite and house requirements
are actually satisfied.

Next independent work: station detail from National Rail schematic and dated
Geograph photos. Unchanged references/credits/CC BY-SA links are in the private
reference manifest; `recon/v43/station-reference.json` extracts 28 mapped ways and
11 point features into the provisional frame. No v43 modelling has been done.
