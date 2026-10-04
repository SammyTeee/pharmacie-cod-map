# Additional authored tutorial reading

Reviewed online 4 October 2026. These are short original summaries with source
links; full text is not mirrored. Exact installed BO3 sources and observed
project results take precedence over community assumptions.

## Proper power switch — Harry Bo21 / DTZxPorter

[Modme: Setting Up A Proper Power Switch](https://wiki.modme.co/wiki/black_ops_3/basics/Setting-up-a-proper-power-switch.html)

The authors cover a replacement power prefab plus lighting states responding
to power flags. They recommend configuring more than one sun-volume state and
testing after recompilation. This is a lighting-state extension, not evidence
that the existing stock switch must be replaced. We did not download its
external prefab archive or copy the script. Our first target is a supported
stock switch upstairs with a reachable use approach and proven perk power
behavior; a visual lighting change can follow independently.

## BO3 Zombies Mapping Guide — n0x

[Author's Steam guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3737598953)

The wall-buy section uses the `spawnable_weapon_` prefabs in the core Zombies
library and places the whole prefab against an accessible wall. It also
describes assembling a functional mystery box rather than assuming a base is
enough. The page displayed removal/incompatibility notices when reviewed, so
it remains supporting reading. We did not mirror its large map/code blocks.
The stock audit independently checks prefab paths and identifies the missing
functional box entities in our current source.

## Getting Started: Radiant Level Editor — Frosty_Mango

[Author's Steam guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3332382324)

This resource lists editor operations, links a tutorial series, and explains a
rotating door with separate model/collision parts. Its visible text does not
provide a complete purchase-trigger recipe, and its property spelling needs
comparison with actual stock KVPs. The page displayed removal/incompatibility
notices. Our gate recipe therefore comes from installed blocker scripts and
the existing generated map; rotating doors are optional polish after removal,
zone activation and AI connection are proven.

## LogicalEdits video leads

The Frosty_Mango guide identifies these authored videos. Saved as follow-up
links only: no transcript obtained and no steps claimed from unseen video.

| Topic | Original video |
|---|---|
| Editor setup | [Getting started](https://www.youtube.com/watch?v=XjPirs0Miuo) |
| Bought doors/debris/electric doors | [Doors](https://www.youtube.com/watch?v=kWDjnTf_Dh0) |
| Spawn entries and zones | [Spawns/zones](https://www.youtube.com/watch?v=8oXyXr6HV7w) |
| Pack-a-Punch, box and perks | [Reward prefabs](https://www.youtube.com/watch?v=35D-rESvws8) |
| Traps, later scope | [Traps](https://www.youtube.com/watch?v=7e8KEnAyRbc) |

Additional authored lead: [GAM3VIDZ bought doors/debris tutorial](https://www.youtube.com/watch?v=POVNi0m822I).
Its retrieved description confirms the topic; the actual demonstration was
not inspected/transcribed in this pass.

## IceGrenade resources

[Author-maintained BO3 getting-started wiki](https://github.com/IceGrenade/bo3/wiki/Black-Ops-3-Mod-Tools-Get-Started)
is a tutorial directory, including map mechanics and pathing resources. Use
the original author links for additional learning rather than mirror-site
versions or apply WaW instructions without checking the BO3 differences.

## Official reference already installed

`<ToolsRoot>/docs_modtools/` is primary documentation available offline.
[Our bundled-doc review](../../../docs/BLENDER_RADIANT_WORKFLOW.md) identifies
QuickStart, Scale_Standards, Generate_LED, Images and Build_light pages.
The tutorial library does not redistribute those PDFs or stock game sources.
