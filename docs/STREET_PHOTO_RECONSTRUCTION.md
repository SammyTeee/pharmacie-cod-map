# High Street and Pharmacie exterior: photographic reconstruction specification

Reviewed 2026-10-03. This is a detailed description for rebuilding the visible street, not a description of the existing approximate Blender scenery. Sam requested as much useful photographic detail as possible. Read this before rebuilding the street or assigning shopfront textures. Pub interiors have their own [specification](PUB_PHOTO_RECONSTRUCTION.md). Exact originals, dimensions, review coverage and hashes are in [RECONSTRUCTION_SOURCE_INDEX.md](RECONSTRUCTION_SOURCE_INDEX.md) and reconstruction-sources.json.

## Evidence conventions and orientation

- **Observed** means visible in the named source, including appearance rather than guaranteed construction material. **User-confirmed** means Sam explicitly established it. **Inferred** means a plausible connection across overlapping photographs. **Proposed** means a modelling/gameplay choice. **Unknown** means the source does not establish it. Do not silently upgrade these categories.
- Unless specified otherwise, left/right in a building description means looking directly at that building from the street. Image-left is not always world-left. When looking out of the Pharmacie towards the opposite row, left/right reverses relative to looking at the Pharmacie.
- Keep the existing project convention: street face approximately Y=0, pub rear towards +Y, X increasing to the right when facing Pharmacie. The opposite shops face the pub, and their photo-left runs towards increasing world X when viewed from the pub (you turn around to look at that row). Do not reverse a photograph to compensate for placement order.
- Name the two longitudinal street ends **crossing end** (Post Office/Natural Wellbeing views) and **junction end** (Fox & Hounds corner). These labels avoid unsupported compass directions and ambiguous 'left end'.
- Street View UI address labels indicate the panorama's location, not necessarily the address of every shop visible. Do not assign building addresses from them. Apr2026 is shown on several captures; dates in watermarks vary and are not independent capture dates.
- The whole-street reconstruction should preserve adjacency, facade rhythm, roof variation and sightlines before chasing tiny lettering. A photogrammetric survey, rear access coverage and a real scale anchor are still absent. Notes can guide a close visual match but cannot recover invisible geometry or exact distances.

## Source map: which image answers which question

| Sources | Strongest evidence | Weakness / best modelling use |
|---|---|---|
| S01 | Wreake Valley frontage and junction with pub | Roof/top partly clipped; best for joinery and lettering |
| S02 | Dry cleaners and nail/spa unit right of pub, road towards crossing | Strong oblique perspective; good depth/order, poor direct whole-facade texture |
| S03/S04 | Mini Market fragment, Aston, broad Fox frontage | Cars hide bases; close overlap, not two separate buildings |
| S05 | Floral and Let's Move including upstairs bays, parking edge | Oblique; exposes bay depth and kerb return |
| S06 | Near-frontal Mini Market, Aston, Let's Move, partial Floral/Fox | Cars/people/UI occlude; good main elevation proportions |
| S07 | Alley, Wreake side wall and pub attachment | Rear alley continuation not fully visible |
| S08 | Post Office crossing looking towards shop row/junction | Distant fronts compressed; best overall street sightline |
| S09 | Natural Wellbeing access gap, Post Office, Papermoon, Pasha | Traffic poles/people obstruct patches; useful overlapping elevation |
| S10 | Papermoon/Pasha/Floral transition and Post Office edge | Roof and utilities visible; crop pieces individually |
| S11/S12 | Opposite shop sequence and disabled parking build-out | Cars hide pavement/door bases; resolve order and roof modules |
| S13 | Fox front, right corner return, junction/island | Useful 3D corner evidence; distant continuation incomplete |
| S14/S15/S16 | Natural Wellbeing front gable and deep side return | White blank screenshot border in originals; never texture that margin |
| P07/P08/P25 | Whole pub terrace and upper roof/chimney rhythm | Different sign/date state; photographic perspective, not measurements |
| P15/P28 | Pharmacie joinery, recess, upper details | P15 roof omitted; P28 angle shows depth but compresses width |
| P11/P27 | Pub lighting and entrance at night | Condensation/reflections conceal interiors; not alternate wall geometry |

## Street topology: connections that must survive reconstruction

**User-confirmed and supported by S07:** facing Pharmacie, the narrow access alley lies beyond the left edge of Wreake Valley Flooring. Wreake Valley directly adjoins Pharmacie; Pharmacie directly adjoins the dry cleaners. There is no frontage alley between flooring shop and pub. Treat the existing separated left scenery block as an error, not source evidence.

**Observed opposite-row sequence, from crossing end towards junction end:** Natural Wellbeing; a separate access lane; Post Office; Papermoon; narrow white doorway associated with HM signage; Pasha Barber; Floral Fantasy; a narrow blue doorway at the Floral/Let's Move transition; Let's Move; Syston Mini Market; narrow dark passage/doorway beside Aston; Aston & Co; Fox & Hounds corner. The narrow doorways belong within the terrace rhythm; they are not automatically full-width public alleys. Exact ownership of upstairs access doors is unknown.

**Observed pub-side sequence, facing its fronts:** alley → Wreake Valley → Pharmacie → Syston Dry Cleaners and Laundry → blue-fascia nail/spa shop → further attached fronts towards the crossing. Beyond the blue shop, S02/P08 reveal other fronts, a green unit and a larger brick building with projecting red signs; identities and full ordered inventory are not established sufficiently for exact shop text. Use documented placeholders there until close source coverage exists.

The Post Office row is an extension of the opposite side, not another building beside Pharmacie. Natural Wellbeing is at the crossing end of that row. Fox & Hounds is the junction landmark at the other end. The roadway is a town-centre corridor with bends/kerb changes and junction infrastructure, not an isolated ruler-straight road strip surrounded by countryside.

## Shared architectural vocabulary

### Pharmacie/Wreake terrace module — P07/P08/P25/S01/S07

- Observed: two-storey frontage with a pitched grey slate-like roof over red/orange brick. Matching dark-framed tall upper windows continue across Wreake and pub. Roof ridge runs along the terrace rather than each shop receiving an independent front gable.
- Observed: both shops share the same upper architectural language. Wreake has three upper windows and Pharmacie has three; P08/P25 show the six-window sequence. The shop division is apparent through fascia colour and a rainwater pipe/vertical boundary, not an air gap.
- Observed: windows have many small rectangular panes, heavy dark outer frames, a horizontal sash division, pale lintels and pale projecting sills. Some panes show curtains/blinds; do not bake different nearby shop reflections into the window geometry.
- Observed: two dark blue/grey brick courses form a horizontal band around sill level, continuing along the frontage and exposed side. A decorative alternating brick/dark course runs below the eaves. These continuous bands are more useful alignment anchors than signage.
- Observed: gutters are dark, eaves project slightly, and black downpipes run down the frontage/edges. Weathering collects on pale stone sills and the fascia's top flashing. The roof has many thin horizontal tile courses, not a giant flat grey cap.
- Observed: brick chimneys punctuate the roofline, with pale/terracotta pots; roof antennas occur in wider views. Chimney count/location should be traced from P08/P25 rather than evenly repeated above every shop.
- Unknown: complete back roof shape, structural separation inside adjoining buildings, true overall depth and surveyed roof pitch. Visible silhouette can be matched without pretending these are known.

### Opposite terrace modules — S06/S09/S10/S11/S12/S13

- Observed: the Post Office/Papermoon/Pasha section has a relatively low continuous pitched roof and paired white upstairs windows. Floral/Let's Move introduces two projecting white upper bays with small pyramidal/hipped roofs. Mini Market/Aston sits under a taller corniced roof module. Fox drops back to a lower, broader cream frontage.
- Do not force one common ridge height, one window type, or one flat roof across this whole row. The stepped silhouette and bay projections are defining features.
- Observed: chimneys sit along party-wall positions and within roofs; dark gutters and downpipes break the red-brick elevations. Small wall cables, lamp brackets, alarms, aerials and satellite dishes create secondary detail.
- Proposed: ordinary wall faces use repeatable brick/render materials; photo derivatives provide shop signage and carefully selected display panels. Bay depth, thresholds, roof shapes and side returns should be geometry.

## Building B01: Wreake Valley Flooring

Sources S01/S07/P07/P08/P25. Confidence: high for facade/order, low for unseen interior/depth.

- Broad olive/sage-green timber-style shopfront with a cream sign panel. Green is muted, neither bright neon nor turquoise. The top fascia has a projecting green cornice and scroll-like end brackets.
- Lettering reads 'wreake valley flooring' in lower-case green, with the initial portions of words darker/bolder than others. Small telephone text occupies the left of the cream sign; overlapping outlined rounded-square logo appears at the right. Sign is horizontal and extends across the whole frontage.
- Two green square/fluted outer posts stand on the pavement line. Their bases terminate at a shallow green plinth. A dark rainwater pipe lies near the outer brick corner on the alley side.
- Shopfront is recessed towards a central green double door, with broad front display panes and angled inner returns forming a shallow trapezoidal entry bay. It is not a flat rectangle with a door pasted onto its centre.
- Door leaves each have a tall glazed upper panel and solid recessed lower panel. A glazed transom sits above the doors. Small stickers/posters cover portions of glass; a horizontal letter plate appears low on one leaf.
- Recess floor is pale small rectangular tile, clearly distinct from the grey/brown pavement slabs outside. No prominent raised entrance step is visible in S01; do not infer a high platform.
- Large glass windows show flooring samples and pale display racks. White/red Karndean graphics occur on both major panes; white 'amtico flooring' lettering is prominent on the right. Display reflection includes the opposite shops; it is a reflection, not another facade physically inside this shop.
- Grey translucent text bands sit near display-window bottoms. Window framing is green throughout, with dark interiors and bright fluorescent-style ceiling strips glimpsed inside.
- Three upper dark sash windows in the shared brick terrace above. Their heights/heads/sills align with the pub's three. Wreake frontage appears comparable in module width to pub in the broad terrace photographs; existing gameplay scene widths are not real measurements.
- Small alarm boxes occur on upper brick between window groups. Photograph dates show no basis for making these giant props.
- Rebuild priorities: adjacency first; green/cream fascia; recessed double-door geometry; matching upper module; coherent alley-side return. Interior flooring-shop layout is unknown and can remain scenery.

## Site A01: alley beyond Wreake Valley

Sources S07/S01/P08. Confidence: high for mouth location and side-wall appearance; rear route unknown.

- Alley opens immediately beyond Wreake's left outer corner, between the flooring shop's deep side elevation and a neighbouring building with white-painted lower wall/red-brick upper wall.
- It is a narrow vehicle-access opening in S07, containing a small white hatchback. Use the car only as qualitative evidence that this is wider than a single-person slot; do not calculate a precise metre width from an unidentified foreshortened vehicle.
- Short red-brick boundary wall with dark coping extends near the mouth alongside Wreake. White vertical gateposts bookend visible boundary sections. A small dark-blue notice is attached to the wall; exact text is unreadable and should not be invented.
- Wreake's side wall is long, largely blank red brick, with matching blue/grey horizontal bands wrapping around the corner. Some pale rectangular infill/stone patches are visible; the sources do not prove they are usable windows.
- A tall vertical flooring-ad panel is attached near the front corner of the side elevation. It contains stacked flooring/interior images and red/cream/grey areas; amtico and Karndean branding is partly readable. Model as a flat sign/decal against the side wall.
- Ground appears worn mixed hard paving with patches/discolouration rather than a continuation of pristine road asphalt. Green weeds occur at the wall/pavement edges.
- Rear depth, gates further back, connection to Pharmacie rear exit and property boundaries are not fully photographed. Reconnecting the game route behind the neighbour is a proposed playable adaptation, not verified geography.
- Do not confuse this opening with the separate lane between Natural Wellbeing and the Post Office, or with the narrow dark doorway between Mini Market and Aston.

## Building B02: The Pharmacie Arms exterior

Sources P15/P25/P28/P07/P08/P11/P27, with S01/S02/S07 for neighbour relations.

### Overall composition

- Broad black shopfront below three tall dark upper sash windows in red brick. Matching shared roof and brick band language with Wreake as described above. The adjacent dry-cleaner upper facade is a different taller module with larger white-framed windows.
- Facade reads as layered joinery: projecting top cornice/flashing, broad sign field, moulded lower fascia rails, fluted/decorative terminal corbels, tall panelled side pilasters, angled display bays and recessed inner entrance. Do not simplify the visible profile to a single black plane if matching street-level views.
- Black finish is slightly worn and satin/dull; exposed edge weathering is grey. Fascia lettering is large white serif mixed-case 'The Pharmacie Arms'. Smaller white uppercase 'FREEHOUSE' sits centred above main wording.
- P15 shows a dark 'CAMRA Pub of the Year' banner across the lower middle upper-window area. P25/P28 instead show a pale 'JB KITCHEN' board with smaller 'UPSTAIRS AT THE PHARMACIE ARMS' text. These are alternate photographed states. Select one documented time state; do not stack both on top of each other as permanent decor.
- Alarm boxes sit on brick beside lower upper-window regions; one pentagonal/polygonal pale box is near the kitchen sign. Black downpipe at left/shared boundary; blue pole is at the right boundary towards dry cleaners.

### Entrance and display bays

- P15 shows left outer display pane, angled inward pane, recessed fixed glazing, entrance-door assembly offset to the right within the recess, inward right pane, right outer display pane. The walk-through portion is not the entire width of the recess.
- Both display bays project from inner entrance line to the outer shopfront/pavement line. Angled return glazing is a critical silhouette from P28; define real corners and depth.
- Low blue/pale-cyan patterned bands occupy the lower display glass, above dark plinth panels. The pattern is a dense small repeated motif. This is not pale-blue paint covering the entire shopfront.
- White decorative plaques on display glass list drinks: Cask Ales/Lagers, Craft Beers/Ciders, Wines/Spirits, Cocktails. Plaques have curved/notched ornamental corners and dark centred serif text.
- Outer vertical pilasters are black, tall, with inset elongated rectangular panels and broader bases. Dark tiled plinth runs below display windows. The fascia corbels at top outer ends have vertically fluted/curved profiles.
- Inner glazing and doors are black-framed. P15 closed state shows fixed left glazed panel and door assembly to its right; P26/P28 open state gives real depth and door swing evidence. Preserve the existing offset entrance interpretation; verify hinges/panes against these sources before modifying openings.
- Door lower panels are solid black, with inset moulding and brass-coloured hardware/letter plate visible. Door/stile glass contains many small stickers; these are decals rather than separate thick collision blocks.
- A long dark inner lintel carries two lines of small white text describing real ale/craft beers/ciders/wines/gin/spirits and snacks/soft drinks/tea/coffee. Treat this as an inner recess sign rather than the main external fascia.
- Recess/threshold surface is dark brown small rectangular tiles/brick pavers in a regular pattern. It extends across the entrance bay and meets larger pale pavement slabs outside. A continuous game collision floor is necessary; a photo shadow is not a hole.
- A standing menu/live-music sign sits near the left/centre recess in some sources; another narrow black 'OPEN/WELCOME' board sits towards the right in P28. These positions vary; do not permanently block the doorway with both.
- Vertical illuminated OPEN sign appears on left glazing. Posters/menu notices and small circular stickers occur on both sides. Texture layers must avoid duplicated opposite-shop reflections.

### Lighting/state

- Night image P11 shows five bright downward pools along the main fascia. Small recessed lamps under top fascia/cornice provide them; they are not five huge hanging exterior lamps.
- A line of white fairy/string lights sits above fascia at the brick/flashing transition in P11/P27. It is an observed night arrangement, not proof of year-round presence.
- Interior glows warm behind windows, with occasional coloured light/reflections. Night condensation makes glass cloudy. Reproduce geometry from clear daylight photos and choose glass/lighting separately.
- P15 approximate image anchors are already documented in the photo workflow: full frontage crop (28,190)..(1000,674), door crop (535,435)..(700,674), source 1024×751. These are existing chosen crop coordinates, not exact surveyed joinery boundaries. Use visual review before relying on them for a new detailed model.

## Building B03: Syston Dry Cleaners and Laundry

Sources S02/P07/P08/P25. Confidence: high facade/order; oblique upper coverage.

- Attached immediately right of pub; no alley. Taller red-brick upper block differs from the pub/Wreake six-sash module. Large white-framed sash-like windows and broad pale tapered lintels are visible, with smaller windows higher up in wide P07. Do not transplant Pharmacie's small-pane dark windows onto this unit.
- Shop joinery is dark charcoal/slate-grey. Fascia reads 'Syston Dry Cleaners and Laundry' in playful individual multicoloured letters on a grey field, with pale border and projecting/weathered moulding above.
- Left entrance is recessed into a shallow bay with a glazed door, lower panel, upper arched-shaped glazing/detail and visible interior corridor. Orange/terracotta entry floor contrasts with pavement.
- Main display area has projecting framed panes with angled/chamfered ends, resting on a low red-brick base. Vertical posts divide glazing into multiple sections; glazing is not one uninterrupted storefront image.
- Bright coloured window text advertises dry cleaning, delivery/collection, domestic/commercial laundering, wedding dresses, offers and duvets. Exact pricing varies across sources; P07 and S02 do not show identical wording/state.
- A yellow freestanding advertising board stands near the right display corner. It is below waist-height relative to doors and small enough not to become a building-scale object.
- Bright blue slender pole at left boundary (between pub and cleaner) carries pale rectangular plates and an orange-bordered timetable/notice. A small grey protective/utility block sits by its base. Describe as blue street pole/notice; precise service ownership is not proved.
- Exposed brick between fascia/pilasters and upper windows has cables/downpipes. Small weeds grow at shop/pavement seams.
- Rebuild priorities: charcoal fascia with multicolour lettering; recessed left entry; brick window base; different taller white-window upper module; boundary blue pole.

## Building B04: blue nail/spa unit and farther pub-side row

Sources S02/P08. Confidence: medium for immediate unit, low for farther identities.

- Immediately beyond dry cleaners, a narrow frontage has a bright blue sign with pale cursive nail/spa wording. Existing notes call it nail/spa shop; exact trading name should be checked at original resolution before lettering a final sign.
- White-framed storefront and upper white projecting window bays contrast with dark cleaner joinery. A blank pale projecting box-sign is visible at left of blue fascia from this approach.
- Left lower pane/opening is protected by a white metal accordion/diamond lattice security grille. This is surface geometry with real shallow depth, not a white-filled window.
- Right display glazing shows pale beauty-service graphics, with a door/opening around its right area. Image angle prevents reliable full front subdivision; preserve uncertain edges rather than inventing symmetry.
- Brick lower section is exposed beneath the grilled area. Small pavement A-board stands outside the glazing.
- Beyond are other attached red-brick shop units, a green frontage, projecting red signs on a larger brick building and signal poles towards the crossing. Source coverage does not establish every doorway/window count or shop name.
- Proposed placeholder strategy: closed red-brick masses with observed roof-height changes and white/dark frames. Do not duplicate the nail-shop photograph onto each missing unit or add arbitrary street gaps.

## Building B05: Natural Wellbeing at the crossing end

Sources S14/S15/S16/S09/S08. Confidence: high visible front/side; rear extent only partial.

- Two-storey red-brick building with a large front-facing triangular gable. This roof orientation differs from the long parallel-ridge Post Office terrace.
- Gable apex has dark timber-style framing and pale cream vertical infill strips: a central tall strip with shorter strips stepping down towards both roof slopes. Dark diagonal/top rafters outline the triangle. Do not model it as a flat rectangular shop roof.
- Black/dark bargeboards and eaves project beyond walls. Slate/grey roof plane recedes along side. Tall brick chimney with several terracotta pots is visible behind ridge in corner views; rear TV aerial also visible.
- Four white upper window units are arranged in two paired groups. Each pair has a shared pale surround/lintel with stepped/quoin-like blocks at sides, pale sill, central dividing pier and small upper panes above larger lower panes. White curtains/blinds obscure rooms.
- Pale alarm box near front brick centre below gable infill. Small wall cables and a satellite dish appear in corner views; do not confuse the dish's black circular face with a wall window.
- Strong orange fascia spans nearly full frontage. Dark lettering reads 'NATURAL WELLBEING' with a circular leaf/flame-like logo at left. A narrow dark strip below carries smaller orange telephone text.
- Ground floor: pale door towards the left, broad pale-framed display pane to the right. Door has glazed upper area and solid pale lower section/letter plate. Window has pastel leaf/wellbeing graphics and treatment imagery rather than transparent views of a deep shop interior.
- A pale stone/rendered base and side piers frame the shop. Three short grey bollards stand along frontage in S14/S16; they are separate street objects, not part of the window.
- Deep side wall towards the access lane: red brick above a broad cream-rendered lower wall, a small upper window near the front and more upper windows towards the rear, black downpipe and utility cables, satellite dishes on the brick zone.
- Side access doorway lies further back within an arched pale surround; lane extends alongside to smaller rear structures. Small round speed/vehicle warning signs and 'keep clear' type signs appear at the lane mouth. A white truck in S15 occludes the route; S16 gives cleaner lane evidence. Truck is not permanent building geometry.
- Left of front, a neighbouring decorative brick building/church-like gable is partly visible. Identity and whole facade unknown; use matching partial background mass without assigning a business name.
- Critical spatial distinction: lane here separates Natural Wellbeing from Post Office, a second distinct access opening in the reconstructed street.

## Building B06: Post Office

Sources S09/S08/S10. Confidence: high facade and exposed corner.

- Low two-storey red-brick terrace beginning on the far side of Natural Wellbeing's access lane. Side elevation is visible in S08; pitched roof runs along row, with triangular brick gable at the exposed end and projecting dark eaves.
- Facade brick has a shallow decorative dentil/corbel course below eaves. Several brick chimneys rise above the roof; upper white paired windows sit above individual ground units.
- Post Office occupies a comparatively broad red-and-white frontage. Ground wall largely white; saturated red frames, fascia surround and entrance reveal. Sign strip is pale/white with red 'Post Office', circular red logos and 'postoffice.co.uk'.
- Main glazing is large left display, entrance opening right of centre, a smaller red-framed window to its right, and a wall-mounted ATM at the far right ground wall. The entrance is dark/recessed in S09; don't fill it with a flat red panel.
- ATM has pale surround and dark purple/blue lower machine face. Above it, a red panel reads 'Free cash withdrawals'. It is a wall inset, not a standalone cash machine in the road.
- Main left window contains red posters/services text and smaller notices. Pavement A-board with yellow face stands near entry in S08. Hanging flower baskets are visible at fascia/corner positions in S08; leaves/flowers are garnish, not silhouette anchors.
- Red cylindrical/pillar postbox stands between Post Office and Papermoon in S09/S10, with small cap, front slot/notice and dark base. Separate it from ATM and shop fascia.
- Signals obstruct portions of shopfront, but don't belong in facade textures. Place poles as actual props on pavement near crossing. The signal's currently green/red state varies and is not fixed geography.
- Exposed lane-side brick wall and lower adjoining structures are visible to the left. Temporary cages/barriers and warning signs at lane mouth vary between shots; record separately from masonry.

## Building B07: Papermoon

Sources S09/S10/S12. Confidence: high facade.

- Attached next to Post Office under the same low roof/brick upper terrace. A paired white upstairs window sits above shop; gutter and downpipe continue.
- Pale cream sign with thin spaced blue-grey uppercase 'PAPERMOON', a small dot/logo left and smaller 'Gifts · Cards · Home' wording towards right. Dark blue-grey painted outer frame/cornice.
- Main display glass takes most left width. Narrow blue-grey glazed door sits at right with solid lower panel. The window base is dark, with low brick/plinth detail, not a giant ground-floor wall.
- Display has dense small gift items, cards and ornaments; foliage/green garland decor forms a broad inverted arch around the upper display. A small triangular bunting line runs beneath top frame.
- Grey/dark A-frame chalkboard stands outside around centre-right. It may shift; avoid blocking the entire pavement with a fixed giant board.
- Red postbox near left edge belongs to pavement, not repeated in both Post Office and Papermoon textures.
- Thin black cables and compact fixtures sit above fascia. Keep appearance scale small relative to windows.

## Doorway D01 and building B08: HM access and Pasha Barber

Sources S10/S12/S09. Confidence: high visible facade, doorway ownership uncertain.

- Between Papermoon and Pasha is a narrow brick strip containing a pale/white glazed door and rectangular pale sign above. Blue projecting 'HM' mortgage-related sign is visible higher on brick. Full exact lettering/tenant relation needs sharper source verification.
- Do not expand this slim doorway into another shop as wide as Papermoon or a road-sized alley. It is a real part of the terrace's facade rhythm.
- Pasha fascia is black with white uppercase 'PASHA BARBER', small face/head graphics at ends and striped barber-pole decoration around end areas. Black heavy joinery frame and dark cornice.
- Large front glazing has a bold white circular emblem: crossed barber implements within the ring and curved Pasha/Barber/Traditional wording. Ring dominates glass; preserve as decal/texture rather than cutting a circular hole in facade.
- Ground-level strip shows a row of haircut/head thumbnails. Side menu/pricing panel is dark with small pale text. Exact prices illegible at overview scale.
- Narrow doorway/opening sits at the left of main circular display. A tall freestanding barber advertisement board stands near that side in S10/S12; it is separate from window decal.
- Paired white upper windows and shared roof/chimneys remain ordinary terrace elements, not the later white projecting bay type.

## Building B09: Floral Fantasy and doorway D02

Sources S05/S10/S11/S12. Confidence: high facade/upper bay, operating status unknown.

- Pale/white ground shopfront beneath a black/dark fascia with a long cream oval/rounded-end inset. 'Floral Fantasy' appears in flowing dark script, with smaller telephone text towards left.
- Door is towards left, pale frame, glazed upper panels/transom and solid lower portion. Number '8A' visible on outer pale left pier in S05/S10. This visible label can be recorded without assigning other shops panorama addresses.
- Main right window is broad and divided vertically into tall panes. Glass is obscured by dense pale green/grey swirling floral/leaf patterned film, curtains or screening; precise material uncertain. Do not render it as an empty black shop or a second transparent Mini Market.
- Low dark threshold/plinth line, pale outer posts, slightly projecting shop glazing. Old fascia top is worn/dark and not perfectly straight pristine metal.
- Upper storey above this region has a projecting white bay with central broad pane and narrower angled side panes, white transom areas, cream/white cornice and a small grey tiled pyramidal/hipped roof.
- Another flat white upstairs sash sits in the brick between the two bays spanning the Floral/Let's Move region. Thus bay–flat-window–bay rhythm matters more than one upper window copied per shop.
- Narrow bright royal-blue solid door with pale outer surround and small glazed/transom above appears to the right of Floral before Let's Move's main entrance. Treat it as separate access opening within terrace.
- Source filename calls Floral 'shut down'; image establishes obscured glass and existing signage only. Trading status is not needed to model the visible facade accurately.

## Building B10: Let's Move estate agents

Sources S05/S06/S11/S12. Confidence: high facade/order and shared upper bay rhythm.

- Dark navy/blue shopfront with broad fascia. Main 'Let's move' wording pale/white and slanted; smaller 'ESTATE AGENTS' orange/red underneath. Thin orange/red line runs along sign; small phone text at right.
- Slim projecting sign at left bears 'lm' in orange and pale lettering on dark face. It projects roughly perpendicular to facade; don't texture it flat onto front and count it as another shop.
- Entrance recessed at left side of main frontage, dark blue door/glass and pale shallow reveal. Broad display window right of entrance filled with regular property-listing cards in rows/columns, hanging on thin lines rather than giant scattered posters.
- Small narrow access door also appears at the right transition toward Mini Market in S06; doorway ownership uncertain, retain observed opening location.
- White/pale framing and dark low base. Pavement standing estate-agent board is visible near entry. People/mobility scooter in sources are temporary occlusions and should not be included in facade derivatives.
- White upstairs projecting bay occurs above the right portion of this combined low-roof module; small hipped roof stands out against long grey roof slope. Brick side/central sash between bays visible.
- Facade looks broadly comparable to Mini Market but shorter in some views due to perspective. Do not use apparent pixels from a strongly oblique photo as direct width metres.

## Building B11: Syston Mini Market

Sources S06/S11/S12/S03/S04. Confidence: high main elevation; base partly hidden by cars.

- Wide bright red fascia: 'SYSTON' in large yellow uppercase with underline-like bar, 'MINI MARKET' in large white uppercase. Smaller pale line below lists vape/sweets/soft drinks/tobacco; small national flag graphics run across sign's lower right region.
- Colourful display graphics separate ground panes: warm orange drinks/alcohol imagery at left, vivid blue bottles/grocery imagery centre, purple/magenta vape imagery at right. These are window advertisements, not actual three-dimensional oversized bottles behind glass.
- Smaller dark header strips above display panels read OFF LICENCE, COLD DRINKS, GROCERY, VAPES. Ground glazing divided by dark vertical frames; glazed entrance towards right-of-centre between display regions, dark door and inner reveal.
- Upper facade is red brick with **two tall white sash windows**, broad pale tapered lintels and pale sills. Window style larger/simpler than Pharmacie's dark multipane sash.
- A prominent pale/white dentilled cornice runs beneath dark roof eaves across Mini Market and Aston module. Roof ridge/eaves sit higher than Floral/Let's Move region; party-wall chimney/brick upstand marks the change.
- Brick chimney with pale pots rises above roof; a small pale alarm is centred high between upper windows. Black cables/lamp brackets lie above fascia.
- Cars hide portions of bottom display and doorway approaches. Green hatchback lies in foreground disabled bay in S06/S11; never include its whole silhouette in a storefront texture.
- Right boundary toward Aston includes a narrow dark gate/passage/opening with pale top panel between frontage modules. It breaks continuity of ground shop joinery without separating upper terrace into isolated buildings.
- Rebuild priorities: two-sash taller brick module, red/yellow/white sign, three colourful panel regions, actual door, dark narrow neighbouring access, disabled bay outside.

## Building B12: Aston & Co

Sources S03/S04/S06/S11/S13. Confidence: high elevation.

- Narrow unit between Mini Market and Fox. Upper wall is painted pale white/grey brick, distinctly contrasting with Mini Market's red brick; one tall white-framed upper sash window with pale sill.
- Shares taller corniced roof/eaves module with Mini Market, then meets the lower Fox roof immediately to right. A brick chimney/upstand at this transition makes silhouette step obvious.
- Red sign spanning frontage reads 'Aston&Co' in pale/white lettering; smaller 'ESTATE & LETTING AGENTS' underneath.
- Ground display window at left takes most frontage, red frame and multiple property listing cards arranged in a grid. Narrow red door at right with glazed upper panels and solid lower panel. Dark threshold/plinth.
- Small pale alarm box attached to upper wall to right of sash; black wall fixtures/cables near sign. No photo evidence of a second upper window for this narrow unit.
- Street lamp/pole in front appears between Mini Market/Aston region in S03/S04; cars cover low bases. It is not a pilaster separating the buildings.

## Building B13: Fox & Hounds and corner return

Sources S13/S03/S04/S11. Confidence: high front and partial corner geometry.

- Broad low two-storey cream/off-white rendered pub with black plinth. Long shallow-looking grey slate/tile roof along main elevation, noticeably lower than adjoining Aston/Mini Market roof. Roof has slight irregularity/weathering, not a flat cap.
- Upper windows are rectangular multipane pale sage/grey-green frames. Broad frontage has several upper window groups, three clearly visible in S13. Wall is not one huge advertising photograph.
- Main sign is cream with dark border and dark serif 'THE FOX & HOUNDS', an arched/raised central crest and silhouettes of running animals. It is above the entrance towards right-of-centre, not centred over entire building width.
- Separate rectangular cream/dark framed sign at left reads 'FINE FOOD, REAL ALE & WINES'. Both signs are wall-mounted distinct shapes.
- Main doorway has a pale sage/grey surround and dark inset door, projecting traditional hood/cornice and black lanterns near each side. Signs/hood are shallow geometric relief.
- Ground windows: paired panes grouped at left, a smaller window around mid-left, and another paired group to right of entrance. Each has many small rectangular panes and pale sage/grey sill/frame. Preserve varied width groups; no continuous shop display glazing.
- Black framed noticeboard lies to right of entrance; cream/dark wall poster to left advertises pub food/beer garden. Small wall grille visible above ground-window level.
- Right corner is angled/chamfered or rounded in plan rather than a zero-depth flat panel. S13 shows the pub continuing around junction with additional pale wall/window/sign area. Match visible front-to-return angle; exact radius/whole side length unknown.
- Dark plinth wraps the corner. Pavement and double-yellow edge sweep around it. Lamps/downpipes and low bollards are separate props near front.
- Beyond corner, narrow adjoining/distant facades and side street become visible. Their complete layout and identities are unknown; provide depth/sightline closure with coherent background masses.

## Road, pavement and junction: surface-by-surface notes

### Road alignment and width

- S08 gives a corridor view from crossing towards junction; S13 gives a junction view. Road edges change direction and include kerb bulges. Preserve a slight evolving alignment rather than laying every building along two perfectly parallel planes.
- Ordinary grey asphalt is unevenly toned, with darker repair patches and utility covers. White painted markings are worn/off-white, yellow edge lines muted yellow. Colours vary with exposure; do not sample a photograph as an unlit engine colour standard.
- Two-way traffic observed. Exact real carriageway width, grade, crossfall and lane widths are unknown. Establish one coherent estimated scale from building/door references before gameplay widening.
- The pub's existing estimated 7m frontage and game-expanded approximately 12.66m are separate scales. Use a real-proportion reconstruction layer plus an explicit gameplay adjustment; do not claim the widened scene is 1:1.

### Pub-side pavement and kerb — S01/S02/S07/P08/P25

- Pavement is a mix of pale grey/buff rectangular slabs and smaller brown/grey blocks near shops/recesses. Courses run along/against fronts with irregular repairs. Not one pure uniformly grey slab texture everywhere.
- Pavement connects directly to recessed shop tiles without huge steps; continuous walking line follows facade. Wreake and Pharmacie recess surfaces differ from public paving.
- Concrete/stone kerb has a narrow raised edge. Dark rectangular drain grate appears at the road edge near blue pole/dry cleaners in S02. Place it flush in gutter, not as a raised block.
- Double yellow lines follow curb towards crossing in S02/S07/P08, curving where kerb curves. Do not draw a straight line through a drain or across an access mouth without checking the photograph.
- Small weeds/dirt at plinths, pipes, tile joints and boundary-wall base. Use restrained decals/props, not large vegetation barriers at doors.

### Opposite pavement build-out and parking — S05/S06/S11

- Pavement protrudes into carriageway near Floral/Let's Move region, with a curved/chamfered return into parking alignment by Mini Market. White bay markings and double yellows follow different segments around this feature.
- Disabled parking bay visible outside Mini Market region, with white dashed/short corner marks and large 'DISABLED' road lettering. Adjacent parked cars show continued bay alignment towards Aston/Fox.
- Photograph's disabled text orientation follows road/bay, not building fascia. Keep road marking as a surface layer on asphalt.
- Pavement slabs have service covers, gutters and slight edge irregularity. Cars obscure some boundary points; trace visible kerb segments across multiple views instead of inventing a long perfect straight rectangle.
- Parking bays are observed layout; specific green/silver/white cars are temporary. If used as scenery props later, position independently with gameplay collision intentional.

### Crossing — S08/S09/S10/S02

- Signal-controlled pedestrian crossing at Post Office end. Tall grey poles with dark three-lamp traffic heads facing along road; pedestrian pushbutton boxes and near-side pavement fixtures visible.
- White zigzag road markings run along approaches. They are a specific crossing treatment, not random roadside chevrons or the generic evenly spaced centre dashes currently in Blender.
- Reddish/pink tactile paving area near crossing poles contrasts with grey paving. Model as flat tactile surface, not a high red podium.
- Road transverse line/marking visible near crossing in S09. Full crossing footprint and opposite landing are not shown cleanly in one frame; place from combined sources and flag estimated length/positions.
- Traffic signals partly occlude Post Office/Papermoon and pub-side distant row. Do not include them in shopfront derivatives, or reconstructing separate signal props will create duplicates.
- Pole counts should be traced across images before final asset placement; overlapping views can show the same pole repeatedly. Current signal colour is temporary and can be selected for game mood.

### Fox junction and island — S13

- Road/pavement wraps around Fox corner and a side street opens to right in image. Traffic island occupies foreground/right junction area, with pale kerb, small paved top and yellow-faced blue keep-left bollard.
- Blue circular roundabout sign has white rotating arrows. Separate yellow directional board below/near it reads Queniborough Lodge with a black left arrow and lodging symbol. Signpost, direction board and traffic island must not merge into a single giant billboard.
- Several slim grey lighting poles with flat asymmetric rectangular heads stand around corner; visible positions should be established from corner/overlapping views, not evenly spaced by procedural guess.
- Background includes lower buildings, trees and an open junction view. Do not terminate road against a blank wall immediately beside Fox or leave exposed sky/countryside behind a paper-thin pub.
- Exact junction plan, all side-road branches and island dimensions are unknown. This view supports a recognizable corner silhouette/blockout, not a precise roundabout survey.

## Street furniture inventory and placement rules

| Detail | Observed location/sources | Reconstruction rule |
|---|---|---|
| Blue notice/timetable pole | Pub/dry-cleaner boundary, S02/P25/P28 | One object, slim pole; do not duplicate onto both shop textures |
| Grey streetlights, flat dark heads | Both longitudinal views and junction | Match observed sightline positions; IDs across views require triangulation |
| Traffic signals/pushbuttons | Post Office crossing, S08/S09/S10 | Separate props; pole offsets estimated until plan traced |
| Red postbox | Post Office/Papermoon seam, S09/S10 | Independent compact cylinder with cap/slot/base |
| Short grey bollards | Natural Wellbeing frontage, S14/S16; Fox vicinity | Different objects; do not treat as window mullions |
| Shop A-boards | Pub, cleaner, nail/spa, Post Office, Papermoon, barber, estate agent | Movable dressing; leave traversable pavement and doorway approaches |
| Drain grates | Kerb/gutter near pub side and opposite build-out | Flush plane/detail, no accidental raised collider |
| Satellite dishes/aerials | Natural Wellbeing/terrace upper areas | Small geometry or decals with correct orientation |
| Alarm boxes | Pub/Wreake, Mini Market/Aston, Natural Wellbeing | Small wall details; varying shapes, avoid uniform copies everywhere |
| Temporary cages/barriers/cones | Natural Wellbeing/Post Office lane sources | Record as temporary; not evidence of fixed walls/gates |
| Utility cables/downpipes | Most brick facades | Vertical/horizontal shallow detail; keep contiguous across facade modules |
| Cars/people | Many source streets | Occlusions/state, not texture-ready facade information |
| Google markers/arrows/UI | All Street View captures | Exclude from reconstruction geometry/materials |

## Relative scale and tracing anchors

No new world measurements are asserted here. Use these relationships as constraints while tracing:

1. Pharmacie and Wreake share upper-window height, pale sills, dark brick bands and eaves. Match those levels before shop-specific details.
2. Pub shopfront has three upper windows; Wreake three; Mini Market two; Aston one. Natural Wellbeing has two paired groups/four white upper units. These counts are stable visible anchors.
3. Wreake and pub entries recede behind outer display corners. Keep recess depth in proportion to door height using P28/S01; do not derive depth from a single angled screenshot as metres.
4. Floral/Let's Move upper bays project beyond brick face, with sloping side panes and small roof caps. Bay–flat-window–bay rhythm across module must remain visible at street level.
5. Mini Market/Aston eaves and cornice are higher than adjacent low bay terrace and Fox frontage. Do not use existing v12 arbitrary height numbers as photographic evidence.
6. Natural Wellbeing roof gable points towards street; Post Office terrace roof runs along row. Their distinct orientation survives any gameplay scale change.
7. Fox is broad and low compared with narrow Aston. Its sign is local to entry region, not stretched across all frontage.
8. Pub's blue glazing bands sit below eye-level display plaques; door handles/stickers are compact details. Layer large masses → door/window rhythm → fascia → small decals.
9. Photo rectangles must be perspective-corrected within a single facade plane. Roof, angled glass and projecting bays belong to other planes and cannot be rectified together with wall in one homography.
10. Choose one lens/viewpoint and compare render against original image for each anchor. A moving game screenshot cannot prove ratio accuracy unless camera height/FOV and framing are controlled.

## Source hazards: what must never become architecture

- S01 and several root screenshots contain browser/minimap/Google footer content or repeated screenshot bands. Crop to real image content without editing originals.
- S14/S15/S16 have large blank white margins; these are file canvas, not white walls extending beside Natural Wellbeing.
- Shop glazing reflects the opposite row; red 'MINI MARKET' or Aston wording visible reversed on pub/Wreake glass is reflection, not a real sign in the pub.
- Cars mask facade bases, people mask entrances, Google point markers overlay signs. These missing patches cannot be reconstructed perfectly from text; use another source or keep a documented neutral placeholder.
- Signage changes: CAMRA banner vs JB Kitchen board; dry-cleaner prices; pub door open/closed; skeleton/outdoor boards not relevant to street dimensions. Do not combine all photographed states indiscriminately.
- Sunset/night colour, wet/condensed glass and photographic shadows should not become permanent opaque geometry or pre-lit patches without deliberate choice.
- Current BO3 broken-shopfront screenshots show entire source-street portions on individual panels. They are debugging evidence and do not define intended facade width/order.

## Reconstruction sequence and visual acceptance checks

1. Trace two street rows with correct shop/access order. Position crossing end and junction end. Keep uncertain pub-side extension as labelled placeholders.
2. Block actual depth/roof masses and corner returns. Join Wreake/pub/cleaner correctly; reserve alley outside Wreake. Provide rear-facing geometry so side views do not expose paper-thin boards.
3. Shape road, kerbs, pavement build-out, access mouths, parking bay, crossing approach and junction island. Record every estimated metre value separately from these observations.
4. Build facade modules: six dark upper terrace windows; white bay pair; Mini Market/Aston cornice; Fox cream corner; Natural Wellbeing gable; Post Office red/white facade.
5. Add shop recesses, doors, thresholds, plinths and pane divisions. Use separate geometry for angled glazing and overhead signs.
6. Prepare individual sign/window derivatives with source tags/crops. Keep large brick/render/roof faces repeatable; avoid photo-baked duplicate cars/lamps/reflections/UI.
7. Add visible street furniture, then small utilities/weathering. Keep low-priority/distant props simple without sacrificing key silhouettes.
8. Compare renders from S07 (alley/pub attachment), P25 (pub elevation), S06 (Mini Market row), S08 (crossing corridor), S13 (Fox corner), S14/S16 (Natural Wellbeing front/side). Record which image each comparison targets.
9. Check order, window counts, roof steps, sign colour/text, recesses, facade contacts, kerb curvature and projected bay shapes before tiny typography. A fixed photo wall alone cannot satisfy side/corner views.
10. After visual match, document intentional gameplay clearance widening and collision differences. Final BO3 checks must separately prove texture crops, outside spawns, pavement collision, alley rear route and interaction placement.

## Missing evidence to request/capture only when needed

| Missing part | Why it matters | Best next view |
|---|---|---|
| Full pub-side run beyond nail/spa unit | Exact shop order, roof steps and frontage widths | Several near-frontal views with overlap towards crossing |
| Wreake alley rear/end | Real rear connection/gates/width/depth | Looking inward from alley mouth, plus rear view if accessible |
| Pub/Wreake full roof from multiple sides | Hip/end pitch and ridge depth | Oblique wide view from both street directions |
| Entire crossing footprint/opposite pavement | Pole positions, tactile pads, road geometry | Wide view along both approaches and across crossing |
| Junction/island full layout | Corner turn and side-road closures | Wider junction view facing back along High Street |
| One real known dimension | Uniform calibration | Door/frontage measurement or verified scaled survey |
| Occluded lower shopfronts | Avoid baking parked cars | Alternate panorama/time with clean threshold/window bases |

No new live Street View capture was made for this specification. Supplied originals remain untouched. The existing photos are sufficient for a detailed first street reconstruction; the missing items constrain a claim of exact 1:1 geography.
