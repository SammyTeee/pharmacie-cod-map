"""Prepare the pinned engine's audio from the existing owned dump; never run it."""
from pathlib import Path
import hashlib,json,os,shutil,sys,time,wave,zipfile
ROOT=Path(__file__).resolve().parents[1];ENGINE=ROOT/'build/skate-3-rust-engine'
sys.path.insert(0,str(ENGINE))
from tools.asset_pipeline import audio_export as audio
SOURCE=Path('S:/Skate3Recomp-Windows/game');STAGE=ROOT/'build/pharmacie-skate'
PRIVATE=STAGE/'assets/private';WORK=STAGE/'audio-work-v63';TOOLS=STAGE/'audio-tools-r2117'
ARCHIVE=STAGE/'vgmstream-r2117.zip'
assert not (PRIVATE/'audio').exists(),'Existing audio is preserved; inspect it before retrying'
assert not WORK.exists(),'Use a fresh conversion workspace'
assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()==audio.VGMSTREAM_SHA,'Decoder checksum mismatch'
before=hashlib.sha256((SOURCE/'default.xex').read_bytes()).hexdigest()
if not TOOLS.exists():
    with zipfile.ZipFile(ARCHIVE) as archive:
        for member in archive.infolist():
            assert (TOOLS/member.filename).resolve().is_relative_to(TOOLS.resolve())
        archive.extractall(TOOLS)
decoder=next(TOOLS.rglob('vgmstream-cli.exe'))
assert shutil.disk_usage(STAGE).free>1_300_000_000,'Insufficient audio conversion headroom'
os.environ['SKATE_SETUP_SPEECH']='0' # Original dialogue is not needed for our street session.
original_decode=audio._decode
def guarded_decode(*args,**kwargs):
    assert shutil.disk_usage(STAGE).free>400_000_000,'Audio conversion stopped to preserve disk headroom'
    return original_decode(*args,**kwargs)
audio._decode=guarded_decode
def report(message):print('AUDIO_PREP',message,flush=True)
start=time.monotonic()
with (STAGE/'audio-preparation.log').open('wb') as log:
    manifest=audio.convert(SOURCE,PRIVATE,WORK,decoder,report,log)
assert hashlib.sha256((SOURCE/'default.xex').read_bytes()).hexdigest()==before
files=list((PRIVATE/'audio').rglob('*.wav'));frames=0;silent=0;size=0
for path in files:
    with wave.open(str(path),'rb') as clip:
        assert clip.getsampwidth()==2 and 1<=clip.getnchannels()<=6
        data=clip.readframes(clip.getnframes());frames+=clip.getnframes()
        if not any(data):silent+=1
    size+=path.stat().st_size
result={'status':'audio_conversion_and_pcm_validation_pass','source_xex_sha256':before,
    'decoder_archive_sha256':audio.VGMSTREAM_SHA,'manifest_version':manifest['version'],
    'wav_files':len(files),'pcm_frames':frames,'silent_clips':silent,'wav_bytes':size,
    'seconds':time.monotonic()-start,'speech_pcm_decoded':False,
    'runtime_audio_test':'pending; current user-controlled process was not restarted',
    'private_only':True}
(STAGE/'audio-preparation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
