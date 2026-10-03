from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'scripts/preview_street_fronts.py').read_text().replace('street-photo-fronts-v11.png','street-photo-fronts-v13.png')
exec(compile(code,__file__,'exec'))
