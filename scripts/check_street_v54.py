from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
f=ROOT/'scripts/check_extension_v41.py';s=f.read_text()
s=s.replace("'pharmacie-station-holmdale-v45.blend')","'pharmacie-station-holmdale-v45.blend','pharmacie-surveyed-streets-v54.blend')")
s=s.replace("('v44','v45')","('v44','v45','v54')").replace("output_version=='v45'","output_version in ('v45','v54')")
s=s.replace("keys=['main','holmdale','station_access','station_link']","route['holmdale']=json.loads((ROOT/'recon/v53/holmdale-alignment.json').read_text())['holmdale_world']\nroute['barkby']=json.loads((ROOT/'recon/v54/prepared-street.json').read_text())['barkby_world']\nkeys=['main','holmdale','station_access','station_link','barkby']")
s=s.replace("'station_link':1.4","'station_link':1.4,'barkby':3.5")
s=s.replace('(4,-11.5,0),(4,-1.3,0)','(3.9,-11.5,0),(1.5,-3,0),(3.26,-1.69,0)').replace('(12,-11.5,0),(12,-1.1,0)','(4,-5,0),(9.5,-5,0)').replace('(3,-3,0),(13,-3,0)','(3,-9,0),(8.5,-9,0)')
s=s.replace('for off in (0,half+1.2,-half-1.2):',"for off in ((0,.2,-.2) if key=='house_approach' else (0,half+1.2,-half-1.2)):")
ns={'__file__':str(f)};exec(compile(s,str(f),'exec'),ns);result=ns['result']
