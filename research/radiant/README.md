# BO3 Radiant learning packet

Prepared 4 October 2026 for the eventual Pharmacie conversion. Start with
[the conversion playbook](../../docs/RADIANT_CONVERSION_PLAYBOOK.md), then
[the placement plan](../../docs/RADIANT_GAMEPLAY_PLACEMENT_PLAN.md) and
[the installed-stock audit](../../docs/RADIANT_STOCK_GAMEPLAY_AUDIT.md).
This is research and planning, not a new engine build.

## What is saved locally

The [tutorial library index](tutorial-library/README.md) links 15 selected BO3
pages from the **UGX-Mods community wiki**, stored as unchanged HTML plus
readable plain text. The library includes its unchanged license, credits and
upstream README. Some pages are short indexes or image-only stubs; the index
identifies them. Image/video references remain links, not downloaded media.

[sources.json](tutorial-library/sources.json) records the exact upstream paths,
commit, retrieval timestamp, byte counts and SHA256 hashes. The snapshot is
pinned to `331184f27904c1fbe24cd59b5d752511f698746a`; it does not follow `main`
silently. The upstream wiki is a Confluence migration and warns about broken
formatting/links. Its beta-era guidance needs comparison with the installed
tools and our actual results.

[External reading notes](tutorial-library/EXTERNAL_READING_NOTES.md) store
short original summaries and links for additional author-written tutorials.
They are not scraped full copies or video transcripts. The licensed UGX
snapshot is kept separately under `vendor/ugx`; its license and derivative
notices apply to those files. No license change to the map is asserted here.

## Offline use

Search the saved text without opening a browser:

```powershell
rg -n 'riser_location|player_volume|treasure|barrier|script_string' research/radiant/tutorial-library/vendor/ugx -g '*.txt'
python research/radiant/collect_tutorials.py --verify
```

The verifier checks all 33 source/derivative files against the manifest; it
does not validate tutorial accuracy or engine behavior. The collector uses
only Python's standard library and `curl.exe`. It refuses to overwrite an
existing snapshot. `--refresh-text` rebuilds readable text offline from the
unchanged HTML and records updated derivative hashes.

## How future agents should use this

1. Read the latest street/alley handover and choose the intended saved Blender
   checkpoint explicitly. Do not infer a new baseline from a version number.
2. Read the playbook, placement JSON and stock audit before authoring gameplay.
3. Use installed stock sources to settle actual KVPs and prefab composition;
   use tutorials to understand the workflow. Record any disagreement.
4. Make one small conventional feature work before widening gameplay: wall
   buy, bought gate/zone, power/perk, then box/Pack-a-Punch as separate slices.
5. Inspect the generated map in Radiant and verify it in BO3 under the existing
   controls/deployment agreement. Preserve evidence for each feature.

The universal-modder knowledge index was searched during this research pass:
[upstream index](https://github.com/rehan-remade/universal-modder/blob/main/knowledge/INDEX.md).
It contained no BO3-specific field note at review time. Project-specific
findings therefore stay in this repo's audit, playbook and MODLOG.
