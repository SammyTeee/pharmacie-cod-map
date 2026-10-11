# Extension delivery audit — 11 October 2026

The original Street View / Blender extension goal is delivered as an editable, evidence-led working copy. This audit is separate from the v58 engine startup issue.

| Requirement | Current evidence |
| --- | --- |
| Recon selected A/B route | recon/v53/capture-manifest.json: 92 stops, 368 accepted directional views over 1,090.77 m. The actual user export follows Holmdale–Melton–Barkby; older Taraj corridor is retained. |
| Save screenshots with provenance and detailed notes | All 368 recorded local originals were rehashed during this audit: zero missing or changed. Manifest contains URLs, dates, positions, hashes and metadata caveats; docs/AUTHORED_ROUTE_SURVEY_2026-10-11.md records observations. Originals remain local, excluded from Git. |
| Reconstruct connected route and number 29 | Saved v57 includes added road, 60 frontage assemblies, station approaches, end-plot relocation and asymmetric turning apron. Nine review images cover house, porch, Holmdale overhead and street sections. |
| Best evidence-supported scale / overhead fit | docs/SURVEYED_ROUTE_V57.md and recon/v56/prepared-final.json record 1.0640686466 BU/m, north-up pixel trace, road width comparison and tolerances. Concealed depths remain estimates; the 20.25 m Barkby joining compromise preserves approved old buildings. No exact-survey claim. |
| Preserve approved house/pub geometry | v57 build-validation preserves 24,102 prior active objects; approved number 29 assembly unchanged from v53 placement. recon/v57/v40-preservation.json records all 15,512 original fingerprints unchanged, with five obsolete boundary pieces archived. Porch preview visibly retains central door and two glazed returns. |
| Verify geometry and routes | recon/v57/build-validation.json: 435 latest closed meshes, no nonmanifold/nonpositive entries. route-checks.json: 39,771 clearance rays / 4,419 support samples, zero failures across eleven selected routes. Two lateral enclosure misses remain disclosed; these checks do not prove complete containment or engine behaviour. |
| Show previews | recon/v57/index.html and nine tracked PNGs; house porch and Holmdale overhead inspected again in this audit. |
| Commit / push editable deliverable | v57 Git blob 0238de75b7907f99596445c4af33b770d2466b38 matches local hash-object. Mapping commit da30d12 is in origin/master; later v58 source commit f4000d2 also pushed. |

Remaining refinements are explicitly approximate scenery/hidden architecture and optional future detail, not missing route collection or missing editable delivery. Successful v58 compilation does not establish runtime purchases, traversal, AI or co-op. The startup exit remains a separate unresolved engine-test issue.
