from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'scripts/preview_street_fronts.py').read_text().replace('street-photo-fronts-v11.png','street-photo-fronts-v12.png')
exec(compile(code,__file__,'exec'))
code=code.replace('(5.0,-1.2,3.9)','(5.0,-11.8,3.9)').replace('(4.0,-13,3.8)','(5.0,0,3.8)').replace('street-photo-fronts-v12.png','street-pub-neighbours-v12.png')
exec(compile(code,__file__,'exec'))
result={'previews':['street-photo-fronts-v12.png','street-pub-neighbours-v12.png']}
