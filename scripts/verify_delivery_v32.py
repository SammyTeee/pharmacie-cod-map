"""Verify saved checkpoints and local gallery/media before the mapping push."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links.extend(v for k, v in attrs if k in ('src', 'href') and v)

report = {'engine_verified': False, 'galleries': {}, 'videos': {}, 'checkpoints': {}}
sources = json.loads((ROOT / 'docs/reconstruction-sources.json').read_text())['sources']
for source in sources:
    assert hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() == source['sha256'], source['path']
report['original_reference_hashes_unchanged'] = len(sources)
for version in ('v30', 'v31', 'v32'):
    folder = ROOT / 'recon' / version
    parser = Links()
    parser.feed((folder / 'index.html').read_text(encoding='utf-8'))
    local = [link.split('#')[0] for link in parser.links
             if not link.startswith(('https:', 'http:', '#'))]
    missing = [link for link in local if not (folder / link).is_file()]
    assert not missing, (version, missing)
    report['galleries'][version] = {'local_links': len(local), 'missing': missing}
    validation = json.loads((folder / 'validation.json').read_text())
    assert validation.get('source_photos_unchanged', validation.get('original_reference_hashes_unchanged')) == 44
    assert not validation.get('failures', [])
    assert not validation.get('route_failures', [])
    changes = json.loads((folder / 'changes.json').read_text())
    parent = ROOT / 'assets/blender' / Path(changes['source']).name
    assert hashlib.sha256(parent.read_bytes()).hexdigest() == changes['source_sha256']
    checkpoint = ROOT / 'assets/blender' / Path(changes['output']).name
    report['checkpoints'][version] = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    for video in folder.glob('*.webm'):
        probe = json.loads(subprocess.check_output([
            'C:/ffmpeg/ffprobe.exe', '-v', 'error', '-show_format', '-show_streams',
            '-of', 'json', str(video)]))
        stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        assert (stream['width'], stream['height'], stream['r_frame_rate']) == (1280, 720, '24/1')
        expected = 28 if video.name == 'general-flythrough.webm' else (20 if version == 'v30' else 26)
        duration = float(probe['format']['duration'])
        assert abs(duration - expected) < .1, (video, duration)
        report['videos'][video.relative_to(ROOT).as_posix()] = {
            'duration_seconds': duration, 'bytes': video.stat().st_size,
            'sha256': hashlib.sha256(video.read_bytes()).hexdigest()}
(ROOT / 'recon/v32/delivery-validation.json').write_text(json.dumps(report, indent=2))
print('DELIVERY_CHECKS_PASS', len(report['galleries']), len(report['videos']))
