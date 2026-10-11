from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'scripts/check_street_v56.py'
s=p.read_text().replace('pharmacie-surveyed-route-v56.blend','pharmacie-surveyed-route-v57.blend').replace('"\'v56\'"','"\'v57\'"')
ns={'__file__':str(p)};exec(compile(s,str(p),'exec'),ns);result=ns['result']
