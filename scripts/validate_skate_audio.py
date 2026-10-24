"""Validate completed private audio, including legitimate multichannel banks."""
from pathlib import Path
import collections,hashlib,json,wave
ROOT=Path(__file__).resolve().parents[1];STAGE=ROOT/'build/pharmacie-skate';AUDIO=STAGE/'assets/private/audio'
manifest=json.loads((AUDIO/'audio_manifest.json').read_text());assert manifest['version']==5
refs=[]
for group in ('ambience','grains','wheels'):
    for item in manifest[group].values():
        refs.append(item['file'])
        if 'grain' in item:refs.append(item['grain'])
        refs.extend(band['file'] for band in item.get('bands',[]))
for samples in manifest['banks'].values():refs.extend(item['file'] for item in samples)
refs.extend(manifest['aems']['projects']);refs.extend(manifest['aems']['banks'].values());refs.extend(manifest['aems']['splice'].values())
if manifest['aems'].get('mixmap'):refs.append(manifest['aems']['mixmap'])
for reference in refs:
    target=(AUDIO/reference).resolve();assert target.is_relative_to(AUDIO.resolve()) and target.is_file(),reference
files=list(AUDIO.rglob('*.wav'));frames=0;silent=0;size=0;channels=collections.Counter()
for path in files:
    with wave.open(str(path),'rb') as clip:
        assert clip.getsampwidth()==2 and 1<=clip.getnchannels()<=6
        assert clip.getframerate()>0 and clip.getnframes()>0
        data=clip.readframes(clip.getnframes());assert len(data)==clip.getnframes()*clip.getnchannels()*2
        frames+=clip.getnframes();silent+=int(not any(data));channels[clip.getnchannels()]+=1
    size+=path.stat().st_size
source_hash=hashlib.sha256(Path('S:/Skate3Recomp-Windows/game/default.xex').read_bytes()).hexdigest()
assert source_hash==json.loads((STAGE/'asset-preparation.json').read_text())['source_xex_sha256']
report={'status':'audio_conversion_and_pcm_validation_pass','manifest_version':5,'source_xex_sha256':source_hash,
        'wav_files':len(files),'verified_local_references':len(refs),'pcm_frames':frames,'silent_clips':silent,
        'wav_bytes':size,'channel_counts':dict(channels),'ambience_beds':len(manifest['ambience']),
        'rolling_grains':len(manifest['grains']),'wheel_streams':len(manifest['wheels']),'effect_banks':len(manifest['banks']),
        'speech_pcm_decoded':False,'private_only':True,'runtime_audio_test':'pending'}
(STAGE/'audio-preparation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
