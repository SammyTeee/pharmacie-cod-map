from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'scripts/preview_street_fronts.py').read_text().replace('(5.0,-1.2,3.9)','(5.5,-2.4,1.6)').replace('(4.0,-13,3.8)','(5.5,2.4,.8)').replace('camdata.lens=16','camdata.lens=24').replace('street-photo-fronts-v11.png','front-threshold-v16.png')
exec(compile(code,__file__,'exec'))
