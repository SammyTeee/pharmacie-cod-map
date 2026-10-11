from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'scripts/audit_preservation_v45.py';s=p.read_text()
s=s.replace("dest=ROOT/'recon/v45'","dest=ROOT/'recon/v54'").replace("(dest/'v40-fingerprints.json').read_text()","(ROOT/'recon/v45/v40-fingerprints.json').read_text()")
s=s.replace("name=='pharmacie-station-holmdale-v45.blend'","name=='pharmacie-surveyed-streets-v54.blend'")
s=s.replace("'Mapping v34 | Beyond Taraj boundary head']","'Mapping v34 | Beyond Taraj boundary head','Mapping v34 | Rear parcel boundary 1 00']")
ns={'__file__':str(p)};exec(compile(s,str(p),'exec'),ns);result=ns['result']
