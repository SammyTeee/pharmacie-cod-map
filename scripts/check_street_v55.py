from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'scripts/check_street_v54.py'
s=p.read_text().replace('pharmacie-surveyed-streets-v54.blend','pharmacie-route-working-v55.blend').replace("'v54'","'v55'")
ns={'__file__':str(p)};exec(compile(s,str(p),'exec'),ns);result=ns['result']
