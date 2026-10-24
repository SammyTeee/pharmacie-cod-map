"""Record the inspected house start separately from earlier street captures."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'recon/skate-v60'
capture=OUT/'runtime-holmdale-v64.png';assert Image.open(capture).size==(1280,720)
path=ROOT/'build/skate-runtime-demo.log';raw=path.read_bytes()
log=raw.decode('utf-16' if raw[:2] in (b'\xff\xfe',b'\xfe\xff') else 'utf-8',errors='replace')
flat=re.sub(r'\s+',' ',log)
assert 'GAME_VERIFY_OK' in log and 'physics_failed:true' not in log
assert 'Game audio: 22 ambience beds, 14 rolling grains, 244 sample banks' in flat
report=json.loads((OUT/'holmdale-rebase-v64.json').read_text())
report.update(runtime_validation='Sound-enabled asset check and GAME_VERIFY_OK pass; house/start capture visually inspected',
              capture=capture.name,capture_sha256=hashlib.sha256(capture.read_bytes()).hexdigest(),
              riding_verification='Human trial in progress; landings/grinds/whole-route travel not yet established')
(OUT/'holmdale-rebase-v64.json').write_text(json.dumps(report,indent=2))
page=OUT/'index.html';text=page.read_text()
section='''<section id="holmdale-runtime"><h2>Start at number 29 Holmdale Road</h2><a href="runtime-holmdale-v64.png"><img src="runtime-holmdale-v64.png" alt="Actual skating runtime in front of number 29, showing the approved porch and garage"></a><p>A supported start on the approach to number 29. The entire exported world is translated together so this start is near the engine origin. Blender placement stays unchanged. Sound-enabled startup now loads rolling, wheel, impact, grind and footstep systems. Full-board landings, grinds and travel across the whole route still need the human trial.</p><p><a href="holmdale-rebase-v64.json">Start verification and limits</a> · <a href="holmdale-native-probe-v64.json">Native geometry checks</a> · <a href="holmdale-contact-probe-v64.json">Feature contact stress check</a></p></section>'''
if 'id="holmdale-runtime"' in text:text=re.sub(r'<section id="holmdale-runtime">.*?</section>',lambda _:section,text,count=1,flags=re.S)
else:text=text.replace('<section id="runtime">',section+'<section id="runtime">',1)
text=text.replace('This first prototype is silent.','This earlier capture predates the private audio preparation; the Holmdale start above has sound enabled.')
page.write_text(text,encoding='utf-8');print('HOLMDALE_RUNTIME_REVIEW_UPDATED')
