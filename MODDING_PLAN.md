# Call of Duty: World at War modding plan

- **Install:** Steam PC version at `S:\SteamLibrary\steamapps\common\Call of Duty World at War`.
- **Observed version:** `CoDWaW.exe` reports file version 1.7 / product version 1.7x; adjacent `version.inf` says `ExtVersion=1.6`. Verify the version displayed by the running game and reconcile before compiling.
- **Engine/toolchain:** WaW's PC World at War Mod Tools, Radiant map editor, Asset Manager, and map compile/light/link/fastfile stages. The separate Mod Tools folder was not found next to the game in the initial directory check; confirm Steam Tools library state and exact paths. Do not install into the game folder without the user's approval.
- **Game mode/safety:** User-owned PC game. Develop and verify custom Zombies in offline/single-player/private use only. No anti-cheat bypass or public multiplayer modifications.
- **Chosen route:** Official/community-standard native map authoring. It reaches the requested custom level and gameplay directly and handles collision, player movement, zombie navigation, and round scripts. Gaussian splats are not the level format and are not suitable as playable collision/pathing geometry.
- **Map naming:** Use lowercase `nazi_zombie_<suffix>`; the suffix is not yet selected. Create from a working Zombies template and preserve required scripts/prefabs.
- **Milestones:** (1) compile/launch template; (2) block out main room and exterior shell; (3) prove spawn, zombie pathing, rounds, doors; (4) apply one photo-derived pharmacy feature-wall texture; (5) dress the pub and improve lighting; (6) add and tune Noseley boss; (7) package with provenance/credits after rights and build checks.
- **Asset approach:** Keep the originals in `references/pharmacie-syston/`. Derive selected custom wall panels from front-on photos, while modelling major architecture, bar, display cabinets, and gameplay objects in Radiant or a validated model workflow. Inspect stock WaW source textures and Asset Manager conversion settings before choosing final dimensions/format.
- **Lab plan:** Keep sources and intermediates in this repository; keep extracted game files outside the repository. Do not alter saves or the game install as part of initial map work. Ask before installing tools into the game directory, changing settings, or publishing.
- **Unknowns:** Mod Tools installed path/version; running game version; available Zombies template/scripts; accepted raw image source and final texture format/compression; main-room dimensions and upstairs/side-room plan; Noseley model/animation constraints; licensing for web-sourced images.

## External references

- [Official Steam listing for World at War](https://store.steampowered.com/app/10090/Call_of_Duty_World_at_War/)
- [World at War Mod Tools mapping overview](https://openmods.net/guides/getting-started-call-of-duty-world-at-war)
- [Modme: creating a basic Zombies map](https://wiki.modme.co/wiki/world_at_war/Creating-A-Basic-Zombie-Map.html)
- [Zeroy: World at War Zombies map tutorial](https://wiki.zeroy.com/index.php?title=Call_of_Duty_5%3A_Zombie_Map_Tutorial%3A_Der_Riese)
