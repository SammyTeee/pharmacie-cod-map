"""Resume our interrupted pinned audio export, retaining completed PCM clips."""
from pathlib import Path
import hashlib,inspect,json,os,re,shutil,sys,time,wave
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine'))
from tools.asset_pipeline import audio_export as audio
STAGE=ROOT/'build/pharmacie-skate';SOURCE=Path('S:/Skate3Recomp-Windows/game')
OUTPUT=STAGE/'assets/private/audio';WORK=STAGE/'audio-work-v63'
assert OUTPUT.is_dir() and WORK.is_dir() and not (OUTPUT/'audio_manifest.json').exists()
assert hashlib.sha256((STAGE/'vgmstream-r2117.zip').read_bytes()).hexdigest()==audio.VGMSTREAM_SHA
decoder=next((STAGE/'audio-tools-r2117').rglob('vgmstream-cli.exe'))
before=hashlib.sha256((SOURCE/'default.xex').read_bytes()).hexdigest()
os.environ['SKATE_SETUP_SPEECH']='0'
manifest={'version':audio.VERSION,'ambience':{},'grains':{},'wheels':{},'banks':{},'patches':{}}
for stem in audio.AMBIENCE:
    path=OUTPUT/'ambience'/(stem+'.wav');manifest['ambience'][stem]={'file':f'ambience/{stem}.wav',**audio._wav_info(path)}
for path in sorted((OUTPUT/'grains').glob('*.grain')):
    stem=path.stem;info=audio.grain(path.read_bytes())
    bands=[{'file':f'grains/{stem}/{i}.wav',**audio._wav_info(OUTPUT/'grains'/stem/f'{i}.wav')} for i in range(audio.GRAIN_BANDS)]
    manifest['grains'][stem]={'file':f'grains/{stem}.wav','grain':f'grains/{stem}.grain','duration':info.duration,
                             'bands':bands,**audio._wav_info(path.with_suffix('.wav'))}
for path in sorted((OUTPUT/'wheels').glob('*.wav')):
    manifest['wheels'][path.stem]={'file':f'wheels/{path.name}',**audio._wav_info(path)}
assert manifest['grains'] and manifest['wheels']
original_decode=audio._decode
def cached_decode(vgmstream,directory,names,log):
    assert shutil.disk_usage(STAGE).free>300_000_000,'Resume stopped to preserve disk headroom'
    missing=[]
    for name in names:
        cached=OUTPUT/'banks'/directory.name/(Path(name).stem+'.wav')
        if cached.exists():shutil.copyfile(cached,directory/(name+'.wav'))
        else:missing.append(name)
    if missing:original_decode(vgmstream,directory,missing,log)
audio._decode=cached_decode
def cached_collections(game_root,work):
    from tools.asset_pipeline.vlt import convert
    database=work/'database/data/db'
    names=(ROOT/'build/skate-3-rust-engine/tools/asset_pipeline/names.txt').read_text(encoding='utf-8').splitlines()
    converted=convert(database/'skaterschema',database/'skatercollections',names)
    text=(database/'skatercollections_summaryreport.txt').read_text(encoding='latin-1')
    return converted['collections'],re.findall(r'\.class/([A-Za-z0-9_]+)\.xml',text)
audio._collections=cached_collections
# Reuse the pinned exporter's complete bank/AEMS/speech-index stage verbatim.
# Only allow existing generated work folders and inject the completed PCM manifest.
source=inspect.getsource(audio.convert);tail=source[source.index("    report('Decoding sound effect banks')"):]
tail=tail.replace('folder.mkdir(parents=True)','folder.mkdir(parents=True, exist_ok=True)')
function="def resume(game_root,private,work,vgmstream,report,log,manifest):\n    audio_root=game_root/'data/audio'\n    output=private/'audio'\n"+tail
namespace=dict(audio.__dict__);exec(compile(function,'<pinned audio bank resume>','exec'),namespace)
def report(message):print('AUDIO_RESUME',message,flush=True)
started=time.monotonic()
with (STAGE/'audio-preparation-resume.log').open('wb') as log:
    manifest=namespace['resume'](SOURCE,STAGE/'assets/private',WORK,decoder,report,log,manifest)
assert hashlib.sha256((SOURCE/'default.xex').read_bytes()).hexdigest()==before
files=list(OUTPUT.rglob('*.wav'));frames=0;silent=0;size=0
for path in files:
    with wave.open(str(path),'rb') as clip:
        assert clip.getsampwidth()==2 and 1<=clip.getnchannels()<=6
        data=clip.readframes(clip.getnframes());frames+=clip.getnframes()
        silent+=int(not any(data))
    size+=path.stat().st_size
result={'status':'audio_conversion_and_pcm_validation_pass','source_xex_sha256':before,
    'decoder_archive_sha256':audio.VGMSTREAM_SHA,'manifest_version':manifest['version'],
    'wav_files':len(files),'pcm_frames':frames,'silent_clips':silent,'wav_bytes':size,
    'ambience_beds':len(manifest['ambience']),'rolling_grains':len(manifest['grains']),
    'wheel_streams':len(manifest['wheels']),'effect_banks':len(manifest['banks']),
    'resume_seconds':time.monotonic()-started,'speech_pcm_decoded':False,
    'runtime_audio_test':'pending; user-controlled process not restarted','private_only':True}
(STAGE/'audio-preparation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
