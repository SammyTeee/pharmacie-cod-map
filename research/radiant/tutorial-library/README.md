# Saved BO3 mapping tutorials

Source: [UGX-Mods/community-wiki](https://github.com/UGX-Mods/community-wiki).
Commit: `331184f27904c1fbe24cd59b5d752511f698746a`.
License: [unchanged AGPL-3.0 text](vendor/ugx/LICENSE).
Attribution: [upstream credits](vendor/ugx/CREDITS.md) and original page notices
in each HTML file. Readable `.txt` derivatives identify the local conversion
and retain the upstream license. Original HTML is authoritative.

All these are BO3 pages. None of the WaW guides they link are treated as direct
BO3 entity recipes. No tutorial attachments, game prefabs, images or videos
were downloaded. Relative media and page links may require the upstream site.

| Saved readable page | Coverage and practical use |
|---|---|
| [Zones](vendor/ugx/zones.txt) | Short BO3-specific changes; `info_volume`/player-volume coverage. Not a complete zone-manager recipe. |
| [Spawners, risers, barriers](vendor/ugx/zombie-spawners-risers-barriers.txt) | Factory spawner, named riser groups, window entry association. Compare actual KVPs with installed stock. |
| [Box locations](vendor/ugx/mystery-box-locations.txt) | Early-beta warning about incomplete stock box locations; recommends examining The Giant. Attachment links only. |
| [Dogs](vendor/ugx/dogs.txt) | Dog entry/round setup; later scope, not required for first core. |
| [Script error information](vendor/ugx/script-error-information.txt) | Debug/log settings and limits of available script debug information. |
| [Purchase loops](vendor/ugx/purchase-loops.txt) | Explains use triggers, affordability, score deduction and waits. Educational; normal doors/weapons should use stock systems. |
| [Weapon list](vendor/ugx/weapon-list.txt) | Historical identity lookup; installed weapon tables decide actual availability/prices. |
| [WaW scripting differences](vendor/ugx/waw-scripting-differences.txt) | BO3 language/module changes; helps avoid copying obsolete WaW recipes. |
| [Materials/textures](vendor/ugx/materials-and-textures.txt) | TIFF/APE image and material concepts, surface categories and texture channels. |
| [Models](vendor/ugx/models.txt) | Model conversion outline; do not assume our detailed Blender export is already supported. |
| [Custom sounds](vendor/ugx/sounds.txt) | WAV/alias/link workflow; its instruction to ignore particular errors is historical advice, not our acceptance rule. |
| [Sound aliases](vendor/ugx/soundaliases.txt) | Additional audio pipeline/detail reference; complete sound-bank deployment remains mandatory here. |
| [Weapon-system index](vendor/ugx/weapon-system.txt) | Link index only; not a complete weapon placement guide. |
| [Radiant Black](vendor/ugx/radiant-black.txt) | Image-only stub. Use bundled QuickStart for editor operation. |
| [APE](vendor/ugx/asset-property-editor.txt) | Work-in-progress stub. Use bundled asset docs and the materials page. |

The upstream HTML sits beside each text file with the same stem. Full source
URLs, hashes and sizes are in [the manifest](sources.json). Collection and
offline verification are described in [the research README](../README.md).

## Reading order for this map

Read zones and spawners/barriers together; then the box caution; then purchase
loops and script errors. Use asset pages when conversion reaches materials,
models or audio. Wall buys, doors, power, perks and Pack-a-Punch receive exact
local recipes in [the stock audit](../../../docs/RADIANT_STOCK_GAMEPLAY_AUDIT.md),
with broader authored tutorial links in [external notes](EXTERNAL_READING_NOTES.md).

## Version pitfalls

- A visible model/base is not a complete interactive prefab.
- A zone label or flag name is not activation logic by itself.
- New zones need supported geometry, player-volume coverage, registered state,
  spawn entries and navigation through their bought connections.
- Beta-era missing-asset claims and advice to ignore warnings need checking
  against installed build `5284267`; no automated changes follow those claims.
- Tutorial examples of a custom purchase loop do not establish multiplayer
  race handling, door path reconnection or standard weapon behavior.
