from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'scripts/audit_street_v55.py'
s=p.read_text().replace('pharmacie-route-working-v55.blend','pharmacie-surveyed-route-v56.blend').replace("recon/v55","recon/v56")
ns={'__file__':str(p)};exec(compile(s,str(p),'exec'),ns);result=ns['result']
