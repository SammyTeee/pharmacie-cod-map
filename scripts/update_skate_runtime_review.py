"""Add verified runtime evidence to the local Blender design review."""
from pathlib import Path
import json,hashlib,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'recon/skate-v60'
capture=OUT/'runtime-floor-v62.png';assert Image.open(capture).size==(1280,720)
log=(ROOT/'build/skate-runtime-demo.log').read_text(encoding='utf-16' if (ROOT/'build/skate-runtime-demo.log').read_bytes()[:2] in (b'\xff\xfe',b'\xfe\xff') else 'utf-8',errors='replace')
assert 'GAME_VERIFY_OK' in log and 'physics_failed:false' in log
input_text=capture.with_suffix('.input.txt').read_text();ready='Status: [Ready,' in input_text
def integer(label):return int(re.search(r'^'+re.escape(label)+r': (\d+)',input_text,re.M).group(1))
assert 'physical:PhysicsGround' in log and 'physics_failed:true' not in log
repair=json.loads((ROOT/'build/pharmacie-skate/repair-contact-repro-v62/candidate-validation.json').read_text())
report={'capture':capture.name,'capture_sha256':hashlib.sha256(capture.read_bytes()).hexdigest(),'actual_runtime':True,'automatic_capture_pass':True,'ground_state_observed':True,'resting_physics_ticks':integer('Physics ticks'),'resting_contacts':integer('Contacts'),'native_animation_clips_available':integer('Native OnBoard/OffBoard clips available'),'controller_slot_1_ready_at_final_capture':ready,'input_driving_by_agent':False,'collision_rebuild_proof':repair,'riding_ollie_landing_grind_verification':'pending human controller trial','limits':['Startup capture is not a broad gameplay or performance verdict.','Upstream core has one known failing group-8 impact test.','No runtime audio extracted.','Material/lighting adaptation remains approximate.']}
(OUT/'runtime-validation.json').write_text(json.dumps(report,indent=2))
page=OUT/'index.html';text=page.read_text();section='''<section id="runtime"><h2>Repaired street — actual runtime</h2><a href="runtime-floor-v62.png"><img src="runtime-floor-v62.png" alt="The skater standing on the repaired Syston street inside the standalone Rust prototype"></a><p>v62: a continuous level riding surface replaces overlapping starter-road collision. Contact labels are corrected to address the ramp crash. The rebuilt package preserves all visual data, four grind paths and 704 authored skate-feature collision triangles. Native collision checks and runtime startup pass; ridden ramps, landings and grinds still need Sam's controller trial. Controller slot 1 was connected at capture. This first prototype is silent.</p><p><a href="flat-floor-v62.json">Floor measurements</a> · <a href="flat-floor-native-probe-v62.json">Native collision checks</a> · <a href="runtime-validation.json">Runtime verification and limits</a></p></section>'''
if 'id="runtime"' in text:text=re.sub(r'<section id="runtime">.*?</section>',lambda _:section,text,count=1,flags=re.S)
if 'id="runtime"' not in text:text=text.replace('<section><h2>Skate variant</h2>',section+'<section><h2>Skate variant — Blender design</h2>')
text=text.replace('Design preview only. These are Blender material renders and a labelled still reel, not captured gameplay. Runtime skating, tricks and grind behaviour are pending verification.','The film and design stills are Blender previews. A real runtime startup capture appears below. Riding, tricks and grind behaviour remain pending verification.')
page.write_text(text,encoding='utf-8');print('RUNTIME_REVIEW_UPDATED',ready)
