# User-selected Holmdale–Melton survey — 11 October 2026

Survey complete; latest connected Blender working copy is
`assets/blender/pharmacie-surveyed-route-v57.blend`. Read
`docs/SURVEYED_ROUTE_V57.md` for reconstruction, scale/placement limits and tests.
BO3 unchanged. Final Git delivery is authorized.

## Route identity

The user's actual route is in browser tab 3. Tab 2 contained the earlier 702 m
test; the assistant initially checked that older tab and corrected this openly.
Current saved export starts at `[52.6933508,-1.0789163]`, ends at
`[52.698169,-1.0721588]`, and follows Holmdale, Melton and Barkby Road for about 1090.77 m.
92 proposed observations at 12 m intervals; four directions each.

Original export and browser planner screenshot are local under
`references/streetview-capture/authored-route-2026-10-11/`. Originals, including
failed capture attempts, are retained; filenames and SHA256 hashes are recorded
in `ledger.json`. Personal imagery is ignored by Git. Do not force-add it.

## Collection method and limitations

Supported `cua_repl` browser actions open the visible Google Maps panorama URLs.
No hidden imagery API, panorama download endpoint, or extracted game assets.
Each image has requested stop/heading, actual visible browser URL when resolved,
page/AX observations, capture UTC time, SHA256, and visual review status.
DOM controls can precede image loading; native Tab.url can retain the requested
API URL. Later capture guard waits for a resolved `@52...` URL and records the
accessibility header. Earlier screenshots are visibly usable where marked but
some actual GPS locations remain unverified; do not substitute requested GPS.
The DOM's Report a problem link supplies an observed panorama ID for deduplication.
Contact sheets are separate derivatives. Black images must be retried with a new
revision, not overwritten or treated as evidence. Some neighboring stops resolve
to the same panorama. Planned stop count is not a unique-panorama count.

Holmdale imagery observed as September 2023; Melton images so far mostly March
2026. Dates apply per image, not uniformly to the whole route. Source labels are
camera-location labels and do not prove the address of a building in view.

## Observations reviewed so far

Directions below are relative to the authored route, generally northwest along
Holmdale then northeast along Melton. They are not house-number assignments.
Measurements are not established by these perspective views alone.

### Stops 001–005 (0–48 m): turning end and number 29 context

- Squared/widened end of tarmac carriageway, with footway/kerb around adjoining
  plots rather than a circular symmetrical turning bulb.
- Long red-brick boundary to one side, soldier coping and tall grey privacy
  screening backed by welded wire panels; garage joins its end near number 29.
- Number 29 retains the main hipped roof, smaller forward right wing, recessed
  corner porch and perpendicular dark-green garage. Use the user's 19 close
  photos for the porch; distant Street View must not override approved v51.
- Opposite end plots include low cream bungalows with dark hipped roofs,
  white garage doors and gravel aprons. Two-storey red-brick and mock-Tudor
  gabled houses begin immediately along the street; this is not all bungalows.
- Utility pole with multiple overhead cables, rounded yellow-green shrubs,
  low hedges, flowering borders and irregular drive entrances. Cars obscure
  portions of boundaries; do not model their silhouettes as architecture.

### Stops 006–010 (60–108 m): residential middle

- Red-brick two-storey semis with hipped roofs and shared central chimneys.
  White-rendered fronts alternate with exposed red brick and white window frames.
- Two-storey faceted/rectangular bay windows, small porch canopies and integrated
  single garages; individual roof/facade variants matter more than generic doors.
- Shallow gravel/concrete drives; short brick walls, metal gates, timber pickets
  and dense trimmed hedges vary plot to plot. A few open gravel forecourts.
- Parked cars occupy road edges and driveways. Narrow continuous pavements,
  no painted centreline on Holmdale, occasional covers and patch repairs.
- Street lamps and telephone poles sit near plot edges, not in pavement centres.

### Stops 011–014 (120–156 m): approach to Melton

- Hipped semis and some detached red-brick gabled houses with projecting glazed
  porch/bay forms; narrow side drives to garages or rear gardens.
- Taller greenery, purple-leaf tree, timber boundary along a corner plot;
  visibility opens to the main road near the give-way mouth.
- Holmdale mouth has road marking and bends into a much broader Melton Road.
  Keep the junction open rather than continuing residential kerb across it.

### Stops 015–020 (168–228 m): Melton junction and crossing

- Main road has centre/lane markings and double yellow edge lines around mouths.
  Broad footways and dropped crossing kerbs replace the narrower Holmdale edge.
- Low red-brick building at the corner; a row including a blue-fascia corner
  shop and grey/black Lucille Hair Studio frontage. Red cylindrical post box.
- Signal-controlled crossing: dark posts, signal heads, crossing studs/lines and
  tactile landing zones. Record as static Blender proposals, not engine signals.
- Across the road, open green with mature trees, low brick edge and footpaths;
  low buildings visible beyond. Don't fill this gap with a continuous terrace.
- Red-brick hipped semis with two-storey white bays, short iron front fences and
  green hedges continue after the shops. Road furniture should stay wall-side.

### Stops 021–027 (240–312 m): side roads, green and church vicinity

- Side-road mouths break the housing frontage; pale street-sign plates and
  short metal boundary rails. Reddish block/coloured road surface at one mouth.
- Large dark evergreen and adjoining green with low pale picket/metal fence.
- Brick church-like building with tall decorative front window/gable and
  a small lawn enclosure; exact venue identity needs close sign verification.
- Opposite, open parking/vehicle forecourt, long low boundary and detached
  Victorian red-brick building with pale window surrounds and projecting bays.
- Older frontage replaces hipped semis: two-storey brick houses, slate pitched
  roofs and prominent tall chimneys. Pavement backs directly onto some walls.

### Stops 028–035 (324–408 m): terrace and retail cluster

- Two-storey Victorian brick houses with white bay-window surrounds, small
  brick-walled front gardens, some grey/white-rendered fronts and inset doors.
- Side street opens beside a white corner building. Double yellow corners,
  short black bollards and a corner retail apron.
- GREEN'S OFF LICENCE visible on a pale fascia below a tall steep gabled brick
  building; adjacent narrow shops have individual blue/white/dark fascias.
- Opposite Happy Garden has a bright yellow fascia below a bay and a small
  peaked upper frontage; adjoining grey-fronted business and side-street gap.
- Retail terrace includes dormers, projecting upper bays, tall chimney stacks,
  green fascia and varied sill heights. Do not substitute one repeated shop.
- Stop 035 ahead was black in the first revision; reject/retry that image.

### Stops 036–040 (420–468 m): modern infill and wider gaps

- Long modern red-brick residential block with shallow gabled roof sections,
  regular small white windows, grey horizontal bands and black front railings.
- Opposite, mixed old shops and a flat-fronted brick structure with arched lower
  openings. Then open construction/yard area behind a low irregular brick wall.
- Large mature roadside tree at a corner, low red-brick commercial/hall mass
  beyond, a bus-stop area and a side road beside the residential block.
- More negative space than the dense retail stretch: preserve yard depth and
  sightlines instead of filling every road edge with building boxes.

### Stops 041–045 (480–528 m): independent businesses and hall

- Dark teal/charcoal cafe-like corner frontage, repeated display windows and
  long fascia under upper white sash-style windows. Exact lettering needs close
  inspection before transcription; model the observed panel divisions first.
- Small dark-painted shop with a peaked pediment above a recessed central door;
  separate display windows either side. Steps sit within its apron.
- L. HARRIS / joinery manufacturer signage on a low brick frontage, pale sloped
  roof, shuttered openings and narrow access lane alongside a taller brick end.
- Opposite brick hall has broad arched white windows and vivid blue double
  doors below a shaped gable; adjoining historic brick terrace.
- Detached two-storey bay-fronted brick corner building and side-road entrance;
  street furniture/fencing varies and the junction must remain traversable.

### Stops 046–050 (540–588 m): crossing, small green and supermarket

- Bay-fronted red-brick corner property, low black railing and side-road opening.
- Zebra crossing has striped Belisha posts with yellow globes and pavement
  approach space. Small green/public space with trees and a visible monument
  beyond; exact monument details remain pending close inspection.
- Large low supermarket has grey/white panel cladding, dark framing and a
  long glazed front; ALDI logo visible. Sloped broad roof form, deep setback,
  planted verge with flowering trees, shrubs and grass.
- Opposite brick terraces sit much closer to the pavement; pale stone/white
  shopfront beside them. Preserve this asymmetry of street setbacks.

## Scale and reconstruction gates

### Stops 051–060: supermarket, large forecourts and Taraj

- ALDI has a broad glazed entrance/canopy, low sloping roof, open car park,
  landscaped curb islands and trees. Opposite houses sit behind short walls;
  setbacks differ substantially from the tightly packed shops further north.
- Low brick commercial/hall side walls, steel gates and open yards precede a
  long shallow-roof pet-store frontage with blue fascia and tall sign pylon.
- Public paving near the pet store includes bollards, an ornate clock/pole and
  hanging flower baskets. Signal crossing has tactile landings; keep these clear.
- Mace occupies a pale corner shop opposite; adjoining narrow grey shopfronts
  have separate doors/windows. Taraj's cream frontage, blue awning and recessed
  entrance are visible. Retain the user's approved existing Taraj assembly.

### Stops 061–070: retail terrace and brook bridge

- Taraj's end wall and access opening lead to Costcutter Carpets & Beds, a broad
  pale flat frontage with large windows, signage and pavement displays.
- Opposite narrow brick/render shops have individual fascia heights and doors;
  FOX lettering is visible on a dark fascia. Do not assume every sign is current.
- Green-awning corner florist/retail frontage has plant displays and a setback;
  road crosses a brook with metal rails on both sides. Glass bus shelter nearby.
- Bridge approach opens beside a parking/public-space entrance; ornate historic
  brick frontage beyond has shaped gable, arched features and chimney details.
- Two-storey brick shop rows: green Specsavers frontage, blue/white signs,
  varied pitched roofs/chimneys. Gold/coin sign on the opposite corner. Bus stop
  and green-framed shelter stand in a pavement widening, not the traffic lane.

### Stops 071–080: central shops and roundabout approach

- Food Warehouse occupies a long modern brick block with large ground glazing,
  bright boards and upper windows; railed ramp/steps in its recessed apron.
- Opposite William Hill, Byrite Electrical, Greggs and Sunlit Chemist are separate
  premises; varied older render above a continuous modern brick shop strip.
- Syston grocery corner, vehicle access gap and a lower blue/yellow frontage;
  across the road a brick chemist complex has repeated steep gables and a narrow
  upper feature window. Keep the access gap open.
- Costa has two prominent brick gables, burgundy fascia and ground glazing;
  Betfred is lower alongside. Nearby traditional brick building has circular/
 arched ornament and a paved area with temporary canopy (not permanent geometry).
- Bistro Oggi's dark teal corner has stepped cornice, rectangular upper windows,
  recessed ground windows/door. Adjacent narrow red shopfront is separate.
- Mini-roundabout and zebra approaches: splitter/refuge islands, yellow globes,
  signs, lamp posts, traffic markings and broad corner pavement. Parked vehicles
  and buses occlude portions; use the other directional views for those walls.

### Stops 081–092: turn into Barkby Road

The small contact sheets were initially misread as Brook Street. The panorama
titles, road text and mapped coordinates establish **Barkby Road**; this corrects
the commentary. Brookside is a different nearby street visible on the overhead.

- Wraparound teal Bistro Oggi corner continues as a low service side wall with
  small high windows, vents, alarm and kitchen extraction. Side yard/open gates
  must remain separate from the neighbouring building.
- Opposite Head 2 Head and traditional brick terraces have individual white sash
  windows/doors, narrow front strips and occasional taller three-storey volumes.
- Tall old brick house has white door surround; adjacent dark timber/metal gates
  and garages form a low side-drive boundary. Red/cream brick side walls vary.
- Low long commercial sheds behind a forecourt/parking entrance, iron fencing,
  hedges and white-painted cottage pair with tall chimney stacks.
- Further along: narrow Victorian brick terraces with stone lintels and recessed
  doors, individual front gardens; gravel/paved drives between building groups.
- Blue-painted end house beside a cream-painted house, three ground/upper
  openings, neighbouring exposed-brick gable; red-brick hipped semis opposite
  with bay windows, white low fences and short driveways. Utility pole/wires.
- Stop 092 is the selected endpoint, not an observed road termination. Any map
  closure beyond it is a gameplay adaptation and must be labelled as such.

## Collection completion

All 92 proposed stops have four reviewed directional images. Twelve initial
unloaded attempts remain rejected. Stop 035 ahead r2 was black and retained;
r3 is the accepted full-size retry. Later views include April 2023 imagery;
Holmdale September 2023 and Melton March 2026 cannot be treated as one survey date.
`metadata-repair.json` separately records resolved visible panorama URLs for the
first 45 stops; retain requested and resolved coordinates as different fields.
Saved satellite screens cover the whole route, station/Holmdale, the turning end,
town centre and Barkby junction. Copyright date does not establish capture date.

Existing extension transform: `recon/v41/extension-route.json`, 1.0640686466
Blender units per geographic metre and rigid rotation -139.215303 degrees.
This was inferred to join the approved older map; it is not survey measurement.
At that scale a 1 m observed dimension should use 1.0641 BU consistently.
Google top-down comparison must check road bends, plot sides, building footprints,
setbacks and junction mouths. Use at least two identifiable distance baselines;
record uncertainty and discrepancies instead of claiming exact physical scale.
Do not globally rescale or move approved old pub/retail/house geometry to conceal
alignment error. Any adaptation should be recorded separately from observation.
Height estimates need roof/eaves/storey checks; perspective alone is insufficient.
After modelling: closed-mesh checks, source fingerprint preservation, selected
clearance/support rays and matched previews. These are not BO3 runtime tests.

Remaining: finish all 92 stops and image retries/metadata repair, Google overhead
comparison, detailed catalogue, reconstruction and verification/previews/push.
