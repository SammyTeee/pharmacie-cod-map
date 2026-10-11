from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'scripts/check_street_v54.py'
s=p.read_text().replace('pharmacie-surveyed-streets-v54.blend','pharmacie-surveyed-route-v56.blend').replace("'v54'","'v56'")
s=s.replace("ns={'__file__':str(f)};", "s=s.replace(\"route['holmdale_turning_end']=[list(end-t*.5),list(end+t*3)]\", \"trace=json.loads((ROOT/'recon/v56/prepared-final.json').read_text())['trace_world']; centre=Vector([sum(p[i] for p in trace[:-1])/(len(trace)-1) for i in (0,1)]); route['holmdale_turning_end']=[list(end),list(centre)]\")\nns={'__file__':str(f)};")
ns={'__file__':str(p)};exec(compile(s,str(p),'exec'),ns);result=ns['result']
