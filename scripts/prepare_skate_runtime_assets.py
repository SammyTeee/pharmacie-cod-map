"""Prepare runtime inputs from Sam's existing local dump, not retail maps."""
from pathlib import Path
import json,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];ENGINE=ROOT/'build/skate-3-rust-engine';sys.path.insert(0,str(ENGINE))
from tools.asset_pipeline import asset_exports as exports
from tools.asset_pipeline.render_parameters import convert as parameters
SOURCE=Path('S:/Skate3Recomp-Windows/game');STAGE=ROOT/'build/pharmacie-skate';WORK=STAGE/'asset-work';WORK.mkdir(parents=True,exist_ok=True)
for p in ('assets/private/stock','assets/private/default_skater'):(STAGE/p).mkdir(parents=True,exist_ok=True)
assert (SOURCE/'default.xex').is_file()
hash_before=hashlib.sha256((SOURCE/'default.xex').read_bytes()).hexdigest()
report_path=STAGE/'asset-preparation.json';state=json.loads(report_path.read_text()) if report_path.exists() else {'source':str(SOURCE),'source_xex_sha256':hash_before,'steps':{}}
assert state['source_xex_sha256']==hash_before
def report(message):print('ASSET_PREP',message,flush=True)
with (STAGE/'asset-conversion-details.log').open('a',encoding='utf-8') as log:
 converted=None
 for name,fn in [('core',exports.core),('character',exports.character),('hud',exports.hud)]:
  if state['steps'].get(name,{}).get('status')=='complete':
   if name=='core':converted=json.loads((STAGE/'assets/private/stock/skater-collections.json').read_text())
   continue
  started=time.monotonic();result=fn(SOURCE,STAGE,WORK,report,log,converted)
  if name=='core':converted=result
  state['steps'][name]={'status':'complete','seconds':time.monotonic()-started};report_path.write_text(json.dumps(state,indent=2))
 if 'render_parameters' not in state['steps']:
  count=parameters(STAGE/'assets',converted);state['steps']['render_parameters']={'status':'complete','groups':count};report_path.write_text(json.dumps(state,indent=2))
assert hashlib.sha256((SOURCE/'default.xex').read_bytes()).hexdigest()==hash_before
state['status']='core_character_hud_ready_for_runtime_validation';state['limits']='Own map used; no disc-world map conversion, original game execution, audio extraction or customiser roster preparation. Full skating runtime remains to be checked.'
report_path.write_text(json.dumps(state,indent=2));report('LOCAL_SKATING_INPUTS_PREPARED')
