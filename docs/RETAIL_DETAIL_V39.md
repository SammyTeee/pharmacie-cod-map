# Individual shop display detail v39

Latest checkpoint: `assets/blender/pharmacie-retail-detail-v39.blend`, from v38.
Matched review: `recon/v39/index.html`.

Sam requested continued substantial detailing and a push. This pass adds 1,118 closed mesh solids across six existing businesses: Designer Daisies flower pots with stems/petals/tickets, Syston Jewellers velvet trays/rings/necklaces, Specsavers spectacle rims/bridges/arms/stands, Greggs bread trays/scoring, Age UK hanging shirts/folded clothes/tags, and Costcutter Carpets & Beds rolled carpet/sample swatches. Separate cloth/paper materials have fine procedural grain. Existing entrances, opaque glazing/backing, building positions and all pub/Taraj/Town Square interiors are retained. 72 superseded generic display parts are archived unchanged.

Business categories come from the numbered B035/B036/B015/B024/B017/B002 street dossiers; native00113 provides the visible florist/jeweller reference. Individual products, stock arrangements, generic wording and display construction are modelling approximations, not surveyed inventory or evidence for shop interiors. No new photo-derived raster assets or source-photo edits. Shops remain closed scenery.

Close-up review caught inward normals on reoriented horizontal pot/carpet rings; corrected the winding in the generator and saved checkpoint. Added small supports beneath spectacles and display rings to avoid floating goods. Temporary render lighting is never saved.

Validation: new meshes are manifold positive-volume solids; 13,941 parent mesh geometries/transforms (including archived originals) and 44 original reference hashes retained. Road/pub checks and 1,054 selected pavement/shelter/Town Square entry samples pass at 0.42m radial clearance. These are sampled visible-mesh rays, not full pavement circulation, continuous capsule collision, BO3 AI, purchases, stepping or co-op tests. Engine unchanged.

Reproduce with `detail_street_v39.py` on v38, then `check_street_v39.py` and `check_local_street_v39.py` on v39. `inspect_street_v39.py` makes matched images on v38/v39; `gallery_street_v39.py` verifies image files and writes the gallery. The normal/support fix scripts document intermediate corrections, now incorporated in the final generator; do not rerun them on the final checkpoint. Logs: `build/v39-*.log`.

Further work remains: more individual facade architecture, street wear, deeper display bays and selected accessible shop interiors, plus separate Radiant conversion/runtime tests. This pass is not a finished street or engine release. The existing hosted v34 video remains the previous tour.
