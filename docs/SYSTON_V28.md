# Syston street appearance and detail — v28

Latest saved source: [pharmacie-syston-detail-v28.blend](../assets/blender/pharmacie-syston-detail-v28.blend).
This continues the complete v26 Taraj/bridge scene through v27 and v28.

V27 changes street materials and adds Costa awnings, outdoor tables/chairs and
window divisions. V28 adds crossing markings, tactile paving and spherical
Belisha beacons; kerb joints, drain grilles and utility covers; roundabout arrows;
and individual Costa, Amy Clarke Hair, Specsavers and GLO frontage treatments.
Amy Clarke now has a central entrance, broad white-framed windows, brick base,
upper window rails/lintels and two topiary pots.

![Crossing](../recon/v28/01_crossing.png)

![Amy Clarke Hair](../recon/v28/02_amy_clarke.png)

![Costa](../recon/v28/03_costa.png)

![Street and bridge](../recon/v28/04_street.png)

The completed Blender log ends with `V28_COMPLETE` and `Blender quit`.
[V27 checks](../recon/v27/validation.json) record 6,659 retained mesh geometries,
394 material assignments and 91 new closed solids. [V28 checks](../recon/v28/validation.json)
record 6,749 preserved mesh geometries, 2,031 new closed solids and 390 clear
upward road rays. Superseded details are archived. These assertions ran during
generation; they are not independent saved-file or BO3 navigation verification.
Crossing and Amy Clarke renders were visually reviewed after crash recovery.

Road/parcel dimensions remain estimated. Drain and cover placement is indicative.
Dropped crossing kerbs still need reconstruction; the crossing render shows
raised edges. Other frontages still need comparable individual detail. Glazing
is opaque scenery; no unseen shop interiors are claimed. No engine export,
compiler run, deployment or game test was performed for these passes.

Reproduce in Blender 5.2 from v26 with `scripts/refine_syston_v27.py`, then
`scripts/detail_street_v28.py`. Each script opens its own input checkpoint.
Temporary review daylight is applied after saving. Four v28 Cycles renders use
1400×950 resolution and 20 samples. Local logs: `build/syston-v27.log` and
`build/syston-v28.log`.
