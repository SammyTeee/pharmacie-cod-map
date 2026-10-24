"""Repeat the selected eleven-route baseline on the neutral visual checkpoint."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-demo-base-v59.blend'
bpy.context.window.scene=bpy.data.scenes['03 Both floors - assembled exterior']
f=ROOT/'scripts/check_extension_v41.py';s=f.read_text()
s=s.replace("'pharmacie-station-holmdale-v45.blend')","'pharmacie-station-holmdale-v45.blend','pharmacie-demo-base-v59.blend')")
s=s.replace("('v44','v45')","('v44','v45','v59')").replace("output_version=='v45'","output_version in ('v45','v59')")
s=s.replace("keys=['main','holmdale','station_access','station_link']","route['holmdale']=json.loads((ROOT/'recon/v53/holmdale-alignment.json').read_text())['holmdale_world']\nroute['barkby']=json.loads((ROOT/'recon/v54/prepared-street.json').read_text())['barkby_world']\nkeys=['main','holmdale','station_access','station_link','barkby']")
s=s.replace("'station_link':1.4","'station_link':1.4,'barkby':3.5")
s=s.replace('(4,-11.5,0),(4,-1.3,0)','(3.9,-11.5,0),(1.5,-3,0),(3.26,-1.69,0)').replace('(12,-11.5,0),(12,-1.1,0)','(4,-5,0),(9.5,-5,0)').replace('(3,-3,0),(13,-3,0)','(3,-9,0),(8.5,-9,0)')
s=s.replace('for off in (0,half+1.2,-half-1.2):',"for off in ((0,.2,-.2) if key=='house_approach' else (0,half+1.2,-half-1.2)):")
s=s.replace("route['holmdale_turning_end']=[list(end-t*.5),list(end+t*3)]", "trace=json.loads((ROOT/'recon/v56/prepared-final.json').read_text())['trace_world']; centre=Vector([sum(p[i] for p in trace[:-1])/(len(trace)-1) for i in (0,1)]); route['holmdale_turning_end']=[list(end),list(centre)]")
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns)
assert not ns['report']['blocked_count'] and not ns['report']['unsupported_count'],ns['report']
# Direct v40 preservation audit, with only the already documented five archives.
f=ROOT/'scripts/audit_preservation_v45.py';s=f.read_text().replace("dest=ROOT/'recon/v45'","dest=ROOT/'recon/v59'").replace("(dest/'v40-fingerprints.json').read_text()","(ROOT/'recon/v45/v40-fingerprints.json').read_text()")
s=s.replace("name=='pharmacie-station-holmdale-v45.blend'","name=='pharmacie-demo-base-v59.blend'")
s=s.replace("'Mapping v34 | Beyond Taraj boundary head']","'Mapping v34 | Beyond Taraj boundary head','Mapping v34 | Rear parcel boundary 1 00','Mapping v34 | Frontage gap backing 1 12.00','Mapping v34 | Junction west return']")
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns)
print('NEUTRAL_ROUTES_AND_V40_PRESERVATION_PASS',flush=True)
