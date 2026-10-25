"""Record a source-matched, freshly lit and cleanly relinked core package.

This accepts build evidence for a private runtime trial, not gameplay quality.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'build/bo3-core'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument('--tools-root',type=Path,required=True)
parser.add_argument('--compile-log',type=Path,default=OUT/'build.log')
args = parser.parse_args()
tools_root = args.tools_root
result = json.loads((OUT/'relink-result.json').read_text())
assert result['exitCode'] == 0, 'No successful exact-process relink'
log = (OUT/'relink.stdout.log').read_text(errors='replace')+(OUT/'relink.stderr.log').read_text(errors='replace')
assert not re.search(r'ERROR:|ASSERTBEGIN|bad static model|Could not load mesh',log,re.I)
assert re.search(r'Linking "en_zm_pharmacie_core65".*done:',log)
compile_log = args.compile_log.read_text(errors='replace')
assert 'leaked' not in compile_log.lower() and 'ASSERTBEGIN' not in compile_log and 'ERROR:' not in compile_log
local_map = ROOT/'map_source/zm/zm_pharmacie_core65.map'
staged_map = tools_root/'map_source/zm/zm_pharmacie_core65.map'
assert sha(local_map)==sha(staged_map), 'Current source differs from compiled source'
route_checks = json.loads((OUT/'route-clearance.json').read_text())
floor_checks = json.loads((OUT/'visual-floor-check.json').read_text())
ground_checks = json.loads((OUT/'ground-repair.json').read_text())
for checks_for_map in (route_checks,floor_checks):
    assert checks_for_map['map_sha256']==sha(local_map), 'Stale floor/route check'
assert route_checks['failure_count']==0, 'Blocked/unsupported open route'
assert floor_checks['missing_count']==floor_checks['height_mismatch_count']==0, 'Visual floor lacks matching collision'
assert ground_checks['missing_count']==0, 'Missing safety foundation support'
project_source = ROOT/'usermaps/zm_pharmacie_core65'
script_hashes = {}
for source in sorted((project_source/'scripts').rglob('*')):
    if source.is_file():
        relative = source.relative_to(project_source)
        assert sha(source)==sha(tools_root/'usermaps/zm_pharmacie_core65'/relative), 'Staged script differs: '+str(relative)
        script_hashes[str(relative)] = sha(source)
raw = tools_root/'share/raw/maps/zm'
for suffix in ('.d3dbsp','.led','_navmesh.hkt'):
    p = raw/('zm_pharmacie_core65'+suffix)
    assert p.is_file() and p.stat().st_size > 0
    assert p.stat().st_mtime >= local_map.stat().st_mtime, 'Stale '+str(p)
models = json.loads((OUT/'model-report.json').read_text())
checks = json.loads((OUT/'source-checks.json').read_text())
assert checks['triangles']==models['triangles'] and checks['models']==len(models['models'])
package = tools_root/'usermaps/zm_pharmacie_core65/zone'
files = [{'path':str(p.relative_to(package)), 'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(package.rglob('*')) if p.is_file()]
assert {'zm_pharmacie_core65.ff','en_zm_pharmacie_core65.ff'} <= {f['path'] for f in files}
assert any(f['path'].lower().startswith('snd') for f in files), 'Missing nested sound output'
record = {'stage':'Compiled candidate for private runtime trial', 'acceptedUtc':datetime.now(timezone.utc).isoformat(),
          'map_sha256':sha(local_map),'source_blend_sha256':models['source_sha256'], 'models':len(models['models']),
          'script_sha256':script_hashes,'compile_log_sha256':sha(args.compile_log),
          'floor_source_checks':{'route_samples':route_checks['samples'],'visible_floor_samples':floor_checks['samples'],'ground_samples':ground_checks['samples']},
          'exported_triangles':models['triangles'], 'native_photo_materials':len(checks['native_photo_pixel_checks']),
          'linker_exit_code':0,'packageFiles':files,'lighting_bytes':(raw/'zm_pharmacie_core65.led').stat().st_size,
          'native_warning_limit':'First conversion reports 15 pre-bone and 48 non-planar/stretch warnings on terrain backing/street fittings; final cached relink exits 0. Export count is not a claim that BO3 retained every degenerate triangle.',
          'pending':['Inspected actual runtime capture','Door/weapon purchases','Zombie pursuit and round completion','Co-op']}
(OUT/'build-acceptance.json').write_text(json.dumps(record,indent=2)+'\n')
print('CORE_BUILD_CANDIDATE_ACCEPTED',len(files),'files;',sum(f['bytes'] for f in files),'bytes; linker exit 0')
