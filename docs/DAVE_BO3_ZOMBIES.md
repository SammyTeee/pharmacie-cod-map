# Dave zombie replacement trial — 25 October 2026

## Sam's playtest approval — 25 October

Sam reports the Dave zombies look excellent in game and explicitly requests
keeping Dave in place of ordinary zombies. Visible appearance/likeness is now
human-confirmed. Specific combat, death, co-op and performance cases below have
not individually been reported. The accepted Dave66 assets and map are preserved.
Sam requested a separate mutated boss Dave, about three times human height;
boss development must not replace the approved ordinary Dave character.

Sam requested trying the existing Dave model as the ordinary zombies in BO3.
The separate `zm_pharmacie_dave66` map is now natively compiled, lit, linked,
source/package checked and hash-verified deployed for a private human-controlled
trial. Sam has now played it and approved Dave's in-game appearance; this task
has not sent game controls.

Run `PLAY-DAVE-ZOMBIES.cmd` from the repository. It validates the accepted map,
scripts and all package files before using the existing backed-up deployment/
launcher. Sam retains movement, combat, purchases and all game controls.
`PLAY-PHARMACIE-ZOMBIES.cmd` still targets core65 separately.

## What changed

- Preserved the original Dave v1/v2 files and the neutral Blender map sources.
  Source character: `assets/generated/dave-zombie-v2/dave-rigged_character_glb.glb`.
- Read the actual installed stock zombie body XModel bind skeleton: 78 bones,
  including the limb, head, weapon/eye tags and finger hierarchy. The source
  auto-rig has 24 bones and different naming/local axes. Simply renaming the
  existing FBX would not establish compatibility.
- Mapped existing skin weights to the stock names, aligned continuous limb chains
  with stock bind directions, retained Dave's torso/head proportions, and used a
  1.04 uniform size adaptation. Joint placement remains a prototype fit.
- Welded coincident UV-split geometry within .001 engine units before simplifying,
  retaining per-loop texture coordinates. This removed the ragged cracks seen
  when disconnected seam islands were simplified independently.
- Separated head/body along the stock upper-neck region. Exported 21,395 body
  triangles / 5,373 head triangles (26,768 total), with 9,411 / 2,678 welded source
  vertices respectively. A single 4096-square base-colour atlas is retained.
  This first native material uses neutral normals/roughness; no claim of full
  Blender PBR parity is made.
- Both native XModels round-trip through the installed `export2bin` as version 7,
  retaining the exact stock bone names/parents and bind positions within .0001
  engine units. Actual stock walk and attack source frames each match all 78
  candidate bones and produce finite, inspected mesh poses in Blender.
- A namespaced character/archetype/variant/spawner retains stock zombie AI and
  animation tables. Dave supplies separate head/body models. Stock hats, random
  head aliases and German zombie dismemberment substitutions are removed.
- Cloned the accepted core65 source into `zm_pharmacie_dave66`, changing its one
  native zombie actor spawner class. Geometry, collision, doors and paid
  progression are otherwise identical. Original map/scripts remain unchanged.

## Native build evidence

All private conversion data, stock-derived skeleton metadata/GDT definitions and
native intermediates stay in ignored `build/dave-bo3/`. Do not commit/distribute
the stock-derived skeleton or animation data. The scripts read the user's own
official Mod Tools installation and contain no copied stock character data.

Tools root: `S:/SteamLibrary/steamapps/common/Call of Duty Black Ops III 455130`.
The native linker identifies stable 3421953 / v593. Installed Blender: 5.2.2 LTS.

The first asset-only link rejected a zero normal and tiny weights. Welding and
valid normalized geometric fallback normals fixed the former. A .005 minimum
weight still produced 1,121 body / 274 head native warnings and nonzero exit;
the exporter now drops weights below .011 and renormalizes up to four influences.
The documented CoD exporter threshold is .010097; our .011 margin passes the
installed native converter. Final asset-only link exits 0 with no reported
conversion warnings/errors. The earlier failed outputs are not accepted.

The separate map's geometry/navigation compiler, fresh lighting export and final
localized linker all completed successfully. The build process exits 0. Source
checks confirm the copy differs only in actor classname, and the unchanged
layout matches the source-audited core65 receipt. Inherited checks cover 35,238
ground, 11,813 visible-floor and 1,592 route samples; these remain source checks,
not native movement tests.

`build/dave-bo3/build-acceptance.json` records map/script/package hashes, native
evidence, inherited floor checks and pending runtime cases. Seven linked package
files, including nested sound output, were hash-verified deployed to the separate
retail `usermaps/zm_pharmacie_dave66` folder. Deployment receipt:
`build/dave-bo3/deployment.json`. Backup:
`build/before-blender-test-20261025-123328`.

## Review and limits

[BO3 pose gallery](../recon/dave-bo3/index.html) and
[four-pose sheet](../recon/dave-bo3/bo3-pose-sheet.jpg) show the actual adapted mesh
in its bind pose and two stock zombie poses. These are Blender renders using
stock animation source frames, not screenshots from the game.

Beyond Sam's visible appearance approval, detailed runtime acceptance remains pending: pursuit, melee,
headshots/hit reactions, death/ragdoll/crawler behavior, completed rounds, co-op
and horde performance. Hands are weighted as rigid hand regions because the
generated source has no finger weights. There is no facial rig. Dismemberment
swaps are disabled for this prototype; proper Dave gib/crawler assets and the
stock hitbox fit still require review. No distance LODs have yet been authored.
Original opaque-glasses/likeness limits from [the model notes](DAVE_ZOMBIE_MODEL.md)
remain. No account credit was spent, no game inputs were sent and no Git push
was performed by this conversion task.

## Reproduction

1. Run Blender background with `scripts/prepare_dave_bo3.py`.
2. Run installed `export2bin.exe '*.xmodel_export'` from `build/dave-bo3/`.
3. Run `python scripts/package_dave_bo3.py` and
   `./scripts/build-dave-bo3-lab.ps1` (namespaced staging/backed-up GDT rebuild).
4. Run Blender background with `scripts/render_dave_bo3.py`, then
   `python scripts/gallery_dave_bo3.py` for the pose review.
5. Run `python scripts/generate_dave_test.py`, then
   `./scripts/build-dave-test.ps1` and `python scripts/accept_dave_test.py`.
6. Use `scripts/open-dave-zombies.ps1 -DeployOnly` for a checked deployment,
   or the launcher above when Sam is ready to control the test.

## Sources

- [ZeRoY's authored custom zombie model guide](https://wiki.zeroy.com/index.php?title=Call_of_Duty_bo3:_ZM_Models):
  character/archetype/variant/spawner chain, head/body and BO3 rig requirements.
- [pv_blender_cod format reader](https://github.com/prov3ntus/pv_blender_cod/blob/main/PyCoD/xbin.py):
  binary token layouts, bone matrices and animation frame format.
- [CoDEmanX exporter settings](https://github.com/CoDEmanX/blender-cod/blob/master/io_scene_cod/__init__.py):
  documented .010097 small-weight conversion threshold.
- Actual installed `model_export/t7_characters_zombie.gdt`, `archetypes/archetypes.gdt`,
  stock zombie body XModel, native walk/attack XAnims and official compiler logs
  supplied the acceptance evidence. Stock files are referenced, not redistributed.
