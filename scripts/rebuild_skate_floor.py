"""Rebuild the v60 starter-street collision repair without replacing a live map.

Input is the output of light_skate_demo.py. A fresh staging directory is required.
The native probe must be built from scripts/skate_map_probe.rs first.
"""
from pathlib import Path
import argparse,collections,hashlib,json,struct,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'build/skate-3-rust-engine/tools/vendor/university/tools/blender_owned_map'))
from analyze_skate import Reader

def package(path):
    blob=path.read_bytes();r=Reader(blob)
    assert r.take(8,'magic')==b'SKATE15\0'
    r.skip(4,'endian');r.string('map');r.skip(196,'environment')
    countoff=r.offset;counts=struct.unpack('<9I',r.take(36,'counts'))
    length=r.u32('material size');mr=Reader(r.stored(length,'materials'));skate=set()
    for i in range(counts[0]):
        name=mr.string('material')
        if 'Skate v60 |' in name:skate.add(i+1)
        mr.skip(80,'fields');defined=mr.u32('definition')
        if defined:
            mr.skip(16,'identity');mr.string('shader');mr.skip(8,'family flags')
            for _ in range(mr.u32('bindings')):mr.string('role');mr.skip(16,'binding')
            for _ in range(mr.u32('parameters')):
                mr.string('parameter')
                for _ in range(mr.u32('values')):mr.string('value')
            mr.string('source')
    def skip_storage():r.u32('method');r.skip(r.u32('size'),'payload')
    for _ in range(counts[1]):r.string('texture');r.skip(12,'dimensions');skip_storage()
    skip_storage();skip_storage()
    prefix=bytearray(blob[:r.offset]);struct.pack_into('<I',prefix,countoff+16,0)
    collision=r.stored(counts[4]*48,'collision');suffix=blob[r.offset:]
    features=collections.Counter()
    for start in range(0,len(collision),48):
        tri=collision[start:start+48]
        if struct.unpack_from('<I',tri,40)[0] in skate:
            # Contact tag is deliberately corrected; all other feature bytes stay.
            features[tri[:36]+tri[40:]]+=1
    assert features,'Expected authored v60 ramp/rail materials'
    return bytes(prefix),suffix,features

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT/'build/pharmacie-skate/pharmacie-street-session-demo.skate')
    parser.add_argument('--staging',type=Path,required=True)
    args=parser.parse_args();source=args.source.resolve();stage=args.staging.resolve()
    assert stage.is_relative_to(ROOT/'build'),'Staging must be under project build/'
    assert not stage.exists(),'Use a fresh staging directory; existing packages are preserved'
    probe=ROOT/'build/skate-3-rust-engine/target/debug/examples/pharmacie_map_probe.exe'
    contact_probe=probe.with_name('pharmacie_contact_probe.exe')
    assert probe.is_file(),'Build the native probe before preparing a candidate'
    assert contact_probe.is_file(),'Build scripts/skate_contact_probe.rs as pharmacie_contact_probe first'
    before=package(source);stage.mkdir(parents=True)
    tagged=stage/'contact-corrected.skate';candidate=stage/'street-session.skate'
    for script,src,out,report in (
        ('fix_skate_surface_tags_v61.py',source,tagged,'surface-tags.json'),
        ('flatten_skate_street_v62.py',tagged,candidate,'flat-floor.json'),
    ):
        subprocess.run([sys.executable,str(ROOT/'scripts'/script),'--source',str(src),'--output',str(out),'--report',str(stage/report)],check=True)
    after=package(candidate)
    assert before[0]==after[0],'Visual/environment/material/texture data changed'
    assert before[1]==after[1],'Rail, light, route or extension records changed'
    assert before[2]==after[2],'Authored skate feature collision changed'
    result=subprocess.run([str(probe),str(candidate)],check=True,capture_output=True,text=True,encoding='utf-8')
    native=json.loads(result.stdout);(stage/'native-probe.json').write_text(json.dumps(native,indent=2))
    contact_result=subprocess.run([str(contact_probe),str(candidate)],check=True,capture_output=True,text=True,encoding='utf-8')
    contact=json.loads(contact_result.stdout);(stage/'feature-contact-stress.json').write_text(json.dumps(contact,indent=2))
    report={'candidate':str(candidate.relative_to(ROOT)),'sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'presentation_bytes_unchanged':True,'rail_and_extension_bytes_unchanged':True,
            'authored_skate_collision_geometry_unchanged':True,'preserved_skate_feature_triangles':sum(before[2].values()),
            'native_collision_and_contact_vote_pass':True,'live_map_replaced':False,
            'authored_feature_wheel_contact_solver_cases':contact['wheel_contact_cases'],
            'limits':'Static candidate verification; runtime capture and human riding retest remain separate.'}
    (stage/'candidate-validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
