# Pharmacie-Syston — start here

Prepared for Brownie and his AI on 7 November 2026.

Open **`Pharmacie-Syston.blend` in the repository root** with Blender 5.2.2 LTS
(the version used to verify it). Select scene **`03 Both floors - assembled
exterior`** for the complete pub, neighbouring streets and extended Syston route.
The other scenes contain ground-floor, upstairs and reference/detail views.

This is a byte-for-byte copy of the latest neutral street project,
`assets/blender/pharmacie-demo-base-v59.blend`, not a reconstruction or simplified
export. No objects, textures, materials, archived collections or scene data were
removed. SHA-256:
`c39f15e8b24e099f5b9753778597ef89bf9b76fa815324612af1fb5569f0a834`.

The file opened successfully in background Blender on 7 November. All 52
file-backed images are packed inside the file; there are no linked libraries,
missing images or unpacked external paths reported by Blender. The file can be
opened without Sam's original Windows folders. Keep the packed resources when
saving; old absolute paths shown in image settings are provenance, not download
requirements. Exact dependency inventory: [handover/blender-dependencies.json](handover/blender-dependencies.json).
This was an open/dependency check, not a new render or gameplay test.

## Older versions and local assets

**Sam keeps the older Blender versions locally. They should not be needed for
normal work on this project. If a previous checkpoint, comparison or original
reference becomes useful, reach out to Sam rather than rebuilding it or assuming
it has been lost.** Sam approved removing all 72 checkpoint paths under
`assets/blender/` from tracking while keeping every local copy and existing Git
history. The root `Pharmacie-Syston.blend` is the single tracked Blender project.

The separate `pharmacie-skate-street-v60.blend` is a skating adaptation, not a
replacement for the neutral project: it changes parked-vehicle visibility and
adds skating geometry. It and the original v59 stay locally with Sam, outside
the current tracked file list. Preserve them separately. Dave, Rocky and boss character
sources are also separate work; they are not included in this neutral street
file. Their latest assets were uncommitted at the start of this review and must
be accounted for separately from the Blender street handover.

Some historical scripts assert old checkpoint filenames. Do not regenerate a
scene from an old builder to obtain the current project. Ask Sam for the needed
checkpoint; when a tool specifically expects v59, an identical copy of the root
file at `assets/blender/pharmacie-demo-base-v59.blend` also supplies that source.
That compatibility path is ignored. `scripts/open-blender.ps1` now opens the root
project by default; its optional skate switch requires Sam's separate local file.

The ignored `build/` folder contains local tools, game/runtime data, compiled
maps, backups and experiments. Brownie does not need it to open this Blender
file. Original private reference captures also remain with Sam; their presence
on his machine does not mean they are included in a clone.

## Reading order for the next AI

1. Root [AGENTS.md](../AGENTS.md): user corrections, preservation rules and
   separation between Blender, BO3 and skate work. Earlier "latest" filenames
   deeper in the document describe historical stages.
2. [BLENDER_DEMO_V59.md](BLENDER_DEMO_V59.md): current neutral visual pass,
   verification and visible unfinished work.
3. [SURVEYED_ROUTE_V57.md](SURVEYED_ROUTE_V57.md) and
   [AUTHORED_ROUTE_SURVEY_2026-10-11.md](AUTHORED_ROUTE_SURVEY_2026-10-11.md):
   route coverage, sources, placement compromises and survey limits.
4. [PUB_PHOTO_RECONSTRUCTION.md](PUB_PHOTO_RECONSTRUCTION.md),
   [STREET_PHOTO_RECONSTRUCTION.md](STREET_PHOTO_RECONSTRUCTION.md),
   [THE_PHARMACIE_MAP_NOTES.md](THE_PHARMACIE_MAP_NOTES.md) and
   [PHOTO_ASSET_PLAN.md](PHOTO_ASSET_PLAN.md): appearance and source provenance.
5. [MODLOG.md](../MODLOG.md): dated evidence and later separate game/character
   work. Consult the task-specific documents before changing those branches.

The established scene uses **1.0640686466 Blender units per physical metre**.
Do not globally rescale approved architecture merely because the UI says metric.
The pub, corrected Taraj interior/bar, number 29 porch/windows/garage and
approved building placement must be preserved. Use separate working copies for
substantial changes and keep observed features distinct from estimated or
gameplay-adapted ones. Source reference images must stay unchanged.

This is a connected reference-led working model, not a completed architectural
survey. Some later shops have repeated opaque window proxies, blank fascias and
estimated concealed volumes. Some route joins/footprints are deliberate
compromises; see the v57 notes. Blender clearance checks do not establish BO3
collision, navigation or co-op behavior.

The compact BO3 core65 and separate Dave66/Dave67 projects are independent engine
copies. Do not replace the full Blender scene with their cropped play areas.
Sam retains game controls. This handover does not authorize game deployment,
launches, new paid generation or public distribution of third-party assets.

## Keeping downloads manageable

The cleanup reduces current tracked working files from 4.292 GB to approximately
1.345 GB, before small new notes. Existing commits still contain the older files.
Use a shallow clone to download only the latest snapshot and its commit:

```sh
git clone --depth 1 git@github.com:SammyTeee/pharmacie-cod-map.git
```

An existing full clone does not shrink merely by pulling a cleanup commit. No
history rewrite or force push is part of this ordinary checkpoint prune.

The audit and savings are in [REPOSITORY_SIZE_REVIEW.md](REPOSITORY_SIZE_REVIEW.md).
