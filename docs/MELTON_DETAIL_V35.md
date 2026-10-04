# Melton Road detail pass v35

Checkpoint: `assets/blender/pharmacie-melton-detail-v35.blend`.

Sam requested substantially more detail while preserving the approved street plan. This additive pass retains all 10,217 parent mesh geometries and adds 2,860 closed meshes across 46 catalogue frontages. The road, shop positions, pub, Taraj interiors, brook opening and existing enclosure remain intact.

Added pitched terrace roof volumes, ridge caps, chimney stacks/pots, slate courses, cornices/dentils, lintel relief, alternate blind slats, restrained utility boxes/cables, listing-card grids, merchandise display relief, opening-hours panels, barber poles, projecting signs, florist tubs and Halls produce crates. Existing distinctive gables and earlier Amy/GLO/Specsavers roof work are retained. Golden Barber gains its reference-led black/gold fascia treatment.

Sources are the numbered dossiers in `docs/street-catalogue/entries/`, including native photo 00113 for the barber/florist/jeweller terrace. Details and business categories follow the catalogue; unseen roof slopes, precise chimney positions, generic merchandise and service fittings are modelling approximations. The original photos are neither embedded nor modified. Future work remains: the Town Square passage needs an actual enclosed traversable interior, the shelter and wider frontage architecture need further individual refinement, and most shops remain scenery rather than accessible rooms.

Validation: all 2,860 new mesh solids are manifold and have positive volume; all 10,217 parent mesh geometries and 44 reference hashes are unchanged. The 3,429 road-centre samples and 572 retained pub/alley samples pass at 0.42m radius. These are visible-mesh ray samples, not continuous collision sweeps or BO3 navigation/runtime tests. Engine files are unchanged.

Matched before/after review: `recon/v35/index.html`. Existing published v34 video remains at https://sammyt.wtf/preview.webm and shows the previous checkpoint.

Visual review caught the Banking Hub's asymmetric facade and clipped rear parcel. New details use the actual facade centre; its roof is restricted to the retained facade depth so it does not overhang the brook opening. Golden Barber lettering sits in front of the new black fascia.

Reproduce with `scripts/detail_melton_v35.py` on v34, `scripts/check_melton_v35.py` on v35, and `scripts/inspect_melton_v35.py` on each checkpoint. Logs are in `build/v35-*.log`. The small `fit_*v35.py`/sign-fix scripts document the inspection corrections to the first generated checkpoint; those corrections are included in the final generator and should not be reapplied to the final file.
