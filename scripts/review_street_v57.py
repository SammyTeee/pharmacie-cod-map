from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'scripts/review_street_v56.py';s=p.read_text().replace('recon/v56','recon/v57')
ns={'__file__':str(p)};exec(compile(s,str(p),'exec'),ns);result=ns['result']
